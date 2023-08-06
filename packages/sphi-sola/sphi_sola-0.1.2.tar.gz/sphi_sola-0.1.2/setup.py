#!/usr/bin/env python

import codecs
from setuptools import setup

# create disttribution with `python setup.py sdist`

# Version info -- read without importing
_locals = {}
with open("sphi_sola/_version.py") as hndl:
    exec(hndl.read(), None, _locals)
version = _locals["__version__"]


desc = ''

with codecs.open("README.rst", encoding="utf-8") as hndl:
    desc += hndl.read()

with codecs.open("HISTORY.rst", encoding="utf-8") as hndl:
    desc += '\n\n\n'
    desc += hndl.read()

setup(
    name="sphi_sola",
    version=version,
    description="Sphinx theme based on Solarized colour scheme.",
    long_description=desc,
    author="Matthias Stein",
    author_email="git.matthias@gmail.com",
    packages=[
        "sphi_sola"
    ],
    include_package_data=True,
    url="https://github.com/matthias-stein/sphi_sola",
    entry_points={
        "sphinx.html_themes": [
            "sphi_sola = sphi_sola"
        ]
    },
    install_requires=[
        'sphinx>=1.6',
        'pygments-style-solarized==0.1.1'
    ]
)
