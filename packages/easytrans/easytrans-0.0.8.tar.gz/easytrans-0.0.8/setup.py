#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com

import setuptools

with open("easytrans/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easytrans",
    version="0.0.8",
    author="Frank YCJ",
    author_email="1320259466@qq.com",
    description="The easytrans makes the file transfer simpler!",
    keywords='file format transfer word doc pdf png jpg txt convert',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YouAreOnlyOne",
    # packages=setuptools.find_packages(),
    packages=["easytrans"],
    install_requires=["fitz>=0.0.1.dev2", "PyMuPDF>1.0.0", "python-docx>0.5.0", "openpyxl>=3.0.5", "Pillow>=8.0.1"],
    # python_requires=">=2.4",
    license="Apache 2.0 license",
    Platform="OS All",

    project_urls={
        "Bug Tracker": "https://github.com/YouAreOnlyOne/FastFrameJar/issues",
        "Documentation": "https://github.com/YouAreOnlyOne/FastFrameJar",
        "Source Code": "https://github.com/YouAreOnlyOne/FastFrameJar",
    },

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "easytrans": ["README"],
        "easytrans": ["README.md"],
        "": ["README.md"],
        "easytrans/doc": ["*.md", "*"],
        "easytrans/res": ["*.docx", "*.doc", "*.xls", "*.xlsx", "*"],
        "easytrans": ["LICENSE"],
    },
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
