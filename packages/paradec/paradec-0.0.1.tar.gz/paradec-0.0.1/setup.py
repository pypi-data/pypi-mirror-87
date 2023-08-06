#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 21:14:06 2020

@author: malte
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paradec", # Replace with your own username
    version="0.0.1",
    author="Malte Algren",
    author_email="malte__algren@hotmail.com",
    description="Python decorator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/malteal/paradec",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)