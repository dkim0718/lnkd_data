#!/usr/bin/env python

from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import os
import sys

# import `

here = os.path.abspath(os.path.dirname(__file__))

def readme():
    with open('README.md') as f:
        return f.read()

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding','utf-8')
    sep = kwargs.get('sep','\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

# long_description = read('README.txt','CHANGES.txt')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='lnkd_tools',
    # version=lnkd_tools.__version__,
    version='0.1',
    url='https://github.com/dkim0718/lnkd_tools',
    license='MIT',
    author='Do Yoon Kim',
    # tests_require=['pytest'],
    install_requires=[
        'pandas',
                    ],
    # cmdclass={'test': PyTest},
    author_email='dkim0718@gmail.com',
    description='Convenience tools for working with LinkedIn data',
    # long_description=long_description,
    long_description=readme(),
    packages=['lnkd_tools'],
    zip_safe=False,
    # include_package_data=True,
    # platforms='any',
    # test_suite='sandman.test.test_sandman',
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers = [
        'Programming Language :: Python 2.7',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        # 'Environment :: Web Environment',
        # 'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        # 'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Utilities',
        # 'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    # scripts=['bin/lnkd-test'],
    entry_points ={
        'console_scripts': ['finniest-joke=lnkd_tools.command_line:main'],
    },
    include_package_data=True
    # extras_require={
    #     'testing': ['pytest'],
    # }
)