#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-tspwplib',
    author="Patrick O'Hara",
    author_email='pohara@turing.ac.uk',
    maintainer="Patrick O'Hara",
    maintainer_email='pohara@turing.ac.uk',
    license='MIT',
    url='https://github.com/PatrickOHara/pytest-tspwplib',
    description='A simple plugin to use with tspwplib',
    long_description="",
    py_modules=['pytest_tspwplib'],
    python_requires='>=3.6',
    install_requires=[
        "tspwplib",
        "pytest>=3.5.0",
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'tspwplib = pytest_tspwplib',
        ],
    },
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
)
