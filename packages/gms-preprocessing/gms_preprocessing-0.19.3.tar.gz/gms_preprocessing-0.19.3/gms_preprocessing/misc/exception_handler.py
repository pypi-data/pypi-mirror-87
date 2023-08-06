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
import functools
import shutil
import sys
import traceback
import warnings
from logging import getLogger
from typing import Union, List, TYPE_CHECKING  # noqa F401  # flake8 issue

from ..options.config import GMS_config as CFG
from ..misc import database_tools as DB_T
from ..misc.helper_functions import is_proc_level_lower
from .definition_dicts import db_jobs_statistics_def, proc_chain

if TYPE_CHECKING:
    from ..model.gms_object import GMS_object  # noqa F401  # flake8 issue
    from ..model.gms_object import failed_GMS_object

__author__ = 'Daniel Scheffler'


def trace_unhandled_exceptions(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        result = None

        # noinspection PyBroadException
        try:
            result = func(*args, **kwargs)
        except Exception:
            print('Exception in ' + func.__name__)
            traceback.print_exc()
        return result

    return wrapped_func


class ExceptionHandler(object):
    def __init__(self, logger=None):
        self.GMS_objs = None  # type: Union[List[GMS_object], GMS_object, collections.OrderedDict, failed_GMS_object]
        self.GMS_mapper_name = ''
        self.GMS_mapper_failed = False
        self._exc_details = None
        self._logger = logger

    @property
    def logger(self):
        if not self._logger:
            self._logger = getLogger('ExceptionHandler')
            self._logger.setLevel(CFG.log_level)
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    def __call__(self, GMS_mapper):
        self.log_uncaught_exceptions(GMS_mapper)

    def log_uncaught_exceptions(self, GMS_mapper):
        """Decorator function for handling unexpected exceptions that occurr within GMS mapper functions. Traceback is
        sent to logfile of the respective GMS object and the scene ID is added to the 'failed_sceneids' column
        within the jobs table of the postgreSQL database.

        :param GMS_mapper:  A GMS mapper function that takes a GMS object, does some processing and returns it back.
        """

        @functools.wraps(GMS_mapper)  # needed to avoid pickling errors
        def wrapped_GMS_mapper(GMS_objs, **kwargs):
            # type: (Union[List[GMS_object], GMS_object, collections.OrderedDict, failed_GMS_object], dict) -> Union[GMS_object, List[GMS_object], failed_GMS_object]  # noqa
            """

            :param GMS_objs: one OR multiple instances of GMS_object or one instance of failed_object
            :param kwargs:
            :return:
            """

            self.GMS_mapper_name = GMS_mapper.__name__
            self.GMS_objs = GMS_objs

            if not GMS_objs:
                return GMS_objs

            # noinspection PyBroadException
            try:
                # GMS_mapper inputs CONTAIN NO failed_GMS_objects -> run the mapper normally
                if not self.is_failed(self.GMS_objs):
                    self.update_progress_started()

                    # run the mapper function and store its results
                    self.GMS_objs = GMS_mapper(GMS_objs, **kwargs)

                    self.increment_progress()

                # GMS_mapper inputs CONTAIN failed_GMS_objects -> log and return mapper inputs as received
                else:
                    GMS_obj = self.get_sample_GMS_obj(self.GMS_objs)  # failed_GMS_object
                    # FIXME in case self.GMS_objs is a list and the failed object is not at first position
                    # FIXME GMS_obj.failedMapper will not work
                    print("Scene %s (entity ID %s) skipped %s due to an unexpected exception in %s."
                          % (GMS_obj.scene_ID, GMS_obj.entity_ID, self.GMS_mapper_name,
                             GMS_obj.failedMapper))  # TODO should be logged by PC.logger

                return self.GMS_objs  # Union[GMS_object, List[GMS_object]]

            except OSError:
                _, exc_val, _ = self.exc_details

                if exc_val.strerror == 'Input/output error':
                    # check free disk space
                    usageNamedTuple = shutil.disk_usage(CFG.path_fileserver)
                    percent_free = usageNamedTuple.free / usageNamedTuple.total
                    gigabytes_free = usageNamedTuple.free / (1024 ** 3)
                    if usageNamedTuple.free / usageNamedTuple.total < 0.025:
                        self.logger.warning('\nCatched an unexpected IO error and FREE DISK SPACE IS ONLY %.2f percent '
                                            '(~%.1f GB)!' % (percent_free * 100, gigabytes_free))

                elif CFG.disable_exception_handler:
                    raise
                else:
                    return self.handle_failed()  # failed_GMS_object

            except Exception:
                if CFG.disable_exception_handler:
                    raise
                else:
                    return self.handle_failed()  # failed_GMS_object

        return wrapped_GMS_mapper

    @property
    def exc_details(self):
        if not self._exc_details:
            type_, value_ = sys.exc_info()[:2]
            traceback_ = traceback.format_exc()
            self._exc_details = type_, value_, traceback_
        return self._exc_details

    @staticmethod
    def is_failed(GMS_objs):
        from ..model.gms_object import failed_GMS_object
        return isinstance(GMS_objs, failed_GMS_object) or \
            (isinstance(GMS_objs, list) and isinstance(GMS_objs[0], failed_GMS_object))

    @staticmethod
    def get_sample_GMS_obj(GMS_objs):
        # type: (Union[list, tuple, collections.OrderedDict, failed_GMS_object]) -> Union[GMS_object, failed_GMS_object]
        return \
            GMS_objs if isinstance(GMS_objs, collections.OrderedDict) else \
            GMS_objs[0] if isinstance(GMS_objs, (list, tuple)) else GMS_objs

    def update_progress_started(self):
        """in case of just initialized objects:
        update statistics column in jobs table of postgreSQL database to 'started'"""
        if isinstance(self.GMS_objs, collections.OrderedDict) and self.GMS_objs['proc_level'] is None:

            if not self.GMS_objs['subsystem'] or self.GMS_objs['subsystem'] in ['VNIR1', 'S2A10', 'S2B10']:
                self.logger.debug("Setting job statistics array to 'STARTED'.")

                # update statistics column ONLY in case of full cube or first subsystem
                DB_T.increment_decrement_arrayCol_in_postgreSQLdb(
                    CFG.conn_database, 'jobs', 'statistics', cond_dict={'id': CFG.ID},
                    idx_val2decrement=db_jobs_statistics_def['pending'],
                    idx_val2increment=db_jobs_statistics_def['started'],
                    timeout=30000)

    def increment_progress(self):
        """Update statistics column in jobs table of postgreSQL database.

        NOTE: This function ONLY receives those GMS_objects that have been sucessfully processed by the GMS_mapper.
        """
        # get a GMS object from which we get the new proc_level
        GMS_obj = self.get_sample_GMS_obj(self.GMS_objs)

        # validate proc_level
        if GMS_obj.proc_level is None:
            raise ValueError('Received GMS_object for %s %s without processing level after being processed by %s.'
                             % (GMS_obj.entity_ID, GMS_obj.subsystem, self.GMS_mapper_name))

        # NOTE: in case GMS_obj represents a subsystem and another one has already been marked as FAILED the
        # failed_sceneids column and the statistics column is NOT updated once more
        # check if another subsystem of the same scene ID already failed - don't increment the stats anymore
        if not GMS_obj.subsystem or GMS_obj.subsystem in ['VNIR1', 'S2A10', 'S2B10']:
            another_ss_failed = False

            if GMS_obj.subsystem:
                # check if another subsystem of the same scene ID has been marked as failed before
                res = DB_T.get_info_from_postgreSQLdb(CFG.conn_database, 'jobs', ['failed_sceneids'],
                                                      {'id': CFG.ID})
                assert res, "Query delivered no result."

                if res[0][0] is not None and GMS_obj.scene_ID in res[0][0]:
                    self.logger.debug("Found another failed subsystem of scene %s in the database.")
                    another_ss_failed = True

            # update statistics column ONLY in case of full cube or first subsystem and if no other subsystem failed
            if not another_ss_failed:
                self.logger.debug("Decrementing job statistics array for %s objects."
                                  % proc_chain[proc_chain.index(GMS_obj.proc_level) - 1])
                self.logger.debug("Incrementing job statistics array for %s objects." % GMS_obj.proc_level)

                DB_T.increment_decrement_arrayCol_in_postgreSQLdb(
                    CFG.conn_database, 'jobs', 'statistics', cond_dict={'id': CFG.ID},
                    idx_val2decrement=db_jobs_statistics_def[GMS_obj.proc_level] - 1,
                    idx_val2increment=db_jobs_statistics_def[GMS_obj.proc_level],
                    timeout=30000)

    @staticmethod
    def update_progress_failed(failed_Obj, procL_failed=None):
        """Update statistics column in jobs table of postgreSQL database.

        :param failed_Obj:      instance of gms_object failed_GMS_object
        :param procL_failed:    processing level to be decremented. If not given, the one from failed_Obj is used.
        :return:
        """
        DB_T.increment_decrement_arrayCol_in_postgreSQLdb(
            CFG.conn_database, 'jobs', 'statistics', cond_dict={'id': CFG.ID},
            idx_val2decrement=db_jobs_statistics_def[procL_failed or failed_Obj.proc_level],
            idx_val2increment=db_jobs_statistics_def['FAILED'],
            timeout=30000)

    def handle_failed(self):
        from ..model.gms_object import failed_GMS_object

        try:
            _, exc_val, exc_tb = self.exc_details

            # collect some informations about failed GMS object and summarize them in failed_GMS_object
            failed_Obj = failed_GMS_object(self.get_sample_GMS_obj(self.GMS_objs),
                                           self.GMS_mapper_name, *self.exc_details)

            # log the exception and raise warning
            failed_Obj.logger.error('\n' + exc_tb, exc_info=False)
            self.logger.warning("\nLogged an uncaught exception within %s during processing of scene ID %s "
                                "(entity ID %s):\n '%s'\n"
                                % (self.GMS_mapper_name, failed_Obj.scene_ID, failed_Obj.entity_ID, exc_val))

            # add the scene ID to failed_sceneids column in jobs table of DB and update statistics column
            # NOTE: in case failed_Obj represents a subsystem and another one has already been marked as FAILED the
            # failed_sceneids column and the statistics column is NOT updated once more

            another_ss_failed = False
            another_ss_succeeded = False
            higher_procL = None

            if failed_Obj.subsystem:
                # check if another subsystem of the same scene ID has been marked as failed before
                res = DB_T.get_info_from_postgreSQLdb(CFG.conn_database, 'jobs', ['failed_sceneids'], {'id': CFG.ID})
                assert res, "Query delivered no result."

                if res[0][0] is not None and failed_Obj.scene_ID in res[0][0]:
                    self.logger.debug("Found another failed subsystem of scene %s in the database.")
                    another_ss_failed = True

                # check if another subsystem already reached a higher processing level
                # NOTE: this fixes issue #50
                # NOTE: This works not only for GMS_object instances but also for L1A inputs (OrderedDicts) because
                #       failed_GMS_object inherits from GMS_object and GMS_object.proc_status_all_GMS_objs has already
                #       been updated by the first subsystem (that earlier reached L1A)
                # FIXME proc_status_all_GMSobjs is not available if other subsystems are processed by another
                # FIXME multiprocessing worker or on another machine (cluster node)
                from ..model.gms_object import GMS_object

                procstatus_other_ss = {k: v for k, v in GMS_object.proc_status_all_GMSobjs[failed_Obj.scene_ID].items()
                                       if k != failed_Obj.subsystem}
                for ss, statusentry in procstatus_other_ss.items():
                    for procL in statusentry.keys():
                        if is_proc_level_lower(failed_Obj.proc_level, procL) and statusentry[procL] == 'finished':
                            higher_procL = procL
                            self.logger.debug("Found another subsystem that already reached a higher processing level.")
                            another_ss_succeeded = True
                            break

            if not another_ss_failed:  # applies also to full cubes
                DB_T.append_item_to_arrayCol_in_postgreSQLdb(CFG.conn_database, 'jobs',
                                                             {'failed_sceneids': failed_Obj.scene_ID}, {'id': CFG.ID})

                if not another_ss_succeeded:
                    self.update_progress_failed(failed_Obj)
                else:
                    self.update_progress_failed(failed_Obj, procL_failed=higher_procL)

            return failed_Obj

        except Exception:
            # raise exceptions that occurr during self.handle_failed() -> must be ProgrammingErrors
            raise


def log_uncaught_exceptions(GMS_mapper, logger=None):
    exc_handler = ExceptionHandler(logger=logger)
    return exc_handler.log_uncaught_exceptions(GMS_mapper)


def ignore_warning(warning_type):
    """A decorator to ignore a specific warning when executing a function.

    :param warning_type:    the type of the warning to ignore
    """

    def _ignore_warning(func):
        @functools.wraps(func)
        def __ignore_warning(*args, **kwargs):
            with warnings.catch_warnings(record=True):
                # Catch all warnings of this type
                warnings.simplefilter('always', warning_type)
                # Execute the function
                result = func(*args, **kwargs)

            return result

        return __ignore_warning

    return _ignore_warning
