#!/usr/bin/env python
## https://packaging.python.org/tutorials/packaging-projects/#creating-setup-py
import typing
import os

from setuptools import setup
from setuptools import find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

tests_requirements = [
    'pytest',
    'pytest-runner',
    'mock;python_version<="3.3"',
    'flake8',
    'autopep8',
    'pylint',
]

setup(
    name='webapp',
    version='0.0.1',
    description='Webapp',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    package_data={
        '': ['*.html', ]
    },
    install_requires=[
        'typing;python_version<"3.5"',
        'flask==1.1.1',
        'fastjsonschema',
    ],
    extras_require={
        'gunicorn': [
            'gunicorn',
        ],
        'tests': tests_requirements,
    },
    dependency_links=[
    ],
    setup_requires=[
    ],
    tests_require=tests_requirements,
    test_suite='tests',
)
