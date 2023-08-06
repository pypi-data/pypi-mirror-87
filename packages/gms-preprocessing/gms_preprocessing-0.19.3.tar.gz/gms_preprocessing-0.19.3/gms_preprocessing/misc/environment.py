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

import os
import sys
import warnings

try:
    from osgeo import gdal
except ImportError:
    import gdal
from logging import getLogger
from ecmwfapi.api import APIKeyFetchError, get_apikey_values

from ..options.config import GMS_config as CFG
from .spatial_index_mediator import SpatialIndexMediatorServer, Connection
from .exceptions import GMSEnvironmentError, MissingNonPipLibraryWarning
from ..misc.locks import redis_conn

__author__ = 'Daniel Scheffler'


class GMSEnvironment(object):
    """GeoMultiSens Environment class."""

    def __init__(self, logger=None):
        self.logger = logger or getLogger('GMSEnvironment')
        self.logger.info('Checking system environment...')
        self.spatIdxSrvRunning = None

    def _check_spatial_index_mediator_server(self):
        try:
            # get instance of SpatialIndexMediatorServer (raises GMSEnvironmentError if bindings are missing)
            SpatIdxSrv = SpatialIndexMediatorServer(CFG.path_spatIdxSrv, logger=self.logger)

            # check if spatial index mediator is running and start if needed
            if not SpatIdxSrv.is_running:
                SpatIdxSrv.start()

            # test connection
            conn = Connection(host=CFG.spatial_index_server_host, port=CFG.spatial_index_server_port, timeout=5.0)
            conn.disconnect()

            os.environ['GMS_SPAT_IDX_SRV_STATUS'] = 'available'

        except Exception as e:
            self.logger.error(e, exc_info=False)
            self.logger.warning('Coregistration will be skipped!')
            os.environ['GMS_SPAT_IDX_SRV_STATUS'] = 'unavailable'

    def _check_redis_server(self):
        if CFG.max_parallel_reads_writes > 0 and not redis_conn:
            self.logger.warning("Unable to connect to redis server. Is the server installed and running? For "
                                "installation on Ubuntu, use 'sudo apt install redis-server'. \n"
                                "NOTE: Without connection to redis server, any kind of locking (IO / RAM / database) "
                                "is disabled!")

    def _check_nonpip_packages(self):
        """Check for not pip-installable packages."""

        # fmask # conda install -c conda-forge python-fmask
        try:
            # noinspection PyUnresolvedReferences
            import fmask  # noqa F401 unused
        except ImportError:
            if 'FMASK' in list(CFG.cloud_masking_algorithm.values()):
                msg = "FMASK library is not installed because it is not pip-installable and must be installed " \
                      "manually, e.g. for Anaconda by running 'conda install -c conda-forge python-fmask'!"
                self.logger.warning(MissingNonPipLibraryWarning(msg))

        # 'pyhdf', # conda install --yes -c conda-forge pyhdf
        try:
            # noinspection PyUnresolvedReferences
            import pyhdf  # noqa F401 unused
        except ImportError:
            if gdal.GetDriverByName('HDF4') is None:
                msg = "The library 'pyhdf' is missing and the HDF4 driver of GDAL is not available. ASTER data cannot "\
                      "be processed! For Anaconda, run 'conda install --yes -c conda-forge pyhdf' to fix that!"
                self.logger.warning(MissingNonPipLibraryWarning(msg))

        # # 'sicor', # pip install git+https://gitext.gfz-potsdam.de/hollstei/sicor.git
        # try:
        #     # noinspection PyUnresolvedReferences
        #     import sicor  # noqa F401 unused
        # except ImportError:
        #     msg = "The library 'sicor' has not been installed automatically because installation requires login " \
        #           "credentials. See installation instrucions here: https://gitext.gfz-potsdam.de/EnMAP/sicor"
        #     self.logger.warning(MissingNonPipLibraryWarning(msg))

    def check_dependencies(self):
        # pyLibs = []
        # javaLibs = []

        self._check_spatial_index_mediator_server()
        self._check_redis_server()
        self._check_nonpip_packages()

    def check_ports(self):
        # portsDict = {
        #     8654: 'SpatialIndexMediator'
        # }

        pass

    @staticmethod
    def check_read_write_permissions():
        if not os.path.isdir(CFG.path_tempdir):
            os.makedirs(CFG.path_tempdir, exist_ok=True)

        if not os.access(CFG.path_tempdir, os.R_OK):
            raise PermissionError('No read-permissions at %s.' % CFG.path_tempdir)

        if not os.access(CFG.path_tempdir, os.W_OK):
            raise PermissionError('No write-permissions at %s.' % CFG.path_tempdir)

        if not os.access(CFG.path_tempdir, os.X_OK):
            raise PermissionError('No delete-permissions at %s.' % CFG.path_tempdir)

    @staticmethod
    def check_paths():  # TODO to be completed
        # check existence of database paths, etc.
        # check existence of cloud classifier dill objects from PG.get_path_cloud_class_obj()

        if not os.path.exists(CFG.path_archive):
            raise GMSEnvironmentError("The given provider archive path '%s' does not exist!" % CFG.path_archive)

    @staticmethod
    def ensure_properly_activated_GDAL():
        if 'conda' in sys.version:
            conda_rootdir = sys.prefix
            gdal_data_dir = os.path.join(conda_rootdir, 'share', 'gdal')

            # GDAL_DATA
            if 'GDAL_DATA' not in os.environ:
                # Prevents "Unable to open EPSG support file gcs.csv".
                warnings.warn("GDAL_DATA variable not set. Setting it to '%s'." % gdal_data_dir)
                os.environ['GDAL_DATA'] = gdal_data_dir
            if os.path.abspath(os.environ['GDAL_DATA']) != gdal_data_dir:
                warnings.warn("GDAL_DATA variable seems to be incorrectly set since Anaconda´s Python is "
                              "executed from %s and GDAL_DATA = %s. Setting it to '%s'."
                              % (conda_rootdir, os.environ['GDAL_DATA'], gdal_data_dir))
                os.environ['GDAL_DATA'] = gdal_data_dir

            # CPL_ZIP_ENCODING
            if 'CPL_ZIP_ENCODING' not in os.environ:
                # Prevents "Warning 1: Recode from CP437 to UTF-8 failed with the error: "Invalid argument"."
                # during gdal.Open().
                os.environ['CPL_ZIP_ENCODING'] = 'UTF-8'

    def check_ecmwf_api_creds(self):
        try:
            get_apikey_values()
        except APIKeyFetchError as e:
            self.logger.error(e, exc_info=False)
            self.logger.warning("ECMWF API credentials could not be found! Atmospheric correction may fail or use "
                                "default input parameters as fallback. Place a credentials file called .ecmwfapirc "
                                "into the user root directory that runs GeoMultiSens or set the environment variables "
                                "'ECMWF_API_KEY', 'ECMWF_API_URL' and 'ECMWF_API_EMAIL'!")
