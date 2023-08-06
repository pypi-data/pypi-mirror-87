#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013-2020 Pytroll

# Author(s):

#   Adam Dybbroe <adam.dybbroe@smhi.se>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from setuptools import setup, find_packages
import os.path


try:
    # HACK: https://github.com/pypa/setuptools_scm/issues/190#issuecomment-351181286
    # Stop setuptools_scm from including all repository files
    import setuptools_scm.integration
    setuptools_scm.integration.find_files = lambda _: []
except ImportError:
    pass


description = ('Reading and manipulaing satellite sensor spectral responses and the '
               'solar spectrum, to perfom various corrections to VIS and NIR band data')

try:
    with open('./README', 'r') as fd:
        long_description = fd.read()
except IOError:
    long_description = ''

requires = ['docutils>=0.3', 'numpy>=1.5.1', 'scipy>=0.14',
            'python-geotiepoints>=1.1.1',
            'h5py>=2.5', 'requests', 'six', 'pyyaml',
            'appdirs']

dask_extra = ['dask[array]']
test_requires = ['pyyaml', 'dask[array]', 'xlrd', 'pytest', 'xarray']
if sys.version < '3.0':
    test_requires.append('mock')
    try:
        # This is needed in order to let the unittests pass
        # without complaining at the end on certain systems
        import multiprocessing
    except ImportError:
        pass

NAME = 'pyspectral'

setup(name=NAME,
      description=description,
      author='Adam Dybbroe',
      author_email='adam.dybbroe@smhi.se',
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU General Public License v3 ' +
                   'or later (GPLv3+)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering'],
      url='https://github.com/pytroll/pyspectral',
      long_description=long_description,
      license='GPLv3',

      packages=find_packages(),
      include_package_data=True,
      package_data={
          # If any package contains *.txt files, include them:
          '': ['*.txt', '*.det'],
          'pyspectral': [os.path.join('etc', 'pyspectral.yaml'),
                         os.path.join('data', '*.dat'),
                         os.path.join('data', '*.XLS'),
                         'data/modis/terra/Reference_RSR_Dataset/*.det'],

      },

      # Project should use reStructuredText, so ensure that the docutils get
      # installed or upgraded on the target machine
      install_requires=requires,
      extras_require={'xlrd': ['xlrd'], 'trollsift': ['trollsift'],
                      'matplotlib': ['matplotlib'],
                      'pandas': ['pandas'],
                      'tqdm': ['tqdm'],
                      'dask': dask_extra},
      scripts=['bin/plot_rsr.py', 'bin/composite_rsr_plot.py',
               'bin/download_atm_correction_luts.py',
               'bin/download_rsr.py'],
      data_files=[('share', ['pyspectral/data/e490_00a.dat',
                             'pyspectral/data/MSG_SEVIRI_Spectral_Response_Characterisation.XLS'])],
      test_suite='pyspectral.tests.suite',
      tests_require=test_requires,
      python_requires='>=3.7',
      zip_safe=False,
      use_scm_version=True
      )
