"""
This module contains the tests for the commit hook.
"""

from conftest import cmd, write_file
from git_pep8_commit_hook import commit_hook


class TestPep8CommitHook(object):
    """
    Test class for the pep8 commit hook.
    """
    # pylint: disable=protected-access,too-many-public-methods,no-self-use

    def test_current_commit(self, temp_repo_dir):
        """Test commit_hook._current_commit"""

        # Test empty tree
        empty_hash = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'
        assert commit_hook._current_commit() == empty_hash

        # Test after commit
        cmd(temp_repo_dir, 'git commit --allow-empty -m msg')
        assert commit_hook._current_commit() == 'HEAD'

    def test_list_of_committed_files(self, temp_repo_dir):
        """Test commit_hook._get_list_of_committed_files"""

        # Test empty tree
        assert commit_hook._get_list_of_committed_files() == []

        # Create file 'a'
        test_file = write_file(temp_repo_dir, 'a', 'foo')
        assert commit_hook._get_list_of_committed_files() == []

        # Add 'a'
        cmd(temp_repo_dir, 'git add ' + test_file)
        assert commit_hook._get_list_of_committed_files() == [test_file]

        # Commit 'a'
        cmd(temp_repo_dir, 'git commit -m msg')
        assert commit_hook._get_list_of_committed_files() == []

        # Edit 'a'
        write_file(temp_repo_dir, 'a', 'bar')
        assert commit_hook._get_list_of_committed_files() == []

        # Add 'a'
        cmd(temp_repo_dir, 'git add ' + test_file)
        assert commit_hook._get_list_of_committed_files() == [test_file]

    def test_is_python_file(self, temp_repo_dir):
        """Test commit_hook._is_python_file"""

        # Extension (py)
        test_file = write_file(temp_repo_dir, 'a.py', '')
        assert commit_hook._is_python_file(test_file)

        # Extension (txt)
        test_file = write_file(temp_repo_dir, 'a.txt', '')
        assert commit_hook._is_python_file(test_file) is False

        # Empty
        test_file = write_file(temp_repo_dir, 'b', '')
        assert commit_hook._is_python_file(test_file) is False

        # Shebang
        write_file(temp_repo_dir, 'b', '#!/usr/bin/env python')
        assert commit_hook._is_python_file(test_file)

    def test_parse_score(self):
        """Test commit_hook._parse_score"""

        text = ''
        assert commit_hook._parse_violations(text) == 0

        text = '...'
        assert commit_hook._parse_violations(text) == 1

        text = '...\n...'
        assert commit_hook._parse_violations(text) == 2
