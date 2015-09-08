"""
Git pre-commit hook for checking coding style of Python code. The hook requires
pep8.

Apache License 2.0
    http://www.apache.org/licenses/LICENSE-2.0.html

LICENSE:
    MIT Licence
    https://opensource.org/licenses/MIT
"""

from __future__ import print_function
import argparse
import sys
from git_pep8_commit_hook import commit_hook

VERSION = '0.1.0'


def main():
    """ Main function handling configuration files etc """
    parser = argparse.ArgumentParser(
        description='Git pep8 commit hook')
    parser.add_argument(
        '--max-violations-per-file',
        default=0,
        type=int,
        help=(
            'Maximum number of violations. Files with a highter violation '
            'count will stop the commit. Default: 0'))
    parser.add_argument(
        '--pep8',
        default='pep8',
        help='Path to pep8 executable. Default: pep8')
    parser.add_argument(
        '--config',
        default='setup.cfg',
        help=(
            'Path to pep8 config file file. Options in the config will '
            'override the command line parameters. Default: setup.cfg'))
    parser.add_argument(
        '--pep8-params',
        help='Custom pep8 parameters to add to the pep8 command')
    parser.add_argument(
        '--version',
        action='store_true',
        help='Print current version number')
    args = parser.parse_args()

    if args.version:
        print('git_pep8_commit_hook version {}'.format(VERSION))
        sys.exit(0)

    result = commit_hook.check_repo(
        args.max_violations_per_file, args.pep8, args.config, args.pep8_params)

    if result:
        sys.exit(0)
    sys.exit(1)

if __name__ == 'git_pep8_commit_hook':
    main()
    sys.exit(0)

sys.exit(1)
