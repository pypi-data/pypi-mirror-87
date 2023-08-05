#!/usr/bin/env python

from setuptools import setup

# note: this is a repeat of the README, to evolve, good enough for now.
long_desc = """
Contributors welcome, either adding new functionality or fixing bugs.

See also: https://msdn.microsoft.com/en-us/library/bb417343.aspx
"""

setup(
    name="cabarchive",
    version="0.2.3",
    license="LGPL-2.1-or-later",
    description="A pure-python library for creating and extracting cab files",
    long_description=long_desc,
    author="Richard Hughes",
    author_email="richard@hughsie.com",
    url="https://github.com/hughsie/python-cabarchive",
    packages=[
        "cabarchive",
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
        "Topic :: System :: Archiving",
    ],
    keywords=["cabextract", "cab", "archive", "extract"],
    package_data={
        "cabarchive": [
            "py.typed",
            "archive.pyi",
            "errors.pyi",
            "file.pyi",
            "parser.pyi",
            "utils.pyi",
            "writer.pyi",
            "__init__.pyi",
        ]
    },
)
