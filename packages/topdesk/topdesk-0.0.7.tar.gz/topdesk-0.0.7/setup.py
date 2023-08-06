#!/usr/bin/env python
import os
from setuptools import setup, find_packages

with open('README.md', encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='topdesk',
    author='Veit Heller',
    version='0.0.7',
    license='GPLv3',
    url='https://gitlab.com/wobcom/topdesk',
    description='A modern TOPdesk wrapper for Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages('.'),
    install_requires=[
        "requests>=2.22.0",
    ]
)

