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

import copy
import datetime
import functools
import glob
import json
import os
import re
import shutil
import sys
import warnings
import logging
from collections import OrderedDict
from itertools import chain
from typing import Iterable, List, Union, Generator, TYPE_CHECKING  # noqa F401  # flake8 issue
import psutil
import time
from pkg_resources import parse_version

import numpy as np
import spectral
from spectral.io import envi
from pandas import DataFrame, read_csv
from nested_dict import nested_dict

try:
    from osgeo import gdalnumeric
except ImportError:
    import gdalnumeric

from geoarray import GeoArray, NoDataMask, CloudMask
from py_tools_ds.geo.coord_grid import is_coord_grid_equal
from py_tools_ds.geo.projection import EPSG2WKT, WKT2EPSG, get_UTMzone, isProjectedOrGeographic
from py_tools_ds.geo.map_info import geotransform2mapinfo, mapinfo2geotransform
from py_tools_ds.geo.coord_calc import calc_FullDataset_corner_positions
from py_tools_ds.geo.coord_trafo import pixelToLatLon, pixelToMapYX, imXY2mapXY, imYX2mapYX
from py_tools_ds.numeric.array import get_array_tilebounds
from sicor.options import get_options as get_ac_options

from ..misc.logging import GMS_logger as DatasetLogger
from ..misc.logging import close_logger
from ..misc import database_tools as DB_T
from ..misc import path_generator as PG
from ..model.mgrs_tile import MGRS_tile
from ..model.metadata import \
    METADATA, get_dict_LayerOptTherm, metaDict_to_metaODict, get_LayerBandsAssignment, layerdependent_metadata
from ..options.config import GMS_config as CFG
from ..algorithms import geoprocessing as GEOP
from ..io import input_reader as INP_R
from ..io import output_writer as OUT_W
from ..misc import helper_functions as HLP_F
from ..misc import definition_dicts as DEF_D
from ..misc.locks import IOLock

if TYPE_CHECKING:
    from ..algorithms.L1C_P import L1C_object  # noqa F401  # flake8 issue

__author__ = 'Daniel Scheffler'


class GMS_object(object):
    # class attributes
    # NOTE: these attributes can be modified and seen by ALL GMS_object instances
    proc_status_all_GMSobjs = nested_dict()

    def __init__(self, pathImage=''):
        # add private attributes
        self._logger = None
        self._loggers_disabled = False
        self._log = ''
        self._MetaObj = None
        self._LayerBandsAssignment = None
        self._coreg_needed = None
        self._resamp_needed = None
        self._arr = None
        self._mask_nodata = None
        self._mask_clouds = None
        self._mask_clouds_confidence = None
        self._masks = None
        self._dem = None
        self._pathGen = None
        self._ac_options = {}
        self._ac_errors = None
        self._spat_homo_errors = None
        self._spec_homo_errors = None
        self._accuracy_layers = None
        self._dict_LayerOptTherm = None
        self._cloud_masking_algorithm = None
        self._coreg_info = None

        # defaults
        self.proc_level = 'init'
        self.image_type = ''
        self.satellite = ''
        self.sensor = ''
        self.subsystem = ''
        self.sensormode = ''
        self.acq_datetime = None  # also includes time, set by from_disk() and within L1A_P
        self.entity_ID = ''
        self.scene_ID = -9999
        self.filename = ''
        self.dataset_ID = -9999
        self.outInterleave = 'bsq'
        self.VAA_mean = None  # set by self.calc_mean_VAA()
        self.corner_lonlat = None
        self.trueDataCornerPos = []  # set by self.calc_corner_positions()
        self.trueDataCornerLonLat = []  # set by self.calc_corner_positions()
        self.fullSceneCornerPos = []  # set by self.calc_corner_positions()
        self.fullSceneCornerLonLat = []  # set by self.calc_corner_positions()
        # rows,cols,bands of the full scene (not of the subset as possibly represented by self.arr.shape)
        self.shape_fullArr = [None, None, None]
        self.arr_shape = 'cube'
        self.arr_desc = ''  # description of data units for self.arr
        self.arr_pos = None  # <tuple> in the form ((row_start,row_end),(col_start,col_end))
        self.tile_pos = None  # <list>, filled by self.get_tilepos()
        self.GeoTransProj_ok = True  # set by self.validate_GeoTransProj_GeoAlign()
        self.GeoAlign_ok = True  # set by self.validate_GeoTransProj_GeoAlign()
        self.masks_meta = {}  # set by self.build_L1A_masks()
        # self.CLD_obj               = CLD_P.GmsCloudClassifier(classifier=self.path_cloud_class_obj)

        # set pathes
        self.path_archive = ''
        self.path_procdata = ''
        self.ExtractedFolder = ''
        self.baseN = ''
        self.path_logfile = ''
        self.path_archive_valid = False
        self.path_InFilePreprocessor = None
        self.path_MetaPreprocessor = None

        self.job_ID = CFG.ID
        self.dataset_ID = -9999 if self.scene_ID == -9999 else \
            int(DB_T.get_info_from_postgreSQLdb(CFG.conn_database, 'scenes', ['datasetid'],
                                                {'id': self.scene_ID})[0][0])
        self.scenes_proc_ID = None  # set by Output writer after creation/update of db record in table scenes_proc
        self.mgrs_tiles_proc_ID = None  # set by Output writer after creation/update of db rec in table mgrs_tiles_proc
        self.MGRS_info = None
        self.lonlat_arr = None  # set by self.write_tiles_to_ENVIfile
        self.trueDataCornerUTM = None  # set by self.from_tiles

        self.mem_usage = {}

        # set pathes
        self.path_cloud_class_obj = ''

        # handle initialization arguments
        if pathImage:
            self.arr = pathImage  # run the setter for 'arr' which creates an Instance of GeoArray

    def __getstate__(self):
        """Defines how the attributes of GMS object are pickled."""

        self.close_loggers()
        del self.pathGen  # path generator can only be used for the current processing level

        # delete arrays if their in-mem size is to big to be pickled
        # => (avoids MaybeEncodingError: Error sending result: '[<gms_preprocessing.algorithms.L2C_P.L2C_object
        #    object at 0x7fc44f6399e8>]'. Reason: 'error("'i' format requires -2147483648 <= number <= 2147483647",)')
        if self.proc_level == 'L2C' and CFG.inmem_serialization:
            self.flush_array_data()

        return self.__dict__

    def __setstate__(self, ObjDict):
        """Defines how the attributes of GMS object are unpickled."""

        self.__dict__ = ObjDict
        # TODO unpickle meta to MetaObj

    def __deepcopy__(self, memodict={}):
        """Returns a deepcopy of the object excluding loggers because loggers are not serializable."""

        cls = self.__class__
        result = cls.__new__(cls)
        self.close_loggers()
        del self.pathGen  # has a logger
        memodict[id(self)] = result

        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memodict))
        return result

    def set_pathes(self):
        self.baseN = self.pathGen.get_baseN()
        self.path_procdata = self.pathGen.get_path_procdata()
        self.ExtractedFolder = self.pathGen.get_path_tempdir()
        self.path_logfile = self.pathGen.get_path_logfile()
        self.pathGen = PG.path_generator(self.__dict__)  # passes a logger in addition to previous attributes
        self.path_archive = self.pathGen.get_local_archive_path_baseN()

        if not CFG.inmem_serialization:
            self.path_InFilePreprocessor = os.path.join(self.ExtractedFolder, '%s%s_DN.bsq'
                                                        % (self.entity_ID,
                                                           ('_%s' % self.subsystem if self.subsystem else '')))
        else:  # keep data in memory
            self.path_InFilePreprocessor = None  # None: keeps all produced data in memory (numpy array attributes)

        self.path_MetaPreprocessor = self.path_archive

    def validate_pathes(self):
        if not os.path.isfile(self.path_archive) and not os.path.isdir(self.path_archive):
            self.logger.info("The %s dataset '%s' has not been processed earlier and no corresponding raw data archive"
                             "has been found at %s." % (self.sensor, self.entity_ID, self.path_archive))
            self.logger.info('Trying to download the dataset...')
            self.path_archive_valid = self._data_downloader(self.sensor, self.entity_ID)
        else:
            self.path_archive_valid = True

        if not CFG.inmem_serialization and self.ExtractedFolder and not os.path.isdir(self.ExtractedFolder):
            os.makedirs(self.ExtractedFolder)

        assert os.path.exists(self.path_archive), 'Invalid path to RAW data. File %s does not exist at %s.' \
                                                  % (os.path.basename(self.path_archive),
                                                     os.path.dirname(self.path_archive))
        assert isinstance(self.path_archive, str), 'Invalid path to RAW data. Got %s instead of string or unicode.' \
                                                   % type(self.path_archive)
        if not CFG.inmem_serialization and self.ExtractedFolder:
            assert os.path.exists(self.path_archive), \
                'Invalid path for temporary files. Directory %s does not exist.' % self.ExtractedFolder

    @property
    def logger(self):
        if self._loggers_disabled:
            return None
        if self._logger and self._logger.handlers[:]:
            return self._logger
        else:
            self._logger = DatasetLogger('log__' + self.baseN, fmt_suffix=self.scene_ID, path_logfile=self.path_logfile,
                                         log_level=CFG.log_level, append=True)
            return self._logger

    @logger.setter
    def logger(self, logger):
        assert isinstance(logger, logging.Logger) or logger in ['not set', None], \
            "GMS_obj.logger can not be set to %s." % logger

        # save prior logs
        # if logger is None and self._logger is not None:
        #    self.log += self.logger.captured_stream
        self._logger = logger

    @property  # FIXME does not work yet
    def log(self):
        """Returns a string of all logged messages until now."""

        return self._log

    @log.setter
    def log(self, string):
        assert isinstance(string, str), "'log' can only be set to a string. Got %s." % type(string)
        self._log = string

    @property
    def proc_status(self):
        # type: () -> str
        """
        Get the processing status of the current GMS_object (subclass) instance for the current processing level.

        Possible values: 'initialized', 'running', 'finished', 'failed'
        """
        # NOTE: self.proc_status_all_GMSobjs is a class attribute (visible and modifyable from any other subsystem)
        return self.proc_status_all_GMSobjs[self.scene_ID][self.subsystem][self.proc_level]

    @proc_status.setter
    def proc_status(self, new_status):
        # type: (str) -> None
        self.proc_status_all_GMSobjs[self.scene_ID][self.subsystem][self.proc_level] = new_status

    @property
    def GMS_identifier(self):
        return GMS_identifier(self.image_type, self.satellite, self.sensor, self.subsystem, self.proc_level,
                              self.dataset_ID, self.logger)

    @property
    def MetaObj(self):
        # TODO if there is no MetaObj -> create MetaObj by reading metadata from disk
        # reading from disk should use L1A_P.L1A_object.import_metadata -> so just return None

        return self._MetaObj

    @MetaObj.setter
    def MetaObj(self, MetaObj):
        assert isinstance(MetaObj, METADATA), "'MetaObj' can only be set to an instance of METADATA class. " \
                                              "Got %s." % type(MetaObj)
        self._MetaObj = MetaObj

    @MetaObj.deleter
    def MetaObj(self):
        if self._MetaObj and self._MetaObj.logger not in [None, 'not set']:
            self._MetaObj.logger.close()
            self._MetaObj.logger = None

        self._MetaObj = None

    @property
    def pathGen(self):
        # type: () -> PG.path_generator
        """
        Returns the path generator object for generating file pathes belonging to the GMS object.
        """

        if self._pathGen and self._pathGen.proc_level == self.proc_level:
            return self._pathGen
        else:
            self._pathGen = PG.path_generator(self.__dict__.copy(), MGRS_info=self.MGRS_info)

        return self._pathGen

    @pathGen.setter
    def pathGen(self, pathGen):
        assert isinstance(pathGen, PG.path_generator), 'GMS_object.pathGen can only be set to an instance of ' \
                                                       'path_generator. Got %s.' % type(pathGen)
        self._pathGen = pathGen

    @pathGen.deleter
    def pathGen(self):
        self._pathGen = None

    @property
    def subset(self):
        return [self.arr_shape, self.arr_pos]

    @property
    def LayerBandsAssignment(self):
        # FIXME merge that with self.MetaObj.LayerBandsAssignment
        # FIXME -> otherwise a change of LBA in MetaObj is not recognized here
        if self._LayerBandsAssignment:
            return self._LayerBandsAssignment
        elif self.image_type == 'RSD':
            self._LayerBandsAssignment = get_LayerBandsAssignment(self.GMS_identifier) \
                if self.sensormode != 'P' else get_LayerBandsAssignment(self.GMS_identifier, nBands=1)
            return self._LayerBandsAssignment
        else:
            return ''

    @LayerBandsAssignment.setter
    def LayerBandsAssignment(self, LBA_list):
        self._LayerBandsAssignment = LBA_list
        self.MetaObj.LayerBandsAssignment = LBA_list

    @property
    def dict_LayerOptTherm(self):
        if self._dict_LayerOptTherm:
            return self._dict_LayerOptTherm
        elif self.LayerBandsAssignment:
            self._dict_LayerOptTherm = get_dict_LayerOptTherm(self.GMS_identifier, self.LayerBandsAssignment)
            return self._dict_LayerOptTherm
        else:
            return None

    @property
    def georef(self):
        """Returns True if the current dataset can serve as spatial reference."""

        return True if self.image_type == 'RSD' and re.search(r'OLI', self.sensor, re.I) else False

    @property
    def coreg_needed(self):
        if self._coreg_needed is None:
            self._coreg_needed = not (self.dataset_ID == CFG.datasetid_spatial_ref)
        return self._coreg_needed

    @coreg_needed.setter
    def coreg_needed(self, value):
        self._coreg_needed = value

    @property
    def coreg_info(self):
        if not self._coreg_info:
            self._coreg_info = {
                'corrected_shifts_px': {'x': 0, 'y': 0},
                'corrected_shifts_map': {'x': 0, 'y': 0},
                'original map info': self.MetaObj.map_info,
                'updated map info': None,
                'shift_reliability': None,
                'reference scene ID': None,
                'reference entity ID': None,
                'reference geotransform': None,
                # reference projection must be the own projection in order to avoid overwriting with a wrong EPSG
                'reference projection': self.MetaObj.projection,
                'reference extent': {'rows': None, 'cols': None},
                'reference grid': [list(CFG.spatial_ref_gridx),
                                   list(CFG.spatial_ref_gridy)],
                'success': False
            }

        return self._coreg_info

    @coreg_info.setter
    def coreg_info(self, val):
        self._coreg_info = val

    @property
    def resamp_needed(self):
        if self._resamp_needed is None:
            gt = mapinfo2geotransform(self.MetaObj.map_info)
            self._resamp_needed = not is_coord_grid_equal(gt, CFG.spatial_ref_gridx,
                                                          CFG.spatial_ref_gridy)
        return self._resamp_needed

    @resamp_needed.setter
    def resamp_needed(self, value):
        self._resamp_needed = value

    @property
    def arr(self):
        # type: () -> GeoArray
        # TODO this must return a subset if self.subset is not None
        return self._arr

    @arr.setter
    def arr(self, *geoArr_initArgs):
        # TODO this must be able to handle subset inputs in tiled processing
        self._arr = GeoArray(*geoArr_initArgs)

        # set nodata value and geoinfos
        # NOTE: MetaObj is NOT gettable before import_metadata has been executed!
        if hasattr(self, 'MetaObj') and self.MetaObj:
            self._arr.nodata = self.MetaObj.spec_vals['fill']
            self._arr.gt = mapinfo2geotransform(self.MetaObj.map_info) if self.MetaObj.map_info else [0, 1, 0, 0, 0, -1]
            self._arr.prj = self.MetaObj.projection
        else:
            self._arr.nodata = DEF_D.get_outFillZeroSaturated(self._arr.dtype)[0]

        # set bandnames like this: [B01, .., B8A,]
        if self.LayerBandsAssignment:
            if len(self.LayerBandsAssignment) == self._arr.bands:
                self._arr.bandnames = self.LBA2bandnames(self.LayerBandsAssignment)
            else:
                warnings.warn("Cannot set 'bandnames' attribute of GMS_object.arr because LayerBandsAssignment has %s "
                              "bands and GMS_object.arr has %s bands."
                              % (len(self.LayerBandsAssignment), self._arr.bands))

    @arr.deleter
    def arr(self):
        self._arr = None

    @property
    def arr_meta(self):
        return self.MetaObj.to_odict()

    @property
    def mask_nodata(self):
        if self._mask_nodata is not None:
            if not self._mask_nodata.is_inmem and self._mask_nodata.bands > 1:
                # NoDataMask object self._mask_nodata points to multi-band image file (bands mask_nodata/mask_clouds)
                # -> read processes of not needed bands need to be avoided
                self._mask_nodata = NoDataMask(self._mask_nodata[:, :, 0],
                                               geotransform=self._mask_nodata.gt,
                                               projection=self._mask_nodata.prj)
            return self._mask_nodata

        elif self._masks:
            # return nodata mask from self.masks
            self._mask_nodata = NoDataMask(self._masks[:, :, 0],  # TODO use band names
                                           geotransform=self._masks.gt,
                                           projection=self._masks.prj)
            return self._mask_nodata

        elif isinstance(self.arr, GeoArray):
            self.logger.info('Calculating nodata mask...')
            self._mask_nodata = self.arr.mask_nodata  # calculates mask nodata if not already present
            return self._mask_nodata
        else:
            return None

    @mask_nodata.setter
    def mask_nodata(self, *geoArr_initArgs):
        if geoArr_initArgs[0] is not None:
            self._mask_nodata = NoDataMask(*geoArr_initArgs)
            self._mask_nodata.nodata = False
            self._mask_nodata.gt = self.arr.gt
            self._mask_nodata.prj = self.arr.prj
        else:
            del self.mask_nodata

    @mask_nodata.deleter
    def mask_nodata(self):
        self._mask_nodata = None

    @property
    def mask_clouds(self):
        if self._mask_clouds is not None:
            if not self._mask_clouds.is_inmem and self._mask_clouds.bands > 1:
                # CloudMask object self._mask_clouds points to multi-band image file on disk
                # (bands mask_nodata/mask_clouds) -> read processes of not needed bands need to be avoided
                self._mask_clouds = CloudMask(self._mask_clouds[:, :, 1],
                                              geotransform=self._mask_clouds.gt,
                                              projection=self._mask_clouds.prj)  # TODO add legend
            return self._mask_clouds

        elif self._masks and self._masks.bands > 1:  # FIXME this will not be secure if there are more than 2 bands
            # return cloud mask from self.masks
            self._mask_clouds = CloudMask(self._masks[:, :, 1],  # TODO use band names
                                          geotransform=self._masks.gt,
                                          projection=self._masks.prj)
            return self._mask_clouds
        else:
            return None  # TODO don't calculate cloud mask?

    @mask_clouds.setter
    def mask_clouds(self, *geoArr_initArgs):
        if geoArr_initArgs[0] is not None:  # FIXME shape validation?
            self._mask_clouds = CloudMask(*geoArr_initArgs)
            self._mask_clouds.nodata = 0
            self._mask_clouds.gt = self.arr.gt
            self._mask_clouds.prj = self.arr.prj
        else:
            del self.mask_clouds

    @mask_clouds.deleter
    def mask_clouds(self):
        self._mask_clouds = None

    @property
    def dem(self):
        """
        Returns an SRTM DEM in the exact dimension an pixel grid of self.arr as an instance of GeoArray.
        """

        if self._dem is None:
            self.logger.info('Generating DEM...')
            DC_args = (self.arr.box.boxMapXY, self.arr.prj, self.arr.xgsd, self.arr.ygsd)
            try:
                DC = INP_R.DEM_Creator(dem_sensor='SRTM', logger=self.logger)
                self._dem = DC.from_extent(*DC_args)
            except RuntimeError:
                self.logger.warning('SRTM DEM generation failed. Falling back to ASTER...')
                DC = INP_R.DEM_Creator(dem_sensor='ASTER', logger=self.logger)
                self._dem = DC.from_extent(*DC_args)

            self._dem.nodata = DEF_D.get_outFillZeroSaturated(self._dem.dtype)[0]
        return self._dem

    @dem.setter
    def dem(self, *geoArr_initArgs):
        if geoArr_initArgs[0] is not None:
            geoArr = GeoArray(*geoArr_initArgs)
            assert self._dem.shape[:2] == self.arr.shape[:2]

            self._dem = geoArr
            self._dem.nodata = DEF_D.get_outFillZeroSaturated(self._dem.dtype)[0]
            self._dem.gt = self.arr.gt
            self._dem.prj = self.arr.prj
        else:
            del self.dem

    @dem.deleter
    def dem(self):
        self._dem = None

    @property
    def masks(self):
        # if self.mask_nodata is not None and self.mask_clouds is not None and \
        #     self._masks is not None and self._masks.bands==1:

        #     self.build_combined_masks_array()

        return self._masks

    @masks.setter
    def masks(self, *geoArr_initArgs):
        """
        NOTE: This does not automatically update mask_nodata and mask_clouds BUT if mask_nodata and mask_clouds are
        None their getters will automatically synchronize!
        """

        if geoArr_initArgs[0] is not None:
            self._masks = GeoArray(*geoArr_initArgs)
            self._masks.nodata = 0
            self._masks.gt = self.arr.gt
            self._masks.prj = self.arr.prj
        else:
            del self.masks

    @masks.deleter
    def masks(self):
        self._masks = None

    @property
    def mask_clouds_confidence(self):
        return self._mask_clouds_confidence

    @mask_clouds_confidence.setter
    def mask_clouds_confidence(self, *geoArr_initArgs):
        if geoArr_initArgs[0] is not None:
            cnfArr = GeoArray(*geoArr_initArgs)

            assert cnfArr.shape == self.arr.shape[:2], \
                "The 'mask_clouds_confidence' GeoArray can only be instanced with an array of the same dimensions " \
                "like GMS_obj.arr. Got %s." % str(cnfArr.shape)

            # noinspection PyProtectedMember
            if cnfArr._nodata is None:
                cnfArr.nodata = DEF_D.get_outFillZeroSaturated(cnfArr.dtype)[0]
            cnfArr.gt = self.arr.gt
            cnfArr.prj = self.arr.prj
            cnfArr.bandnames = ['confidence']

            self._mask_clouds_confidence = cnfArr
        else:
            del self.mask_clouds_confidence

    @mask_clouds_confidence.deleter
    def mask_clouds_confidence(self):
        self._mask_clouds_confidence = None

    @property
    def ac_errors(self):
        """Returns an instance of GeoArray containing error information calculated by the atmospheric correction.

        :return:
        """

        return self._ac_errors

    @ac_errors.setter
    def ac_errors(self, *geoArr_initArgs):
        if geoArr_initArgs[0] is not None:
            errArr = GeoArray(*geoArr_initArgs)

            if CFG.ac_bandwise_accuracy:
                assert errArr.shape == self.arr.shape, \
                    "The 'ac_errors' GeoArray can only be instanced with an array of the same dimensions like " \
                    "GMS_obj.arr. Got %s." % str(errArr.shape)
            else:
                assert errArr.shape[:2] == self.arr.shape[:2], \
                    "The 'ac_errors' GeoArray can only be instanced with an array of the same X/Y dimensions like " \
                    "GMS_obj.arr. Got %s." % str(errArr.shape)

            # noinspection PyProtectedMember
            if errArr._nodata is None:
                errArr.nodata = DEF_D.get_outFillZeroSaturated(errArr.dtype)[0]
            errArr.gt = self.arr.gt
            errArr.prj = self.arr.prj
            errArr.bandnames = self.LBA2bandnames(self.LayerBandsAssignment) if errArr.ndim == 3 else ['median']

            self._ac_errors = errArr
        else:
            del self.ac_errors

    @ac_errors.deleter
    def ac_errors(self):
        self._ac_errors = None

    @property
    def spat_homo_errors(self):
        if not self._spat_homo_errors and self.coreg_info['shift_reliability'] is not None:
            errArr = GeoArray(np.full(self.arr.shape[:2], self.coreg_info['shift_reliability'], dtype=np.uint8),
                              geotransform=self.arr.geotransform,
                              projection=self.arr.projection,
                              bandnames=['shift_reliability'],
                              nodata=DEF_D.get_outFillZeroSaturated(np.uint8)[0])
            errArr[self.arr.mask_nodata.astype(np.int8) == 0] = errArr.nodata

            self._spat_homo_errors = errArr

        return self._spat_homo_errors

    @spat_homo_errors.deleter
    def spat_homo_errors(self):
        self._spat_homo_errors = None

    @property
    def spec_homo_errors(self):
        """Returns an instance of GeoArray containing error information calculated during spectral homogenization.

        :return:
        """

        return self._spec_homo_errors

    @spec_homo_errors.setter
    def spec_homo_errors(self, *geoArr_initArgs):
        if geoArr_initArgs[0] is not None:
            errArr = GeoArray(*geoArr_initArgs)

            if CFG.spechomo_bandwise_accuracy:
                assert errArr.shape == self.arr.shape, \
                    "The 'spec_homo_errors' GeoArray can only be instanced with an array of the same dimensions like " \
                    "GMS_obj.arr. Got %s." % str(errArr.shape)
            else:
                assert errArr.shape[:2] == self.arr.shape[:2], \
                    "The 'spec_homo_errors' GeoArray can only be instanced with an array of the same X/Y dimensions " \
                    "like GMS_obj.arr. Got %s." % str(errArr.shape)

            # noinspection PyProtectedMember
            if errArr._nodata is None:
                errArr.nodata = DEF_D.get_outFillZeroSaturated(errArr.dtype)[0]
            errArr.gt = self.arr.gt
            errArr.prj = self.arr.prj
            errArr.bandnames = self.LBA2bandnames(self.LayerBandsAssignment) if errArr.ndim == 3 else ['median']

            self._spec_homo_errors = errArr
        else:
            del self.spec_homo_errors

    @spec_homo_errors.deleter
    def spec_homo_errors(self):
        self._spec_homo_errors = None

    @property
    def accuracy_layers(self):
        return self._accuracy_layers

    @accuracy_layers.setter
    def accuracy_layers(self, *geoArr_initArgs):
        if geoArr_initArgs[0] is not None:
            acc_lay = GeoArray(*geoArr_initArgs)
            assert acc_lay.shape[:2] == self.arr.shape[:2],\
                "The 'accuracy_layers' GeoArray can only be instanced with an array of the same dimensions like " \
                "GMS_obj.arr. Got %s." % str(acc_lay.shape)

            # noinspection PyProtectedMember
            if acc_lay._nodata is None:
                acc_lay.nodata = DEF_D.get_outFillZeroSaturated(acc_lay.dtype)[0]
            acc_lay.gt = self.arr.gt
            acc_lay.prj = self.arr.prj

            if not acc_lay.bandnames:
                raise ValueError

            self._accuracy_layers = acc_lay
        else:
            del self._accuracy_layers

    @accuracy_layers.deleter
    def accuracy_layers(self):
        self._accuracy_layers = None

    @property
    def accuracy_layers_meta(self):
        if self._accuracy_layers is not None:
            return {'map info': geotransform2mapinfo(self._accuracy_layers.gt, self._accuracy_layers.projection),
                    'coordinate system string': self._accuracy_layers.projection,
                    'bands': self._accuracy_layers.bands,
                    'band names': list(self._accuracy_layers.bandnames),
                    'data ignore value': self._accuracy_layers.nodata}
        else:
            return None

    def generate_accuracy_layers(self):
        if not self.proc_level.startswith('L2'):
            self.logger.warning('Attempt to get %s accuracy layers failed - they are a Level 2 feature only.'
                                % self.proc_level)
            return None

        try:
            from ..algorithms.L2C_P import AccuracyCube
            self._accuracy_layers = AccuracyCube(self)  # don't use setter because it sets it to a GeoArray instance

        except ValueError as e:
            if str(e) == 'The given GMS_object contains no accuracy layers for combination.':
                if any([CFG.ac_estimate_accuracy, CFG.spathomo_estimate_accuracy, CFG.spechomo_estimate_accuracy]):
                    self.logger.warning('The given GMS_object contains no accuracy layers although computation '
                                        'of accurracy layers was enabled in job configuration.')
                else:
                    pass  # self._accuracy_layers keeps None
            else:
                raise

        except Exception as e:
            raise RuntimeError('Failed to generate AccuracyCube!', e)

    @property
    def cloud_masking_algorithm(self):
        if not self._cloud_masking_algorithm:
            self._cloud_masking_algorithm = CFG.cloud_masking_algorithm[self.satellite]
        return self._cloud_masking_algorithm

    @property
    def ac_options(self):
        # type: () -> dict
        """
        Returns the options dictionary needed as input for atmospheric correction. If an empty dictionary is returned,
        atmospheric correction is not yet available for the current sensor and will later be skipped.
        """

        if not self._ac_options:
            path_ac_options = CFG.path_custom_sicor_options or PG.get_path_ac_options(self.GMS_identifier)

            if path_ac_options and os.path.exists(path_ac_options):
                # don't validate because options contain pathes that do not exist on another server:
                opt_dict = get_ac_options(path_ac_options, validation=False)

                # update some file paths depending on the current environment
                opt_dict['DEM']['fn'] = CFG.path_dem_proc_srtm_90m
                opt_dict['ECMWF']['path_db'] = CFG.path_ECMWF_db
                opt_dict['S2Image'][
                    'S2_MSI_granule_path'] = None  # only a placeholder -> will always be None for GMS usage
                opt_dict['output'] = []  # outputs are not needed for GMS -> so
                opt_dict['report']['report_path'] = os.path.join(self.pathGen.get_path_procdata(), '[TYPE]')
                if 'uncertainties' in opt_dict:
                    if CFG.ac_estimate_accuracy:
                        opt_dict['uncertainties']['snr_model'] = PG.get_path_snr_model(self.GMS_identifier)
                    else:
                        del opt_dict['uncertainties']  # SICOR will not compute uncertainties if that key is missing

                # apply custom configuration
                opt_dict["logger"]['level'] = CFG.log_level
                opt_dict["ram"]['upper_limit'] = CFG.ac_max_ram_gb
                opt_dict["ram"]['unit'] = 'GB'
                opt_dict["AC"]['fill_nonclear_areas'] = CFG.ac_fillnonclear_areas
                opt_dict["AC"]['clear_area_labels'] = CFG.ac_clear_area_labels
                # opt_dict['AC']['n_cores'] = CFG.CPUs if CFG.allow_subMultiprocessing else 1

                self._ac_options = opt_dict
            else:
                self.logger.warning('There is no options file available for atmospheric correction. '
                                    'Atmospheric correction must be skipped.')

        return self._ac_options

    def get_copied_dict_and_props(self, remove_privates=False):
        # type: (bool) -> dict
        """Returns a copy of the current object dictionary including the current values of all object properties."""

        # loggers must be closed
        self.close_loggers()
        # this disables automatic recreation of loggers (otherwise loggers are created by using getattr()):
        self._loggers_disabled = True

        out_dict = self.__dict__.copy()

        # add properties
        property_names = [p for p in dir(self.__class__) if isinstance(getattr(self.__class__, p), property)]
        [out_dict.update({propK: copy.copy(getattr(self, propK))}) for propK in property_names]

        # remove private attributes
        if remove_privates:
            out_dict = {k: v for k, v in out_dict.items() if not k.startswith('_')}

        self._loggers_disabled = False  # enables automatic recreation of loggers

        return out_dict

    def attributes2dict(self, remove_privates=False):
        # type: (bool) -> dict
        """Returns a copy of the current object dictionary including the current values of all object properties."""

        # loggers must be closed
        self.close_loggers()
        # this disables automatic recreation of loggers (otherwise loggers are created by using getattr()):
        self._loggers_disabled = True

        out_dict = self.__dict__.copy()

        # add some selected property values
        for i in ['GMS_identifier', 'LayerBandsAssignment', 'coreg_needed', 'coreg_info', 'resamp_needed',
                  'dict_LayerOptTherm', 'georef', 'MetaObj']:
            if i == 'MetaObj':
                out_dict['meta_odict'] = self.MetaObj.to_odict()
            else:
                out_dict[i] = getattr(self, i)

        # remove private attributes
        if remove_privates:
            out_dict = {k: v for k, v in out_dict.items() if not k.startswith('_')}

        self._loggers_disabled = False  # enables automatic recreation of loggers
        return out_dict

    def _data_downloader(self, sensor, entity_ID):
        self.logger.info('Data downloader started.')
        success = False
        " > download source code for Landsat here < "
        if not success:
            self.logger.critical(
                "Download for %s dataset '%s' failed. No further processing possible." % (sensor, entity_ID))
            raise RuntimeError('Archive download failed.')
        return success

    @classmethod
    def from_disk(cls, tuple_GMS_subset):
        """Fills an already instanced GMS object with data from disk. Excludes array attributes in Python mode.

        :param tuple_GMS_subset:    <tuple> e.g. ('/path/gms_file.gms', ['cube', None])
        """
        GMS_obj = cls()

        path_GMS_file = tuple_GMS_subset[0]
        GMSfileDict = INP_R.GMSfile2dict(path_GMS_file)

        # copy all attributes from GMS file (private attributes are not touched since they are not included in GMS file)

        # set MetaObj first in order to make some getters and setters work
        GMS_id = GMS_identifier(image_type=GMSfileDict['image_type'], satellite=GMSfileDict['satellite'],
                                sensor=GMSfileDict['sensor'], subsystem=GMSfileDict['subsystem'],
                                proc_level=GMSfileDict['proc_level'], dataset_ID=GMSfileDict['dataset_ID'], logger=None)
        GMS_obj.MetaObj = METADATA(GMS_id).from_odict(GMSfileDict['meta_odict'])

        for key, value in GMSfileDict.items():
            if key in ['GMS_identifier', 'georef', 'dict_LayerOptTherm']:
                continue  # properties that should better be created on the fly
            elif key == 'acq_datetime':
                GMS_obj.acq_datetime = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f%z')
            else:
                try:
                    setattr(GMS_obj, key, value)
                except Exception:
                    raise AttributeError("Can't set attribute %s." % key)

        GMS_obj.arr_shape, GMS_obj.arr_pos = tuple_GMS_subset[1]

        GMS_obj.arr = GMS_obj.pathGen.get_path_imagedata()
        # self.mask_nodata and self.mask_clouds are auto-synchronized via self.masks (see their getters):
        GMS_obj.masks = GMS_obj.pathGen.get_path_maskdata()
        GMS_obj.accuracy_layers = GMS_obj.pathGen.get_path_accuracylayers()

        return GMS_obj

    @classmethod
    def from_sensor_subsystems(cls, list_GMS_objs):
        # type: (List[GMS_object]) -> GMS_object
        """Merge separate GMS objects belonging to the same scene-ID into ONE GMS object.

        :param list_GMS_objs:   <list> of GMS objects covering the same geographic area but representing different
                                sensor subsystems (e.g. 3 GMS_objects for Sentinel-2 10m/20m/60m bands)
        """
        GMS_obj_merged = cls()

        # assertions
        assert len(list_GMS_objs) > 1, "'GMS_object.from_sensor_subsystems()' expects multiple input GMS objects. " \
                                       "Got %d." % len(list_GMS_objs)
        assert all([is_coord_grid_equal(list_GMS_objs[0].arr.gt, *obj.arr.xygrid_specs) for obj in list_GMS_objs[1:]]),\
            "The input GMS objects must have the same pixel grid. Received: %s" \
            % np.array([obj.arr.xygrid_specs for obj in list_GMS_objs])
        assert len(list(set([GMS_obj.proc_level for GMS_obj in list_GMS_objs]))) == 1, \
            "The input GMS objects for GMS_object.from_sensor_subsystems() must have the same processing level."
        subsystems = [GMS_obj.subsystem for GMS_obj in list_GMS_objs]
        assert len(subsystems) == len(list(set(subsystems))), \
            "The input 'list_GMS_objs' contains duplicates: %s" % subsystems

        ##################
        # merge logfiles #
        ##################

        # read all logs into DataFrame, sort it by the first column
        [GMS_obj.close_loggers() for GMS_obj in list_GMS_objs]  # close the loggers of the input objects
        paths_inLogs = [GMS_obj.pathGen.get_path_logfile() for GMS_obj in list_GMS_objs]
        allLogs_df = DataFrame()
        for log in paths_inLogs:
            df = read_csv(log, sep='\n', delimiter=None, header=None,  # no delimiter needed
                          engine='python')  # engine suppresses a pandas warning
            allLogs_df = allLogs_df.append(df)

        allLogs_df = allLogs_df.sort_values(0)  # sorting uses timestamps that appear on first position in logs
        allLogs_df = allLogs_df.drop_duplicates()  # otherwise, e.g., logs from AC would appear 3 times for S2A

        # set common metadata, needed for logfile
        GMS_obj_merged.baseN = list_GMS_objs[0].pathGen.get_baseN(merged_subsystems=True)
        GMS_obj_merged.path_logfile = list_GMS_objs[0].pathGen.get_path_logfile(merged_subsystems=True)
        GMS_obj_merged.scene_ID = list_GMS_objs[0].scene_ID

        # write the merged logfile and flush previous logger
        np.savetxt(GMS_obj_merged.path_logfile, np.array(allLogs_df), delimiter=None, fmt="%s")
        GMS_obj_merged.close_loggers()

        # log
        GMS_obj_merged.logger.info('Merging the subsystems %s to a single GMS object...'
                                   % ', '.join([GMS_obj.subsystem for GMS_obj in list_GMS_objs]))

        ##################
        # MERGE METADATA #
        ##################

        # copy all attributes from the first input GMS file (private attributes are not touched)
        for key, value in list_GMS_objs[0].__dict__.copy().items():
            if key in ['GMS_identifier', 'georef', 'dict_LayerOptTherm']:
                continue  # properties that should better be created on the fly
            elif key in ['baseN', 'path_logfile', 'scene_ID', 'subsystem']:
                continue  # either previously set with common values or not needed for merged GMS_object
            try:
                setattr(GMS_obj_merged, key, value)
            except Exception:
                raise AttributeError("Can't set attribute %s." % key)

        # update LayerBandsAssignment and get full list of output bandnames
        from .metadata import get_LayerBandsAssignment
        # use identifier of first input GMS object for getting LBA (respects current proc_level):
        gms_idf = list_GMS_objs[0].GMS_identifier
        GMS_obj_merged.LayerBandsAssignment = get_LayerBandsAssignment(gms_idf, return_fullLBA=True)
        bandnames = ['B%s' % i if len(i) == 2 else 'B0%s' % i for i in GMS_obj_merged.LayerBandsAssignment]

        # update layer-dependent metadata with respect to remaining input GMS objects
        GMS_obj_merged.MetaObj.LayerBandsAssignment = GMS_obj_merged.LayerBandsAssignment
        GMS_obj_merged.MetaObj.Subsystem = ''

        GMS_obj_merged.subsystem = ''
        del GMS_obj_merged.pathGen  # must be refreshed because subsystem is now ''
        GMS_obj_merged.close_loggers()  # must also be refreshed because it depends on pathGen

        for attrN in layerdependent_metadata:
            # combine values from separate subsystems to a single value
            attrDic_fullLBA = {}
            for GMS_obj in list_GMS_objs:
                attr_val = getattr(GMS_obj.MetaObj, attrN)
                if isinstance(attr_val, list):
                    attrDic_fullLBA.update(dict(zip(GMS_obj.LayerBandsAssignment, attr_val)))
                elif isinstance(attr_val, (dict, OrderedDict)):
                    attrDic_fullLBA.update(attr_val)
                else:
                    raise ValueError(attrN)

            # update the attribute in self.MetaObj
            if attrDic_fullLBA:
                val2set = [attrDic_fullLBA[bN] for bN in GMS_obj_merged.LayerBandsAssignment] \
                    if isinstance(getattr(list_GMS_objs[0].MetaObj, attrN), list) else attrDic_fullLBA
                setattr(GMS_obj_merged.MetaObj, attrN, val2set)

        ####################
        # MERGE ARRAY DATA #
        ####################

        # find the common extent. NOTE: boundsMap is expected in the order [xmin,xmax,ymin,ymax]
        geoExtents = np.array([GMS_obj.arr.box.boundsMap for GMS_obj in list_GMS_objs])
        common_extent = (min(geoExtents[:, 0]), max(geoExtents[:, 1]), min(geoExtents[:, 2]), max(geoExtents[:, 3]))

        # overwrite array data with merged arrays, clipped to common_extent and reordered according to FullLayerBandsAss
        for attrname in ['arr', 'ac_errors', 'dem', 'mask_nodata', 'mask_clouds', 'mask_clouds_confidence', 'masks']:

            # get current attribute of each subsystem without running property getters
            all_arrays = [getattr(GMS_obj, '_%s' % attrname) for GMS_obj in list_GMS_objs]

            # get the same geographical extent for each input GMS object
            if len(set(tuple(ext) for ext in geoExtents.tolist())) > 1:
                # in case of different extents
                geoArrs_same_extent = []

                for geoArr in all_arrays:

                    if geoArr is not None:
                        # FIXME mask_clouds_confidence is no GeoArray until here
                        # FIXME -> has no nodata value -> calculation throughs warning
                        geoArr_same_extent = \
                            GeoArray(*geoArr.get_mapPos(
                                mapBounds=np.array(common_extent)[[0, 2, 1, 3]],  # pass (xmin, ymin, xmax, ymax)
                                mapBounds_prj=geoArr.prj),
                                     bandnames=list(geoArr.bandnames.keys()),
                                     nodata=geoArr.nodata)
                        geoArrs_same_extent.append(geoArr_same_extent)
                    else:
                        # e.g. in case of cloud mask that is only appended to the GMS object with the same
                        # spatial resolution)
                        geoArrs_same_extent.append(None)

            else:
                # skip get_mapPos() if all input GMS objects have the same extent
                geoArrs_same_extent = all_arrays

            # validate output GeoArrays #
            #############################

            if len([gA for gA in geoArrs_same_extent if gA is not None]) > 1:
                equal_bounds = all([geoArrs_same_extent[0].box.boundsMap == gA.box.boundsMap
                                    for gA in geoArrs_same_extent[1:]])
                equal_epsg = all([geoArrs_same_extent[0].epsg == gA.epsg for gA in geoArrs_same_extent[1:]])
                equal_xydims = all([geoArrs_same_extent[0].shape[:2] == gA.shape[:2] for gA in geoArrs_same_extent[1:]])
                if not all([equal_bounds, equal_epsg, equal_xydims]):
                    raise RuntimeError('Something went wrong during getting the same geographical extent for all the '
                                       'input GMS objects. The extents, projections or pixel dimensions of the '
                                       'calculated input GMS objects are not equal.')

            # set output arrays #
            #####################

            # handle those arrays where bands have to be reordered according to FullLayerBandsAssignment
            if attrname in ['arr', 'ac_errors'] and list(set(geoArrs_same_extent)) != [None]:
                # check that each desired band name for the current attribute is provided by one of the input
                # GMS objects
                available_bandNs = list(chain.from_iterable([list(gA.bandnames) for gA in geoArrs_same_extent]))
                for bN in bandnames:
                    if bN not in available_bandNs:
                        raise ValueError("The given input GMS objects (subsystems) do not provide a bandname '%s' for "
                                         "the attribute '%s'. Available band names amongst all input GMS objects are: "
                                         "%s" % (bN, attrname, str(available_bandNs)))

                # merge arrays
                def get_band(bandN):
                    return [gA[bandN] for gA in geoArrs_same_extent if gA and bandN in gA.bandnames][0]
                full_geoArr = GeoArray(np.dstack([get_band(bandN) for bandN in bandnames]),
                                       geoArrs_same_extent[0].gt, geoArrs_same_extent[0].prj,
                                       bandnames=bandnames,
                                       nodata=geoArrs_same_extent[0].nodata)

                # handle CFG.ac_bandwise_accuracy (average ac_errors if needed)
                # NOTE: full_geoArr will only have 3 dims in case of multiple subsystems
                #       -> median cannot directly computed during AC due to different GSDs of the subsystems
                #       -> first perform spatial homogenization, directly after that compute median
                #       -> this is not done later (e.g., in  L2C) to avoid memory overflows in L2B or L2C
                if attrname == 'ac_errors' and not CFG.ac_bandwise_accuracy and full_geoArr.bands > 1:
                    full_geoArr = np.median(full_geoArr, axis=2).astype(full_geoArr.dtype)

                setattr(GMS_obj_merged, attrname, full_geoArr)

            # handle the remaining arrays
            else:
                # masks, dem, mask_nodata, mask_clouds, mask_clouds_confidence
                if attrname == 'dem':
                    # use the DEM of the first input object
                    # (if the grid is the same, the DEMs should be the same anyway)
                    GMS_obj_merged.dem = geoArrs_same_extent[0]

                elif attrname == 'mask_nodata':
                    # must not be merged -> self.arr is already merged, so just recalculate it (np.all)
                    GMS_obj_merged.mask_nodata = GMS_obj_merged.calc_mask_nodata(overwrite=True)

                elif attrname == 'mask_clouds':
                    # possibly only present in ONE subsystem (set by atm. Corr.)
                    mask_clouds = [msk for msk in geoArrs_same_extent if msk is not None]
                    if len(mask_clouds) > 1:
                        raise ValueError('Expected mask clouds in only one subsystem. Got %s.' % len(mask_clouds))
                    GMS_obj_merged.mask_clouds = mask_clouds[0] if mask_clouds else None

                elif attrname == 'mask_clouds_confidence':
                    # possibly only present in ONE subsystem (set by atm. Corr.)
                    mask_clouds_conf = [msk for msk in geoArrs_same_extent if msk is not None]
                    if len(mask_clouds_conf) > 1:
                        raise ValueError(
                            'Expected mask_clouds_conf in only one subsystem. Got %s.' % len(mask_clouds_conf))
                    GMS_obj_merged.mask_clouds_confidence = mask_clouds_conf[0] if mask_clouds_conf else None

                elif attrname == 'masks':
                    # self.mask_nodata and self.mask_clouds will already be set here -> so just recreate it from there
                    GMS_obj_merged.masks = None

        # avoid unequal nodata edges between individual layers (resampling artifacts etc.) #
        ####################################################################################

        # get pixel values of areas that have not been atmospherically corrected (non-clear)
        nonclear_labels = [lbl for lbl in ["Clear", "Snow", "Water", "Shadow", "Cirrus", "Cloud"]
                           if lbl not in CFG.ac_clear_area_labels]
        cloud_mask_legend = DEF_D.get_mask_classdefinition('mask_clouds', GMS_obj_merged.satellite)
        nonclear_pixVals = [cloud_mask_legend[lbl] for lbl in nonclear_labels]

        # apply cloud mask to image data and all products derived from image data
        # (only if image data represents BOA-Ref and cloud areas are not to be filled with TOA-Ref)

        if re.search(r'BOA_Reflectance', GMS_obj_merged.MetaObj.PhysUnit, re.I) and not CFG.ac_fillnonclear_areas:
            # fill non-clear areas with no data values (for all bands)
            for pixVal in nonclear_pixVals:
                mask_nonclear = GMS_obj_merged.mask_clouds[:] == pixVal
                GMS_obj_merged.arr[mask_nonclear] = DEF_D.get_outFillZeroSaturated(GMS_obj_merged.arr.dtype)[0]

                if GMS_obj_merged.ac_errors:
                    GMS_obj_merged.ac_errors[mask_nonclear] = \
                        DEF_D.get_outFillZeroSaturated(GMS_obj_merged.ac_errors.dtype)[0]

        # update no data mask (adds all pixels to no data where at least one band has no data)
        GMS_obj_merged.calc_mask_nodata(overwrite=True)

        # apply updated nodata mask to array data (only to no data area, not to non-clear area)
        # => this sets all pixels to no data where at least one band has no data
        #    NOTE: This may cause the cloud mask not exactly match the holes in self.arr so that there may be small
        #          gaps between the cloud edge and where the image data begins. This is due to resampling, e.g. from
        #          Sentinel-2 60m grid to Landsat 30 m grid. Nodata mask marks those areas as no data although there is
        #          no cloud at exactly that pixel. This is ok!
        area2replace = np.all([GMS_obj_merged.mask_nodata[:] == 0] +
                              [GMS_obj_merged.mask_clouds[:] != pixVal for pixVal in nonclear_pixVals], axis=0) \
            if GMS_obj_merged.mask_clouds is not None else GMS_obj_merged.mask_nodata[:] == 0

        for attrname in ['arr', 'ac_errors']:
            attr_val = getattr(GMS_obj_merged, attrname)

            if attr_val is not None:
                attr_val[area2replace] = DEF_D.get_outFillZeroSaturated(attr_val.dtype)[0]
                setattr(GMS_obj_merged, attrname, attr_val)

        # recreate self.masks
        GMS_obj_merged.build_combined_masks_array()

        # update array-dependent metadata
        GMS_obj_merged.MetaObj.cols = GMS_obj_merged.arr.cols
        GMS_obj_merged.MetaObj.rows = GMS_obj_merged.arr.rows
        GMS_obj_merged.MetaObj.bands = GMS_obj_merged.arr.bands
        GMS_obj_merged.MetaObj.map_info = geotransform2mapinfo(GMS_obj_merged.arr.gt, GMS_obj_merged.arr.prj)
        GMS_obj_merged.MetaObj.projection = GMS_obj_merged.arr.prj

        # update corner coordinates  # (calc_corner_positions is a method of L1A_object)
        GMS_obj_merged.calc_corner_positions()

        # set shape of full array
        GMS_obj_merged.shape_fullArr = GMS_obj_merged.arr.shape

        return GMS_obj_merged

    @classmethod
    def from_tiles(cls, list_GMS_tiles):
        # type: (list) -> GMS_object
        """Merge separate GMS objects with different spatial coverage but belonging to one scene-ID to ONE GMS object.

        :param list_GMS_tiles: <list> of GMS objects that have been created by cut_GMS_obj_into_blocks()
        """
        GMS_obj = cls()

        if 'IMapUnorderedIterator' in str(type(list_GMS_tiles)):
            list_GMS_tiles = list(list_GMS_tiles)

        # copy all attributes except of array attributes
        tile1 = list_GMS_tiles[0]
        [setattr(GMS_obj, i, getattr(tile1, i)) for i in tile1.__dict__
         if not callable(getattr(tile1, i)) and not isinstance(getattr(tile1, i), (np.ndarray, GeoArray))]

        # MERGE ARRAY-ATTRIBUTES
        list_arraynames = [i for i in tile1.__dict__ if not callable(getattr(tile1, i)) and
                           isinstance(getattr(tile1, i), (np.ndarray, GeoArray))]
        list_arraynames = ['_arr'] + [i for i in list_arraynames if
                                      i != '_arr']  # list must start with _arr, otherwise setters will not work

        for arrname in list_arraynames:
            samplearray = getattr(tile1, arrname)
            assert isinstance(samplearray, (np.ndarray, GeoArray)), \
                'Received a %s object for attribute %s. Expected a numpy array or an instance of GeoArray.' \
                % (type(samplearray), arrname)
            is_3d = samplearray.ndim == 3
            bands = (samplearray.shape[2],) if is_3d else ()  # dynamic -> works for arr, cld_arr,...
            target_shape = tuple(GMS_obj.shape_fullArr[:2]) + bands
            target_dtype = samplearray.dtype
            merged_array = GMS_obj._merge_arrays(list_GMS_tiles, arrname, target_shape, target_dtype)

            setattr(GMS_obj, arrname if not arrname.startswith('_') else arrname[1:],
                    merged_array)  # use setters if possible
            # NOTE: this asserts that each attribute starting with '_' has also a property with a setter!

        # UPDATE ARRAY-DEPENDENT ATTRIBUTES
        GMS_obj.arr_shape = 'cube'
        GMS_obj.arr_pos = None

        # update MetaObj attributes
        GMS_obj.MetaObj.cols = GMS_obj.arr.cols
        GMS_obj.MetaObj.rows = GMS_obj.arr.rows
        GMS_obj.MetaObj.bands = GMS_obj.arr.bands
        GMS_obj.MetaObj.map_info = geotransform2mapinfo(GMS_obj.arr.gt, GMS_obj.arr.prj)
        GMS_obj.MetaObj.projection = GMS_obj.arr.prj

        # calculate data_corners_imXY (mask_nodata is always an array here because get_mapPos always returns an array)
        corners_imYX = calc_FullDataset_corner_positions(
            GMS_obj.mask_nodata, assert_four_corners=False, algorithm='shapely')
        GMS_obj.trueDataCornerPos = [(YX[1], YX[0]) for YX in corners_imYX]  # [UL, UR, LL, LR]

        # calculate trueDataCornerLonLat
        data_corners_LatLon = pixelToLatLon(GMS_obj.trueDataCornerPos,
                                            geotransform=GMS_obj.arr.gt, projection=GMS_obj.arr.prj)
        GMS_obj.trueDataCornerLonLat = [(YX[1], YX[0]) for YX in data_corners_LatLon]

        # calculate trueDataCornerUTM
        data_corners_utmYX = pixelToMapYX(GMS_obj.trueDataCornerPos, geotransform=GMS_obj.arr.gt,
                                          projection=GMS_obj.arr.prj)  # FIXME asserts gt in UTM coordinates
        GMS_obj.trueDataCornerUTM = [(YX[1], YX[0]) for YX in data_corners_utmYX]

        return GMS_obj

    def get_subset_obj(self, imBounds=None, mapBounds=None, mapBounds_prj=None, out_prj=None, logmsg=None,
                       progress=False, v=False):
        # type: (tuple, tuple, str, str, str, bool, bool) -> Union[GMS_object, None]
        """Return a subset of the given GMS object, based on the given bounds coordinates.

        Array attributes are clipped and relevant metadata keys are updated according to new extent. In case the subset
        does not contain any data but only no-data values, None is returned.

        :param imBounds:        <tuple> tuple of image coordinates in the form (xmin,xmax,ymin,ymax)
        :param mapBounds:       <tuple> tuple of map coordinates in the form (xmin,xmax,ymin,ymax)
        :param mapBounds_prj:   <str> a WKT string containing projection of the given map bounds
                                (can be different to projection of the GMS object; ignored if map bounds not given)
        :param out_prj:         <str> a WKT string containing output projection.
                                If not given, the projection of self.arr is used.
        :param logmsg:          <str> a message to be logged when this method is called
        :param progress:        <bool> whether to show progress bar (default: False)
        :param v:               <bool> verbose mode (default: False)
        :return:                <GMS_object> the GMS object subset
        """

        if logmsg:
            self.logger.info(logmsg)

        # copy object
        from ..misc.helper_functions import get_parentObjDict
        parentObjDict = get_parentObjDict()
        sub_GMS_obj = parentObjDict[self.proc_level](*HLP_F.initArgsDict[self.proc_level])  # init
        sub_GMS_obj.__dict__.update(
            {k: getattr(self, k) for k in self.__dict__.keys()
             if not isinstance(getattr(self, k), (GeoArray, np.ndarray))}.copy())

        sub_GMS_obj = copy.deepcopy(sub_GMS_obj)

        # clip all array attributes using the given bounds
        # list_arraynames = [i for i in self.__dict__ if not callable(getattr(self, i)) and \
        #                   isinstance(getattr(self, i), np.ndarray)]
        list_arraynames = [i for i in ['arr', 'masks', 'ac_errors', 'mask_clouds_confidence', 'spec_homo_errors',
                                       'accuracy_layers']
                           if hasattr(self, i) and getattr(self, i) is not None]  # FIXME hardcoded
        assert list_arraynames
        assert imBounds or mapBounds, "Either 'imBounds' or 'mapBounds' must be given. Got nothing."

        # calculate mapBounds if not already given
        if not mapBounds:
            rS, rE, cS, cE = imBounds
            (xmin, ymax), (xmax, ymin) = [imXY2mapXY((imX, imY), self.arr.gt) for imX, imY in
                                          [(cS, rS), (cE + 1, rE + 1)]]
            mapBounds_prj = self.arr.projection
        else:
            xmin, xmax, ymin, ymax = mapBounds

        # avoid disk IO if requested area is within the input array # TODO

        ####################################################################
        # subset all array attributes and update directly related metadata #
        ####################################################################

        for arrname in list_arraynames:
            # get input data for array subsetting
            geoArr = getattr(self, arrname)

            # get subsetted and (possibly) reprojected array
            subArr = GeoArray(*geoArr.get_mapPos((xmin, ymin, xmax, ymax), mapBounds_prj,
                                                 out_prj=out_prj or geoArr.prj,
                                                 rspAlg='near' if arrname == 'masks' else 'cubic',
                                                 progress=progress),
                              bandnames=list(geoArr.bandnames), nodata=geoArr.nodata)

            # show result
            if v:
                subArr.show(figsize=(10, 10))

            # update array-related attributes of sub_GMS_obj
            if arrname == 'arr':
                # return None in case the subset object contains only nodata
                if subArr.min() == subArr.max() and \
                   np.std(subArr) == 0 and \
                   np.unique(subArr) == subArr.nodata:
                    return None

                sub_GMS_obj.MetaObj.map_info = geotransform2mapinfo(subArr.gt, subArr.prj)
                sub_GMS_obj.MetaObj.projection = subArr.prj
                sub_GMS_obj.MetaObj.rows, sub_GMS_obj.MetaObj.cols = subArr.arr.shape[:2]
                sub_GMS_obj.MetaObj.CS_UTM_ZONE = get_UTMzone(prj=subArr.prj)  # FIXME only works for UTM
                sub_GMS_obj.MetaObj.CS_EPSG = WKT2EPSG(subArr.prj)
            elif arrname == 'masks':
                sub_GMS_obj.masks_meta['map info'] = geotransform2mapinfo(subArr.gt, subArr.prj)
                sub_GMS_obj.masks_meta['coordinate system string'] = subArr.prj
                sub_GMS_obj.masks_meta['lines'], sub_GMS_obj.masks_meta['samples'] = subArr.arr.shape[:2]
                sub_GMS_obj.masks_meta['CS_UTM_ZONE'] = get_UTMzone(prj=subArr.prj)  # FIXME only works for UTM
                sub_GMS_obj.masks_meta['CS_EPSG'] = WKT2EPSG(subArr.prj)
            else:
                # other layers are either not written (i.e. have no separate meta)
                # or their meta is directly derived from the corresponding array
                pass

            delattr(sub_GMS_obj,
                    arrname)  # connected filePath must be disconnected because projection change will be rejected
            setattr(sub_GMS_obj, arrname, subArr)

        # copy subset mask data to mask_nodata and mask_clouds
        sub_GMS_obj.mask_nodata = sub_GMS_obj.masks[:, :, 0]  # ==> getters will automatically return it from self.masks
        # FIXME not dynamic:
        sub_GMS_obj.mask_clouds = sub_GMS_obj.masks[:, :, 1] if sub_GMS_obj.masks.bands > 1 else None

        ###################
        # update metadata #
        ###################

        # update arr_pos
        sub_GMS_obj.arr_shape = 'block'
        if imBounds is not None:
            rS, rE, cS, cE = imBounds
            sub_GMS_obj.arr_pos = ((rS, rE), (cS, cE))
        else:
            pass  # FIXME how to set arr_pos in that case?

        # calculate new attributes 'corner_utm' and 'corner_lonlat'
        rows, cols, bands = sub_GMS_obj.arr.shape
        ULxy, URxy, LLxy, LRxy = [[0, 0], [cols - 1, 0], [0, rows - 1], [cols - 1, rows - 1]]
        # FIXME asserts gt in UTM coordinates:
        utm_coord_YX = pixelToMapYX([ULxy, URxy, LLxy, LRxy], geotransform=subArr.gt, projection=subArr.prj)
        # ULyx,URyx,LLyx,LRyx:
        lonlat_coord = pixelToLatLon([ULxy, URxy, LLxy, LRxy], geotransform=subArr.gt, projection=subArr.prj)
        sub_GMS_obj.corner_utm = [[YX[1], YX[0]] for YX in utm_coord_YX]  # ULxy,URxy,LLxy,LRxy
        sub_GMS_obj.corner_lonlat = [[YX[1], YX[0]] for YX in lonlat_coord]  # ULxy,URxy,LLxy,LRxy

        # calculate 'bounds_LonLat' and 'bounds_utm'
        sub_GMS_obj.bounds_LonLat = HLP_F.corner_coord_to_minmax(sub_GMS_obj.corner_lonlat)
        sub_GMS_obj.bounds_utm = HLP_F.corner_coord_to_minmax(sub_GMS_obj.corner_utm)

        # calculate data_corners_imXY (mask_nodata is always an array here because get_mapPos always returns an array)
        corners_imYX = calc_FullDataset_corner_positions(
            sub_GMS_obj.mask_nodata, assert_four_corners=False, algorithm='shapely')
        sub_GMS_obj.trueDataCornerPos = [(YX[1], YX[0]) for YX in corners_imYX]

        # calculate trueDataCornerLonLat
        data_corners_LatLon = pixelToLatLon(sub_GMS_obj.trueDataCornerPos,
                                            geotransform=subArr.gt, projection=subArr.prj)
        sub_GMS_obj.trueDataCornerLonLat = [(YX[1], YX[0]) for YX in data_corners_LatLon]

        # calculate trueDataCornerUTM
        if isProjectedOrGeographic(subArr.prj) == 'projected':
            data_corners_utmYX = [imYX2mapYX(imYX, gt=subArr.gt) for imYX in corners_imYX]
            sub_GMS_obj.trueDataCornerUTM = [(YX[1], YX[0]) for YX in data_corners_utmYX]
        else:
            self.logger.error("Error while setting 'trueDataCornerUTM' due to unexpected projection of subArr: %s."
                              % subArr.prj)

        return sub_GMS_obj

    @staticmethod
    def _merge_arrays(list_GMS_tiles, arrname2merge, target_shape, target_dtype):
        # type: (list, str, tuple, np.dtype) -> np.ndarray
        """Merge multiple arrays into a single one.

        :param list_GMS_tiles:
        :param arrname2merge:
        :param target_shape:
        :param target_dtype:
        :return:
        """
        out_arr = np.empty(target_shape, dtype=target_dtype)
        for tile in list_GMS_tiles:
            (rowStart, rowEnd), (colStart, colEnd) = tile.arr_pos
            out_arr[rowStart:rowEnd + 1, colStart:colEnd + 1] = getattr(tile, arrname2merge)
        return out_arr

    def log_for_fullArr_or_firstTile(self, log_msg, subset=None):
        """Send a message to the logger only if full array or the first tile is currently processed.
        This function can be called when processing any tile but log message will only be sent from first tile.

        :param log_msg:  the log message to be logged
        :param subset:   subset argument as sent to e.g. DN2TOARadRefTemp that indicates which tile is to be processed.
                         Not needed if self.arr_pos is not None.
        """

        if subset is None and \
            (self.arr_shape == 'cube' or self.arr_pos is None or [self.arr_pos[0][0], self.arr_pos[1][0]] == [0, 0]) or\
                subset == ['cube', None] or (subset and [subset[1][0][0], subset[1][1][0]] == [0, 0]) or \
                hasattr(self, 'logAtThisTile') and getattr(self, 'logAtThisTile'):  # cube or 1st tile
            self.logger.info(log_msg)
        else:
            pass

    @staticmethod
    def LBA2bandnames(LayerBandsAssignment):
        """Convert LayerbandsAssignment from format ['1','2',...] to bandnames like this: [B01, .., B8A,]."""
        return ['B%s' % i if len(i) == 2 else 'B0%s' % i for i in LayerBandsAssignment]

    def get_tilepos(self, target_tileshape, target_tilesize):
        self.tile_pos = [[target_tileshape, tb]
                         for tb in get_array_tilebounds(array_shape=self.shape_fullArr, tile_shape=target_tilesize)]

    @staticmethod
    def rescale_array(inArray, outScaleFactor, inScaleFactor=1):
        """Adjust the scaling factor of an array to match the given output scale factor."""

        assert isinstance(inArray, np.ndarray)
        return inArray.astype(np.int16) * (outScaleFactor / inScaleFactor)

    def calc_mask_nodata(self, fromBand=None, overwrite=False):
        """Calculates a no data mask with (values: 0=nodata; 1=data)

        :param fromBand:  <int> index of the band to be used (if None, all bands are used)
        :param overwrite: <bool> whether to overwrite existing nodata mask that has already been calculated
        :return:
        """

        self.logger.info('Calculating nodata mask...')

        if self._mask_nodata is None or overwrite:
            self.arr.calc_mask_nodata(fromBand=fromBand, overwrite=overwrite)
            self.mask_nodata = self.arr.mask_nodata
            return self.mask_nodata

    def apply_nodata_mask_to_ObjAttr(self, attrname, out_nodata_val=None):
        # type: (str,int) -> None
        """Applies self.mask_nodata to the specified array attribute by setting all values where mask_nodata is 0 to the
        given nodata value.

        :param attrname:         The attribute to apply the nodata mask to. Must be an array attribute or
                                 a string path to a previously saved ENVI-file.
        :param out_nodata_val:   set the values of the given attribute to this value.
        """

        assert hasattr(self, attrname)

        if getattr(self, attrname) is not None:

            if isinstance(getattr(self, attrname), str):
                update_spec_vals = True if attrname == 'arr' else False
                self.apply_nodata_mask_to_saved_ENVIfile(getattr(self, attrname), out_nodata_val, update_spec_vals)
            else:
                assert isinstance(getattr(self, attrname), (np.ndarray, GeoArray)), \
                    'L1A_obj.%s must be a numpy array or an instance of GeoArray. Got type %s.' \
                    % (attrname, type(getattr(self, attrname)))
                assert hasattr(self, 'mask_nodata') and self.mask_nodata is not None

                self.log_for_fullArr_or_firstTile('Applying nodata mask to L1A_object.%s...' % attrname)

                nodata_val = out_nodata_val if out_nodata_val else \
                    DEF_D.get_outFillZeroSaturated(getattr(self, attrname).dtype)[0]
                getattr(self, attrname)[self.mask_nodata.astype(np.int8) == 0] = nodata_val

                if attrname == 'arr':
                    self.MetaObj.spec_vals['fill'] = nodata_val

    def build_combined_masks_array(self):
        # type: () -> dict
        """Generates self.masks attribute (unsigned integer 8bit) from by concatenating all masks included in GMS obj.
        The corresponding metadata is assigned to L1A_obj.masks_meta. Empty mask attributes are skipped."""

        arrays2combine = [aN for aN in ['mask_nodata', 'mask_clouds']
                          if hasattr(self, aN) and isinstance(getattr(self, aN), (GeoArray, np.ndarray))]
        if arrays2combine:
            self.log_for_fullArr_or_firstTile('Combining masks...')

            def get_data(arrName): return getattr(self, arrName).astype(np.uint8)[:, :, None]

            for aN in arrays2combine:
                if False in np.equal(getattr(self, aN), getattr(self, aN).astype(np.uint8)):
                    warnings.warn('Some pixel values of attribute %s changed during data type '
                                  'conversion within build_combined_masks_array().')

            # set self.masks
            self.masks = get_data(arrays2combine[0]) if len(arrays2combine) == 1 else \
                np.concatenate([get_data(aN) for aN in arrays2combine], axis=2)
            self.masks.bandnames = arrays2combine  # set band names of GeoArray (allows later indexing by band name)

            # set self.masks_meta
            nodataVal = DEF_D.get_outFillZeroSaturated(self.masks.dtype)[0]
            self.masks_meta = {'map info': self.MetaObj.map_info,
                               'coordinate system string': self.MetaObj.projection,
                               'bands': len(arrays2combine),
                               'band names': arrays2combine,
                               'data ignore value': nodataVal}

            return {'desc': 'masks', 'row_start': 0, 'row_end': self.shape_fullArr[0],
                    'col_start': 0, 'col_end': self.shape_fullArr[1], 'data': self.masks}  # usually not needed

    def apply_nodata_mask_to_saved_ENVIfile(self, path_saved_ENVIhdr, custom_nodata_val=None, update_spec_vals=False):
        # type: (str,int,bool) -> None
        """Applies self.mask_nodata to a saved ENVI file with the same X/Y dimensions like self.mask_nodata by setting
        all values where mask_nodata is 0 to the given nodata value.

        :param path_saved_ENVIhdr:  <str> The path of the ENVI file to apply the nodata mask to.
        :param custom_nodata_val:   <int> set the values of the given attribute to this value.
        :param update_spec_vals:    <bool> whether to update self.MetaObj.spec_vals['fill']
        """

        self.log_for_fullArr_or_firstTile('Applying nodata mask to saved ENVI file...')
        assert os.path.isfile(path_saved_ENVIhdr)
        assert hasattr(self, 'mask_nodata') and self.mask_nodata is not None
        if not path_saved_ENVIhdr.endswith('.hdr') and os.path.isfile(os.path.splitext(path_saved_ENVIhdr)[0] + '.hdr'):
            path_saved_ENVIhdr = os.path.splitext(path_saved_ENVIhdr)[0] + '.hdr'
        if custom_nodata_val is None:
            dtype_IDL = int(INP_R.read_ENVIhdr_to_dict(path_saved_ENVIhdr)['data type'])
            nodata_val = DEF_D.get_outFillZeroSaturated(DEF_D.dtype_lib_IDL_Python[dtype_IDL])[0]
        else:
            nodata_val = custom_nodata_val
        FileObj = spectral.open_image(path_saved_ENVIhdr)
        File_memmap = FileObj.open_memmap(writable=True)
        File_memmap[self.mask_nodata == 0] = nodata_val
        if update_spec_vals:
            self.MetaObj.spec_vals['fill'] = nodata_val

    def combine_tiles_to_ObjAttr(self, tiles, target_attr):
        # type: (list,str) -> None
        """Combines tiles, e.g. produced by L1A_P.L1A_object.DN2TOARadRefTemp() to a single attribute.
        If CFG.inmem_serialization is False, the produced attribute is additionally written to disk.

        :param tiles:           <list> a list of dictionaries with the keys 'desc', 'data', 'row_start','row_end',
                                'col_start' and 'col_end'
        :param target_attr:     <str> the name of the attribute to be produced
        """

        warnings.warn("'combine_tiles_to_ObjAttr' is deprecated.", DeprecationWarning)
        assert tiles[0] and isinstance(tiles, list) and isinstance(tiles[0], dict), \
            "The 'tiles' argument has to be list of dictionaries with the keys 'desc', 'data', 'row_start'," \
            "'row_end', 'col_start' and 'col_end'."
        self.logger.info("Building L1A attribute '%s' by combining given tiles..." % target_attr)
        tiles = [tiles] if not isinstance(tiles, list) else tiles
        sampleTile = dict(tiles[0])
        target_shape = self.shape_fullArr if len(sampleTile['data'].shape) == 3 else self.shape_fullArr[:2]
        setattr(self, target_attr, np.empty(target_shape, dtype=sampleTile['data'].dtype))
        for tile in tiles:  # type: dict
            rS, rE, cS, cE = tile['row_start'], tile['row_end'], tile['col_start'], tile['col_end']
            if len(target_shape) == 3:
                getattr(self, target_attr)[rS:rE + 1, cS:cE + 1, :] = tile['data']
            else:
                getattr(self, target_attr)[rS:rE + 1, cS:cE + 1] = tile['data']
        if target_attr == 'arr':
            self.arr_desc = sampleTile['desc']
            self.arr_shape = 'cube' if len(self.arr.shape) == 3 else 'band' if len(self.arr.shape) == 2 else 'unknown'

            if not CFG.inmem_serialization:
                path_radref_file = os.path.join(self.ExtractedFolder, self.baseN + '__' + self.arr_desc)
                # path_radref_file = os.path.abspath('./testing/out/%s_TOA_Ref' % self.baseN)
                while not os.path.isdir(os.path.dirname(path_radref_file)):
                    try:
                        os.makedirs(os.path.dirname(path_radref_file))
                    except OSError as e:  # maybe not neccessary anymore in python 3
                        if not e.errno == 17:
                            raise
                GEOP.ndarray2gdal(self.arr, path_radref_file, importFile=self.MetaObj.Dataname, direction=3)
                self.MetaObj.Dataname = path_radref_file

    def write_tiles_to_ENVIfile(self, tiles, overwrite=True):
        # type: (list,bool) -> None
        """Writes tiles, e.g. produced by L1A_P.L1A_object.DN2TOARadRefTemp() to a single output ENVI file.

        :param tiles:           <list> a list of dictionaries with the keys 'desc', 'data', 'row_start','row_end',
                                'col_start' and 'col_end'
        :param overwrite:       whether to overwrite files that have been produced earlier
        """

        self.logger.info("Writing tiles '%s' temporarily to disk..." % tiles[0]['desc'])
        outpath = os.path.join(self.ExtractedFolder, '%s__%s.%s' % (self.baseN, tiles[0]['desc'], self.outInterleave))
        if CFG.target_radunit_optical in tiles[0]['desc'] or \
           CFG.target_radunit_thermal in tiles[0]['desc']:
            self.arr_desc = tiles[0]['desc']
            self.arr = outpath
            # self.arr = os.path.abspath('./testing/out/%s_TOA_Ref.bsq' % self.baseN)
            self.MetaObj.Dataname = self.arr
            self.arr_shape = \
                'cube' if len(tiles[0]['data'].shape) == 3 else 'band' if len(
                    tiles[0]['data'].shape) == 2 else 'unknown'
        elif tiles[0]['desc'] == 'masks':
            self.masks = outpath
        elif tiles[0]['desc'] == 'lonlat_arr':
            # outpath = os.path.join(os.path.abspath('./testing/out/'),'%s__%s.%s'
            #     %(self.baseN, tiles[0]['desc'], self.outInterleave))
            self.lonlat_arr = outpath
        outpath = os.path.splitext(outpath)[0] + '.hdr' if not outpath.endswith('.hdr') else outpath
        out_shape = self.shape_fullArr[:2] + ([tiles[0]['data'].shape[2]] if len(tiles[0]['data'].shape) == 3 else [1])
        OUT_W.Tiles_Writer(tiles, outpath, out_shape, tiles[0]['data'].dtype, self.outInterleave,
                           self.MetaObj.to_odict(), overwrite=overwrite)

    def to_tiles(self, blocksize=(2048, 2048)):
        # type: (tuple) -> Generator[GMS_object]
        """Returns a generator object where items represent tiles of the given block size for the GMS object.

        # NOTE:  it's better to call get_subset_obj (also takes care of tile map infos)

        :param blocksize:   target dimensions of the generated block tile (rows, columns)
        :return:            <list> of GMS_object tiles
        """

        assert type(blocksize) in [list, tuple] and len(blocksize) == 2, \
            "The argument 'blocksize_RowsCols' must represent a tuple of size 2."

        tilepos = get_array_tilebounds(array_shape=self.shape_fullArr, tile_shape=blocksize)

        for tp in tilepos:
            (xmin, xmax), (ymin, ymax) = tp  # e.g. [(0, 1999), (0, 999)] at a blocksize of 2000*1000 (rowsxcols)
            tileObj = self.get_subset_obj(imBounds=(xmin, xmax, ymin, ymax))  # xmax+1/ymax+1?
            yield tileObj

    def to_MGRS_tiles(self, pixbuffer=10, v=False):
        # type: (int, bool) -> Generator[GMS_object]
        """Returns a generator object where items represent the MGRS tiles for the GMS object.

        :param pixbuffer:   <int> a buffer in pixel values used to generate an overlap between the returned MGRS tiles
        :param v:           <bool> verbose mode
        :return:            <list> of MGRS_tile objects
        """

        assert self.arr_shape == 'cube', "Only 'cube' objects can be cut into MGRS tiles. Got %s." % self.arr_shape
        self.logger.info('Cutting scene %s (entity ID %s) into MGRS tiles...' % (self.scene_ID, self.entity_ID))

        # get GeoDataFrame containing all overlapping MGRS tiles
        # (MGRS geometries completely within nodata area are excluded)
        GDF_MGRS_tiles = DB_T.get_overlapping_MGRS_tiles(CFG.conn_database,
                                                         tgt_corners_lonlat=self.trueDataCornerLonLat)

        if GDF_MGRS_tiles.empty:
            raise RuntimeError('Could not find an overlapping MGRS tile in the database for the current dataset.')

        # calculate image coordinate bounds of the full GMS object for each MGRS tile within the GeoDataFrame
        gt = mapinfo2geotransform(self.MetaObj.map_info)

        def get_arrBounds(MGRStileObj):
            return list(np.array(MGRStileObj.poly_utm.buffer(pixbuffer * gt[1]).bounds)[[0, 2, 1, 3]])

        GDF_MGRS_tiles['MGRStileObj'] = list(GDF_MGRS_tiles['granuleid'].map(lambda mgrsTileID: MGRS_tile(mgrsTileID)))
        GDF_MGRS_tiles['map_bounds_MGRS'] = list(GDF_MGRS_tiles['MGRStileObj'].map(get_arrBounds))  # xmin,xmax,ymin,yma

        # find first tile to log and assign 'logAtThisTile' later
        dictIDxminymin = {(b[0] + b[2]): ID for ID, b in
                          zip(GDF_MGRS_tiles['granuleid'], GDF_MGRS_tiles['map_bounds_MGRS'])}
        firstTile_ID = dictIDxminymin[min(dictIDxminymin.keys())]

        # ensure self.masks exists (does not exist in case of inmem_serialization mode
        # because in that case self.fill_from_disk() is skipped)
        if not hasattr(self, 'masks') or self.masks is None:
            self.build_combined_masks_array()  # creates self.masks and self.masks_meta

        # read whole dataset into RAM in order to fasten subsetting
        self.arr.to_mem()
        self.masks.to_mem()  # to_mem ensures that the whole dataset is present in memory

        # produce data for each MGRS tile in loop
        for GDF_idx, GDF_row in GDF_MGRS_tiles.iterrows():
            tileObj = self.get_subset_obj(mapBounds=GDF_row.map_bounds_MGRS,
                                          mapBounds_prj=EPSG2WKT(GDF_row['MGRStileObj'].EPSG),
                                          out_prj=EPSG2WKT(GDF_row['MGRStileObj'].EPSG),
                                          logmsg='Producing MGRS tile %s from scene %s (entity ID %s).'
                                                 % (GDF_row.granuleid, self.scene_ID, self.entity_ID),
                                          progress=CFG.log_level in ['DEBUG', 10],
                                          v=v)

            MGRS_tileID = GDF_row['granuleid']

            # validate that the MGRS tile truly contains data
            # -> this may not be the case if get_overlapping_MGRS_tiles() yielded invalid tiles due to inaccurate
            #    self.trueDataCornerLonLat
            if tileObj is None or \
               True not in list(np.unique(tileObj.arr.mask_nodata)):
                self.logger.info("MGRS tile '%s' has not been skipped because it contains only no data values."
                                 % MGRS_tileID)
                continue

            # set MGRS info
            tileObj.arr_shape = 'MGRS_tile'
            tileObj.MGRS_info = {'tile_ID': MGRS_tileID, 'grid1mil': MGRS_tileID[:3], 'grid100k': MGRS_tileID[3:]}

            # set logAtThisTile
            tileObj.logAtThisTile = MGRS_tileID == firstTile_ID

            # close logger of tileObj and of self in order to avoid logging permission errors
            tileObj.close_loggers()
            self.close_loggers()

            yield tileObj

        # set array attributes back to file path if they had been a filePath before
        if self.arr.filePath:
            self.arr.to_disk()
        if self.masks.filePath:
            self.masks.to_disk()

    def to_GMS_file(self, path_gms_file=None):
        self.close_loggers()

        dict2write = self.attributes2dict(remove_privates=True)  # includes MetaObj as OrderedDict
        dict2write['arr_shape'], dict2write['arr_pos'] = ['cube', None]
        path_gms_file = path_gms_file if path_gms_file else self.pathGen.get_path_gmsfile()

        for k, v in list(dict2write.items()):
            # if isinstance(v,np.ndarray) or isinstance(v,dict) or hasattr(v,'__dict__'):
            # so, wenn meta-dicts nicht ins gms-file sollen. ist aber vllt ni schlecht
            # -> erlaubt lesen der metadaten direkt aus gms

            if isinstance(v, datetime.datetime):
                dict2write[k] = v.strftime('%Y-%m-%d %H:%M:%S.%f%z')

            elif isinstance(v, (DatasetLogger, logging.Logger)):
                if hasattr(v, 'handlers') and v.handlers[:]:
                    warnings.warn('Not properly closed logger at GMS_obj.logger pointing to %s.' % v.path_logfile)

                close_logger(dict2write[k])
                dict2write[k] = 'not set'

            elif isinstance(v, GMS_identifier):
                dict2write[k] = v.to_odict(include_logger=False)

            elif isinstance(v, OrderedDict) or isinstance(v, dict):
                dict2write[k] = dict2write[k].copy()
                if 'logger' in v:
                    if hasattr(dict2write[k]['logger'], 'handlers') and dict2write[k]['logger'].handlers[:]:
                        warnings.warn("Not properly closed logger at %s['logger'] pointing to %s."
                                      % (k, dict2write[k]['logger'].path_logfile))
                    close_logger(dict2write[k]['logger'])
                    dict2write[k]['logger'] = 'not set'

            elif isinstance(v, np.ndarray):
                # delete every 3D Array larger than 100x100
                if len(v.shape) == 2 and sum(v.shape) <= 200:
                    dict2write[k] = v.tolist()  # numpy arrays are not jsonable
                else:
                    del dict2write[k]

            elif hasattr(v, '__dict__'):
                # löscht Instanzen von Objekten und Arrays, aber keine OrderedDicts
                if hasattr(v, 'logger'):
                    if hasattr(dict2write[k].logger, 'handlers') and dict2write[k].logger.handlers[:]:
                        warnings.warn("Not properly closed logger at %s.logger pointing to %s."
                                      % (k, dict2write[k].logger.path_logfile))
                    close_logger(dict2write[k].logger)
                    dict2write[k].logger = 'not set'
                del dict2write[k]

                # class customJSONEncoder(json.JSONEncoder):
                #     def default(self, obj):
                #         if isinstance(obj, np.ndarray):
                #             return '> numpy array <'
                #         if isinstance(obj, dict): # funktioniert nicht
                #             return '> python dictionary <'
                #         if hasattr(obj,'__dict__'):
                #             return '> python object <'
                #         # Let the base class default method raise the TypeError
                #         return json.JSONEncoder.default(self, obj)
                # json.dump(In, open(path_out_baseN,'w'), skipkeys=True,
                #           sort_keys=True, cls=customJSONEncoder, separators=(',', ': '), indent =4)
        with open(path_gms_file, 'w') as outF:
            json.dump(dict2write, outF, skipkeys=True, sort_keys=True, separators=(',', ': '), indent=4)

    def to_ENVI(self, write_masks_as_ENVI_classification=True, is_tempfile=False, compression=False):
        # type: (object, bool, bool) -> None
        """Write GMS object to disk. Supports full cubes AND 'block' tiles.

        :param self:                               <object> GMS object, e.g. L1A_P.L1A_object
        :param write_masks_as_ENVI_classification:  <bool> whether to write masks as ENVI classification file
        :param is_tempfile:                         <bool> whether output represents a temporary file
                                                    -> suppresses logging and database updating
                                                    - ATTENTION! This keyword asserts that the actual output file that
                                                     is written later contains the final version of the array. The array
                                                     is not overwritten or written once more later, but only renamed.
        :param compression:                         <bool> enable or disable compression
        """
        # monkey patch writer function in order to silence output stream
        envi._write_image = OUT_W.silent_envi_write_image

        assert self.arr_shape in ['cube', 'MGRS_tile', 'block'], \
            "GMS_object.to_ENVI supports only array shapes 'cube', 'MGRS_tile' and 'block'. Got %s." % self.arr_shape

        # set MGRS info in case of MGRS tile
        MGRS_info = None
        if self.arr_shape == 'MGRS_tile':
            assert hasattr(self, 'MGRS_info'), \
                "Tried to write an GMS object in the shape 'MGRS_tile' without without the attribute 'MGRS_info'."
            MGRS_info = self.MGRS_info

        # set self.arr from L1B path to L1A path in order to make to_ENVI copy L1A array (if .arr is not an array)
        if self.proc_level == 'L1B' and not self.arr.is_inmem and os.path.isfile(self.arr.filePath):
            # FIXME this could leed to check the wrong folder if CFG.inmem_serialization is False:
            self.arr = PG.path_generator('L1A', self.image_type, self.satellite, self.sensor, self.subsystem,
                                         self.acq_datetime, self.entity_ID, self.logger,
                                         MGRS_info=MGRS_info).get_path_imagedata()

        # set dicts
        image_type_dict = dict(arr=self.image_type, masks='MAS', mask_clouds='MAC', accuracy_layers='AL')
        metaAttr_dict = dict(arr='arr_meta', masks='masks_meta', mask_clouds='masks_meta',
                             accuracy_layers='accuracy_layers_meta')
        out_dtype_dict = dict(arr='int16', masks='uint8', mask_clouds='uint8', accuracy_layers='int16')
        print_dict = dict(
            RSD_L1A='satellite data', MAS_L1A='masks', MAC_L1A='cloud mask',
            RSD_L1B='satellite data', MAS_L1B='masks', MAC_L1B='cloud mask',
            RSD_L1C='atm. corrected reflectance data', MAS_L1C='masks', MAC_L1C='cloud mask',
            RSD_L2A='geometrically homogenized data', MAS_L2A='masks', MAC_L2A='cloud mask',
            RSD_L2B='spectrally homogenized data', MAS_L2B='masks', MAC_L2B='cloud mask',
            RSD_L2C='MGRS tiled data', MAS_L2C='masks', MAC_L2C='cloud mask', AL_L2C='accuracy layers',)

        # ensure self.masks exists
        if not hasattr(self, 'masks') or self.masks is None:
            self.build_combined_masks_array()  # creates InObj.masks and InObj.masks_meta

        # generate list of attributes to write
        attributes2write = ['arr', 'masks']

        if self.proc_level not in ['L1A', 'L1B'] and write_masks_as_ENVI_classification:
            attributes2write.append('mask_clouds')

        if self.proc_level == 'L2C':
            if CFG.ac_estimate_accuracy or CFG.spathomo_estimate_accuracy or CFG.spechomo_estimate_accuracy:
                attributes2write.append('accuracy_layers')

                # generate accuracy layers to be written
                self.generate_accuracy_layers()
            else:
                self.logger.info('Accuracy layers are not written because their generation has been disabled in the '
                                 'job configuration.')

        ###########################################################
        # loop through all attributes to write and execute writer #
        ###########################################################

        with IOLock(allowed_slots=CFG.max_parallel_reads_writes, logger=self.logger):
            for arrayname in attributes2write:
                descriptor = '%s_%s' % (image_type_dict[arrayname], self.proc_level)

                if hasattr(self, arrayname) and getattr(self, arrayname) is not None:
                    arrayval = getattr(self, arrayname)  # can be a GeoArray (in mem / not in mem) or a numpy.ndarray

                    # initial assertions
                    assert arrayname in metaAttr_dict, "GMS_object.to_ENVI cannot yet write %s attribute." % arrayname
                    assert isinstance(arrayval, (GeoArray, np.ndarray)), "Expected a GeoArray instance or a numpy " \
                                                                         "array for object attribute %s. Got %s." \
                                                                         % (arrayname, type(arrayval))

                    outpath_hdr = self.pathGen.get_outPath_hdr(arrayname)
                    outpath_hdr = os.path.splitext(outpath_hdr)[0] + '__TEMPFILE.hdr' if is_tempfile else outpath_hdr
                    if not os.path.exists(os.path.dirname(outpath_hdr)):
                        os.makedirs(os.path.dirname(outpath_hdr))
                    out_dtype = out_dtype_dict[arrayname]
                    meta_attr = metaAttr_dict[arrayname]

                    if not is_tempfile:
                        self.log_for_fullArr_or_firstTile('Writing %s %s.' % (self.proc_level, print_dict[descriptor]))

                    #########################
                    # GeoArray in disk mode #
                    #########################

                    if isinstance(arrayval, GeoArray) and not arrayval.is_inmem:
                        # object attribute contains GeoArray in disk mode. This is usually the case if the attribute has
                        # been read in Python exec mode from previous processing level and has NOT been modified during
                        # processing.

                        assert os.path.isfile(arrayval.filePath), "The object attribute '%s' contains a not existing " \
                                                                  "file path: %s" % (arrayname, arrayval.filePath)
                        path_to_array = arrayval.filePath

                        #############
                        # full cube #
                        #############

                        if self.arr_shape == 'cube':
                            # image data can just be copied
                            outpath_arr = os.path.splitext(outpath_hdr)[0] + (os.path.splitext(path_to_array)[1]
                                                                              if os.path.splitext(path_to_array)[
                                1] else '.%s' % self.outInterleave)
                            hdr2readMeta = os.path.splitext(path_to_array)[0] + '.hdr'
                            meta2write = INP_R.read_ENVIhdr_to_dict(hdr2readMeta, self.logger) \
                                if arrayname in ['mask_clouds', ] else getattr(self, meta_attr)
                            meta2write.update({'interleave': self.outInterleave,
                                               'byte order': 0,
                                               'header offset': 0,
                                               'data type': DEF_D.dtype_lib_Python_IDL[out_dtype],
                                               'lines': self.shape_fullArr[0],
                                               'samples': self.shape_fullArr[1]})
                            meta2write = metaDict_to_metaODict(meta2write, self.logger)

                            if '__TEMPFILE' in path_to_array:
                                os.rename(path_to_array, outpath_arr)
                                envi.write_envi_header(outpath_hdr, meta2write)
                                HLP_F.silentremove(path_to_array)
                                HLP_F.silentremove(os.path.splitext(path_to_array)[0] + '.hdr')

                            else:
                                try:
                                    shutil.copy(path_to_array, outpath_arr)  # copies file + permissions
                                except PermissionError:
                                    # prevents permission error if outfile already exists and is owned by another user
                                    HLP_F.silentremove(outpath_arr)
                                    shutil.copy(path_to_array, outpath_arr)

                                envi.write_envi_header(outpath_hdr, meta2write)

                            assert OUT_W.check_header_not_empty(outpath_hdr), "HEADER EMPTY: %s" % outpath_hdr
                            setattr(self, arrayname, outpath_arr)  # refresh arr/masks/mask_clouds attributes
                            if arrayname == 'masks':
                                setattr(self, 'mask_nodata', outpath_arr)

                        #########################
                        # 'block' or 'MGRS_tile #
                        #########################

                        else:
                            # data have to be read in subset and then be written
                            if self.arr_pos:
                                (rS, rE), (cS, cE) = self.arr_pos
                                cols, rows = cE - cS + 1, rE - rS + 1
                            else:
                                cS, rS, cols, rows = [None] * 4

                            if '__TEMPFILE' in path_to_array:
                                raise NotImplementedError

                            if arrayname not in ['mask_clouds', 'mask_nodata']:
                                # read image data in subset
                                tempArr = gdalnumeric.LoadFile(path_to_array, cS, rS, cols,
                                                               rows)  # bands, rows, columns OR rows, columns
                                arr2write = tempArr if len(tempArr.shape) == 2 else \
                                    np.swapaxes(np.swapaxes(tempArr, 0, 2), 0, 1)  # rows, columns, (bands)

                            else:
                                # read mask data in subset
                                previous_procL = DEF_D.proc_chain[DEF_D.proc_chain.index(self.proc_level) - 1]
                                PG_obj = PG.path_generator(self.__dict__, proc_level=previous_procL)
                                path_masks = PG_obj.get_path_maskdata()
                                arr2write = INP_R.read_mask_subset(path_masks, arrayname, self.logger,
                                                                   (self.arr_shape, self.arr_pos))

                            setattr(self, arrayname, arr2write)

                    arrayval = getattr(self, arrayname)  # can be a GeoArray (in mem / not in mem) or a numpy.ndarray

                    ####################################
                    # np.ndarray or GeoArray in memory #
                    ####################################

                    if isinstance(arrayval, np.ndarray) or isinstance(arrayval, GeoArray) and arrayval.is_inmem:
                        # must be an if-condition because arrayval can change attribute type from not-inmem-GeoArray
                        # to np.ndarray
                        '''object attribute contains array'''

                        # convert array and metadata of mask clouds to envi classification file ready data
                        arr2write, meta2write = OUT_W.mask_to_ENVI_Classification(self, arrayname) \
                            if arrayname in ['mask_clouds', ] else (arrayval, getattr(self, meta_attr))
                        arr2write = arr2write.arr if isinstance(arr2write, GeoArray) else arr2write
                        assert isinstance(arr2write, np.ndarray), 'Expected a numpy ndarray. Got %s.' % type(arr2write)

                        ##########################
                        # full cube or MGRS_tile #
                        ##########################

                        if self.arr_shape in ['cube', 'MGRS_tile']:
                            # TODO write a function that implements the algorithm from Tiles_Writer for writing cubes
                            # TODO -> no need for Spectral Python

                            # write cube-like attributes
                            meta2write = metaDict_to_metaODict(meta2write, self.logger)
                            success = 1

                            if arrayname not in ['mask_clouds', ]:
                                if compression:
                                    success = OUT_W.write_ENVI_compressed(outpath_hdr, arr2write, meta2write)
                                    if not success:
                                        warnings.warn('Written compressed ENVI file is not GDAL readable! '
                                                      'Writing uncompressed file.')

                                if not compression or not success:
                                    envi.save_image(outpath_hdr, arr2write, metadata=meta2write, dtype=out_dtype,
                                                    interleave=self.outInterleave, ext=self.outInterleave, force=True)

                            else:
                                if compression:
                                    success = OUT_W.write_ENVI_compressed(outpath_hdr, arr2write, meta2write)
                                    if not success:
                                        self.logger.warning('Written compressed ENVI file is not GDAL readable! '
                                                            'Writing uncompressed file.')

                                if not compression or not success:
                                    class_names = meta2write['class names']
                                    class_colors = meta2write['class lookup']
                                    envi.save_classification(outpath_hdr, arr2write, metadata=meta2write,
                                                             dtype=out_dtype, interleave=self.outInterleave,
                                                             ext=self.outInterleave, force=True,
                                                             class_names=class_names, class_colors=class_colors)
                            if os.path.exists(outpath_hdr):
                                OUT_W.reorder_ENVI_header(outpath_hdr, OUT_W.enviHdr_keyOrder)

                        #########################
                        # block-like attributes #
                        #########################

                        else:
                            if compression:  # FIXME
                                warnings.warn(
                                    'Compression is not yet supported for GMS object tiles. Writing uncompressed data.')
                            # write block-like attributes
                            bands = arr2write.shape[2] if len(arr2write.shape) == 3 else 1
                            out_shape = tuple(self.shape_fullArr[:2]) + (bands,)

                            OUT_W.Tiles_Writer(arr2write, outpath_hdr, out_shape, out_dtype, self.outInterleave,
                                               out_meta=meta2write, arr_pos=self.arr_pos, overwrite=False)
                            assert OUT_W.check_header_not_empty(outpath_hdr), "HEADER EMPTY: %s" % outpath_hdr

                        outpath_arr = os.path.splitext(outpath_hdr)[0] + '.%s' % self.outInterleave
                        if not CFG.inmem_serialization:
                            setattr(self, arrayname, outpath_arr)  # replace array by output path

                            if arrayname == 'masks':
                                setattr(self, 'mask_nodata', outpath_arr)

                                # if compression:
                                #    raise NotImplementedError # FIXME implement working compression
                                #    HLP_F.ENVIfile_to_ENVIcompressed(outpath_hdr)

                else:
                    if not is_tempfile:
                        self.logger.warning("The %s can not be written, because there is no corresponding attribute."
                                            % print_dict[descriptor])

        ######################################
        # write GMS-file and update database #
        ######################################

        # IMPORTANT: DO NOT pass the complete object but only a copy of the dictionary in order to prevent ASCII_writer
        #            and data_DB_updater from modifying the attributes of the object!!
        if self.arr_shape in ['cube', 'MGRS_tile'] or [self.arr_pos[0][0], self.arr_pos[1][0]] == [0, 0]:
            # cube or 1st tile

            # WRITE GMS FILE
            self.to_GMS_file()

            # CREATE/UPDATE DATABASE ENTRY
            if not is_tempfile:
                DB_T.data_DB_updater(self.attributes2dict())

                # get id of updated record (needed for cross-refs in later db entrys
                if hasattr(self, 'MGRS_info') and self.MGRS_info:
                    res = DB_T.get_info_from_postgreSQLdb(CFG.conn_database, 'mgrs_tiles_proc', ['id'],
                                                          {'sceneid': self.scene_ID,
                                                           'virtual_sensor_id': CFG.virtual_sensor_id,
                                                           'mgrs_code': self.MGRS_info['tile_ID']})
                    assert len(res) == 1, 'Found multiple database records for the last updated record. sceneid: %s;' \
                                          'mgrs_code: %s; virtual_sensor_id: %s' \
                                          % (self.scene_ID, self.MGRS_info['tile_ID'], CFG.virtual_sensor_id)
                    self.mgrs_tiles_proc_ID = res[0][0]
                else:
                    res = DB_T.get_info_from_postgreSQLdb(CFG.conn_database, 'scenes_proc', ['id'],
                                                          {'sceneid': self.scene_ID})
                    assert len(res) == 1, \
                        'Found multiple database records for the last updated record. sceneid: %s' % self.scene_ID
                    self.scenes_proc_ID = res[0][0]

            # COPY LOGFILE TO MGRS OUTPUT DIRECTORY
            if self.arr_shape == 'MGRS_tile':
                shutil.copy(self.path_logfile, os.path.join(self.pathGen.get_path_procdata(),
                                                            os.path.basename(self.path_logfile)))

        if not is_tempfile:
            self.log_for_fullArr_or_firstTile('%s data successfully saved.' % self.proc_level)

        # close logger
        self.close_loggers()

    def record_mem_usage(self):
        """Record memory usage of current process ID for the current processing level (megabytes)."""
        # get memory usage of current process ID
        mem_usage = int(psutil.Process(os.getpid()).memory_info().rss / 1024**2)

        # update the value (only if there is not a larger value already because we want to record maximum memory needed)
        if self.proc_level not in self.mem_usage or self.mem_usage[self.proc_level] > mem_usage:
            self.mem_usage[self.proc_level] = mem_usage

        # push recorded memory stats to database
        if self.proc_level == 'L2C':
            stats_pushed = DB_T.record_stats_memusage(CFG.conn_database, self)

            if stats_pushed:
                self.logger.info('Recorded memory usage statistics.')

    def block_at_system_overload(self, max_usage=95, timeout=15*60):
        logged = False
        t_start = time.time()

        while psutil.virtual_memory().percent >= max_usage:
            if not logged:
                self.logger.warning('Memory usage is %.1f percent. Waiting until memory usage is below %s percent. '
                                    'Timeout: %s minutes.' % (psutil.virtual_memory().percent, max_usage, timeout / 60))
                logged = True

            if time.time() - t_start > timeout:
                self.logger.exception('Processing could not be continued due to memory overload after waiting '
                                      '%s minutes.' % (timeout / 60))

            time.sleep(5)

    def close_loggers(self):
        # self.GMS_identifier and self.logger are getters - since self.GMS_identifier gets its logger from self.logger,
        # self.logger has to be closed AFTER closing self.GMS_identifier.logger
        if self.GMS_identifier and self.GMS_identifier.logger not in [None, 'not set']:
            self.GMS_identifier.logger.close()
            self.GMS_identifier.logger = None

        if self.MetaObj and self.MetaObj.logger not in [None, 'not set']:
            self.MetaObj.logger.close()
            self.MetaObj.logger = None

        if self._logger not in [None, 'not set']:
            self._logger.close()  # this runs misc.logging.GMS_logger.close()
            self._logger = None  # also adds current captured stream to self.log

    def delete_previous_proc_level_results(self):
        """Deletes results of the previous processing level if the respective flag CFG.exec_L**P[2]) is set to True.
           The function is skipped if the results of the current processing level have not yet been written.
        """

        tgt_proc_level = DEF_D.proc_chain[DEF_D.proc_chain.index(self.proc_level) - 1]

        if getattr(CFG, 'exec_%sP' % tgt_proc_level)[2]:

            pathGenPrev = PG.path_generator(self.__dict__.copy(), proc_level=tgt_proc_level)

            files2delete = [pathGenPrev.get_path_imagedata(),
                            pathGenPrev.get_path_gmsfile(),
                            pathGenPrev.get_path_maskdata(),
                            pathGenPrev.get_path_cloudmaskdata()]

            # ensure that the results of the current processing level have been written
            if self.proc_level != 'L2A':
                pathGenCurr = self.pathGen
            else:
                # after geometric homogenization and subsystem merging (L2A) a path generator without subsystem
                # is needed
                dict4pathGen = self.__dict__.copy()
                dict4pathGen['subsystem'] = ''
                pathGenCurr = PG.path_generator(dict4pathGen)

            filesCurrProcL = [pathGenCurr.get_path_imagedata(),
                              pathGenCurr.get_path_gmsfile(),
                              pathGenCurr.get_path_maskdata(),
                              pathGenCurr.get_path_cloudmaskdata()]

            if self.proc_level == 'L2A' and self.subsystem:
                # in case subsystems have been merged in L2A -> also delete logfiles of L1C
                files2delete.append(pathGenPrev.get_path_logfile())
                filesCurrProcL.append(pathGenCurr.get_path_logfile())

            for fPath, fPathCP in zip(files2delete, filesCurrProcL):
                hdr = '%s.hdr' % os.path.splitext(fPath)[0]
                if os.path.exists(fPath) and os.path.exists(fPathCP):
                    HLP_F.silentremove(fPath)
                    if os.path.exists(hdr):
                        HLP_F.silentremove(hdr)

    def delete_tempFiles(self):
        """Delete all temporary files that have been written during GMS object processing.
        """

        # TODO ensure that all GDAL dataset are closed before. Otherwise the system creates a .fuse_hiddenXXX...
        # TODO right in the moment when we delete the data that are opened in GDAL

        self.logger.info('Deleting temporary data...')

        if sys.platform.startswith('linux'):
            # delete temporary extraction folder
            if os.path.isdir(self.ExtractedFolder):
                shutil.rmtree(self.ExtractedFolder)

            if os.path.isdir(self.ExtractedFolder):
                self.logger.warning('Could not delete temporary extraction folder: %s' % self.ExtractedFolder)

            # delete empty folders: subsystem > sensor > Rootname
            pardir = None
            for i in range(2):  # FIXME range(3)?
                deldir = self.ExtractedFolder if i == 0 else pardir
                pardir = os.path.abspath(os.path.join(deldir, os.path.pardir))
                if not glob.glob('%s/*' % pardir) and os.path.isdir(pardir):
                    os.rmdir(pardir)
                else:
                    break

            # delete all files containing __TEMPFILE
            path_procdata = self.pathGen.get_path_procdata()
            tempfiles = glob.glob(os.path.join(path_procdata, '*__TEMPFILE*'))
            [HLP_F.silentremove(tf) for tf in tempfiles]
        else:
            raise NotImplementedError

        # delete tempfiles created by HLP_F.get_tempfile()
        files2delete = glob.glob(os.path.join(self.ExtractedFolder, '*'))  # all files within ExtractedFolder
        files2delete += glob.glob(os.path.join(CFG.path_tempdir + 'GeoMultiSens_*'))
        for f in files2delete:
            HLP_F.silentremove(f)

        # delete previous proc_level results on demand (according to CFG.exec_L**P[2])
        self.delete_previous_proc_level_results()

        self.logger.close()
        self.logger = None

    def flush_array_data(self):
        del self.arr
        del self.mask_nodata
        del self.mask_clouds
        del self.masks
        del self.dem
        del self.mask_clouds_confidence
        del self.ac_errors
        del self.spat_homo_errors
        del self.spec_homo_errors
        del self.accuracy_layers

        if self.MetaObj:
            self.MetaObj.ViewingAngle_arrProv = {}
            self.MetaObj.IncidenceAngle_arrProv = {}


class GMS_identifier(object):
    def __init__(self, image_type, satellite, sensor, subsystem, proc_level, dataset_ID, logger=None):
        # type: (str, str, str, Union[str, None], str, int, Union[DatasetLogger, None]) -> None
        self.image_type = image_type
        self.satellite = satellite
        self.sensor = sensor
        self.subsystem = subsystem
        self.proc_level = proc_level
        self.dataset_ID = dataset_ID
        self.logger = logger

    def to_odict(self, include_logger=True):
        odict = OrderedDict(zip(
             ['image_type', 'Satellite', 'Sensor', 'Subsystem', 'proc_level', 'dataset_ID'],
             [self.image_type, self.satellite, self.sensor, self.subsystem, self.proc_level, self.dataset_ID]))

        if include_logger:
            odict['logger'] = self.logger

        return odict

    def __repr__(self):
        return repr(self.to_odict())

    def __getstate__(self):
        """Defines how the attributes of MetaObj instances are pickled."""
        close_logger(self.logger)
        self.logger = None

        return self.__dict__


class failed_GMS_object(GMS_object):
    def delete_tempFiles(self):
        pass

    def __init__(self, GMS_object_or_OrdDict, failedMapper, exc_type, exc_val, exc_tb):
        # type: (Union[GMS_object, OrderedDict], str, type(Exception), any, str) -> None
        super(failed_GMS_object, self).__init__()
        needed_attr = ['proc_level', 'image_type', 'scene_ID', 'entity_ID', 'satellite', 'sensor', 'subsystem',
                       'arr_shape', 'arr_pos']

        if isinstance(GMS_object_or_OrdDict, OrderedDict):  # in case of unhandled exception within L1A_map
            OrdDic = GMS_object_or_OrdDict
            [setattr(self, k, OrdDic[k]) for k in needed_attr[:-2]]
            self.arr_shape = 'cube' if 'arr_shape' not in OrdDic else OrdDic['arr_shape']
            self.arr_pos = None if 'arr_pos' not in OrdDic else OrdDic['arr_pos']

        else:  # in case of any other GMS mapper
            [setattr(self, k, getattr(GMS_object_or_OrdDict, k)) for k in needed_attr]

        self.failedMapper = failedMapper
        self.ExceptionType = exc_type.__name__
        self.ExceptionValue = repr(exc_val)
        self.ExceptionTraceback = exc_tb
        self.proc_status = 'failed'

    @property
    def pandasRecord(self):
        columns = ['scene_ID', 'entity_ID', 'satellite', 'sensor', 'subsystem', 'image_type', 'proc_level',
                   'arr_shape', 'arr_pos', 'failedMapper', 'ExceptionType', 'ExceptionValue', 'ExceptionTraceback']
        return DataFrame([getattr(self, k) for k in columns], columns=columns)


class finished_GMS_object(GMS_object):
    def __init__(self, GMS_obj):
        # type: (GMS_object) -> None
        super(finished_GMS_object, self).__init__()
        self.proc_level = GMS_obj.proc_level
        self.image_type = GMS_obj.image_type
        self.scene_ID = GMS_obj.scene_ID
        self.entity_ID = GMS_obj.entity_ID
        self.satellite = GMS_obj.satellite
        self.sensor = GMS_obj.sensor
        self.subsystem = GMS_obj.subsystem
        self.arr_shape = GMS_obj.arr_shape
        self.proc_status = GMS_obj.proc_status

    @property
    def pandasRecord(self):
        columns = ['scene_ID', 'entity_ID', 'satellite', 'sensor', 'subsystem', 'image_type', 'proc_level',
                   'arr_shape', 'arr_pos']
        return DataFrame([getattr(self, k) for k in columns], columns=columns)


def update_proc_status(GMS_mapper):
    """Decorator function for updating the processing status of each GMS_object (subclass) instance.

    :param GMS_mapper:  A GMS mapper function that takes a GMS object, does some processing and returns it back.
    """

    @functools.wraps(GMS_mapper)  # needed to avoid pickling errors
    def wrapped_GMS_mapper(GMS_objs, **kwargs):
        # type: (Union[List[GMS_object], GMS_object, OrderedDict, failed_GMS_object], dict) -> Union[GMS_object, List[GMS_object]]  # noqa

        # noinspection PyBroadException
        try:
            # set processing status to 'running'
            if isinstance(GMS_objs, OrderedDict):
                GMS_objs['proc_status'] = 'running'
            elif isinstance(GMS_objs, GMS_object):
                GMS_objs.proc_status = 'running'
            elif isinstance(GMS_objs, Iterable):
                for GMS_obj in GMS_objs:
                    GMS_obj.proc_status = 'running'
            elif isinstance(GMS_objs, failed_GMS_object):
                assert GMS_objs.proc_status == 'failed'
                return GMS_objs
            else:
                raise TypeError("Unexpected type of 'GMS_objs': %s" % type(GMS_objs))

            # RUN the GMS_mapper
            GMS_objs = GMS_mapper(GMS_objs, **kwargs)

            # set processing status to 'finished'
            if isinstance(GMS_objs, GMS_object):
                GMS_objs.proc_status = 'finished'
            elif isinstance(GMS_objs, Iterable):
                for GMS_obj in GMS_objs:
                    GMS_obj.proc_status = 'finished'
            else:
                raise TypeError("Unexpected type of 'GMS_objs': %s" % type(GMS_objs))
        except Exception:
            # set processing status to 'running'
            if isinstance(GMS_objs, OrderedDict):
                GMS_objs['proc_status'] = 'failed'
            elif isinstance(GMS_objs, GMS_object):
                GMS_objs.proc_status = 'failed'
            elif isinstance(GMS_objs, Iterable):
                for GMS_obj in GMS_objs:
                    GMS_obj.proc_status = 'failed'
            else:
                raise TypeError("Unexpected type of 'GMS_objs': %s" % type(GMS_objs))

            raise

        return GMS_objs  # Union[GMS_object, List[GMS_object]]

    return wrapped_GMS_mapper


def return_GMS_objs_without_arrays(GMS_pipeline):
    """Decorator function for flushing any array attributes within the return value of a GMS pipeline function.

    :param GMS_pipeline:  A GMS mapper function that takes a GMS object, does some processing and returns it back.
    """

    @functools.wraps(GMS_pipeline)  # needed to avoid pickling errors
    def wrapped_GMS_pipeline(*args, **kwargs):
        def flush_arrays(GMS_obj):
            # type: (Union[GMS_object, L1C_object]) -> GMS_object
            GMS_obj.flush_array_data()
            try:
                GMS_obj.delete_ac_input_arrays()
            except AttributeError:
                pass

            return GMS_obj

        ###################################################################
        # prepare results to be back-serialized to multiprocessing master #
        ###################################################################

        # NOTE: Exceptions within GMS pipeline will be forwarded to calling function.
        # NOTE: Exceptions within GMS mappers are catched by exception handler (if enabled)
        returnVal = GMS_pipeline(*args, **kwargs)

        # flush array data because they are too big to be kept in memory for many GMS_objects
        if isinstance(returnVal, (GMS_object, failed_GMS_object)):
            returnVal = flush_arrays(returnVal)
        elif isinstance(returnVal, Iterable):
            returnVal = [flush_arrays(obj) for obj in returnVal]
        else:  # OrderedDict (dataset)
            # the OrderedDict will not contain any arrays
            pass

        return returnVal

    return wrapped_GMS_pipeline


def return_proc_reports_only(GMS_pipeline):
    """Decorator function for flushing any array attributes within the return value of a GMS pipeline function.

    :param GMS_pipeline:  A GMS mapper function that takes a GMS object, does some processing and returns it back.
    """

    @functools.wraps(GMS_pipeline)  # needed to avoid pickling errors
    def wrapped_GMS_pipeline(*args, **kwargs):
        ###################################################################
        # prepare results to be back-serialized to multiprocessing master #
        ###################################################################

        # NOTE: Exceptions within GMS pipeline will be forwarded to calling function.
        # NOTE: Exceptions within GMS mappers are catched by exception handler (if enabled)
        returnVal = GMS_pipeline(*args, **kwargs)

        # flush array data because they are too big to be kept in memory for many GMS_objects
        if isinstance(returnVal, failed_GMS_object):
            pass
        elif isinstance(returnVal, GMS_object):
            returnVal = finished_GMS_object(returnVal)
        elif isinstance(returnVal, Iterable):
            returnVal = [obj if isinstance(obj, failed_GMS_object) else finished_GMS_object(obj) for obj in returnVal]
        else:  # OrderedDict (dataset)
            # the OrderedDict will not contain any arrays
            pass

        return returnVal

    return wrapped_GMS_pipeline


def GMS_object_2_dataset_dict(GMS_obj):
    # type: (GMS_object) -> OrderedDict
    return OrderedDict([
        ('proc_level', GMS_obj.proc_level),
        ('scene_ID', GMS_obj.scene_ID),
        ('dataset_ID', GMS_obj.dataset_ID),
        ('image_type', GMS_obj.image_type),
        ('satellite', GMS_obj.satellite),
        ('sensor', GMS_obj.sensor),
        ('subsystem', GMS_obj.subsystem),
        ('sensormode', GMS_obj.sensormode),
        ('acq_datetime', GMS_obj.acq_datetime),
        ('entity_ID', GMS_obj.entity_ID),
        ('filename', GMS_obj.filename)
    ])


def estimate_mem_usage(dataset_ID, satellite):
    memcols = ['used_mem_l1a', 'used_mem_l1b', 'used_mem_l1c',
               'used_mem_l2a', 'used_mem_l2b', 'used_mem_l2c']

    df = DataFrame(DB_T.get_info_from_postgreSQLdb(
        CFG.conn_database, 'stats_mem_usage_homo',
        vals2return=['software_version'] + memcols,
        cond_dict=dict(
            datasetid=dataset_ID,
            virtual_sensor_id=CFG.virtual_sensor_id,
            target_gsd=CFG.target_gsd[0],  # respects only xgsd
            target_nbands=len(CFG.target_CWL),
            inmem_serialization=CFG.inmem_serialization,
            target_radunit_optical=CFG.target_radunit_optical,
            # skip_coreg=CFG.skip_coreg,
            ac_estimate_accuracy=CFG.ac_estimate_accuracy,
            ac_bandwise_accuracy=CFG.ac_bandwise_accuracy,
            spathomo_estimate_accuracy=CFG.spathomo_estimate_accuracy,
            spechomo_estimate_accuracy=CFG.spechomo_estimate_accuracy,
            spechomo_bandwise_accuracy=CFG.spechomo_bandwise_accuracy,
            # parallelization_level=CFG.parallelization_level,
            # skip_thermal=CFG.skip_thermal,
            # skip_pan=CFG.skip_pan,
            # mgrs_pixel_buffer=CFG.mgrs_pixel_buffer,
            # cloud_masking_algorithm=CFG.cloud_masking_algorithm[satellite],
            is_test=CFG.is_test
        )),
        columns=['software_version'] + memcols
    )

    if not df.empty:
        df['used_mem_max'] = df[memcols].max(axis=1)

        # get records from gms_preprocessing versions higher than CFG.min_version_mem_usage_stats
        vers = list(df.software_version)
        vers_usable = [ver for ver in vers if parse_version(ver) >= parse_version(CFG.min_version_mem_usage_stats)]

        df_sub = df.loc[df.software_version.isin(vers_usable)]

        mem_estim_mb = np.mean(list(df_sub.used_mem_max))  # megabytes
        mem_estim_gb = mem_estim_mb / 1024  # gigabytes

        return int(np.ceil(mem_estim_gb + .1 * mem_estim_gb))
