""" Setup script for PyPI """
import re
from setuptools import setup, find_packages
from distutils.core import setup, Command


class PyTest(Command):
    """Setup class for pytest."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call([sys.executable, "runtests.py"])
        raise SystemExit(errno)

VERSION = re.search(
    r'^VERSION\s*=\s*"(.*)"',
    open("git_pep8_commit_hook/commit_hook.py").read(),
    re.M
    ).group(1)

setup(
    name="git_pep8_commit_hook",
    version=VERSION,
    license="Apache License, Version 2.0",
    description="Git commit hook that checks Python files with pep8.",
    author="Soren Lind Kristiansen",
    author_email="soren@gutsandglory.dk",
    url="https://github.com/sorenlind/git_pep8_commit_hook",
    keywords="git commit pre-commit hook pep8 python",
    platforms=["Any"],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "pep8",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: Apache License, Version 2.0",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        "console_scripts": [
            "git_pep8_commit_hook = git_pep8_commit_hook.commit_hook:main",
        ],
    },
    cmdclass={"test": PyTest},
)
