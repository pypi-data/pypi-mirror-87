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

"""
Level 1B Processor:

Detection of global/local geometric displacements.
"""


import collections
import os
import time
import warnings
from datetime import datetime, timedelta

import numpy as np
from geopandas import GeoDataFrame
from shapely.geometry import box
import pytz
import traceback
from typing import Union, TYPE_CHECKING  # noqa F401  # flake8 issue

from arosics import COREG, DESHIFTER
from geoarray import GeoArray
from py_tools_ds.geo.coord_grid import is_coord_grid_equal
from py_tools_ds.geo.coord_calc import corner_coord_to_minmax
from py_tools_ds.geo.coord_trafo import reproject_shapelyGeometry, transform_any_prj
from py_tools_ds.geo.projection import prj_equal, EPSG2WKT, WKT2EPSG
from py_tools_ds.geo.vector.topology import get_overlap_polygon

from ..options.config import GMS_config as CFG
from ..model.gms_object import GMS_object
from .L1A_P import L1A_object
from ..misc import database_tools as DB_T
from ..misc import helper_functions as HLP_F
from ..misc import path_generator as PG
from ..misc.logging import GMS_logger, close_logger
from ..misc.locks import DatabaseLock
from ..misc.spatial_index_mediator import SpatialIndexMediator
from ..misc.definition_dicts import get_GMS_sensorcode, get_outFillZeroSaturated

if TYPE_CHECKING:
    from shapely.geometry import Polygon  # noqa F401  # flake8 issue
    from logging import Logger  # noqa F401  # flake8 issue

__author__ = 'Daniel Scheffler'


class Scene_finder(object):
    """Scene_finder class to query the postgreSQL database to find a suitable reference scene for co-registration."""

    def __init__(self, src_boundsLonLat, src_AcqDate, src_prj, src_footprint_poly, sceneID_excluded=None,
                 min_overlap=20, min_cloudcov=0, max_cloudcov=20, plusminus_days=30, plusminus_years=10, logger=None):
        # type: (list, datetime, str, Polygon, int, int, int, int, int, int, Logger) -> None
        """Initialize Scene_finder.

        :param src_boundsLonLat:
        :param src_AcqDate:
        :param src_prj:
        :param src_footprint_poly:
        :param sceneID_excluded:
        :param min_overlap:         minimum overlap of reference scene in percent
        :param min_cloudcov:        minimum cloud cover of reference scene in percent
        :param max_cloudcov:        maximum cloud cover of reference scene in percent
        :param plusminus_days:      maximum time interval between target and reference scene in days
        :param plusminus_years:     maximum time interval between target and reference scene in years
        """
        self.boundsLonLat = src_boundsLonLat
        self.src_AcqDate = src_AcqDate
        self.src_prj = src_prj
        self.src_footprint_poly = src_footprint_poly
        self.sceneID_excluded = sceneID_excluded
        self.min_overlap = min_overlap
        self.min_cloudcov = min_cloudcov
        self.max_cloudcov = max_cloudcov
        self.plusminus_days = plusminus_days
        self.plusminus_years = plusminus_years
        self.logger = logger or GMS_logger('ReferenceSceneFinder')

        # get temporal constraints
        def add_years(dt, years): return dt.replace(dt.year + years) \
            if not (dt.month == 2 and dt.day == 29) else dt.replace(dt.year + years, 3, 1)
        self.timeStart = add_years(self.src_AcqDate, -plusminus_years)
        timeEnd = add_years(self.src_AcqDate, +plusminus_years)
        timeNow = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.timeEnd = timeEnd if timeEnd <= timeNow else timeNow

        self.possib_ref_scenes = None  # set by self.spatial_query()
        self.GDF_ref_scenes = GeoDataFrame()  # set by self.spatial_query()
        self.ref_scene = None

    def __getstate__(self):
        """Defines how the attributes of Scene_finder instances are pickled."""
        close_logger(self.logger)
        self.logger = None

        return self.__dict__

    def __del__(self):
        close_logger(self.logger)
        self.logger = None

    def spatial_query(self, timeout=5):
        """Query the postgreSQL database to find possible reference scenes matching the specified criteria.

        :param timeout:     maximum query duration allowed (seconds)
        """
        SpIM = SpatialIndexMediator(host=CFG.spatial_index_server_host, port=CFG.spatial_index_server_port,
                                    timeout=timeout, retries=10)
        with DatabaseLock(allowed_slots=1, logger=self.logger):
            self.possib_ref_scenes = SpIM.getFullSceneDataForDataset(envelope=self.boundsLonLat,
                                                                     timeStart=self.timeStart,
                                                                     timeEnd=self.timeEnd,
                                                                     minCloudCover=self.min_cloudcov,
                                                                     maxCloudCover=self.max_cloudcov,
                                                                     datasetid=CFG.datasetid_spatial_ref,
                                                                     refDate=self.src_AcqDate,
                                                                     maxDaysDelta=self.plusminus_days)

        if self.possib_ref_scenes:
            # fill GeoDataFrame with possible ref scene parameters
            GDF = GeoDataFrame(self.possib_ref_scenes, columns=['object'])
            GDF['sceneid'] = list(GDF['object'].map(lambda scene: scene.sceneid))
            GDF['acquisitiondate'] = list(GDF['object'].map(lambda scene: scene.acquisitiondate))
            GDF['cloudcover'] = list(GDF['object'].map(lambda scene: scene.cloudcover))
            GDF['polyLonLat'] = list(GDF['object'].map(lambda scene: scene.polyLonLat))

            def LonLat2UTM(polyLL):
                return reproject_shapelyGeometry(polyLL, 4326, self.src_prj)

            GDF['polyUTM'] = list(GDF['polyLonLat'].map(LonLat2UTM))
            self.GDF_ref_scenes = GDF

    def _collect_refscene_metadata(self):
        """Collect some reference scene metadata needed for later filtering."""
        GDF = self.GDF_ref_scenes

        # get overlap parameter
        def get_OL_prms(poly): return get_overlap_polygon(poly, self.src_footprint_poly)

        GDF['overlapParams'] = list(GDF['polyLonLat'].map(get_OL_prms))
        GDF['overlap area'] = list(GDF['overlapParams'].map(lambda OL_prms: OL_prms['overlap area']))
        GDF['overlap percentage'] = list(GDF['overlapParams'].map(lambda OL_prms: OL_prms['overlap percentage']))
        GDF['overlap poly'] = list(GDF['overlapParams'].map(lambda OL_prms: OL_prms['overlap poly']))
        del GDF['overlapParams']

        # get processing level of reference scenes
        procL = GeoDataFrame(
            DB_T.get_info_from_postgreSQLdb(CFG.conn_database, 'scenes_proc', ['sceneid', 'proc_level'],
                                            {'sceneid': list(GDF.sceneid)}), columns=['sceneid', 'proc_level'])
        GDF = GDF.merge(procL, on='sceneid', how='left')
        GDF = GDF.where(GDF.notnull(), None)  # replace NaN values with None

        # get path of binary file
        def get_path_binary(GDF_row):
            return PG.path_generator(scene_ID=GDF_row['sceneid'], proc_level=GDF_row['proc_level']) \
                .get_path_imagedata() if GDF_row['proc_level'] else None
        GDF['path_ref'] = GDF.apply(lambda GDF_row: get_path_binary(GDF_row), axis=1)
        GDF['refDs_exists'] = list(GDF['path_ref'].map(lambda p: os.path.exists(p) if p else False))

        # check if a proper entity ID can be gathered from database
        eID = GeoDataFrame(DB_T.get_info_from_postgreSQLdb(CFG.conn_database, 'scenes', ['id', 'entityid'],
                                                           {'id': list(GDF.sceneid)}), columns=['sceneid', 'entityid'])
        GDF = GDF.merge(eID, on='sceneid', how='left')
        self.GDF_ref_scenes = GDF.where(GDF.notnull(), None)

    def _filter_excluded_sceneID(self):
        """Filter reference scene with the same scene ID like the target scene."""
        GDF = self.GDF_ref_scenes
        if not GDF.empty:
            self.logger.info('Same ID filter:  Excluding scene with the same ID like the target scene.')
            self.GDF_ref_scenes = GDF.loc[GDF['sceneid'] != self.sceneID_excluded]
            self.logger.info('%s scenes => %s scenes' % (len(GDF), len(self.GDF_ref_scenes)))

    def _filter_by_overlap(self):
        """Filter all scenes with less spatial overlap than self.min_overlap."""
        GDF = self.GDF_ref_scenes
        if not GDF.empty:
            self.logger.info('Overlap filter:  Excluding all scenes with less than %s percent spatial overlap.'
                             % self.min_overlap)
            self.GDF_ref_scenes = GDF.loc[GDF['overlap percentage'] >= self.min_overlap]
            self.logger.info('%s scenes => %s scenes' % (len(GDF), len(self.GDF_ref_scenes)))

    def _filter_by_proc_status(self):
        """Filter all scenes that have not been processed before according to proc. status (at least L1A is needed)."""
        GDF = self.GDF_ref_scenes
        if not GDF.empty:
            self.logger.info('Processing level filter:  Exclude all scenes that have not been processed before '
                             'according to processing status (at least L1A is needed).')
            self.GDF_ref_scenes = GDF[GDF['proc_level'].notnull()]
            self.logger.info('%s scenes => %s scenes' % (len(GDF), len(self.GDF_ref_scenes)))

    def _filter_by_dataset_existence(self):
        """Filter all scenes where no processed data can be found on fileserver."""
        GDF = self.GDF_ref_scenes
        if not GDF.empty:
            self.logger.info('Existence filter:  Excluding all scenes where no processed data have been found.')
            self.GDF_ref_scenes = GDF[GDF['refDs_exists']]
            self.logger.info('%s scenes => %s scenes' % (len(GDF), len(self.GDF_ref_scenes)))

    def _filter_by_entity_ID_availability(self):
        """Filter all scenes where no proper entity ID can be found in the database (database errors)."""
        GDF = self.GDF_ref_scenes
        if not GDF.empty:
            self.logger.info('DB validity filter:  Exclude all scenes where no proper entity ID can be found in the '
                             'database (database errors).')
            self.GDF_ref_scenes = GDF[GDF['entityid'].notnull()]
            self.logger.info('%s scenes => %s scenes' % (len(GDF), len(self.GDF_ref_scenes)))

    def _filter_by_projection(self):
        """Filter all scenes that have a different projection than the target image."""
        GDF = self.GDF_ref_scenes[self.GDF_ref_scenes.refDs_exists]
        if not GDF.empty:
            # compare projections of target and reference image
            GDF['prj_equal'] = \
                list(GDF['path_ref'].map(lambda path_ref: prj_equal(self.src_prj, GeoArray(path_ref).prj)))

            self.logger.info('Projection filter:  Exclude all scenes that have a different projection than the target '
                             'image.')
            self.GDF_ref_scenes = GDF[GDF['prj_equal']]
            self.logger.info('%s scenes => %s scenes' % (len(GDF), len(self.GDF_ref_scenes)))

    def choose_ref_scene(self):
        """Choose reference scene with minimum cloud cover and maximum overlap."""
        if self.possib_ref_scenes:
            # First, collect some relavant reference scene metadata
            self._collect_refscene_metadata()

            # Filter possible scenes by running all filter functions
            self._filter_excluded_sceneID()
            self._filter_by_overlap()
            self._filter_by_proc_status()
            self._filter_by_dataset_existence()
            self._filter_by_entity_ID_availability()
            self._filter_by_projection()

        # Choose the reference scene out of the filtered DataFrame
        if not self.GDF_ref_scenes.empty:
            GDF = self.GDF_ref_scenes
            GDF = GDF[GDF['cloudcover'] == GDF['cloudcover'].min()]
            GDF = GDF[GDF['overlap percentage'] == GDF['overlap percentage'].max()]

            if not GDF.empty:
                GDF_res = GDF.iloc[0]
                return ref_Scene(GDF_res)
        else:
            return None


class ref_Scene:
    def __init__(self, GDF_record):
        self.scene_ID = int(GDF_record['sceneid'])
        self.entity_ID = GDF_record['entityid']
        self.AcqDate = GDF_record['acquisitiondate']
        self.cloudcover = GDF_record['cloudcover']
        self.polyLonLat = GDF_record['polyLonLat']
        self.polyUTM = GDF_record['polyUTM']
        self.proc_level = GDF_record['proc_level']
        self.filePath = GDF_record['path_ref']


class L1B_object(L1A_object):
    def __init__(self, L1A_obj=None):

        super(L1B_object, self).__init__()

        # set defaults
        self._spatRef_available = None
        self.spatRef_scene = None  # set by self.get_spatial_reference_scene()
        self.deshift_results = collections.OrderedDict()

        if L1A_obj:
            # populate attributes
            [setattr(self, key, value) for key, value in L1A_obj.__dict__.items()]

        self.proc_level = 'L1B'
        self.proc_status = 'initialized'

    @property
    def spatRef_available(self):
        if self._spatRef_available is not None:
            return self._spatRef_available
        else:
            self.get_spatial_reference_scene()
            return self._spatRef_available

    @spatRef_available.setter
    def spatRef_available(self, spatRef_available):
        self._spatRef_available = spatRef_available

    def get_spatial_reference_scene(self):
        boundsLonLat = corner_coord_to_minmax(self.trueDataCornerLonLat)
        footprint_poly = HLP_F.CornerLonLat_to_shapelyPoly(self.trueDataCornerLonLat)
        RSF = Scene_finder(boundsLonLat, self.acq_datetime, self.MetaObj.projection,
                           footprint_poly, self.scene_ID,
                           min_overlap=CFG.spatial_ref_min_overlap,
                           min_cloudcov=CFG.spatial_ref_min_cloudcov,
                           max_cloudcov=CFG.spatial_ref_max_cloudcov,
                           plusminus_days=CFG.spatial_ref_plusminus_days,
                           plusminus_years=CFG.spatial_ref_plusminus_years,
                           logger=self.logger)

        # run spatial query
        self.logger.info('Querying database in order to find a suitable reference scene for co-registration.')
        RSF.spatial_query(timeout=5)
        if RSF.possib_ref_scenes:
            self.logger.info('Query result: %s reference scenes with matching metadata.' % len(RSF.possib_ref_scenes))

            # try to get a spatial reference scene by applying some filter criteria
            self.spatRef_scene = RSF.choose_ref_scene()  # type: Union[ref_Scene, None]
            if self.spatRef_scene:
                self.spatRef_available = True
                self.logger.info('Found a suitable reference image for coregistration: scene ID %s (entity ID %s).'
                                 % (self.spatRef_scene.scene_ID, self.spatRef_scene.entity_ID))
            else:
                self.spatRef_available = False
                self.logger.warning('No scene fulfills all requirements to serve as spatial reference for scene %s '
                                    '(entity ID %s). Coregistration impossible.' % (self.scene_ID, self.entity_ID))

        else:
            self.logger.warning('Spatial query returned no matches. Coregistration impossible.')
            self.spatRef_available = False

    def _get_reference_image_params_pgSQL(self):
        # TODO implement earlier version of this function as a backup for SpatialIndexMediator
        """postgreSQL query: get IDs of overlapping scenes and select most suitable scene_ID
            (with respect to DGM, cloud cover"""
        warnings.warn('_get_reference_image_params_pgSQL is deprecated an will not work anymore.', DeprecationWarning)

        # vorab-check anhand wolkenmaske, welche region von im2shift überhaupt für shift-corr tauglich ist
        # -> diese region als argument in postgresql abfrage
        # scene_ID            = 14536400 # LE71510322000093SGS00 im2shift

        # set query conditions
        min_overlap = 20  # %
        max_cloudcov = 20  # %
        plusminus_days = 30
        AcqDate = self.im2shift_objDict['acquisition_date']
        date_minmax = [AcqDate - timedelta(days=plusminus_days), AcqDate + timedelta(days=plusminus_days)]
        dataset_cond = 'datasetid=%s' % CFG.datasetid_spatial_ref
        cloudcov_cond = 'cloudcover < %s' % max_cloudcov
        # FIXME cloudcover noch nicht für alle scenes im proc_level METADATA verfügbar
        dayrange_cond = "(EXTRACT(MONTH FROM scenes.acquisitiondate), EXTRACT(DAY FROM scenes.acquisitiondate)) " \
                        "BETWEEN (%s, %s) AND (%s, %s)" \
                        % (date_minmax[0].month, date_minmax[0].day, date_minmax[1].month, date_minmax[1].day)
        # TODO weitere Kriterien einbauen!

        def query_scenes(condlist):
            return DB_T.get_overlapping_scenes_from_postgreSQLdb(
                CFG.conn_database,
                table='scenes',
                tgt_corners_lonlat=self.trueDataCornerLonLat,
                conditions=condlist,
                add_cmds='ORDER BY scenes.cloudcover ASC',
                timeout=30000)
        conds_descImportance = [dataset_cond, cloudcov_cond, dayrange_cond]

        self.logger.info('Querying database in order to find a suitable reference scene for co-registration.')

        count, filt_overlap_scenes = 0, []
        while not filt_overlap_scenes:
            if count == 0:
                # search within already processed scenes
                # das ist nur Ergebnis aus scenes_proc
                # -> dort liegt nur eine referenz, wenn die szene schon bei CFG.job-Beginn in Datensatzliste drin war
                res = DB_T.get_overlapping_scenes_from_postgreSQLdb(
                    CFG.conn_database,
                    tgt_corners_lonlat=self.trueDataCornerLonLat,
                    conditions=['datasetid=%s' % CFG.datasetid_spatial_ref],
                    add_cmds='ORDER BY scenes.cloudcover ASC',
                    timeout=25000)
                filt_overlap_scenes = self._sceneIDList_to_filt_overlap_scenes([i[0] for i in res[:50]], 20.)

            else:
                # search within complete scenes table using less filter criteria with each run
                # TODO: Daniels Index einbauen, sonst  bei wachsender Tabellengröße evtl. irgendwann zu langsam
                res = query_scenes(conds_descImportance)
                filt_overlap_scenes = self._sceneIDList_to_filt_overlap_scenes([i[0] for i in res[:50]], min_overlap)

                if len(conds_descImportance) > 1:  # FIXME anderer Referenzsensor?
                    del conds_descImportance[-1]
                else:  # reduce min_overlap to 10 percent if there are overlapping scenes
                    if res:
                        min_overlap = 10
                        filt_overlap_scenes = \
                            self._sceneIDList_to_filt_overlap_scenes([i[0] for i in res[:50]], min_overlap)

                    # raise warnings if no match found
                    if not filt_overlap_scenes:
                        if not res:
                            warnings.warn('No reference scene found for %s (scene ID %s). Coregistration of this scene '
                                          'failed.' % (self.baseN, self.scene_ID))
                        else:
                            warnings.warn('Reference scenes for %s (scene ID %s) have been found but none has more '
                                          'than %s percent overlap. Coregistration of this scene failed.'
                                          % (self.baseN, self.scene_ID, min_overlap))
                        break
            count += 1

        if filt_overlap_scenes:
            ref_available = False
            for count, sc in enumerate(filt_overlap_scenes):
                if count == 2:  # FIXME Abbuch schon bei 3. Szene?
                    warnings.warn('No reference scene for %s (scene ID %s) available. '
                                  'Coregistration of this scene failed.' % (self.baseN, self.scene_ID))
                    break

                # start download of scene data not available and start L1A processing
                def dl_cmd(scene_ID): print('%s %s %s' % (
                    CFG.java_commands['keyword'].strip(),  # FIXME CFG.java_commands is deprecated
                    CFG.java_commands["value_download"].strip(), scene_ID))

                path = PG.path_generator(scene_ID=sc['scene_ID']).get_path_imagedata()

                if not os.path.exists(path):
                    # add scene 2 download to scenes_jobs.missing_scenes

                    # print JAVA download command
                    t_dl_start = time.time()
                    dl_cmd(sc['scene_ID'])

                    # check if scene is downloading
                    download_start_timeout = 5  # seconds
                    # set timout for external processing
                    # -> DEPRECATED BECAUSE CREATION OF EXTERNAL CFG WITHIN CFG IS NOT ALLOWED
                    processing_timeout = 5  # seconds # FIXME increase timeout if processing is really started
                    proc_level = None
                    while True:
                        proc_level_chk = DB_T.get_info_from_postgreSQLdb(
                            CFG.conn_database, 'scenes', ['proc_level'], {'id': sc['scene_ID']})[0][0]
                        if proc_level != proc_level_chk:
                            print('Reference scene %s, current processing level: %s' % (sc['scene_ID'], proc_level_chk))
                        proc_level = proc_level_chk
                        if proc_level_chk in ['SCHEDULED', 'METADATA'] and \
                           time.time() - t_dl_start >= download_start_timeout:
                            warnings.warn('Download of reference scene %s (entity ID %s) timed out. '
                                          'Coregistration of this scene failed.' % (self.baseN, self.scene_ID))
                            break
                        if proc_level_chk == 'L1A':
                            ref_available = True
                            break
                        elif proc_level_chk == 'DOWNLOADED' and time.time() - t_dl_start >= processing_timeout:
                            # proc_level='DOWNLOADED' but scene has not been processed
                            warnings.warn('L1A processing of reference scene %s (entity ID %s) timed out. '
                                          'Coregistration of this scene failed.' % (self.baseN, self.scene_ID))
                            break
                            # DB_T.set_info_in_postgreSQLdb(CFG.conn_database,'scenes',
                            #                             {'proc_level':'METADATA'},{'id':sc['scene_ID']})

                        time.sleep(5)
                else:
                    ref_available = True

                if not ref_available:
                    continue
                else:
                    self.path_imref = path
                    self.imref_scene_ID = sc['scene_ID']
                    self.imref_footprint_poly = sc['scene poly']
                    self.overlap_poly = sc['overlap poly']
                    self.overlap_percentage = sc['overlap percentage']
                    self.overlap_area = sc['overlap area']

                    query_res = DB_T.get_info_from_postgreSQLdb(CFG.conn_database, 'scenes', ['entityid'],
                                                                {'id': self.imref_scene_ID}, records2fetch=1)
                    assert query_res != [], 'No entity-ID found for scene number %s' % self.imref_scene_ID
                    self.imref_entity_ID = query_res[0][0]  # [('LC81510322013152LGN00',)]
                    break
        self.logger.close()

    def _sceneIDList_to_filt_overlap_scenes(self, sceneIDList, min_overlap):
        """find reference scenes that cover at least 20% of the scene with the given ID
        ONLY FIRST 50 scenes are considered"""

        # t0 = time.time()
        dict_sceneID_poly = [{'scene_ID': ID, 'scene poly': HLP_F.scene_ID_to_shapelyPolygon(ID)}
                             for ID in sceneIDList]  # always returns LonLot polygons

        # get overlap polygons and their parameters. result: [{overlap poly, overlap percentage, overlap area}]
        for dic in dict_sceneID_poly:  # input: dicts {scene_ID, ref_poly}
            dict_overlap_poly_params = get_overlap_polygon(dic['scene poly'], self.arr.footprint_poly)
            dic.update(dict_overlap_poly_params)  # adds {overlap poly, overlap percentage, overlap area}
        # print('polygon creation time', time.time()-t0)

        # filter those scene_IDs out where overlap percentage is below 20%
        if min_overlap:
            filt_overlap_scenes = [scene for scene in dict_sceneID_poly if scene['overlap percentage'] >= min_overlap]
        else:
            filt_overlap_scenes = dict_sceneID_poly

        return filt_overlap_scenes

    def get_opt_bands4matching(self, target_cwlPos_nm=550):
        """Automatically determines the optimal bands used für fourier shift theorem matching

        :param target_cwlPos_nm:   the desired wavelength used for matching
        """
        # get GMS_object for reference scene
        path_gmsFile = PG.path_generator(scene_ID=self.spatRef_scene.scene_ID).get_path_gmsfile()
        ref_obj = GMS_object.from_disk((path_gmsFile, ['cube', None]))

        # get spectral characteristics
        ref_cwl = [float(ref_obj.MetaObj.CWL[bN]) for bN in ref_obj.MetaObj.LayerBandsAssignment]
        shift_cwl = [float(self.MetaObj.CWL[bN]) for bN in self.MetaObj.LayerBandsAssignment]
        shift_fwhm = [float(self.MetaObj.FWHM[bN]) for bN in self.MetaObj.LayerBandsAssignment]

        # exclude cirrus/oxygen band of Landsat-8/Sentinel-2
        shift_bbl, ref_bbl = [False] * len(shift_cwl), [False] * len(ref_cwl)  # bad band lists
        for GMS_obj, s_r, bbl in zip([self, ref_obj], ['shift', 'ref'], [shift_bbl, ref_bbl]):
            GMS_obj.GMS_identifier.logger = None  # set a dummy value in order to avoid Exception
            sensorcode = get_GMS_sensorcode(GMS_obj.GMS_identifier)
            if sensorcode in ['LDCM', 'S2A', 'S2B'] and '9' in GMS_obj.LayerBandsAssignment:
                bbl[GMS_obj.LayerBandsAssignment.index('9')] = True
            if sensorcode in ['S2A', 'S2B'] and '10' in GMS_obj.LayerBandsAssignment:
                bbl[GMS_obj.LayerBandsAssignment.index('10')] = True

        # cwl_overlap = (max(min(shift_cwl),min(ref_cwl)),  min(max(shift_cwl),max(ref_cwl))) # -> (min wvl, max wvl)
        # find matching band of reference image for each band of image to be shifted
        match_dic = collections.OrderedDict()
        for idx, cwl, fwhm in zip(range(len(shift_cwl)), shift_cwl, shift_fwhm):
            if shift_bbl[idx]:
                continue  # skip cwl if it is declared as bad band above

            def is_inside(r_cwl, s_cwl, s_fwhm): return s_cwl - s_fwhm / 2 < r_cwl < s_cwl + s_fwhm / 2

            matching_r_cwls = [r_cwl for i, r_cwl in enumerate(ref_cwl) if
                               is_inside(r_cwl, cwl, fwhm) and not ref_bbl[i]]
            if matching_r_cwls:
                match_dic[cwl] = matching_r_cwls[0] if len(matching_r_cwls) else \
                    matching_r_cwls[np.abs(np.array(matching_r_cwls) - cwl).argmin()]

        # set bands4 match based on the above results
        poss_cwls = [cwl for cwl in shift_cwl if cwl in match_dic]
        if poss_cwls:
            if not target_cwlPos_nm:
                shift_band4match = shift_cwl.index(poss_cwls[0]) + 1  # first possible shift band
                ref_band4match = ref_cwl.index(match_dic[poss_cwls[0]]) + 1  # matching reference band
            else:  # target_cwlPos is given
                closestWvl_to_target = poss_cwls[np.abs(np.array(poss_cwls) - target_cwlPos_nm).argmin()]
                shift_band4match = shift_cwl.index(closestWvl_to_target) + 1  # the shift band closest to target
                ref_band4match = ref_cwl.index(match_dic[closestWvl_to_target]) + 1  # matching ref
        else:  # all reference bands are outside of shift-cwl +- fwhm/2
            self.logger.warning('Optimal bands for matching could not be automatically determined. '
                                'Choosing first band of each image.')
            shift_band4match = 1
            ref_band4match = 1

        self.logger.info(
            'Target band for matching:    %s (%snm)' % (shift_band4match, shift_cwl[shift_band4match - 1]))
        self.logger.info(
            'Reference band for matching: %s (%snm)' % (ref_band4match, ref_cwl[ref_band4match - 1]))

        return ref_band4match, shift_band4match

    def compute_global_shifts(self):
        spatIdxSrv_status = os.environ['GMS_SPAT_IDX_SRV_STATUS'] if 'GMS_SPAT_IDX_SRV_STATUS' in os.environ else True

        if spatIdxSrv_status == 'unavailable':
            self.logger.warning('Coregistration skipped due to unavailable Spatial Index Mediator Server!"')

        elif CFG.skip_coreg:
            self.logger.warning('Coregistration skipped according to user configuration.')

        elif self.coreg_needed and self.spatRef_available:
            self.coreg_info.update({'reference scene ID': self.spatRef_scene.scene_ID})
            self.coreg_info.update({'reference entity ID': self.spatRef_scene.entity_ID})

            geoArr_ref = GeoArray(self.spatRef_scene.filePath)
            geoArr_shift = GeoArray(self.arr)
            r_b4match, s_b4match = self.get_opt_bands4matching(target_cwlPos_nm=CFG.coreg_band_wavelength_for_matching)
            coreg_kwargs = dict(
                r_b4match=r_b4match,
                s_b4match=s_b4match,
                align_grids=True,  # FIXME not needed here
                match_gsd=True,  # FIXME not needed here
                max_shift=CFG.coreg_max_shift_allowed,
                ws=CFG.coreg_window_size,
                data_corners_ref=[[x, y] for x, y in self.spatRef_scene.polyUTM.convex_hull.exterior.coords],
                data_corners_tgt=[transform_any_prj(EPSG2WKT(4326), self.MetaObj.projection, x, y)
                                  for x, y in HLP_F.reorder_CornerLonLat(self.trueDataCornerLonLat)],
                nodata=(get_outFillZeroSaturated(geoArr_ref.dtype)[0],
                        get_outFillZeroSaturated(geoArr_shift.dtype)[0]),
                ignore_errors=True,
                v=False,
                q=True
            )

            # initialize COREG object
            try:
                COREG_obj = COREG(geoArr_ref, geoArr_shift, **coreg_kwargs)
            except Exception as e:
                COREG_obj = None
                self.logger.error('\nAn error occurred during coregistration. BE AWARE THAT THE SCENE %s '
                                  '(ENTITY ID %s) HAS NOT BEEN COREGISTERED! Error message was: \n%s\n'
                                  % (self.scene_ID, self.entity_ID, repr(e)))
                self.logger.error(traceback.format_exc())
                # TODO include that in the job summary

            # calculate_spatial_shifts
            if COREG_obj:
                COREG_obj.calculate_spatial_shifts()

                self.coreg_info.update(
                    COREG_obj.coreg_info)  # no clipping to trueCornerLonLat until here -> only shift correction
                self.coreg_info.update({'shift_reliability': COREG_obj.shift_reliability})

                if COREG_obj.success:
                    self.coreg_info['success'] = True
                    self.logger.info("Calculated map shifts (X,Y): %s / %s"
                                     % (COREG_obj.x_shift_map,
                                        COREG_obj.y_shift_map))  # FIXME direkt in calculate_spatial_shifts loggen
                    self.logger.info("Reliability of calculated shift: %.1f percent" % COREG_obj.shift_reliability)

                else:
                    # TODO add database entry with error hint
                    [self.logger.error('ERROR during coregistration of scene %s (entity ID %s):\n%s'
                                       % (self.scene_ID, self.entity_ID, err)) for err in COREG_obj.tracked_errors]

        else:
            if self.coreg_needed:
                self.logger.warning('Coregistration skipped because no suitable reference scene is available or '
                                    'spatial query failed.')
            else:
                self.logger.info('Coregistration of scene %s (entity ID %s) skipped because target dataset ID equals '
                                 'reference dataset ID.' % (self.scene_ID, self.entity_ID))

    def correct_spatial_shifts(self, cliptoextent=True, clipextent=None, clipextent_prj=None, v=False):
        # type: (bool, list, any, bool) -> None
        """Corrects the spatial shifts calculated by self.compute_global_shifts().

        :param cliptoextent:    whether to clip the output to the given extent
        :param clipextent:      list of XY-coordinate tuples giving the target extent (if not given and cliptoextent is
                                True, the 'trueDataCornerLonLat' attribute of the GMS object is used
        :param clipextent_prj:  WKT projection string or EPSG code of the projection for the coordinates in clipextent
        :param v:
        :return:
        """

        # cliptoextent is automatically True if an extent is given
        cliptoextent = cliptoextent if not clipextent else True

        if cliptoextent or self.resamp_needed or (self.coreg_needed and self.coreg_info['success']):

            # get target bounds # TODO implement boxObj call instead here
            if not clipextent:
                trueDataCornerUTM = [transform_any_prj(EPSG2WKT(4326), self.MetaObj.projection, x, y)
                                     for x, y in self.trueDataCornerLonLat]
                xmin, xmax, ymin, ymax = corner_coord_to_minmax(trueDataCornerUTM)
                mapBounds = box(xmin, ymin, xmax, ymax).bounds
            else:
                assert clipextent_prj, \
                    "'clipextent_prj' must be given together with 'clipextent'. Received only 'clipextent'."
                clipextent_UTM = clipextent if prj_equal(self.MetaObj.projection, clipextent_prj) else \
                    [transform_any_prj(clipextent_prj, self.MetaObj.projection, x, y) for x, y in clipextent]
                xmin, xmax, ymin, ymax = corner_coord_to_minmax(clipextent_UTM)
                mapBounds = box(xmin, ymin, xmax, ymax).bounds

            # correct shifts and clip to extent
            # ensure self.masks exists (does not exist in case of inmem_serialization mode because
            # then self.fill_from_disk() is skipped)
            if not hasattr(self, 'masks') or self.masks is None:
                self.build_combined_masks_array()  # creates self.masks and self.masks_meta

            # exclude self.mask_nodata, self.mask_clouds from warping
            del self.mask_nodata, self.mask_clouds

            attributes2deshift = [attrname for attrname in
                                  ['arr', 'masks', 'dem', 'ac_errors', 'mask_clouds_confidence']
                                  if getattr(self, '_%s' % attrname) is not None]
            for attrname in attributes2deshift:
                geoArr = getattr(self, attrname)

                # do some logging
                if self.coreg_needed:
                    if self.coreg_info['success']:
                        self.logger.info("Correcting spatial shifts for attribute '%s'..." % attrname)
                    elif cliptoextent and is_coord_grid_equal(
                         geoArr.gt, CFG.spatial_ref_gridx, CFG.spatial_ref_gridy):
                        self.logger.info("Attribute '%s' has only been clipped to it's extent because no valid "
                                         "shifts have been detected and the pixel grid equals the target grid."
                                         % attrname)
                    elif self.resamp_needed:
                        self.logger.info("Resampling attribute '%s' to target grid..." % attrname)
                elif self.resamp_needed:
                    self.logger.info("Resampling attribute '%s' to target grid..." % attrname)

                # correct shifts
                DS = DESHIFTER(geoArr, self.coreg_info,
                               target_xyGrid=[CFG.spatial_ref_gridx, CFG.spatial_ref_gridy],
                               cliptoextent=cliptoextent,
                               clipextent=mapBounds,
                               align_grids=True,
                               resamp_alg='nearest' if attrname == 'masks' else CFG.spatial_resamp_alg,
                               CPUs=None if CFG.allow_subMultiprocessing else 1,
                               progress=True if v else False,
                               q=True,
                               v=v)
                DS.correct_shifts()

                # update coreg_info
                if attrname == 'arr':
                    self.coreg_info['is shifted'] = DS.is_shifted
                    self.coreg_info['is resampled'] = DS.is_resampled

                # update geoinformations and array shape related attributes
                self.logger.info("Updating geoinformations of '%s' attribute..." % attrname)
                if attrname == 'arr':
                    self.MetaObj.map_info = DS.updated_map_info
                    self.MetaObj.projection = EPSG2WKT(WKT2EPSG(DS.updated_projection))
                    self.shape_fullArr = DS.arr_shifted.shape
                    self.MetaObj.rows, self.MetaObj.cols = DS.arr_shifted.shape[:2]
                else:
                    self.masks_meta['map info'] = DS.updated_map_info
                    self.masks_meta['coordinate system string'] = EPSG2WKT(WKT2EPSG(DS.updated_projection))
                    self.masks_meta['lines'], self.masks_meta['samples'] = DS.arr_shifted.shape[:2]

                    # NOTE: mask_nodata and mask_clouds are updated later by L2A_map mapper function (module pipeline)

                # update the GeoArray instance without loosing its inherent metadata (nodata, ...)
                geoArr.arr, geoArr.gt = DS.GeoArray_shifted.arr, DS.GeoArray_shifted.gt
                if not geoArr.prj:
                    geoArr.prj = DS.GeoArray_shifted.prj
                # setattr(self,attrname, DS.GeoArray_shifted) # NOTE: don't set array earlier because setter will also
                #                                             # update arr.gt/.prj/.nodata from MetaObj

            self.resamp_needed = False
            self.coreg_needed = False

            # recreate self.masks_nodata and self.mask_clouds from self.masks
            self.mask_nodata = self.mask_nodata
            self.mask_clouds = self.mask_clouds
            # FIXME move functionality of self.masks only to output writer and remove self.masks completely
