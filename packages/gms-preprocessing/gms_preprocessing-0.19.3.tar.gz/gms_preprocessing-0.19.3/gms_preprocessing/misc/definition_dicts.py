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
import re

import numpy as np
from typing import TYPE_CHECKING  # noqa F401  # flake8 issue

from ..options.config import GMS_config as CFG

if TYPE_CHECKING:
    from ..model.gms_object import GMS_identifier  # noqa F401  # flake8 issue

__author__ = 'Daniel Scheffler'

dtype_lib_Python_IDL = {'bool_': 0, 'uint8': 1, 'int8': 1, 'int_': 1, 'int16': 2, 'uint16': 12, 'int32': 3,
                        'uint32': 13, 'int64': 14, 'uint64': 15, 'float32': 4, 'float64': 5, 'complex_': 6,
                        'complex64': 9}
dtype_lib_IDL_Python = {0: np.bool_, 1: np.uint8, 2: np.int16, 3: np.int32, 4: np.float32, 5: np.float64,
                        6: np.complex64, 9: np.complex128, 12: np.uint16, 13: np.uint32, 14: np.int64, 15: np.uint64}
dtype_lib_GDAL_Python = {"uint8": 1, "int8": 1, "uint16": 2, "int16": 3, "uint32": 4, "int32": 5, "float32": 6,
                         "float64": 7, "complex64": 10, "complex128": 11}
proc_chain = ['L1A', 'L1B', 'L1C', 'L2A', 'L2B', 'L2C']
db_jobs_statistics_def = {'pending': 1, 'started': 2, None: 2, 'L1A': 3, 'L1B': 4, 'L1C': 5, 'L2A': 6, 'L2B': 7,
                          'L2C': 8, 'FAILED': 9}  # NOTE: OrderedDicts passed to L1A_map have proc_level=None
bandslist_all_errors = ['ac_errors', 'mask_clouds_confidence', 'spat_homo_errors', 'spec_homo_errors']


def get_GMS_sensorcode(GMS_id):
    # type: (GMS_identifier) -> str

    Satellite, Sensor, Subsystem = (GMS_id.satellite, GMS_id.sensor, GMS_id.subsystem)
    Sensor = Sensor[:-1] if re.match(r'SPOT', Satellite, re.I) and Sensor[-1] not in ['1', '2'] else Sensor
    meta_sensorcode = Satellite + '_' + Sensor + ('_' + Subsystem if Subsystem not in ["", None] else "")
    sensorcode_dic = {
        'ALOS_AVNIR-2': 'AVNIR-2',
        'Landsat-4_TM': 'TM4',  # call from layerstacker
        'Landsat-4_TM_SAM': 'TM4',  # call from metadata object
        'Landsat-5_TM': 'TM5',
        'Landsat-5_TM_SAM': 'TM5',
        'Landsat-7_ETM+': 'TM7',
        'Landsat-7_ETM+_SAM': 'TM7',
        'Landsat-8_OLI': 'LDCM',
        'Landsat-8_OLI_TIRS': 'LDCM',
        'Landsat-8_LDCM': 'LDCM',
        'SPOT-1_HRV1': 'SPOT1a',  # MS
        'SPOT-1_HRV2': 'SPOT1b',
        'SPOT-2_HRV1': 'SPOT2a',
        'SPOT-2_HRV2': 'SPOT2b',
        'SPOT-3_HRV1': 'SPOT3a',
        'SPOT-3_HRV2': 'SPOT3b',
        'SPOT-4_HRVIR1': 'SPOT4a',
        'SPOT-4_HRVIR2': 'SPOT4b',
        'SPOT-5_HRG1': 'SPOT5a',  # PAN HRG2A
        'SPOT-5_HRG2': 'SPOT5b',  # MS HRG2J
        'RapidEye-1_MSI': 'RE1',
        'RapidEye-2_MSI': 'RE2',
        'RapidEye-3_MSI': 'RE3',
        'RapidEye-4_MSI': 'RE4',
        'RapidEye-5_MSI': 'RE5',
        'SRTM_SRTM2': 'SRTM2',
        'Terra_ASTER': 'AST_full',
        'Terra_ASTER_VNIR1': 'AST_V1',
        'Terra_ASTER_VNIR2': 'AST_V2',
        'Terra_ASTER_SWIR': 'AST_S',
        'Terra_ASTER_TIR': 'AST_T',
        'Sentinel-2A_MSI': 'S2A_full',
        'Sentinel-2B_MSI': 'S2B_full',
        'Sentinel-2A_MSI_S2A10': 'S2A10',
        'Sentinel-2A_MSI_S2A20': 'S2A20',
        'Sentinel-2A_MSI_S2A60': 'S2A60',
        'Sentinel-2B_MSI_S2B10': 'S2B10',
        'Sentinel-2B_MSI_S2B20': 'S2B20',
        'Sentinel-2B_MSI_S2B60': 'S2B60'
    }
    try:
        return sensorcode_dic[meta_sensorcode]
    except KeyError:
        raise KeyError('Sensor %s is not included in sensorcode dictionary and can not be converted into GMS '
                       'sensorcode.' % meta_sensorcode)


def get_mask_classdefinition(maskname, satellite):
    if maskname == 'mask_nodata':
        return {'No data': 0,
                'Data': 1}
    elif maskname == 'mask_clouds':
        legends = {
            'FMASK': {
                'No Data': 0,
                'Clear': 1,
                'Cloud': 2,
                'Shadow': 3,
                'Snow': 4,
                'Water': 5},
            # seems to be outdated:
            # {'Clear Land': 0, 'Clear Water': 1, 'Cloud Shadow': 2, 'Snow': 3, 'Cloud': 4, 'No data': 255}
            'Classical Bayesian': {
                'Clear': 10,
                'Thick Clouds': 20,
                'Thin Clouds': 30,
                'Snow': 40},  # Classical Bayesian py_tools_ah
            'SICOR': {
                'Clear': 10,
                'Water': 20,
                'Shadow': 30,
                'Cirrus': 40,
                'Cloud': 50,
                'Snow': 60}  # SICOR
        }

        return legends[CFG.cloud_masking_algorithm[satellite]]
    else:
        raise ValueError("'%s' is not a supported mask name." % maskname)


def get_mask_colormap(maskname):
    if maskname == 'mask_clouds':
        # return collections.OrderedDict(zip(['No data','Clear','Thick Clouds','Thin Clouds','Snow','Unknown Class'],
        #                                     [[0,0,0] ,[0,255,0],[80,80,80], [175,175,175],[255,255,255],[255,0,0]]))
        return collections.OrderedDict((
            ('No data', [0, 0, 0]),
            ('Clear', [0, 255, 0]),
            ('Water', [0, 0, 255]),
            ('Shadow', [50, 50, 50]),
            ('Cirrus', [175, 175, 175]),
            ('Cloud', [80, 80, 80]),
            ('Snow', [255, 255, 255]),
            ('Unknown Class', [255, 0, 0]),))
    else:
        return None


def get_outFillZeroSaturated(dtype):
    """Returns the values for 'fill-', 'zero-' and 'saturated' pixels of an image
    to be written with regard to the target data type.

    :param dtype: data type of the image to be written"""

    dtype = str(np.dtype(dtype))
    assert dtype in ['bool', 'int8', 'uint8', 'int16', 'uint16', 'float32'], \
        "get_outFillZeroSaturated: Unknown dType: '%s'." % dtype
    dict_outFill = {'bool': None, 'int8': -128, 'uint8': 0, 'int16': -9999, 'uint16': 9999, 'float32': -9999.}
    dict_outZero = {'bool': None, 'int8': 0, 'uint8': 1, 'int16': 0, 'uint16': 0, 'float32': 0.}
    dict_outSaturated = {'bool': None, 'int8': 127, 'uint8': 256, 'int16': 32767, 'uint16': 65535, 'float32': 65535.}
    return dict_outFill[dtype], dict_outZero[dtype], dict_outSaturated[dtype]


def is_dataset_provided_as_fullScene(GMS_id):
    # type: (GMS_identifier) -> bool
    """Returns True if the dataset belonging to the given GMS_identifier is provided as full scene and returns False if
     it is provided as multiple tiles.

    :param GMS_id:
    :return:
    """

    sensorcode = get_GMS_sensorcode(GMS_id)
    dict_fullScene_or_tiles = {
        'AVNIR-2': True,
        'AST_full': True,
        'AST_V1': True,
        'AST_V2': True,
        'AST_S': True,
        'AST_T': True,
        'TM4': True,
        'TM5': True,
        'TM7': True,
        'LDCM': True,
        'SPOT1a': True,
        'SPOT2a': True,
        'SPOT3a': True,
        'SPOT4a': True,
        'SPOT5a': True,
        'SPOT1b': True,
        'SPOT2b': True,
        'SPOT3b': True,
        'SPOT4b': True,
        'SPOT5b': True,
        'RE5': False,
        'S2A_full': False,
        'S2A10': False,
        'S2A20': False,
        'S2A60': False,
        'S2B_full': False,
        'S2B10': False,
        'S2B20': False,
        'S2B60': False, }
    return dict_fullScene_or_tiles[sensorcode]


def datasetid_to_sat_sen(dsid):
    # type: (int) -> tuple
    conv_dict = {
        8: ('Terra', 'ASTER'),  # ASTER L1B
        104: ('Landsat-8', 'OLI_TIRS'),  # pre-collection-ID
        108: ('Landsat-5', 'TM'),  # pre-collection-ID
        112: ('Landsat-7', 'ETM+'),  # pre-collection-ID SLC-off
        113: ('Landsat-7', 'ETM+'),  # pre-collection-ID SLC-on
        189: ('Terra', 'ASTER'),  # ASTER L1T
        249: ('Sentinel-2A', 'MSI'),  # actually only Sentinel-2
        250: ('Landsat-8', 'OLI_TIRS'),
        251: ('Landsat-7', 'ETM+'),
        252: ('Landsat-5', 'TM'),  # also includes Landsat-4
        }
    try:
        return conv_dict[dsid]
    except KeyError:
        raise ValueError('No satellite / sensor tuple available for dataset ID %s.' % dsid)


def sat_sen_to_datasetid(satellite, sensor):
    # type: (str, str) -> int
    conv_dict = {
        ('Landsat-5', 'TM'): 252,
        ('Landsat-7', 'ETM+'): 251,
        ('Landsat-8', 'OLI_TIRS'): 250,
        ('Sentinel-2A', 'MSI'): 249,
        ('Sentinel-2B', 'MSI'): 249,
        ('Terra', 'ASTER'): 189  # ASTER L1T
    }
    try:
        return conv_dict[(satellite, sensor)]
    except KeyError:
        raise ValueError('No dataset ID available for %s %s.' % (satellite, sensor))
