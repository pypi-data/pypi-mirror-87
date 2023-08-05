#!/usr/bin/env python

import os
import re
import sys

from setuptools import find_packages, setup


def read(*parts):
    """Read file."""
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)
    sys.stdout.write(filename)
    with open(filename, encoding="utf-8", mode="rt") as fp:
        return fp.read()


def get_version():
    """Get current version from code."""
    regex = r"__version__\s=\s\"(?P<version>[\d\.]+?)\""
    path = ("aqman", "__version__.py")
    return re.search(regex, read(*path)).group("version")


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="python-aqman",  # Replace with your own username
    version=get_version(),
    author="Hosung Kim",
    author_email="samhskim1@gmail.com",
    description="Asynchronous Python Client for Radon FTLabs AQMAN101",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hkder/python-aqman",
    include_package_data=True,
    install_requires=["aiohttp>=3.0.0", "attrs>=19.0.0", "yarl>=1.0.0"],
    license="MIT license",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    zip_safe=False,
)
