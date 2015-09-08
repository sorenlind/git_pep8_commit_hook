""" Setup script for PyPI """
from setuptools import setup, find_packages

setup(
    name='git_pep8_commit_hook',
    version='0.1.0',
    license='Apache License, Version 2.0',
    description='Git commit hook that checks Python files with pep8.',
    author='Soren Lind Kristiansen',
    author_email='soren@gutsandglory.dk',
    url='https://github.com/sorenlind/git_pep8_commit_hook',
    keywords="git commit pre-commit hook pep8 python",
    platforms=['Any'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pep8',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: Apache License, Version 2.0',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
    entry_points={
        'console_scripts': [
            'git_pep8_commit_hook=git_pep8_commit_hook:main',
        ],
    },
)
