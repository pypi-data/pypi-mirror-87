#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import allo

setup(
    name='allo-client',
    version=allo.__version__,
    author="Lukas Hameury",
    author_email="lukas.hameury@libriciel.coop",
    description="Libriciel upgrade package",
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.libriciel.fr/libriciel/projets-internes/allo/allo-client",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyInquirer',
        'requests>=2.16.0',
        'gitpython',
        'PyYAML',
        'progressbar2',
        'jsons',
        'ansible',
        'click',
        'urllib3'
    ],
    entry_points={
        'console_scripts': [
            'allo = allo.cmd:cmd'
        ],
    },
)
