#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import division, print_function

from setuptools import setup, find_packages

setup(
    name="kflash",
    py_modules=["kflash"],
    version="1.0.2",
    description=("Kendryte UART ISP Utility - programming code to k210"),
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    author="https://github.com/vowstar/kflash.py/graphs/contributors",
    author_email="vowstar@gmail.com",
    maintainer="Huang Rui",
    maintainer_email="vowstar@gmail.com",
    license="MIT License",
    packages=find_packages(),
    platforms=["all"],
    url="https://github.com/vowstar/kflash.py",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Embedded Systems",
    ],
    install_requires=[
        "pyserial>=3.4",
        "pyelftools>=0.25",
        "backports.tempfile>=1.0",
    ],
    entry_points={
        "console_scripts": [
            "kflash = kflash:main",
        ]
    },
)
