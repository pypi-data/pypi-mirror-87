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

"""Level 1C Processor:   Atmospheric correction of TOA-reflectance data."""

import warnings
import re
import logging
import dill
import traceback
from typing import List  # noqa F401  # flake8 issue
from time import time
import os
import timeout_decorator

import numpy as np
from ecmwfapi.api import APIKeyFetchError
from ecmwfapi.api import APIException as ECMWFAPIException

from geoarray import GeoArray
from py_tools_ds.geo.map_info import mapinfo2geotransform
from pyrsr import RSR

from ..options.config import GMS_config as CFG
from . import geoprocessing as GEOP
from .L1B_P import L1B_object
from ..model.metadata import get_LayerBandsAssignment
from ..misc.definition_dicts import get_outFillZeroSaturated, proc_chain, get_mask_classdefinition
from ..misc.locks import MultiSlotLock
# from .cloud_masking import Cloud_Mask_Creator  # circular dependencies

from sicor.sicor_ac import ac_gms
from sicor.sensors import RSImage
from sicor.Mask import S2Mask
from sicor.ECMWF import download_variables

__author__ = 'Daniel Scheffler'


class L1C_object(L1B_object):
    def __init__(self, L1B_obj=None):
        super(L1C_object, self).__init__()

        if L1B_obj:
            # populate attributes
            [setattr(self, key, value) for key, value in L1B_obj.__dict__.items()]

        # private attributes
        self._VZA_arr = None
        self._VAA_arr = None
        self._SZA_arr = None
        self._SAA_arr = None
        self._RAA_arr = None
        self._lonlat_arr = None

        self.proc_level = 'L1C'
        self.proc_status = 'initialized'

    @property
    def lonlat_arr(self):
        """Calculates pixelwise 2D-array with longitude and latitude coordinates.

        :return:
        """
        if self._lonlat_arr is None:
            self.logger.info('Calculating LonLat array...')
            self._lonlat_arr = \
                GEOP.get_lonlat_coord_array(self.shape_fullArr, self.arr_pos,
                                            mapinfo2geotransform(self.MetaObj.map_info),
                                            self.MetaObj.projection,
                                            meshwidth=10,  # for faster processing
                                            nodata_mask=None,  # dont overwrite areas outside the image with nodata
                                            outFill=get_outFillZeroSaturated(np.float32)[0])[0]
        return self._lonlat_arr

    @lonlat_arr.setter
    def lonlat_arr(self, lonlat_arr):
        self._lonlat_arr = lonlat_arr

    @lonlat_arr.deleter
    def lonlat_arr(self):
        self._lonlat_arr = None

    @property
    def VZA_arr(self):
        """Get viewing zenith angle.

        :return:
        """
        if self._VZA_arr is None:
            self.logger.info('Calculating viewing zenith array...')
            if self.MetaObj.ViewingAngle_arrProv:
                # Sentinel-2
                self._VZA_arr = GEOP.adjust_acquisArrProv_to_shapeFullArr(
                    {k: v.tolist() for k, v in self.MetaObj.ViewingAngle_arrProv.items()},
                    self.shape_fullArr,
                    meshwidth=10,  # for faster processing
                    subset=None,
                    bandwise=0)
            else:
                self._VZA_arr = GEOP.calc_VZA_array(self.shape_fullArr, self.arr_pos, self.fullSceneCornerPos,
                                                    float(self.MetaObj.ViewingAngle),
                                                    float(self.MetaObj.FOV),
                                                    self.logger,
                                                    nodata_mask=None,  # dont overwrite areas outside image with nodata
                                                    outFill=get_outFillZeroSaturated(np.float32)[0],
                                                    meshwidth=10)  # for faster processing
        return self._VZA_arr

    @VZA_arr.setter
    def VZA_arr(self, VZA_arr):
        self._VZA_arr = VZA_arr

    @VZA_arr.deleter
    def VZA_arr(self):
        self._VZA_arr = None

    @property
    def VAA_arr(self):
        """Get viewing azimuth angle.

        :return:
        """
        if self._VAA_arr is None:
            self.logger.info('Calculating viewing azimuth array...')
            if self.MetaObj.IncidenceAngle_arrProv:
                # Sentinel-2
                self._VAA_arr = GEOP.adjust_acquisArrProv_to_shapeFullArr(
                    {k: v.tolist() for k, v in self.MetaObj.IncidenceAngle_arrProv.items()},
                    self.shape_fullArr,
                    meshwidth=10,  # for faster processing
                    subset=None,
                    bandwise=0)
            else:
                # only a mean VAA is available
                if self.VAA_mean is None:
                    self.VAA_mean = \
                        GEOP.calc_VAA_using_fullSceneCornerLonLat(self.fullSceneCornerLonLat, self.MetaObj.orbitParams)
                    assert isinstance(self.VAA_mean, float)

                self._VAA_arr = np.full(self.VZA_arr.shape, self.VAA_mean, np.float32)
        return self._VAA_arr

    @VAA_arr.setter
    def VAA_arr(self, VAA_arr):
        self._VAA_arr = VAA_arr

    @VAA_arr.deleter
    def VAA_arr(self):
        self._VAA_arr = None

    @property
    def SZA_arr(self):
        """Get solar zenith angle.

        :return:
        """
        if self._SZA_arr is None:
            self.logger.info('Calculating solar zenith and azimuth arrays...')
            self._SZA_arr, self._SAA_arr = \
                GEOP.calc_SZA_SAA_array(
                    self.shape_fullArr, self.arr_pos,
                    self.MetaObj.AcqDate,
                    self.MetaObj.AcqTime,
                    self.fullSceneCornerPos,
                    self.fullSceneCornerLonLat,
                    self.MetaObj.overpassDurationSec,
                    self.logger,
                    meshwidth=10,
                    nodata_mask=None,  # dont overwrite areas outside the image with nodata
                    outFill=get_outFillZeroSaturated(np.float32)[0],
                    accurracy=CFG.SZA_SAA_calculation_accurracy,
                    lonlat_arr=self.lonlat_arr if CFG.SZA_SAA_calculation_accurracy == 'fine' else None)
        return self._SZA_arr

    @SZA_arr.setter
    def SZA_arr(self, SZA_arr):
        self._SZA_arr = SZA_arr

    @SZA_arr.deleter
    def SZA_arr(self):
        self._SZA_arr = None

    @property
    def SAA_arr(self):
        """Get solar azimuth angle.

        :return:
        """
        if self._SAA_arr is None:
            # noinspection PyStatementEffect
            self.SZA_arr  # getter also sets self._SAA_arr
        return self._SAA_arr

    @SAA_arr.setter
    def SAA_arr(self, SAA_arr):
        self._SAA_arr = SAA_arr

    @SAA_arr.deleter
    def SAA_arr(self):
        self._SAA_arr = None

    @property
    def RAA_arr(self):
        """Get relative azimuth angle.

        :return:
        """
        if self._RAA_arr is None:
            self.logger.info('Calculating relative azimuth array...')
            self._RAA_arr = GEOP.calc_RAA_array(self.SAA_arr, self.VAA_mean,
                                                nodata_mask=None, outFill=get_outFillZeroSaturated(np.float32)[0])
        return self._RAA_arr

    @RAA_arr.setter
    def RAA_arr(self, RAA_arr):
        self._RAA_arr = RAA_arr

    @RAA_arr.deleter
    def RAA_arr(self):
        self._RAA_arr = None

    def delete_ac_input_arrays(self):
        """Delete AC input arrays if they are not needed anymore."""
        self.logger.info('Deleting input arrays for atmospheric correction...')
        del self.VZA_arr
        del self.SZA_arr
        del self.SAA_arr
        del self.RAA_arr
        del self.lonlat_arr

        # use self.dem deleter
        # would have to be resampled when writing MGRS tiles
        # -> better to directly warp it to the output dims and projection
        del self.dem


class AtmCorr(object):
    def __init__(self, *L1C_objs, reporting=False):
        """Wrapper around atmospheric correction by Andre Hollstein, GFZ Potsdam

        Creates the input arguments for atmospheric correction from one or multiple L1C_object instance(s) belonging to
        the same scene ID, performs the atmospheric correction and returns the atmospherically corrected L1C object(s).

        :param L1C_objs: one or more instances of L1C_object belonging to the same scene ID
        """
        # FIXME not yet usable for data < 2012 due to missing ECMWF archive
        L1C_objs = L1C_objs if isinstance(L1C_objs, tuple) else (L1C_objs,)

        # hidden attributes
        self._logger = None
        self._GSDs = []
        self._data = {}
        self._metadata = {}
        self._nodata = {}
        self._band_spatial_sampling = {}
        self._options = {}

        # assertions
        scene_IDs = [obj.scene_ID for obj in L1C_objs]
        assert len(list(set(scene_IDs))) == 1, \
            "Input GMS objects for 'AtmCorr' must all belong to the same scene ID!. Received %s." % scene_IDs

        self.inObjs = L1C_objs  # type: List[L1C_object]
        self.reporting = reporting
        self.ac_input = {}  # set by self.run_atmospheric_correction()
        self.results = None  # direct output of external atmCorr module (set by run_atmospheric_correction)
        self.proc_info = {}
        self.outObjs = []  # atmospherically corrected L1C objects

        # append AtmCorr object to input L1C objects
        # [setattr(L1C_obj, 'AtmCorr', self) for L1C_obj in self.inObjs] # too big for serialization

        if not re.search(r'Sentinel-2', self.inObjs[0].satellite, re.I):
            self.logger.debug('Calculation of acquisition geometry arrays is currently only validated for Sentinel-2!')
            # validation possible by comparing S2 angles provided by ESA with own angles  # TODO

    @property
    def logger(self):
        if self._logger and self._logger.handlers[:]:
            return self._logger
        else:
            if len(self.inObjs) == 1:
                # just use the logger of the inObj
                logger_atmCorr = self.inObjs[0].logger
            else:
                # in case of multiple GMS objects to be processed at once:
                # get the logger of the first inObj
                logger_atmCorr = self.inObjs[0].logger

                # add additional file handlers for the remaining inObj (that belong to the same scene_ID)
                for inObj in self.inObjs[1:]:
                    path_logfile = inObj.pathGen.get_path_logfile()
                    fileHandler = logging.FileHandler(path_logfile, mode='a')
                    fileHandler.setFormatter(logger_atmCorr.formatter_fileH)
                    fileHandler.setLevel(CFG.log_level)

                    logger_atmCorr.addHandler(fileHandler)

                    inObj.close_loggers()

            self._logger = logger_atmCorr
            return self._logger

    @logger.setter
    def logger(self, logger):
        assert isinstance(logger, logging.Logger) or logger in ['not set', None], \
            "AtmCorr.logger can not be set to %s." % logger
        if logger in ['not set', None]:
            self._logger.close()
            self._logger = logger
        else:
            self._logger = logger

    @logger.deleter
    def logger(self):
        if self._logger not in [None, 'not set']:
            self._logger.close()
            self._logger = None

        [inObj.close_loggers() for inObj in self.inObjs]

    @property
    def GSDs(self):
        """
        Returns a list of spatial samplings within the input GMS objects, e.g. [10,20,60].
        """
        for obj in self.inObjs:
            if obj.arr.xgsd != obj.arr.ygsd:
                warnings.warn("X/Y GSD is not equal for entity ID %s" % obj.entity_ID +
                              (' (%s)' % obj.subsystem if obj.subsystem else '') +
                              'Using X-GSD as key for spatial sampling dictionary.')
                self._GSDs.append(obj.arr.xgsd)

        return self._GSDs

    @property
    def data(self):
        """

        :return:
            ___ attribute: data, type:<class 'dict'>
            ______ key:B05, value_type:<class 'numpy.ndarray'>, repr: [[nan nan nan ...,0. [..] 085998540.0803833 ]]
            ______ key:B01, value_type:<class 'numpy.ndarray'>, repr: [[nan nan nan ...,0. [..] 131225590.13208008]]
            ______ key:B06, value_type:<class 'numpy.ndarray'>, repr: [[nan nan nan ...,0. [..] .14965820.13977051]]
            ______ key:B11, value_type:<class 'numpy.ndarray'>, repr: [[nan nan nan ...,0. [..] .11492920.10192871]]
            ______ key:B02, value_type:<class 'numpy.ndarray'>, repr: [[nan nan nan ...,0. [..] 104187010.10308838]]
            ______ key:B10, value_type:<class 'numpy.ndarray'>, repr: [[nan nan nan ...,0. [..] 013099670.01300049]]
            ______ key:B08, value_type:<class 'numpy.ndarray'>, repr: [[nan nan nan ...,0. [..] .16857910.15783691]]
            ______ key:B04, value_type:<class 'numpy.ndarray'>, repr: [[nan nan nan ...,0. [..] 065490720.06228638]]
            ______ key:B03, value_type:<class 'numpy.ndarray'>, repr: [[nan nan nan ...,0. [..] 082702640.08148193]]
            ______ key:B12, value_type:<class 'numpy.ndarray'>, repr: [[nan nan nan ...,0. [..] 068420410.06060791]]
            ______ key:B8A, value_type:<class 'numpy.ndarray'>, repr: [[nan nan nan ...,0. [..] 192138670.17553711]]
            ______ key:B09, value_type:<class 'numpy.ndarray'>, repr: [[nan nan nan ...,0. [..] .09600830.09887695]]
            ______ key:B07, value_type:<class 'numpy.ndarray'>, repr: [[nan nan nan ...,0. [..] 173339840.15600586]]
        """
        if not self._data:
            data_dict = {}

            for inObj in self.inObjs:
                for bandN, bandIdx in inObj.arr.bandnames.items():
                    if bandN not in data_dict:
                        # float32! -> conversion to np.float16 will convert -9999 to -10000
                        arr2pass = inObj.arr[:, :, bandIdx].astype(np.float32)
                        arr2pass[arr2pass == inObj.arr.nodata] = np.nan  # set nodata values to np.nan
                        data_dict[bandN] = (arr2pass / inObj.MetaObj.ScaleFactor).astype(np.float16)
                    else:
                        inObj.logger.warning("Band '%s' cannot be included into atmospheric correction because it "
                                             "exists multiple times." % bandN)

            # validate: data must have all bands needed for AC
            full_LBA = get_LayerBandsAssignment(self.inObjs[0].GMS_identifier, return_fullLBA=True)
            all_bNs_AC = ['B%s' % i if len(i) == 2 else 'B0%s' % i for i in full_LBA]
            if not all([bN in list(data_dict.keys()) for bN in all_bNs_AC]):
                raise RuntimeError('Atmospheric correction did not receive all the needed bands. \n\tExpected: %s;\n\t'
                                   'Received: %s' % (str(all_bNs_AC), str(list(sorted(data_dict.keys())))))

            self._data = data_dict

        return self._data

    @data.setter
    def data(self, data_dict):
        assert isinstance(data_dict, dict), \
            "'data' can only be set to a dictionary with band names as keys and numpy arrays as values."
        self._data = data_dict

    @property
    def nodata(self):
        """

        :return:
            ___ attribute: nodata, type:<class 'dict'>
            ______ key:60.0, value_type:<class 'numpy.ndarray'>, repr: [[ TrueTrueTrue ..., [..]  False False False]]
            ______ key:10.0, value_type:<class 'numpy.ndarray'>, repr: [[ TrueTrueTrue ..., [..]  False False False]]
            ______ key:20.0, value_type:<class 'numpy.ndarray'>, repr: [[ TrueTrueTrue ..., [..]  False False False]]
        """

        if not self._nodata:
            for inObj in self.inObjs:
                self._nodata[inObj.arr.xgsd] = ~inObj.arr.mask_nodata[:]

        return self._nodata

    @property
    def tile_name(self):
        """Returns S2A tile name.
        NOTE: this is only needed if no DEM is passed to ac_gms

        :return: e.g.
            '32UMA'
        """

        return ''  # FIXME

    @property
    def band_spatial_sampling(self):
        """

        :return: e.g.
            {'B01': 60.0,
             'B02': 10.0,
             'B03': 10.0,
             'B04': 10.0,
             'B05': 20.0,
             'B06': 20.0,
             'B07': 20.0,
             'B08': 10.0,
             'B09': 60.0,
             'B10': 60.0,
             'B11': 20.0,
             'B12': 20.0,
             'B8A': 20.0}
        """

        if not self._band_spatial_sampling:
            for inObj in self.inObjs:
                for bandN in inObj.arr.bandnames:
                    if bandN not in self._band_spatial_sampling:
                        self._band_spatial_sampling[bandN] = inObj.arr.xgsd
        return self._band_spatial_sampling

    @property
    def metadata(self):
        """

        :return:
            ___ attribute: metadata, type:<class 'dict'>
            ______ key:spatial_samplings
            _________ key:60.0
            ____________ key:ULY, value_type:<class 'int'>, repr: 4900020
            ____________ key:NCOLS, value_type:<class 'int'>, repr: 1830
            ____________ key:XDIM, value_type:<class 'int'>, repr: 60
            ____________ key:ULX, value_type:<class 'int'>, repr: 600000
            ____________ key:NROWS, value_type:<class 'int'>, repr: 1830
            ____________ key:YDIM, value_type:<class 'int'>, repr: -60
            _________ key:10.0
            ____________ key:ULY, value_type:<class 'int'>, repr: 4900020
            ____________ key:NCOLS, value_type:<class 'int'>, repr: 10980
            ____________ key:XDIM, value_type:<class 'int'>, repr: 10
            ____________ key:ULX, value_type:<class 'int'>, repr: 600000
            ____________ key:NROWS, value_type:<class 'int'>, repr: 10980
            ____________ key:YDIM, value_type:<class 'int'>, repr: -10
            _________ key:20.0
            ____________ key:ULY, value_type:<class 'int'>, repr: 4900020
            ____________ key:NCOLS, value_type:<class 'int'>, repr: 5490
            ____________ key:XDIM, value_type:<class 'int'>, repr: 20
            ____________ key:ULX, value_type:<class 'int'>, repr: 600000
            ____________ key:NROWS, value_type:<class 'int'>, repr: 5490
            ____________ key:YDIM, value_type:<class 'int'>, repr: -20
            ______ key:SENSING_TIME, value_type:<class 'datetime.datetime'>, repr: 2016-03-26 10:34:06.538000+00:00
        """

        if not self._metadata:
            del self.logger  # otherwise each input object would have multiple fileHandlers

            metadata = dict(
                U=self.inObjs[0].MetaObj.EarthSunDist,
                SENSING_TIME=self.inObjs[0].acq_datetime,
                # SENSING_TIME=datetime.strptime('2015-08-12 10:40:21 +0000', '%Y-%m-%d %H:%M:%S %z'),
                viewing_zenith=self._meta_get_viewing_zenith(),
                viewing_azimuth=self._meta_get_viewing_azimuth(),
                relative_viewing_azimuth=self._meta_get_relative_viewing_azimuth(),
                sun_mean_azimuth=self.inObjs[0].MetaObj.SunAzimuth,
                sun_mean_zenith=90 - self.inObjs[0].MetaObj.SunElevation,
                solar_irradiance=self._meta_get_solar_irradiance(),
                aux_data=self._meta_get_aux_data(),
                spatial_samplings=self._meta_get_spatial_samplings()
            )

            self._metadata = metadata

        return self._metadata

    @property
    def options(self):
        # type: () -> dict
        """Returns a dictionary containing AC options.
        """
        if self._options:
            return self._options
        else:
            self._options = self.inObjs[0].ac_options
            self._options["AC"]['bands'] = [b for b in self.data.keys() if b in self._options["AC"]['bands']]
            self._options["report"]["reporting"] = self.reporting
            return self._options

    def _meta_get_spatial_samplings(self):
        """

        :return:
         {10.0: {'NCOLS': 10980,
           'NROWS': 10980,
           'ULX': 499980.0,
           'ULY': 5800020.0,
           'XDIM': 10.0,
           'YDIM': -10.0},
          20.0: {'NCOLS': 5490,
           'NROWS': 5490,
           'ULX': 499980.0,
           'ULY': 5800020.0,
           'XDIM': 20.0,
           'YDIM': -20.0},
          60.0: {'NCOLS': 1830,
           'NROWS': 1830,
           'ULX': 499980.0,
           'ULY': 5800020.0,
           'XDIM': 60.0,
           'YDIM': -60.0}}
        """
        # set corner coordinates and dims
        spatial_samplings = {}

        for inObj in self.inObjs:

            # validate GSD
            if inObj.arr.xgsd != inObj.arr.ygsd:
                warnings.warn("X/Y GSD is not equal for entity ID %s" % inObj.entity_ID +
                              (' (%s)' % inObj.subsystem if inObj.subsystem else '') +
                              'Using X-GSD as key for spatial sampling dictionary.')

            # set spatial information
            spatial_samplings[inObj.arr.xgsd] = dict(
                ULX=inObj.arr.box.boxMapYX[0][1],
                ULY=inObj.arr.box.boxMapYX[0][0],
                XDIM=inObj.arr.xgsd,
                YDIM=-inObj.arr.ygsd,
                NROWS=inObj.arr.rows,
                NCOLS=inObj.arr.cols)

        return spatial_samplings

    def _meta_get_solar_irradiance(self):
        """

        :return:
        {'B01': 1913.57,
         'B02': 1941.63,
         'B03': 1822.61,
         'B04': 1512.79,
         'B05': 1425.56,
         'B06': 1288.32,
         'B07': 1163.19,
         'B08': 1036.39,
         'B09': 813.04,
         'B10': 367.15,
         'B11': 245.59,
         'B12': 85.25,
         'B8A': 955.19}
        """

        solar_irradiance = {}

        for inObj in self.inObjs:
            for bandN in inObj.arr.bandnames:
                lba_key = bandN[2:] if bandN.startswith('B0') else bandN[1:]
                if bandN not in solar_irradiance:
                    solar_irradiance[bandN] = inObj.MetaObj.SolIrradiance[lba_key]

        return solar_irradiance

    def _meta_get_viewing_zenith(self):
        """

        :return: {B10:ndarray(dtype=float16),[...],B09:ndarray(dtype=float16)}
        """

        viewing_zenith = {}

        for inObj in self.inObjs:  # type: L1C_object
            for bandN, bandIdx in inObj.arr.bandnames.items():
                if bandN not in viewing_zenith:
                    arr2pass = inObj.VZA_arr[:, :, bandIdx] if inObj.VZA_arr.ndim == 3 else inObj.VZA_arr
                    viewing_zenith[bandN] = arr2pass.astype(np.float16)
                    # viewing_zenith[bandN] = inObj.VZA_arr[:, :, bandIdx] if inObj.VZA_arr.ndim==3 else inObj.VZA_arr
        return viewing_zenith

    def _meta_get_viewing_azimuth(self):
        """

        :return: {B10:ndarray(dtype=float16),[...],B09:ndarray(dtype=float16)}
        """

        viewing_azimuth = {}

        for inObj in self.inObjs:  # type: L1C_object
            for bandN, bandIdx in inObj.arr.bandnames.items():
                if bandN not in viewing_azimuth:
                    arr2pass = inObj.VAA_arr[:, :, bandIdx] if inObj.VAA_arr.ndim == 3 else inObj.VAA_arr
                    viewing_azimuth[bandN] = arr2pass.astype(np.float16)
                    # viewing_azimuth[bandN] = inObj.VAA_arr[:, :, bandIdx] if inObj.VAA_arr.ndim==3 else inObj.VAA_arr

        return viewing_azimuth

    def _meta_get_relative_viewing_azimuth(self):
        """

        :return: {B10:ndarray(dtype=float16),[...],B09:ndarray(dtype=float16)}
        """

        relative_viewing_azimuth = {}

        for inObj in self.inObjs:  # type: L1C_object
            for bandN, bandIdx in inObj.arr.bandnames.items():
                if bandN not in relative_viewing_azimuth:
                    arr2pass = inObj.RAA_arr[:, :, bandIdx] if inObj.RAA_arr.ndim == 3 else inObj.RAA_arr
                    relative_viewing_azimuth[bandN] = arr2pass.astype(np.float16)
                    # relative_viewing_azimuth[bandN] = \
                    #     inObj.RAA_arr[:, :, bandIdx] if inObj.RAA_arr.ndim==3 else inObj.RAA_arr

        return relative_viewing_azimuth

    def _meta_get_aux_data(self):
        """

        :return:  {lons:ndarray(dtype=float16),,lats:ndarray(dtype=float16)}
        """

        aux_data = dict(
            # set lons and lats (a 2D array for all bands is enough (different band resolutions dont matter))
            lons=self.inObjs[0].lonlat_arr[::10, ::10, 0].astype(np.float16),  # 2D array of lon values: 0° - 360°
            lats=self.inObjs[0].lonlat_arr[::10, ::10, 1].astype(np.float16)  # 2D array of lat values: -90° - 90°
            # FIXME correct to reduce resolution here by factor 10?
        )

        return aux_data

    def _get_dem(self):
        """Get a DEM to be used in atmospheric correction.

        :return: <np.ndarray> 2D array (with 20m resolution in case of Sentinel-2)
        """
        # determine which input GMS object is used to generate DEM
        if re.search(r'Sentinel-2', self.inObjs[0].satellite):
            # in case of Sentinel-2 the 20m DEM must be passed
            inObj4dem = [obj for obj in self.inObjs if obj.arr.xgsd == 20]
            if not inObj4dem:
                self.logger.warning('Sentinel-2 20m subsystem could not be found. DEM passed to '
                                    'atmospheric correction might have wrong resolution.')
            inObj4dem = inObj4dem[0]
        else:
            inObj4dem = self.inObjs[0]

        try:
            dem = inObj4dem.dem[:].astype(np.float32)
        except Exception as e:
            dem = None
            self.logger.warning('A static elevation is assumed during atmospheric correction due to an error during '
                                'creation of the DEM corresponding to scene %s (entity ID: %s). Error message was: '
                                '\n%s\n' % (self.inObjs[0].scene_ID, self.inObjs[0].entity_ID, repr(e)))
            self.logger.info("Print traceback in case you care:")
            self.logger.warning(traceback.format_exc())

        return dem

    def _get_srf(self):
        """Returns an instance of SRF in the same structure like sicor.sensors.SRF.SensorSRF
        """
        # FIXME calculation of center wavelengths within RSR() used not the GMS algorithm
        # SRF instance must be created for all bands and the previous proc level
        GMSid_fullScene = self.inObjs[0].GMS_identifier
        GMSid_fullScene.subsystem = ''
        GMSid_fullScene.proc_level = proc_chain[proc_chain.index(self.inObjs[0].proc_level) - 1]

        return RSR(satellite=GMSid_fullScene.satellite,
                   sensor=GMSid_fullScene.sensor,
                   subsystem=GMSid_fullScene.subsystem,
                   wvl_unit='nanometers',
                   format_bandnames=True,
                   no_pan=CFG.skip_pan,
                   no_thermal=CFG.skip_thermal,
                   after_ac=GMSid_fullScene.proc_level in ['L1C', 'L2A', 'L2B', 'L2C'],
                   sort_by_cwl=CFG.sort_bands_by_cwl
                   )

    def _get_mask_clouds(self):
        """Returns an instance of S2Mask in case cloud mask is given by input GMS objects. Otherwise None is returned.

        :return:
        """

        tgt_res = self.inObjs[0].ac_options['cld_mask']['target_resolution']

        # check if input GMS objects provide a cloud mask
        avail_cloud_masks = {inObj.GMS_identifier.subsystem: inObj.mask_clouds for inObj in self.inObjs}
        no_avail_CMs = list(set(avail_cloud_masks.values())) == [None]

        # compute cloud mask if not already provided
        if no_avail_CMs:
            algorithm = CFG.cloud_masking_algorithm[self.inObjs[0].satellite]

            if algorithm == 'SICOR':
                return None

            else:
                # FMASK or Classical Bayesian
                try:
                    from .cloud_masking import Cloud_Mask_Creator

                    CMC = Cloud_Mask_Creator(self.inObjs[0], algorithm=algorithm, tempdir_root=CFG.path_tempdir)
                    CMC.calc_cloud_mask()
                    cm_geoarray = CMC.cloud_mask_geoarray
                    cm_array = CMC.cloud_mask_array
                    cm_legend = CMC.cloud_mask_legend
                except Exception:
                    self.logger.error('\nAn error occurred during FMASK cloud masking. Error message was: ')
                    self.logger.error(traceback.format_exc())
                    return None

        else:
            # check if there is a cloud mask with suitable GSD
            inObjs2use = [obj for obj in self.inObjs if obj.mask_clouds is not None and obj.mask_clouds.xgsd == tgt_res]
            if not inObjs2use:
                raise ValueError('Error appending cloud mask to input arguments of atmospheric correction. No input '
                                 'GMS object provides a cloud mask with spatial resolution of %s.' % tgt_res)
            inObj2use = inObjs2use[0]

            # get mask (geo)array
            cm_geoarray = inObj2use.mask_clouds
            cm_array = inObj2use.mask_clouds[:]

            # get legend
            cm_legend = get_mask_classdefinition('mask_clouds', inObj2use.satellite)
            #    {'Clear': 10, 'Thick Clouds': 20, 'Thin Clouds': 30, 'Snow': 40}  # FIXME hardcoded

            # validate that xGSD equals yGSD
            if cm_geoarray.xgsd != cm_geoarray.ygsd:
                warnings.warn("Cloud mask X/Y GSD is not equal for entity ID %s" % inObj2use.entity_ID +
                              (' (%s)' % inObj2use.subsystem if inObj2use.subsystem else '') +
                              'Using X-GSD as key for cloud mask geocoding.')

        # get geocoding
        cm_geocoding = self.metadata["spatial_samplings"][tgt_res]

        # get nodata value
        self.options['cld_mask']['nodata_value_mask'] = cm_geoarray.nodata

        # append cloud mask to input object with the same spatial resolution if there was no mask before
        for inObj in self.inObjs:
            if inObj.arr.xgsd == cm_geoarray.xgsd:
                inObj.mask_clouds = cm_geoarray
                inObj.build_combined_masks_array()
                break  # appending it to one inObj is enough

        return S2Mask(mask_array=cm_array,
                      mask_legend=cm_legend,
                      geo_coding=cm_geocoding)

    def _check_or_download_ECMWF_data(self):
        """Check if ECMWF files are already downloaded. If not, start the downloader."""
        self.logger.info('Checking if ECMWF data are available... (if not, run download!)')

        default_products = [
            "fc_T2M",
            "fc_O3",
            "fc_SLP",
            "fc_TCWV",
            "fc_GMES_ozone",
            "fc_total_AOT_550nm",
            "fc_sulphate_AOT_550nm",
            "fc_black_carbon_AOT_550nm",
            "fc_dust_AOT_550nm",
            "fc_organic_matter_AOT_550nm",
            "fc_sea_salt_AOT_550nm"]

        # NOTE: use_signals must be set to True while executed as multiprocessing worker (e.g., in multiprocessing.Pool)
        @timeout_decorator.timeout(seconds=60*5, timeout_exception=TimeoutError)
        def run_request():
            try:
                with MultiSlotLock('ECMWF download lock', allowed_slots=1, logger=self.logger):
                    t0 = time()
                    # NOTE: download_variables does not accept a logger -> so the output may be invisible in WebApp
                    results = download_variables(date_from=self.inObjs[0].acq_datetime,
                                                 date_to=self.inObjs[0].acq_datetime,
                                                 db_path=CFG.path_ECMWF_db,
                                                 max_step=120,  # default
                                                 ecmwf_variables=default_products,
                                                 processes=0,  # singleprocessing
                                                 force=False)  # dont force download if files already exist
                    t1 = time()
                    self.logger.info("Runtime: %.2f" % (t1 - t0))
                    for result in results:
                        self.logger.info(result)

            except APIKeyFetchError:
                self.logger.error("ECMWF data download failed due to missing API credentials.")

            except (ECMWFAPIException, Exception):
                self.logger.error("ECMWF data download failed for scene %s (entity ID: %s). Traceback: "
                                  % (self.inObjs[0].scene_ID, self.inObjs[0].entity_ID))
                self.logger.error(traceback.format_exc())

        try:
            run_request()
        except TimeoutError:
            self.logger.error("ECMWF data download failed due to API request timeout after waiting 5 minutes.")

    def _validate_snr_source(self):
        """Check if the given file path for the SNR model exists - if not, use a constant SNR of 500."""
        if not os.path.isfile(self.options["uncertainties"]["snr_model"]):
            self.logger.warning('No valid SNR model found for %s %s. Using constant SNR to compute uncertainties of '
                                'atmospheric correction.' % (self.inObjs[0].satellite, self.inObjs[0].sensor))
            # self.options["uncertainties"]["snr_model"] = np.nan  # causes the computed uncertainties to be np.nan
            self.options["uncertainties"]["snr_model"] = 500  # use a constant SNR of 500 to compute uncertainties

    def run_atmospheric_correction(self, dump_ac_input=False):
        # type: (bool) -> list
        """Collects all input data for atmospheric correction, runs the AC and returns the corrected L1C objects
        containing surface reflectance.

        :param dump_ac_input:   allows to dump the inputs of AC to the scene's processing folder in case AC fails
        :return:                list of L1C_object instances containing atmospherically corrected data
        """

        # collect input args/kwargs for AC
        self.logger.info('Calculating input data for atmospheric correction...')

        rs_data = dict(
            data=self.data,
            metadata=self.metadata,
            nodata=self.nodata,
            band_spatial_sampling=self.band_spatial_sampling,
            tile_name=self.tile_name,
            dem=self._get_dem(),
            srf=self._get_srf(),
            mask_clouds=self._get_mask_clouds()
            # returns an instance of S2Mask or None if cloud mask is not given by input GMS objects
        )  # NOTE: all keys of this dict are later converted to attributes of RSImage

        # remove empty values from RSImage kwargs because SICOR treats any kind of RSImage attributes as given
        # => 'None'-attributes may cause issues
        rs_data = {k: v for k, v in rs_data.items() if v is not None}

        script = False

        # check if ECMWF data are available - if not, start the download
        if CFG.auto_download_ecmwf:
            self._check_or_download_ECMWF_data()

        # validate SNR
        if CFG.ac_estimate_accuracy:
            self._validate_snr_source()

        # create an instance of RSImage
        rs_image = RSImage(**rs_data)

        self.ac_input = dict(
            rs_image=rs_image,
            options=self.options,  # dict
            logger=repr(self.logger),  # only a string
            script=script
        )

        # path_dump = self.inObjs[0].pathGen.get_path_ac_input_dump()
        # with open(path_dump, 'wb') as outF:
        #     dill.dump(self.ac_input, outF)

        # run AC
        self.logger.info('Atmospheric correction started.')
        try:
            rs_image.logger = self.logger
            self.results = ac_gms(rs_image, self.options, logger=self.logger, script=script)

        except Exception as e:
            self.logger.error('\nAn error occurred during atmospheric correction. BE AWARE THAT THE SCENE %s '
                              '(ENTITY ID %s) HAS NOT BEEN ATMOSPHERICALLY CORRECTED! Error message was: \n%s\n'
                              % (self.inObjs[0].scene_ID, self.inObjs[0].entity_ID, repr(e)))
            self.logger.error(traceback.format_exc())
            # TODO include that in the job summary

            # serialize AC input
            if dump_ac_input:
                path_dump = self.inObjs[0].pathGen.get_path_ac_input_dump()
                with open(path_dump, 'wb') as outF:
                    self.ac_input['rs_image'].logger = None
                    dill.dump(self.ac_input, outF)

                self.logger.error('An error occurred during atmospheric correction. Inputs have been dumped to %s.'
                                  % path_dump)

            # delete AC input arrays
            for inObj in self.inObjs:  # type: L1C_object
                inObj.delete_ac_input_arrays()

            return list(self.inObjs)

        finally:
            # rs_image.logger must be closed properly in any case
            if rs_image.logger is not None:
                rs_image.logger.close()

        # get processing infos
        self.proc_info = self.ac_input['options']['processing']

        # join results
        self._join_results_to_inObjs()  # sets self.outObjs

        # delete input arrays that are not needed anymore
        [inObj.delete_ac_input_arrays() for inObj in self.inObjs]

        return self.outObjs

    def _join_results_to_inObjs(self):
        """
        Join results of atmospheric correction to the input GMS objects.
        """

        self.logger.info('Joining results of atmospheric correction to input GMS objects.')
        # delete logger
        # -> otherwise logging in inObjs would open a second FileHandler to the same file (which is permitted)
        del self.logger

        self._join_data_ac()
        self._join_data_errors(bandwise=CFG.ac_bandwise_accuracy)
        self._join_mask_clouds()
        self._join_mask_confidence_array()

        # update masks (always do that because masks can also only contain one layer)
        [inObj.build_combined_masks_array() for inObj in self.inObjs]

        # update AC processing info
        [inObj.ac_options['processing'].update(self.proc_info) for inObj in self.inObjs]

        self.outObjs = self.inObjs

    def _join_data_ac(self):
        """
        Join ATMOSPHERICALLY CORRECTED ARRAY as 3D int8 or int16 BOA reflectance array, scaled to scale factor from
        config.
        """

        if self.results.data_ac is not None:
            for inObj in self.inObjs:
                self.logger.info('Joining image data to %s.' % (inObj.entity_ID if not inObj.subsystem else
                                                                '%s %s' % (inObj.entity_ID, inObj.subsystem)))

                assert isinstance(inObj, L1B_object)
                nodata = self.results.nodata[inObj.arr.xgsd]  # 2D mask with True outside of image coverage
                ac_bandNs = [bandN for bandN in inObj.arr.bandnames if bandN in self.results.data_ac.keys()]
                out_LBA = [bN.split('B0')[1] if bN.startswith('B0') else bN.split('B')[1] for bN in ac_bandNs]

                # update metadata #
                ###################

                inObj.arr_desc = 'BOA_Ref'
                inObj.MetaObj.bands = len(self.results.data_ac)
                inObj.MetaObj.PhysUnit = 'BOA_Reflectance in [0-%d]' % CFG.scale_factor_BOARef
                inObj.MetaObj.LayerBandsAssignment = out_LBA
                inObj.LayerBandsAssignment = out_LBA
                inObj.MetaObj.filter_layerdependent_metadata()

                ##################################################################################
                # join SURFACE REFLECTANCE as 3D int16 array, scaled to scale factor from config #
                ##################################################################################

                oF_refl, oZ_refl, oS_refl = get_outFillZeroSaturated(inObj.arr.dtype)
                surf_refl = np.dstack([self.results.data_ac[bandN] for bandN in ac_bandNs])
                surf_refl *= CFG.scale_factor_BOARef  # scale using scale factor (output is float16)

                # set AC nodata values to GMS outFill
                # NOTE: AC nodata contains a pixel mask where at least one band is no data
                #       => Setting these pixels to outZero would also reduce pixel values of surrounding pixels in
                #          spatial homogenization (because resampling only ignores -9999).
                #       It would be possible to generate a zero-data mask here for each subsystem and apply it after
                #       spatial homogenization. Alternatively zero-data pixels could be interpolated spectrally or
                #       spatially within L1A processor (also see issue #74).
                surf_refl[nodata] = oF_refl  # overwrite AC nodata values with GMS outFill

                # apply the original nodata mask (indicating background values)
                surf_refl[np.array(inObj.mask_nodata).astype(np.int8) == 0] = oF_refl

                # set AC NaNs to GMS outFill
                # NOTE: SICOR result has NaNs at no data positions AND non-clear positions
                if self.results.bad_data_value is np.nan:
                    surf_refl[np.isnan(surf_refl)] = oF_refl
                else:
                    surf_refl[surf_refl == self.results.bad_data_value] = oF_refl

                # use inObj.arr setter to generate a GeoArray
                inObj.arr = surf_refl.astype(inObj.arr.dtype)  # -> int16 (also converts NaNs to 0 if needed

        else:
            self.logger.warning('Atmospheric correction did not return a result for the input array. '
                                'Thus the output keeps NOT atmospherically corrected.')

    def _join_data_errors(self, bandwise=False):
        """Join ERRORS ARRAY as 3D or 2D int8 or int16 BOA reflectance array, scaled to scale factor from config.

        :param bandwise:    if True, a 3D array with bandwise information for each pixel is generated
        :return:
        """
        # TODO ac_error values are very close to 0 -> a scale factor of 255 yields int8 values below 10
        # TODO => better to stretch the whole array to values between 0 and 100 and save original min/max?
        if self.results.data_errors is not None:

            for inObj in self.inObjs:
                inObj.logger.info('Joining AC errors to %s.' % (inObj.entity_ID if not inObj.subsystem else
                                                                '%s %s' % (inObj.entity_ID, inObj.subsystem)))

                nodata = self.results.nodata[inObj.arr.xgsd]  # 2D mask with True outside of image coverage
                ac_bandNs = [bandN for bandN in inObj.arr.bandnames if bandN in self.results.data_ac.keys()]
                out_dtype = np.int8 if CFG.ac_scale_factor_errors <= 255 else np.int16
                out_nodata_val = get_outFillZeroSaturated(out_dtype)[0]

                # generate raw ac_errors array
                ac_errors = np.dstack([self.results.data_errors[bandN] for bandN in ac_bandNs])

                # apply scale factor from config to data pixels and overwrite nodata area with nodata value
                ac_errors *= CFG.ac_scale_factor_errors  # scale using scale factor (output is float16)
                ac_errors[np.isnan(ac_errors)] = out_nodata_val  # replace NaNs with outnodata
                ac_errors[nodata] = out_nodata_val  # set all positions where SICOR nodata mask is 1 to outnodata
                ac_errors = np.around(ac_errors).astype(out_dtype)  # round floats to next even int8/int16 value

                # average array over bands if no bandwise information is requested
                if not bandwise:
                    # in case of only one subsystem: directly compute median errors here
                    if len(self.inObjs) == 1:
                        ac_errors = np.median(ac_errors, axis=2).astype(ac_errors.dtype)

                    # in case of multiple subsystems: dont compute median here but first apply geometric homogenization
                    # -> median could only be computed for each subsystem separately
                    else:
                        pass

                # set inObj.ac_errors
                inObj.ac_errors = ac_errors  # setter generates a GeoArray with the same bandnames like inObj.arr

        elif not CFG.ac_estimate_accuracy:
            self.logger.info("Atmospheric correction did not provide a 'data_errors' array because "
                             "'ac_estimate_accuracy' was set to False in the job configuration.")
        else:
            self.logger.warning("Atmospheric correction did not provide a 'data_errors' array. Maybe due to "
                                "missing SNR model? GMS_object.ac_errors kept None.")

    def _join_mask_clouds(self):
        """
        Join CLOUD MASK as 2D uint8 array.
        NOTE: mask_clouds has also methods 'export_mask_rgb()', 'export_confidence_to_jpeg2000()', ...
        """

        if self.results.mask_clouds.mask_array is not None:
            mask_clouds_ac = self.results.mask_clouds.mask_array  # uint8 2D array

            joined = False
            for inObj in self.inObjs:

                # delete all previous cloud masks
                del inObj.mask_clouds  # FIXME validate if FMask product is within AC results

                # append mask_clouds only to the input GMS object with the same dimensions
                if inObj.arr.shape[:2] == mask_clouds_ac.shape:
                    inObj.logger.info('Joining mask_clouds to %s.' % (inObj.entity_ID if not inObj.subsystem else
                                                                      '%s %s' % (inObj.entity_ID, inObj.subsystem)))

                    inObj.mask_clouds = mask_clouds_ac
                    inObj.mask_clouds.legend = self.results.mask_clouds.mask_legend  # dict(value=string, string=value))
                    # FIXME legend is not used later

                    # set cloud mask nodata value
                    tgt_nodata = get_outFillZeroSaturated(mask_clouds_ac.dtype)[0]
                    ac_out_nodata = self.ac_input['options']['cld_mask']['nodata_value_mask']
                    if tgt_nodata not in self.results.mask_clouds.mask_legend.keys():
                        inObj.mask_clouds[inObj.mask_clouds[:] == ac_out_nodata] = tgt_nodata
                        mask_clouds_nodata = tgt_nodata
                    else:
                        warnings.warn('The cloud mask from AC output already uses the desired nodata value %s for the '
                                      'class %s. Using AC output nodata value %s.'
                                      % (tgt_nodata, self.results.mask_clouds.mask_legend[tgt_nodata], ac_out_nodata))
                        mask_clouds_nodata = ac_out_nodata

                    inObj.mask_clouds.nodata = mask_clouds_nodata

                    joined = True

            if not joined:
                self.logger.warning('Cloud mask has not been appended to one of the AC inputs because there was no'
                                    'input GMS object with the same dimensions.')

        else:
            self.logger.warning("Atmospheric correction did not provide a 'mask_clouds.mask_array' array. "
                                "GMS_object.mask_clouds kept None.")

    def _join_mask_confidence_array(self):
        """
        Join confidence array for mask_clouds.
        """
        if self.results.mask_clouds.mask_confidence_array is not None and CFG.ac_estimate_accuracy:
            cfd_arr = self.results.mask_clouds.mask_confidence_array  # float32 2D array, scaled [0-1, nodata 255]
            cfd_arr[cfd_arr == self.ac_input['options']['cld_mask']['nodata_value_mask']] = -1
            cfd_arr = (cfd_arr * CFG.scale_factor_BOARef).astype(np.int16)
            cfd_arr[cfd_arr == -CFG.scale_factor_BOARef] = get_outFillZeroSaturated(cfd_arr.dtype)[0]

            joined = False
            for inObj in self.inObjs:

                # append mask_clouds confidence only to the input GMS object with the same dimensions
                if inObj.arr.shape[:2] == cfd_arr.shape:
                    inObj.logger.info(
                        'Joining mask_clouds_confidence to %s.' % (inObj.entity_ID if not inObj.subsystem else
                                                                   '%s %s' % (inObj.entity_ID, inObj.subsystem)))

                    # set cloud mask confidence array
                    inObj.mask_clouds_confidence = GeoArray(cfd_arr, inObj.arr.gt, inObj.arr.prj,
                                                            nodata=get_outFillZeroSaturated(cfd_arr.dtype)[0])
                    joined = True

            if not joined:
                self.logger.warning('Cloud mask confidence array has not been appended to one of the AC inputs because '
                                    'there was no input GMS object with the same dimensions.')

        elif CFG.cloud_masking_algorithm[self.inObjs[0].satellite] == 'FMASK':
            self.logger.info("Cloud mask confidence array is not appended to AC outputs because "
                             "'cloud_masking_algorithm' was set to FMASK in the job configuration and FMASK does not "
                             "confidence arrays.")

        elif not CFG.ac_estimate_accuracy:
            self.logger.info("Cloud mask confidence array is not appended to AC outputs because "
                             "'ac_estimate_accuracy' was set to False in the job configuration.")
        else:
            self.logger.warning("Atmospheric correction did not provide a 'mask_confidence_array' array for "
                                "attribute 'mask_clouds. GMS_object.mask_clouds_confidence kept None.")
