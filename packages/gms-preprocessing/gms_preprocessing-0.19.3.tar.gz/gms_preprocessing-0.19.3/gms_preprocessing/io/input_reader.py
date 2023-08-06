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
# -*- coding: utf-8 -*-
"""GeoMultiSens Input Reader:  Universal reader for all kinds of GeoMultiSens intermediate results."""

import collections
import fnmatch
import json
import os
import re
import tarfile
import zipfile
from tempfile import NamedTemporaryFile as tempFile
from logging import Logger
from typing import List, Tuple, TYPE_CHECKING  # noqa F401  # flake8 issue
from datetime import datetime
import logging

import dill
import numpy as np
import spectral
from spectral.io import envi as envi
from pyproj import CRS

from geoarray import GeoArray
from py_tools_ds.geo.coord_calc import corner_coord_to_minmax
from py_tools_ds.geo.vector.geometry import boxObj
from py_tools_ds.geo.coord_trafo import transform_any_prj
from py_tools_ds.geo.projection import isProjectedOrGeographic
from pyrsr.rsr import RSR_reader

from ..options.config import GMS_config as CFG
from ..misc import path_generator as PG
from ..misc import helper_functions as HLP_F
from ..misc.logging import GMS_logger, close_logger
from ..misc.database_tools import get_overlapping_scenes_from_postgreSQLdb
from ..misc.path_generator import path_generator
from ..misc.spatial_index_mediator import SpatialIndexMediator
from ..misc.locks import DatabaseLock

if TYPE_CHECKING:
    from ..model.gms_object import GMS_identifier  # noqa F401  # flake8 issue


def read_ENVIfile(path, arr_shape, arr_pos, logger=None, return_meta=False, q=0):
    hdr_path = os.path.splitext(path)[0] + '.hdr' if not os.path.splitext(path)[1] == '.hdr' else path
    return read_ENVI_image_data_as_array(hdr_path, arr_shape, arr_pos, logger=logger, return_meta=return_meta, q=q)


def read_ENVIhdr_to_dict(hdr_path, logger=None):
    # type: (str, Logger) -> dict
    if not os.path.isfile(hdr_path):
        if logger:
            logger.critical('read_ENVIfile: Input data not found at %s.' % hdr_path)
        else:
            print('read_ENVIfile: Input data not found at %s.' % hdr_path)
        raise FileNotFoundError(hdr_path)
    else:
        SpyFileheader = envi.open(hdr_path)
        return SpyFileheader.metadata


def read_ENVI_image_data_as_array(path, arr_shape, arr_pos, logger=None, return_meta=False, q=0):
    """Read ENVI image data as array using a specified read pattern.

    :param path:        <str> Path of the ENVI image or header file
    :param arr_shape:   <str> 'cube','row','col','band','block','pixel' or 'custom'
    :param arr_pos:     None, <int> or <list>. The content of the list depends on the chosen arr_shape as follows:
                        - 'cube':   No array position neccessary. Set arr_pos to None.
                        - 'row':    single int. -> Row with this index will be read.
                        - 'col':    single int. -> Column with this index will be read.
                        - 'band':   single int. -> Band with this index will be read.
                        - 'block':  row_bounds (2-tuple of ints): (a, b) -> Rows a through b-1 will be read.
                                    col_bounds (2-tuple of ints): (a, b) -> Columns a through b-1 will be read.
                        - 'pixel':  row, col (int): Indices of the row & column for the pixel to be read.
                        - 'custom': row_bounds (2-tuple of ints): (a, b) -> Rows a through b-1 will be read.
                                    col_bounds (2-tuple of ints): (a, b) -> Columns a through b-1 will be read.
                                    bands (list of ints):  Optional list of bands to read.
                                                            If not specified, all bands are read.
    :param logger:      <instance> of logging.logger (optional)
    :param return_meta: <bool> whether to return not only raster data but also meta data (optional, default=False)
    :param q:           <bool> quiet mode (supresses all console or logging output) (optional, default=False)
    """
    hdr_path = os.path.splitext(path)[0] + '.hdr' if not os.path.splitext(path)[1] == '.hdr' else path
    if not os.path.isfile(hdr_path):
        if not q:
            if logger:
                logger.critical('read_ENVIfile: Input data not found at %s.' % hdr_path)
            else:
                print('read_ENVIfile: Input data not found at %s.' % hdr_path)
    else:
        assert arr_shape in ['cube', 'row', 'col', 'band', 'block', 'pixel', 'custom'], \
            "Array shape '%s' is not known. Known array shapes are cube, row, col, band, block, pixel, custom." \
            % arr_shape
        if logger and not q:
            logger.info('Reading %s ...' % (os.path.basename(hdr_path)))
        File_obj = spectral.open_image(hdr_path)
        SpyFileheader = envi.open(hdr_path)
        image_data = File_obj.read_bands(range(SpyFileheader.nbands)) if arr_shape == 'cube' else \
            File_obj.read_subimage([arr_pos], range(SpyFileheader.ncols)) if arr_shape == 'row' else \
            File_obj.read_subimage(range(SpyFileheader.nrows), [arr_pos]) if arr_shape == 'col' else \
            File_obj.read_band(arr_pos) if arr_shape == 'band' else \
            File_obj.read_subregion((arr_pos[0][0], arr_pos[0][1] + 1),
                                    (arr_pos[1][0], arr_pos[1][1] + 1)) if arr_shape == 'block' else \
            File_obj.read_pixel(arr_pos[0], arr_pos[1]) if arr_shape == 'pixel' else \
            File_obj.read_subregion((arr_pos[0][0], arr_pos[0][1] + 1),
                                    (arr_pos[1][0], arr_pos[1][1] + 1), arr_pos[2])  # custom
        return (image_data, SpyFileheader.metadata) if return_meta else image_data


def read_mask_subset(path_masks, bandname, logger, subset=None):
    subset = subset if subset else ['cube', None]
    assert subset[0] in ['cube', 'block', 'MGRS_tile'], \
        "INP_R.read_mask_subset(): '%s' subset is not supported." % subset[0]
    path_masks_hdr = \
        os.path.splitext(path_masks)[0] + '.hdr' if not os.path.splitext(path_masks)[1] == '.hdr' else path_masks
    hdrDict = read_ENVIhdr_to_dict(path_masks_hdr, logger)
    (rS, rE), (cS, cE) = ((0, hdrDict['lines']), (0, hdrDict['samples'])) if subset[0] == 'cube' else subset[1]
    band_idx = hdrDict['band names'].index(bandname) if bandname in hdrDict['band names'] else None
    if band_idx is None:
        logger.warning("No band called '%s' in %s. Attribute set to <None>." % (bandname, path_masks))
        mask_sub = None
    else:
        if subset is None or subset[0] == 'cube':
            mask_sub = read_ENVI_image_data_as_array(path_masks_hdr, 'band', band_idx, logger=logger, q=1)
        else:
            mask_sub = read_ENVI_image_data_as_array(
                path_masks_hdr, 'custom', ((rS, rE), (cS, cE), [band_idx]), logger=logger, q=1)
        mask_sub = mask_sub[:, :, 0] if len(mask_sub.shape) == 3 and mask_sub.shape[2] == 1 else mask_sub
    return mask_sub


def GMSfile2dict(path_GMSfile):
    """ Converts a JSON file (like the GMS file) to a Python dictionary with keys and values.

    :param path_GMSfile:    absolute path on disk
    :return:                the corresponding Python dictionary
    """
    with open(path_GMSfile) as inF:
        GMSdict = json.load(inF)
    return GMSdict


def unify_envi_header_keys(header_dict):
    """Ensures the compatibility of ENVI header keys written by Spectral-Python the code internal attribute names.
    (ENVI header keys are always lowercase in contrast to the attribute names used in code).

    :param header_dict:
    """
    refkeys = ['AcqDate', 'AcqTime', 'Additional', 'FieldOfView', 'IncidenceAngle', 'Metafile', 'PhysUnit',
               'ProcLCode', 'Quality', 'Satellite', 'Sensor', 'SunAzimuth', 'SunElevation', 'ViewingAngle']
    unified_header_dict = header_dict
    for key in header_dict.keys():
        for refkey in refkeys:
            if re.match(key, refkey, re.I) and key != refkey:
                unified_header_dict[refkey] = header_dict[key]
                del unified_header_dict[key]
    return unified_header_dict


def get_list_GMSfiles(dataset_list, target):
    """Returns a list of absolute paths pointing to gms-files of truely written datasets that fullfill certain criteria.

    :param dataset_list: [dataset1_dictionary, dataset2_dictionary]
    :param target:       target GMS processing level
    :return              [/path/to/gms_file1.gms, /path/to/gms_file1.gms]
    """
    dataset_list = [dataset_list] if not isinstance(dataset_list, list) else dataset_list

    def get_gmsP(ds, tgt):
        return PG.path_generator(ds, proc_level=tgt).get_path_gmsfile()

    GMS_list = [p for p in [get_gmsP(ds, target) for ds in dataset_list] if os.path.exists(p)]

    return GMS_list


def SRF_Reader(GMS_id, no_thermal=None, no_pan=None, v=False):
    # type: (GMS_identifier, bool, bool, bool) -> collections.OrderedDict
    """Read SRF for any sensor and return a dictionary containing band names as keys and SRF numpy arrays as values.

    :param GMS_id:
    :param no_thermal:      whether to exclude thermal bands from the returned bands list
                            (default: CFG.skip_thermal)
    :param no_pan:          whether to exclude panchromatic bands from the returned bands list
                            (default: CFG.skip_pan)
    :param v:               verbose mode
    """
    # set defaults
    # NOTE: these values cannot be set in function signature because CFG is not present at library import time
    no_thermal = no_thermal if no_thermal is not None else CFG.skip_thermal
    no_pan = no_pan if no_pan is not None else CFG.skip_pan

    logger = GMS_id.logger or Logger(__name__)

    SRF_dict = RSR_reader(satellite=GMS_id.satellite,
                          sensor=GMS_id.sensor,
                          subsystem=GMS_id.subsystem,
                          no_thermal=no_thermal,
                          no_pan=no_pan,
                          after_ac=False,
                          sort_by_cwl=True,
                          tolerate_missing=True,
                          logger=logger,
                          v=v)

    return SRF_dict


def pickle_SRF_DB(L1A_Instances, dir_out):
    list_GMS_identifiers = [i.GMS_identifier for i in L1A_Instances]
    out_dict = collections.OrderedDict()
    logger = GMS_logger('log__SRF2PKL', path_logfile=os.path.join(dir_out, 'log__SRF2PKL.log'),
                        log_level=CFG.log_level, append=False)
    for Id, Inst in zip(list_GMS_identifiers, L1A_Instances):
        Id['logger'] = logger
        out_dict[
            Inst.satellite + '_' + Inst.sensor + (('_' + Inst.subsystem) if Inst.subsystem not in ['', None] else '')] \
            = SRF_Reader(Id)
    print(list(out_dict.keys()))
    outFilename = os.path.join(dir_out, 'SRF_DB.pkl')
    with open(outFilename, 'wb') as outFile:
        dill.dump(out_dict, outFile)
        print('Saved SRF dictionary to %s' % outFilename)
    # with open(outFilename, 'rb') as inFile:
    #     readFile = pickle.load(inFile)
    # [print(i) for i in readFile.keys()]
    logger.close()


def Solar_Irradiance_reader(resol_nm=None, wvl_min_nm=None, wvl_max_nm=None):
    """Read the solar irradiance file and return an array of irradiances.

    :param resol_nm:    spectral resolution for returned irradiances [nanometers]
    :param wvl_min_nm:  minimum wavelength of returned irradiances [nanometers]
    :param wvl_max_nm:  maximum wavelength of returned irradiances [nanometers]
    :return:
    """
    from scipy.interpolate import interp1d

    sol_irr = np.loadtxt(CFG.path_solar_irr, skiprows=1)
    if resol_nm is not None and isinstance(resol_nm, (float, int)):
        wvl_min = (np.min(sol_irr[:, 0]) if wvl_min_nm is None else wvl_min_nm)
        wvl_max = (np.max(sol_irr[:, 0]) if wvl_max_nm is None else wvl_max_nm)
        wvl_rsp = np.arange(wvl_min, wvl_max, resol_nm)
        sol_irr = interp1d(sol_irr[:, 0], sol_irr[:, 1], kind='linear')(wvl_rsp)
    return sol_irr


def open_specific_file_within_archive(path_archive, matching_expression, read_mode='r'):
    # type: (str, str, str) -> (str, str)
    """Finds a specific file within an archive using a given matching expression and returns its content as string.

    :param path_archive:        the file path of the archive
    :param matching_expression: the matching expession to find the file within the archive
    :param read_mode:           the read mode used to open the archive (default: 'r')
    :return: tuple(content_file, filename_file)
    """

    file_suffix = os.path.splitext(path_archive)[1][1:]
    file_suffix = 'tar.gz' if path_archive.endswith('tar.gz') else file_suffix
    assert file_suffix in ['zip', 'tar', 'gz', 'tgz', 'tar.gz'], '*.%s files are not supported.' % file_suffix

    if file_suffix == 'zip':
        archive = zipfile.ZipFile(path_archive, 'r')
        # [print(i) for i in archive.namelist()]
        matching_files = fnmatch.filter(archive.namelist(), matching_expression)

        # NOTE: flink deactivates assertions via python -O flag. So, a usual 'assert matching_files' does NOT work here.
        if not matching_files:
            raise RuntimeError('Matching expression matches no file. Please revise your expression!')
        if len(matching_files) > 1:
            raise RuntimeError('Matching expression matches more than 1 file. Please revise your expression!')

        content_file = archive.read(matching_files[0])
        filename_file = os.path.join(path_archive, matching_files[0])

    else:  # 'tar','gz','tgz', 'tar.gz'
        archive = tarfile.open(path_archive, 'r|gz')  # open in stream mode is much faster than normal mode
        count_matching_files = 0
        for F in archive:
            if fnmatch.fnmatch(F.name, matching_expression):
                content_file = archive.extractfile(F)
                content_file = content_file.read()
                filename_file = os.path.join(path_archive, F.name)
                count_matching_files += 1

        # NOTE: flink deactivates assertions via python -O flag. So, a usual 'assert matching_files' does NOT work here.
        if count_matching_files == 0:
            raise RuntimeError('Matching expression matches no file. Please revise your expression!')
        if count_matching_files > 1:
            raise RuntimeError('Matching expression matches more than 1 file. Please revise your expression!')

    archive.close()
    content_file = content_file.decode('latin-1') \
        if isinstance(content_file, bytes) and read_mode == 'r' else content_file  # Python3

    return content_file, filename_file


class DEM_Creator(object):
    def __init__(self, dem_sensor='SRTM', db_conn='', logger=None):
        """Creator class for digital elevation models based on ASTER or SRTM.

        :param dem_sensor:  'SRTM' or 'ASTER'
        :param db_conn:     database connection string
        """
        if dem_sensor not in ['SRTM', 'ASTER']:
            raise ValueError('%s is not a supported DEM sensor. Choose between SRTM and ASTER (both 30m native GSD).'
                             % dem_sensor)

        self.dem_sensor = dem_sensor
        self.db_conn = db_conn if db_conn else CFG.conn_database
        self.logger = logger or logging.getLogger('DEM_Creator')

        self.project_dir = os.path.abspath(os.path.curdir)
        self.rootpath_DEMs = ''
        self.imNames = []
        self.dsID_dic = dict(ASTER=2, SRTM=225)
        self.DEM = None

    def __getstate__(self):
        """Defines how the attributes of DEM_Creator are pickled."""

        if self.logger not in [None, 'not set']:
            close_logger(self.logger)
            self.logger = None
        return self.__dict__

    def __del__(self):
        close_logger(self.logger)
        self.logger = None

    @staticmethod
    def _get_corner_coords_lonlat(cornerCoords_tgt, prj):
        # transform to Longitude/Latitude coordinates
        tgt_corner_coord_lonlat = [transform_any_prj(prj, 4326, X, Y) for X, Y in cornerCoords_tgt]

        # handle coordinates crossing the 180 degrees meridian
        xvals = [x for x, y in tgt_corner_coord_lonlat]
        if max(xvals) - min(xvals) > 180:
            tgt_corner_coord_lonlat = [(x, y) if x > 0 else (x + 360, y) for x, y in tgt_corner_coord_lonlat]

        return tgt_corner_coord_lonlat

    def get_overlapping_DEM_tiles(self, tgt_corner_coord_lonlat, timeout_sec=30, use_index_mediator=True):
        # type: (List[Tuple], int, bool) -> list
        """Get the overlapping DEM tiles for the given extent.

        :param tgt_corner_coord_lonlat: list of longitude/latitude target coordinates [[X,Y], [X,Y], ...]]
        :param timeout_sec:             database query timeout (seconds)
        :param use_index_mediator:      whether to use or not to use the SpatialIndexMediator (default: True)
        :return: list of matching DEM tile scene IDs
        """
        if use_index_mediator:
            SpIM = SpatialIndexMediator(host=CFG.spatial_index_server_host, port=CFG.spatial_index_server_port,
                                        timeout=timeout_sec, retries=10)
            with DatabaseLock(allowed_slots=1, logger=self.logger):
                scenes = SpIM.getFullSceneDataForDataset(envelope=corner_coord_to_minmax(tgt_corner_coord_lonlat),
                                                         timeStart=datetime(1970, 1, 1, 0, 0, 0),
                                                         timeEnd=datetime(2100, 12, 31, 0, 0, 0),
                                                         minCloudCover=0, maxCloudCover=100,
                                                         datasetid=self.dsID_dic[self.dem_sensor])
            sceneIDs_srtm = [scene.sceneid for scene in scenes]

        else:
            sceneIDs_srtm = get_overlapping_scenes_from_postgreSQLdb(self.db_conn,
                                                                     table='scenes',
                                                                     tgt_corners_lonlat=tgt_corner_coord_lonlat,
                                                                     conditions=['datasetid=%s'
                                                                                 % self.dsID_dic[self.dem_sensor]],
                                                                     timeout=timeout_sec*1000)  # milliseconds
            sceneIDs_srtm = [i[0] for i in sceneIDs_srtm]

        return sceneIDs_srtm

    def _get_DEMPathes_to_include(self, tgt_corner_coord_lonlat, timeout_sec=30):
        # type: (List[Tuple], int) -> list
        """Return the paths of DEM files to merge in order to generate a DEM covering the given area of interest.

        :param tgt_corner_coord_lonlat:     list of longitude/latitude target coordinates [(X,Y), (X,Y), ...]]
        :param timeout_sec:                 database query timeout (seconds)
        :return: list of GDAL readable paths
        """
        # get overlapping SRTM scene IDs from GMS database
        try:
            # try to use the SpatialIndexMediator
            # noinspection PyBroadException
            try:
                sceneIDs_srtm = self.get_overlapping_DEM_tiles(tgt_corner_coord_lonlat, timeout_sec)
            except ConnectionRefusedError:
                # fallback to plain pgSQL
                self.logger.warning('SpatialIndexMediator refused connection. Falling back to plain postgreSQL query.')
                sceneIDs_srtm = self.get_overlapping_DEM_tiles(tgt_corner_coord_lonlat, use_index_mediator=False)
            except Exception as err:
                # fallback to plain pgSQL
                self.logger.warning('Error while running SpatialIndexMediator database query. '
                                    'Falling back to plain postgreSQL query. '
                                    'Error message was: %s' % str(repr(err)))
                sceneIDs_srtm = self.get_overlapping_DEM_tiles(tgt_corner_coord_lonlat, use_index_mediator=False)

            if not sceneIDs_srtm:
                # fallback to plain pgSQL
                self.logger.warning('SpatialIndexMediator did not return matching DEM tiles. '
                                    'Trying plain postgreSQL query..')
                sceneIDs_srtm = self.get_overlapping_DEM_tiles(tgt_corner_coord_lonlat, use_index_mediator=False)

        except TimeoutError:
            raise TimeoutError('Spatial database query for %s DEM generation timed out after %s seconds.'
                               % (self.dem_sensor, timeout_sec))

        if not sceneIDs_srtm:
            raise RuntimeError('No matching %s scene IDs for DEM generation found.' % self.dem_sensor)

        # get corresponding filenames on disk and generate GDALvsiPathes pointing to raster files within archives
        archivePaths = [path_generator(scene_ID=ID).get_local_archive_path_baseN() for ID in sceneIDs_srtm]
        self.rootpath_DEMs = os.path.dirname(archivePaths[0])
        imNameMatchExp = '*.bil' if self.dem_sensor == 'SRTM' else '*dem.tif'
        self.imNames = [fnmatch.filter(HLP_F.get_zipfile_namelist(aP), imNameMatchExp)[0] for aP in archivePaths]
        gdalImPaths = [os.path.join(HLP_F.convert_absPathArchive_to_GDALvsiPath(aP), bN)
                       for aP, bN in zip(archivePaths, self.imNames)]

        return gdalImPaths

    def _run_cmd(self, cmd):
        output, exitcode, err = HLP_F.subcall_with_output(cmd)
        if exitcode:
            self.logger.error('\nAn error occurred during DEM creation.')
            self.logger.warning("Print traceback in case you care:")
            self.logger.warning(err.decode('latin-1'))
        if output:
            return output.decode('UTF-8')

    def from_extent(self, cornerCoords_tgt, prj, tgt_xgsd, tgt_ygsd):
        """Returns a GeoArray of a DEM according to the given target coordinates

        :param cornerCoords_tgt:    list of target coordinates [[X,Y], [X,Y], ...]] (at least 2 coordinates)
        :param prj:                 WKT string of the projection belonging cornerCoords_tgt
        :param tgt_xgsd:            output X GSD
        :param tgt_ygsd:            output Y GSD
        :return: DEM GeoArray
        """

        # generate at least 4 coordinates in case less coords have been given in order to avoid nodata triangles in DEM
        if len(cornerCoords_tgt) < 4 and isProjectedOrGeographic(prj) == 'projected':
            co_yx = [(y, x) for x, y in cornerCoords_tgt]
            cornerCoords_tgt = boxObj(boxMapYX=co_yx).boxMapXY

        # handle coordinate infos
        tgt_corner_coord_lonlat = self._get_corner_coords_lonlat(cornerCoords_tgt, prj)

        # get GDAL readable pathes
        pathes = self._get_DEMPathes_to_include(tgt_corner_coord_lonlat)

        # Build GDAL VRT from pathes and create output DEM
        if not os.path.exists(CFG.path_tempdir):
            os.makedirs(CFG.path_tempdir)  # directory where tempfile is created must exist (CentOS)
        with tempFile(dir=CFG.path_tempdir, prefix='GeoMultiSens_', suffix='_dem_merged.vrt') as tFm, \
                tempFile(dir=CFG.path_tempdir, prefix='GeoMultiSens_', suffix='_dem_out.vrt') as tFo:

            try:
                os.chdir(self.rootpath_DEMs)

                # create a merged VRT of all input DEMs
                t_xmin, t_xmax, t_ymin, t_ymax = corner_coord_to_minmax(tgt_corner_coord_lonlat)
                self._run_cmd('gdalbuildvrt %s %s -te %s %s %s %s -vrtnodata 0'
                              % (tFm.name, ' '.join(pathes), t_xmin, t_ymin, t_xmax, t_ymax))

                # run gdalwarp to match target grid and extent
                merged_prj = GeoArray(tFm.name).prj
                t_xmin, t_xmax, t_ymin, t_ymax = corner_coord_to_minmax(cornerCoords_tgt)
                self._run_cmd('gdalwarp -r average -of VRT -srcnodata 0 -dstnodata 0 '
                              '-tr %s %s -s_srs EPSG:%s -t_srs EPSG:%s -te %s %s %s %s %s %s'
                              % (tgt_xgsd, tgt_ygsd, CRS(merged_prj).to_epsg(), CRS(prj).to_epsg(),
                                 t_xmin, t_ymin, t_xmax, t_ymax, tFm.name, tFo.name))
                assert os.path.exists(tFo.name)

                self.DEM = GeoArray(tFo.name).to_mem()

            finally:
                os.chdir(self.project_dir)

        return self.DEM
