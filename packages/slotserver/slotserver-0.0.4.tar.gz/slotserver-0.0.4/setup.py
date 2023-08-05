# Copyright (c) 2020 Hugh Wade
# SPDX-License-Identifier: MIT
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slotserver",
    version="0.0.4",
    author="Hugh Wade",
    author_email="hugh@hdub.io",
    description="IOT Dashboard data relay",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/h-dub/slotserver",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
