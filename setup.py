#!/usr/bin/env python3

from setuptools import setup, find_packages

description = "Python class for Elechouse Voice Recognition Module V3"

setup(name = 'PyVoiceRecognitionV3',
    packages = find_packages(),
    license = "GPLv3",
    description = description,
    author = "Jan Grosser",
    keywords = ["Voice Recognition"],
    install_requires = [ ],
    # See: https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/
    extras_require = {
        # Install: pip install -e ".[testing]"
        'testing': [ ],
        }
    )

