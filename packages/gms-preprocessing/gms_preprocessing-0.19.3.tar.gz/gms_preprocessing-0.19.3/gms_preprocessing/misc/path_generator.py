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

import collections
import glob
import os
import re
import tempfile
import warnings
import uuid
from logging import Logger
from typing import Union, TYPE_CHECKING  # noqa F401  # flake8 issue

from ..options.config import GMS_config as CFG
from .definition_dicts import get_GMS_sensorcode

if TYPE_CHECKING:
    from ..model.gms_object import GMS_identifier  # noqa F401  # flake8 issue

# get_scene_and_dataset_infos_from_postgreSQLdb # inline in order to avoid circular dependencies

__author__ = 'Daniel Scheffler'


class path_generator(object):
    """Methods return absolute paths corresponding to the input object.
    To be instanced with the dict of a L1A/L1B/... object or a list with the attributes below.
    If 'scene_ID' (integer) is passed to kwargs, all eventually given args are ignored.
    Instead they are retrieved from postgreSQLdb."""

    def __init__(self, *args, **kwargs):
        if 'scene_ID' in kwargs:
            from .database_tools import get_scene_and_dataset_infos_from_postgreSQLdb
            args = [get_scene_and_dataset_infos_from_postgreSQLdb(kwargs['scene_ID'])]  # return [dict]
        assert len(args) in [1, 8, 9], "Received invalid length of 'args' argument."

        isdict = True if len(args) == 1 and type(args[0] in [dict, collections.OrderedDict]) else False
        if not isdict and len(args) == 8:
            args += (None,)  # set logger to None if not given in tuple
        elif isdict and 'logger' not in args[0]:
            args[0].update({'logger': None})  # set logger to None if not given in dict

        argsdict = args[0] if isdict else dict(zip(['proc_level', 'image_type', 'satellite', 'sensor', 'subsystem',
                                                    'acq_datetime', 'entity_ID', 'filename', 'logger'], list(args)))
        self.proc_level = kwargs.get('proc_level', argsdict['proc_level'])
        self.image_type = argsdict['image_type']
        self.satellite = argsdict['satellite']
        # sensor: database distinguishes SLC_OFF and SLC_ON but file structure not
        self.sensor = argsdict['sensor'] if not argsdict['sensor'] in ['ETM+_SLC_OFF', 'ETM+_SLC_ON'] else 'ETM+'
        self.subsystem = argsdict['subsystem']
        self.AcqDate = argsdict['acq_datetime']
        self.entity_ID = argsdict['entity_ID']
        self.filename = argsdict['filename']
        self.logger = argsdict['logger']
        self.MGRS_info = kwargs.get('MGRS_info', None)

    def __getstate__(self):
        """Defines how the attributes of path_generator are pickled."""

        if self.logger not in [None, 'not set']:
            self.logger.close()
            self.logger = None
        return self.__dict__

    def __setstate__(self, ObjDict):
        """Defines how the attributes of GMS object are unpickled."""

        self.__dict__ = ObjDict

    def get_path_rawdata(self):
        """Returns the folder of all downloaded data for the current scene."""
        if self.sensor and re.search(self.sensor, 'SRTM', re.I):
            return os.path.join(CFG.path_archive, self.satellite, self.sensor,
                                self.subsystem)  # FIXME downloader should store data into sensor folder
        else:
            return os.path.join(CFG.path_archive, self.satellite, self.sensor)

    def get_path_procdata(self):
        """Returns the target folder of all processed data for the current scene."""
        pOrd = (CFG.path_procdata_MGRS, 'virtual_sensor_id_%s' % CFG.virtual_sensor_id,
                self.MGRS_info['grid1mil'], self.MGRS_info['grid100k'], self.entity_ID) if self.MGRS_info else \
            (CFG.path_procdata_scenes, self.satellite, self.sensor, self.entity_ID)
        return os.path.join(*pOrd)

    def get_baseN(self, merged_subsystems=False):
        """Returns the basename belonging to the given scene.

        :param merged_subsystems:   if True, a subsystem is not included in the returned basename
                                    (usefor for merged subsystems in L2A+)
        """
        if self.subsystem and not merged_subsystems:
            items2include = (self.satellite, self.sensor, self.subsystem, self.entity_ID)
        else:
            items2include = (self.satellite, self.sensor, self.entity_ID)

        if self.MGRS_info:
            items2include += (self.MGRS_info['tile_ID'],)
        return '__'.join(list(items2include))

    def get_path_logfile(self, merged_subsystems=False):
        """Returns the path of the logfile belonging to the given scene, e.g. '/path/to/file/file.log'.

        :param merged_subsystems:   if True, a subsystem is not included in the returned logfile path
                                    (usefor for merged subsystems in L2A+)
        """
        return os.path.join(self.get_path_procdata(), self.get_baseN(merged_subsystems=merged_subsystems) + '.log')

    def get_local_archive_path_baseN(self):
        """Returns the path of the downloaded raw data archive, e.g. '/path/to/file/file.tar.gz'."""

        folder_rawdata = self.get_path_rawdata()
        self.filename = self.filename if self.filename else self.entity_ID
        if os.path.exists(os.path.join(folder_rawdata, self.filename)):
            outP = os.path.join(folder_rawdata, self.filename)
        else:
            extensions_found = [ext for ext in ['.tar.gz', '.zip', '.hdf']
                                if os.path.exists(os.path.join(folder_rawdata, '%s%s' % (self.filename, ext)))]
            if extensions_found:
                assert len(extensions_found) > 0, \
                    'The dataset %s.* cannot be found at %s' % (self.filename, folder_rawdata)
                assert len(extensions_found) == 1, "The folder %s contains multiple files identified as raw data " \
                                                   "to be processed. Choosing first one.." % folder_rawdata
                outP = os.path.join(folder_rawdata, '%s%s' % (self.filename, extensions_found[0]))
            else:
                if self.filename.endswith('.SAFE') and \
                   os.path.exists(os.path.join(folder_rawdata, os.path.splitext(self.filename)[0]) + '.zip'):
                    outP = os.path.join(folder_rawdata,
                                        os.path.splitext(self.filename)[0]) + '.zip'  # FIXME Bug in Datenbank
                else:
                    raise FileNotFoundError('The dataset %s.* cannot be found at %s'
                                            % (self.filename, folder_rawdata))  # TODO DOWNLOAD COMMAND
        return outP

    def get_path_gmsfile(self):
        """Returns the path of the .gms file belonging to the given processing level, e.g. '/path/to/file/file.gms'."""
        return os.path.join(self.get_path_procdata(), '%s_%s.gms' % (self.get_baseN(), self.proc_level))

    def get_path_imagedata(self):
        """Returns the path of the .bsq file belonging to the given processing level, e.g. '/path/to/file/file.bsq'."""
        return os.path.join(self.get_path_procdata(), '%s_image_data_%s.bsq' % (self.get_baseN(), self.proc_level))

    def get_path_maskdata(self):
        """Returns the path of the *_masks_*.bsq file belonging to the given processing level,
        e.g. '/path/to/file/file_masks_L1A.bsq'."""
        return os.path.join(self.get_path_procdata(), '%s_masks_%s.bsq' % (self.get_baseN(), self.proc_level))

    def get_path_cloudmaskdata(self):
        """Returns the path of the *_mask_clouds_*.bsq file belonging to the given processing level,
        e.g. '/path/to/file/file_mask_clouds_L1A.bsq'."""
        return os.path.join(self.get_path_procdata(), '%s_mask_clouds_%s.bsq' % (self.get_baseN(), self.proc_level))

    def get_path_accuracylayers(self):
        """Returns the path of the *_accuracy_layers_*.bsq file, e.g., '/path/to/file/file_accuracy_layers_L2C.bsq'.

        NOTE: Accuracy layers are only present in L2C.
        """
        if self.proc_level == 'L2C':
            return os.path.join(self.get_path_procdata(), '%s_accuracy_layers_%s.bsq'
                                % (self.get_baseN(), self.proc_level))

    def get_path_tempdir(self):
        path_archive = self.get_local_archive_path_baseN()
        RootName = os.path.splitext(os.path.basename(path_archive))[0]
        RootName = os.path.splitext(RootName)[0] if os.path.splitext(RootName)[1] else RootName
        RootName += '__' + uuid.uuid4().hex  # add a hex code in order to get uniqueness
        return os.path.join(CFG.path_tempdir, RootName, self.sensor, self.subsystem) \
            if self.subsystem else os.path.join(CFG.path_tempdir, RootName, self.sensor)

    def get_outPath_hdr(self, attrName2write):
        # type: (str) -> str
        """Returns the output path for the given attribute to be written.
        :param attrName2write:  <str> name of the GMS object attribute to be written"""
        outNameSuffix = 'image_data' if attrName2write == 'arr' else attrName2write
        outNameHdr = '%s_%s_%s.hdr' % (self.get_baseN(), outNameSuffix, self.proc_level) if outNameSuffix else \
            '%s_%s.hdr' % (self.get_baseN(), self.proc_level)
        return os.path.join(self.get_path_procdata(), outNameHdr)

    def get_path_ac_input_dump(self):
        """Returns the path of the .dill for a dump of atmospheric correction inputs, e.g. '/path/to/file/file.dill'."""
        return os.path.join(self.get_path_procdata(), '%s_ac_input_%s.dill' % (self.get_baseN(), self.proc_level))

    def get_pathes_all_procdata(self):  # TODO
        image = self.get_path_imagedata()
        mask = self.get_path_maskdata()
        mask_clouds = self.get_path_cloudmaskdata()
        accuracylayers = self.get_path_accuracylayers()
        gms_file = self.get_path_gmsfile()
        log_file = self.get_path_logfile()

        all_pathes = [image, mask, mask_clouds, accuracylayers, gms_file, log_file]

        warnings.warn(
            'get_pathes_all_procdata() is not yet completely implemented and will not return complete path list!')
        return all_pathes


def get_tempfile(ext=None, prefix=None, tgt_dir=None):
    """Returns the path to a tempfile.mkstemp() file that can be passed to any function that expects a physical path.
    The tempfile has to be deleted manually.
    :param ext:     file extension (None if None)
    :param prefix:  optional file prefix
    :param tgt_dir: target directory (automatically set if None)
     """
    if tgt_dir is None:
        tgt_dir = CFG.path_tempdir
    prefix = 'GeoMultiSens__' if prefix is None else prefix
    fd, path = tempfile.mkstemp(prefix=prefix, suffix=ext, dir=tgt_dir)
    os.close(fd)
    return path


def get_path_cloud_class_obj(GMS_id, get_all=False):
    """Returns the absolute path of the the training data used by cloud classifier.
    :param GMS_id:
    :param get_all:
    """

    GMS_sensorcode = get_GMS_sensorcode(GMS_id)
    satellite, sensor, logger = GMS_id.satellite, GMS_id.sensor, GMS_id.logger
    path_cloud_classifier_objects = CFG.path_cloud_classif

    obj_name_dic = {
        'AVNIR-2': None,
        'TM4': None,
        'TM5': None,
        'TM7': None,
        'LDCM': None,
        'SPOT1a': None,
        'SPOT1b': None,
        'SPOT2a': None,
        'SPOT2b': None,
        'SPOT3a': None,
        'SPOT3b': None,
        'SPOT4a': None,
        'SPOT4b': None,
        'SPOT5a': None,
        'SPOT5b': None,
        'RE5': None,
        'AST_V1': None,
        'AST_V2': None,
        'AST_S': None,
        'AST_T': None,
        'S2A10': 'S2__cld_mask_20160321_s2_8l0.200_11l0.060_12l0.040_v20161124_16:41:04.h5',
        'S2A20': 'S2__cld_mask_20160321_s2_8l0.200_11l0.060_12l0.040_v20161124_16:41:04.h5',
        'S2A60': 'S2__cld_mask_20160321_s2_8l0.200_11l0.060_12l0.040_v20161124_16:41:04.h5',
        'S2B10': 'S2__cld_mask_20160321_s2_8l0.200_11l0.060_12l0.040_v20161124_16:41:04.h5',
        'S2B20': 'S2__cld_mask_20160321_s2_8l0.200_11l0.060_12l0.040_v20161124_16:41:04.h5',
        'S2B60': 'S2__cld_mask_20160321_s2_8l0.200_11l0.060_12l0.040_v20161124_16:41:04.h5'}

    if get_all:  # returns a list
        listClf = glob.glob(os.path.join(path_cloud_classifier_objects, '*.dill'))
        classifier_names = listClf if listClf != [] else None
        classifier_path = [os.path.join(path_cloud_classifier_objects, str(i)) for i in classifier_names]
        if not os.path.isfile(os.path.join(path_cloud_classifier_objects, classifier_path)[0]):
            logger.warning('Cloud masking is not yet implemented for %s %s.' % (satellite, sensor))
            classifier_path = None
    else:
        try:
            classif_objName = obj_name_dic[GMS_sensorcode]
            if classif_objName:
                classifier_path = os.path.join(path_cloud_classifier_objects, classif_objName)
                if not os.path.isfile(os.path.join(path_cloud_classifier_objects, classifier_path)):
                    warnings.warn("Path generator expects a specific cloud mask object (%s) at %s but it does not "
                                  "exist. Are you sure that 'path_cloud_classif' has been correctly set in the config "
                                  "table of postgreSQL database and that the file is included in the repository? By "
                                  "default the classifier object should be available at "
                                  "<GMS root dir>/database/cloud_classifier/"
                                  % (classif_objName, path_cloud_classifier_objects))
                    logger.warning(
                        'Cloud masking not possible for %s %s due to environment error.'  # TODO move to environment
                        % (satellite, sensor))
                    classifier_path = None
            else:
                logger.warning('Cloud masking is not yet implemented for %s %s.' % (satellite, sensor))
                classifier_path = None

        except KeyError:
            logger.warning("Sensorcode '%s' is not included in sensorcode dictionary and can not be converted into GMS "
                           "sensorcode." % GMS_sensorcode)
            classifier_path = None
    return classifier_path


def get_path_snr_model(GMS_id):
    # type: (GMS_identifier) -> str
    """Returns the absolute path of the SNR model for the given sensor.

    :param GMS_id:
    """

    satellite, sensor = (GMS_id.satellite, GMS_id.sensor)
    satellite = 'RapidEye' if re.match(r'RapidEye', satellite, re.I) else satellite
    sensor = sensor[:-1] if re.match(r'SPOT', satellite, re.I) and sensor[-1] not in ['1', '2'] else sensor
    return os.path.join(CFG.path_SNR_models, satellite, sensor, 'SNR_model.csv')


def get_path_ac_options(GMS_id):
    # type: (GMS_identifier)->Union[str, None]
    """Returns the path of the options json file needed for atmospheric correction.
    """

    GMSid_ac = GMS_id
    GMSid_ac.subsystem = ''
    sensorcode = get_GMS_sensorcode(GMSid_ac)

    ac_options_file_dic = {
        'AVNIR-2': None,
        'TM4': 'l8_options.json',
        'TM5': 'l8_options.json',
        'TM7': 'l8_options.json',  # AC uses Landsat-8 options for L7 but reads only a subset of the options
        'LDCM': 'l8_options.json',
        'SPOT1a': None,
        'SPOT1b': None,
        'SPOT2a': None,
        'SPOT2b': None,
        'SPOT3a': None,
        'SPOT3b': None,
        'SPOT4a': None,
        'SPOT4b': None,
        'SPOT5a': None,
        'SPOT5b': None,
        'RE5': None,
        'AST_full': None,
        'S2A_full': 's2_options.json',
        'S2B_full': 's2_options.json',
    }

    try:
        fName_optFile = ac_options_file_dic[get_GMS_sensorcode(GMS_id)]
    except KeyError:
        GMS_id.logger.warning(
            "Sensorcode '%s' is not included in ac_options dictionary. "
            "Thus atmospheric correction is not available for the current scene." % sensorcode)
        fName_optFile = None

    if fName_optFile:
        from sicor import options
        path_ac = os.path.join(os.path.dirname(options.__file__), fName_optFile)

        # validate
        logger = GMS_id.logger or Logger(__name__)
        if not os.path.exists(path_ac):
            logger.warning('Could not locate options file for atmospheric correction at %s.' % path_ac)

        return path_ac
    else:
        return None
