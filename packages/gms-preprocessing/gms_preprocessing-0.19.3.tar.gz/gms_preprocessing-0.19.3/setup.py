#!/usr/bin/env python
# -*- coding: utf-8 -*-

# gms_preprocessing, spatial and spectral homogenization of satellite remote sensing data
#
# Copyright (C) 2020  Daniel Scheffler (GFZ Potsdam, daniel.scheffler@gfz-potsdam.de)
#
# This software was developed within the context of the GeoMultiSens project funded
# by the German Federal Ministry of Education and Research
# (project grant code: 01 IS 14 010 A-C).
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
# Please note the following exception: `gms_preprocessing` depends on tqdm, which
# is distributed under the Mozilla Public Licence (MPL) v2.0 except for the files
# "tqdm/_tqdm.py", "setup.py", "README.rst", "MANIFEST.in" and ".gitignore".
# Details can be found here: https://github.com/tqdm/tqdm/blob/master/LICENCE.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
import warnings
from importlib import util

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

version = {}
with open("gms_preprocessing/version.py", encoding='utf-8') as version_file:
    exec(version_file.read(), version)

req = [
    'arosics>=1.0.0',
    'cerberus',
    'dill',
    'ephem',
    'gdal',
    'geoalchemy2',
    'geoarray>=0.9.0',
    'geopandas',
    'iso8601',
    'jsmin',
    'matplotlib',
    'natsort',
    'nested_dict',
    'numpy',
    'openpyxl',  # implicitly needed by pandas to write GMS job summaries as excel files
    'pandas',
    'psutil',
    'psycopg2',
    'pyinstrument',
    'pyorbital',
    'pyproj',
    'pyrsr>=0.3.1',
    'py_tools_ds>=0.16.3',
    'pytz',
    'redis',  # named redis on PyPI and redis-py on conda-forge
    'redis-semaphore',
    'retools',
    'scikit-learn',
    'scipy',
    'shapely',
    'sicor>=0.15.2',
    'spechomo',
    'spectral>=0.16',  # spectral<0.16  has some problems with writing signed integer 8bit data
    'sqlalchemy',
    'timeout_decorator',
    'tqdm',
    # fmask # conda install -c conda-forge python-fmask
    # 'pyhdf', # conda install --yes -c conda-forge pyhdf
]

req_setup = ['setuptools-git']  # needed for package_data version controlled by GIT

req_test = ['coverage', 'nose', 'nose2', 'nose-htmloutput', 'rednose']

req_doc = ['sphinx-autodoc-typehint', 'sphinx-argparse', 'sphinx_rtd_theme']

req_lint = ['flake8', 'pycodestyle', 'pydocstyle']

req_dev = req_setup + req_test + req_doc + req_lint

setup(
    author="Daniel Scheffler",
    author_email='daniel.scheffler@gfz-potsdam.de',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="GeoMultiSens - Scalable Multi-Sensor Analysis of Remote Sensing Data",
    extras_require={
        "doc": req_doc,
        "test": req_test,
        "lint": req_lint,
        "dev": req_dev
    },
    keywords='gms_preprocessing',
    include_package_data=True,
    install_requires=req,
    license="GPL-3.0-or-later",
    long_description=readme,
    name='gms_preprocessing',
    package_data={"gms_preprocessing": ["database/**/**/*",
                                        "options/options_default.json"]},
    package_dir={'gms_preprocessing': 'gms_preprocessing'},
    packages=find_packages(exclude=['.github', 'benchmarks', 'docs', 'examples', 'tests*']),
    scripts=["bin/run_gms.py", "bin/run_gms.sh"],
    test_suite='tests',
    tests_require=req_test,
    url='https://gitext.gfz-potsdam.de/geomultisens/gms_preprocessing',
    version=version['__version__'],
    zip_safe=False
)


# check for pyhdf
if not util.find_spec('pyhdf'):
    warnings.warn('If you have not compiled GDAL with HDF4 support you need to install pyhdf manually '
                  '(see http://pysclint.sourceforge.net/pyhdf/install.html) for processing Terra ASTER data.'
                  'It is not automatically installed.')

# check for fmask
if not util.find_spec('fmask'):
    warnings.warn("FMask library is missing. If you want to compute cloud masks via FMask, you have to install it "
                  "manually (e.g., by running 'conda install -c conda-forge python-fmask').")
