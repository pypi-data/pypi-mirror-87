#!/usr/bin/env python3
#
# Copyright (C) 2019-2020 Cochise Ruhulessin
#
# This file is part of unimatrix.
#
# unimatrix is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# unimatrix is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with unimatrix.  If not, see <https://www.gnu.org/licenses/>.
from setuptools import find_namespace_packages
from setuptools import setup


version = str.strip(open('unimatrix/VERSION').read())
requirements = str.split(open('requirements.txt').read(), '\n')

setup(
    name='unimatrix',
    version=version,
    description='Unimatrix One Core Library',
    author='Cochise Ruhulessin',
    author_email='cochise.ruhulessin@digitalcitizen.nl',
    url='https://gitlab.com/unimatrixone/libraries/python-unimatrix',
    install_requires=list(filter(bool, requirements)),
    packages=find_namespace_packages(),
    include_package_data=True,
    license="GPLv3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Clustering",
        "Topic :: System :: Distributed Computing"
    ]
)
