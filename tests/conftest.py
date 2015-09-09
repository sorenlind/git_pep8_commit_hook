"""Shared text fixtures and functions"""

from __future__ import print_function
import pytest
import tempfile
import os
import subprocess
import shutil


@pytest.fixture()
def temp_repo_dir(request):
    """"Create test directory and repo. Delete when test function completes."""
    # Create temporary directory
    tmp_dir = tempfile.mkdtemp(prefix='pep8_hook_test_')

    # Set current working directory to the temporary directory for
    # all the commands run in the test
    os.chdir(tmp_dir)

    # Initialize temporary git repository
    cmd(tmp_dir, 'git init')

    def remove_temp_repo_dir():
        """Delete directory when test function."""
        print ("remove repository")
        shutil.rmtree(tmp_dir)

    request.addfinalizer(remove_temp_repo_dir)

    return tmp_dir


def cmd(current_working_directory, args):
    """Run command in specified directory."""
    return subprocess.check_output(args.split(), cwd=current_working_directory)


def write_file(current_working_directory, filename, contents):
    """Write file with specified contents in specified directory."""
    with open(os.path.join(current_working_directory, filename), 'w') as wfile:
        wfile.write(contents)
    return filename
