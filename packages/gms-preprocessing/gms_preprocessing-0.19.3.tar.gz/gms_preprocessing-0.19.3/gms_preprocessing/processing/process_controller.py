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

from __future__ import (division, print_function, unicode_literals, absolute_import)

import numpy as np
from pandas import DataFrame
import datetime
import os
import time
from itertools import chain
import signal
import re
from typing import TYPE_CHECKING
import shutil
import sys
from natsort import natsorted

from ..io import output_writer as OUT_W
from ..io import input_reader as INP_R
from ..misc import database_tools as DB_T
from ..misc import helper_functions as HLP_F
from ..misc.path_generator import path_generator
from ..misc.logging import GMS_logger, shutdown_loggers
from ..algorithms import L1A_P, L1B_P, L1C_P, L2A_P, L2B_P, L2C_P
from ..model.metadata import get_LayerBandsAssignment
from ..model.gms_object import failed_GMS_object, GMS_object, GMS_identifier
from .pipeline import (L1A_map, L1A_map_1, L1A_map_2, L1A_map_3, L1B_map, L1C_map,
                       L2A_map, L2B_map, L2C_map)
from ..options.config import set_config
from .multiproc import MAP, imap_unordered
from ..misc.definition_dicts import proc_chain, db_jobs_statistics_def
from ..misc.locks import release_unclosed_locks
from ..version import __version__, __versionalias__

from py_tools_ds.numeric.array import get_array_tilebounds

if TYPE_CHECKING:
    from collections import OrderedDict  # noqa F401  # flake8 issue
    from typing import List  # noqa F401  # flake8 issue
    from ..options.config import GMS_config  # noqa F401  # flake8 issue


__author__ = 'Daniel Scheffler'


class ProcessController(object):
    def __init__(self, job_ID, **config_kwargs):
        """gms_preprocessing process controller

        :param job_ID:          job ID belonging to a valid database record within table 'jobs'
        :param config_kwargs:   keyword arguments to be passed to gms_preprocessing.set_config()
        """

        # assertions
        if not isinstance(job_ID, int):
            raise ValueError("'job_ID' must be an integer value. Got %s." % type(job_ID))

        # set GMS configuration
        config_kwargs.update(dict(reset_status=True))
        self.config = set_config(job_ID, **config_kwargs)  # type: GMS_config

        # defaults
        self._logger = None
        self._DB_job_record = None
        self.profiler = None

        self.failed_objects = []
        self.L1A_newObjects = []
        self.L1B_newObjects = []
        self.L1C_newObjects = []
        self.L2A_newObjects = []
        self.L2A_tiles = []
        self.L2B_newObjects = []
        self.L2C_newObjects = []

        self.summary_detailed = None
        self.summary_quick = None

        # check if process_controller is executed by debugger
        # isdebugging = 1 if True in [frame[1].endswith("pydevd.py") for frame in inspect.stack()] else False
        # if isdebugging:  # override the existing settings in order to get write access everywhere
        #    pass

        # called_from_iPyNb = 1 if 'ipykernel/__main__.py' in sys.argv[0] else 0

        # create job log
        self._path_job_logfile = os.path.join(self.config.path_job_logs, '%s.log' % self.config.ID)
        if os.path.exists(self._path_job_logfile):
            HLP_F.silentremove(self._path_job_logfile)

        self.logger.info("Executing gms_preprocessing, version: %s (%s)" % (__version__, __versionalias__))
        self.logger.info('Process Controller initialized for job ID %s (comment: %s).'
                         % (self.config.ID, self.DB_job_record.comment))
        self.logger.info('Job logfile: %s' % self._path_job_logfile)

        # save config
        self._path_job_optionsfile = os.path.join(self.config.path_job_logs, '%s_options.json' % self.config.ID)
        self.config.save(self._path_job_optionsfile)
        self.logger.info('Job options file: %s' % self._path_job_optionsfile)

        if self.config.delete_old_output:
            self.logger.info('Deleting previously processed data...')
            self.DB_job_record.delete_procdata_of_entire_job(force=True)

    @property
    def logger(self):
        if self._logger and self._logger.handlers[:]:
            return self._logger
        else:
            self._logger = GMS_logger('ProcessController__%s' % self.config.ID, fmt_suffix='ProcessController',
                                      path_logfile=self._path_job_logfile, log_level=self.config.log_level, append=True)
            return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    @logger.deleter
    def logger(self):
        if self._logger not in [None, 'not set']:
            self._logger.close()
            self._logger = None

    @property
    def DB_job_record(self):
        if self._DB_job_record:
            return self._DB_job_record
        else:
            self._DB_job_record = DB_T.GMS_JOB(self.config.conn_database)
            self._DB_job_record.from_job_ID(self.config.ID)
            return self._DB_job_record

    @DB_job_record.setter
    def DB_job_record(self, value):
        self._DB_job_record = value

    @property
    def sceneids_failed(self):
        return [obj.scene_ID for obj in self.failed_objects]

    def _add_local_availability_single_dataset(self, dataset):
        # type: (OrderedDict) -> OrderedDict
        # TODO revise this function
        # query the database and get the last written processing level and LayerBandsAssignment
        DB_match = DB_T.get_info_from_postgreSQLdb(
            self.config.conn_database, 'scenes_proc', ['proc_level', 'layer_bands_assignment'],
            dict(sceneid=dataset['scene_ID']))

        # get the corresponding logfile
        path_logfile = path_generator(dataset).get_path_logfile(merged_subsystems=False)
        path_logfile_merged_ss = path_generator(dataset).get_path_logfile(merged_subsystems=True)

        def get_AllWrittenProcL_dueLog(path_log):  # TODO replace this by database query + os.path.exists
            """Returns all processing level that have been successfully written according to logfile."""

            if not os.path.exists(path_log):
                if path_log == path_logfile:  # path_logfile_merged_ss has already been searched
                    self.logger.info("No logfile named '%s' found for %s at %s. Dataset has to be reprocessed."
                                     % (os.path.basename(path_log), dataset['entity_ID'], os.path.dirname(path_log)))
                AllWrittenProcL_dueLog = []
            else:
                logfile = open(path_log, 'r').read()
                AllWrittenProcL_dueLog = re.findall(r":*(\S*\s*) data successfully saved.", logfile, re.I)
                if not AllWrittenProcL_dueLog and path_logfile == path_logfile_merged_ss:  # AllWrittenProcL_dueLog = []
                    self.logger.info('%s: According to logfile no completely processed data exist at any '
                                     'processing level. Dataset has to be reprocessed.' % dataset['entity_ID'])
                else:
                    AllWrittenProcL_dueLog = natsorted(list(set(AllWrittenProcL_dueLog)))
            return AllWrittenProcL_dueLog

        # check if there are not multiple database records for this dataset
        if len(DB_match) == 1 or DB_match == [] or DB_match == 'database connection fault':

            # get all processing level that have been successfully written
            # NOTE: first check for merged subsystem datasets because they have hiver processing levels
            AllWrittenProcL = get_AllWrittenProcL_dueLog(path_logfile_merged_ss)
            if not AllWrittenProcL:
                AllWrittenProcL = get_AllWrittenProcL_dueLog(path_logfile)
            else:
                # A L2A+ dataset with merged subsystems has been found. Use that logfile.
                path_logfile = path_logfile_merged_ss

            dataset['proc_level'] = None  # default (dataset has to be reprocessed)

            # loop through all the found proc. levels and find the one that fulfills all requirements
            for ProcL in reversed(AllWrittenProcL):
                if dataset['proc_level']:
                    break  # proc_level found; no further searching for lower proc_levels
                assumed_path_GMS_file = '%s_%s.gms' % (os.path.splitext(path_logfile)[0], ProcL)

                # check if there is also a corresponding GMS_file on disk
                if os.path.isfile(assumed_path_GMS_file):
                    GMS_file_dict = INP_R.GMSfile2dict(assumed_path_GMS_file)
                    target_LayerBandsAssignment = \
                        get_LayerBandsAssignment(
                            GMS_identifier(
                                image_type=dataset['image_type'],
                                satellite=dataset['satellite'],
                                sensor=dataset['sensor'],
                                subsystem=dataset['subsystem'] if path_logfile != path_logfile_merged_ss else '',
                                proc_level=ProcL,  # must be respected because LBA changes after atm. Corr.
                                dataset_ID=dataset['dataset_ID']),
                            nBands=(1 if dataset['sensormode'] == 'P' else None))

                    # check if the LayerBandsAssignment of the written dataset on disk equals the
                    # desired LayerBandsAssignment
                    if target_LayerBandsAssignment == GMS_file_dict['LayerBandsAssignment']:

                        # update the database record if the dataset could not be found in database
                        if DB_match == [] or DB_match == 'database connection fault':
                            self.logger.info('The dataset %s is not included in the database of processed data but'
                                             ' according to logfile %s has been written successfully. Recreating '
                                             'missing database entry.' % (dataset['entity_ID'], ProcL))
                            DB_T.data_DB_updater(GMS_file_dict)

                            dataset['proc_level'] = ProcL

                        # if the dataset could be found in database
                        elif len(DB_match) == 1:
                            try:
                                self.logger.info('Found a matching %s dataset for %s. Processing skipped until %s.'
                                                 % (ProcL, dataset['entity_ID'],
                                                    proc_chain[proc_chain.index(ProcL) + 1]))
                            except IndexError:
                                self.logger.info('Found a matching %s dataset for %s. Processing already done.'
                                                 % (ProcL, dataset['entity_ID']))

                            if DB_match[0][0] == ProcL:
                                dataset['proc_level'] = DB_match[0][0]
                            else:
                                dataset['proc_level'] = ProcL

                    else:
                        self.logger.info('Found a matching %s dataset for %s but with a different '
                                         'LayerBandsAssignment (desired: %s; found %s). Dataset has to be reprocessed.'
                                         % (ProcL, dataset['entity_ID'],
                                            target_LayerBandsAssignment, GMS_file_dict['LayerBandsAssignment']))
                else:
                    self.logger.info('%s for dataset %s has been written due to logfile but no corresponding '
                                     'dataset has been found.' % (ProcL, dataset['entity_ID']) +
                                     ' Searching for lower processing level...'
                                     if AllWrittenProcL.index(ProcL) != 0 else '')

        elif len(DB_match) > 1:
            self.logger.info('According to database there are multiple matches for the dataset %s. Dataset has to '
                             'be reprocessed.' % dataset['entity_ID'])
            dataset['proc_level'] = None

        else:
            dataset['proc_level'] = None

        return dataset

    def add_local_availability(self, datasets):
        # type: (List[OrderedDict]) -> List[OrderedDict]
        """Check availability of all subsets per scene and processing level.

        NOTE: The processing level of those scenes, where not all subsystems are available in the same processing level
              is reset.

        :param datasets:    List of one OrderedDict per subsystem as generated by CFG.data_list
        """
        datasets = [self._add_local_availability_single_dataset(ds) for ds in datasets]

        ######################################################################################################
        # validate that all subsystems of the same sceneid are at the same processing level; otherwise reset #
        ######################################################################################################
        datasets_validated = []
        datasets_grouped = HLP_F.group_dicts_by_key(datasets, key='scene_ID')

        for ds_group in datasets_grouped:
            proc_lvls = [ds['proc_level'] for ds in ds_group]

            if not len(list(set(proc_lvls))) == 1:
                # reset processing level of those scenes where not all subsystems are available
                self.logger.info('%s: Found already processed subsystems at different processing levels %s. '
                                 'Dataset has to be reprocessed to avoid errors.'
                                 % (ds_group[0]['entity_ID'], proc_lvls))

                for ds in ds_group:
                    ds['proc_level'] = None
                    datasets_validated.append(ds)
            else:
                datasets_validated.extend(ds_group)

        return datasets_validated

    @staticmethod
    def _is_inMEM(GMS_objects, dataset):
        # type: (list, OrderedDict) -> bool
        """Checks whether a dataset within a dataset list has been processed in the previous processing level.
        :param GMS_objects: <list> a list of GMS objects that has been recently processed
        :param dataset:     <collections.OrderedDict> as generated by L0A_P.get_data_list_of_current_jobID()
        """
        # check if the scene ID of the given dataset is in the scene IDs of the previously processed datasets
        return dataset['scene_ID'] in [obj.scene_ID for obj in GMS_objects]

    def _get_processor_data_list(self, procLvl, prevLvl_objects=None):
        """Returns a list of datasets that have to be read from disk and then processed by a specific processor.

        :param procLvl:
        :param prevLvl_objects:
        :return:
        """
        def is_procL_lower(dataset):
            return HLP_F.is_proc_level_lower(dataset['proc_level'], target_lvl=procLvl)

        if prevLvl_objects is None:
            return [dataset for dataset in self.config.data_list if is_procL_lower(dataset)]  # TODO generator?
        else:
            return [dataset for dataset in self.config.data_list if is_procL_lower(dataset) and
                    not self._is_inMEM(prevLvl_objects + self.failed_objects, dataset)]

    def get_DB_objects(self, procLvl, prevLvl_objects=None, parallLev=None, blocksize=None):
        """
        Returns a list of GMS objects for datasets available on disk that have to be processed by the current processor.

        :param procLvl:         <str> processing level oof the current processor
        :param prevLvl_objects: <list> of in-mem GMS objects produced by the previous processor
        :param parallLev:       <str> parallelization level ('scenes' or 'tiles')
                                -> defines if full cubes or blocks are to be returned
        :param blocksize:       <tuple> block size in case blocks are to be returned, e.g. (2000,2000)
        :return:
        """
        # TODO get prevLvl_objects automatically from self
        if procLvl == 'L1A':
            return []
        else:
            # handle input parameters
            parallLev = parallLev or self.config.parallelization_level
            blocksize = blocksize or self.config.tiling_block_size_XY
            prevLvl = proc_chain[proc_chain.index(procLvl) - 1]  # TODO replace by enum

            # get GMSfile list
            dataset_dicts = self._get_processor_data_list(procLvl, prevLvl_objects)
            GMSfile_list_prevLvl_inDB = INP_R.get_list_GMSfiles(dataset_dicts, prevLvl)

            # create GMS objects from disk with respect to parallelization level and block size
            if parallLev == 'scenes':
                # get input parameters for creating GMS objects as full cubes
                work = [[GMS, ['cube', None]] for GMS in GMSfile_list_prevLvl_inDB]
            else:
                # define tile positions and size
                def get_tilepos_list(GMSfile):
                    return get_array_tilebounds(array_shape=INP_R.GMSfile2dict(GMSfile)['shape_fullArr'],
                                                tile_shape=blocksize)

                # get input parameters for creating GMS objects as blocks
                work = [[GMSfile, ['block', tp]] for GMSfile in GMSfile_list_prevLvl_inDB
                        for tp in get_tilepos_list(GMSfile)]

            # create GMS objects for the found files on disk
            # NOTE: DON'T multiprocess that with MAP(GMS_object(*initargs).from_disk, work)
            # in case of multiple subsystems GMS_object(*initargs) would always point to the same object in memory
            # -> subsystem attribute will be overwritten each time
            from ..misc.helper_functions import get_parentObjDict
            parentObjDict = get_parentObjDict()
            DB_objs = [parentObjDict[prevLvl].from_disk(tuple_GMS_subset=w) for w in work]

            if DB_objs:
                DB_objs = list(chain.from_iterable(DB_objs)) if list in [type(i) for i in DB_objs] else list(DB_objs)

            return DB_objs

    def run_all_processors(self, custom_data_list=None, serialize_after_each_mapper=False):
        """
        Run all processors at once.
        """
        # enable clean shutdown possibility
        # NOTE: a signal.SIGKILL (kill -9 ...) forces to kill the process and cannot be catched or handled
        signal.signal(signal.SIGINT, self.stop)  # catches a KeyboardInterrupt
        signal.signal(signal.SIGTERM, self.stop)  # catches a 'kill' or 'pkill'

        # noinspection PyBroadException
        try:
            if self.config.profiling:
                from pyinstrument import Profiler
                self.profiler = Profiler()  # or Profiler(use_signal=False), see below
                self.profiler.start()

            self.logger.info('Execution of entire GeoMultiSens pre-processing chain started for job ID %s...'
                             % self.config.ID)

            self.DB_job_record.reset_job_progress()  # updates attributes of DB_job_record and related DB entry
            self.config.status = 'running'
            GMS_object.proc_status_all_GMSobjs.clear()  # reset
            self.update_DB_job_record()  # TODO implement that into config.status.setter

            self.failed_objects = []

            # get list of datasets to be processed
            if custom_data_list:
                self.config.data_list = custom_data_list

            # add local availability
            self.config.data_list = self.add_local_availability(self.config.data_list)
            self.update_DB_job_statistics(self.config.data_list)

            if not serialize_after_each_mapper:
                # group dataset dicts by sceneid
                dataset_groups = HLP_F.group_dicts_by_key(self.config.data_list, key='scene_ID')

                # close logger to release FileHandler of job log (workers will log into job logfile)
                del self.logger

                # RUN PREPROCESSING
                from .pipeline import run_complete_preprocessing
                GMS_objs = imap_unordered(run_complete_preprocessing, dataset_groups, flatten_output=True)

                # separate results into successful and failed objects
                def assign_attr(tgt_procL):
                    return [obj for obj in GMS_objs if isinstance(obj, GMS_object) and obj.proc_level == tgt_procL]

                self.L1A_newObjects = assign_attr('L1A')
                self.L1B_newObjects = assign_attr('L1B')
                self.L1C_newObjects = assign_attr('L1C')
                self.L2A_newObjects = assign_attr('L2A')
                self.L2B_newObjects = assign_attr('L2B')
                self.L2C_newObjects = assign_attr('L2C')
                self.failed_objects = [obj for obj in GMS_objs if isinstance(obj, failed_GMS_object)]

            else:
                self.L1A_processing()
                self.L1B_processing()
                self.L1C_processing()
                self.L2A_processing()
                self.L2B_processing()
                self.L2C_processing()

            # create summary
            self.create_job_summary()

            self.logger.info('Execution finished.')
            self.logger.info('The job logfile, options file and the summary files have been saved here: \n'
                             '%s.*' % os.path.splitext(self.logger.path_logfile)[0])
            # TODO implement failed_with_warnings:
            self.config.status = 'finished' if not self.failed_objects else 'finished_with_errors'
            self.config.end_time = datetime.datetime.now()
            self.config.computation_time = self.config.end_time - self.config.start_time
            self.logger.info('Time for execution: %s' % self.config.computation_time)

        except Exception:  # noqa E722  # bare except
            self.config.status = 'failed'

            if not self.config.disable_exception_handler:
                self.logger.error('Execution failed with an error:', exc_info=True)
            else:
                self.logger.error('Execution failed with an error:')
                raise

        finally:
            # update database entry of current job
            self.update_DB_job_record()

            if self.config.profiling:
                self.profiler.stop()
                print(self.profiler.output_text(unicode=True, color=True))

            self.shutdown()

    def stop(self, signum, frame):
        """Interrupt the running process controller gracefully."""

        self.logger.info('Process controller stopped via %s.'
                         % ('KeyboardInterrupt' if signum == 2 else 'SIGTERM command'))
        self.config.status = 'canceled'
        self.update_DB_job_record()

        self.shutdown()

        if signum == 2:
            raise KeyboardInterrupt('Received a KeyboardInterrupt.')  # terminate execution and show traceback
        elif signum == 15:
            sys.exit(0)
            # raise SystemExit()

    def shutdown(self):
        """Shutdown the process controller instance (loggers, remove temporary directories, ...)."""
        self.logger.info('Shutting down gracefully...')

        # release unclosed locks
        release_unclosed_locks()

        # clear any temporary files
        tempdir = os.path.join(self.config.path_tempdir)
        self.logger.info('Deleting temporary directory %s.' % tempdir)
        if os.path.exists(tempdir):
            shutil.rmtree(tempdir, ignore_errors=True)

        del self.logger
        shutdown_loggers()

    def benchmark(self):
        """
        Run a benchmark.
        """
        data_list_bench = self.config.data_list
        for count_datasets in range(len(data_list_bench)):
            t_processing_all_runs, t_IO_all_runs = [], []
            for count_run in range(10):
                current_data_list = data_list_bench[0:count_datasets + 1]
                if os.path.exists(self.config.path_database):
                    os.remove(self.config.path_database)
                t_start = time.time()
                self.run_all_processors(current_data_list)
                t_processing_all_runs.append(time.time() - t_start)
                t_IO_all_runs.append(globals()['time_IO'])

            assert current_data_list, 'Empty data list.'
            OUT_W.write_global_benchmark_output(t_processing_all_runs, t_IO_all_runs, current_data_list)

    def L1A_processing(self):
        """
        Run Level 1A processing: Data import and metadata homogenization
        """
        if self.config.exec_L1AP[0]:
            self.logger.info('\n\n##### Level 1A Processing started - raster format and metadata homogenization ####\n')

            datalist_L1A_P = self._get_processor_data_list('L1A')

            if self.config.parallelization_level == 'scenes':
                # map
                L1A_resObjects = MAP(L1A_map, datalist_L1A_P, CPUs=12)
            else:  # tiles
                all_L1A_tiles_map1 = MAP(L1A_map_1, datalist_L1A_P,
                                         flatten_output=True)  # map_1 # merge results to new list of splits

                L1A_obj_tiles = MAP(L1A_map_2, all_L1A_tiles_map1)  # map_2
                grouped_L1A_Tiles = HLP_F.group_objects_by_attributes(
                    L1A_obj_tiles, 'scene_ID', 'subsystem')  # group results

                L1A_objects = MAP(L1A_P.L1A_object.from_tiles, grouped_L1A_Tiles)  # reduce

                L1A_resObjects = MAP(L1A_map_3, L1A_objects)  # map_3

            self.L1A_newObjects = [obj for obj in L1A_resObjects if isinstance(obj, L1A_P.L1A_object)]
            self.failed_objects += [obj for obj in L1A_resObjects if isinstance(obj, failed_GMS_object) and
                                    obj.scene_ID not in self.sceneids_failed]

        return self.L1A_newObjects

    def L1B_processing(self):
        """
        Run Level 1B processing: calculation of geometric shifts
        """
        # TODO implement check for running spatial index mediator server
        # run on full cubes

        if self.config.exec_L1BP[0]:
            self.logger.info('\n\n####### Level 1B Processing started - detection of geometric displacements #######\n')

            L1A_DBObjects = self.get_DB_objects('L1B', self.L1A_newObjects, parallLev='scenes')
            L1A_Instances = self.L1A_newObjects + L1A_DBObjects  # combine newly and earlier processed L1A data

            L1B_resObjects = MAP(L1B_map, L1A_Instances)

            self.L1B_newObjects = [obj for obj in L1B_resObjects if isinstance(obj, L1B_P.L1B_object)]
            self.failed_objects += [obj for obj in L1B_resObjects if isinstance(obj, failed_GMS_object) and
                                    obj.scene_ID not in self.sceneids_failed]

        return self.L1B_newObjects

    def L1C_processing(self):
        """
        Run Level 1C processing: atmospheric correction
        """
        if self.config.exec_L1CP[0]:
            self.logger.info('\n\n############## Level 1C Processing started - atmospheric correction ##############\n')

            if self.config.parallelization_level == 'scenes':
                L1B_DBObjects = self.get_DB_objects('L1C', self.L1B_newObjects)
                L1B_Instances = self.L1B_newObjects + L1B_DBObjects  # combine newly and earlier processed L1B data

                # group by scene ID (all subsystems belonging to the same scene ID must be processed together)
                grouped_L1B_Instances = HLP_F.group_objects_by_attributes(L1B_Instances, 'scene_ID')

                L1C_resObjects = MAP(L1C_map, grouped_L1B_Instances, flatten_output=True,
                                     CPUs=15)  # FIXME CPUs set to 15 for testing

            else:  # tiles
                raise NotImplementedError("Tiled processing is not yet completely implemented for L1C processor. Use "
                                          "parallelization level 'scenes' instead!")
                # blocksize = (5000, 5000)
                # """if newly processed L1A objects are present: cut them into tiles"""
                # L1B_newTiles = []
                # if self.L1B_newObjects:
                #     tuples_obj_blocksize = [(obj, blocksize) for obj in self.L1B_newObjects]
                #     L1B_newTiles = MAP(HLP_F.cut_GMS_obj_into_blocks, tuples_obj_blocksize, flatten_output=True)
                #
                # """combine newly and earlier processed L1B data"""
                # L1B_newDBTiles = self.get_DB_objects('L1C', self.L1B_newObjects, blocksize=blocksize)
                # L1B_tiles = L1B_newTiles + L1B_newDBTiles
                #
                # # TODO merge subsets of S2/Aster in order to provide all bands for atm.correction
                # L1C_tiles = MAP(L1C_map, L1B_tiles)
                # grouped_L1C_Tiles = \
                #     HLP_F.group_objects_by_attributes(L1C_tiles, 'scene_ID', 'subsystem')  # group results
                # [L1C_tiles_group[0].delete_tempFiles() for L1C_tiles_group in grouped_L1C_Tiles]
                # L1C_resObjects = MAP(L1C_P.L1C_object().from_tiles, grouped_L1C_Tiles)  # reduce

            self.L1C_newObjects = [obj for obj in L1C_resObjects if isinstance(obj, L1C_P.L1C_object)]
            self.failed_objects += [obj for obj in L1C_resObjects if isinstance(obj, failed_GMS_object) and
                                    obj.scene_ID not in self.sceneids_failed]

        return self.L1C_newObjects

    def L2A_processing(self):
        """
        Run Level 2A processing: geometric homogenization
        """
        if self.config.exec_L2AP[0]:
            self.logger.info(
                '\n\n#### Level 2A Processing started - shift correction / geometric homogenization ####\n')

            """combine newly and earlier processed L1C data"""
            L1C_DBObjects = self.get_DB_objects('L2A', self.L1C_newObjects, parallLev='scenes')
            L1C_Instances = self.L1C_newObjects + L1C_DBObjects  # combine newly and earlier processed L1C data

            # group by scene ID (all subsystems belonging to the same scene ID must be processed together)
            grouped_L1C_Instances = HLP_F.group_objects_by_attributes(L1C_Instances, 'scene_ID')

            L2A_resTiles = MAP(L2A_map, grouped_L1C_Instances, flatten_output=True)

            self.L2A_tiles = [obj for obj in L2A_resTiles if isinstance(obj, L2A_P.L2A_object)]
            self.failed_objects += [obj for obj in L2A_resTiles if isinstance(obj, failed_GMS_object) and
                                    obj.scene_ID not in self.sceneids_failed]

        return self.L2A_tiles

    def L2B_processing(self):
        """
        Run Level 2B processing: spectral homogenization
        """
        if self.config.exec_L2BP[0]:
            self.logger.info('\n\n############# Level 2B Processing started - spectral homogenization ##############\n')

            if self.config.parallelization_level == 'scenes':
                # don't know if scenes makes sense in L2B processing because full objects are very big!
                """if newly processed L2A objects are present: merge them to scenes"""
                grouped_L2A_Tiles = HLP_F.group_objects_by_attributes(self.L2A_tiles, 'scene_ID')  # group results
                # reduce # will be too slow because it has to pickle back really large L2A_newObjects
                # L2A_newObjects  = MAP(HLP_F.merge_GMS_tiles_to_GMS_obj, grouped_L2A_Tiles)
                L2A_newObjects = [L2A_P.L2A_object.from_tiles(tileList) for tileList in grouped_L2A_Tiles]

                """combine newly and earlier processed L2A data"""
                L2A_DBObjects = self.get_DB_objects('L2B', self.L2A_tiles)
                L2A_Instances = L2A_newObjects + L2A_DBObjects  # combine newly and earlier processed L2A data

                L2B_resObjects = MAP(L2B_map, L2A_Instances)

            else:  # tiles
                L2A_newTiles = self.L2A_tiles  # tiles have the block size specified in L2A_map_2

                """combine newly and earlier processed L2A data"""
                blocksize = (2048, 2048)  # must be equal to the blocksize of L2A_newTiles specified in L2A_map_2
                L2A_newDBTiles = self.get_DB_objects('L2B', self.L2A_tiles, blocksize=blocksize)
                L2A_tiles = L2A_newTiles + L2A_newDBTiles

                L2B_tiles = MAP(L2B_map, L2A_tiles)

                # group results # FIXME nötig an dieser Stelle?
                grouped_L2B_Tiles = HLP_F.group_objects_by_attributes(L2B_tiles, 'scene_ID')
                [L2B_tiles_group[0].delete_tempFiles() for L2B_tiles_group in grouped_L2B_Tiles]

                L2B_resObjects = [L2B_P.L2B_object.from_tiles(tileList) for tileList in grouped_L2B_Tiles]

            self.L2B_newObjects = [obj for obj in L2B_resObjects if isinstance(obj, L2B_P.L2B_object)]
            self.failed_objects += [obj for obj in L2B_resObjects if isinstance(obj, failed_GMS_object) and
                                    obj.scene_ID not in self.sceneids_failed]

        return self.L2B_newObjects

    def L2C_processing(self):
        """
        Run Level 2C processing: accurracy assessment and MGRS tiling
        """
        # FIXME only parallelization_level == 'scenes' implemented
        if self.config.exec_L2CP[0]:
            self.logger.info('\n\n########## Level 2C Processing started - calculation of quality layers ###########\n')

            """combine newly and earlier processed L2A data"""
            L2B_DBObjects = self.get_DB_objects('L2C', self.L2B_newObjects, parallLev='scenes')
            L2B_Instances = self.L2B_newObjects + L2B_DBObjects  # combine newly and earlier processed L2A data

            L2C_resObjects = MAP(L2C_map, L2B_Instances, CPUs=8)  # FIXME 8 workers due to heavy IO
            # FIXME in case of inmem_serialization mode results are too big to be back-pickled
            self.L2C_newObjects = [obj for obj in L2C_resObjects if isinstance(obj, L2C_P.L2C_object)]
            self.failed_objects += [obj for obj in L2C_resObjects if isinstance(obj, failed_GMS_object) and
                                    obj.scene_ID not in self.sceneids_failed]

        return self.L2C_newObjects

    def update_DB_job_record(self):
        """
        Update the database records of the current job (table 'jobs').
        """
        # TODO move this method to config.Job
        # update 'failed_sceneids' column of job record within jobs table
        sceneids_failed = list(set([obj.scene_ID for obj in self.failed_objects]))
        DB_T.update_records_in_postgreSQLdb(
            self.config.conn_database, 'jobs',
            {'failed_sceneids': sceneids_failed,  # update 'failed_sceneids' column
             'finishtime': self.config.end_time,  # add job finish timestamp
             'status': self.config.status},  # update 'job_status' column
            {'id': self.config.ID}, timeout=30000)

    def update_DB_job_statistics(self, usecase_datalist):
        """
        Update job statistics of the running job in the database.
        """
        # TODO move this method to config.Job
        already_updated_IDs = []
        for ds in usecase_datalist:
            if ds['proc_level'] is not None and ds['scene_ID'] not in already_updated_IDs:
                # update statistics column of jobs table
                DB_T.increment_decrement_arrayCol_in_postgreSQLdb(
                    self.config.conn_database, 'jobs', 'statistics', cond_dict={'id': self.config.ID},
                    idx_val2decrement=db_jobs_statistics_def['pending'],
                    idx_val2increment=db_jobs_statistics_def[ds['proc_level']],
                    timeout=30000)

                # avoid double updating in case of subsystems belonging to the same scene ID
                already_updated_IDs.append(ds['scene_ID'])

    def create_job_summary(self):
        """
        Create job success summary
        """

        # get objects with highest requested processing level
        highest_procL_Objs = []
        for pL in reversed(proc_chain):
            if getattr(self.config, 'exec_%sP' % pL)[0]:
                highest_procL_Objs = \
                    getattr(self, '%s_newObjects' % pL) if pL != 'L2A' else (self.L2A_tiles or self.L2A_newObjects)
                break

        gms_objects2summarize = highest_procL_Objs + self.failed_objects
        if gms_objects2summarize:
            # create summaries
            detailed_JS, quick_JS = get_job_summary(gms_objects2summarize)
            detailed_JS.to_excel(os.path.join(self.config.path_job_logs, '%s_summary.xlsx' % self.config.ID))
            detailed_JS.to_csv(os.path.join(self.config.path_job_logs, '%s_summary.csv' % self.config.ID), sep='\t')
            self.logger.info('\nQUICK JOB SUMMARY (ID %s):\n' % self.config.ID + quick_JS.to_string())

            self.summary_detailed = detailed_JS
            self.summary_quick = quick_JS

        else:
            # TODO implement check if proc level with lowest procL has to be processed at all (due to job.exec_L1X)
            # TODO otherwise it is possible that get_job_summary receives an empty list
            self.logger.warning("Job summary skipped because get_job_summary() received an empty list of GMS objects.")

    def clear_lists_procObj(self):
        self.failed_objects = []
        self.L1A_newObjects = []
        self.L1B_newObjects = []
        self.L1C_newObjects = []
        self.L2A_tiles = []
        self.L2B_newObjects = []
        self.L2C_newObjects = []


def get_job_summary(list_GMS_objects):
    # get detailed job summary
    DJS_cols = ['GMS_object', 'scene_ID', 'entity_ID', 'satellite', 'sensor', 'subsystem', 'image_type', 'proc_level',
                'arr_shape', 'arr_pos', 'failedMapper', 'ExceptionType', 'ExceptionValue', 'ExceptionTraceback']
    DJS = DataFrame(columns=DJS_cols)
    DJS['GMS_object'] = list_GMS_objects

    for col in DJS_cols[1:]:
        def get_val(obj): return getattr(obj, col) if hasattr(obj, col) else None
        DJS[col] = list(DJS['GMS_object'].map(get_val))

    del DJS['GMS_object']
    DJS = DJS.sort_values(by=['satellite', 'sensor', 'entity_ID'])

    # get quick job summary
    QJS = DataFrame(columns=['satellite', 'sensor', 'count', 'proc_successfully', 'proc_failed'])
    all_sat, all_sen = zip(*[i.split('__') for i in (np.unique(DJS['satellite'] + '__' + DJS['sensor']))])
    QJS['satellite'] = all_sat
    QJS['sensor'] = all_sen
    # count objects with the same satellite/sensor/sceneid combination
    QJS['count'] = [len(DJS[(DJS['satellite'] == sat) & (DJS['sensor'] == sen)]['scene_ID'].unique())
                    for sat, sen in zip(all_sat, all_sen)]
    QJS['proc_successfully'] = [len(DJS[(DJS['satellite'] == sat) &
                                        (DJS['sensor'] == sen) &
                                        (DJS['failedMapper'].isnull())]['scene_ID'].unique())
                                for sat, sen in zip(all_sat, all_sen)]
    QJS['proc_failed'] = QJS['count'] - QJS['proc_successfully']
    QJS = QJS.sort_values(by=['satellite', 'sensor'])
    return DJS, QJS
