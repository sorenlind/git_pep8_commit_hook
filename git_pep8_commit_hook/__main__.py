"""
Git pre-commit hook for checking coding style of Python code. The hook requires
pep8.

Apache License 2.0
    http://www.apache.org/licenses/LICENSE-2.0.html

LICENSE:
    MIT Licence
    https://opensource.org/licenses/MIT
"""

import sys
from .commit_hook import main


if __name__ == 'git_pep8_commit_hook':
    main()
    sys.exit(0)

sys.exit(1)
