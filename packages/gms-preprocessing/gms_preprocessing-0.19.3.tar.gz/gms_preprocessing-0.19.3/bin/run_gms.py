#!/usr/bin/env python
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

__author__ = 'Daniel Scheffler'

import argparse
import warnings
import os

import matplotlib

matplotlib.use('Agg')  # switch matplotlib backend to 'Agg' and disable warning in case its already 'Agg'

from gms_preprocessing import ProcessController, __version__  # noqa: E402
from gms_preprocessing.misc.database_tools import GMS_JOB  # noqa: E402
from gms_preprocessing.options.config import get_conn_database  # noqa: E402
from gms_preprocessing.options.config import path_options_default  # noqa: E402
from gms_preprocessing.options.config import get_options  # noqa: E402
from gms_preprocessing.options.options_schema import get_param_from_json_config  # noqa: E402

options_default = get_options(path_options_default, validation=True)  # type: dict


def parsedArgs_to_user_opts(cli_args):
    # type: (argparse.Namespace) -> dict
    """Convert argparse Namespace object to dictionary of explicitly given parameters.

    NOTE:   All options that have not been given explicitly (None values) are removed. Reason: all options to
            passed set_config WILL OVERRIDE job settings read from the GMS database (e.g., specified by the WebUI)
            => only override job configuration defined by WebUI if CLI options are explicitly given
            => if json_opts are given: configuration defined by WebUI will be overridden by this json config in any case

    :param cli_args:    options as parsed by the argparse.ArgumentParser
    """

    # convert argparse Namespace object to dictionary
    opts = {k: v for k, v in vars(cli_args).items() if not k.startswith('_') and k != 'func'}

    # remove those options that have not been given explicitly (None values)
    user_opts = dict()
    for k, v in opts.items():
        # values are None if they are not given by the user -> don't pass to set_config
        if v is None:
            continue

        # remove keys that are not to be passed to set_config
        elif k in ['jobid', 'sceneids', 'entityids', 'filenames', 'comment', ]:
            continue

        else:
            user_opts.update({k: v})

    return user_opts


def run_from_jobid(args):
    # TODO distinguish between ID of a master, processing or download job
    # TODO master: find corresponding sub-jobs and run them
    # TODO processing: check for not downloaded scenes and run processing after download
    # TODO download: run only the downloader

    # set up process controller instance
    kwargs = parsedArgs_to_user_opts(args)

    if 'GMS_IS_TEST' in os.environ and os.environ['GMS_IS_TEST'] == 'True':
        kwargs['is_test'] = True

    PC = ProcessController(args.jobid, **kwargs)

    # run the job
    if 'GMS_IS_TEST_CONFIG' in os.environ and os.environ['GMS_IS_TEST_CONFIG'] == 'True':
        # in case of software test, it is enough to get an instance of process controller because all inputs are
        # validated within options.config.Job_Config (indirectly called by ProcessController.__init__() )
        pass
    else:
        PC.run_all_processors()


def run_from_sceneids(args):
    # create and run a download job
    warnings.warn('Currently the console argument parser expects the given scenes as already downloaded.')  # TODO

    # create a new processing job from scene IDs
    dbJob = GMS_JOB(get_conn_database(args.db_host))
    dbJob.from_sceneIDlist(list_sceneIDs=args.sceneids,
                           virtual_sensor_id=get_user_input_or_default('virtual_sensor_id', args),
                           datasetid_spatial_ref=get_user_input_or_default('datasetid_spatial_ref', args),
                           comment=args.comment)
    _run_job(dbJob, **parsedArgs_to_user_opts(args))


def run_from_entityids(args):
    """Create a new job from entity IDs.

    :param args:
    :return:
    """
    dbJob = GMS_JOB(get_conn_database(args.db_host))
    dbJob.from_entityIDlist(list_entityids=args.entityids,
                            virtual_sensor_id=get_user_input_or_default('virtual_sensor_id', args),
                            datasetid_spatial_ref=get_user_input_or_default('datasetid_spatial_ref', args),
                            comment=args.comment)
    _run_job(dbJob, **parsedArgs_to_user_opts(args))


def run_from_filenames(args):
    """Create a new GMS job from filenames of downloaded archives and run it!

    :param args:
    :return:
    """
    dbJob = GMS_JOB(get_conn_database(args.db_host))
    dbJob.from_filenames(list_filenames=args.filenames,
                         virtual_sensor_id=get_user_input_or_default('virtual_sensor_id', args),
                         datasetid_spatial_ref=get_user_input_or_default('datasetid_spatial_ref', args),
                         comment=args.comment)
    _run_job(dbJob, **parsedArgs_to_user_opts(args))


def run_from_constraints(args):
    # create a new job from constraints
    # TODO
    raise NotImplementedError


def _run_job(dbJob, **config_kwargs):
    # type: (GMS_JOB, dict) -> None
    """

    :param dbJob:
    :return:
    """
    # create a database record for the given job
    dbJob.create()

    # set up process controller instance
    if 'GMS_IS_TEST' in os.environ and os.environ['GMS_IS_TEST'] == 'True':
        config_kwargs['is_test'] = True

    PC = ProcessController(dbJob.id, **config_kwargs)

    # run the job
    if 'GMS_IS_TEST_CONFIG' in os.environ and os.environ['GMS_IS_TEST_CONFIG'] == 'True':
        # in case of software test, it is enough to get an instance of process controller because all inputs are
        # validated within options.config.Job_Config (indirectly called by ProcessController.__init__() )
        pass
    else:
        PC.run_all_processors()


def get_user_input_or_default(paramname, argsparse_ns):
    user_input = getattr(argsparse_ns, paramname)

    return user_input if user_input is not None else \
        get_param_from_json_config(paramname, options_default)


def get_gms_argparser():
    """Return argument parser for run_gms.py program."""

    ##################################################################
    # CONFIGURE MAIN PARSER FOR THE GEOMULTISENS PREPROCESSING CHAIN #
    ##################################################################

    parser = argparse.ArgumentParser(
        prog='run_gms.py',
        description='=' * 70 + '\n' + 'GeoMultiSens preprocessing console argument parser. '
                                      'Python implementation by Daniel Scheffler (daniel.scheffler@gfz-potsdam.de)',
        epilog="The argument parser offers multiple sub-argument parsers (jobid, sceneids, ...) for starting GMS jobs. "
               "use '>>> python /path/to/gms_preprocessing/run_gms.py <sub-parser> -h' for detailed documentation and "
               "usage hints.")

    parser.add_argument('--version', action='version', version=__version__)

    #################################################################
    # CONFIGURE SUBPARSERS FOR THE GEOMULTISENS PREPROCESSING CHAIN #
    #################################################################

    ##############################################
    # define parsers containing common arguments #
    ##############################################

    general_opts_parser = argparse.ArgumentParser(add_help=False)
    gop_p = general_opts_parser.add_argument

    gop_p('-jc', '--json_config', nargs='?', type=str,
          help='file path of a JSON file containing options. See here for an example: '
               'https://gitext.gfz-potsdam.de/geomultisens/gms_preprocessing/'
               'blob/master/gms_preprocessing/options/options_default.json')

    # '-exec_L1AP': dict(nargs=3, type=bool, help="L1A Processor configuration",
    #                   metavar=tuple("[run processor, write output, delete output]".split(' ')), default=[1, 1, 1]),

    gop_p('-DH', '--db_host', nargs='?', type=str,
          default='localhost',  # hardcoded here because default json is read from database and host must be available
          help='host name of the server that runs the postgreSQL database')

    # NOTE: don't define any defaults here for parameters that are passed to set_config!
    #       -> otherwise, we cannot distinguish between explicity given parameters and default values
    #       => see docs in parsedArgs_to_user_opts() for explanation
    gop_p('-DOO', '--delete_old_output', nargs='?', type=bool, default=None,
          help='delete previously created output of the given job ID before running the job')

    gop_p('-vid', '--virtual_sensor_id', type=int, default=None,
          help='ID of the target (virtual) sensor')

    gop_p('-dsid_spat', '--datasetid_spatial_ref', type=int, default=None,
          help='dataset ID of the spatial reference')

    gop_p('--CPUs', type=int, default=None,
          help='number of CPU cores to be used for processing (default: "None" -> use all available')

    gop_p('-c', '--comment', nargs='?', type=str,
          default='',
          help='comment concerning the job')

    ##################
    # add subparsers #
    ##################

    subparsers = parser.add_subparsers()

    parser_jobid = subparsers.add_parser(
        'jobid', parents=[general_opts_parser],
        description='Run a GeoMultiSens preprocessing job using an already existing job ID.',
        help="Run a GeoMultiSens preprocessing job using an already existing job ID (Sub-Parser).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser_sceneids = subparsers.add_parser(
        'sceneids', parents=[general_opts_parser],
        description='Run a GeoMultiSens preprocessing job for a given list of scene IDs.',
        help="Run a GeoMultiSens preprocessing job for a given list of scene IDs (Sub-Parser).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser_entityids = subparsers.add_parser(
        'entityids', parents=[general_opts_parser],
        description='Run a GeoMultiSens preprocessing job for a given list of entity IDs.',
        help="Run a GeoMultiSens preprocessing job for a given list of entity IDs (Sub-Parser).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser_filenames = subparsers.add_parser(
        'filenames', parents=[general_opts_parser],
        description='Run a GeoMultiSens preprocessing job for a given list of filenames of '
                    'downloaded satellite image archives!',
        help="Run a GeoMultiSens preprocessing job for a given list of filenames of downloaded satellite "
             "image archives! (Sub-Parser).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser_constraints = subparsers.add_parser(
        'constraints', parents=[general_opts_parser],
        description='Run a GeoMultiSens preprocessing job matching the given constraints.',
        help="Run a GeoMultiSens preprocessing job matching the given constraints (Sub-Parser).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    #################
    # ADD ARGUMENTS #
    #################

    ##########################
    # add indivial arguments #
    ##########################

    # add arguments to parser_jobid
    jid_p = parser_jobid.add_argument
    jid_p('jobid', type=int, help='job ID of an already created GeoMultiSens preprocessing job '
                                  '(must be present in the jobs table of the database)')

    # add arguments to parser_sceneids
    sid_p = parser_sceneids.add_argument
    sid_p('sceneids', nargs='+', type=int,
          help="list of scene IDs corresponding to valid records within the 'scenes' table of the database")

    # add arguments to parser_entityids
    eid_p = parser_entityids.add_argument
    eid_p('entityids', nargs='+', type=str,
          help="list of entity IDs corresponding to valid records within the 'scenes' table of the database")
    # FIXME satellite and sensor are required

    # add arguments to parser_filenames
    eid_p = parser_filenames.add_argument
    eid_p('filenames', nargs='+', type=str,
          help="list of filenames of satellite image archives corresponding to valid records within the 'scenes' "
               "table of the database")

    # add arguments to parse_constraints
    con_p = parser_constraints.add_argument
    # TODO
    # con_p('constraints', nargs='+', type=str, help="list of entity IDs corresponding to valid records within the "
    #                                            "'scenes' table of the database")

    #################################
    # LINK PARSERS TO RUN FUNCTIONS #
    #################################

    parser_jobid.set_defaults(func=run_from_jobid)
    parser_sceneids.set_defaults(func=run_from_sceneids)
    parser_entityids.set_defaults(func=run_from_entityids)
    parser_filenames.set_defaults(func=run_from_filenames)
    parser_constraints.set_defaults(func=run_from_constraints)

    return parser


if __name__ == '__main__':
    parsed_args = get_gms_argparser().parse_args()
    parsed_args.func(parsed_args)

    print('\nready.')
