#!/usr/bin/env python

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup

# Package meta-data.
NAME = "py ice40"
DESCRIPTION = "python tools for interacting with iCE40 chips and flash"
URL = "https://github.com/elmsfu/py-ice40"
EMAIL = "elms@freshred.net"
AUTHOR = "Elms"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = None

REQUIRED = ["python-periphery", "pylibftdi"]

EXTRAS = {
    # "spidev": ["python-periphery"], "ftdi": ["pylibftdi"]
}


here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    entry_points={"console_scripts": ["example_config=py_ice40.example_config:main"]},
    packages=find_packages(exclude=("tests",)),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: System :: Hardware",
        "Topic :: System :: Hardware :: Hardware Drivers",
    ],
    keywords="spi embedded linux beaglebone raspberrypi rpi",
)
