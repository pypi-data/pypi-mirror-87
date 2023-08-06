#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2020 - Rafael Guerreiro Osorio - Ipea.

pynad
"""

from setuptools import setup, find_packages

with open('README.rst', 'r') as file:
    long_description = file.read()

setup(
    name='pynad',
    version='1.0.0',
    author='Rafael Guerreiro Osorio',
    author_email='rafael.osorio@ipea.gov.br',
    description="A package to manage pnad's microdata and metadata",
    long_description=long_description,

    # homepage
    url='',

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: '
        + 'GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    packages=find_packages(),
    install_requires=['tablib', 'xlrd', 'xlwt'],

    # command line app
    entry_points={
        "console_scripts": ['pynad = pynad.pynad:main']
        })
