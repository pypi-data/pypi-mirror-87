# -*- coding: utf-8 -*-

# from distutils.core import setup
from setuptools import setup, find_packages

# read the contents of your README file
from os import path
import doctestprinter


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="doctestprinter",
    version=doctestprinter.__version__,
    author="David Scheliga",
    author_email="David.Scheliga@gmx.de",
    url="https://gitlab.com/david.scheliga/doctestprinter",
    project_urls={
        "Documentation": "https://doctestprinter.readthedocs.io/en/latest/",
        "Source Code Repository": "https://gitlab.com/david.scheliga/doctestprinter",
    },
    description="Helper methods to print readable results for doctest strings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GNU General Public License v3 (GPLv3)",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
    ],
    keywords="helper, doctest",
    python_requires=">=3.6",
    py_modules=["doctestprinter"]
)
