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

"""Module 'metadata' for handling any type of metadata of GeoMultiSens compatible sensor systems."""

from __future__ import (division, print_function, unicode_literals, absolute_import)

import collections
import datetime
import glob
import math
import os
import re
import sys
import warnings
import iso8601
import xml.etree.ElementTree as ET
from typing import List, TYPE_CHECKING  # noqa F401  # flake8 issue

import numpy as np
import pyproj
from matplotlib import dates as mdates
from pyorbital import astronomy
from natsort import natsorted

from py_tools_ds.geo.map_info import geotransform2mapinfo
from py_tools_ds.geo.projection import WKT2EPSG
from pyrsr import RSR
from sicor.options import get_options as get_ac_options

from ..options.config import GMS_config as CFG
from ..io.input_reader import open_specific_file_within_archive, Solar_Irradiance_reader, SRF_Reader
from ..io.output_writer import enviHdr_keyOrder
from ..algorithms import geoprocessing as GEOP
from ..misc import helper_functions as HLP_F
from ..misc import database_tools as DB_T
from ..misc.path_generator import path_generator, get_path_ac_options
from ..misc.definition_dicts import get_GMS_sensorcode, is_dataset_provided_as_fullScene, datasetid_to_sat_sen
from ..misc.exceptions import ACNotSupportedError

if TYPE_CHECKING:
    from ..model.gms_object import GMS_identifier  # noqa F401  # flake8 issue

__author__ = 'Daniel Scheffler', 'Robert Behling'


class METADATA(object):
    def __init__(self, GMS_id):
        # private attributes
        self._AcqDateTime = None

        # unpack GMS_identifier
        self.GMS_identifier = GMS_id
        self.image_type = GMS_id.image_type
        self.Satellite = GMS_id.satellite
        self.Sensor = GMS_id.sensor
        self.Subsystem = GMS_id.subsystem
        self.proc_level = GMS_id.proc_level
        self.logger = GMS_id.logger

        self.Dataname = ''
        self.FolderOrArchive = ''
        self.Metafile = ""  # File containing image metadata (automatically found)
        self.EntityID = ""  # ID to identify the original scene
        self.SceneID = ''  # postgreSQL-database identifier
        self.Sensormode = ""
        self.gResolution = -99.  # resolution [m]
        self.AcqDate = ""  # YYYY-MM-DD
        self.AcqTime = ""  # HH:MM:SS
        self.Offsets = {}  # Dict with offset for each band (radiance)
        self.Gains = {}  # Dict with gain for each band (radiance)
        self.OffsetsRef = {}  # Dict with offset for each band for conversion to Reflectance (Landsat8)
        self.GainsRef = {}  # Dict with gain for each band for conversion to Reflectance (Landsat8)
        self.CWL = {}
        self.FWHM = {}
        self.ProcLCode = ""  # processing Level: Sensor specific Code
        self.ProcLStr = ""  # processing Level: Sensor independent String (raw,rad cal, rad+geom cal, ortho)
        self.SunElevation = -99.0  # Sun elevation angle at center of product [Deg]
        # Sun azimuth angle at center of product, in degrees from North (clockwise) at the time of the first image line
        self.SunAzimuth = -99.0
        self.SolIrradiance = []
        self.ThermalConstK1 = {}
        self.ThermalConstK2 = {}
        self.EarthSunDist = 1.0
        # viewing zenith angle of the Sensor (offNadir) [Deg] (usually) in Case of RapidEye "+"
        # being East and “-” being West
        self.ViewingAngle = -99.0
        self.ViewingAngle_arrProv = {}
        # viewing azimuth angle. The angle between the view direction of the satellite and a line perpendicular to
        # the image or tile center.[Deg]
        self.IncidenceAngle = -9999.99
        self.IncidenceAngle_arrProv = {}
        self.FOV = 9999.99  # field of view of the sensor [Deg]
        # Sensor specific quality code: See ro2/behling/Satelliten/doc_allg/ReadOutMetadata/SatMetadata.xls
        self.Quality = []
        self.PhysUnit = "DN"
        # Factor to get reflectance values in [0-1]. Sentinel2A provides scaling factors for the Level1C
        # TOA-reflectance products
        self.ScaleFactor = -99
        self.CS_EPSG = -99.  # EPSG-Code of coordinate system
        self.CS_TYPE = ""
        self.CS_DATUM = ""
        self.CS_UTM_ZONE = -99.
        self.WRS_path = -99.
        self.WRS_row = -99.
        # List of Corner Coordinates in order of Lon/Lat/DATA_X/Data_Y for all given image corners
        self.CornerTieP_LonLat = []
        self.CornerTieP_UTM = []
        self.LayerBandsAssignment = []  # List of spectral bands in the same order as they are stored in the rasterfile.
        self.additional = []
        self.image_type = 'RSD'
        self.orbitParams = {}
        self.overpassDurationSec = -99.
        self.scene_length = -99.
        self.rows = -99.
        self.cols = -99.
        self.bands = -99.
        self.nBands = -99.
        self.map_info = []
        self.projection = ""
        self.wvlUnit = ""
        self.spec_vals = {'fill': None, 'zero': None, 'saturated': None}

        self.version_gms_preprocessing = CFG.version
        self.versionalias_gms_preprocessing = CFG.versionalias

    def read_meta(self, scene_ID, stacked_image, data_folderOrArchive, LayerBandsAssignment=None):
        """
        Read metadata.
        """

        self.SceneID = scene_ID
        self.Dataname = stacked_image
        self.FolderOrArchive = data_folderOrArchive
        self.LayerBandsAssignment = LayerBandsAssignment if LayerBandsAssignment else []

        if re.search(r"SPOT", self.Satellite, re.I):
            self.Read_SPOT_dimap2()
        elif re.search(r"Terra", self.Satellite, re.I):
            self.Read_ASTER_hdffile(self.Subsystem)
        elif re.search(r"Sentinel-2A", self.Satellite, re.I) or re.search(r"Sentinel-2B", self.Satellite, re.I):
            self.Read_Sentinel2_xmls()
        elif re.search(r"LANDSAT", self.Satellite, re.I):
            self.Read_LANDSAT_mtltxt(self.LayerBandsAssignment)
        elif re.search(r"RapidEye", self.Satellite, re.I):
            self.Read_RE_metaxml()
        elif re.search(r"ALOS", self.Satellite, re.I):
            self.Read_ALOS_summary()
            self.Read_ALOS_LEADER()  # for gains and offsets
        else:
            raise NotImplementedError("%s is not a supported sensor or sensorname is misspelled." % self.Satellite)

        return self

    def __getstate__(self):
        """Defines how the attributes of MetaObj instances are pickled."""
        if self.logger:
            self.logger.close()

        return self.__dict__

    @property
    def AcqDateTime(self):
        """Returns a datetime.datetime object containing date, time and timezone (UTC time)."""
        if not self._AcqDateTime and self.AcqDate and self.AcqTime:
            self._AcqDateTime = datetime.datetime.strptime('%s %s%s' % (self.AcqDate, self.AcqTime, '.000000+0000'),
                                                           '%Y-%m-%d %H:%M:%S.%f%z')

        return self._AcqDateTime

    @AcqDateTime.setter
    def AcqDateTime(self, DateTime):
        # type: (datetime.datetime) -> None
        if isinstance(DateTime, str):
            self._AcqDateTime = datetime.datetime.strptime(DateTime, '%Y-%m-%d %H:%M:%S.%f%z')
        elif isinstance(DateTime, datetime.datetime):
            self._AcqDateTime = DateTime

        self.AcqDate = DateTime.strftime('%Y-%m-%d')
        self.AcqTime = DateTime.strftime('%H:%M:%S')

    @property
    def overview(self):
        attr2include = \
            ['Dataname', 'Metafile', 'EntityID', 'Satellite', 'Sensor', 'Subsystem', 'gResolution', 'AcqDate',
             'AcqTime', 'CWL', 'FWHM', 'Offsets', 'Gains', 'ProcLCode', 'ProcLStr', 'SunElevation', 'SunAzimuth',
             'ViewingAngle', 'IncidenceAngle', 'FOV', 'SolIrradiance', 'ThermalConstK1', 'ThermalConstK2',
             'EarthSunDist', 'Quality', 'PhysUnit', 'additional', 'GainsRef', 'OffsetsRef', 'CornerTieP_LonLat',
             'CS_EPSG', 'CS_TYPE', 'CS_DATUM', 'CS_UTM_ZONE', 'LayerBandsAssignment']
        return collections.OrderedDict((attr, getattr(self, attr)) for attr in attr2include)

    @property
    def LayerBandsAssignment_full(self):
        # type: () -> list
        """Return complete LayerBandsAssignment without excluding thermal or panchromatic bands.

        NOTE: CFG.sort_bands_by_cwl is respected, so returned list may be sorted by central wavelength
        """
        return get_LayerBandsAssignment(self.GMS_identifier, no_thermal=False, no_pan=False, return_fullLBA=True)

    @property
    def bandnames(self):
        return [('Band %s' % i) for i in self.LayerBandsAssignment]

    def Read_SPOT_dimap2(self):
        """----METHOD_2------------------------------------------------------------
        # read metadata from spot dimap file
        """

        # self.default_attr()
        if os.path.isdir(self.FolderOrArchive):
            glob_res = glob.glob(os.path.join(self.FolderOrArchive, '*/scene01/metadata.dim'))
            assert len(glob_res) > 0, 'No metadata.dim file can be found in %s!' % self.FolderOrArchive
            self.Metafile = glob_res[0]
            dim_ = open(self.Metafile, "r").read()
        else:  # archive
            dim_, self.Metafile = open_specific_file_within_archive(self.FolderOrArchive, '*/scene01/metadata.dim')

        # special values
        h1 = re.findall(r"<SPECIAL_VALUE_INDEX>([a-zA-Z0-9]*)</SPECIAL_VALUE_INDEX>", dim_, re.I)
        h2 = re.findall(r"<SPECIAL_VALUE_TEXT>([a-zA-Z0-9]*)</SPECIAL_VALUE_TEXT>", dim_, re.I)
        self.additional.append(["SpecialValues:"])
        for ii, ind in enumerate(h1):
            self.additional[0].append(["%s:%s" % (ind, h2[ii])])

        # EntityID
        h3 = re.search(r"<SOURCE_ID>([a-zA-Z0-9]*)</SOURCE_ID>", dim_, re.I)
        self.EntityID = h3.group(1)

        # AcqDate
        h4 = re.search(r"<IMAGING_DATE>([0-9-]*)</IMAGING_DATE>", dim_, re.I)
        AcqDate = h4.group(1)

        # Earth sun distance
        self.EarthSunDist = self.get_EarthSunDistance(AcqDate)

        # AcqTime
        h5 = re.search(r"<IMAGING_TIME>([0-9:]*)</IMAGING_TIME>", dim_, re.I)
        AcqTime = h5.group(1)

        # set self.AcqDateTime as well as self.AcqDate and self.AcqTime
        self.AcqDateTime = datetime.datetime.strptime(
            '%s %s%s' % (AcqDate, AcqTime, '.000000+0000'), '%Y-%m-%d %H:%M:%S.%f%z')

        # Satellite + Sensor
        h6 = re.search(r"<MISSION>([a-zA-Z]*)</MISSION>[a-zA-Z0-9\s]*"
                       r"<MISSION_INDEX>([0-9]*)</MISSION_INDEX>[a-zA-Z0-9\s]*"
                       r"<INSTRUMENT>([a-zA-Z]*)</INSTRUMENT>[a-zA-Z0-9\s]*"
                       r"<INSTRUMENT_INDEX>([0-9]*)</INSTRUMENT_INDEX>[a-zA-Z0-9\s]*"
                       r"<SENSOR_CODE>([a-zA-Z0-9]*)</SENSOR_CODE>",
                       dim_, re.I)
        self.Satellite = "-".join([h6.group(1), h6.group(2)])
        self.Sensor = "".join([h6.group(3), h6.group(4), h6.group(5)])

        # Angles: incidence angle, sunAzimuth, sunElevation
        h7 = re.search(r"<INCIDENCE_ANGLE>(.*)</INCIDENCE_ANGLE>[\s\S]*"
                       r"<SUN_AZIMUTH>(.*)</SUN_AZIMUTH>[\s\S]"
                       r"*<SUN_ELEVATION>(.*)</SUN_ELEVATION>", dim_, re.I)
        self.IncidenceAngle = float(h7.group(1))
        self.SunAzimuth = float(h7.group(2))
        self.SunElevation = float(h7.group(3))

        # Viewing Angle: not always included in the metadata.dim file
        h8 = re.search(r"<VIEWING_ANGLE>(.*)</VIEWING_ANGLE>", dim_, re.I)
        if type(h8).__name__ == 'NoneType':
            self.ViewingAngle = 0
        else:
            self.ViewingAngle = float(h8.group(1))

        # Field of View
        self.FOV = get_FieldOfView(self.GMS_identifier)

        # Units
        self.ScaleFactor = 1
        self.PhysUnit = "DN"

        # ProcLevel
        h11 = re.search(r"<PROCESSING_LEVEL>([a-zA-Z0-9]*)</PROCESSING_LEVEL>", dim_, re.I)
        self.ProcLCode = h11.group(1)

        # Quality
        h12 = re.findall(r"<Bad_Pixel>[\s]*"
                         r"<PIXEL_INDEX>([0-9]*)</PIXEL_INDEX>[\s]*"
                         r"<BAD_PIXEL_STATUS>([^<]*)</BAD_PIXEL_STATUS>"
                         r"</Bad_Pixel>", dim_,
                         re.I)
        self.Quality = h12

        # Coordinate Reference System
        re_CS_EPSG = re.search(r'<HORIZONTAL_CS_CODE>epsg:([0-9]*)</HORIZONTAL_CS_CODE>', dim_, re.I)
        re_CS_TYPE = re.search(r'<HORIZONTAL_CS_TYPE>([a-zA-Z0-9]*)</HORIZONTAL_CS_TYPE>', dim_, re.I)
        re_CS_DATUM = re.search(r'<HORIZONTAL_CS_NAME>([\w+\s]*)</HORIZONTAL_CS_NAME>', dim_, re.I)
        self.CS_EPSG = int(re_CS_EPSG.group(1)) if re_CS_EPSG is not None else self.CS_EPSG
        self.CS_TYPE = 'LonLat' if re_CS_TYPE is not None and re_CS_TYPE.group(1) == 'GEOGRAPHIC' else 'UTM' \
            if re_CS_TYPE is not None and re_CS_TYPE.group(1) == 'UTM' else self.CS_TYPE
        self.CS_DATUM = 'WGS84' if re_CS_DATUM is not None and re_CS_DATUM.group(1) == 'WGS 84' else self.CS_DATUM

        # Corner Coordinates
        h121 = re.findall(r"<TIE_POINT_CRS_X>(.*)</TIE_POINT_CRS_X>", dim_, re.I)
        h122 = re.findall(r"<TIE_POINT_CRS_Y>(.*)</TIE_POINT_CRS_Y>", dim_, re.I)
        if len(h121) == 4 and self.CS_TYPE == 'LonLat':
            # Set Corner Tie Point Coordinates (order = UL,UR,LL,LR)
            self.CornerTieP_LonLat.append(tuple([float(h121[0]), float(h122[0])]))  # UL
            self.CornerTieP_LonLat.append(tuple([float(h121[1]), float(h122[1])]))  # UR
            self.CornerTieP_LonLat.append(tuple([float(h121[3]), float(h122[3])]))  # LL
            self.CornerTieP_LonLat.append(tuple([float(h121[2]), float(h122[2])]))  # LR
            #    ul_lon,ul_lat = self.inDs.GetGCPs()[0].GCPX,self.inDs.GetGCPs()[0].GCPY # funktioniert nur bei SPOT
            #    lr_lon,lr_lat = self.inDs.GetGCPs()[2].GCPX,self.inDs.GetGCPs()[2].GCPY

        ##########################
        # band specific metadata #
        ##########################

        LBA_full_sorted = natsorted(self.LayerBandsAssignment_full)

        # Gains and Offsets
        h9 = re.search(r"<Image_Interpretation>[\s\S]*</Image_Interpretation>", dim_, re.I)
        h9_ = h9.group(0)
        h91 = re.findall(r"<PHYSICAL_UNIT>([^<]*)</PHYSICAL_UNIT>", h9_, re.I)
        h92 = re.findall(r"<PHYSICAL_BIAS>([^<]*)</PHYSICAL_BIAS>", h9_, re.I)
        h93 = re.findall(r"<PHYSICAL_GAIN>([^<]*)</PHYSICAL_GAIN>", h9_, re.I)
        self.additional.append(["Physical Units per band:"])
        for ii, ind in enumerate(h91):  # FIXME does not respect sort_bands_by_cwl
            self.additional[-1].append(ind)
        # Offsets
        for ii, (ind, band) in enumerate(zip(h92, LBA_full_sorted)):
            self.Offsets[band] = float(ind)
        # Gains
        for ii, (ind, band) in enumerate(zip(h93, LBA_full_sorted)):
            # gains in dimap file represent reciprocal 1/gain
            self.Gains[band] = 1 / float(ind)

        # Solar irradiance, central wavelengths , full width half maximum per band
        self.wvlUnit = 'Nanometers'
        # derive number of bands from number of given gains/offsets in header file or from raster data
        # noinspection PyBroadException
        try:
            self.nBands = (np.mean([len(self.Gains), len(self.Offsets)])
                           if np.std([len(self.Gains), len(self.Offsets)]) == 0 and len(self.Gains) != 0 else
                           GEOP.GEOPROCESSING(self.Dataname, self.logger).bands)
        except Exception:
            self.logger.warning('Unable to get number of bands for the dataset %s Provider values are used for '
                                'solar irradiation, CWL and FWHM!.' % self.Dataname)
        self.LayerBandsAssignment = get_LayerBandsAssignment(self.GMS_identifier, self.nBands)

        # Exact values calculated based in SRFs
        self.SolIrradiance, self.CWL, self.FWHM = self.calc_solar_irradiance_CWL_FWHM_per_band()
        # Provider values
        if not self.SolIrradiance:
            h10 = re.search(r"<Solar_Irradiance>[\s\S]*"
                            r"</Solar_Irradiance>", dim_, re.I)
            h10_ = h10.group(0)
            h101 = re.findall(r"<SOLAR_IRRADIANCE_VALUE>([^<]*)"
                              r"</SOLAR_IRRADIANCE_VALUE>", h10_, re.I)
            if h101:
                self.SolIrradiance = dict(zip(LBA_full_sorted, h101))
                #    self.additional.append(["Solar Irradiance per band:"])
                #    for ii,ind in enumerate(h101):
                #       self.additional[-1].append(ind)
            else:  # Preconfigured Irradiation values
                spot_irr_dic = {
                    'SPOT1a': dict(zip(LBA_full_sorted, [1855., 1615., 1090., 1680.])),
                    'SPOT1b': dict(zip(LBA_full_sorted, [1845., 1575., 1040., 1690.])),
                    'SPOT2a': dict(zip(LBA_full_sorted, [1865., 1620., 1085., 1705.])),
                    'SPOT2b': dict(zip(LBA_full_sorted, [1865., 1615., 1090., 1670.])),
                    'SPOT3a': dict(zip(LBA_full_sorted, [1854., 1580., 1065., 1668.])),
                    'SPOT3b': dict(zip(LBA_full_sorted, [1855., 1597., 1067., 1667.])),
                    'SPOT4a': dict(zip(LBA_full_sorted, [1843., 1568., 1052., 233., 1568.])),
                    'SPOT4b': dict(zip(LBA_full_sorted, [1851., 1586., 1054., 240., 1586.])),
                    'SPOT5a': dict(zip(LBA_full_sorted, [1858., 1573., 1043., 236., 1762.])),
                    'SPOT5b': dict(zip(LBA_full_sorted, [1858., 1575., 1047., 234., 1773.]))}
                self.SolIrradiance = spot_irr_dic[get_GMS_sensorcode(self.GMS_identifier)]
            # Preconfigured CWLs --   # ref: Guyot & Gu (1994): 'Effect of Radiometric Corrections on NDVI-Determined
            # from SPOT-HRV and Landsat-TM Data'; Hill 1990 Comparative Analysis of Landsat-5 TM and SPOT HRV-1 Data for
            # Use in Multiple Sensor Approaches ; # resource: SPOT techical report: Resolutions and spectral modes
            sensorcode = get_GMS_sensorcode(self.GMS_identifier)[:2]
            if sensorcode in ['SPOT1a', 'SPOT1b', 'SPOT2a', 'SPOT2b', 'SPOT3a', 'SPOT3b']:
                self.CWL = dict(zip(LBA_full_sorted, [545., 638., 819., 615.]))
            elif sensorcode in ['SPOT4a', 'SPOT4b']:
                self.CWL = dict(zip(LBA_full_sorted, [540., 650., 835., 1630., 645.]))
            elif sensorcode == ['SPOT5a', 'SPOT5b']:
                self.CWL = dict(zip(LBA_full_sorted, [540., 650., 835., 1630., 595.]))

        self.orbitParams = get_orbit_params(self.GMS_identifier)
        self.filter_layerdependent_metadata()
        self.spec_vals = get_special_values(self.GMS_identifier)

    def Read_LANDSAT_mtltxt(self, LayerBandsAssignment):
        """----METHOD_3------------------------------------------------------------
        read metadata from LANDSAT metafile: <dataname>.MTL.txt. Metadatafile of LPGS processing chain
        :param LayerBandsAssignment:
        """

        # self.default_attr()
        self.LayerBandsAssignment = LayerBandsAssignment
        self.nBands = len(LayerBandsAssignment)
        if os.path.isdir(self.FolderOrArchive):
            glob_res = glob.glob(os.path.join(self.FolderOrArchive, '*MTL.txt'))
            assert len(glob_res) > 0, 'No *.MTL metadata file can be found in %s!' % self.FolderOrArchive
            self.Metafile = glob_res[0]
            mtl_ = open(self.Metafile, "r").read()
        else:  # archive
            mtl_, self.Metafile = open_specific_file_within_archive(self.FolderOrArchive, '*MTL.txt')

        # Processing Level
        h1 = re.search(r'PRODUCT_TYPE = "([a-zA-Z0-9]*)"', mtl_, re.I)
        if h1 is None:
            h1 = re.search(r'DATA_TYPE = "([a-zA-Z0-9]*)"', mtl_, re.I)
        self.ProcLCode = h1.group(1)

        # Satellite + Sensor + Sensor Mode
        h2 = re.search(r'SPACECRAFT_ID = "([a-zA-Z0-9_]*)"[\s]*'
                       r'SENSOR_ID = "([a-zA-Z0-9+]*)"[\s]*'
                       r'SENSOR_MODE = "([\S]*)"',
                       mtl_, re.I)
        if h2:
            self.Satellite = 'Landsat-%s' % re.search(r'LANDSAT[\D]*([0-9])', h2.group(1), re.I).group(1)
            self.Sensor = h2.group(2)
            self.Sensormode = h2.group(3)
        else:
            h2a = re.search(r'SPACECRAFT_ID = "([a-zA-Z0-9_]*)"', mtl_, re.I)
            h2b = re.search(r'SENSOR_ID = "([a-zA-Z0-9_+]*)"', mtl_, re.I)
            h2c = re.search(r'SENSOR_MODE = "([a-zA-Z0-9_+]*)"', mtl_, re.I)
            self.Satellite = 'Landsat-%s' % re.search(r'LANDSAT[\D]*([0-9])', h2a.group(1), re.I).group(1)
            self.Sensor = h2b.group(1)
            self.Sensormode = h2c.group(1) if h2c is not None else self.Sensormode  # Landsat-8
        self.Sensor = 'ETM+' if self.Sensor == 'ETM' else self.Sensor

        # EntityID
        h2c = re.search(r'LANDSAT_SCENE_ID = "([A-Z0-9]*)"', mtl_, re.I)
        if h2c:
            self.EntityID = h2c.group(1)

        # Acquisition Date + Time
        h3 = re.search(r'ACQUISITION_DATE = ([0-9-]*)[\s]*'
                       r'SCENE_CENTER_SCAN_TIME = "?([0-9:]*)"?',
                       mtl_, re.I)
        if h3 is None:
            h3 = re.search(r'DATE_ACQUIRED = ([0-9-]*)[\s]*'
                           r'SCENE_CENTER_TIME = "?([0-9:]*)"?',
                           mtl_, re.I)
        AcqDate = h3.group(1)
        AcqTime = h3.group(2)

        # set self.AcqDateTime as well as self.AcqDate and self.AcqTime
        self.AcqDateTime = datetime.datetime.strptime(
            '%s %s%s' % (AcqDate, AcqTime, '.000000+0000'), '%Y-%m-%d %H:%M:%S.%f%z')

        # Earth sun distance
        self.EarthSunDist = self.get_EarthSunDistance(self.AcqDate)

        # Units
        self.ScaleFactor = 1
        self.PhysUnit = "DN"

        # Angles: incidence angle, sunAzimuth, sunElevation, field of view
        h5 = re.search(r"SUN_AZIMUTH = ([\S]*)[\s]*"
                       r"SUN_ELEVATION = ([\S]*)",
                       mtl_, re.I)
        self.SunAzimuth = float(h5.group(1))
        self.SunElevation = float(h5.group(2))
        self.FOV = get_FieldOfView(self.GMS_identifier)

        # Quality
        h6 = re.search(r"GROUP = CORRECTIONS_APPLIED[\s\S]*"
                       r"END_GROUP = CORRECTIONS_APPLIED",
                       mtl_, re.I)
        if h6 is None:
            h6 = re.search(r"GROUP = IMAGE_ATTRIBUTES[\s\S]*"
                           r"END_GROUP = IMAGE_ATTRIBUTES",
                           mtl_, re.I)

        h6_ = h6.group(0)
        h61 = (h6_.split("\n"))
        x = 0
        for i in h61:
            if x == 0 or x + 1 == len(h61):
                pass
            else:
                i_ = i.strip().replace('"', "")
                self.Quality.append(i_.split(" = "))
            x += 1

        # Additional: coordinate system, geom. Resolution
        h7 = re.search(r"GROUP = PROJECTION_PARAMETERS[\s\S]*END_GROUP = L1_METADATA_FILE", mtl_, re.I)
        h7_ = h7.group(0)
        h71 = (h7_.split("\n"))
        for x, i in enumerate(h71):
            if re.search(r"Group", i, re.I):
                pass
            else:
                i_ = i.strip().replace('"', "")
                self.additional.append(i_.split(" = "))
        re_CS_TYPE = re.search(r'MAP_PROJECTION = "([\w+\s]*)"', h7_, re.I)
        re_CS_DATUM = re.search(r'DATUM = "([\w+\s]*)"', h7_, re.I)
        re_CS_UTM_ZONE = re.search(r'ZONE_NUMBER = ([0-9]*)\n', mtl_, re.I)
        re_CS_UTM_ZONE = re.search(r'UTM_ZONE = ([0-9]*)\n', h7_,
                                   re.I) if re_CS_UTM_ZONE is None else re_CS_UTM_ZONE  # Landsat8
        self.CS_TYPE = 'LonLat' if re_CS_TYPE is not None and re_CS_TYPE.group(1) == 'GEOGRAPHIC' else 'UTM' \
            if re_CS_TYPE is not None and re_CS_TYPE.group(1) == 'UTM' else self.CS_TYPE
        self.CS_DATUM = 'WGS84' if re_CS_DATUM is not None and re_CS_DATUM.group(1) == 'WGS84' else self.CS_DATUM
        self.CS_UTM_ZONE = int(re_CS_UTM_ZONE.group(1)) if re_CS_UTM_ZONE is not None else self.CS_UTM_ZONE
        # viewing Angle
        self.ViewingAngle = 0
        # Landsat8
        h8 = re.search(r"ROLL_ANGLE = ([\S]*)", mtl_, re.I)
        if h8:
            self.ViewingAngle = float(h8.group(1))

        # Corner Coordinates ## Lon/Lat for all given image corners UL,UR,LL,LR (tuples)
        h10_UL = re.findall(r"PRODUCT_UL_CORNER_[A-Z]+ = (.*)[\S]*", mtl_, re.I)
        h10_UR = re.findall(r"PRODUCT_UR_CORNER_[A-Z]+ = (.*)[\S]*", mtl_, re.I)
        h10_LL = re.findall(r"PRODUCT_LL_CORNER_[A-Z]+ = (.*)[\S]*", mtl_, re.I)
        h10_LR = re.findall(r"PRODUCT_LR_CORNER_[A-Z]+ = (.*)[\S]*", mtl_, re.I)
        if not h10_UL:  # Landsat8
            h10_UL = re.findall(r"CORNER_UL_[\S]+ = (.*)[\S]*", mtl_, re.I)
            h10_UR = re.findall(r"CORNER_UR_[\S]+ = (.*)[\S]*", mtl_, re.I)
            h10_LL = re.findall(r"CORNER_LL_[\S]+ = (.*)[\S]*", mtl_, re.I)
            h10_LR = re.findall(r"CORNER_LR_[\S]+ = (.*)[\S]*", mtl_, re.I)
        if h10_UL:  # Set Corner Tie Point Coordinates (order = UL,UR,LL,LR)
            self.CornerTieP_LonLat.append(tuple([float(h10_UL[i]) for i in [1, 0]]))
            self.CornerTieP_LonLat.append(tuple([float(h10_UR[i]) for i in [1, 0]]))
            self.CornerTieP_LonLat.append(tuple([float(h10_LL[i]) for i in [1, 0]]))
            self.CornerTieP_LonLat.append(tuple([float(h10_LR[i]) for i in [1, 0]]))
            self.CornerTieP_UTM.append(tuple([float(h10_UL[i]) for i in [2, 3]]))
            self.CornerTieP_UTM.append(tuple([float(h10_UR[i]) for i in [2, 3]]))
            self.CornerTieP_UTM.append(tuple([float(h10_LL[i]) for i in [2, 3]]))
            self.CornerTieP_UTM.append(tuple([float(h10_LR[i]) for i in [2, 3]]))

        # WRS path/row
        h11_p = re.search(r'WRS_PATH = ([0-9]*)', mtl_, re.I)
        if h11_p:
            self.WRS_path = h11_p.group(1)
        h11_r1 = re.search(r'STARTING_ROW = ([0-9]*)', mtl_, re.I)
        h11_r2 = re.search(r'ENDING_ROW = ([0-9]*)', mtl_, re.I)
        if h11_r1 is None:  # Landsat-8
            h11_r = re.search(r'WRS_ROW = ([0-9]*)', mtl_, re.I)
            self.WRS_row = int(h11_r.group(1))
        else:
            self.WRS_row = int(h11_r1.group(1)) if h11_r1.group(1) == h11_r2.group(1) else self.WRS_row

        # Fill missing values
        if self.EntityID == '':
            self.logger.info('Scene-ID could not be extracted and has to be retrieved from %s metadata database...'
                             % self.Satellite)
            result = DB_T.get_info_from_postgreSQLdb(CFG.conn_database, 'scenes', ['entityID'],
                                                     {'id': self.SceneID})

            if len(result) == 1:  # e.g. [('LE71950282003121EDC00',)]
                self.EntityID = result[0][0]
            elif len(result) == 0:
                self.logger.warning("Scene ID could not be assigned because no dataset matching to the query "
                                    "parameters could be found in metadata database.")
            else:  # e.g. [('LE71950282003121EDC00',), ('LE71950282003105ASN00',)]
                self.logger.warning("Scene ID could not be assigned because %s datasets matching to the query "
                                    "parameters were found in metadata database." % len(result))
        # if self.EntityID=='':
        #     dataset = 'LANDSAT_TM' if self.Satellite=='Landsat-5' else \
        #          'LANDSAT_ETM' if self.Satellite=='Landsat-7' else 'LANDSAT_8' if self.Satellite=='Landsat-8' else ''
        #     if dataset != '':
        #         webmeta = list(usgsapi.search(dataset,'EE',distance=0,ll={'longitude':self.CornerTieP_LonLat[2][0], \
        #                     'latitude':self.CornerTieP_LonLat[2][1]},ur={'longitude':self.CornerTieP_LonLat[1][0], \
        #                     'latitude':self.CornerTieP_LonLat[1][1]},start_date=self.AcqDate,end_date=self.AcqDate))
        #         if len(webmeta)==1:
        #             self.EntityID=webmeta[0]['entityId']
        #         else:
        #             sen  = {'MSS':'M','TM':'T','ETM+':'E','OLI_TIRS':'C','OLI':'O'}[self.Sensor]
        #             sat  = self.Satellite.split('-')[1]
        #             path_res = re.search(r'WRS_PATH = ([0-9]+)',mtl_, re.I)
        #             path_str = "%03d"%int(path_res.group(1)) if path_res!=None else '000'
        #             row_res  = re.search(r'STARTING_ROW = ([0-9]+)',mtl_, re.I)
        #             if row_res is None: row_res = re.search(r'WRS_ROW = ([0-9]+)',mtl_, re.I)
        #             row_str  = "%03d"%int(row_res.group(1)) if row_res!=None else '000'
        #             tt       = datetime.datetime.strptime(self.AcqDate, '%Y-%m-%d').timetuple()
        #             julianD  = '%d%03d'%(tt.tm_year,tt.tm_yday)
        #             station_res  = re.search(r'GROUND_STATION = "([\S]+)"',mtl_, re.I)
        #             if station_res is None: station_res  = re.search(r'STATION_ID = "([\S]+)"',mtl_, re.I)
        #             station_str = station_res.group(1) if station_res is not None else 'XXX'
        #             idWithoutVersion = 'L%s%s%s%s%s%s'%(sen,sat,path_str,row_str,julianD,station_str)
        #             filt_webmeta     = [i for i in webmeta if i['entityId'].startswith(idWithoutVersion)]
        #             if len(filt_webmeta) == 1:
        #                 self.EntityID = filt_webmeta[0]['entityId']

        ##########################
        # band specific metadata #
        ##########################
        LBA_full_sorted = natsorted(self.LayerBandsAssignment_full)

        # Gains and Offsets
        h4 = re.search(r"GROUP = MIN_MAX_RADIANCE[\s\S]*END_GROUP = MIN_MAX_PIXEL_VALUE", mtl_, re.I)
        h4_ = h4.group(0)
        h4max_rad = re.findall(r" LMAX_BAND[0-9]+ = ([\S]*)", h4_, re.I)  # space in front IS needed
        h4min_rad = re.findall(r" LMIN_BAND[0-9]+ = ([\S]*)", h4_, re.I)  # space in front IS needed
        h4max_pix = re.findall(r"QCALMAX_BAND[0-9]+ = ([\S]*)", h4_, re.I)
        h4min_pix = re.findall(r"QCALMIN_BAND[0-9]+ = ([\S]*)", h4_, re.I)
        if not h4max_rad:
            h4max_rad = re.findall(r" RADIANCE_MAXIMUM_BAND_[0-9_VCID]+ = ([\S]*)", h4_,
                                   re.I)  # space in front IS needed
            h4min_rad = re.findall(r" RADIANCE_MINIMUM_BAND_[0-9_VCID]+ = ([\S]*)", h4_,
                                   re.I)  # space in front IS needed
            h4max_pix = re.findall(r"QUANTIZE_CAL_MAX_BAND_[0-9_VCID]+ = ([\S]*)", h4_, re.I)
            h4min_pix = re.findall(r"QUANTIZE_CAL_MIN_BAND_[0-9_VCID]+ = ([\S]*)", h4_, re.I)
        # additional: LMAX, LMIN, QCALMAX, QCALMIN
        self.additional.append([["LMAX"], ["LMIN"], ["QCALMAX"], ["QCALMIN"]])
        # Offsets + Gains
        Gains, Offsets = [], []
        for ii, ind in enumerate(h4min_rad):
            Gains.append(
                (float(h4max_rad[ii]) - float(h4min_rad[ii])) / (float(h4max_pix[ii]) - float(h4min_pix[ii])))
            Offsets.append(float(ind) - float(h4min_pix[ii]) * Gains[-1])
            self.additional[-1][-4].append(h4max_rad[ii])
            self.additional[-1][-3].append(h4min_rad[ii])
            self.additional[-1][-2].append(h4max_pix[ii])
            self.additional[-1][-1].append(h4min_pix[ii])
        self.Gains = {bN: Gains[i] for i, bN in enumerate(LBA_full_sorted)}
        self.Offsets = {bN: Offsets[i] for i, bN in enumerate(LBA_full_sorted)}

        # Solar irradiance, central wavelengths , full width half maximum per band
        self.wvlUnit = 'Nanometers'
        # Exact values calculated based in SRFs
        self.SolIrradiance, self.CWL, self.FWHM = self.calc_solar_irradiance_CWL_FWHM_per_band()  # 3x dict
        # Provider values
        if not self.SolIrradiance:  # Preconfigured Irradiation and CWL values
            if re.search(r"[\D]*5", self.Satellite):
                # Landsat 5; resource for center wavelength (6 = thermal)
                self.SolIrradiance = {'1': 1957.,
                                      '2': 1826.,
                                      '3': 1554.,
                                      '4': 1036.,
                                      '5': 215.,
                                      '6': 0.0,
                                      '7': 80.67}
                self.CWL = {'1': 485.,
                            '2': 560.,
                            '3': 660.,
                            '4': 830.,
                            '5': 1650.,
                            '6': 11450.,
                            '7': 2215.}
            if re.search(r"[\D]*7", self.Satellite):
                # Landsat 7; resource for center wavelength:
                # http://opticks.org/confluence/display/opticksDev/Sensor+Wavelength+Definitions
                # 6L(thermal),6H(thermal),B8(pan)
                self.SolIrradiance = {'1': 1969.,
                                      '2': 1840.,
                                      '3': 1551.,
                                      '4': 1044.,
                                      '5': 225.7,
                                      '6L': 0.0,
                                      '6H': 0.0,
                                      '7': 82.07,
                                      '8': 1368.}
                self.CWL = {'1': 482.5,
                            '2': 565.,
                            '3': 660.,
                            '4': 825.,
                            '5': 1650.,
                            '6L': 11450.,
                            '6H': 11450.,
                            '7': 2215.,
                            '8': 710.}
            if re.search(r"[\D]*8", self.Satellite):  # Landsat 8
                # no irradiation values available
                self.CWL = {'1': 443.,
                            '2': 482.6,
                            '3': 561.3,
                            '4': 654.6,
                            '5': 864.6,
                            '6': 1609.1,
                            '7': 2201.2,
                            '8': 591.7,
                            '9': 1373.5,
                            '10': 10903.6,
                            '11': 12003.}
        # if None in SolIrradiance:

        # Thermal Constants (K1 = [W*m-2*um-1]; K1 = [K])
        if re.search(r"[\D]*5", self.Satellite):
            # resource: http://www.yale.edu/ceo/Documentation/Landsat_DN_to_Kelvin.pdf
            ThermalConstK1 = [0., 0., 0., 0., 0., 607.76, 0.]
            ThermalConstK2 = [0., 0., 0., 0., 0., 1260.56, 0.]
        if re.search(r"[\D]*7", self.Satellite):
            # resource: http://www.yale.edu/ceo/Documentation/Landsat_DN_to_Kelvin.pdf
            ThermalConstK1 = [0., 0., 0., 0., 0., 666.09, 666.09, 0., 0.]
            ThermalConstK2 = [0., 0., 0., 0., 0., 1282.71, 1282.71, 0., 0.]
        if re.search(r"[\D]*8", self.Satellite):  # Landsat 8
            K1_res = re.findall(r"K1_CONSTANT_BAND_[0-9]+ = ([\S]*)", mtl_, re.I)
            K2_res = re.findall(r"K2_CONSTANT_BAND_[0-9]+ = ([\S]*)", mtl_, re.I)
            if len(K1_res) == 2:
                ThermalConstK1 = [0., 0., 0., 0., 0., 0., 0., 0., 0., float(K1_res[0]), float(K1_res[1])]
                ThermalConstK2 = [0., 0., 0., 0., 0., 0., 0., 0., 0., float(K2_res[0]), float(K2_res[1])]
            else:
                self.logger.error('Unable to set thermal constants. Expected to derive 2 values for K1 and K2. '
                                  'Found %s' % len(K1_res))
        self.ThermalConstK1 = {bN: ThermalConstK1[i] for i, bN in enumerate(LBA_full_sorted)}
        self.ThermalConstK2 = {bN: ThermalConstK2[i] for i, bN in enumerate(LBA_full_sorted)}

        # reflectance coefficients (Landsat8)
        h9 = re.search(r"GROUP = RADIOMETRIC_RESCALING[\s\S]*END_GROUP = RADIOMETRIC_RESCALING", mtl_, re.I)
        if h9:
            h9_ = h9.group(0)
            h9gain_ref = re.findall(r" REFLECTANCE_MULT_BAND_[0-9]+ = ([\S]*)", h9_, re.I)
            h9gain_ref_bandNr = re.findall(r" REFLECTANCE_MULT_BAND_([0-9]+) = [\S]*", h9_, re.I)
            h9offs_ref = re.findall(r" REFLECTANCE_ADD_BAND_[0-9]+ = ([\S]*)", h9_, re.I)
            h9offs_ref_bandNr = re.findall(r" REFLECTANCE_ADD_BAND_([0-9]+) = [\S]*", h9_, re.I)
            if h9gain_ref:
                GainsRef = [None] * len(self.Gains)
                OffsetsRef = [None] * len(self.Offsets)

                for ii, ind in zip(h9gain_ref_bandNr, h9gain_ref):
                    GainsRef[LBA_full_sorted.index(ii)] = ind
                for ii, ind in zip(h9offs_ref_bandNr, h9offs_ref):
                    OffsetsRef[LBA_full_sorted.index(ii)] = ind

                self.GainsRef = {bN: GainsRef[i] for i, bN in enumerate(LBA_full_sorted)}
                self.OffsetsRef = {bN: OffsetsRef[i] for i, bN in enumerate(LBA_full_sorted)}

        self.orbitParams = get_orbit_params(self.GMS_identifier)
        self.filter_layerdependent_metadata()
        self.spec_vals = get_special_values(self.GMS_identifier)

        # mtl.close()

    def Read_RE_metaxml(self):
        """----METHOD_4------------------------------------------------------------
        read metadata from RapidEye metafile: <dataname>metadata.xml
        """

        # self.default_attr()
        if os.path.isdir(self.FolderOrArchive):
            glob_res = glob.glob(os.path.join(self.FolderOrArchive, '*/*_metadata.xml'))
            assert len(glob_res) > 0, 'No *metadata.xml file can be found in %s/*/!' % self.FolderOrArchive
            self.Metafile = glob_res[0]
            mxml_ = open(self.Metafile, "r").read()
        else:  # archive
            mxml_, self.Metafile = open_specific_file_within_archive(self.FolderOrArchive, '*/*_metadata.xml')

        # EntityID
        h1 = re.search(r"<[a-z]*:identifier>([\S]*)</[a-z]*:identifier>", mxml_, re.I)
        self.EntityID = h1.group(1) if h1 else "Not found"

        # Processing Level
        h2 = re.search(r"<[a-z]*:productType>([a-zA-Z0-9]*)</[a-z]*:productType>", mxml_, re.I)
        self.ProcLCode = h2.group(1) if h2 else "Not found"

        # Satellite
        h3 = re.search(r"<[a-z]*:serialIdentifier>([a-zA-Z0-9-]*)</[a-z]*:serialIdentifier>", mxml_, re.I)
        self.Satellite = 'RapidEye-%s' % re.search(r'[\D]*([0-9])', h3.group(1), re.I).group(1) if h3 else "Not found"

        # Sensor (Instrument shortname)
        h4 = re.search(r"<[a-z]*:Instrument>[\s]*<eop:shortName>([\S]*)</[a-z]*:shortName>", mxml_, re.I)
        self.Sensor = h4.group(1) if h4 else "Not found"

        # Acquisition Parameters: Incidence Angle, SunAzimuth, SunElevation, ViewingAngle, FieldOfView, AcqDate, AcqTime
        try:
            h5 = re.search(r'<[a-z]*:incidenceAngle uom="deg">([\S]*)'
                           r'</[a-z]*:incidenceAngle>[\s]*'
                           r'<opt:illuminationAzimuthAngle uom="deg">([\S]*)'
                           r'</opt:illuminationAzimuthAngle>[\s]*'
                           r'<opt:illuminationElevationAngle uom="deg">([\S]*)'
                           r'</opt:illuminationElevationAngle>[\s]*'
                           r'<re:azimuthAngle uom="deg">([\S]*)'
                           r'</re:azimuthAngle>[\s]*'
                           r'<re:spaceCraftViewAngle uom="deg">([\S]*)'
                           r'</re:spaceCraftViewAngle>[\s]*'
                           r'<re:acquisitionDateTime>([0-9-]*)T([0-9:]*)[\S]*'
                           r'</re:acquisitionDateTime>',
                           mxml_, re.I)
            self.IncidenceAngle = float(h5.group(1))
            self.SunAzimuth = float(h5.group(2))
            self.SunElevation = float(h5.group(3))
            # angle from true north at the image or tile center to the scan (line) direction at image center,
            # in clockwise positive degrees.
            self.additional.append(["spaceCraftAzimuthAngle:", str(round(float(h5.group(4)), 1))])
            self.ViewingAngle = float(h5.group(5))
            self.FOV = get_FieldOfView(self.GMS_identifier)
            AcqDate = h5.group(6)
            AcqTime = h5.group(7)

        except AttributeError:
            h5 = re.search(r'<hma:acrossTrackIncidenceAngle uom="deg">([\S]*)'
                           r'</hma:acrossTrackIncidenceAngle>[\s]*'
                           r'<ohr:illuminationAzimuthAngle uom="deg">([\S]*)'
                           r'</ohr:illuminationAzimuthAngle>[\s]*'
                           r'<ohr:illuminationElevationAngle uom="deg">([\S]*)'
                           r'</ohr:illuminationElevationAngle>[\s]*'
                           r'<re:azimuthAngle uom="deg">([\S]*)'
                           r'</re:azimuthAngle>[\s]*'
                           r'<re:acquisitionDateTime>([0-9-]*)'
                           r'T([0-9:]*)[\S]*'
                           r'</re:acquisitionDateTime>',
                           mxml_, re.I)  #
            self.IncidenceAngle = float(h5.group(1))
            self.SunAzimuth = float(h5.group(2))
            self.SunElevation = float(h5.group(3))
            self.additional.append(["spaceCraftAzimuthAngle:", str(round(float(h5.group(4)), 1))])
            self.ViewingAngle = 9999.99
            self.FOV = get_FieldOfView(self.GMS_identifier)
            AcqDate = h5.group(5)
            AcqTime = h5.group(6)
        # set self.AcqDateTime as well as self.AcqDate and self.AcqTime
        self.AcqDateTime = datetime.datetime.strptime(
            '%s %s%s' % (AcqDate, AcqTime, '.000000+0000'), '%Y-%m-%d %H:%M:%S.%f%z')

        # Earth sun distance
        self.EarthSunDist = self.get_EarthSunDistance(self.AcqDate)

        # Additional: Projection
        h6 = re.search(r"<re:geodeticDatum>([\S]*)"
                       r"</re:geodeticDatum>[\s]*"
                       r"<re:projection>([\S^<\s]*)"
                       r"</re:projection>",
                       mxml_, re.I)
        try:
            self.additional.append(["SpatialReference",
                                    ["geodeticDatum", h6.group(1)],
                                    ["projection", h6.group(2)]
                                    ])
        except AttributeError:  # Level1-B data has no geodaticDatum
            pass

        # Corrections applied + Quality
        h7 = re.search(r"<re:radiometricCorrectionApplied>([\w]*)"
                       r"</re:radiometricCorrectionApplied>[\s]*"
                       r"<re:radiometricCalibrationVersion>([\S]*)"
                       r"</re:radiometricCalibrationVersion>[\s]*"
                       r"<re:geoCorrectionLevel>([\S\s^<]*)"
                       r"</re:geoCorrectionLevel>[\s]*"
                       r"<re:elevationCorrectionApplied>([\S]*)"
                       r"</re:elevationCorrectionApplied>[\s]*"
                       r"<re:atmosphericCorrectionApplied>([\w]*)"
                       r"</re:atmosphericCorrectionApplied>[\s]*"
                       r"<re:productAccuracy>([\S\s^<]*)"
                       r"</re:productAccuracy>", mxml_, re.I)
        # fuer IRIS ihre Daten
        if h7 is None:
            h7 = re.search(r"<re:radiometricCorrectionApplied>([\w]*)"
                           r"</re:radiometricCorrectionApplied>[\s]*"
                           r"<re:geoCorrectionLevel>([\S\s^<]*)"
                           r"</re:geoCorrectionLevel>[\s]*"
                           r"<re:elevationCorrectionApplied>([\S]*)"
                           r"</re:elevationCorrectionApplied>[\s]*"
                           r"<re:atmosphericCorrectionApplied>([\w]*)"
                           r"</re:atmosphericCorrectionApplied>",
                           mxml_, re.I)
            self.additional.append(
                ["Corrections",
                 ["radiometricCorrectionApplied", h7.group(1)],
                 ["geoCorrectionLevel", h7.group(2)],
                 ["elevationCorrectionApplied", h7.group(3)],
                 ["atmosphericCorrectionApplied", h7.group(4)]
                 ])
        else:
            self.additional.append(
                ["Corrections",
                 ["radiometricCorrectionApplied", h7.group(1)],
                 ["radiometricCalibrationVersion", h7.group(2)],
                 ["geoCorrectionLevel", h7.group(3)],
                 ["elevationCorrectionApplied", h7.group(4)],
                 ["atmosphericCorrectionApplied", h7.group(5)]
                 ])
            self.Quality.append(["geomProductAccuracy[m]:", str(
                round(float(h7.group(6)), 1))])  # Estimated product horizontal CE90 uncertainty [m]

        # additional. missing lines, suspectlines, binning, shifting, masking
        h81 = re.findall(r"<re:percentMissingLines>([^<]*)</re:percentMissingLines>", mxml_, re.I)
        h82 = re.findall(r"<re:percentSuspectLines>([^<]*)</re:percentSuspectLines>", mxml_, re.I)
        h83 = re.findall(r"<re:binning>([^<]*)</re:binning>", mxml_, re.I)
        h84 = re.findall(r"<re:shifting>([^<]*)</re:shifting>", mxml_, re.I)
        h85 = re.findall(r"<re:masking>([^<]*)</re:masking>", mxml_, re.I)

        self.Quality.append(
            ["MissingLines[%]perBand", h81])  # Percentage of missing lines in the source data of this band
        # Percentage of suspect lines (lines that contained downlink errors) in the source data for the band
        self.Quality.append(["SuspectLines[%]perBand", h82])
        self.additional.append(
            ["binning_perBand", h83])  # Indicates the binning used (across track x along track) [1x1,2x2,3x3,1x2,2x1]
        self.additional.append(
            ["shifting_perBand", h84])  # Indicates the sensor applied right shifting [none, 1bit, 2bits, 3bits, 4bits]
        self.additional.append(["masking_perBand", h85])  # Indicates the sensor applied masking [111, 110, 100, 000]

        # Units
        self.ScaleFactor = 1
        self.PhysUnit = "DN"

        # Coordinate Reference System
        re_CS_EPSG = re.search(
            r'<re:ProductInformation>[\s\S]*'
            r'<re:epsgCode>([0-9]*)</re:epsgCode>[\s\S]*'
            r'</re:ProductInformation>',
            mxml_, re.I)
        re_CS_TYPE = re.search(
            r'<re:ProductInformation>[\s\S]*'
            r'<re:projection>([\s\S]*)</re:projection>[\s\S]*'
            r'</re:ProductInformation>',
            mxml_, re.I)
        re_CS_DATUM = re.search(
            r'<re:ProductInformation>[\s\S]*'
            r'<re:geodeticDatum>([\w+\s]*)</re:geodeticDatum>[\s\S]*'
            r'</re:ProductInformation>',
            mxml_, re.I)
        re_CS_UTM_ZONE = re.search(
            r'<re:ProductInformation>[\s\S]*'
            r'<re:projectionZone>([0-9]*)</re:projectionZone>[\s\S]*'
            r'</re:ProductInformation>',
            mxml_, re.I)
        self.CS_EPSG = int(re_CS_EPSG.group(1)) if re_CS_EPSG else self.CS_EPSG
        self.CS_TYPE = 'LonLat' if re_CS_TYPE and not re.search(r'UTM', re_CS_TYPE.group(1)) else 'UTM' \
            if re_CS_TYPE and re.search(r'UTM', re_CS_TYPE.group(1)) else self.CS_TYPE
        self.CS_DATUM = 'WGS84' if re_CS_DATUM is not None and re_CS_DATUM.group(1) == 'WGS_1984' else self.CS_DATUM
        self.CS_UTM_ZONE = int(re_CS_UTM_ZONE.group(1)) if re_CS_UTM_ZONE is not None else self.CS_UTM_ZONE

        # Corner Coordinates ## Lon/Lat for all given image corners UL,UR,LL,LR (tuples)
        h10_UL = re.findall(
            r'<re:topLeft>'
            r'<re:latitude>(.*)</re:latitude>'
            r'<re:longitude>(.*)</re:longitude>'
            r'</re:topLeft>',
            mxml_, re.I)
        h10_UR = re.findall(
            r'<re:topRight>'
            r'<re:latitude>(.*)</re:latitude>'
            r'<re:longitude>(.*)</re:longitude>'
            r'</re:topRight>',
            mxml_, re.I)
        h10_LL = re.findall(
            r'<re:bottomLeft>'
            r'<re:latitude>(.*)</re:latitude>'
            r'<re:longitude>(.*)</re:longitude>'
            r'</re:bottomLeft>',
            mxml_, re.I)
        h10_LR = re.findall(
            r'<re:bottomRight>'
            r'<re:latitude>(.*)</re:latitude>'
            r'<re:longitude>(.*)</re:longitude>'
            r'</re:bottomRight>',
            mxml_, re.I)
        if h10_UL:  # Set Corner Tie Point Coordinates (order = UL,UR,LL,LR)
            self.CornerTieP_LonLat.append(tuple([float(h10_UL[0][1]), float(h10_UL[0][0])]))
            self.CornerTieP_LonLat.append(tuple([float(h10_UR[0][1]), float(h10_UR[0][0])]))
            self.CornerTieP_LonLat.append(tuple([float(h10_LL[0][1]), float(h10_LL[0][0])]))
            self.CornerTieP_LonLat.append(tuple([float(h10_LR[0][1]), float(h10_LR[0][0])]))

        ##########################
        # band specific metadata #
        ##########################

        LBA_full_sorted = natsorted(self.LayerBandsAssignment_full)

        # Gains + Offsets
        h9 = re.findall(r"<re:radiometricScaleFactor>([^<]*)</re:radiometricScaleFactor>",
                        mxml_, re.I)
        self.Gains = dict(zip(LBA_full_sorted, [float(gain) for gain in h9]))
        self.Offsets = dict(zip(LBA_full_sorted, [0, 0, 0, 0, 0]))

        # Solar irradiance, central wavelengths , full width half maximum per band
        self.wvlUnit = 'Nanometers'
        # derive number of bands from number of given gains/offsets in header file or from raster data
        # noinspection PyBroadException
        try:
            self.nBands = (np.mean([len(self.Gains), len(self.Offsets)])
                           if np.std([len(self.Gains), len(self.Offsets)]) == 0 and len(self.Gains) != 0 else
                           GEOP.GEOPROCESSING(self.Dataname, self.logger).bands)
        except Exception:
            self.logger.warning('Unable to get number of bands for the dataset %s Provider values are used for '
                                'solar irradiation, CWL and FWHM!.' % self.Dataname)
        self.LayerBandsAssignment = get_LayerBandsAssignment(self.GMS_identifier, self.nBands)

        # Exact values calculated based in SRFs
        self.SolIrradiance, self.CWL, self.FWHM = self.calc_solar_irradiance_CWL_FWHM_per_band()
        # Provider values
        if not self.SolIrradiance:
            # Preconfigured Irradiation values
            self.SolIrradiance = dict(zip(LBA_full_sorted, [1997.8, 1863.5, 1560.4, 1395.0, 1124.4]))
            # Preconfigured CWLs
            self.CWL = dict(zip(LBA_full_sorted, [475., 555., 657., 710., 805.]))

        self.orbitParams = get_orbit_params(self.GMS_identifier)
        self.filter_layerdependent_metadata()
        self.spec_vals = get_special_values(self.GMS_identifier)

    def Read_ASTER_hdffile(self, subsystem):
        """#----METHOD_5------------------------------------------------------------
        read metadata from ASTER hdf
        input:
            hdffile:
            subsystem:
        output:
        :param subsystem:
        """

        #    self.default_attr()
        dat_ = open(self.FolderOrArchive, "r").read() if sys.version_info[0] < 3 else \
            open(self.FolderOrArchive, "rb").read().decode('latin-1')

        # Split meta from raster data
        meta = re.search(r"GROUP[\s]*=[\s]"
                         r"ASTERGENERICMETADATA[\s\S]*?"
                         r"END_GROUP[\s]*=[\s]"
                         r"INVENTORYMETADATA",
                         dat_, re.I)
        meta_ = meta.group(0) if meta else ''
        genericmeta = re.search(r"GROUP[\s]*=[\s]"
                                r"ASTERGENERICMETADATA[\s\S]*?"
                                r"END_GROUP[\s]*=[\s]"
                                r"ASTERGENERICMETADATA",
                                meta_, re.I)
        inventorymeta = re.search(r"GROUP[\s]*=[\s]"
                                  r"INVENTORYMETADATA[\s\S]*?"
                                  r"END_GROUP[\s]*=[\s]"
                                  r"INVENTORYMETADATA",
                                  meta_, re.I)
        gcsgenericmeta = re.search(r"GROUP[\s]*=[\s]"
                                   r"GDSGENERICMETADATA[\s\S]*?"
                                   r"END_GROUP[\s]*=[\s]"
                                   r"GDSGENERICMETADATA",
                                   meta_, re.I)
        vnirmeta = re.search(r"GROUP[\s]*=[\s]"
                             r"PRODUCTSPECIFICMETADATAVNIR[\s\S]*?"
                             r"END_GROUP[\s]*=[\s]"
                             r"PRODUCTSPECIFICMETADATAVNIR",
                             meta_, re.I)
        swirmeta = re.search(r"GROUP[\s]*=[\s]"
                             r"PRODUCTSPECIFICMETADATASWIR[\s\S]*?"
                             r"END_GROUP[\s]*=[\s]"
                             r"PRODUCTSPECIFICMETADATASWIR",
                             meta_, re.I)
        tirmeta = re.search(r"GROUP[\s]*=[\s]"
                            r"PRODUCTSPECIFICMETADATATIR[\s\S]*?"
                            r"END_GROUP[\s]*=[\s]"
                            r"PRODUCTSPECIFICMETADATATIR",
                            meta_, re.I)
        genericmeta_ = genericmeta.group(0) if genericmeta else ''
        inventorymeta_ = inventorymeta.group(0) if inventorymeta else ''
        gcsgenericmeta_ = gcsgenericmeta.group(0) if gcsgenericmeta else ''
        vnirmeta_ = vnirmeta.group(0) if vnirmeta else ''
        swirmeta_ = swirmeta.group(0) if swirmeta else ''
        tirmeta_ = tirmeta.group(0) if tirmeta else ''
        h_ = '\n\n\n'.join([genericmeta_, inventorymeta_, gcsgenericmeta_, vnirmeta_, swirmeta_, tirmeta_])

        # with open("./testing/out/ASTER_HDFmeta__h_.txt", "w") as allMetaOut:
        #     allMetaOut.write(h_)

        # EntityID
        h1 = re.search(r"OBJECT[\s]*=[\s]*"
                       r"IDOFASTERGDSDATAGRANULE[\s\S]*"
                       r"END_OBJECT[\s]*=[\s]*"
                       r"IDOFASTERGDSDATAGRANULE",
                       h_, re.I)
        h11 = re.search(r'VALUE[\s]*=[\s]*"([\s\S]*)"', h1.group(0), re.I)
        self.EntityID = [h11.group(1), re.search(r"\"(ASTL1A[\s0-9]*)\"", h_).group(1)]

        # Viewing Angle
        h2 = re.search(r"GROUP[\s]*=[\s]*"
                       r"POINTINGANGLES[\s\S]*"
                       r"END_GROUP[\s]*=[\s]*"
                       r"POINTINGANGLES",
                       h_, re.I)
        h21 = re.findall(r"VALUE[\s]*=[\s]*([-]*[0-9.0-9]+)", h2.group(0), re.I)
        self.additional.append(["ViewingAngles", "VNIR", float(h21[0]), "SWIR", float(h21[1]), "TIR", float(h21[2])])
        if max(float(h21[0]), float(h21[1]), float(h21[2])) - min(float(h21[0]), float(h21[1]), float(h21[2])) < 1:
            self.ViewingAngle = float(h21[0])
        else:
            self.ViewingAngle = -99.0

        # additional GainMode
        h3 = re.search(r"GROUP[\s]*=[\s]*"
                       r"GAININFORMATION[\s\S]*"
                       r"END_GROUP[\s]*=[\s]*"
                       r"GAININFORMATION",
                       genericmeta_, re.I)
        h31 = re.findall(r'VALUE[\s]*=[\s]*[\S]?\"[0-9A-Z]*\", \"([A-Z]*)\"', h3.group(0), re.I)
        gains = {'HGH': [170.8, 179.0, 106.8, 27.5, 8.8, 7.9, 7.55, 5.27, 4.02, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'],
                 'NOR': [427.0, 358.0, 218.0, 55.0, 17.6, 15.8, 15.1, 10.55, 8.04, 28.17, 27.75, 26.97, 23.30, 21.38],
                 'LOW': [569.0, 477.0, 290.0, 73.3, 23.4, 21.0, 20.1, 14.06, 10.72, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'],
                 'LO1': [569.0, 477.0, 290.0, 73.3, 23.4, 21.0, 20.1, 14.06, 10.72, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'],
                 'LO2': ['N/A', 'N/A', 'N/A', 73.3, 103.5, 98.7, 83.8, 62.0, 67.0, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'],
                 'OFF': "OFF"}
        self.additional.append([["GainMode:"], ["Max_radiance:"]])
        for x, i in enumerate(h31[:15]):
            self.additional[-1][-2].append(i)
            self.additional[-1][-1].append(gains[i][x])

        # Units
        self.ScaleFactor = 1
        self.PhysUnit = "DN"

        # Satellite
        self.Satellite = 'Terra'

        # Sensor
        h10 = re.search(r"OBJECT[\s]*=[\s]*"
                        r"INSTRUMENTSHORTNAME[\s\S]*"
                        r"END_OBJECT[\s]*=[\s]*"
                        r"INSTRUMENTSHORTNAME", h_, re.I)
        self.Sensor = re.search(r"VALUE[\s]*=[\s]*[\"]([A-Za-z]*)\"", h10.group(0), re.I).group(1)

        # Subsystem
        h5 = re.search(r"GROUP[\s]*=[\s]*"
                       r"OBSERVATIONMODE[\s\S]*"
                       r"END_GROUP[\s]*=[\s]*"
                       r"OBSERVATIONMODE", h_, re.I)
        avail_subsystems = re.findall(r'VALUE[\s]*=[\s]*[(]\"([a-zA-Z0-9]*)\", \"([ONF]*)\"', h5.group(0), re.I)
        if subsystem not in ['VNIR1', 'VNIR2', 'SWIR', 'TIR']:
            raise ValueError('Unexpected subsystem >%s<. Unable to specify the correct ASTER subsystem to be '
                             'processed.' % subsystem)
        else:
            if subsystem == 'VNIR1' and avail_subsystems[0][1] == 'ON':
                self.nBands = 3
            if subsystem == 'VNIR2' and avail_subsystems[1][1] == 'ON':
                self.nBands = 1
            if subsystem == 'SWIR' and avail_subsystems[2][1] == 'ON':
                self.nBands = 6
            if subsystem == 'TIR' and avail_subsystems[3][1] == 'ON':
                self.nBands = 5
        self.Subsystem = subsystem

        # Field of view (requires Satellite, Sensor, Subsystem)
        self.FOV = get_FieldOfView(self.GMS_identifier)

        # Ground resolution
        re_res_GSD = re.findall(r'OBJECT[\s]*=[\s]*'
                                r'SPATIALRESOLUTION[\s\S]*'
                                r'VALUE[\s]*=[\s]*[\S]{1}([1-9][0-9]), ([1-9][0-9]), ([1-9][0-9])[\s\S]*'
                                r'END_OBJECT[\s]*=[\s]*'
                                r'SPATIALRESOLUTION', h_, re.I)
        idx_subsystem = \
            0 if subsystem[:4] == 'VNIR' else \
            1 if subsystem[:4] == 'SWIR' else \
            2 if subsystem[:4] == 'TIR' else None
        self.gResolution = float(re_res_GSD[0][idx_subsystem]) \
            if re_res_GSD and idx_subsystem is not None else self.gResolution

        # Flight direction
        h6 = re.search(r"OBJECT[\s]*=[\s]*"
                       r"FLYINGDIRECTION[\s\S]*\"([ASDE]*?)\"",
                       h_, re.I)
        Fdir = {'AS': "Ascending", 'DE': "Descending"}
        self.additional.append(["Flight Direction", Fdir[h6.group(1)]])

        # SunAzimuth SunElevation
        h7 = re.search(r"OBJECT[\s]*=[\s]*"
                       r"SOLARDIRECTION[\s\S]*"
                       r"END_OBJECT[\s]*=[\s]*"
                       r"SOLARDIRECTION",
                       h_, re.I)
        h71 = re.search(r"VALUE[\s]*=[\s]*[\S]{1}([0-9.]*), ([0-9.]*)", h7.group(0), re.I)
        self.SunAzimuth = float(h71.group(1))
        self.SunElevation = float(h71.group(2))

        # data Quality
        h8 = re.findall(r"GROUP[\s]*=[\s]*"
                        r"DATAQUALITY[1-9][0-4BN]?[^.]*"
                        r"END_GROUP[\s]*=[\s]*"
                        r"DATAQUALITY[1-9][0-4BN]?",
                        h_, re.I)
        h81 = re.findall(r'VALUE[\s]*=[\s]*([^\n]*)', "\n".join(h8), re.I)
        self.Quality.append(["NoOfBadPixel:"])
        for i in h81:
            self.Quality[-1].append(i)

        # ProdLevel
        h9 = re.search(r"OBJECT[\s]*=[\s]*"
                       r"SHORTNAME[\s\S]*"
                       r"END_OBJECT[\s]*=[\s]*"
                       r"SHORTNAME", h_, re.I)
        self.ProcLCode = re.search(r"VALUE[\s]*=[\s]*[\"]([0-9A-Za-z]*)\"", h9.group(0), re.I).group(1)

        # AcqTime
        h11 = re.search(r"OBJECT[\s]*=[\s]*"
                        r"TIMEOFDAY[\s\S]*"
                        r"END_OBJECT[\s]*=[\s]*"
                        r"TIMEOFDAY", h_, re.I)
        h111 = re.search(r"VALUE[\s]*=[\s]*[\"]([\d][\d][\d][\d][\d][\d])[\S]*\"", h11.group(0), re.I)
        if type(h111).__name__ != 'NoneType':
            AcqTime = "%s:%s:%s" % (h111.group(1)[:2], h111.group(1)[2:4], h111.group(1)[4:6])
        else:
            h112 = re.search(r"VALUE[\s]*=[\s]*[\"]([\d:]*)[\S]*\"", h11.group(0), re.I)
            AcqTime = h112.group(1)

        # AcqDate
        h12 = re.search(r"OBJECT[\s]*=[\s]*"
                        r"CALENDARDATE[\s\S]*"
                        r"END_OBJECT[\s]*=[\s]*"
                        r"CALENDARDATE", h_, re.I)
        h121 = re.search(r"VALUE[\s]*=[\s]*[\"]([\d]*)\"", h12.group(0), re.I)
        if type(h121).__name__ != 'NoneType':
            AcqDate = "%s-%s-%s" % (h121.group(1)[:4], h121.group(1)[4:6], h121.group(1)[6:8])
        else:
            h121 = re.search(r"VALUE[\s]*=[\s]*[\"]([\d-]*)\"", h12.group(0), re.I)
            AcqDate = h121.group(1)

        # set self.AcqDateTime as well as self.AcqDate and self.AcqTime
        self.AcqDateTime = datetime.datetime.strptime(
            '%s %s%s' % (AcqDate, AcqTime, '.000000+0000'), '%Y-%m-%d %H:%M:%S.%f%z')

        # Earth sun distance
        self.EarthSunDist = self.get_EarthSunDistance(self.AcqDate)

        # data Quality
        h13 = re.search(r"GROUP[\s]*=[\s]*"
                        r"QASTATS[\s\S]*"
                        r"END_GROUP[\s]*=[\s]*"
                        r"QASTATS",
                        h_, re.I)
        h131 = re.findall(r'VALUE[\s]*=[\s]*([0-9.0-9]*)', h13.group(0), re.I)
        self.Quality.append(["PercMissingData:", h131[0]])  # The percentage of missing data of the scene [%]
        self.Quality.append(["PercOutOfBoundsData:", h131[1]])  # The percentage of out of bounds data of the scene [%]
        self.Quality.append(["PercInterpolatedData:", h131[2]])  # The percentage of interpolated data of the scene [%]

        # Coordinate Reference System (L1B+)
        topgroupname = 'PRODUCTSPECIFICMETADATA' + subsystem[:4]
        # read only the information from first band in current ASTER subsystem
        # (the others should have the same parameters)
        re_res_procParm = re.search(r'GROUP[\s]*=[\s]*%s[\s\S]*'
                                    r'GROUP[\s]*=[\s]*(PROCESSINGPARAMETERS%s[\s\S]*'
                                    r'END_GROUP[\s]*=[\s]*PROCESSINGPARAMETERS%s)[\s\S]*'
                                    r'END_GROUP[\s]*=[\s]*%s'
                                    % (topgroupname, self.LayerBandsAssignment[0],
                                       self.LayerBandsAssignment[0], topgroupname),
                                    h_, re.I)
        if type(re_res_procParm).__name__ != 'NoneType':
            re_res_procParm = re_res_procParm.group(1)
            re_CS_TYPE = re.search(r'OBJECT[\s]*=[\s]*'
                                   r'MPMETHOD[\s\S]*'
                                   r'VALUE[\s]*=[\s]*"([\s\S]*)"[\s\S]*'
                                   r'END_OBJECT[\s]*=[\s]*'
                                   r'MPMETHOD',
                                   re_res_procParm, re.I)
            re_CS_UTM_ZONE = re.search(r'OBJECT[\s]*=[\s]*'
                                       r'UTMZONECODE[\s\S]*'
                                       r'VALUE[\s]*=[\s]*([0-9][0-9]?)[\s\S]*'
                                       r'END_OBJECT[\s]*=[\s]*'
                                       r'UTMZONECODE',
                                       re_res_procParm, re.I)
            self.CS_TYPE = 'LonLat' if re_CS_TYPE and not re.search(r'UTM', re_CS_TYPE.group(1)) else 'UTM' \
                if re_CS_TYPE and re.search(r'UTM', re_CS_TYPE.group(1)) else self.CS_TYPE
            self.CS_DATUM = 'WGS84' if self.CS_TYPE == 'UTM' else self.CS_DATUM
            self.CS_UTM_ZONE = int(re_CS_UTM_ZONE.group(1)) if re_CS_UTM_ZONE else self.CS_UTM_ZONE

        # Corner Coordinates ## Lon/Lat for all given image corners UL,UR,LL,LR (tuples)
        re_res_sceneInfo = re.search(r'GROUP[\s]*=[\s]*'
                                     r'SCENEINFORMATION[\s\S]*'
                                     r'END_GROUP[\s]*=[\s]*'
                                     r'SCENEINFORMATION', h_,
                                     re.I).group(0)
        re_res_UL = re.findall(r'OBJECT[\s]*=[\s]*'
                               r'UPPERLEFT[\s\S]*'
                               r'VALUE[\s]*=[\s]*[\S]{1}([0-9.]*), ([0-9.]*)[\s\S]*'
                               r'END_OBJECT[\s]*=[\s]*'
                               r'UPPERLEFT',
                               re_res_sceneInfo, re.I)
        re_res_UR = re.findall(r'OBJECT[\s]*=[\s]*'
                               r'UPPERRIGHT[\s\S]*'
                               r'VALUE[\s]*=[\s]*[\S]{1}([0-9.]*), ([0-9.]*)[\s\S]*'
                               r'END_OBJECT[\s]*=[\s]*'
                               r'UPPERRIGHT',
                               re_res_sceneInfo, re.I)
        re_res_LL = re.findall(r'OBJECT[\s]*=[\s]*'
                               r'LOWERLEFT[\s\S]*'
                               r'VALUE[\s]*=[\s]*[\S]{1}([0-9.]*), ([0-9.]*)[\s\S]*'
                               r'END_OBJECT[\s]*=[\s]*'
                               r'LOWERLEFT',
                               re_res_sceneInfo, re.I)
        re_res_LR = re.findall(r'OBJECT[\s]*=[\s]*'
                               r'LOWERRIGHT[\s\S]*'
                               r'VALUE[\s]*=[\s]*[\S]{1}([0-9.]*), ([0-9.]*)[\s\S]*'
                               r'END_OBJECT[\s]*=[\s]*'
                               r'LOWERRIGHT',
                               re_res_sceneInfo, re.I)
        if re_res_UL:  # Set Corner Tie Point Coordinates (order = UL,UR,LL,LR)
            self.CornerTieP_LonLat.append(tuple([float(re_res_UL[0][1]), float(re_res_UL[0][0])]))
            self.CornerTieP_LonLat.append(tuple([float(re_res_UR[0][1]), float(re_res_UR[0][0])]))
            self.CornerTieP_LonLat.append(tuple([float(re_res_LL[0][1]), float(re_res_LL[0][0])]))
            self.CornerTieP_LonLat.append(tuple([float(re_res_LR[0][1]), float(re_res_LR[0][0])]))

        ##########################
        # band specific metadata #
        ##########################

        LBA_full_sorted = natsorted(self.LayerBandsAssignment_full)

        # Gains/Offsets
        h4 = re.findall(r"GROUP[\s]*=[\s]*"
                        r"UNITCONVERSIONCOEFF[1-9][0-4BN]?[^(]*"
                        r"END_GROUP[\s]*=[\s]*"
                        r"UNITCONVERSIONCOEFF[1-9][0-4BN]?",
                        h_, re.I)
        h41 = re.findall(r'VALUE[\s]*=[\s]*([0-9.0-9]+)', "\n".join(h4), re.I)
        h42 = re.findall(r'VALUE[\s]*=[\s]*([-]+[0-9.0-9]+)', "\n".join(h4), re.I)
        self.Gains = dict(zip(LBA_full_sorted, [float(i) for i in h41]))
        self.Offsets = dict(zip(LBA_full_sorted, [float(i) for i in h42]))

        # Solar irradiance, central wavelengths , full width half maximum per band
        self.wvlUnit = 'Nanometers'
        self.LayerBandsAssignment = get_LayerBandsAssignment(self.GMS_identifier, self.nBands)

        # Exact values calculated based in SRFs
        self.SolIrradiance, self.CWL, self.FWHM = self.calc_solar_irradiance_CWL_FWHM_per_band()
        # Provider values
        if not self.SolIrradiance:
            # Preconfigured Irradiation values
            self.SolIrradiance = dict(zip(LBA_full_sorted, [1845.99, 1555.74, 1119.47] + [None] * 12))
            # Preconfigured CWLs
            self.CWL = dict(zip(LBA_full_sorted, [556., 659., 807., 804., 1656., 2167., 2208., 2266., 2336., 2400.,
                                                  8291., 8634., 9075., 10657., 11318]))

            # Thermal Constants (K1 = [W*m-2*um-1]; K1 = [K])
        # Preconfigured values; resource:  http://www.pancroma.com/ASTER%20Surface%20Temperature%20Analysis.html
        self.ThermalConstK1 = dict(zip(LBA_full_sorted,
                                       [0.] * 10 + [3040.136402, 2482.375199, 1935.060183, 866.468575, 641.326517]))
        self.ThermalConstK2 = dict(zip(LBA_full_sorted,
                                       [0.] * 10 + [1735.337945, 1666.398761, 1585.420044, 1350.069147, 1271.221673]))

        self.orbitParams = get_orbit_params(self.GMS_identifier)
        self.filter_layerdependent_metadata()
        self.spec_vals = get_special_values(self.GMS_identifier)

    def Read_ALOS_summary(self):
        """----METHOD_6------------------------------------------------------------
        read metadata from ALOS summary.txt
        """

        # self.default_attr()
        if os.path.isdir(self.FolderOrArchive):
            glob_res = glob.glob(os.path.join(self.FolderOrArchive, '*/*data*/summary.txt'))
            assert len(glob_res) > 0, 'No summary.txt file can be found in %s/*/*data*/!' % self.FolderOrArchive
            self.Metafile = glob_res[0]
            sum_ = open(self.Metafile, "r").read()
        else:  # archive
            sum_, self.Metafile = open_specific_file_within_archive(self.FolderOrArchive, '*/*data*/summary.txt')

        # EntityID
        h1 = re.search(r'Scs_SceneID="([a-zA-Z0-9]*)"', sum_, re.I)
        self.EntityID = h1.group(1)

        # Satellite, Sensor, ProcLevel,
        h5 = re.search(r'Lbi_Satellite="([\S]*)"[\s]*'
                       r'Lbi_Sensor="([\S-]*)"[\s]*'
                       r'Lbi_ProcessLevel="([\S-]*)"',
                       sum_, re.I)
        self.Satellite = h5.group(1)
        self.Sensor = h5.group(2)
        self.ProcLCode = h5.group(3)

        # Ground resolution
        re_res_GSD = re.search(r'Pds_PixelSpacing="([\d]*)"', sum_, re.I)
        self.gResolution = float(re_res_GSD.group(1)) if re_res_GSD else self.gResolution

        # Additional map info + resampling
        try:  # no mapinfo or resampling for Level1A
            hx = re.search(r'Ps_(ResamplingMethod="[\S]*")[\s]*'
                           r'Pds_(UTM_ZoneNo="[\S]*")[\s]*'
                           r'Pds_(MapDirection="[\S]*")[\s]*'
                           r'Pds_(PixelSpacing="[\d]*")',
                           sum_, re.I)
            self.additional.append(["Map_Info:  " + ', '.join(hx.groups())])
        except AttributeError:
            pass

        # SunElevation, SunAzimuth, ViewingAngle =(Img_Pointing_Angle),
        # IncidenceAngle =(Img_SceneCenterAngle), Field of View
        h2 = re.search(r'Img_SunAngleElevation="([\d.]*)"[\s]*'
                       r'Img_SunAngleAzimuth="([\d.]*)"[\s]*'
                       r'Img_PointingAngle="([\d.]*)"[\s]*'
                       r'Img_SceneCenterAngle="([\S]*)"',
                       sum_, re.I)
        self.SunElevation = float(h2.group(1))
        self.SunAzimuth = float(h2.group(2))
        self.ViewingAngle = float(h2.group(3))
        incAngle = h2.group(4)
        if incAngle.lower().startswith("l"):  # L means incidence angle to the left. Set to negativ values
            self.IncidenceAngle = float("-" + incAngle[1:])
        elif incAngle.lower().startswith("r"):  # R means incidence angle to the right. Set to positiv values
            self.IncidenceAngle = float(incAngle[1:])
        else:  # Sign ("L" or "R") will not be added in case of zero.
            self.IncidenceAngle = float(incAngle)
        self.FOV = get_FieldOfView(self.GMS_identifier)

        self.ScaleFactor = 1
        self.PhysUnit = "DN"

        # Additional: Exposure coefficients, Saturation coefficients of each band
        h4 = re.search(r'Img_ExposureOfBand1="([\d.-]*)"[\s]*'
                       r'Img_ExposureOfBand2="([\d.-]*)"[\s]*'
                       r'Img_ExposureOfBand3="([\d.-]*)"[\s]*'
                       r'Img_ExposureOfBand4="([\d.-]*)"[\s]*'
                       r'Img_SaturationLevelOfBand1="([\d.-]*)"[\s]*'
                       r'Img_SaturationLevelOfBand2="([\d.-]*)"[\s]*'
                       r'Img_SaturationLevelOfBand3="([\d.-]*)"[\s]*'
                       r'Img_SaturationLevelOfBand4="([\d.-]*)"',
                       sum_, re.I)

        self.additional.append(["Exposure Coeffients: B1:'%s',B2:'%s',B3:'%s',B4:'%s'"
                                % (h4.group(1), h4.group(2), h4.group(3), h4.group(4))])
        self.additional.append(["Saturation coeffients: B1:'%s',B2:'%s',B3:'%s',B4:'%s'"
                                % (h4.group(5), h4.group(6), h4.group(7), h4.group(8))])

        # AcqDate + AcqTime
        h6 = re.search(r'Lbi_ObservationDate="([\d]*)"', sum_, re.I)
        AcqDate = "%s-%s-%s" % (h6.group(1)[:4], h6.group(1)[4:6], h6.group(1)[6:8])
        re_AcqTime = re.search(r'Img_SceneCenterDateTime="[0-9]* ([0-9][0-9]:[0-9][0-9]:.*)"', sum_, re.I)
        AcqTime_dec = re_AcqTime.group(1) if re_AcqTime else self.AcqTime
        AcqTime = AcqTime_dec.split('.')[0]

        # set self.AcqDateTime as well as self.AcqDate and self.AcqTime
        if AcqTime_dec:
            self.AcqDateTime = datetime.datetime.strptime(
                '%s %s%s' % (AcqDate, AcqTime_dec, '+0000'), '%Y-%m-%d %H:%M:%S.%f%z')
        else:
            self.AcqDateTime = datetime.datetime.strptime('%s%s' % (AcqDate, '+0000'), '%Y-%m-%d%z')
            self.AcqTime = AcqTime

        # Earth sun distance
        self.EarthSunDist = self.get_EarthSunDistance(self.AcqDate)

        # Quality (clouds)
        # cloudsperc = {'0': "0 to 2%", '1': "3 to 10%", '1': "11 to 20%", '1': "21 to 30%", '1': "31 to 40%",
        #               '1': "41 to 50%",
        #               '1': "51 to 60%", '1': "61 to 70%", '1': "71 to 80%", '1': "81 to 90%", '1': "91 to 100%",
        #               '99': "No assessment"}  FIXME F601 dictionary key '1' repeated with different values
        # h7 = re.search(r'Img_CloudQuantityOfAllImage="([\d]*)"', sum_, re.I)
        # self.Quality.append(["CloudCoverage: " + cloudsperc[h7.group(1)]])

        # Corner Coordinates ## Lon/Lat for all given image corners UL,UR,LL,LR (tuples)
        h10_UL = re.findall(r'Img_[\s\S]*SceneLeftTopLatitude="(.*)"[\s\S]'
                            r'Img_[\s\S]*SceneLeftTopLongitude="(.*)"',
                            sum_, re.I)
        h10_UR = re.findall(r'Img_[\s\S]*SceneRightTopLatitude="(.*)"[\s\S]'
                            r'Img_[\s\S]*SceneRightTopLongitude="(.*)"',
                            sum_, re.I)
        h10_LL = re.findall(r'Img_[\s\S]*SceneLeftBottomLatitude="(.*)"[\s\S]'
                            r'Img_[\s\S]*SceneLeftBottomLongitude="(.*)"',
                            sum_, re.I)
        h10_LR = re.findall(
            r'Img_[\s\S]*SceneRightBottomLatitude="(.*)"[\s\S]'
            r'Img_[\s\S]*SceneRightBottomLongitude="(.*)"',
            sum_, re.I)
        if h10_UL:  # Set Corner Tie Point Coordinates (order = UL,UR,LL,LR)
            self.CornerTieP_LonLat.append(tuple([float(h10_UL[0][1]), float(h10_UL[0][0])]))
            self.CornerTieP_LonLat.append(tuple([float(h10_UR[0][1]), float(h10_UR[0][0])]))
            self.CornerTieP_LonLat.append(tuple([float(h10_LL[0][1]), float(h10_LL[0][0])]))
            self.CornerTieP_LonLat.append(tuple([float(h10_LR[0][1]), float(h10_LR[0][0])]))

        # Coordinate Reference System
        re_res_CS_UTM_ZONE = re.search(r'Pds_UTM_ZoneNo="([0-9][0-9]?)"', sum_, re.I)
        self.CS_UTM_ZONE = int(re_res_CS_UTM_ZONE.group(1)) if re_res_CS_UTM_ZONE else self.CS_UTM_ZONE
        if self.CS_UTM_ZONE != -99.:
            self.CS_TYPE = 'UTM'
            self.CS_EPSG = self.CS_EPSG if self.CornerTieP_LonLat == [] else int('326' + str(self.CS_UTM_ZONE)) \
                if self.CornerTieP_LonLat[0][1] > 0.0 else int('327' + str(self.CS_UTM_ZONE))
            self.CS_DATUM = 'WGS84'
        else:
            self.CS_TYPE = 'LonLat' if self.CornerTieP_LonLat != [] and -180. <= self.CornerTieP_LonLat[0][0] <= 180. \
                                       and -90. <= self.CornerTieP_LonLat[0][1] <= 90. else self.CS_TYPE
            self.CS_EPSG = 4326 if self.CS_TYPE == 'LonLat' else self.CS_TYPE
            self.CS_DATUM = 'WGS84' if self.CS_TYPE == 'LonLat' else self.CS_DATUM

        ##########################
        # band specific metadata #
        ##########################

        LBA_full_sorted = natsorted(self.LayerBandsAssignment_full)

        # GainMode with corresponding coefficients + Offsets
        gains_AVNIR = {'1': ['N/A', 'N/A', 'N/A', 'N/A'], '2': [0.5880, 0.5730, 0.5020, 0.5570],
                       '3': [0.9410, 0.9140, 1.2040, 0.835], '4': [1.412, 1.373, 'N/A', 0.8350]}
        # gains_PRISM = {'1': ['N/A', 'N/A', 'N/A', 'N/A'], '2': [0.501, 'N/A', 'N/A', 'N/A'],
        #                '3': ['N/A', 'N/A', 'N/A', 'N/A'], '4': ['N/A', 'N/A', 'N/A', 'N/A']}

        h3 = re.search(r'Img_GainModeBand1="([1-4])"[\s]*'
                       r'Img_GainModeBand2="([1-4])"[\s]*'
                       r'Img_GainModeBand3="([1-4])"'
                       r'[\s]*Img_GainModeBand4="([1-4])"',
                       sum_, re.I)
        self.additional.append(
            ["GainMode: B1:'%s',B2:'%s',B3:'%s',B4:'%s'" % (h3.group(1), h3.group(2), h3.group(3), h3.group(4))])
        self.Gains = dict(zip(LBA_full_sorted, [gains_AVNIR[h3.group(1)][0], gains_AVNIR[h3.group(2)][1],
                                                gains_AVNIR[h3.group(3)][2], gains_AVNIR[h3.group(4)][3]]))
        self.Offsets = dict(zip(LBA_full_sorted, [0, 0, 0, 0]))  # only gains are required for DN2radiance calculation

        # Solar irradiance, central wavelengths, full width half maximum per band
        self.wvlUnit = 'Nanometers'
        # derive number of bands from number of given gains/offsets in header file or from raster data
        # noinspection PyBroadException
        try:
            self.nBands = (np.mean([len(self.Gains), len(self.Offsets)])
                           if np.std([len(self.Gains), len(self.Offsets)]) == 0 and len(self.Gains) != 0 else
                           GEOP.GEOPROCESSING(self.Dataname, self.logger).bands)
        except Exception:
            self.logger.warning('Unable to get number of bands for the dataset %s Provider values are used for '
                                'solar irradiation, CWL and FWHM!.' % self.Dataname)
        self.LayerBandsAssignment = get_LayerBandsAssignment(self.GMS_identifier, self.nBands)

        # Exact values calculated based in SRFs
        self.SolIrradiance, self.CWL, self.FWHM = self.calc_solar_irradiance_CWL_FWHM_per_band()
        # Provider values
        if not self.SolIrradiance:
            # Preconfigured Irradiation values
            # = Thullier. source: https://earth.esa.int/c/document_library/get_file?folderId=19584&name=DLFE-262.pdf
            self.SolIrradiance = dict(zip(LBA_full_sorted, [1943.3, 1813.7, 1562.3, 1076.5]))
            # Preconfigured CWLs
            self.CWL = dict(zip(LBA_full_sorted, [460., 560., 650., 825.]))
            # http://www.isprs-ann-photogramm-remote-sens-spatial-inf-sci.net/I-7/291/2012/isprsannals-I-7-291-2012.pdf
            self.FWHM = dict(zip(LBA_full_sorted, [80., 80., 80., 130.]))

        self.filter_layerdependent_metadata()
        self.orbitParams = get_orbit_params(self.GMS_identifier)
        self.spec_vals = get_special_values(self.GMS_identifier)

    def Read_ALOS_LEADER(self):
        """Read metadata from ALOS leader file. binary.

        For exact information content see:
        file:///misc/ro2/behling/Satelliten/ALOS/doc/ALOS Product Format description.pdf
        """

        #    self.default_attr()
        if os.path.isdir(self.FolderOrArchive):
            glob_res = glob.glob(os.path.join(self.FolderOrArchive, '*/*data*/LED-*'))
            assert len(glob_res) > 0, 'No LED* file can be found in %s/*/*data*/!' % self.FolderOrArchive
            self.Metafile = glob_res[0]
            lead_ = open(self.Metafile, "rb").read()
        else:  # archive
            lead_, self.Metafile = \
                open_specific_file_within_archive(self.FolderOrArchive, '*/*data*/LED-*', read_mode='rb')

        # Gains & offsets
        LBA_full_sorted = natsorted(self.LayerBandsAssignment_full)
        self.Gains = dict(zip(LBA_full_sorted, [float(lead_[4680 * 3 + 2703:4680 * 3 + 2710]),
                                                float(lead_[4680 * 3 + 2719:4680 * 3 + 2726]),
                                                float(lead_[4680 * 3 + 2735:4680 * 3 + 2742]),
                                                float(lead_[4680 * 3 + 2751:4680 * 3 + 2758])]))
        self.Offsets = dict(zip(LBA_full_sorted, [float(lead_[4680 * 3 + 2711:4680 * 3 + 2718]),
                                                  float(lead_[4680 * 3 + 2727:4680 * 3 + 2734]),
                                                  float(lead_[4680 * 3 + 2743:4680 * 3 + 2750]),
                                                  float(lead_[4680 * 3 + 2759:4680 * 3 + 2766])]))

    def Read_Sentinel2_xmls(self):
        """Read metadata from Sentinel-2 generic xml and granule xml"""

        # query database to get entityid
        assert self.SceneID and self.SceneID != -9999, "Read_Sentinel2_xmls(): Missing scene ID. "
        res = DB_T.get_info_from_postgreSQLdb(CFG.conn_database, 'scenes', ['entityid'], {'id': self.SceneID})
        assert len(res) != 0, \
            "Invalid SceneID given - no corresponding scene with the ID=%s found in database.\n" % self.SceneID
        assert len(res) == 1, "Error in database. The sceneid %s exists more than once. \n" % self.SceneID

        S2AB = 'S2A' if re.search(r"Sentinel-2A", self.Satellite, re.I) else 'S2B'
        S2ABgranuleID = res[0][0]

        #################
        # get XML roots #
        #################

        if os.path.isdir(self.FolderOrArchive):
            # metadata has to be read from folder
            #####################################

            # get xml_Scene_root (contains scene metadata)
            glob_res = glob.glob(os.path.join(self.FolderOrArchive, '%s*.xml' % S2AB))
            if not glob_res:
                # new style packaging
                glob_res = glob.glob(os.path.join(self.FolderOrArchive, 'MTD*.xml'))
            assert len(glob_res) > 0, 'No %s*.xml or MTD*.xml file can be found in %s/!' % (S2AB, self.FolderOrArchive)
            self.Metafile = glob_res[0]
            xml_Scene_root = ET.parse(glob_res[0]).getroot()  # xml_parser from file

            # get xml_GR_root (contains granule metadata)
            glob_res = glob.glob(os.path.join(self.FolderOrArchive, 'GRANULE/' + S2ABgranuleID + '/%s*.xml' % S2AB))
            if not glob_res:
                # new style packaging
                glob_res = glob.glob(os.path.join(self.FolderOrArchive, 'GRANULE/' + S2ABgranuleID + '/MTD*.xml'))
            assert len(glob_res) > 0, \
                'No  /GRANULE/<%sgranuleID>/%s*.xml or MTD*.xml file can be found in %s/!' \
                % (S2AB, S2AB, self.FolderOrArchive)
            self.Metafile = self.Metafile + ", " + glob_res[0]
            xml_GR_root = ET.parse(glob_res).getroot()  # xml_parser from file

        else:
            # metadata has to be read from within archive
            #############################################

            # get xml_Scene_root and xml_GR_root (contain scene and granule metadata)
            try:
                # old style packaging
                xml_SC_str_, self.Metafile = \
                    open_specific_file_within_archive(self.FolderOrArchive, '*.SAFE/%s*.xml' % S2AB)
                xml_GR_str_, Metafile_ = \
                    open_specific_file_within_archive(self.FolderOrArchive, '*.SAFE/GRANULE/' +
                                                      S2ABgranuleID + '/%s*.xml' % S2AB)
            except RuntimeError:  # wrong matching expression
                # new style packaging
                xml_SC_str_, self.Metafile = open_specific_file_within_archive(self.FolderOrArchive, '*.SAFE/MTD*.xml')
                xml_GR_str_, Metafile_ = open_specific_file_within_archive(self.FolderOrArchive, '*.SAFE/GRANULE/' +
                                                                           S2ABgranuleID + '/MTD*.xml')

            xml_Scene_root = ET.fromstring(xml_SC_str_)
            xml_GR_root = ET.fromstring(xml_GR_str_)
            self.Metafile = self.Metafile + ", " + Metafile_

        ###################################
        # EXTRACT METADATA FROM XML ROOTS #
        ###################################

        # define Sentinel 2 metadata (hard coded)
        self.Sensor = "MSI"

        # extract metadata from xml_Scene_root #
        ########################################

        # get the namespace within the xml_Scene_root
        m = re.match(r'{(.*)\}', xml_Scene_root.tag)  # extract namespace from "{https://....}Level-1C_Tile_ID"
        assert m, 'XML Namespace could not be identified within Sentinel-2 metadata XML file.'
        namespace = m.group(1)

        self.EntityID = \
            xml_Scene_root.find(".//Datatake").attrib['datatakeIdentifier']  # FIXME tileID (Granule) oder scene ID???
        self.Satellite = xml_Scene_root.find(".//SPACECRAFT_NAME").text

        # AcqDate, AcqTime
        # NOTE ths corresponds to the while data take, not to the granule, BUT has th same value as the one from granule
        # DateTime     = xml_Scene_root.find(".//PRODUCT_START_TIME").text
        # ''' PRODUCT_START_TIME = Sensing Time of the first line of the first scene in the product.
        # Alternative: 'DATATAKE_SENSING_START': Sensing start time of the Datatake'''
        # self.AcqDate = DateTime[:10]
        # self.AcqTime = DateTime[11:19]

        self.ScaleFactor = int(xml_Scene_root.find(".//QUANTIFICATION_VALUE").text)
        self.PhysUnit = "TOA_Reflectance in [0-%d]" % self.ScaleFactor

        # Flight direction
        Fdir = {'ASCENDING': "Ascending", 'DESCENDING': "Descending"}
        self.additional.append(["Flight Direction", Fdir[xml_Scene_root.find(".//SENSING_ORBIT_DIRECTION").text]])

        self.ProcLCode = xml_Scene_root.find(".//PROCESSING_LEVEL").text

        # extract metadata from xml_GR_root #
        #####################################

        # get the namespace within the xml_GR_root
        m = re.match(r'{(.*)\}', xml_GR_root.tag)  # extract namespace from "{https://....}Level-1C_Tile_ID"
        assert m, 'XML Namespace could not be identified within metadata XML file.'
        namespace = m.group(1)  # e.g., "https://psd-12.sentinel2.eo.esa.int/PSD/S2_PDI_Level-1C_Tile_Metadata.xsd"

        # set self.AcqDateTime as well as self.AcqDate and self.AcqTime
        self.AcqDateTime = iso8601.parse_date(xml_GR_root.find(".//SENSING_TIME").text)

        # SunAngles
        self.SunElevation = 90 - float(xml_GR_root.find(".//Mean_Sun_Angle/ZENITH_ANGLE").text)  # mean angle of granule
        self.SunAzimuth = float(xml_GR_root.find(".//Mean_Sun_Angle/AZIMUTH_ANGLE").text)  # mean angle of granule

        # coordinate system
        geo_codings = HLP_F.find_in_xml_root(namespace, xml_GR_root, 'Geometric_Info', "Tile_Geocoding")
        self.CS_EPSG = int(geo_codings.find(".//HORIZONTAL_CS_CODE").text.split(":")[1])
        CooSys = geo_codings.find(".//HORIZONTAL_CS_NAME").text
        self.CS_DATUM = "WGS84" if re.search(r"wgs84", CooSys, re.I).group(0) else self.CS_DATUM
        self.CS_TYPE = "UTM" if re.search(r"utm", CooSys, re.I).group(0) else self.CS_TYPE
        if self.CS_TYPE == "UTM":
            tmp = CooSys.split(" ")[-1]
            self.CS_UTM_ZONE = \
                int(tmp[:-1]) if tmp[-1] == 'N' else \
                -int(tmp[:-1]) if tmp[-1] == 'S' else self.CS_UTM_ZONE

        # corner coords
        subsytem_Res_dic = {"%s10" % S2AB: 10, "%s20" % S2AB: 20, "%s60" % S2AB: 60}
        if self.CS_TYPE == 'UTM':
            spatial_samplings = {float(size.get("resolution")): {key: int(size.find(key).text)
                                                                 for key in ["NROWS", "NCOLS"]} for size in
                                 geo_codings.findall("Size")}
            for geo in geo_codings.findall("Geoposition"):
                spatial_samplings[float(geo.get("resolution"))].update(
                    {key: float(geo.find(key).text) for key in ["ULX", "ULY", "XDIM", "YDIM"]})

            ss_sub = spatial_samplings[subsytem_Res_dic[self.Subsystem]]
            LRX = ss_sub['ULX'] + ss_sub['NCOLS'] * ss_sub['XDIM']
            LRY = ss_sub['ULY'] + ss_sub['NROWS'] * ss_sub['YDIM']
            self.CornerTieP_UTM = [(ss_sub['ULX'], ss_sub['ULY']), (LRX, ss_sub['ULY']),
                                   (ss_sub['ULX'], LRY), (LRX, LRY)]  # (x,y) for UL,UR,LL,LR

        # geometricResolution
        self.gResolution = subsytem_Res_dic[self.Subsystem]

        # determine metadata from extracted metadata values
        self.EarthSunDist = self.get_EarthSunDistance(self.AcqDate)

        # Quality flags # FIXME does not work (at least with old data)
        Quality_temp = (xml_Scene_root.find(".//Technical_Quality_Assessment"))
        self.Quality.append(["DEGRADED_ANC_DATA_PERCENTAGE", Quality_temp.find("./DEGRADED_ANC_DATA_PERCENTAGE").text])
        self.Quality.append(["DEGRADED_MSI_DATA_PERCENTAGE", Quality_temp.find("./DEGRADED_MSI_DATA_PERCENTAGE").text])
        Quality_temp2 = xml_Scene_root.find(".//Quality_Inspections")
        quality_flags = ["SENSOR_QUALITY_FLAG", "GEOMETRIC_QUALITY_FLAG", "GENERAL_QUALITY_FLAG",
                         "FORMAT_CORRECTNESS_FLAG", "RADIOMETRIC_QUALITY_FLAG"]

        try:
            # layout example: <SENSOR_QUALITY_FLAG>PASSED</SENSOR_QUALITY_FLAG>
            for ql in quality_flags:
                self.Quality.append([ql, Quality_temp2.find("./" + ql).text])
        except AttributeError:
            # since ~11/2017 the quality checks layout in the XML has changed:
            # layout example: <quality_check checkType="SENSOR_QUALITY">PASSED</quality_check>
            elements = Quality_temp2.findall('quality_check')
            checkTypeValDict = {ele.attrib['checkType']: ele.text for ele in elements}
            for ql in quality_flags:
                self.Quality.append([ql, checkTypeValDict[ql.split('_FLAG')[0]]])

        ##########################
        # band specific metadata #
        ##########################

        LBA_full_sorted = natsorted(self.LayerBandsAssignment_full)

        # ATTENTION Gains are only provided for 12 bands! I don't know why?
        Gains = [float(ele.text) for ele in xml_Scene_root.findall(".//PHYSICAL_GAINS")]
        Gains = Gains if len(Gains) == 13 else [1] + Gains
        self.Gains = dict(zip(LBA_full_sorted, Gains))
        # FIXME assuming that the first band at 443nm has been left out here IS POSSIBLY WRONG
        # FIXME (could also be band 8A oder band 9 (water vapour))

        # Solar irradiance, central wavelengths, full width half maximum per band
        self.wvlUnit = 'Nanometers'
        self.LayerBandsAssignment = get_LayerBandsAssignment(self.GMS_identifier)

        # Exact values calculated based in SRFs
        self.SolIrradiance, self.CWL, self.FWHM = self.calc_solar_irradiance_CWL_FWHM_per_band()
        # Provider values
        if not self.SolIrradiance:
            # get from xml file
            self.SolIrradiance = \
                dict(zip(LBA_full_sorted,
                         [float(ele.text) for ele in
                          xml_Scene_root.find(".//Solar_Irradiance_List").findall("SOLAR_IRRADIANCE")]))
            # Preconfigured CWLs
            self.CWL = dict(zip(LBA_full_sorted,
                                [float(ele.text) for ele in
                                 xml_Scene_root.find(".//Spectral_Information_List").findall(".//CENTRAL")]))

        # SensorAngles
        meta_temp = {}
        branch = HLP_F.find_in_xml_root(namespace, xml_GR_root, *("Geometric_Info", "Tile_Angles"))
        meta_temp["bandId2bandName"] = {int(ele.get("bandId")): ele.text.split("_")[-2] for ele in
                                        xml_GR_root.findall(".//MASK_FILENAME") if ele.get("bandId") is not None}
        meta_temp["bandName2bandId"] = {bandName: bandId for bandId, bandName in
                                        meta_temp["bandId2bandName"].items()}
        meta_temp["bandIds"] = sorted(list(meta_temp["bandId2bandName"].keys()))
        meta_temp["viewing_zenith_detectors"] = \
            {bandId: {bf.get("detectorId"): HLP_F.get_values_from_xml(HLP_F.find_in_xml(bf, *("Zenith", "Values_List")))
                      for bf in branch.findall("Viewing_Incidence_Angles_Grids[@bandId='%i']" % bandId)}
             for bandId in meta_temp["bandIds"]}
        meta_temp["viewing_zenith"] = HLP_F.stack_detectors(meta_temp["viewing_zenith_detectors"])

        meta_temp["viewing_azimuth_detectors"] = {bandId: {bf.get("detectorId"): HLP_F.get_values_from_xml(
            HLP_F.find_in_xml(bf, *("Azimuth", "Values_List"))) for bf in branch.findall(
            "Viewing_Incidence_Angles_Grids[@bandId='%i']" % bandId)} for bandId in meta_temp["bandIds"]}
        meta_temp["viewing_azimuth"] = HLP_F.stack_detectors(meta_temp["viewing_azimuth_detectors"])
        # mean values of all mean band values  # FIXME
        self.ViewingAngle = np.mean([np.nanmean(i) for i in meta_temp['viewing_zenith'].values()])
        self.IncidenceAngle = np.mean([np.nanmean(i) for i in meta_temp['viewing_azimuth'].values()])
        # 5000m step arrays per band. dict: key = bandindex, value = stacked_array for all detectors

        self.ViewingAngle_arrProv = meta_temp['viewing_zenith']
        self.IncidenceAngle_arrProv = meta_temp['viewing_azimuth']
        LBA2Id_dic = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '8A': 8, '9': 9, '10': 10,
                      '11': 11, '12': 12}

        def filter_dic(AngleArr): return {LBAn: AngleArr[LBA2Id_dic[LBAn]] for LBAn in self.LayerBandsAssignment}

        self.ViewingAngle_arrProv = filter_dic(self.ViewingAngle_arrProv)
        self.IncidenceAngle_arrProv = filter_dic(self.IncidenceAngle_arrProv)

        self.FOV = get_FieldOfView(self.GMS_identifier)
        self.orbitParams = get_orbit_params(self.GMS_identifier)
        self.filter_layerdependent_metadata()
        self.spec_vals = get_special_values(self.GMS_identifier)

    def add_rasObj_dims_projection_physUnit(self, rasObj, dict_LayerOptTherm, temp_logger=None):
        self.rows = rasObj.rows
        self.cols = rasObj.cols
        self.bands = rasObj.bands
        if rasObj.projection != '':
            self.map_info = geotransform2mapinfo(rasObj.geotransform, rasObj.projection)
            self.projection = rasObj.projection
            self.gResolution = abs(rasObj.geotransform[1])
            self.CS_EPSG = WKT2EPSG(rasObj.projection)

        dict_conv_physUnit = {'Rad': "W * m-2 * sr-1 * micrometer-1",
                              'TOA_Ref': 'TOA_Reflectance in [0-%d]' % CFG.scale_factor_TOARef,
                              'BOA_Ref': 'BOA_Reflectance in [0-%d]' % CFG.scale_factor_BOARef,
                              'Temp': 'Degrees Celsius with scale factor = 100'}
        if list(set(dict_LayerOptTherm.values())) == ['optical']:
            self.PhysUnit = dict_conv_physUnit[CFG.target_radunit_optical]
        elif list(set(dict_LayerOptTherm.values())) == ['thermal']:
            self.PhysUnit = dict_conv_physUnit[CFG.target_radunit_thermal]
        elif sorted(list(set(dict_LayerOptTherm.values()))) == ['optical', 'thermal']:
            self.PhysUnit = ['Optical bands: %s' % dict_conv_physUnit[CFG.target_radunit_optical],
                             'Thermal bands: %s' % dict_conv_physUnit[CFG.target_radunit_thermal]]
        else:
            logger = self.logger if hasattr(self, 'logger') else temp_logger
            assert logger, "ERROR: Physical unit could not be determined due to unexpected 'dict_LayerOptTherm'. " \
                           "Got %s." % dict_LayerOptTherm
            logger.error("Physical unit could not be determined due to unexpected 'dict_LayerOptTherm'. Got %s."
                         % dict_LayerOptTherm)

    def to_odict(self):
        # type: () -> collections.OrderedDict
        """Creates an OrderedDict containing selected attribute of the METADATA object that will later be included in
        ENVI file headers in the same order.

        """
        # FIXME orbit params are missing
        # descr_dic = dict(  # FillZeroSaturated von HLP_F ausgeben lassen
        #     ALOS_Rad=
        #     "(1) GEOCODED Level1B2 Product; '" + self.Dataname + "'\n "
        #     "(2) Int16 RadianceData in [W * m-2 * sr-1 * micrometer-1]*10; "
        #     "radiance scale factor: 10 (fillPixels: -99, zeroPixels:0, saturatedPixels: 32767 (Max of Int16))'",
        #     ALOS_Ref=
        #     "(1) Orthorectified JAXA or GFZ; '" + self.Dataname + "'\n "
        #     "(2) Int16 TOA_Reflectance in [0-10000]; "
        #     "radiance scale factor: 10 (fillPixels: -99, zeroPixels:0, saturatedPixels: 32767 (Max of Int16))'",
        #     Terra_Rad=
        #     "(1) Orthorectified JAXA or GFZ; '" + self.Dataname + "'\n "
        #     "(2) Int16 RadianceData in [W * m-2 * sr-1 * micrometer-1]*10; "
        #     "radiance scale factor: 10 (fillPixels: -99, zeroPixels:0, saturatedPixels: 32767 (Max of Int16))'",
        #     Terra_Ref=
        #     "(1) Orthorectified JAXA or GFZ; '" + self.Dataname + "'\n "
        #     "(2) Int16 TOA_Reflectance in [0-10000]; "
        #     "radiance scale factor: 10 (fillPixels: -99, zeroPixels:0, saturatedPixels: 32767 (Max of Int16))'",
        #     Landsat_Rad=
        #     "(1) Landsat DN: "+self.ProcLCode+ " Product; '"+self.Dataname+"'\n "
        #     "(2) Int16 RadianceData in [W * m-2 * sr-1 * micrometer-1]*10; "
        #     "radiance scale factor: 10 (fillPixels: -99, zeroPixels:0, saturatedPixels: 32767 (Max of Int16))'",
        #     Landsat_Ref=
        #     "(1) Landsat DN: "+self.ProcLCode +  " Product; '" + self.Dataname + "'\n "
        #     "(2) Int16 TOA_Reflectance in [0-10000] "
        #     "(fillPixels: -99, zeroPixels:0, saturatedPixels: 32767 (Max of Int16))'",
        #     RapidEye_Rad=
        #     "(1) Ortho Level3A01 Product; '"+self.Dataname+"'\n "
        #     "(2) Int16 RadianceData in [W * m-2 * sr-1 * micrometer-1]*10; "
        #     "radiance scale factor: 10 (fillPixels: -99, zeroPixels:0, saturatedPixels: 32767 (Max of Int16))'",
        #     RapidEye_Ref=
        #     "(1) Ortho Level3A01 Product; '" + self.Dataname + "'\n "
        #     "(2) Int16 TOA_Reflectance in [0-10000] "
        #     "(fillPixels: -99, zeroPixels:0, saturatedPixels: 32767 (Max of Int16))'",
        #     SPOT_Rad=
        #     "(1) Ortho Level3A01 Product; '" + self.Dataname + "'\n "
        #     "(2) Int16 RadianceData in [W * m-2 * sr-1 * micrometer-1]*10; "
        #     "radiance scale factor: 10 (fillPixels: -99, zeroPixels:0, saturatedPixels: 32767 (Max of Int16))'",
        #     SPOT_Ref=
        #     "(1) Ortho Level3A01 Product; '" + self.Dataname + "'\n "
        #     "(2) Int16 TOA_Reflectance in [0-10000] "
        #     "(fillPixels: -99, zeroPixels:0, saturatedPixels: 32767 (Max of Int16))'")

        # copy directly compatible keys
        Meta = collections.OrderedDict()
        # Meta['description'] = descr_dic[self.Satellite + '_' + CFG.target_radunit_optical]

        for odictKey in enviHdr_keyOrder:
            if odictKey in map_odictKeys_objAttrnames:
                attrVal = getattr(self, map_odictKeys_objAttrnames[odictKey])
                if attrVal and map_odictKeys_objAttrnames[odictKey] in layerdependent_metadata:
                    # convert band specific metadata dicts to lists in the order of LayerBandsAssignment
                    Meta.update({odictKey: [attrVal[band] for band in self.LayerBandsAssignment if band in attrVal]})
                else:
                    Meta.update({odictKey: attrVal})
            elif odictKey == 'map info' and self.map_info:
                Meta['map info'] = self.map_info
            elif odictKey == 'coordinate system string' and self.projection:
                Meta['coordinate system string'] = self.projection
            elif odictKey == 'data ignore value':
                Meta['data ignore value'] = self.spec_vals['fill'] if 'fill' in self.spec_vals else None
            elif odictKey == 'corner coordinates lonlat':
                Meta['corner coordinates lonlat'] = str(self.CornerTieP_LonLat).replace('(', '[').replace(')', ']')
            elif odictKey == 'wavelength units':
                Meta['wavelength units'] = "Nanometers"
            elif odictKey == 'band names':
                Meta['band names'] = self.bandnames

        # add keys that will not be included into ENVI header
        if self.ViewingAngle_arrProv is not None:
            Meta['ViewingAngle_arrProv'] = {k: v.tolist() for k, v in self.ViewingAngle_arrProv.items()}
        Meta['IncidenceAngle'] = self.IncidenceAngle
        if self.IncidenceAngle_arrProv is not None:
            Meta['IncidenceAngle_arrProv'] = {k: v.tolist() for k, v in self.IncidenceAngle_arrProv.items()}

        return Meta

    def from_odict(self, odict):
        # type: (collections.OrderedDict) -> METADATA

        # copy directly compatible keys
        # [setattr(self, attrN, odict[odictKey]) for odictKey, attrN in map_odictKeys_objAttrnames.items()]

        for odictKey, attrN in map_odictKeys_objAttrnames.items():
            if attrN not in layerdependent_metadata:
                setattr(self, attrN, odict[odictKey])
            else:
                # convert band specific metadata to dicts
                setattr(self, attrN, dict(zip(odict['LayerBandsAssignment'], odict[odictKey])))

        # set the remaining attributes
        if 'map info' in odict:
            self.map_info = odict['map info']
        if 'coordinate system string' in odict:
            self.projection = odict['coordinate system string']
        if 'data ignore value' in odict:
            self.spec_vals['fill'] = odict['data ignore value']
        if 'ViewingAngle_arrProv' in odict:
            self.ViewingAngle_arrProv = {bN: np.array(odict['ViewingAngle_arrProv'][bN])
                                         for bN in self.LayerBandsAssignment if bN in odict['ViewingAngle_arrProv']}
        if 'IncidenceAngle_arrProv' in odict:
            self.IncidenceAngle_arrProv = {bN: np.array(odict['IncidenceAngle_arrProv'][bN])
                                           for bN in self.LayerBandsAssignment if bN in odict['IncidenceAngle_arrProv']}

        return self

    def calc_solar_irradiance_CWL_FWHM_per_band(self):
        # type: () -> (dict, dict, dict)
        sensorcode = get_GMS_sensorcode(self.GMS_identifier)
        # ms_pan = ('multi' if self.nBands > 1 else 'pan')

        irr_bands, cwl_bands, fwhm_bands = {}, {}, {}

        if not sensorcode:
            self.logger.warning('GMS-sensorcode missing. Provider values are used for solar irradiation, CWL and FWHM.')
        else:
            self.logger.info('Calculating solar irradiance, central wavelengths and full width half maxima...')

            sol_irr = Solar_Irradiance_reader(wvl_min_nm=350, wvl_max_nm=2500)
            srf_dict = SRF_Reader(self.GMS_identifier, no_pan=False, no_thermal=False)

            for band in srf_dict.keys():
                if srf_dict[band] is None:
                    irr_bands[band] = None
                    cwl_bands[band] = None
                    fwhm_bands[band] = None
                else:
                    WVL_band = (srf_dict[band][:, 0] if 300 < np.max(srf_dict[band][:, 0]) < 15000 else
                                srf_dict[band][:, 0] * 1000)  # reads wavelengths given in nm and µm
                    RSP_band = srf_dict[band][:, 1]
                    # sol_irr_at_WVL = \
                    #     scipy.interpolate.interp1d(sol_irr[:, 0], sol_irr[:, 1], kind='linear')(WVL_band)  # ASTER
                    # band 8: ValueError: A value in x_new is above the interpolation range.
                    sol_irr_at_WVL = np.interp(WVL_band, sol_irr[:, 0], sol_irr[:, 1], left=0, right=0)

                    irr_bands[band] = round(np.sum(sol_irr_at_WVL * RSP_band) / np.sum(RSP_band), 2)
                    cwl_bands[band] = round(np.sum(WVL_band * RSP_band) / np.sum(RSP_band), 2)
                    fwhm_bands[band] = round(np.max(WVL_band[RSP_band >= (np.max(RSP_band) / 2.)]) -
                                             np.min(WVL_band[RSP_band >= (np.max(RSP_band) / 2.)]), 2)

        return irr_bands, cwl_bands, fwhm_bands

    def get_EarthSunDistance(self, acqDate):
        """Get earth sun distance (requires file of pre calculated earth sun distance per day)

        :param acqDate:
        """

        if not os.path.exists(CFG.path_earthSunDist):
            self.logger.warning("\n\t WARNING: Earth Sun Distance is assumed to be "
                                "1.0 because no database can be found at %s.""" % CFG.path_earthSunDist)
            return 1.0
        if not acqDate:
            self.logger.warning("\n\t WARNING: Earth Sun Distance is assumed to be 1.0 because "
                                "acquisition date could not be read from metadata.")
            return 1.0

        with open(CFG.path_earthSunDist, "r") as EA_dist_f:
            EA_dist_dict = {}
            for line in EA_dist_f:
                date, EA = [item.strip() for item in line.split(",")]
                EA_dist_dict[date] = EA

        return float(EA_dist_dict[acqDate])

    def calc_center_acquisition_time(self, fullSceneCornerLonLat, logger):
        """Calculates a missing center acquistion time using acquisition date, full scene corner coordinates and
        solar azimuth.

        :param fullSceneCornerLonLat:
        :param logger:
        """
        assert is_dataset_provided_as_fullScene(self.GMS_identifier) and len(fullSceneCornerLonLat) == 4, \
            'Center acquisition time can only be computed for datasets provided as full scenes, not for tiles.'

        ul, lr = fullSceneCornerLonLat[0], fullSceneCornerLonLat[3]
        center_coord = [np.mean([ul[0], lr[0]]), np.mean([ul[1], lr[1]])]
        time0_ord = mdates.date2num(
            datetime.datetime.strptime('%s %s' % (self.AcqDate, '00:00:00'), '%Y-%m-%d %H:%M:%S'))
        time1_ord = mdates.date2num(
            datetime.datetime.strptime('%s %s' % (self.AcqDate, '23:59:59'), '%Y-%m-%d %H:%M:%S'))
        time_stamps_ord = np.linspace(time0_ord, time1_ord, 12 * 60 * 60)
        time_stamps_with_tzinfo = mdates.num2date(time_stamps_ord)
        time_stamps = np.array([time_stamps_with_tzinfo[i].replace(tzinfo=None)
                                for i in range(len(time_stamps_with_tzinfo))])
        sols_az_rad = astronomy.get_alt_az(time_stamps, [center_coord[0]] * time_stamps.size,
                                           [center_coord[1]] * time_stamps.size)[1]
        sol_azs = 180 * sols_az_rad / math.pi
        diff_az = np.abs(float(self.SunAzimuth) - sol_azs)
        acq_datetime = time_stamps[np.where(diff_az == np.min(diff_az))][0]
        AcqTime = acq_datetime.strftime(format='%H:%M:%S')
        logger.info('Center acquisition time has been calculated: %s' % AcqTime)

        # update self.
        self.AcqDateTime = datetime.datetime.strptime(
            '%s %s%s' % (self.AcqDate, AcqTime, '.000000+0000'), '%Y-%m-%d %H:%M:%S.%f%z')
        return self.AcqTime

    def get_overpassDuration_SceneLength(self, fullSceneCornerLonLat, fullSceneCornerPos, shape_fullArr, logger):
        """Calculates duration of image acquisition in seconds.

        :param fullSceneCornerLonLat:
        :param fullSceneCornerPos:
        :param shape_fullArr:
        :param logger:
        """
        assert is_dataset_provided_as_fullScene(self.GMS_identifier) and len(fullSceneCornerLonLat) == 4, \
            'Overpass duration and scene length can only be computed for datasets provided as full scenes, not for ' \
            'tiles.'

        # check if current scene is a subset
        assert fullSceneCornerPos != list(([0, 0], [0, shape_fullArr[1] - 1],
                                           [shape_fullArr[0] - 1, 0], [shape_fullArr[0] - 1, shape_fullArr[1] - 1])),\
            'Overpass duration and scene length cannot be calculated because the given data represents a subset of ' \
            'the original scene.'

        # compute scene length
        orbitAltitudeKm, orbitPeriodMin = self.orbitParams[0], self.orbitParams[2]
        UL, UR, LL, LR = fullSceneCornerLonLat
        geod = pyproj.Geod(ellps='WGS84')
        scene_length = np.mean([geod.inv(UL[0], UL[1], LL[0], LL[1])[2],
                                geod.inv(UR[0], UR[1], LR[0], LR[1])[2]]) / 1000  # along-track distance [km]
        logger.info('Calculation of scene length...: %s km' % round(float(scene_length), 2))

        # compute overpass duration
        orbitPeriodLength = 2 * math.pi * (6371 + orbitAltitudeKm)
        overpassDurationSec = (scene_length / orbitPeriodLength) * orbitPeriodMin * 60.
        logger.info('Calculation of overpass duration...: %s sec' % round(overpassDurationSec, 2))

        return overpassDurationSec, scene_length

    def filter_layerdependent_metadata(self):
        for attrname in layerdependent_metadata:
            attrVal = getattr(self, attrname)

            if not attrVal:
                continue

            if isinstance(attrVal, dict):
                setattr(self, attrname, {bN: attrVal[bN] for bN in self.LayerBandsAssignment})

            elif isinstance(attrVal, collections.OrderedDict):
                setattr(self, attrname, collections.OrderedDict((bN, attrVal[bN]) for bN in self.LayerBandsAssignment))

            else:
                raise ValueError

            if attrVal:
                assert len(getattr(self, attrname)) == len(self.LayerBandsAssignment)


layerdependent_metadata = ['SolIrradiance', 'CWL', 'FWHM', 'Offsets', 'OffsetsRef', 'Gains', 'GainsRef',
                           'ThermalConstK1', 'ThermalConstK2', 'ViewingAngle_arrProv', 'IncidenceAngle_arrProv']


map_odictKeys_objAttrnames = {
    'samples': 'cols',
    'lines': 'rows',
    'bands': 'bands',
    'version_gms_preprocessing': 'version_gms_preprocessing',
    'versionalias_gms_preprocessing': 'versionalias_gms_preprocessing',
    'CS_EPSG': 'CS_EPSG',
    'CS_TYPE': 'CS_TYPE',
    'CS_DATUM': 'CS_DATUM',
    'CS_UTM_ZONE': 'CS_UTM_ZONE',
    'scene length': 'scene_length',
    'wavelength': 'CWL',
    'bandwidths': 'FWHM',
    'LayerBandsAssignment': 'LayerBandsAssignment',
    'data gain values': 'Gains',
    'data offset values': 'Offsets',
    'reflectance gain values': 'GainsRef',
    'reflectance offset values': 'OffsetsRef',
    'Metafile': 'Metafile',
    'Satellite': 'Satellite',
    'Sensor': 'Sensor',
    'Subsystem': 'Subsystem',
    'EntityID': 'EntityID',
    'SceneID': 'SceneID',
    'gResolution': 'gResolution',
    'AcqDate': 'AcqDate',
    'AcqTime': 'AcqTime',
    'overpass duraction sec': 'overpassDurationSec',
    'ProcLCode': 'ProcLCode',
    'SunElevation': 'SunElevation',
    'SunAzimuth': 'SunAzimuth',
    'SolIrradiance': 'SolIrradiance',
    'ThermalConstK1': 'ThermalConstK1',
    'ThermalConstK2': 'ThermalConstK2',
    'EarthSunDist': 'EarthSunDist',
    'ViewingAngle': 'ViewingAngle',
    'IncidenceAngle': 'IncidenceAngle',
    'FieldOfView': 'FOV',
    'PhysUnit': 'PhysUnit',
    'ScaleFactor': 'ScaleFactor',
    'Quality': 'Quality',
    'Additional': 'additional'
}


def get_LayerBandsAssignment(GMS_id, nBands=None, sort_by_cwl=None, no_thermal=None, no_pan=None,
                             return_fullLBA=False, proc_level=''):
    # type: (GMS_identifier, int, bool, bool, bool, bool, str) -> list
    """Returns LayerBandsAssignment corresponding to given satellite, sensor and subsystem and with respect to
    CFG.sort_bands_by_cwl, CFG.skip_thermal and CFG.skip_pan.

    :param GMS_id:  <dict>, derived from self.get_GMS_identifier()
                            NOTE: only if there is an additional key 'proc_level', the processing level will be
                            respected. This is needed to get the correct LBA after atm. correction
    :param nBands:          should be specified if number of bands differs from standard
                            (e.g. SPOT data containing no PAN)
    :param sort_by_cwl:     whether to sort the returned bands list by central wavelength position
                            (default: CFG.sort_bands_by_cwl)
    :param no_thermal:      whether to exclude thermal bands from the returned bands list
                            (default: CFG.skip_thermal)
    :param no_pan:          whether to exclude panchromatic bands from the returned bands list
                            (default: CFG.skip_pan)
    :param return_fullLBA:  in case there is a subsystem:
                            whether to return LayerBandsAssignment for all bands or for the current subsystem
    :param proc_level:      processing level for which the LayerBandsAssignment is returned
                            (overrides the proc_level given with GMS_id)
    """
    # set defaults
    # NOTE: these values cannot be set in function signature because CFG is not present at library import time
    sort_by_cwl = sort_by_cwl if sort_by_cwl is not None else CFG.sort_bands_by_cwl
    no_thermal = no_thermal if no_thermal is not None else CFG.skip_thermal
    no_pan = no_pan if no_pan is not None else CFG.skip_pan
    proc_level = proc_level or GMS_id.proc_level

    if GMS_id.image_type == 'RSD':
        GMS_sensorcode = get_GMS_sensorcode(GMS_id)
        assert GMS_sensorcode, 'Unable to get Layer Bands Assignment. No valid sensorcode privided (got >None<). '

        if return_fullLBA:
            GMS_sensorcode = \
                'AST_full' if GMS_sensorcode.startswith('AST') else \
                'S2A_full' if GMS_sensorcode.startswith('S2A') else \
                'S2B_full' if GMS_sensorcode.startswith('S2B') else GMS_sensorcode

        dict_LayerBandsAssignment = {
            'AVNIR-2': ['1', '2', '3', '4'],
            'AST_full': ['1', '2', '3N', '3B', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'],
            'AST_V1': ['1', '2', '3N'],
            'AST_V2': ['3B'],
            'AST_S': ['4', '5', '6', '7', '8', '9'],
            'AST_T': ['10', '11', '12', '13', '14'],
            'TM4': ['1', '2', '3', '4', '5', '6', '7'],
            'TM5': ['1', '2', '3', '4', '5', '6', '7'],
            'TM7': ['1', '2', '3', '4', '5', '6L', '6H', '7', '8'],
            'LDCM': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'],
            'SPOT1a': ['1', '2', '3', '4'],
            'SPOT2a': ['1', '2', '3', '4'],
            'SPOT3a': ['1', '2', '3', '4'],
            'SPOT4a': ['1', '2', '3', '4', '5'],
            'SPOT5a': ['1', '2', '3', '4', '5'],
            'SPOT1b': ['1', '2', '3', '4'],
            'SPOT2b': ['1', '2', '3', '4'],
            'SPOT3b': ['1', '2', '3', '4'],
            'SPOT4b': ['1', '2', '3', '4', '5'],
            'SPOT5b': ['1', '2', '3', '4', '5'],
            'RE5': ['1', '2', '3', '4', '5'],
            'S2A_full': ['1', '2', '3', '4', '5', '6', '7', '8', '8A', '9', '10', '11', '12'],
            'S2B_full': ['1', '2', '3', '4', '5', '6', '7', '8', '8A', '9', '10', '11', '12'],
            'S2A10': ['2', '3', '4', '8'],
            'S2A20': ['5', '6', '7', '8A', '11', '12'],
            'S2A60': ['1', '9', '10'],
            'S2B10': ['2', '3', '4', '8'],
            'S2B20': ['5', '6', '7', '8A', '11', '12'],
            'S2B60': ['1', '9', '10'], }

        dict_cwlSorted_LayerBandsAssignment = {
            'TM4': ['1', '2', '3', '4', '5', '7', '6'],
            'TM5': ['1', '2', '3', '4', '5', '7', '6'],
            'TM7': ['1', '2', '3', '8', '4', '5', '7', '6L', '6H'],
            'LDCM': ['1', '2', '3', '8', '4', '5', '9', '6', '7', '10', '11'],
            'SPOT1a': ['1', '4', '2', '3'],
            'SPOT2a': ['1', '4', '2', '3'],
            'SPOT3a': ['1', '4', '2', '3'],
            'SPOT4a': ['1', '5', '2', '3', '4'],
            'SPOT5a': ['1', '5', '2', '3', '4'],
            'SPOT1b': ['1', '4', '2', '3'],
            'SPOT2b': ['1', '4', '2', '3'],
            'SPOT3b': ['1', '4', '2', '3'],
            'SPOT4b': ['1', '5', '2', '3', '4'],
            'SPOT5b': ['1', '5', '2', '3', '4'],
        }

        if nBands is None or nBands == len(dict_LayerBandsAssignment[GMS_sensorcode]):
            assert GMS_sensorcode in dict_LayerBandsAssignment, \
                'Unable to get Layer Bands Assignment. No valid sensorcode privided (got >%s<).' % GMS_sensorcode
            LayerBandsAssignment = dict_LayerBandsAssignment[GMS_sensorcode]
            if sort_by_cwl and GMS_sensorcode in ['TM4', 'TM5', 'TM7', 'LDCM']:
                LayerBandsAssignment = dict_cwlSorted_LayerBandsAssignment[GMS_sensorcode]

        else:  # special case SPOT MSI containing no PAN or SPOT PAN containing only PAN
            assert re.match(r'SPOT', GMS_id.satellite, re.I) and \
                   nBands in [len(dict_LayerBandsAssignment[GMS_sensorcode]) - 1, 1], \
                   "Unable to get Layer Bands Assignment. Provided number of bands doesn´t match known layer band " \
                   "assignments."
            LayerBandsAssignment = [dict_LayerBandsAssignment[GMS_sensorcode][-1]] if nBands == 1 \
                else dict_LayerBandsAssignment[GMS_sensorcode][:-1]

        if no_thermal:
            LayerBandsAssignment = [i for i in LayerBandsAssignment if not isTHERMAL(GMS_id, i)]
        if no_pan:
            LayerBandsAssignment = [i for i in LayerBandsAssignment if not isPAN(GMS_id, i)]
    else:
        LayerBandsAssignment = ['1']

    # remove those bands that are excluded by atmospheric corrections if proc_level >= L1C
    if proc_level not in [None, 'L1A', 'L1B']:  # TODO replace with enum procL

        if CFG.target_radunit_optical == 'BOA_Ref':
            # return LBA after AC
            try:
                bands_after_ac = get_bands_after_AC(GMS_id)
                LayerBandsAssignment = [i for i in LayerBandsAssignment if i in bands_after_ac]
            except ACNotSupportedError:
                # atmospheric correction is not yet supported -> LBA will be the same after L1C
                pass

        if proc_level in ['L2B', 'L2C']:
            # handle different number of bands after spectral homogenization to target sensor

            if GMS_id.dataset_ID == CFG.datasetid_spectral_ref:
                pass  # return normal LBA from above

            elif CFG.datasetid_spectral_ref is not None:
                # the target sensor is NOT a custom sensor but has the spectral characteristics of a known sensor
                # => use the LBA of the target sensor after AC as the new LBA for the requested sensor

                # find out how the spectral characteristics of this known target sensor look like after AC
                from ..model.gms_object import GMS_identifier  # noqa F811  # redefinition of unused 'GMS_identifier'
                tgt_sat, tgt_sen = datasetid_to_sat_sen(CFG.datasetid_spectral_ref)
                tgt_GMSid = GMS_identifier(image_type='RSD', satellite=tgt_sat, sensor=tgt_sen, subsystem='',
                                           proc_level='L2A', dataset_ID=-9999, logger=None)
                try:
                    tgt_sen_LBA = get_bands_after_AC(tgt_GMSid)

                except ACNotSupportedError:
                    # use the target sensor LBA before AC (because target sensor could not be atmospherically corrected)
                    tgt_GMSid.proc_level = 'L1B'

                    tgt_sen_LBA = get_LayerBandsAssignment(tgt_GMSid)

                LayerBandsAssignment = tgt_sen_LBA

            else:
                # fallback: return a LBA matching the number of bands after spectral homogenization
                LayerBandsAssignment = [str(i + 1) for i in range(len(CFG.target_CWL))]

    return LayerBandsAssignment


def get_bands_after_AC(GMS_id):
    # type: (GMS_identifier) -> List[str]
    """Returns a list of bands that are not removed by atmospheric correction.

    :param GMS_id:  <dict>, derived from self.get_GMS_identifier()
    :return: e.g. ['1', '2', '3', '4', '5', '6', '7', '9'] for Landsat-8
    """
    path_ac_options = get_path_ac_options(GMS_id)

    if not path_ac_options or not os.path.exists(path_ac_options):
        raise ACNotSupportedError('Atmospheric correction is not yet supported for %s %s.'
                                  % (GMS_id.satellite, GMS_id.sensor))

    # FIXME this does not work for L7
    # NOTE: don't validate because options contain pathes that do not exist on another server
    ac_bandNs = get_ac_options(path_ac_options, validation=False)['AC']['bands']
    ac_out_bands = [bN.split('B0')[1] if bN.startswith('B0') else bN.split('B')[1] for bN in ac_bandNs]  # sorted

    return ac_out_bands


def get_center_wavelengths_by_LBA(satellite, sensor, LBA, subsystem=None):
    # type: (str, str, list, str) -> List[float]
    """Returns a list of center wavelengths of spectral bands for the given satellite/sensor/LayerBandsAss. combination.

    :param satellite:   target satellite (e.g., 'Sentinel-2A')
    :param sensor:      target sensor (e.g., 'MSI')
    :param LBA:         LayerBandsAssignment
    :param subsystem:   target sensor subsystem (e.g., 'VNIR')
    """
    srf = RSR(satellite=satellite, sensor=sensor, subsystem=subsystem, LayerBandsAssignment=LBA)

    return list(srf.wvl)


def get_dict_LayerOptTherm(GMS_id, LayerBandsAssignment):
    dict_out = collections.OrderedDict()
    [dict_out.update({lr: 'thermal' if isTHERMAL(GMS_id, lr) else 'optical'}) for lr in LayerBandsAssignment]
    return dict_out


def isPAN(GMS_id, LayerNr):
    GMS_sensorcode = get_GMS_sensorcode(GMS_id)
    dict_isPAN = {'TM7': ['8'], 'LDCM': ['8'],
                  'SPOT1a': ['4'], 'SPOT2a': ['4'], 'SPOT3a': ['4'], 'SPOT4a': ['5'], 'SPOT5a': ['5'],
                  'SPOT1b': ['4'], 'SPOT2b': ['4'], 'SPOT3b': ['4'], 'SPOT4b': ['5'], 'SPOT5b': ['5']}
    return True if GMS_sensorcode in dict_isPAN and LayerNr in dict_isPAN[GMS_sensorcode] else False


def isTHERMAL(GMS_id, LayerNr):
    GMS_sensorcode = get_GMS_sensorcode(GMS_id)
    dict_isTHERMAL = {'TM4': ['6'], 'TM5': ['6'], 'TM7': ['6L', '6H'], 'LDCM': ['10', '11'],
                      'AST_T': ['10', '11', '12', '13', '14']}
    return True if GMS_sensorcode in dict_isTHERMAL and LayerNr in dict_isTHERMAL[GMS_sensorcode] else False


def get_FieldOfView(GMS_id):
    GMS_sensorcode = get_GMS_sensorcode(GMS_id)
    dict_FOV = {'AVNIR-2': 5.79,
                'AST_V1': 6.09, 'AST_V2': 5.19, 'AST_S': 4.9, 'AST_T': 4.9,
                # http://eospso.gsfc.nasa.gov/sites/default/files/mission_handbooks/Terra.pdf
                'TM4': 14.92, 'TM5': 14.92, 'TM7': 14.92, 'LDCM': 14.92,
                'SPOT1a': 4.18, 'SPOT2a': 4.18, 'SPOT3a': 4.18, 'SPOT4a': 4.18, 'SPOT5a': 4.18,
                'SPOT1b': 4.18, 'SPOT2b': 4.18, 'SPOT3b': 4.18, 'SPOT4b': 4.18, 'SPOT5b': 4.18,
                'RE5': 6.99,
                'S2A10': 20.6, 'S2A20': 20.6, 'S2A60': 20.6,
                'S2B10': 20.6, 'S2B20': 20.6, 'S2B60': 20.6}
    return dict_FOV[GMS_sensorcode]


def get_orbit_params(GMS_id):
    GMS_sensorcode = get_GMS_sensorcode(GMS_id)

    # sensor altitude above ground [kilometers]
    dict_altitude = {'AVNIR-2': 691.65,
                     'AST_V1': 705, 'AST_V2': 705, 'AST_S': 705, 'AST_T': 705,
                     'TM4': 705, 'TM5': 705, 'TM7': 705, 'LDCM': 705,
                     'SPOT1a': 822, 'SPOT2a': 822, 'SPOT3a': 822, 'SPOT4a': 822, 'SPOT5a': 822,
                     'SPOT1b': 822, 'SPOT2b': 822, 'SPOT3b': 822, 'SPOT4b': 822, 'SPOT5b': 822,
                     'RE5': 630,
                     'S2A10': 786, 'S2A20': 786, 'S2A60': 786,
                     'S2B10': 786, 'S2B20': 786, 'S2B60': 786}

    # sensor inclination [degrees]
    dict_inclination = {'AVNIR-2': 98.16,
                        'AST_V1': 98.3, 'AST_V2': 98.3, 'AST_S': 98.3, 'AST_T': 98.3,
                        'TM4': 98.2, 'TM5': 98.2, 'TM7': 98.2, 'LDCM': 98.2,
                        'SPOT1a': 98.7, 'SPOT2a': 98.7, 'SPOT3a': 98.7, 'SPOT4a': 98.7, 'SPOT5a': 98.7,
                        'SPOT1b': 98.7, 'SPOT2b': 98.7, 'SPOT3b': 98.7, 'SPOT4b': 98.7, 'SPOT5b': 98.7,
                        'RE5': 98,
                        'S2A10': 98.62, 'S2A20': 98.62, 'S2A60': 98.62,
                        'S2B10': 98.62, 'S2B20': 98.62, 'S2B60': 98.62}

    # time needed for one complete earth revolution [minutes]
    dict_period = {'AVNIR-2': 98.7,
                   'AST_V1': 98.88, 'AST_V2': 98.88, 'AST_S': 98.88, 'AST_T': 98.88,
                   'TM4': 98.9, 'TM5': 98.9, 'TM7': 98.9, 'LDCM': 98.9,
                   'SPOT1a': 101.4, 'SPOT2a': 101.4, 'SPOT3a': 101.4, 'SPOT4a': 101.4, 'SPOT5a': 101.4,
                   'SPOT1b': 101.4, 'SPOT2b': 101.4, 'SPOT3b': 101.4, 'SPOT4b': 101.4, 'SPOT5b': 101.4,
                   'RE5': 96.7,
                   'S2A10': 100.6, 'S2A20': 100.6, 'S2A60': 100.6,
                   'S2B10': 100.6, 'S2B20': 100.6, 'S2B60': 100.6}

    return [dict_altitude[GMS_sensorcode], dict_inclination[GMS_sensorcode], dict_period[GMS_sensorcode]]


def get_special_values(GMS_id):
    GMS_sensorcode = get_GMS_sensorcode(GMS_id)  # type: str
    dict_fill = {'AVNIR-2': 0,
                 'AST_V1': 0, 'AST_V2': 0, 'AST_S': 0, 'AST_T': 0,
                 'TM4': 0, 'TM5': 0, 'TM7': 0, 'LDCM': 0,
                 'SPOT1a': 0, 'SPOT2a': 0, 'SPOT3a': 0, 'SPOT4a': 0, 'SPOT5a': 0,
                 'SPOT1b': 0, 'SPOT2b': 0, 'SPOT3b': 0, 'SPOT4b': 0, 'SPOT5b': 0,
                 'RE5': 0,
                 'S2A10': 0, 'S2A20': 0, 'S2A60': 0,
                 'S2B10': 0, 'S2B20': 0, 'S2B60': 0,
                 }
    dict_zero = {'AVNIR-2': None,
                 'AST_V1': 1, 'AST_V2': 1, 'AST_S': 1, 'AST_T': 1,
                 'TM4': None, 'TM5': None, 'TM7': None, 'LDCM': None,
                 'SPOT1a': None, 'SPOT2a': None, 'SPOT3a': None, 'SPOT4a': None, 'SPOT5a': None,
                 'SPOT1b': None, 'SPOT2b': None, 'SPOT3b': None, 'SPOT4b': None, 'SPOT5b': None,
                 'RE5': None,
                 'S2A10': None, 'S2A20': None, 'S2A60': None,
                 'S2B10': None, 'S2B20': None, 'S2B60': None,
                 }
    dict_saturated = {'AVNIR-2': None,
                      'AST_V1': 255, 'AST_V2': 255, 'AST_S': 255, 'AST_T': 65535,
                      'TM4': None, 'TM5': None, 'TM7': None, 'LDCM': 65535,
                      'SPOT1a': 255, 'SPOT2a': 255, 'SPOT3a': 255, 'SPOT4a': 255, 'SPOT5a': 255,
                      'SPOT1b': 255, 'SPOT2b': 255, 'SPOT3b': 255, 'SPOT4b': 255, 'SPOT5b': 255,
                      'RE5': None,
                      'S2A10': 65535, 'S2A20': 65535, 'S2A60': 65535,
                      'S2B10': 65535, 'S2B20': 65535, 'S2B60': 65535
                      }
    return {'fill': dict_fill[GMS_sensorcode],
            'zero': dict_zero[GMS_sensorcode],
            'saturated': dict_saturated[GMS_sensorcode]}


def metaDict_to_metaODict(metaDict, logger=None):
    """Converts a GMS metadata dictionary to an ordered dictionary according to the sorting given in
    Output_writer.enviHdr_keyOrder.

    :param metaDict:    <dict> GMS metadata dictionary
    :param logger:      <logging.logger> if given, warnings will be logged. Otherwise they are raised.
    """

    from ..io.output_writer import enviHdr_keyOrder
    expected_keys = [k for k in enviHdr_keyOrder if k in metaDict]
    only_gmsFile_keys = ['ViewingAngle_arrProv', 'IncidenceAngle_arrProv', 'projection']
    unexpected_keys = [k for k in metaDict.keys() if k not in expected_keys and k not in only_gmsFile_keys]

    if unexpected_keys:
        msg = 'Got unexpected keys in metadata dictionary: %s. Adding them at the end of output header files.' \
              % ', '.join(unexpected_keys)
        if logger:
            logger.warning(msg)
        else:
            warnings.warn(msg)

    meta_vals = [metaDict[k] for k in expected_keys] + [metaDict[k] for k in unexpected_keys]
    return collections.OrderedDict(zip(expected_keys + unexpected_keys, meta_vals))


def LandsatID2dataset(ID_list):
    dataset_list = []
    for ID in ID_list:
        dataset = dict(image_type='RSD', satellite=None, sensor=None, subsystem=None, acquisition_date=None,
                       entity_ID=ID)
        dataset['satellite'] = 'Landsat-5' if ID[:3] == 'LT5' else 'Landsat-7' if ID[:3] == 'LE7' \
            else 'Landsat-8' if ID[:3] == 'LC8' else dataset['satellite']
        dataset['sensor'] = 'TM' if ID[:3] == 'LT5' else 'ETM+' if ID[:3] == 'LE7' else \
            'OLI_TIRS' if ID[:3] == 'LC8' else dataset['satellite']
        dataset['subsystem'] = None
        dataset['acquisition_date'] = \
            (datetime.datetime(int(ID[9:13]), 1, 1) + datetime.timedelta(int(ID[13:16]) - 1)).strftime('%Y-%m-%d')
        dataset_list.append(dataset)
    return dataset_list


def get_sensormode(dataset):
    if re.search(r'SPOT', dataset['satellite']):
        path_archive = path_generator(dataset).get_local_archive_path_baseN()
        dim_ = open_specific_file_within_archive(path_archive, '*/scene01/metadata.dim')[0]
        SPOT_mode = re.search(r"<SENSOR_CODE>([a-zA-Z0-9]*)</SENSOR_CODE>", dim_, re.I).group(1)
        assert SPOT_mode in ['J', 'X', 'XS', 'A', 'P', 'M'], 'Unknown SPOT sensor mode: %s' % SPOT_mode
        return 'M' if SPOT_mode in ['J', 'X', 'XS'] else 'P'
    else:
        return 'M'
