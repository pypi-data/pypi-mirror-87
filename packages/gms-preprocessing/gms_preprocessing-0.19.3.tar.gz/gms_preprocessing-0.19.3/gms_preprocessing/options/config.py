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

import datetime
import socket
import os
import warnings
import numpy as np
import builtins
import re
import psycopg2
import psycopg2.extras
from collections import OrderedDict
from collections.abc import Mapping
import multiprocessing
from inspect import getargvalues, stack, signature, _empty
import json
from json import JSONDecodeError
from jsmin import jsmin
from cerberus import Validator
import pkgutil
import logging
import time
import psutil
from pprint import pformat
from typing import TYPE_CHECKING

from .options_schema import gms_schema_input, gms_schema_config_output, parameter_mapping, get_param_from_json_config
from ..version import __version__, __versionalias__

if TYPE_CHECKING:
    from gms_preprocessing.misc.database_tools import GMS_JOB  # noqa F401  # flake8 issue


__author__ = 'Daniel Scheffler'


class GMS_configuration(object):
    def __getattr__(self, attr):
        if hasattr(builtins, 'GMS_JobConfig'):
            if attr in ['job', 'usecase']:
                # This is only to keep compatibility with HU-INF codes
                return getattr(builtins, 'GMS_JobConfig')
            return getattr(builtins.GMS_JobConfig, attr)
        else:
            raise EnvironmentError("Config has not been set already on this machine. Run 'set_config()' first!'")

    def __repr__(self):
        return getattr(builtins, 'GMS_JobConfig').__repr__()


GMS_config = GMS_configuration()  # type: JobConfig


path_gmslib = os.path.dirname(pkgutil.get_loader("gms_preprocessing").path)
path_options_default = os.path.join(path_gmslib, 'options', 'options_default.json')


def set_config(job_ID, json_config='', reset_status=False, **kwargs):
    """Set up a configuration for a new gms_preprocessing job!

    :param job_ID:          job ID of the job to be executed, e.g. 123456 (must be present in database)
    :param json_config:     path to JSON file containing configuration parameters or a string in JSON format
    :param reset_status:    whether to reset the job status or not (default=False)
    :param kwargs:          keyword arguments to be passed to JobConfig
                            NOTE: All keyword arguments given here WILL OVERRIDE configurations that have been
                                  previously set via WebUI or via the json_config parameter!

    :Keyword Arguments:
        - inmem_serialization:     False: write intermediate results to disk in order to save memory
                                   True:  keep intermediate results in memory in order to save IO time
        - parallelization_level:   <str> choices: 'scenes' - parallelization on scene-level
                                                   'tiles'  - parallelization on tile-level
        - db_host:         host name of the server that runs the postgreSQL database
        - spatial_index_server_host:   host name of the server that runs the SpatialIndexMediator
        - spatial_index_server_port:   port used for connecting to SpatialIndexMediator
        - delete_old_output:        <bool> whether to delete previously created output of the given job ID
                                    before running the job (default = False)
        - exec_L1AP:       list of 3 elements: [run processor, write output, delete output if not needed anymore]
        - exec_L1BP:       list of 3 elements: [run processor, write output, delete output if not needed anymore]
        - exec_L1CP:       list of 3 elements: [run processor, write output, delete output if not needed anymore]
        - exec_L2AP:       list of 3 elements: [run processor, write output, delete output if not needed anymore]
        - exec_L2BP:       list of 3 elements: [run processor, write output, delete output if not needed anymore]
        - exec_L2CP:       list of 3 elements: [run processor, write output, delete output if not needed anymore]
        - CPUs:            number of CPU cores to be used for processing (default: None -> use all available)
        - allow_subMultiprocessing:
                           allow multiprocessing within workers
        - disable_exception_handler:
                           enable/disable automatic handling of unexpected exceptions (default: True -> enabled)
        - log_level:       the logging level to be used (choices: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL';
                           default: 'INFO')
        - tiling_block_size_XY:
                           X/Y block size to be used for any tiling process (default: (2048,2048)
        - is_test:         whether the current job represents a software test job (run by a test runner) or not
                           (default=False)
        - profiling:       enable/disable code profiling (default: False)
        - benchmark_global:
                           enable/disable benchmark of the whole processing pipeline
        - path_procdata_scenes:
                           output path to store processed scenes
        - path_procdata_MGRS:
                           output path to store processed MGRS tiles
        - path_archive:    input path where downloaded data are stored
        - virtual_sensor_id:       1:  Landsat-8,  10: Sentinel-2A 10m
        - datasetid_spatial_ref:   249 Sentinel-2A
    :rtype: JobConfig
    """
    # validate kwargs
    for k in kwargs:
        if k not in parameter_mapping and k != 'db_host':
            raise ValueError("'%s' is not a valid parameter. Valid parameters are: \n%s"
                             % (k, list(parameter_mapping.keys())))

    #################################
    # set GMS_JobConfig in builtins #
    #################################
    # FIXME virtual_sensor_id and datasetid_spatial_ref are not respected by JobConfig.
    if not hasattr(builtins, 'GMS_JobConfig') or reset_status:
        builtins.GMS_JobConfig = JobConfig(job_ID, json_config=json_config, **kwargs)

    #####################
    # check environment #
    #####################
    if not hasattr(builtins, 'GMS_EnvOK') or not getattr(builtins, 'GMS_EnvOK'):
        # check environment
        from ..misc import environment as ENV
        logger = logging.getLogger('GMSEnvironmentChecker')
        logger.setLevel(logging.DEBUG)
        GMSEnv = ENV.GMSEnvironment()
        GMSEnv.check_dependencies()
        GMSEnv.check_read_write_permissions()
        GMSEnv.ensure_properly_activated_GDAL()
        GMSEnv.check_ecmwf_api_creds()

        # close unclosed locks from previous runs
        from ..misc.locks import release_unclosed_locks
        release_unclosed_locks()

        builtins.GMS_EnvOK = True

    return getattr(builtins, 'GMS_JobConfig')


def get_conn_database(hostname='localhost', timeout=3):
    # type: (str, int) -> str
    """Return database connection string.

    :param hostname:    the host that runs the GMS postgreSQL database
    :param timeout:     connection timeout in seconds
    :return:
    """
    return "dbname='geomultisens' user='gmsdb' password='gmsdb' host='%s' connect_timeout=%d" \
           % (hostname, timeout)


class JobConfig(object):
    def __init__(self, ID, json_config='', **user_opts):
        """Create a job configuration

        Workflow:
        # 0. Environment
        # 1. 2 Wege, wo JSON herkommen kann: per console-command oder aus Datenbank
        #       - bei console-command: GMS_JOB.from_... muss default-options in DB schreiben
        # => zuerst JobConfig auf Basis von JSON erstellen
        # 2. dann überschreiben mit user-defined parametern (entweder init-parameter oder db-settings per webapp)

        :param ID:          job ID of the job to be executed, e.g. 123456 (must be present in database)
        :param json_config  path to JSON file containing configuration parameters or a string in JSON format
        :param user_opts    keyword arguments as passed by gms_preprocessing.set_config()
        """
        # privates
        self._DB_job_record = None  # type: GMS_JOB
        self._DB_config_table = None  # type: dict
        self._kwargs_defaults = None

        # fixed attributes
        # possible values: 'pending', 'running', 'canceled', 'failed', 'finished_with_warnings',
        # 'finished_with_errors', 'finished'
        self.status = 'pending'
        self.start_time = datetime.datetime.now()
        self.end_time = None
        self.computation_time = None
        self.hostname = socket.gethostname()
        self.version = __version__
        self.versionalias = __versionalias__

        #######################
        # POPULATE PARAMETERS #
        #######################

        # args
        self.ID = ID
        self.json_config = json_config
        self.kwargs = user_opts

        # database connection
        self.db_host = user_opts['db_host']
        self.conn_database = get_conn_database(hostname=self.db_host)

        # get validated options dict from JSON-options
        self.json_opts_fused_valid = self.get_json_opts(validate=True)

        gp = self.get_parameter

        ##################
        # global options #
        ##################

        self.inmem_serialization = gp('inmem_serialization')
        self.parallelization_level = gp('parallelization_level')
        self.spatial_index_server_host = gp('spatial_index_server_host')
        self.spatial_index_server_port = gp('spatial_index_server_port')
        self.CPUs = gp('CPUs', fallback=multiprocessing.cpu_count())
        self.CPUs_all_jobs = gp('CPUs_all_jobs')
        self.max_mem_usage = gp('max_mem_usage')
        self.critical_mem_usage = gp('critical_mem_usage')
        self.max_parallel_reads_writes = gp('max_parallel_reads_writes')
        self.allow_subMultiprocessing = gp('allow_subMultiprocessing')
        self.delete_old_output = gp('delete_old_output')
        self.disable_exception_handler = gp('disable_exception_handler')
        self.disable_IO_locks = gp('disable_IO_locks')
        self.disable_CPU_locks = gp('disable_CPU_locks')
        self.disable_DB_locks = gp('disable_DB_locks')
        self.disable_memory_locks = gp('disable_memory_locks')
        self.min_version_mem_usage_stats = gp('min_version_mem_usage_stats')
        self.log_level = gp('log_level')
        self.tiling_block_size_XY = gp('tiling_block_size_XY')
        self.is_test = gp('is_test')
        self.profiling = gp('profiling')
        self.benchmark_global = gp('benchmark_global')

        #########
        # paths #
        #########

        # external
        self.path_spatIdxSrv = self.DB_config_table['path_spatial_index_mediator_server']
        self.path_tempdir = self.absP(self.DB_config_table['path_tempdir'])
        self.path_custom_sicor_options = gp('path_custom_sicor_options')
        self.path_dem_proc_srtm_90m = self.absP(self.DB_config_table['path_dem_proc_srtm_90m'])
        self.path_spechomo_classif = gp('path_spechomo_classif')

        # internal (included in gms_preprocessing repository)
        self.path_earthSunDist = self.joinP(path_gmslib, 'database', 'earth_sun_distance',
                                            'Earth_Sun_distances_per_day_edited.csv')
        self.path_SNR_models = self.joinP(path_gmslib, 'database', 'snr')
        self.path_cloud_classif = self.joinP(path_gmslib, 'database', 'cloud_classifier')
        self.path_solar_irr = self.joinP(path_gmslib, 'database', 'solar_irradiance',
                                         'SUNp1fontenla__350-2500nm_@0.1nm_converted.txt')

        if not self.is_test:
            def get_dbpath(dbkey):
                return self.joinP(self.path_fileserver, self.DB_config_table[dbkey])

            # normal mode
            self.path_fileserver = self.DB_config_table['path_data_root']
            self.path_archive = gp('path_archive', fallback=get_dbpath('foldername_download'))
            self.path_procdata_scenes = gp('path_procdata_scenes', fallback=get_dbpath('foldername_procdata_scenes'))
            self.path_procdata_MGRS = gp('path_procdata_MGRS', fallback=get_dbpath('foldername_procdata_MGRS'))
            self.path_ECMWF_db = gp('path_ECMWF_db', fallback=self.absP(self.DB_config_table['path_ECMWF_db']))
            self.path_benchmarks = gp('path_benchmarks', fallback=self.absP(self.DB_config_table['path_benchmarks']))
            self.path_job_logs = gp('path_job_logs', fallback=get_dbpath('foldername_job_logs'))

        else:
            # software test mode, the repository should be self-contained -> use only relative paths
            self.path_fileserver = self.joinP(path_gmslib, '..', 'tests', 'data')
            self.path_archive = self.joinP(path_gmslib, '..', 'tests', 'data', 'archive_data')
            self.path_procdata_scenes = self.joinP(path_gmslib, '..', 'tests', 'data', 'output_scenes')
            # self.path_procdata_scenes = '/data1/gms/mount/db/data/processed_scenes/test_loggingerrors/'  # FIXME
            self.path_procdata_MGRS = self.joinP(path_gmslib, '..', 'tests', 'data', 'output_mgrs_tiles')
            self.path_ECMWF_db = self.joinP(path_gmslib, '..', 'tests', 'data', 'processed_ECMWF')
            self.path_benchmarks = self.joinP(path_gmslib, '..', 'tests', 'data', 'benchmarks')
            self.path_job_logs = self.joinP(path_gmslib, '..', 'tests', 'data', 'job_logs')
            # self.path_job_logs = '/data1/gms/mount/db/data/job_logs/'  # FIXME

        ###########################
        # processor configuration #
        ###########################

        # general_opts
        self.skip_thermal = gp('skip_thermal')
        self.skip_pan = gp('skip_pan')
        self.sort_bands_by_cwl = gp('sort_bands_by_cwl')
        self.target_radunit_optical = gp('target_radunit_optical')
        self.target_radunit_thermal = gp('target_radunit_thermal')
        self.scale_factor_TOARef = gp('scale_factor_TOARef')
        self.scale_factor_BOARef = gp('scale_factor_BOARef')
        self.mgrs_pixel_buffer = gp('mgrs_pixel_buffer')
        self.output_data_compression = gp('output_data_compression')
        self.write_ENVIclassif_cloudmask = gp('write_ENVIclassif_cloudmask')

        # processor specific opts

        # L1A
        self.exec_L1AP = gp('exec_L1AP')
        self.SZA_SAA_calculation_accurracy = gp('SZA_SAA_calculation_accurracy')
        self.export_VZA_SZA_SAA_RAA_stats = gp('export_VZA_SZA_SAA_RAA_stats')

        # L1B
        self.exec_L1BP = gp('exec_L1BP')
        self.skip_coreg = gp('skip_coreg')
        self.spatial_ref_min_overlap = gp('spatial_ref_min_overlap')
        self.spatial_ref_min_cloudcov = gp('spatial_ref_min_cloudcov')
        self.spatial_ref_max_cloudcov = gp('spatial_ref_max_cloudcov')
        self.spatial_ref_plusminus_days = gp('spatial_ref_plusminus_days')
        self.spatial_ref_plusminus_years = gp('spatial_ref_plusminus_years')
        self.coreg_band_wavelength_for_matching = gp('coreg_band_wavelength_for_matching')
        self.coreg_max_shift_allowed = gp('coreg_max_shift_allowed')
        self.coreg_window_size = gp('coreg_window_size')

        # L1C
        self.exec_L1CP = gp('exec_L1CP')
        self.cloud_masking_algorithm = gp('cloud_masking_algorithm')
        self.export_L1C_obj_dumps = gp('export_L1C_obj_dumps')
        self.auto_download_ecmwf = gp('auto_download_ecmwf')
        self.ac_fillnonclear_areas = gp('ac_fillnonclear_areas')
        self.ac_clear_area_labels = gp('ac_clear_area_labels')
        self.ac_scale_factor_errors = gp('ac_scale_factor_errors')
        self.ac_max_ram_gb = gp('ac_max_ram_gb')
        self.ac_estimate_accuracy = gp('ac_estimate_accuracy')
        self.ac_bandwise_accuracy = gp('ac_bandwise_accuracy')

        # L2A
        self.exec_L2AP = gp('exec_L2AP')
        self.align_coord_grids = gp('align_coord_grids')
        self.match_gsd = gp('match_gsd')
        self.spatial_resamp_alg = gp('spatial_resamp_alg')
        self.clip_to_extent = gp('clip_to_extent')
        self.spathomo_estimate_accuracy = gp('spathomo_estimate_accuracy')

        # L2B
        self.exec_L2BP = gp('exec_L2BP')
        self.spechomo_method = gp('spechomo_method')
        self.spechomo_n_clusters = gp('spechomo_n_clusters')
        self.spechomo_rfr_n_trees = 50  # this is static confic value, not a user option
        self.spechomo_rfr_tree_depth = 10  # this is static confic value, not a user option
        self.spechomo_classif_alg = gp('spechomo_classif_alg')
        self.spechomo_kNN_n_neighbors = gp('spechomo_kNN_n_neighbors')
        self.spechomo_estimate_accuracy = gp('spechomo_estimate_accuracy')
        self.spechomo_bandwise_accuracy = gp('spechomo_bandwise_accuracy')

        if self.spechomo_method == 'RFR':
            raise NotImplementedError("The spectral harmonization method 'RFR' is currently not completely implemented."
                                      "Please us another one.")
            # FIXME RFR classifiers are missing (cannot be added to the repository to to file size > 1 GB)

        # L2C
        self.exec_L2CP = gp('exec_L2CP')

        ################################
        # target sensor specifications #
        ################################

        self.virtual_sensor_id = gp('virtual_sensor_id', attr_db_job_record='virtualsensorid')
        # FIXME Why is datasetid_spatial_ref missing in virtual_sensors table
        self.datasetid_spatial_ref = gp('datasetid_spatial_ref', attr_db_job_record='datasetid_spatial_ref')

        VSSpecs = self.get_virtual_sensor_specs()
        self.virtual_sensor_name = VSSpecs['name']

        # spectral specifications
        self.datasetid_spectral_ref = VSSpecs['spectral_characteristics_datasetid']  # None in case of custom sensor
        # FIXME column is empty a known datasetid as spectral characteristics virtual sensor is chosen:
        self.target_CWL = VSSpecs['wavelengths_pos']
        # FIXME column is empty a known datasetid as spectral characteristics virtual sensor is chosen:
        self.target_FWHM = VSSpecs['band_width']

        # spatial specifications
        target_gsd_tmp = VSSpecs['spatial_resolution']  # table features only 1 value for X/Y-dims FIXME user inputs?
        # FIXME target GSD setting is a duplicate to datasetid_spatial_ref!
        self.target_gsd = xgsd, ygsd = \
            [target_gsd_tmp]*2 if isinstance(target_gsd_tmp, (int, float)) else target_gsd_tmp
        self.target_epsg_code = VSSpecs['projection_epsg']
        # FIXME values in case user defines only Landsat?
        self.spatial_ref_gridx = np.arange(xgsd / 2., xgsd / 2. + 2 * xgsd, xgsd).tolist()  # e.g. [15, 45]
        self.spatial_ref_gridy = np.arange(ygsd / 2., ygsd / 2. + 2 * ygsd, ygsd).tolist()

        #############
        # data list #
        #############

        self.data_list = self.get_data_list_of_current_jobID()

        ############
        # validate #
        ############
        self.validate_exec_configs()

        GMSValidator(allow_unknown=True, schema=gms_schema_config_output).validate(self.to_dict())

        # check if parallel read/write processes have been limited on a storage mountpoint shared between multiple hosts
        if self.max_parallel_reads_writes != 0:
            self.check_no_read_write_limit_on_xtfs_mountpoint()

    def get_init_argskwargs(self, ignore=("logger",)):
        """
        Return a tuple containing dictionary of calling function's. named arguments and a list of
        calling function's unnamed positional arguments.
        """

        posname, kwname, argskwargs = getargvalues(stack()[1][0])[-3:]
        argskwargs.update(argskwargs.pop(kwname, []))
        argskwargs = {k: v for k, v in argskwargs.items() if k not in ignore and k != 'self' and not k.startswith('__')}
        sig = signature(self.__init__)
        argsnames = [k for k in sig.parameters if sig.parameters[k].default == _empty]
        return {'args': {k: v for k, v in argskwargs.items() if k in argsnames},
                'kwargs': {k: v for k, v in argskwargs.items() if k not in argsnames}}

    def get_parameter(self, key_user_opts, attr_db_job_record='', fallback=None):
        # 1. JobConfig parameters: parameters that are directly passed to JobConfig
        if key_user_opts in self.kwargs:
            return self.kwargs[key_user_opts]

        # 2. WebUI parameters: parameters that have been defined via WebUI
        if attr_db_job_record:
            return getattr(self.DB_job_record, attr_db_job_record)

        # 3. JSON parameters: parameters that have been defined via JSON Input (command line or advanced UI params)
        val_json = get_param_from_json_config(key_user_opts, self.json_opts_fused_valid)
        if val_json or val_json is False:
            return val_json

        # fallback: if nothing has been returned until here
        return fallback

    @property
    def DB_job_record(self):
        # type: () -> GMS_JOB
        if not self._DB_job_record:
            # check if job ID exists in database
            from ..misc.database_tools import GMS_JOB  # noqa F811  # redefinition of unused 'GMS_JOB' from line 22
            try:
                self._DB_job_record = GMS_JOB(self.conn_database).from_job_ID(self.ID)
            except ValueError:
                raise

        return self._DB_job_record

    @property
    def DB_config_table(self):
        # type: () -> dict
        """Returns the content of the config table of the postgreSQL database as dictionary."""
        if not self._DB_config_table:
            from ..misc.database_tools import get_info_from_postgreSQLdb
            db_cfg = dict(get_info_from_postgreSQLdb(self.conn_database, 'config', ['key', 'value']))

            # convert relative to absolute paths
            self._DB_config_table = {k: self.absP(v) if k.startswith('path_') and v.startswith('./') else v
                                     for k, v in db_cfg.items()}

        return self._DB_config_table

    def get_virtual_sensor_specs(self):
        # type: () -> dict
        """Returns the content of the virtual_sensors table of the postgreSQL database as dictionary."""
        from ..misc.database_tools import get_info_from_postgreSQLdb

        # column spectral_characteristics_datasetid is not used later because its given by jobs.datasetid_spatial_ref
        cols2read = ['name', 'projection_epsg', 'spatial_resolution', 'spectral_characteristics_datasetid',
                     'wavelengths_pos', 'band_width']

        res = get_info_from_postgreSQLdb(self.conn_database, 'virtual_sensors',
                                         cols2read, {'id': self.virtual_sensor_id})[0]

        VSSpecs = dict()
        for i, col in enumerate(cols2read):
            val = res[i]
            if col == 'spectral_characteristics_datasetid' and val == -1:  # nodata value
                val = None

            VSSpecs[col] = val

        return VSSpecs

    def get_json_opts(self, validate=True):
        """Get a dictionary of GMS config parameters according to the jobs table of the database.

        NOTE: Reads the default options from options_default.json and updates the values with those from database.
        """
        def update_dict(d, u):
            for k, v in u.items():
                if isinstance(v, Mapping):
                    d[k] = update_dict(d.get(k, {}), v)
                else:
                    d[k] = v
            return d

        # read options_default.json
        default_options = get_options(path_options_default, validation=validate)

        #############################################
        # update default options with those from DB #
        #############################################

        if self.DB_job_record.analysis_parameter:
            try:
                params_dict = json.loads(jsmin(self.DB_job_record.analysis_parameter))
            except JSONDecodeError:
                warnings.warn('The advanced options given in the WebUI could not be decoded. '
                              'JSON decoder failed with the following error:')
                raise

            # convert values to useful data types and update the default values
            params_dict = json_to_python(params_dict)
            update_dict(default_options, params_dict)

        ###############################################################################################################
        # if json config is provided (via python bindings or CLI parser -> override all options with that json config #
        ###############################################################################################################

        if self.json_config:
            if self.json_config.startswith("{"):
                try:
                    params_dict = json.loads(jsmin(self.json_config))
                except JSONDecodeError:
                    warnings.warn('The given JSON options string could not be decoded. '
                                  'JSON decoder failed with the following error:')
                    raise
            elif os.path.isfile(self.json_config):
                try:
                    with open(self.json_config, 'r') as inF:
                        params_dict = json.loads(jsmin(inF.read()))
                except JSONDecodeError:
                    warnings.warn('The given JSON options file %s could not be decoded. '
                                  'JSON decoder failed with the following error:' % self.json_config)
                    raise

            else:
                raise ValueError("The parameter 'json_config' must be a JSON formatted string or a JSON file on disk.")

            # convert values to useful data types and update the default values
            params_dict = json_to_python(params_dict)
            update_dict(default_options, params_dict)

        if validate:
            GMSValidator(allow_unknown=True, schema=gms_schema_input).validate(default_options)

        json_options = default_options
        return json_options

    @staticmethod
    def absP(relP):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), relP))

    @staticmethod
    def joinP(*items):
        return os.path.join(*items)

    def get_data_list_of_current_jobID(self):
        """
        Get a list of datasets to be processed from database and return it together with some metadata.

        :return:    <list> of OrderedDicts, e.g. [OrderedDict([('proc_level', None), ('scene_ID', 5895940),
                    ('datasetid', 104), ('image_type', 'RSD'), ('satellite', 'Landsat-8'), ('sensor', 'OLI_TIRS'),
                    ('subsystem', ''), ('acquisition_date', datetime.datetime(2015, 2, 5, 10, 2, 52)),
                    ('entity_ID', 'LC81930242015036LGN00'), ('filename', 'LC81930242015036LGN00.tar.gz'),
                    ('sensormode', 'M'), ('logger', None)]), ...]
        """
        from ..model.metadata import get_sensormode
        data_list = []
        with psycopg2.connect(self.conn_database) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(r"""
                    WITH jobs_unnested AS (
                            SELECT id, unnest(sceneids) AS sceneid FROM jobs
                        )
                    SELECT jobs_unnested.sceneid,
                           scenes.datasetid,
                           scenes.acquisitiondate,
                           scenes.entityid,
                           scenes.filename,
                           COALESCE(scenes_proc.proc_level::text, 'L1A') AS proc_level,
                           datasets.image_type,
                           satellites.name AS satellite,
                           sensors.name AS sensor,
                           subsystems.name AS subsystem
                    FROM jobs_unnested
                    LEFT OUTER JOIN scenes ON scenes.id = jobs_unnested.sceneid
                    LEFT OUTER JOIN scenes_proc ON scenes_proc.sceneid = jobs_unnested.sceneid
                    LEFT OUTER JOIN datasets ON datasets.id = datasetid
                    LEFT OUTER JOIN satellites ON satellites.id = satelliteid
                    LEFT OUTER JOIN sensors ON sensors.id = sensorid
                    LEFT OUTER JOIN subsystems ON subsystems.id = subsystemid
                    WHERE jobs_unnested.id = %s
                    """,
                            (self.ID,))

                for row in cur.fetchall():
                    ds = OrderedDict()
                    ds["proc_level"] = row["proc_level"] if not self.is_test else None
                    ds["scene_ID"] = row["sceneid"]
                    ds["dataset_ID"] = row["datasetid"]
                    ds["image_type"] = row["image_type"]
                    ds["satellite"] = row["satellite"]
                    ds["sensor"] = row["sensor"]
                    ds["subsystem"] = row["subsystem"]
                    ds["acq_datetime"] = row["acquisitiondate"]
                    ds["entity_ID"] = row["entityid"]
                    ds["filename"] = row["filename"]

                    ds['sensor'] = 'ETM+' if re.search(r'ETM+', ds['sensor']) else ds['sensor']
                    if self.skip_thermal and ds['subsystem'] == 'TIR':
                        continue  # removes ASTER TIR in case of skip_thermal
                    ds['subsystem'] = '' if ds['subsystem'] is None else ds['subsystem']
                    ds['sensormode'] = get_sensormode(ds)
                    if self.skip_pan and ds['sensormode'] == 'P':
                        continue  # removes e.g. SPOT PAN in case of skip_pan

                    if re.search(r"Sentinel-2A", ds['satellite'], re.I):
                        for subsystem in ['S2A10', 'S2A20', 'S2A60']:
                            sub_ds = ds.copy()
                            sub_ds['subsystem'] = subsystem
                            data_list.append(sub_ds)
                    elif re.search(r"Sentinel-2B", ds['satellite'], re.I):
                        for subsystem in ['S2B10', 'S2B20', 'S2B60']:
                            sub_ds = ds.copy()
                            sub_ds['subsystem'] = subsystem
                            data_list.append(sub_ds)
                    elif re.search(r"Terra", ds['satellite'], re.I):
                        for subsystem in ['VNIR1', 'VNIR2', 'SWIR', 'TIR']:
                            sub_ds = ds.copy()
                            sub_ds['subsystem'] = subsystem
                            data_list.append(sub_ds)
                    else:
                        data_list.append(ds)

        self.data_list = data_list
        return self.data_list

    def validate_exec_configs(self):
        for i in ['L1AP', 'L1BP', 'L1CP', 'L2AP', 'L2BP', 'L2CP']:
            exec_lvl = getattr(self, 'exec_%s' % i)

            if exec_lvl is None:
                continue

            # check input format
            if all([len(exec_lvl) == 3, (np.array(exec_lvl) == np.array(np.array(exec_lvl, np.bool), np.int)).all()]):
                execute, write, delete = exec_lvl

                # written output cannot be turned off in execution mode 'Python'
                if not self.inmem_serialization and execute and not write:
                    warnings.warn("If CFG.inmem_serialization is False the output writer for %s has to be enabled "
                                  "because any operations on GMS_obj.arr read the intermediate results from disk. "
                                  "Turning it on.." % i)
                    write = True
                    setattr(self, 'exec_%s' % i, [execute, write, delete])

            else:
                raise ValueError('Execution mode must be provided as list of 3 elements containing only boolean '
                                 'values. Got %s for %s.' % (exec_lvl, i))

    def check_no_read_write_limit_on_xtfs_mountpoint(self):
        intensive_IO_paths = [self.path_fileserver, self.path_archive, self.path_benchmarks,
                              self.path_dem_proc_srtm_90m, self.path_ECMWF_db, self.path_procdata_MGRS,
                              self.path_procdata_scenes]

        mount_points = {el.mountpoint: el for el in psutil.disk_partitions(all=True)}

        for path in intensive_IO_paths:
            for mp, mp_object in mount_points.items():
                if path.startswith(mp) and mp_object.device.startswith('xtreemfs'):
                    warnings.warn("Path %s appears to be on an XtreemFS mountpoint. It is highly recommended to set "
                                  "the configuration parameter 'max_parallel_reads_writes' to 0 in that case! "
                                  "Otherwise read/write processes might be slowed down! Continuing in 20 seconds.."
                                  % path)
                    time.sleep(20)
                    break

    def to_dict(self):
        """Generate a dictionary in the same structure like the one in options_default.json from the current config."""
        opts_default = get_options(path_options_default)

        # add all keys included in options_default.json
        outdict = dict()
        for key in opts_default.keys():
            if not isinstance(opts_default[key], (dict, OrderedDict)):
                outdict[key] = getattr(self, key)
            else:
                group = key
                if group not in outdict:
                    outdict[group] = dict()

                for group_key in opts_default[group]:
                    if not isinstance(opts_default[group][group_key], (dict, OrderedDict)):
                        outdict[group][group_key] = getattr(self, group_key)
                    else:
                        subgroup = group_key
                        if subgroup not in outdict[group]:
                            outdict[group][subgroup] = dict()

                        for subgroup_key in opts_default[group][subgroup]:
                            try:
                                outdict[group][subgroup][subgroup_key] = getattr(self, subgroup_key)
                            except AttributeError:
                                procexec_keys = ['run_processor', 'write_output', 'delete_output']
                                if subgroup_key in procexec_keys:
                                    proc_code = subgroup
                                    outdict[group][subgroup][subgroup_key] = \
                                        getattr(self, 'exec_%sP' % proc_code)[procexec_keys.index(subgroup_key)]
                                else:
                                    raise

        # add job metadata
        outdict.update(dict(
            job_meta={k: getattr(self, k) for k in ['ID', 'start_time', 'end_time', 'computation_time', 'hostname']},
            data_list={'dataset_%s' % i: ds for i, ds in enumerate(self.data_list)}))

        # add data_list

        return outdict

    def to_jsonable_dict(self):
        # type: (JobConfig) -> dict
        return python_to_json(self.to_dict())

    def save(self, path_outfile):
        """Save the JobConfig instance to a JSON file in the same structure like the one in options_default.json.

        :param path_outfile:    path of the output JSON file
        """
        with open(path_outfile, 'w') as outF:
            json.dump(self.to_jsonable_dict(), outF, skipkeys=False, indent=4)

    def __repr__(self):
        return pformat(self.to_dict())


def is_GMSConfig_available():
    try:
        if GMS_config is not None:
            return True
    except (EnvironmentError, OSError):
        return False


def json_to_python(value):
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    if type(value) is dict:
        return {json_to_python(k): json_to_python(v) for k, v in value.items()}
    elif type(value) is list:
        return [json_to_python(v) for v in value]
    else:
        if value == "None":
            return None
        if value == "slice(None, None, None)":
            return slice(None)
        if value in [True, "true"]:
            return True
        if value in [False, "false"]:
            return False
        if is_number(value):
            try:
                if str(int(value)) != str(float(value)):
                    return int(value)
                else:
                    return float(value)
            except ValueError:
                return float(value)
        else:
            return value


def python_to_json(value):
    if type(value) in [dict, OrderedDict]:
        return {python_to_json(k): python_to_json(v) for k, v in value.items()}
    elif type(value) is list:
        return [python_to_json(v) for v in value]
    elif type(value) is np.ndarray:
        return [python_to_json(v) for v in value.tolist()]
    else:
        if value is None:
            return "None"
        if value is slice(None):
            return "slice(None, None, None)"
        if value is True:
            return "true"
        if value is False:
            return "false"
        if type(value) is datetime.datetime:
            return datetime.datetime.strftime(value, '%Y-%m-%d %H:%M:%S.%f%z')
        else:
            return value


class GMSValidator(Validator):
    def __init__(self, *args, **kwargs):
        """

        :param args:    Arguments to be passed to cerberus.Validator
        :param kwargs:  Keyword arguments to be passed to cerberus.Validator
        """
        super(GMSValidator, self).__init__(*args, **kwargs)

    def validate(self, document2validate, **kwargs):
        if super(GMSValidator, self).validate(document=document2validate, **kwargs) is False:
            raise ValueError("Options is malformed: %s" % str(self.errors))


def get_options(target, validation=True):
    """Return dictionary with all options.

    :param validation: True / False, whether to validate options read from files or not
    :param target: if path to file, then json is used to load, otherwise the default template is used
    :return: dictionary with options
    """

    if os.path.isfile(target):
        with open(target, "r") as fl:
            options = json_to_python(json.loads(jsmin(fl.read())))

        if validation is True:
            GMSValidator(allow_unknown=True, schema=gms_schema_input).validate(options)

        return options
    else:
        raise FileNotFoundError("Options file not found at file path %s." % target)
