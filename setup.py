#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), "r") as f:
        return f.read()


setup(
    name="liquidcrystal",
    version="0.1",
    author="Davide Depau",
    author_email="apps@davideddu.org",
    description="A Python port of Arduino's LiquidCrystal library that uses PyWiring to access an HD44780-based LCD "
                "display through any supported I/O port.",
    license="GPLv2",
    keywords="lcd pywiring i2c gpio parallel serial liquidcrystal display",
    url="http://github.com/Davidedd/python-liquidcrystal",
    packages=['liquidcrystal'],
    long_description=read('README.md'),
    requires=["pywiring", "numpy"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Programming Language :: Python",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
)
