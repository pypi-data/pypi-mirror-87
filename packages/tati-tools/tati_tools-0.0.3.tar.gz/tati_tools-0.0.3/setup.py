#!/usr/bin/env python
# -*- coding: utf-8 -*-

# For a fully annotated version of this file and what it does, see
# https://github.com/pypa/sampleproject/blob/master/setup.py

# To upload this file to PyPI you must build it then upload it:
# python setup.py sdist bdist_wheel  # build in 'dist' folder
# python-m twine upload dist/*  # 'twine' must be installed: 'pip install twine'


import io
import os
import re
import sys
from shutil import rmtree
from typing import Tuple, List

from setuptools import Command, find_packages, setup

# Package meta-data
NAME = "tati_tools"
description = "Tools for computer vision tasks."
URL = "https://github.com/tatigabru/tati_tools"
EMAIL = "travellingtati@gmail.com"
AUTHOR = "Tati Gabru"
REQUIRES_PYTHON = ">=3.6.0"
current_dir = os.path.abspath(os.path.dirname(__file__))


def get_version():
    """Get version from __init__.py file"""
    version_file = os.path.join(current_dir, NAME, "__init__.py")
    with io.open(version_file, encoding="utf-8") as f:
        return re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read(), re.M).group(1)


# Packages are required for this module
try:
    with open(os.path.join(current_dir, "requirements.txt"), encoding="utf-8") as f:
        required = f.read().split("\n")
except FileNotFoundError:
    required = []

# What packages are optional?
extras = {"test": ["pytest"]}
version = get_version()

about = {"__version__": version}


def get_test_requirements():
    """Optional packages"""
    requirements = ["pytest", "black==19.3b0"]
    if sys.version_info < (3, 3):
        requirements.append("mock")
    return requirements


def get_long_description():
    with io.open(os.path.join(current_dir, "README.md"), encoding="utf-8") as f:
        return f.read()


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options: List[Tuple] = []

    @staticmethod
    def status(s):
        """Print things in bold."""
        print(s)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(os.path.join(current_dir, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution...")
        os.system(f"{sys.executable} setup.py sdist bdist_wheel --universal")

        self.status("Uploading the package to PyPI via Twine...")
        os.system("twine upload dist/*")

        self.status("Pushing git tags...")
        os.system("git tag v{}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


setup(
    name=NAME,
    version=version,
    author=AUTHOR,
    author_email=EMAIL,
    description=description,
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    license="License :: OSI Approved :: MIT License",
    url=URL,
    packages=find_packages(exclude=["tests", "docs", "images"]),
    install_requires=required,
    extras_require={"tests": get_test_requirements()},
    python_requires=REQUIRES_PYTHON,
    keywords=[
        "Deep Learning",
        "Machine Learning",
        "Computer Vision",
        "PyTorch",
        "Kaggle",
        "Masks",
        "Polygons",
        "Satellite Imaging",        
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    cmdclass={"upload": UploadCommand},
)