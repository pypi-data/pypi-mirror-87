#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import sys
import setuptools
from distutils.core import Command
import subprocess
from setuptools.command.build_py import build_py

# def npm_install(args=["npm","--global", "install", "apify"]):
#     subprocess.Popen(args, shell=True)

class NPMInstall(build_py):
    def run(self):
        args=["npm","-g", "install", "apify"]
        subprocess.Popen(args, shell=True)

# class NPMInstall(build_py):
#     def run(self):
#         self.run_command('npm install -g apify')
#         build_py.run(self)


with open("Readme.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

#if sys.version_info >= (3,8):
#    sys.exit("Python version greater than 3.7 not supported because of numpy and moviepy compatibility issues with python version 3.8")

# 
# This will store node modules
print("Installing npm: ", flush=True)
node_folder_path = os.path.join(os.path.expanduser("~"), ".alternat")
if not os.path.exists(node_folder_path):
    os.mkdir(node_folder_path)
try:
    output = subprocess.check_output(["npm", "install", "apify"], cwd=node_folder_path)
except subprocess.CalledProcessError as e:
    print("\n Subprocess error")
    print(str(e.output))

# helper functions to make it easier to list dependencies not as a python list, but vertically w/ optional built-in comments to why a certain version of the dependency is listed
def cleanup(x):
    return re.sub(r" *#.*", "", x.strip())  # comments


def to_list(buffer):
    return list(filter(None, map(cleanup, buffer.splitlines())))


# normal dependencies ###
#
# these get resolved and installed via either of these two:
#
#   pip install alternat
#   pip install -e .
#
# IMPORTANT: when updating these, please make sure to sync conda/meta.yaml
dep_groups = {
    "core": to_list(
        """
        pillow
        google-cloud-vision==1.0.0
        tldextract
        easyocr
        pyyaml
        treelib
        uvicorn
        fastapi==0.62.0
        typer==0.3.2
"""
    )
}

__version__ = None # Explicitly set version.
exec(open('alternat/version.py').read()) # loads __version__

requirements = [y for x in dep_groups.values() for y in x]
setup_requirements = to_list(
    """
    pytest-runner
    setuptools>=36.2
"""
)


# test dependencies ###
test_requirements = to_list(
    """
    pytest
"""
)

#mkdir my-project
#cd my-project
#npm install bitcoinjs-lib

setuptools.setup(
    name="alternat",
    version=__version__,
    author="keplerlab",
    author_email="keplerwaasi@gmail.com",
    description="Alternat is a tool that automates alt text generation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/keplerlab/alternat.git",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Documentation": "https://alternat.readthedocs.io",
        "Source": "https://github.com/keplerlab/alternat",
        "Tracker": "https://github.com/keplerlab/alternat/issues",
    },
    cmdclass={
        'npm_install': NPMInstall
    },
    include_package_data=True,
    zip_safe=False,
)
