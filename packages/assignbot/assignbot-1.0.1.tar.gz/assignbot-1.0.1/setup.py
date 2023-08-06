#!/usr/bin/env python
#
# copyright 2020-2020 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of assignbot.
#
# Assignbot is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# Assignbot is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with assignbot.  If not, see <http://www.gnu.org/licenses/>.

"""The setup script."""

from setuptools import setup, find_packages

requirements = ["python-gitlab", "pyyaml", "pandas", "boto3"]
setup_requirements = []
test_requirements = []

with open("README.rst") as fobj:
    long_description = fobj.read()


setup(
    name="assignbot",
    author="Logilab",
    author_email="contact@logilab.fr",
    version="1.0.1",
    licence="LGPL",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Automatically assign review on gitlab/heptapod",
    long_description=long_description,
    entry_points={"console_scripts": ["assignbot=assignbot.__main__:main"]},
    install_requires=requirements,
    include_package_data=True,
    packages=find_packages(exclude=["test"]),
    setup_requires=setup_requirements,
    url="https://forge.extranet.logilab.fr/open-source/assignbot",
    zip_safe=False,
)
