# /usr/bin/env python

# This file is part of error404.

# error404 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# error404 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with error404.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="error404",
    version="1.1.8-alpha.0",
    description="Colourful tests for Python!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="harens",
    license="GPLv3",
    zip_safe=False,
    package_data={"error404": ["py.typed"]},
    packages=find_packages(exclude=("tests",)),
    author_email="harensdeveloper@gmail.com",
    url="https://harens.github.io",
    download_url="https://github.com/harens/error404/archive/master.zip",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Typing :: Typed",
    ],
    project_urls={
        "Source": "https://github.com/harens/error404",
        "Tracker": "https://github.com/harens/error404/issues",
    },
    keywords="tests, emoji",
)
