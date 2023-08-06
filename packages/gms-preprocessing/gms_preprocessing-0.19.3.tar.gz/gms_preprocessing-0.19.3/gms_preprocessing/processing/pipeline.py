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

from typing import List, Tuple, Generator, Iterable, Union  # noqa F401  # flake8 issue
from psutil import virtual_memory

from ..options.config import GMS_config as CFG
from ..misc import exception_handler as EXC_H
from ..misc.path_generator import path_generator
from ..misc.logging import GMS_logger
from ..misc.locks import ProcessLock, MemoryReserver, redis_conn
from ..algorithms import L1A_P
from ..algorithms import L1B_P
from ..algorithms import L1C_P
from ..algorithms import L2A_P
from ..algorithms import L2B_P
from ..algorithms import L2C_P
from ..model.gms_object import \
    failed_GMS_object, update_proc_status, return_proc_reports_only, estimate_mem_usage
from ..model.gms_object import GMS_object  # noqa F401  # flake8 issue
from ..algorithms.geoprocessing import get_common_extent

__author__ = 'Daniel Scheffler'


@EXC_H.log_uncaught_exceptions
@update_proc_status
def L1A_map(dataset_dict):  # map (scene-wise parallelization)
    # type: (dict) -> L1A_P.L1A_object

    L1A_obj = L1A_P.L1A_object(**dataset_dict)
    L1A_obj.block_at_system_overload(max_usage=CFG.critical_mem_usage)
    L1A_obj.import_rasterdata()
    L1A_obj.import_metadata()
    L1A_obj.validate_GeoTransProj_GeoAlign()  # sets self.GeoTransProj_ok and self.GeoAlign_ok
    L1A_obj.apply_nodata_mask_to_ObjAttr('arr')  # nodata mask is automatically calculated
    L1A_obj.add_rasterInfo_to_MetaObj()
    L1A_obj.reference_data('UTM')
    L1A_obj.calc_TOARadRefTemp()
    L1A_obj.calc_corner_positions()  # requires mask_nodata
    L1A_obj.calc_center_AcqTime()  # (if neccessary); requires corner positions
    L1A_obj.calc_mean_VAA()
    L1A_obj.calc_orbit_overpassParams()  # requires corner positions
    L1A_obj.apply_nodata_mask_to_ObjAttr('mask_clouds', 0)

    if CFG.exec_L1AP[1]:
        L1A_obj.to_ENVI(CFG.write_ENVIclassif_cloudmask)
    L1A_obj.record_mem_usage()
    L1A_obj.delete_tempFiles()

    return L1A_obj


@EXC_H.log_uncaught_exceptions
@update_proc_status
def L1A_map_1(dataset_dict, block_size=None):  # map (scene-wise parallelization)
    # type: (dict, tuple) -> List[L1A_P.L1A_object]

    L1A_obj = L1A_P.L1A_object(**dataset_dict)
    L1A_obj.block_at_system_overload(max_usage=CFG.critical_mem_usage)
    L1A_obj.import_rasterdata()
    L1A_obj.import_metadata()
    L1A_obj.validate_GeoTransProj_GeoAlign()  # sets self.GeoTransProj_ok and self.GeoAlign_ok
    L1A_obj.apply_nodata_mask_to_ObjAttr('arr')  # nodata mask is automatically calculated
    L1A_obj.add_rasterInfo_to_MetaObj()
    L1A_obj.reference_data('UTM')
    tiles = [tile for tile in
             # cut (block-wise parallelization)
             L1A_obj.to_tiles(blocksize=block_size if block_size else CFG.tiling_block_size_XY)
             if tile is not None]    # None is returned in case the tile contains no data at all
    return tiles


@EXC_H.log_uncaught_exceptions
@update_proc_status
def L1A_map_2(L1A_tile):  # map (block-wise parallelization)
    # type: (L1A_P.L1A_object) -> L1A_P.L1A_object
    L1A_tile.calc_TOARadRefTemp()
    if not CFG.inmem_serialization:
        L1A_tile.to_ENVI(CFG.write_ENVIclassif_cloudmask, is_tempfile=True)
    return L1A_tile


@EXC_H.log_uncaught_exceptions
@update_proc_status
def L1A_map_3(L1A_obj):  # map (scene-wise parallelization)
    # type: (L1A_P.L1A_object) -> L1A_P.L1A_object
    L1A_obj.calc_corner_positions()  # requires mask_nodata
    L1A_obj.calc_center_AcqTime()  # (if neccessary); requires corner positions
    L1A_obj.calc_mean_VAA()
    L1A_obj.calc_orbit_overpassParams()  # requires corner positions
    L1A_obj.apply_nodata_mask_to_ObjAttr('mask_clouds', 0)
    if CFG.exec_L1AP[1]:
        L1A_obj.to_ENVI(CFG.write_ENVIclassif_cloudmask)
        L1A_obj.delete_tempFiles()
    else:
        L1A_obj.delete_tempFiles()
    L1A_obj.record_mem_usage()
    return L1A_obj


@EXC_H.log_uncaught_exceptions
@update_proc_status
def L1B_map(L1A_obj):
    # type: (L1A_P.L1A_object) -> L1B_P.L1B_object
    """L1A_obj enthält in Python- (im Gegensatz zur inmem_serialization-) Implementierung KEINE ARRAY-DATEN!,
    nur die für die ganze Szene gültigen Metadaten"""

    L1A_obj.block_at_system_overload(max_usage=CFG.critical_mem_usage)

    L1B_obj = L1B_P.L1B_object(L1A_obj)
    L1B_obj.compute_global_shifts()

    if CFG.exec_L1BP[1]:
        L1B_obj.to_ENVI(CFG.write_ENVIclassif_cloudmask)
    L1B_obj.record_mem_usage()
    L1B_obj.delete_tempFiles()
    return L1B_obj


@EXC_H.log_uncaught_exceptions
@update_proc_status
def L1C_map(L1B_objs):
    # type: (Iterable[L1B_P.L1B_object]) -> List[L1C_P.L1C_object]
    """Atmospheric correction.

    NOTE: all subsystems (containing all spatial samplings) belonging to the same scene ID are needed

    :param L1B_objs: list containing one or multiple L1B objects belonging to the same scene ID.
    """
    list(L1B_objs)[0].block_at_system_overload(max_usage=CFG.critical_mem_usage)

    # initialize L1C objects
    L1C_objs = [L1C_P.L1C_object(L1B_obj) for L1B_obj in L1B_objs]

    # check in config if atmospheric correction is desired
    if CFG.target_radunit_optical == 'BOA_Ref':
        # atmospheric correction (asserts that there is an ac_options.json file on disk for the current sensor)
        if L1C_objs[0].ac_options:
            # perform atmospheric correction
            L1C_objs = L1C_P.AtmCorr(*L1C_objs).run_atmospheric_correction(dump_ac_input=False)
        else:
            [L1C_obj.logger.warning('Atmospheric correction is not yet supported for %s %s and has been skipped.'
                                    % (L1C_obj.satellite, L1C_obj.sensor)) for L1C_obj in L1C_objs]
    else:
        [L1C_obj.logger.warning('Atmospheric correction skipped because optical conversion type is set to %s.'
                                % CFG.target_radunit_optical) for L1C_obj in L1C_objs]

    # write outputs and delete temporary data
    for L1C_obj in L1C_objs:
        if CFG.exec_L1CP[1]:
            L1C_obj.to_ENVI(CFG.write_ENVIclassif_cloudmask)
        if L1C_obj.arr_shape == 'cube':
            L1C_obj.delete_tempFiles()
        L1C_obj.delete_ac_input_arrays()

    [L1C_obj.record_mem_usage() for L1C_obj in L1C_objs]
    return L1C_objs


@EXC_H.log_uncaught_exceptions
@update_proc_status
def L2A_map(L1C_objs, block_size=None, return_tiles=True):
    # type: (Union[List[L1C_P.L1C_object], Tuple[L1C_P.L1C_object]], tuple, bool) -> Union[List[L2A_P.L2A_object], L2A_P.L2A_object]  # noqa
    """Geometric homogenization.

    Performs correction of geometric displacements, resampling to target grid of the usecase and merges multiple
    GMS objects belonging to the same scene ID (subsystems) to a single L2A object.
    NOTE: Output L2A_object must be cut into tiles because L2A_obj size in memory exceeds maximum serialization size.

    :param L1C_objs:        list containing one or multiple L1C objects belonging to the same scene ID.
    :param block_size:      X/Y size of output tiles in pixels, e.g. (1024,1024)
    :param return_tiles:    return computed L2A object in tiles
    :return:                list of L2A_object tiles
    """
    L1C_objs[0].block_at_system_overload(max_usage=CFG.critical_mem_usage)

    # initialize L2A objects
    L2A_objs = [L2A_P.L2A_object(L1C_obj) for L1C_obj in L1C_objs]

    # get common extent (NOTE: using lon/lat coordinates here would cause black borders around the UTM image
    #                          because get_common_extent() just uses the envelop without regard to the projection
    clip_extent = \
        get_common_extent([obj.trueDataCornerUTM for obj in L2A_objs]) \
        if len(L2A_objs) > 1 else L2A_objs[0].trueDataCornerUTM

    # correct geometric displacements and resample to target grid
    for L2A_obj in L2A_objs:
        L2A_obj.correct_spatial_shifts(cliptoextent=CFG.clip_to_extent,
                                       clipextent=clip_extent, clipextent_prj=L2A_obj.arr.prj)

    # merge multiple subsystems belonging to the same scene ID to a single GMS object
    if len(L2A_objs) > 1:
        L2A_obj = L2A_P.L2A_object.from_sensor_subsystems(L2A_objs)
    else:
        L2A_obj = L2A_objs[0]

        # update attributes
        L2A_obj.calc_mask_nodata(overwrite=True)
        L2A_obj.calc_corner_positions()

    # write output
    if CFG.exec_L2AP[1]:
        L2A_obj.to_ENVI(CFG.write_ENVIclassif_cloudmask)

    # delete tempfiles of separate subsystem GMS objects
    [L2A_obj.delete_tempFiles() for L2A_obj in L2A_objs]

    if return_tiles:
        L2A_tiles = list(L2A_obj.to_tiles(blocksize=block_size if block_size else CFG.tiling_block_size_XY))
        L2A_tiles = [i for i in L2A_tiles if i is not None]  # None is returned in case the tile contains no data at all
        [L2A_tile.record_mem_usage() for L2A_tile in L2A_tiles]
        return L2A_tiles
    else:
        L2A_obj.record_mem_usage()
        return L2A_obj


@EXC_H.log_uncaught_exceptions
@update_proc_status
def L2B_map(L2A_obj):
    # type: (L2A_P.L2A_object) -> L2B_P.L2B_object
    L2A_obj.block_at_system_overload(max_usage=CFG.critical_mem_usage)
    L2B_obj = L2B_P.L2B_object(L2A_obj)
    L2B_obj.spectral_homogenization()
    if CFG.exec_L2BP[1]:
        L2B_obj.to_ENVI(CFG.write_ENVIclassif_cloudmask)
    if L2B_obj.arr_shape == 'cube':
        L2B_obj.delete_tempFiles()
    L2B_obj.record_mem_usage()
    return L2B_obj


@EXC_H.log_uncaught_exceptions
@update_proc_status
def L2C_map(L2B_obj):
    # type: (L2B_P.L2B_object) -> L2C_P.L2C_object
    L2B_obj.block_at_system_overload(max_usage=CFG.critical_mem_usage)
    L2C_obj = L2C_P.L2C_object(L2B_obj)
    if CFG.exec_L2CP[1]:
        L2C_MRGS_tiles = L2C_obj.to_MGRS_tiles(pixbuffer=CFG.mgrs_pixel_buffer)
        [MGRS_tile.to_ENVI(CFG.write_ENVIclassif_cloudmask,
                           compression=CFG.output_data_compression) for MGRS_tile in L2C_MRGS_tiles]
    L2C_obj.record_mem_usage()
    L2C_obj.delete_tempFiles()
    return L2C_obj  # contains no array data in Python mode


@return_proc_reports_only
# @return_GMS_objs_without_arrays
def run_complete_preprocessing(list_dataset_dicts_per_scene):  # map (scene-wise parallelization)
    # type: (List[dict]) -> Union[L1A_P.GMS_object, List, Generator]
    """

    NOTE: Exceptions in this function are must be catched by calling function (process controller).

    :param list_dataset_dicts_per_scene:
    :return:
    """
    with GMS_logger('log__%s' % CFG.ID, fmt_suffix=list_dataset_dicts_per_scene[0]['scene_ID'],
                    log_level=CFG.log_level, append=True) as pipeline_logger:

        # set CPU and memory limits
        cpulimit = CFG.CPUs_all_jobs
        mem2reserve = 15

        if redis_conn:
            mem_estim = estimate_mem_usage(list_dataset_dicts_per_scene[0]['dataset_ID'],
                                           list_dataset_dicts_per_scene[0]['satellite'])
            if mem_estim:
                mem2reserve = mem_estim
            else:
                cpulimit = int((virtual_memory().total * .8 - virtual_memory().used) / 1024 ** 3 / mem2reserve)
                pipeline_logger.info('No memory usage statistics from earlier jobs found for the current '
                                     'configuration. Limiting processes to %s in order to collect memory statistics '
                                     'first.' % cpulimit)

        # start processing
        with MemoryReserver(mem2lock_gb=mem2reserve, logger=pipeline_logger, max_usage=CFG.max_mem_usage),\
                ProcessLock(allowed_slots=cpulimit, logger=pipeline_logger):

            if len(list(set([ds['proc_level'] for ds in list_dataset_dicts_per_scene]))) != 1:
                raise ValueError('Lists of subsystem datasets with different processing levels are not supported here. '
                                 'Received %s.' % list_dataset_dicts_per_scene)

            input_proc_level = list_dataset_dicts_per_scene[0]['proc_level']

            ##################
            # L1A processing #
            ##################

            L1A_objects = []
            if CFG.exec_L1AP[0] and input_proc_level is None:
                L1A_objects = \
                    [L1A_map(subsystem_dataset_dict) for subsystem_dataset_dict in list_dataset_dicts_per_scene]

                if any([isinstance(obj, failed_GMS_object) for obj in L1A_objects]):
                    return L1A_objects

            ##################
            # L1B processing #
            ##################

            # select subsystem with optimal band for co-registration
            # L1B_obj_coreg = L1B_map(L1A_objects[0])
            # copy coreg information to remaining subsets

            L1B_objects = L1A_objects
            if CFG.exec_L1BP[0]:
                # add earlier processed L1A data
                if input_proc_level == 'L1A':
                    for ds in list_dataset_dicts_per_scene:
                        GMSfile = path_generator(ds, proc_level='L1A').get_path_gmsfile()
                        L1A_objects.append(L1A_P.L1A_object.from_disk([GMSfile, ['cube', None]]))

                L1B_objects = [L1B_map(L1A_obj) for L1A_obj in L1A_objects]

                del L1A_objects

                if any([isinstance(obj, failed_GMS_object) for obj in L1B_objects]):
                    return L1B_objects

            ##################
            # L1C processing #
            ##################

            L1C_objects = L1B_objects
            if CFG.exec_L1CP[0]:
                # add earlier processed L1B data
                if input_proc_level == 'L1B':
                    for ds in list_dataset_dicts_per_scene:
                        GMSfile = path_generator(ds, proc_level='L1B').get_path_gmsfile()
                        L1B_objects.append(L1B_P.L1B_object.from_disk([GMSfile, ['cube', None]]))

                L1C_objects = L1C_map(L1B_objects)

                del L1B_objects

                if any([isinstance(obj, failed_GMS_object) for obj in L1C_objects]):
                    return L1C_objects

            if not CFG.exec_L2AP[0]:
                return L1C_objects

            ##################
            # L2A processing #
            ##################

            # add earlier processed L1C data
            if input_proc_level == 'L1C':
                for ds in list_dataset_dicts_per_scene:
                    GMSfile = path_generator(ds, proc_level='L1C').get_path_gmsfile()
                    L1C_objects.append(L1C_P.L1C_object.from_disk([GMSfile, ['cube', None]]))

            L2A_obj = L2A_map(L1C_objects, return_tiles=False)

            del L1C_objects

            if isinstance(L2A_obj, failed_GMS_object) or not CFG.exec_L2BP[0]:
                return L2A_obj

            ##################
            # L2B processing #
            ##################

            # add earlier processed L2A data
            if input_proc_level == 'L2A':
                assert len(list_dataset_dicts_per_scene) == 1, \
                    'Expected only a single L2A dataset since subsystems are merged.'
                GMSfile = path_generator(list_dataset_dicts_per_scene[0], proc_level='L2A').get_path_gmsfile()
                L2A_obj = L2A_P.L2A_object.from_disk([GMSfile, ['cube', None]])

            L2B_obj = L2B_map(L2A_obj)

            del L2A_obj

            if isinstance(L2B_obj, failed_GMS_object) or not CFG.exec_L2CP[0]:
                return L2B_obj

            ##################
            # L2C processing #
            ##################

            # add earlier processed L2B data
            if input_proc_level == 'L2B':
                assert len(list_dataset_dicts_per_scene) == 1, \
                    'Expected only a single L2B dataset since subsystems are merged.'
                GMSfile = path_generator(list_dataset_dicts_per_scene[0], proc_level='L2B').get_path_gmsfile()
                L2B_obj = L2B_P.L2B_object.from_disk([GMSfile, ['cube', None]])

            L2C_obj = L2C_map(L2B_obj)  # type: Union[GMS_object, failed_GMS_object, List]

            del L2B_obj

            return L2C_obj
