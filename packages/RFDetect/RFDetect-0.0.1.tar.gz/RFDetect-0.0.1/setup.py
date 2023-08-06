
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 11:17:34 2020

"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RFDetect", 
    version="0.0.1",
    author="Chen",
    author_email="chen.rui@northeastern.edu",
    description="a python package to use Random Forest module to detect XSS.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.ccs.neu.edu/Capstone-Team/RandomForest",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #python_requires='>=3.6',
)