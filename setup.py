#!/bin/sh
# it's a kind of magic to run python with -B key
# https://stackoverflow.com/questions/17458528/why-does-this-snippet-with-a-shebang-bin-sh-and-exec-python-inside-4-single-q
''''exec python3 -B -- "$0" ${1+"$@"} # '''

import os
import re
import setuptools
import setuptools.command.test
import sys


base_path = os.path.dirname(__file__)

with open(os.path.join(base_path, 'src', 's2e2', '__init__.py')) as f:
    version = re.compile(r""".*__version__ = ["'](.*?)['"]""", re.S).match(f.read()).group(1)

with open(os.path.join(base_path, 'README.rst')) as f:
    readme = f.read()


class PyTest(setuptools.command.test.test):
    def initialize_options(self):
        setuptools.command.test.test.initialize_options(self)

    def run_tests(self):
        import pytest
        errno = pytest.main(['-v', '-p', 'no:cacheprovider'])
        sys.exit(errno)


setuptools.setup(
    name='s2e2',
    version=version,
    description='Simple String Expression Evaluator library',
    long_description=readme,
    keywords='expression-evaluator string-expression',

    author='Mikhail Zinin',
    author_email='mzinin@gmail.com',
    url='https://github.com/mzinin/s2e2.python',
    license='MIT',

    packages=['s2e2', 's2e2.functions', 's2e2.operators' ],
    package_data={'': ['README.rst']},
    package_dir={'': 'src'},

    python_requires='>=3.4',
    tests_require=['pytest', 'mock'],
    test_suite='test',
    cmdclass = {'test': PyTest},

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Topic :: Software Development :: Libraries",
    ],
)
