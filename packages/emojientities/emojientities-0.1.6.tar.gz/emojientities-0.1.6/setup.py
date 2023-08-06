#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools
import versioneer


with open("README.md") as f:
    longDescription = f.read()

with open("requirements.txt") as f:
    requirements = f.read()

setuptools.setup(
    name="emojientities",
    version=versioneer.get_version(),
    author="Christoph Fink",
    author_email="christoph@christophfink.com",
    description="provides `string.emojis` (all emoji chars from unicode.org)",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/christoph.fink/python-emojientities",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    cmdclass=versioneer.get_cmdclass(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    license="GPLv3",
)
