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
import fnmatch
import tempfile
import shutil
import tarfile
import zipfile
import itertools
import warnings
import re
from glob import glob

# custom
try:
    from osgeo import gdal
except ImportError:
    import gdal
import fmask

from ..misc.helper_functions import convert_absPathArchive_to_GDALvsiPath, subcall_with_output
from ..misc.definition_dicts import get_mask_classdefinition
from ..misc.database_tools import get_info_from_postgreSQLdb
from ..misc.exceptions import FmaskError, FmaskWarning
from geoarray import GeoArray

__author__ = 'Daniel Scheffler'


class _FMASK_Runner(object):
    """The FMASK runner base class (not to be called directly)."""

    def __init__(self, path_providerArchive, satellite, extract_archive, tempdir_root):
        # TODO provide options of fmask_usgsLandsatStacked argparser
        # private attributes
        self._gdal_path_archive = None
        self._files_in_archive = None
        self._angles_stack = None
        self._metaFile = None
        self._TOARef = None

        assert fmask

        self.path_archive = path_providerArchive
        self.satellite = satellite
        self.extract_archive = extract_archive
        self.validate_inputs()

        self.project_dir = os.path.abspath(os.path.curdir)
        self.is_extracted = None
        self.cloud_mask = None
        self.cloud_mask = None
        self.saturationmask_legend = {}

        # create temporary directory
        if tempdir_root and not os.path.isdir(tempdir_root):
            os.makedirs(tempdir_root)
        self.tempdir = tempfile.mkdtemp(dir=tempdir_root,
                                        prefix='FMASK__%s__' % os.path.basename(self.path_archive))

        # create subdirectory for FMASK internal intermediate files
        os.makedirs(os.path.join(self.tempdir, 'FMASK_intermediates'))

    def validate_inputs(self):
        if not os.path.exists(self.path_archive):
            raise FileNotFoundError(self.path_archive)
        if self.satellite not in ['Landsat-4', 'Landsat-5', 'Landsat-7', 'Landsat-8', 'Sentinel-2A', 'Sentinel-2B']:
            raise ValueError('%s is not a supported satellite for cloud mask calculation via FMASK.' % self.satellite)

    @property
    def is_GMSConfig_available(self):
        from ..options.config import GMS_config as CFG
        try:
            if CFG is not None:
                return True
        except (EnvironmentError, OSError):
            return False

    @property
    def gdal_path_archive(self):
        if not self._gdal_path_archive:
            self._gdal_path_archive = convert_absPathArchive_to_GDALvsiPath(self.path_archive)
        return self._gdal_path_archive

    @property
    def files_in_archive(self):
        if not self._files_in_archive:
            os.chdir(os.path.dirname(self.path_archive))
            self._files_in_archive = gdal.ReadDirRecursive(self.gdal_path_archive)
        return self._files_in_archive

    @staticmethod
    def run_cmd(cmd):
        output, exitcode, err = subcall_with_output(cmd)
        if exitcode:
            raise FmaskError("Error during FMASK cloud masking: \n" + err.decode('latin-1'))
        if output:
            return output.decode('UTF-8')

    def extract_tar_archive(self):
        with tarfile.open(self.path_archive) as tarF:
            tarF.extractall(self.tempdir)
        self.is_extracted = True

    def extract_zip_archive(self):
        with zipfile.ZipFile(self.path_archive, "r") as z:
            z.extractall(self.tempdir)
        self.is_extracted = True

    def to_saved_rasterFile(self, value, attrname):
        pathFile = os.path.join(self.tempdir, "%s.bsq" % attrname)
        if isinstance(value, str) and os.path.exists(value):
            pathFile = value
        elif isinstance(value, GeoArray):
            value.q = True
            value.save(pathFile)
        else:
            raise TypeError("The attribute '%s' can only be set by an existing path or an instance of GeoArray. "
                            "Received %s" % (attrname, type(value)))

        assert isinstance(pathFile, str) and os.path.exists(pathFile)

        return pathFile

    def calc_cloudMask(self, path_out=None, fmt=None):
        if path_out:
            gdal.Translate(path_out, gdal.Open(self.cloud_mask), format=fmt)
            self.cloud_mask = GeoArray(path_out)
        elif self.cloud_mask is not None and isinstance(self.cloud_mask, str) and os.path.exists(self.cloud_mask):
            self.cloud_mask = GeoArray(self.cloud_mask).to_mem()
        else:
            self.cloud_mask = None

        if self.cloud_mask:
            if self.is_GMSConfig_available:
                self.cloud_mask.legend = \
                    get_mask_classdefinition('mask_clouds', self.satellite)
            else:  # use default FMASK legend
                warnings.warn('GMS configuration not available. Using default cloud mask legend.', FmaskWarning)
                self.cloud_mask.legend = \
                    {'No Data': 0, 'Clear': 1, 'Cloud': 2, 'Shadow': 3, 'Snow': 4, 'Water': 5}

        return self.cloud_mask

    def clean(self):
        shutil.rmtree(self.tempdir)
        self.is_extracted = False
        os.chdir(self.project_dir)
        self._metaFile = None
        self._angles_stack = None
        self._TOARef = None


class FMASK_Runner_Landsat(_FMASK_Runner):
    def __init__(self, path_providerArchive, satellite, TOARef=None, opticalDNs=None, thermalDNs=None,
                 tempdir_root=None):
        """FMASK wrapper class for Landsat 4-8.

        :param path_providerArchive:    file path of the provider .tar.gz archive
        :param satellite:               name of the satellite: 'Landsat-4', 'Landsat-5', 'Landsat-7', 'Landsat-8'
        :param TOARef:                  file path or GeoArray instance of top-of-atmosphere reflectance data
                                        scaled from 0 to 10000 (optional -> generated from archive if not given)
        :param opticalDNs:              file path or GeoArray instance of optical data (digital numbers)
        :param thermalDNs:              file path or GeoArray instance of thermal data (digital numbers)
        :param tempdir_root:            directory to write intermediate data (auto-determined if not given)
        """

        # private attributes
        self._optical_stack = None
        self._thermal_stack = None
        self._saturationmask = None

        self.FileMatchExp = {
            'Landsat-4': dict(optical='L*_B[1-5,7].TIF', thermal='L*_B6.TIF', meta='*_MTL.txt'),
            'Landsat-5': dict(optical='L*_B[1-5,7].TIF', thermal='L*_B6.TIF', meta='*_MTL.txt'),
            'Landsat-7': dict(optical='L*_B[1-5,7].TIF', thermal='L*_B6_VCID_?.TIF', meta='*_MTL.txt'),
            'Landsat-8': dict(optical='L*_B[1-7,9].TIF', thermal='L*_B1[0,1].TIF', meta='*_MTL.txt')
        }[satellite]

        super(FMASK_Runner_Landsat, self).__init__(path_providerArchive, satellite, extract_archive=False,
                                                   tempdir_root=tempdir_root)

        # populate optional attributes
        if TOARef is not None:
            self.TOARef = TOARef
        if opticalDNs is not None:
            self.optical_stack = opticalDNs
        if thermalDNs is not None:
            self.thermal_stack = thermalDNs

    @property
    def optical_stack(self):
        if self._optical_stack is None:
            if not self.is_extracted:
                self.extract_tar_archive()
            opt_fNames = list(sorted(fnmatch.filter(os.listdir(self.tempdir), self.FileMatchExp['optical'])))
            fNames_str = ' '.join([os.path.join(self.tempdir, fName) for fName in opt_fNames])

            # create stack of optical bands
            self._optical_stack = os.path.join(self.tempdir, 'optical_stack.vrt')
            self.run_cmd('gdalbuildvrt %s -separate %s' % (self._optical_stack, fNames_str))

        return self._optical_stack

    @optical_stack.setter
    def optical_stack(self, value):
        self._optical_stack = super(FMASK_Runner_Landsat, self).to_saved_rasterFile(value, 'optical_stack')

    @property
    def thermal_stack(self):
        if self._thermal_stack is None:
            if not self.is_extracted:
                self.extract_tar_archive()
            opt_fNames = list(sorted(fnmatch.filter(os.listdir(self.tempdir), self.FileMatchExp['thermal'])))
            fNames_str = ' '.join([os.path.join(self.tempdir, fName) for fName in opt_fNames])

            # create stack of thermal bands
            self._thermal_stack = os.path.join(self.tempdir, 'thermal_stack.vrt')
            self.run_cmd('gdalbuildvrt %s -separate %s' % (self._thermal_stack, fNames_str))

        return self._thermal_stack

    @thermal_stack.setter
    def thermal_stack(self, value):
        self._thermal_stack = super(FMASK_Runner_Landsat, self).to_saved_rasterFile(value, 'thermal_stack')

    @property
    def metaFile(self):
        if not self._metaFile:
            if not self.is_extracted:
                self.extract_tar_archive()
            self._metaFile = os.path.join(self.tempdir, fnmatch.filter(os.listdir(self.tempdir), '*_MTL.txt')[0])

        return self._metaFile

    @property
    def angles_stack(self):
        if self._angles_stack is None:
            self._angles_stack = os.path.join(self.tempdir, 'angles.vrt')
            self.run_cmd('fmask_usgsLandsatMakeAnglesImage.py -m %s -t %s -o %s'
                         % (self.metaFile, self.optical_stack, self._angles_stack))

        return self._angles_stack

    @property
    def saturationmask(self):
        if self._saturationmask is None:
            self._saturationmask = os.path.join(self.tempdir, 'saturationmask.vrt')
            self.run_cmd('fmask_usgsLandsatSaturationMask.py -m %s -i %s -o %s'
                         % (self.metaFile, self.optical_stack, self._saturationmask))
            self.saturationmask_legend = {'blue': 0, 'green': 1, 'red': 2}

        return self._saturationmask

    @property
    def TOARef(self):
        if self._TOARef is None:
            self._TOARef = os.path.join(self.tempdir, 'TOARef.vrt')
            self.run_cmd('fmask_usgsLandsatTOA.py -m %s -i %s -z %s -o %s'
                         % (self.metaFile, self.optical_stack, self.angles_stack, self._TOARef))

        return self._TOARef

    @TOARef.setter
    def TOARef(self, value):
        self._TOARef = super(FMASK_Runner_Landsat, self).to_saved_rasterFile(value, 'TOARef')

    def calc_cloudMask(self, path_out=None, fmt=None):
        # type: (str, str) -> any

        """Calculate the cloud mask!

        :param path_out:    output path (if not given, a GeoArray instance is returned)
        :param fmt:         output GDAL driver code, e.g. 'ENVI' (only needed if path_out is given)
        :return: a GeoArray instance of the computed cloud mask
        """

        try:
            self.cloud_mask = os.path.join(self.tempdir, 'fmask_cloudmask.vrt')
            self.run_cmd('fmask_usgsLandsatStacked.py %s'
                         % ' '.join(['-m %s' % self.metaFile,
                                     '-a %s' % self.TOARef,
                                     '-t %s' % self.thermal_stack,
                                     '-z %s' % self.angles_stack,
                                     '-s %s' % self.saturationmask,
                                     '-o %s' % self.cloud_mask,
                                     '-e %s' % os.path.join(self.tempdir, 'FMASK_intermediates')
                                     ]))
            return super(FMASK_Runner_Landsat, self).calc_cloudMask(path_out=path_out, fmt=fmt)

        finally:
            self.clean()

    def clean(self):
        self._thermal_stack = None
        self._optical_stack = None
        self._saturationmask = None

        super(FMASK_Runner_Landsat, self).clean()
        assert not os.path.isdir(self.tempdir), 'Error deleting temporary FMASK directory.'


class FMASK_Runner_Sentinel2(_FMASK_Runner):
    def __init__(self, path_providerArchive, satellite, scene_ID=None, granule_ID='', target_res=20, TOARef=None,
                 extract_archive=False, tempdir_root=None):
        """FMASK wrapper class for Sentinel-2.

        :param path_providerArchive:    file path of the provider .zip archive
        :param satellite:               name of the satellite: 'Sentinel-2A' or 'Sentinel-2B'
        :param scene_ID:                the GeoMultiSens scene ID of the given scene (needed if granule_ID is not given)
        :param granule_ID:              the Sentinel-2 granule ID
        :param target_res:              target spatial resolution of the cloud mask (default: 20m)
        :param TOARef:                  file path or GeoArray instance of top-of-atmosphere reflectance data
                                        scaled from 0 to 10000 (optional -> read from archive if not given)
        :param extract_archive:         whether to extract the archive to disk or to read from the archive directly
                                        (default: False); NOTE: There is no remarkable speed difference.
        :param tempdir_root:            directory to write intermediate data (auto-determined if not given)
        """

        self._granule_ID = granule_ID

        self.scene_ID = scene_ID
        self.tgt_res = target_res

        oldStPref = '*GRANULE/' + self.granule_ID + '*/'
        self.FileMatchExp = {
            'Sentinel-2A': dict(opticalOLDStyle='%s*_B0[1-8].jp2 %s*_B8A.jp2 %s*_B09.jp2 %s*_B1[0-2].jp2'
                                                % (oldStPref, oldStPref, oldStPref, oldStPref),
                                opticalNEWStyle='*_B0[1-8].jp2 *_B8A.jp2 *_B09.jp2 *_B1[0-2].jp2',
                                metaOLDStyle='%sS2A*.xml' % oldStPref,
                                metaNEWStyle='*MTD_TL.xml'),
            'Sentinel-2B': dict(opticalOLDStyle='%s*_B0[1-8].jp2 %s*_B8A.jp2 %s*_B09.jp2 %s*_B1[0-2].jp2'
                                                % (oldStPref, oldStPref, oldStPref, oldStPref),
                                opticalNEWStyle='*_B0[1-8].jp2 *_B8A.jp2 *_B09.jp2 *_B1[0-2].jp2',
                                metaOLDStyle='%sS2B*.xml' % oldStPref,
                                metaNEWStyle='*MTD_TL.xml'),
        }[satellite]

        super(FMASK_Runner_Sentinel2, self).__init__(path_providerArchive, satellite, extract_archive,
                                                     tempdir_root=tempdir_root)

        # populate optional attributes
        if TOARef is not None:
            self.TOARef = TOARef

    @property
    def granule_ID(self):
        """Gets the Sentinel-2 granule ID from the database using the scene ID in case the granule ID has not been
        given."""

        if not self._granule_ID and self.scene_ID and self.scene_ID != -9999 and self.is_GMSConfig_available:
            from ..options.config import GMS_config as CFG
            res = get_info_from_postgreSQLdb(CFG.conn_database, 'scenes', ['entityid'], {'id': self.scene_ID})
            assert len(res) != 0, \
                "Invalid SceneID given - no corresponding scene with the ID=%s found in database.\n" % self.scene_ID
            assert len(res) == 1, "Error in database. The sceneid %s exists more than once. \n" % self.scene_ID
            self._granule_ID = res[0][0]

        return self._granule_ID

    @property
    def metaFile(self):
        if not self._metaFile:
            fNs_meta = fnmatch.filter(self.files_in_archive, self.FileMatchExp['metaNEWStyle'])
            if not fNs_meta:
                fNs_meta = fnmatch.filter(self.files_in_archive, self.FileMatchExp['metaOLDStyle'])
                if len(fNs_meta) > 1:
                    raise RuntimeError('Found multiple metadata files for the given %s dataset. Please provide the '
                                       'granule ID where you want to use the metadata from.' % self.satellite)
                elif not fNs_meta:
                    raise RuntimeError('Could not find a metadata file for the given %s dataset.' % self.satellite)
            fN_meta = fNs_meta[0]

            # only extract the metadata file
            self._metaFile = os.path.join(self.tempdir, 'meta.xml')
            with zipfile.ZipFile(self.path_archive) as z:
                with z.open(fN_meta) as zf, open(self._metaFile, 'wb') as f:
                    shutil.copyfileobj(zf, f)

        return self._metaFile

    @property
    def angles_stack(self):
        if self._angles_stack is None:
            self._angles_stack = os.path.join(self.tempdir, 'angles.vrt')
            self.run_cmd('fmask_sentinel2makeAnglesImage.py -i %s -o %s' % (self.metaFile, self._angles_stack))

        return self._angles_stack

    @property
    def TOARef(self):
        if self._TOARef is None:
            if not self.extract_archive:
                fileList = self.files_in_archive
            else:
                if not self.is_extracted:
                    self.extract_zip_archive()
                fileList = glob(self.tempdir + '/**', recursive=True)

            matchExps = self.FileMatchExp['opticalOLDStyle'].split()
            opt_fNames = list(itertools.chain.from_iterable(
                [list(sorted(fnmatch.filter(fileList, mE))) for mE in matchExps]))
            if not opt_fNames:
                matchExps = self.FileMatchExp['opticalNEWStyle'].split()
                opt_fNames = list(itertools.chain.from_iterable(
                    [list(sorted(fnmatch.filter(fileList, mE))) for mE in matchExps]))
            fNames_str = ' '.join(opt_fNames) if self.is_extracted else \
                ' '.join([os.path.join(self.gdal_path_archive, fName) for fName in opt_fNames])

            # create stack of TOARef bands
            self._TOARef = os.path.join(self.tempdir, 'TOARef.vrt')
            self.run_cmd('gdalbuildvrt %s -resolution user -tr %s %s -separate %s'
                         % (self._TOARef, self.tgt_res, self.tgt_res, fNames_str))

        return self._TOARef

    @TOARef.setter
    def TOARef(self, value):
        self._TOARef = super(FMASK_Runner_Sentinel2, self).to_saved_rasterFile(value, 'TOARef')

    def calc_cloudMask(self, path_out=None, fmt=None):
        # type: (str, str) -> any

        """Calculate the cloud mask!

        :param path_out:    output path (if not given, a GeoArray instance is returned)
        :param fmt:         output GDAL driver code, e.g. 'ENVI' (only needed if path_out is given)
        :return: a GeoArray instance of the computed cloud mask
        """

        try:
            self.cloud_mask = os.path.join(self.tempdir, 'fmask_cloudmask.vrt')
            self.run_cmd('fmask_sentinel2Stacked.py %s'
                         % ' '.join(['-a %s' % self.TOARef,
                                     '-z %s' % self.angles_stack,
                                     '-o %s' % self.cloud_mask,
                                     '-e %s' % os.path.join(self.tempdir, 'FMASK_intermediates')
                                     ]))
            return super(FMASK_Runner_Sentinel2, self).calc_cloudMask(path_out=path_out, fmt=fmt)

        finally:
            self.clean()

    def clean(self):
        super(FMASK_Runner_Sentinel2, self).clean()
        assert not os.path.isdir(self.tempdir), 'Error deleting temporary FMASK directory.'


class Cloud_Mask_Creator(object):
    def __init__(self, GMS_object, algorithm, target_res=None, tempdir_root=None):
        """A class for creating cloud masks.

        :param GMS_object:  instance or subclass instance of model.gms_object.GMS_object
        :param algorithm:   'FMASK' or 'Classical Bayesian
        :param target_res:  target resolution of the computed cloud mask (if not given, the appropriate resolution
                            needed for atmospheric correction is chosen)
        """

        self.GMS_obj = GMS_object
        self.algorithm = algorithm
        self.tgt_res = target_res if target_res else self.GMS_obj.ac_options['cld_mask']['target_resolution']
        self.tempdir_root = tempdir_root

        self.cloud_mask_geoarray = None
        self.cloud_mask_array = None
        self.cloud_mask_legend = None
        self.success = None

        if self.GMS_obj.satellite not in ['Landsat-4', 'Landsat-5', 'Landsat-7', 'Landsat-8',
                                          'Sentinel-2A', 'Sentinel-2B']:
            self.GMS_obj.error(
                'Cloud masking is not yet implemented for %s %s...' % (self.GMS_obj.satellite, self.GMS_obj.sensor))
            self.success = False
        if algorithm not in ['FMASK', 'Classical Bayesian']:  # TODO move validation to config
            raise ValueError(algorithm)

    def calc_cloud_mask(self):
        if self.success is False:
            return None, None, None

        self.GMS_obj.logger.info("Calculating cloud mask based on '%s' algorithm..." % self.algorithm)

        if self.algorithm == 'FMASK':
            if re.search(r'Landsat', self.GMS_obj.satellite, re.I):
                FMR = FMASK_Runner_Landsat(self.GMS_obj.path_archive, self.GMS_obj.satellite)

            else:
                FMR = FMASK_Runner_Sentinel2(self.GMS_obj.path_archive, self.GMS_obj.satellite,
                                             scene_ID=self.GMS_obj.scene_ID,
                                             target_res=self.tgt_res, tempdir_root=self.tempdir_root)

            self.cloud_mask_geoarray = FMR.calc_cloudMask()
            self.cloud_mask_array = self.cloud_mask_geoarray[:]
            self.cloud_mask_legend = self.cloud_mask_geoarray.legend

        else:
            raise NotImplementedError("The cloud masking algorithm '%s' is not yet implemented." % self.algorithm)

        self.validate_cloud_mask()

        return self.cloud_mask_geoarray, self.cloud_mask_array, self.cloud_mask_legend

    def validate_cloud_mask(self):
        assert self.cloud_mask_geoarray.xgsd == self.cloud_mask_geoarray.ygsd == self.tgt_res
        self.success = True
