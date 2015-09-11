git\_pep8\_commit\_hook
=======================

|Build Status|

Git pre-commit hook for checking coding style of Python code. The hook
requires pep8. It will check files with the ``.py`` extension and files
that contain ``#!`` (shebang) and ``python`` in the first line. Heavily
inspired by and partly based on `git-pylint-commit-hook`_ by Sebastian
Dahlgren.

Since ``pep8`` itself, by default, looks for a ``setup.cfg`` file in the
repository root directory, so does this script. The script works without
the ``setup.cfg`` file. The options for the script can either be placed
in the ``[pep8_pre_commit_hook]`` section of the configuration file or
be passed as command line parameters. If the same option is specified in
both the configuration file and the parameters, the configuration file
takes precedence.

Installation
------------

Install via PyPI

::

  pip install git_pep8_commit_hook

Usage
-----

Having installed the script, if you add it to your ``pre-commit`` file
which should be placed in the ``hooks`` subfolder for the Git folder
(usually ``.git/hooks``), it will be called automatically when you run
``git commit``. If you want to skip the checks for a certain commit, you
can add the ``-n`` flag and run ``git commit -n``.

Configuration
~~~~~~~~~~~~~

By default, the script looks for a ``setup.cfg`` in the root directory
of your repository. If the script does not find a configuration file, it
uses default settings. The file might look like this:

::

  [pep8]
  ignore = E226,E302,E41
  max-line-length = 79

  [pep8_pre_commit_hook]
  max-violations-per-file = 5

The ``[pep8]`` section is used by pep8. The ``[pep8_pre_commit_hook]``
section is used by the commit hook script. You may specify the following
options:

-  **pep8-command** is for the actual command, for instance if pep8 is
   not installed globally, but is in a virtualenv inside the project
   itself.

-  **pep8-params** lets you pass custom parameters to pep8

-  **max-violations-per-file** lets you specify how many violations of
   the PEP 0008 standard you are willing to accept for any file. If at
   least one file has more than the specified number of violations, the
   commit will be blocked. The default value is 0.

Alternatively you can pass the above directly to the commit hook script
as arguments. In addition to the above, you can also pass the following
arguments to the script:

-  **config** lets you specify an alternative config file for both pep8
   itself and the commit hook script.

-  **version** displays the current version of the commit hook script.

-  **help** displays a help message explaining the arguments.

Running tests
-------------

The tests are written using ``pytest``. You can run the tests without
installing pytest and without installing the script by typing
``python runtests.py``. Alternatively, you can install pytest by running
\`pip install pyte

.. _git-pylint-commit-hook: https://github.com/sebdah/git-pylint-commit-hook

.. |Build Status| image:: https://travis-ci.org/sorenlind/git_pep8_commit_hook.svg?branch=master
   :target: https://travis-ci.org/sorenlind/git_pep8_commit_hook