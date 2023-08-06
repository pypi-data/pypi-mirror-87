# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 12:16:50 2019

@author: Soumitra
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="soumi",
    version="1.1.0",
    author="Soumitra Mandal",
    author_email="soumitramandal1999@gmail.com",
    description="A small package to help with simple mathematical operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Soumitra-Mandal/python-packaging",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
