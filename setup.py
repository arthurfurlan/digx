#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

import pypandoc
from setuptools import find_packages, setup

# package variables
package = 'digx'
readme = pypandoc.convert('README.md', 'rst')

# dynamic package info
init_py = open(os.path.join(package, '__init__.py')).read()
version = re.search(
    "^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)
author = re.search(
    "^__author__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)
email = re.search(
    "^__email__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)

setup(
    name=package,
    version='1.0.0',
    description='Dig eXtended',
    long_description=readme,
    author=author,
    author_email=email,
    url='https://github.com/arthurfurlan/digx',
    packages=find_packages(),
    install_requires=['dnspython'],
    entry_points={
        'console_scripts': [
            'digx=digx.digx:cli',
        ],
    },
    license="GPL2",
    keywords=['dns', 'cli', 'dig'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
    ],
)
