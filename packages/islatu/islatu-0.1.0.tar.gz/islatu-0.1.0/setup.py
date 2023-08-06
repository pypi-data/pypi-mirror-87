#! /usr/bin/env python
"""
setup.py for islatu

@author: Andrew R. McCluskey (andrew.mccluskey@diamond.ac.uk)
"""

# System imports
import io
from os import path
from setuptools import setup, find_packages
import islatu

PACKAGES = find_packages()

# versioning
VERSION = islatu.__version__


THIS_DIRECTORY = path.abspath(path.dirname(__file__))
with io.open(path.join(THIS_DIRECTORY, 'README.md')) as f:
    LONG_DESCRIPTION = f.read()

INFO = {
        'name': 'islatu',
        'description': 'X-ray reflectometry reduction in Python.',
        'author': 'Andrew R. McCluskey',
        'author_email': 'andrew.mccluskey@diamond.ac.uk ',
        'packages': PACKAGES,
        'include_package_data': True,
        'setup_requires': ['cython', 'numpy', 'scipy', 'uncertainties', 'pillow', 'pandas'],
        'install_requires': ['cython', 'numpy', 'scipy', 'uncertainties', 'pillow', 'pandas'],
        'version': VERSION,
        'license': 'MIT',
        'long_description': LONG_DESCRIPTION,
        'long_description_content_type': 'text/markdown',
        'classifiers': ['Development Status :: 2 - Pre-Alpha',
                        'Intended Audience :: Science/Research',
                        'License :: OSI Approved :: MIT License',
                        'Natural Language :: English',
                        'Operating System :: OS Independent',
                        'Programming Language :: Python :: 3.5',
                        'Programming Language :: Python :: 3.6',
                        'Programming Language :: Python :: 3.7',
                        'Programming Language :: Python :: 3.8',
                        'Programming Language :: Python :: 3.9',
                        'Topic :: Scientific/Engineering',
                        'Topic :: Scientific/Engineering :: Chemistry',
                        'Topic :: Scientific/Engineering :: Physics']
        }

####################################################################
# this is where setup starts
####################################################################


def setup_package():
    """
    Runs package setup
    """
    setup(**INFO)


if __name__ == '__main__':
    setup_package()
