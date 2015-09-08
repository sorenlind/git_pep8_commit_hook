""" Commit hook for pep8 """

from __future__ import print_function

import os
import sys
import subprocess
import collections
import ConfigParser


ExecutionConfig = collections.namedtuple(
    'ExecutionConfig',
    'pep8, max_violations_per_file, stderr'
)

ExecutionResult = collections.namedtuple(
    'ExecutionResult',
    'status, stdout, stderr'
)


def _execute(cmd):
    """ Executes specified command """
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    status = process.poll()
    return ExecutionResult(status, stdout, stderr)


def _current_commit():
    """ Returns the current commit. """
    if _execute('git rev-parse --verify HEAD'.split()).status:
        return '4b825dc642cb6eb9a060e54bf8d69288fbee4904'
    else:
        return 'HEAD'


def _get_list_of_committed_files():
    """ Returns a list of files about to be commited. """
    files = []

    diff_index_cmd = 'git diff-index --cached %s' % _current_commit()
    output = subprocess.check_output(
        diff_index_cmd.split()
    )
    for result in output.split('\n'):
        if result != '':
            result = result.split()
            if result[4] in ['A', 'M']:
                files.append(result[5])

    return files


def _is_python_file(filename):
    """Check if the input file looks like a Python script

    Returns True if the filename ends in ".py" or if the first line
    contains "python" and "#!", returns False otherwise.

    """
    if filename.endswith('.py'):
        return True
    else:
        with open(filename, 'r') as file_handle:
            first_line = file_handle.readline()
        return 'python' in first_line and '#!' in first_line


def _parse_violations(pep8_output):
    """ Parse the pep8 output and count the number of violations. """
    return len(pep8_output.splitlines())


def check_repo(
        max_violations_per_file,
        pep8='pep8',
        config='setup.cfg',
        pep8_params=None):
    """ Main function doing the checks

    :type max_violations_per_file: int
    :param max_violations_per_file: Max violations per file to pass the commit
    :type pep8: str
    :param pep8: Path to pep8 executable
    :type config: str
    :param config: Path to config file
    :type pep8_params: str
    :param pep8_params: Custom pep8 parameters to add to the pep8 command
    """
    # List of checked files and their results
    python_files = []

    # Find Python files
    for filename in _get_list_of_committed_files():
        try:
            if _is_python_file(filename):
                python_files.append((filename))
        except IOError:
            print('File not found (probably deleted): {}\t\tSKIPPED'.format(
                filename))

    # Don't do anything if there are no Python files
    if len(python_files) == 0:
        sys.exit(0)

    # Load any pre-commit-hooks options from a setup.cfg file (if there is one)
    if os.path.exists(config):
        conf = ConfigParser.SafeConfigParser()
        conf.read(config)
        if conf.has_option('pep8-pre-commit-hook', 'command'):
            pep8 = conf.get('pep8-pre-commit-hook', 'command')
        if conf.has_option('pep8-pre-commit-hook', 'params'):
            pep8_params += ' ' + conf.get('pep8-pre-commit-hook', 'params')
        if conf.has_option('pep8-pre-commit-hook', 'max-violations-per-file'):
            max_violations_per_file = int(conf.get(
                'pep8-pre-commit-hook', 'max-violations-per-file'))

    # Set the exit code
    return check_files(
        python_files, pep8, config, pep8_params, max_violations_per_file)


def check_files(
        python_files, pep8, config, pep8_params, max_violations_per_file):
    """ Checks specified files using pep8 """
    all_filed_passed = True

    i = 1
    for python_file in python_files:

        # Start pep8ing
        sys.stdout.write("Running pep8 on {} (file {}/{})..\t".format(
            python_file, i, len(python_files)))
        sys.stdout.flush()
        try:
            command = [pep8]

            if pep8_params:
                command += pep8_params.split()
                if '--config' not in pep8_params:
                    command.append('--config={}'.format(config))
            else:
                command.append('--config={}'.format(config))

            command.append(python_file)

            proc = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            out, _ = proc.communicate()
        except OSError:
            print("\nAn error occurred. Is pep8 installed?")
            sys.exit(1)

        # Verify the violation count
        violations = _parse_violations(out)
        if violations <= int(max_violations_per_file):
            status = 'PASSED'
        else:
            status = 'FAILED'
            all_filed_passed = False

        # Add some output
        print('{} violations (max {}) - {}'.format(
            violations, max_violations_per_file, status))
        if 'FAILED' in status:
            print(out)

        # Increment parsed files
        i += 1

    return all_filed_passed
