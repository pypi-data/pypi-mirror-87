#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2020 Pytroll developers
#
# Author(s):
#
#   Adam.Dybbroe <a000680@c20671.ad.smhi.se>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Unit testing the generic rsr hdf5 reader."""

import sys
import os.path
import numpy as np
import xarray as xr
import pytest
from pyspectral.rsr_reader import RelativeSpectralResponse
from pyspectral.utils import WAVE_NUMBER
from pyspectral.utils import RSR_DATA_VERSION
from pyspectral.tests.unittest_helpers import assertNumpyArraysEqual


if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

if sys.version_info < (3,):
    from mock import patch
else:
    from unittest.mock import patch

TEST_RSR = {'20': {}, }
TEST_RSR['20']['det-1'] = {}
TEST_RSR['20']['det-1']['central_wavelength'] = 3.75
TEST_RSR['20']['det-1']['wavelength'] = np.array([
    3.6123999, 3.6163599, 3.6264927, 3.6363862, 3.646468,
    3.6564937, 3.6664478, 3.6765388, 3.6865413, 3.6964585,
    3.7065142, 3.716509, 3.7264658, 3.7364102, 3.7463682,
    3.7563652, 3.7664226, 3.7763396, 3.7863384, 3.7964207,
    3.8063589, 3.8163606, 3.8264089, 3.8364836, 3.8463381,
    3.8563975, 3.8664163, 3.8763755, 3.8864797, 3.8964978,
    3.9064275, 3.9164873, 3.9264729, 3.9364026, 3.9465107,
    3.9535347], dtype='float32')

TEST_RSR['20']['det-1']['response'] = np.array([
    0.01, 0.0118, 0.01987, 0.03226, 0.05028, 0.0849,
    0.16645, 0.33792, 0.59106, 0.81815, 0.96077, 0.92855,
    0.86008, 0.8661, 0.87697, 0.85412, 0.88922, 0.9541,
    0.95687, 0.91037, 0.91058, 0.94256, 0.94719, 0.94808,
    1., 0.92676, 0.67429, 0.44715, 0.27762, 0.14852,
    0.07141, 0.04151, 0.02925, 0.02085, 0.01414, 0.01], dtype='float32')

TEST_RSR2 = {'20': {}, }
TEST_RSR2['20']['det-1'] = {}
TEST_RSR2['20']['det-1']['central_wavelength'] = 3.75
TEST_RSR2['20']['det-1']['wavelength'] = TEST_RSR['20']['det-1']['wavelength'].copy()
TEST_RSR2['20']['det-1']['response'] = TEST_RSR['20']['det-1']['response'].copy()

RESULT_WVN_RSR = np.array([2529.38232422,  2533.8840332,  2540.390625,  2546.81494141,
                           2553.30859375,  2559.88378906,  2566.40722656,  2573.02270508,
                           2579.72949219,  2586.37451172,  2593.09375,  2599.87548828,
                           2606.55371094,  2613.41674805,  2620.29760742,  2627.18286133,
                           2634.06005859,  2641.07421875,  2648.06713867,  2655.03930664,
                           2662.14794922,  2669.25170898,  2676.36572266,  2683.50805664,
                           2690.69702148,  2697.95288086,  2705.29199219,  2712.56982422,
                           2719.94970703,  2727.43554688,  2734.8605957,  2742.37988281,
                           2749.9831543,  2757.48510742,  2765.21142578,  2768.24291992], dtype=np.float32)

DIR_PATH_ITEMS = ['test', 'path', 'to', 'rsr', 'data']
TEST_CONFIG = {}

TEST_RSR_DIR = os.path.join(*DIR_PATH_ITEMS)
TEST_CONFIG['rsr_dir'] = TEST_RSR_DIR


class TestRsrReader(unittest.TestCase):
    """Class for testing pyspectral.rsr_reader."""

    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse.load')
    @patch('pyspectral.rsr_reader.download_rsr')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._get_rsr_data_version')
    def test_rsr_response(self, get_rsr_version, download_rsr, load, isfile, exists):
        """Test the RelativeSpectralResponse class initialisation."""
        load.return_code = None
        download_rsr.return_code = None
        isfile.return_code = True
        exists.return_code = True
        get_rsr_version.return_code = RSR_DATA_VERSION

        with patch('pyspectral.rsr_reader.get_config', return_value=TEST_CONFIG):
            with self.assertRaises(AttributeError):
                test_rsr = RelativeSpectralResponse('GOES-16')
                test_rsr = RelativeSpectralResponse(instrument='ABI')

            test_rsr = RelativeSpectralResponse('GOES-16', 'AbI')
            self.assertEqual(test_rsr.platform_name, 'GOES-16')
            self.assertEqual(test_rsr.instrument, 'abi')
            test_rsr = RelativeSpectralResponse('GOES-16', 'ABI')
            self.assertEqual(test_rsr.instrument, 'abi')

        with patch('pyspectral.rsr_reader.get_config', return_value=TEST_CONFIG):
            test_rsr = RelativeSpectralResponse('GOES-16', 'abi')

        self.assertEqual(test_rsr.platform_name, 'GOES-16')
        self.assertEqual(test_rsr.instrument, 'abi')
        self.assertEqual(
            test_rsr.filename, os.path.join(TEST_RSR_DIR, 'rsr_abi_GOES-16.h5'))

        with patch('pyspectral.rsr_reader.get_config', return_value=TEST_CONFIG):
            test_rsr = RelativeSpectralResponse(
                filename=os.path.join(TEST_RSR_DIR, 'rsr_abi_GOES-16.h5'))

        self.assertEqual(
            test_rsr.filename, os.path.join(TEST_RSR_DIR, 'rsr_abi_GOES-16.h5'))

    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse.load')
    @patch('pyspectral.rsr_reader.download_rsr')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._get_rsr_data_version')
    def test_convert(self, get_rsr_version, download_rsr, load, isfile, exists):
        """Test the conversion method."""
        load.return_code = None
        download_rsr.return_code = None
        isfile.return_code = True
        exists.return_code = True
        get_rsr_version.return_code = RSR_DATA_VERSION

        with patch('pyspectral.rsr_reader.get_config', return_value=TEST_CONFIG):
            test_rsr = RelativeSpectralResponse('EOS-Aqua', 'modis')
            test_rsr.rsr = TEST_RSR
            test_rsr.convert()
            self.assertAlmostEqual(test_rsr.rsr['20']['det-1']['central_wavenumber'], 2647.397, 3)
            self.assertTrue(np.allclose(test_rsr.rsr['20']['det-1'][WAVE_NUMBER], RESULT_WVN_RSR, 5))
            self.assertEqual(test_rsr._wavespace, WAVE_NUMBER)

            with self.assertRaises(NotImplementedError):
                test_rsr.convert()

    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse.load')
    @patch('pyspectral.rsr_reader.download_rsr')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._get_rsr_data_version')
    def test_integral(self, get_rsr_version, download_rsr, load, isfile, exists):
        """Test the calculation of the integral of the spectral responses."""
        load.return_code = None
        download_rsr.return_code = None
        isfile.return_code = True
        exists.return_code = True
        get_rsr_version.return_code = RSR_DATA_VERSION

        with patch('pyspectral.rsr_reader.get_config', return_value=TEST_CONFIG):
            test_rsr = RelativeSpectralResponse('EOS-Aqua', 'modis')
            test_rsr.rsr = TEST_RSR2
            res = test_rsr.integral('20')
            self.assertAlmostEqual(res['det-1'], 0.185634, 6)


class MyHdf5Mock(object):
    def __init__(self, attrs):
        self.attrs = attrs


class TestPopulateRSRObject(unittest.TestCase):
    """Testing populate the RelativeSpectralResponse instance from the hdf5 file."""

    def setUp(self):
        """Initialise the tests."""
        bandnames = np.array([b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'10', b'11',
                              b'12', b'13', b'14', b'15', b'16', b'17', b'18', b'19', b'20',
                              b'21', b'22', b'23', b'24', b'25', b'26', b'27', b'28', b'29',
                              b'30', b'31', b'32', b'33', b'34', b'35', b'36'], dtype='|S2')
        hdf5_attrs_aqua_modis = {'band_names': bandnames,
                                 'description': 'Relative Spectral Responses for MODIS',
                                 'platform': 'eos',
                                 'sat_number': 2}
        hdf5_attrs_aqua_modis_b = {'band_names': bandnames,
                                   'description': b'Relative Spectral Responses for MODIS',
                                   'platform': b'eos',
                                   'sat_number': 2}
        self.modis_bandnames = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                                '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                                '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                                '31', '32', '33', '34', '35', '36']

        self.h5f_aqua_modis = MyHdf5Mock(hdf5_attrs_aqua_modis)
        self.h5f_aqua_modis_b = MyHdf5Mock(hdf5_attrs_aqua_modis_b)

        hdf5_attrs_aqua_modis_err = {'band_names': bandnames,
                                     'description': 'Relative Spectral Responses for MODIS',
                                     'platform': 'eos'}

        self.h5f_aqua_modis_err = MyHdf5Mock(hdf5_attrs_aqua_modis_err)

        bandnames = np.array([b'M1', b'M2', b'M3', b'M4', b'M5', b'M6', b'M7', b'M8', b'M9',
                              b'M10', b'M11', b'M12', b'M13', b'M14', b'M15', b'M16', b'I1',
                              b'I2', b'I3', b'I4', b'I5', b'DNB'], dtype='|S3')

        hdf5_attrs_noaa20_viirs = {'band_names': bandnames,
                                   'description': b'Relative Spectral Responses for VIIRS',
                                   'platform_name': b'NOAA-20',
                                   'sensor': b'viirs'}
        self.viirs_bandnames = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10',
                                'M11', 'M12', 'M13', 'M14', 'M15', 'M16',
                                'I1', 'I2', 'I3', 'I4', 'I5', 'DNB']
        self.viirs_detector_names = ['det-1', 'det-2', 'det-3', 'det-4', 'det-5',
                                     'det-6', 'det-7', 'det-8', 'det-9', 'det-10',
                                     'det-11', 'det-12', 'det-13', 'det-14', 'det-15',
                                     'det-16']
        self.viirs_rsr_data = xr.Dataset({'wavelength': xr.DataArray(np.arange(10)),
                                          'response': xr.DataArray(np.arange(10))})
        self.viirs_rsr_data.attrs['central_wavelength'] = 100.0
        self.viirs_rsr_data['wavelength'].attrs['scale'] = 0.01

        self.h5f_noaa20_viirs = MyHdf5Mock(hdf5_attrs_noaa20_viirs)

    @patch('pyspectral.rsr_reader.RelativeSpectralResponse.load')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._check_filename_exist')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._get_filename')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._check_instrument')
    def test_create_rsr_instance(self, check_instrument, get_filename, check_filename_exist, load):
        """Test creating the instance."""

        load.return_value = None
        check_filename_exist.return_value = None
        get_filename.return_value = None
        check_instrument.return_value = None

        with pytest.raises(AttributeError) as exec_info:
            _ = RelativeSpectralResponse('MyPlatform')

        exception_raised = exec_info.value
        expected_value = 'platform name and sensor or filename must be specified'
        self.assertEqual(str(exception_raised), expected_value)

    @patch('pyspectral.rsr_reader.RelativeSpectralResponse.load')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._check_filename_exist')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._get_filename')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._check_instrument')
    def test_set_description(self, check_instrument, get_filename, check_filename_exist, load):
        """Test setting the description."""

        load.return_value = None
        check_filename_exist.return_value = None
        get_filename.return_value = None
        check_instrument.return_value = None

        test_rsr = RelativeSpectralResponse('NOAA-20', 'viirs')
        test_rsr.set_description(self.h5f_noaa20_viirs)

        self.assertEqual(test_rsr.description, 'Relative Spectral Responses for VIIRS')

        test_rsr = RelativeSpectralResponse('EOS-Aqua', 'modis')
        test_rsr.set_description(self.h5f_aqua_modis)

        self.assertEqual(test_rsr.description, 'Relative Spectral Responses for MODIS')

    @patch('pyspectral.rsr_reader.RelativeSpectralResponse.load')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._check_filename_exist')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._get_filename')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._check_instrument')
    def test_set_platform_name(self, check_instrument, get_filename, check_filename_exist, load):
        """Test setting the platform name."""

        load.return_value = None
        check_filename_exist.return_value = None
        get_filename.return_value = None
        check_instrument.return_value = None

        test_rsr = RelativeSpectralResponse('EOS-Aqua', 'modis')
        test_rsr.set_platform_name(self.h5f_aqua_modis)
        self.assertEqual(test_rsr.platform_name, 'EOS-Aqua')

        test_rsr = RelativeSpectralResponse('MyPlatform', 'modis')
        self.assertEqual(test_rsr.platform_name, 'MyPlatform')

        modis_aqua_filepath = "/mypath/myfilename"
        test_rsr = RelativeSpectralResponse(filename=modis_aqua_filepath)
        test_rsr.filename = modis_aqua_filepath

        test_rsr.set_platform_name(self.h5f_aqua_modis)
        self.assertEqual(test_rsr.platform_name, 'EOS-Aqua')

        modis_aqua_filepath = "/mypath/myfilename"
        test_rsr = RelativeSpectralResponse(filename=modis_aqua_filepath)
        test_rsr.filename = modis_aqua_filepath

        test_rsr.set_platform_name(self.h5f_aqua_modis_b)
        self.assertEqual(test_rsr.platform_name, 'EOS-Aqua')

        viirs_noaa20_filepath = "/mypath/myfilename"
        test_rsr = RelativeSpectralResponse(filename=viirs_noaa20_filepath)
        test_rsr.filename = viirs_noaa20_filepath

        test_rsr.set_platform_name(self.h5f_noaa20_viirs)
        self.assertEqual(test_rsr.platform_name, 'NOAA-20')

        test_rsr = RelativeSpectralResponse(filename=modis_aqua_filepath)
        test_rsr.filename = modis_aqua_filepath
        test_rsr.set_platform_name(self.h5f_aqua_modis_err)
        self.assertEqual(test_rsr.platform_name, None)

    @patch('pyspectral.rsr_reader.RelativeSpectralResponse.load')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._check_filename_exist')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._get_filename')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._check_instrument')
    def test_set_instrument(self, check_instrument, get_filename, check_filename_exist, load):
        """Test setting the instrument name."""

        load.return_value = None
        check_filename_exist.return_value = None
        get_filename.return_value = None
        check_instrument.return_value = None

        test_rsr = RelativeSpectralResponse('EOS-Aqua', 'modis')
        test_rsr.set_instrument(self.h5f_aqua_modis)
        self.assertEqual(test_rsr.instrument, 'modis')

        modis_aqua_filepath = "/mypath/myfilename"
        test_rsr = RelativeSpectralResponse(filename=modis_aqua_filepath)
        test_rsr.filename = modis_aqua_filepath
        test_rsr.platform_name = 'EOS-Aqua'
        test_rsr.set_instrument(self.h5f_aqua_modis)
        self.assertEqual(test_rsr.instrument, 'modis')

        viirs_noaa20_filepath = "/mypath/myfilename"
        test_rsr = RelativeSpectralResponse(filename=viirs_noaa20_filepath)
        test_rsr.filename = viirs_noaa20_filepath

        test_rsr.set_instrument(self.h5f_noaa20_viirs)
        self.assertEqual(test_rsr.instrument, 'viirs')

    @patch('pyspectral.rsr_reader.RelativeSpectralResponse.load')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._check_filename_exist')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._get_filename')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._check_instrument')
    def test_set_band_names(self, check_instrument, get_filename, check_filename_exist, load):
        """Test setting the band names."""

        load.return_value = None
        check_filename_exist.return_value = None
        get_filename.return_value = None
        check_instrument.return_value = None

        test_rsr = RelativeSpectralResponse('EOS-Aqua', 'modis')
        test_rsr.set_band_names(self.h5f_aqua_modis)
        expected = self.modis_bandnames
        self.assertCountEqual(test_rsr.band_names, expected)

    @patch('pyspectral.rsr_reader.RelativeSpectralResponse.load')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._check_filename_exist')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._get_filename')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._check_instrument')
    def test_set_band_central_wavelength_per_detector(self,
                                                      check_instrument, get_filename,
                                                      check_filename_exist, load):
        """Test setting the band specific central wavelength for a detector."""

        load.return_value = None
        check_filename_exist.return_value = None
        get_filename.return_value = None
        check_instrument.return_value = None

        test_rsr = RelativeSpectralResponse('NOAA-20', 'viirs')

        h5f = {}
        for name in self.viirs_bandnames:
            h5f[name] = {}
            for det_name in self.viirs_detector_names:
                h5f[name][det_name] = self.viirs_rsr_data

        test_rsr.rsr['M1'] = {'det-1': {}}
        test_rsr.set_band_central_wavelength_per_detector(h5f, 'M1', 'det-1')
        self.assertIn('central_wavelength', test_rsr.rsr['M1']['det-1'])
        self.assertEqual(test_rsr.rsr['M1']['det-1']['central_wavelength'], 100.)

    @patch('pyspectral.rsr_reader.RelativeSpectralResponse.load')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._check_filename_exist')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._get_filename')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._check_instrument')
    def test_set_band_wavelengths_per_detector(self,
                                               check_instrument, get_filename,
                                               check_filename_exist, load):
        """Test setting the band wavelengths for a detector."""

        load.return_value = None
        check_filename_exist.return_value = None
        get_filename.return_value = None
        check_instrument.return_value = None

        test_rsr = RelativeSpectralResponse('NOAA-20', 'viirs')

        h5f = {}
        for name in self.viirs_bandnames:
            h5f[name] = {}
            for det_name in self.viirs_detector_names:
                h5f[name][det_name] = self.viirs_rsr_data

        test_rsr.rsr['M1'] = {'det-1': {}}
        test_rsr.set_band_wavelengths_per_detector(h5f, 'M1', 'det-1')

        expected = np.array([0., 10000., 20000., 30000., 40000., 50000.,
                             60000., 70000., 80000., 90000.])
        assertNumpyArraysEqual(test_rsr.rsr['M1']['det-1']['wavelength'].data, expected)

    @patch('pyspectral.rsr_reader.RelativeSpectralResponse.load')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._check_filename_exist')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._get_filename')
    @patch('pyspectral.rsr_reader.RelativeSpectralResponse._check_instrument')
    def test_set_band_responses_per_detector(self,
                                             check_instrument, get_filename,
                                             check_filename_exist, load):
        """Test setting the band responses for a detector."""

        load.return_value = None
        check_filename_exist.return_value = None
        get_filename.return_value = None
        check_instrument.return_value = None

        test_rsr = RelativeSpectralResponse('NOAA-20', 'viirs')

        h5f = {}
        for name in self.viirs_bandnames:
            h5f[name] = {}
            for det_name in self.viirs_detector_names:
                h5f[name][det_name] = self.viirs_rsr_data

        test_rsr.rsr['M1'] = {'det-1': {}}
        test_rsr.set_band_responses_per_detector(h5f, 'M1', 'det-1')

        expected = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        assertNumpyArraysEqual(test_rsr.rsr['M1']['det-1']['response'].data, expected)
