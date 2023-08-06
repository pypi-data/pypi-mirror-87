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
import os
import re
import warnings

import gdal
import gdalnumeric
import numpy as np
from natsort import natsorted

try:
    from pyhdf import SD
except ImportError:
    SD = None

from geoarray import GeoArray
from py_tools_ds.geo.coord_calc import calc_FullDataset_corner_positions
from py_tools_ds.geo.coord_trafo import pixelToLatLon, imYX2mapYX
from py_tools_ds.geo.map_info import mapinfo2geotransform
from py_tools_ds.geo.projection import EPSG2WKT, isProjectedOrGeographic

from ..options.config import GMS_config as CFG
from . import geoprocessing as GEOP
from ..misc.definition_dicts import get_outFillZeroSaturated, is_dataset_provided_as_fullScene
from ..misc.locks import IOLock
from ..model.gms_object import GMS_object
from ..model import metadata as META

__author__ = 'Daniel Scheffler'


class L1A_object(GMS_object):
    """Features input reader and raster-/metadata homogenization."""

    def __init__(self, image_type='', satellite='', sensor='', subsystem='', sensormode='', acq_datetime=None,
                 entity_ID='', scene_ID=-9999, filename='', dataset_ID=-9999, proc_status='', **kwargs):
        """:param :  instance of gms_object.GMS_object or None
        """
        # TODO docstring

        # NOTE: kwargs is in here to allow instanciating with additional arg 'proc_level'

        # load default attribute values and methods
        super(L1A_object, self).__init__()

        # unpack kwargs
        self.proc_level = 'L1A'
        self.image_type = image_type  # FIXME not needed anymore?
        self.satellite = satellite
        self.sensor = sensor
        self.subsystem = subsystem
        self.sensormode = sensormode
        self.acq_datetime = acq_datetime
        self.entity_ID = entity_ID
        self.scene_ID = scene_ID
        self.filename = filename
        self.dataset_ID = dataset_ID

        # set pathes (only if there are valid init args)
        if image_type and satellite and sensor:
            self.set_pathes()  # also overwrites logfile
            self.validate_pathes()

            if self.path_archive_valid:
                self.logger.info('L1A object for %s %s%s (entity-ID %s) successfully initialized.'
                                 % (self.satellite, self.sensor,
                                    (' ' + self.subsystem) if self.subsystem not in [None, ''] else '', self.entity_ID))

        # (re)set the processing status
        if self.scene_ID in self.proc_status_all_GMSobjs:
            del self.proc_status_all_GMSobjs[self.scene_ID]

        self.proc_status = proc_status or 'initialized'  # if proc_status = 'running' is given by L1A_map

    def import_rasterdata(self):
        if re.search(r"ALOS", self.satellite, re.I):
            '''First 22 lines are nodata: = maybe due to an issue of the GDAL CEOS driver.
            But: UL of metadata refers to [row =0, col=21]! So the imported GeoTransform is correct when
            the first 21 columns are deleted.'''
            self.archive_to_rasObj(self.path_archive, self.path_InFilePreprocessor,
                                   subset=['block', [[None, None], [21, None]]])
        elif re.search(r"Terra", self.satellite, re.I):
            self.ASTER_HDF_to_rasObj(self.path_archive, path_output=self.path_InFilePreprocessor)
        else:
            self.archive_to_rasObj(self.path_archive, path_output=self.path_InFilePreprocessor)

        # set shape_fullArr
        self.shape_fullArr = self.arr.shape

    def archive_to_rasObj(self, path_archive, path_output=None, subset=None):
        from ..misc.helper_functions import convert_absPathArchive_to_GDALvsiPath

        assert subset is None or isinstance(subset, list) and len(subset) == 2, \
            "Subset argument has be a list with 2 elements."
        if subset:
            assert subset[0] == 'block',\
                "The function 'archive_to_rasObj' only supports block subsetting. Attempted to perform '%s' " \
                "subsetting." % subset[0]

        self.logger.info('Reading %s %s %s image data...' % (self.satellite, self.sensor, self.subsystem))
        gdal_path_archive = convert_absPathArchive_to_GDALvsiPath(path_archive)
        project_dir = os.path.abspath(os.curdir)
        os.chdir(os.path.dirname(path_archive))
        files_in_archive = gdal.ReadDirRecursive(gdal_path_archive)  # needs ~12sek for Landsat-8
        assert files_in_archive, 'No files in archive %s for scene %s (entity ID: %s). ' \
                                 % (os.path.basename(path_archive), self.scene_ID, self.entity_ID)
        full_LayerBandsAssignment = META.get_LayerBandsAssignment(self.GMS_identifier, no_thermal=False, no_pan=False)

        ####################################################
        # get list of raster files to be read from archive #
        ####################################################

        image_files = []
        is_ALOS_Landsat_S2 = \
            re.search(r'ALOS', self.satellite) or re.search(r'Landsat', self.satellite) or \
            re.search(r'Sentinel-2', self.satellite)
        n_files2search = len(full_LayerBandsAssignment) if is_ALOS_Landsat_S2 else 1

        for File in natsorted(files_in_archive):
            search_res = \
                re.search(r"IMG-0[0-9]-[\s\S]*", File) if re.search(r'ALOS', self.satellite) else \
                re.search(r"[\S]*_B[1-9][0-9]?[\S]*.TIF", File) if re.search(r'Landsat', self.satellite) else \
                re.search(r"[0-9]*.tif", File) if re.search(r'RapidEye', self.satellite) else \
                re.search(r"imagery.tif", File) if re.search(r'SPOT', self.satellite) else \
                re.search(r"[\S]*.SAFE/GRANULE/%s/IMG_DATA/[\S]*_B[0-9][\S]*.jp2"
                          % self.entity_ID, File) if re.search(r'Sentinel-2', self.satellite) else None

            if search_res:
                if re.search(r'Sentinel-2', self.satellite):
                    # add only those files that are corresponding to subsystem (e.g. S2A10: fullLBA = ['2','3','4','8'])
                    if 1 in [1 if re.search(r"[\S]*_B[0]?%s.jp2" % LBAn, os.path.basename(File)) else 0
                             for LBAn in full_LayerBandsAssignment]:
                        image_files.append(File)
                else:
                    image_files.append(File)

        # create and fill raster object
        if n_files2search > 1:
            #####################################
            # validate number of expected files #
            #####################################

            if re.search(r'ETM+', self.sensor) and self.acq_datetime > datetime.datetime(year=2003, month=5, day=31):
                expected_files_count = 2 * len(full_LayerBandsAssignment)
            else:
                expected_files_count = len(full_LayerBandsAssignment)

            assert len(image_files) == expected_files_count, "Expected %s image files in '%s'. Found %s." \
                                                             % (len(full_LayerBandsAssignment), path_archive,
                                                                len(image_files))

            ###############################
            # get paths of files to stack #
            ###############################

            # NOTE: image_files is a SORTED list of image filenames; self.LayerBandsAssignment may be sorted by CWL
            filtered_files = []
            for bN in self.LayerBandsAssignment:  # unsorted, e.g., ['1', '2', '3', '4', '5', '9', '6', '7']
                for fN, b in zip(image_files, natsorted(full_LayerBandsAssignment)):  # both sorted nicely
                    if b == bN:
                        filtered_files.append(fN)

            paths_files2stack = [os.path.join(gdal_path_archive, i) for i in filtered_files]

            #########################
            # read the raster data  #
            #########################

            rasObj = GEOP.GEOPROCESSING(paths_files2stack[0], self.logger)

            # in case a subset is to be read: prepare rasObj instance to read a subset
            if subset:
                full_dim = [0, rasObj.rowEnd, 0, rasObj.colEnd]
                sub_dim = [subset[1][0][0], subset[1][0][1], subset[1][1][0], subset[1][0][1]]
                sub_dim = [sub_dim[i] if sub_dim[i] else full_dim[i] for i in range(len(sub_dim))]
                subset = ['block', [[sub_dim[0], sub_dim[1] + 1], [sub_dim[2], sub_dim[3] + 1]]]
                rasObj = GEOP.GEOPROCESSING(paths_files2stack[0], self.logger, subset=subset)

            # perform layer stack
            with IOLock(allowed_slots=CFG.max_parallel_reads_writes, logger=self.logger):
                if CFG.inmem_serialization and path_output is None:  # numpy array output
                    self.arr = rasObj.Layerstacking(paths_files2stack)
                    self.path_InFilePreprocessor = paths_files2stack[0]
                else:  # 'MEMORY' or physical output
                    rasObj.Layerstacking(paths_files2stack, path_output=path_output)  # writes an output (gdal_merge)
                    self.arr = path_output

        else:
            assert image_files != [], 'No image files found within the archive matching the expected naming scheme.'
            path_file2load = os.path.join(gdal_path_archive, image_files[0])
            rasObj = GEOP.GEOPROCESSING(path_file2load, self.logger)

            if subset:
                full_dim = [0, rasObj.rowEnd, 0, rasObj.colEnd]
                sub_dim = [subset[1][0][0], subset[1][0][1], subset[1][1][0], subset[1][0][1]]
                sub_dim = [sub_dim[i] if sub_dim[i] else full_dim[i] for i in range(len(sub_dim))]
                subset = ['block', [[sub_dim[0], sub_dim[1] + 1], [sub_dim[2], sub_dim[3] + 1]]]
                rasObj = GEOP.GEOPROCESSING(path_file2load, self.logger, subset=subset)

            # read a single file
            with IOLock(allowed_slots=CFG.max_parallel_reads_writes, logger=self.logger):
                if CFG.inmem_serialization and path_output is None:  # numpy array output
                    self.arr = gdalnumeric.LoadFile(path_file2load) if subset is None else \
                        gdalnumeric.LoadFile(path_file2load, rasObj.colStart, rasObj.rowStart, rasObj.cols, rasObj.rows)
                    self.path_InFilePreprocessor = path_file2load
                else:  # 'MEMORY' or physical output
                    GEOP.ndarray2gdal(rasObj.tondarray(), path_output,
                                      geotransform=rasObj.geotransform, projection=rasObj.projection)
                    self.arr = path_output

        os.chdir(project_dir)

    def ASTER_HDF_to_rasObj(self, path_archive, path_output=None):
        subsystem_identifier = 'VNIR' if self.subsystem in ['VNIR1', 'VNIR2'] else 'SWIR' \
            if self.subsystem == 'SWIR' else 'TIR'

        ds = gdal.Open(path_archive)

        if ds:
            sds_md = ds.GetMetadata('SUBDATASETS')
            data_arr = None
            for bidx, b in enumerate(self.LayerBandsAssignment):
                sds_name = [i for i in sds_md.values() if '%s_Band%s:ImageData' % (subsystem_identifier, b) in str(i) or
                            '%s_Swath:ImageData%s' % (subsystem_identifier, b) in str(i)][0]
                data = gdalnumeric.LoadFile(sds_name)
                if bidx == 0:
                    data_arr = np.empty(data.shape + (len(self.LayerBandsAssignment),), data.dtype)
                data_arr[:, :, bidx] = data

            if CFG.inmem_serialization and path_output is None:  # numpy array output
                self.arr = data_arr
            else:
                GEOP.ndarray2gdal(data_arr, path_output, geotransform=ds.GetGeoTransform(),
                                  projection=ds.GetProjection(), direction=3)
                self.arr = path_output

        elif SD is not None:
            self.logger.info('Missing HDF4 support within GDAL. Reading HDF file using alternative reader.')
            hdfFile = SD.SD(path_archive, SD.SDC.READ)
            i, list_matching_dsIdx = 0, []

            while True:  # Get dataset indices within HDF file
                # noinspection PyBroadException
                try:
                    ds = hdfFile.select(i)
                    if subsystem_identifier in str(ds.dimensions()) and 'ImagePixel' in str(ds.dimensions()):
                        list_matching_dsIdx.append(i)
                    i += 1
                except Exception:
                    break

            list_matching_dsIdx = list_matching_dsIdx[:3] if self.subsystem == 'VNIR1' else \
                [list_matching_dsIdx[-1]] if self.subsystem == 'VNIR2' else list_matching_dsIdx
            data_arr = None
            for i, dsIdx in enumerate(list_matching_dsIdx):
                data = hdfFile.select(dsIdx)[:]
                if i == 0:
                    data_arr = np.empty(data.shape + (len(self.LayerBandsAssignment),), data.dtype)
                data_arr[:, :, i] = data

            if CFG.inmem_serialization and path_output is None:  # numpy array output
                self.arr = data_arr
            else:
                GEOP.ndarray2gdal(data_arr, path_output, direction=3)
                self.arr = path_output

        else:
            self.logger.error('Missing HDF4 support. Reading HDF file failed.')
            raise ImportError('No suitable library for reading HDF4 data available.')

        del ds

    def import_metadata(self):
        """Reads metainformation of the given file from the given ASCII metafile.
        Works for: RapidEye (metadata.xml),SPOT(metadata.dim),LANDSAT(mtl.txt),ASTER(downloaded coremetadata),
        ALOS(summary.txt & Leader file)

        :return:
        """

        self.logger.info('Reading %s %s %s metadata...' % (self.satellite, self.sensor, self.subsystem))
        self.MetaObj = META.METADATA(self.GMS_identifier)
        self.MetaObj.read_meta(self.scene_ID, self.path_InFilePreprocessor,
                               self.path_MetaPreprocessor, self.LayerBandsAssignment)

        self.logger.debug("The following metadata have been read:")
        [self.logger.debug("%20s : %-4s" % (key, val)) for key, val in self.MetaObj.overview.items()]

        # set some object attributes directly linked to metadata
        self.subsystem = self.MetaObj.Subsystem
        self.arr.nodata = self.MetaObj.spec_vals['fill']

        # update acquisition date to a complete datetime object incl. date, time and timezone
        if self.MetaObj.AcqDateTime:
            self.acq_datetime = self.MetaObj.AcqDateTime

        # set arr_desc
        self.arr_desc = \
            'DN' if self.MetaObj.PhysUnit == 'DN' else \
            'Rad' if self.MetaObj.PhysUnit == "W * m-2 * sr-1 * micrometer-1" else \
            'TOA_Ref' if re.search(r'TOA_Reflectance', self.MetaObj.PhysUnit, re.I) else \
            'BOA_Ref' if re.search(r'BOA_Reflectance', self.MetaObj.PhysUnit, re.I) else \
            'Temp' if re.search(r'Degrees Celsius', self.MetaObj.PhysUnit, re.I) else None

        assert self.arr_desc, 'GMS_obj contains an unexpected physical unit: %s' % self.MetaObj.PhysUnit

    def calc_TOARadRefTemp(self, subset=None):
        """Convert DN, Rad or TOA_Ref data to TOA Reflectance, to Radiance or to Surface Temperature
        (depending on CFG.target_radunit_optical and target_radunit_thermal).
        The function can be executed by a L1A_object representing a full scene or a tile. To process a file from disk
        in tiles, provide an item of self.tile_pos as the 'subset' argument."""

        proc_opt_therm = sorted(list(set(self.dict_LayerOptTherm.values())))
        assert proc_opt_therm in [['optical', 'thermal'], ['optical'], ['thermal']]

        inFill, inZero, inSaturated = \
            self.MetaObj.spec_vals['fill'], self.MetaObj.spec_vals['zero'], self.MetaObj.spec_vals['saturated']
        (rS, rE), (cS, cE) = self.arr_pos or ((0, self.shape_fullArr[0]), (0, self.shape_fullArr[1]))
        #        in_mem = hasattr(self, 'arr') and isinstance(self.arr, np.ndarray)
        #        if in_mem:
        #            (rS, rE), (cS, cE) =
        #                self.arr_pos if self.arr_pos else ((0,self.shape_fullArr[0]),(0,self.shape_fullArr[1]))
        #            bands = true_bands = self.arr.shape[2] if len(self.arr.shape) == 3 else 1
        #        else:
        #            subset = subset if subset else ['block', self.arr_pos] if self.arr_pos else ['cube', None]
        #            bands, rS, rE, cS, cE =
        #                list(GEOP.get_subsetProps_from_subsetArg(self.shape_fullArr, subset).values())[2:7]
        #            ds = gdal.Open(self.MetaObj.Dataname); true_bands = ds.RasterCount; ds = None
        assert len(self.LayerBandsAssignment) == self.arr.bands, \
            "DN2RadRef-Input data have %s bands although %s bands are specified in self.LayerBandsAssignment." \
            % (self.arr.bands, len(self.LayerBandsAssignment))

        ################################
        # perform conversion if needed #
        ################################

        data_optical, data_thermal, optical_bandsList, thermal_bandsList = None, None, [], []
        for optical_thermal in ['optical', 'thermal']:
            if optical_thermal not in self.dict_LayerOptTherm.values():
                continue
            conv = getattr(CFG, 'target_radunit_%s' % optical_thermal)
            conv = conv if conv != 'BOA_Ref' else 'TOA_Ref'
            assert conv in ['Rad', 'TOA_Ref', 'Temp'], 'Unsupported conversion type: %s' % conv
            arr_desc = self.arr_desc.split('/')[0] if optical_thermal == 'optical' else self.arr_desc.split('/')[-1]
            assert arr_desc in ['DN', 'Rad', 'TOA_Ref', 'Temp'], 'Unsupported array description: %s' % arr_desc

            bList = [i for i, lr in enumerate(self.LayerBandsAssignment) if
                     self.dict_LayerOptTherm[lr] == optical_thermal]

            # custom_subsetProps = [[rS,rE],[cS,cE],bList]

            inArray = np.take(self.arr, bList, axis=2)
            # inArray = np.take(self.arr,bList,axis=2) if in_mem else \
            #    INP_R.read_ENVI_image_data_as_array(self.MetaObj.Dataname,'custom',custom_subsetProps,self.logger,q=1)
            inArray = inArray[:, :, 0] if len(inArray.shape) == 3 and inArray.shape[2] == 1 else inArray  # 3D to 2D

            if arr_desc == 'DN':
                self.log_for_fullArr_or_firstTile('Calculating %s...' % conv, subset)

                # get input parameters #
                ########################

                off = [self.MetaObj.Offsets[b] for b in self.LayerBandsAssignment]
                gai = [self.MetaObj.Gains[b] for b in self.LayerBandsAssignment]
                irr = [self.MetaObj.SolIrradiance[b] for b in self.LayerBandsAssignment]
                zen, esd = 90 - float(self.MetaObj.SunElevation), self.MetaObj.EarthSunDist
                k1 = [self.MetaObj.ThermalConstK1[b] for b in self.LayerBandsAssignment]
                k2 = [self.MetaObj.ThermalConstK2[b] for b in self.LayerBandsAssignment]

                OFF, GAI, IRR, K1, K2 = [list(np.array(par)[bList]) for par in [off, gai, irr, k1, k2]]

                # perform conversion #
                ######################
                res = \
                    GEOP.DN2Rad(inArray, OFF, GAI, inFill, inZero, inSaturated) if conv == 'Rad' else \
                    GEOP.DN2TOARef(inArray, OFF, GAI, IRR, zen, esd, inFill, inZero,
                                   inSaturated) if conv == 'TOA_Ref' else \
                    GEOP.DN2DegreesCelsius_fastforward(inArray, OFF, GAI, K1, K2, 0.95, inFill, inZero, inSaturated)
                if conv == 'TOA_Ref':
                    self.MetaObj.ScaleFactor = CFG.scale_factor_TOARef

            elif arr_desc == 'Rad':
                raise NotImplementedError("Conversion Rad to %s is currently not supported." % conv)

            elif arr_desc == 'TOA_Ref':
                if conv == 'Rad':
                    """http://s2tbx.telespazio-vega.de/sen2three/html/r2rusage.html?highlight=quantification182
                    rToa = (float)(DN_L1C_band / QUANTIFICATION_VALUE);
                    L = (rToa * e0__SOLAR_IRRADIANCE_For_band * cos(Z__Sun_Angles_Grid_Zenith_Values)) /
                        (PI * U__earth_sun_distance_correction_factor);
                    L = (U__earth_sun_distance_correction_factor * rToa * e0__SOLAR_IRRADIANCE_For_band * cos(
                        Z__Sun_Angles_Grid_Zenith_Values)) / PI;"""
                    if re.search(r'Sentinel-2', self.satellite, re.I):
                        warnings.warn('Physical gain values unclear for Sentinel-2! This may cause errors when '
                                      'calculating radiance from TOA Reflectance. ESA provides only 12 gain values for '
                                      '13 bands and it not clear for which bands the gains are provided.')
                    raise NotImplementedError("Conversion TOA_Ref to %s is currently not supported." % conv)
                else:  # conv=='TOA_Ref'
                    if self.MetaObj.ScaleFactor != CFG.scale_factor_TOARef:
                        res = self.rescale_array(inArray, CFG.scale_factor_TOARef, self.MetaObj.ScaleFactor)
                        self.MetaObj.ScaleFactor = CFG.scale_factor_TOARef
                        self.log_for_fullArr_or_firstTile(
                            'Rescaling Ref data to scaling factor %d.' % CFG.scale_factor_TOARef)
                    else:
                        res = inArray
                        self.log_for_fullArr_or_firstTile('The input data already represents TOA '
                                                          'reflectance with the desired scale factor of %d.'
                                                          % CFG.scale_factor_TOARef)

            else:  # arr_desc == 'Temp'
                raise NotImplementedError("Conversion Temp to %s is currently not supported." % conv)

            # ensure int16 as output data type (also relevant for auto-setting of nodata value)
            if isinstance(res, (np.ndarray, GeoArray)):
                # change data type to int16 and update nodata values within array
                res = res if res.dtype == np.int16 else res.astype(np.int16)
                res[res == inFill] = get_outFillZeroSaturated(np.int16)[0]

            if optical_thermal == 'optical':
                data_optical, optical_bandsList = res, bList
            else:
                data_thermal, thermal_bandsList = res, bList

        #################################################
        # combine results from optical and thermal data #
        #################################################

        if data_optical is not None and data_thermal is not None:
            bands_opt, bands_therm = [1 if len(d.shape) == 2 else d.shape[2] for d in [data_optical, data_thermal]]
            r, c, b = data_optical.shape[0], data_optical.shape[1], bands_opt + bands_therm
            dataOut = np.empty((r, c, b), data_optical.dtype)

            for idx_out, idx_in in zip(optical_bandsList, range(bands_opt)):
                dataOut[:, :, idx_out] = data_optical[:, :, idx_in]
            for idx_out, idx_in in zip(thermal_bandsList, range(bands_therm)):
                dataOut[:, :, idx_out] = data_thermal[:, :, idx_in]
        else:
            dataOut = data_optical if data_thermal is None else data_thermal
        assert dataOut is not None

        self.update_spec_vals_according_to_dtype('int16')
        tiles_desc = '_'.join([desc for op_th, desc in zip(['optical', 'thermal'],
                                                           [CFG.target_radunit_optical,
                                                            CFG.target_radunit_thermal])
                               if desc in self.dict_LayerOptTherm.values()])

        self.arr = dataOut
        self.arr_desc = tiles_desc

        return {'desc': tiles_desc, 'row_start': rS, 'row_end': rE, 'col_start': cS, 'col_end': cE, 'data': dataOut}

    def validate_GeoTransProj_GeoAlign(self):
        project_dir = os.path.abspath(os.curdir)
        if self.MetaObj.Dataname.startswith('/vsi'):
            os.chdir(os.path.dirname(self.path_archive))
        rasObj = GEOP.GEOPROCESSING(self.MetaObj.Dataname, self.logger)
        if rasObj.geotransform == (0.0, 1.0, 0.0, 0.0, 0.0, 1.0) and rasObj.projection == '':
            if re.search(r'ALOS', self.satellite) and self.MetaObj.ProcLCode == '1B2':
                self.GeoTransProj_ok, self.GeoAlign_ok = False, True
            else:
                self.GeoTransProj_ok, self.GeoAlign_ok = False, False
        os.chdir(project_dir)

    def reference_data(self, out_CS='UTM'):
        """Perform georeferencing of self.arr or the corresponding data on disk respectively.
        Method is skipped if self.GeoAlign_ok and self.GeoTransProj_ok evaluate to 'True'. All attributes connected
        with the georeference of self.arr are automatically updated."""

        from ..io.output_writer import add_attributes_to_ENVIhdr

        if False in [self.GeoAlign_ok, self.GeoTransProj_ok]:
            previous_dataname = self.MetaObj.Dataname
            if hasattr(self, 'arr') and isinstance(self.arr, (GeoArray, np.ndarray)) and \
               self.MetaObj.Dataname.startswith('/vsi'):
                outP = os.path.join(self.ExtractedFolder, self.baseN + '__' + self.arr_desc)
                # FIXME ineffective but needed as long as georeference_by_TieP_or_inherent_GCPs does not support
                # FIXME direct array inputs
                GEOP.ndarray2gdal(self.arr, outPath=outP, geotransform=mapinfo2geotransform(self.MetaObj.map_info),
                                  projection=self.MetaObj.projection,
                                  direction=3)
                assert os.path.isfile(outP), 'Writing tempfile failed.'
                self.MetaObj.Dataname = outP
            rasObj = GEOP.GEOPROCESSING(self.MetaObj.Dataname, self.logger)

            # --Georeference if neccessary
            if self.GeoAlign_ok and not self.GeoTransProj_ok:
                self.logger.info('Adding georeference from metadata to image...')
                rasObj.add_GeoTransform_Projection_using_MetaData(self.MetaObj.CornerTieP_LonLat,
                                                                  CS_TYPE=self.MetaObj.CS_TYPE,
                                                                  CS_DATUM=self.MetaObj.CS_DATUM,
                                                                  CS_UTM_ZONE=self.MetaObj.CS_UTM_ZONE,
                                                                  gResolution=self.MetaObj.gResolution,
                                                                  shape_fullArr=self.shape_fullArr)
                self.add_rasterInfo_to_MetaObj(rasObj)
                add_attributes_to_ENVIhdr(
                    {'map info': self.MetaObj.map_info, 'coordinate system string': self.MetaObj.projection},
                    os.path.splitext(self.MetaObj.Dataname)[0] + '.hdr')
                self.arr = self.MetaObj.Dataname
                self.GeoTransProj_ok = True

            if not self.GeoAlign_ok:
                self.logger.info('Georeferencing image...')
                rasObj.georeference_by_TieP_or_inherent_GCPs(TieP=self.MetaObj.CornerTieP_LonLat, dst_CS=out_CS,
                                                             dst_CS_datum='WGS84', mode='GDAL', use_workspace=True,
                                                             inFill=self.MetaObj.spec_vals['fill'])

                if not CFG.inmem_serialization:
                    path_warped = os.path.join(self.ExtractedFolder, self.baseN + '__' + self.arr_desc)
                    GEOP.ndarray2gdal(rasObj.tondarray(direction=3), path_warped, importFile=rasObj.desc, direction=3)
                    self.MetaObj.Dataname = path_warped
                    self.arr = path_warped
                else:  # CFG.inmem_serialization is True
                    self.arr = rasObj.tondarray(direction=3)

                self.shape_fullArr = [rasObj.rows, rasObj.cols, rasObj.bands]
                self.add_rasterInfo_to_MetaObj()  # uses self.MetaObj.Dataname as inFile
                self.update_spec_vals_according_to_dtype()
                self.calc_mask_nodata()  # uses nodata value from self.MetaObj.spec_vals
                self.GeoTransProj_ok, self.GeoAlign_ok = True, True

            if rasObj.get_projection_type() == 'LonLat':
                self.MetaObj.CornerTieP_LonLat = rasObj.get_corner_coordinates('LonLat')

            if rasObj.get_projection_type() == 'UTM':
                self.MetaObj.CornerTieP_UTM = rasObj.get_corner_coordinates('UTM')

            if CFG.inmem_serialization:
                self.delete_tempFiles()  # these files are needed later in Python execution mode
                self.MetaObj.Dataname = previous_dataname  # /vsi.. pointing directly to raw data archive (which exists)

    def calc_corner_positions(self):
        """Get true corner positions in the form
        [UL, UR, LL, LR] as [(ULrow,ULcol),(URrow,URcol),...],[(ULLon,ULLat),(URLon,URLat),..]"""

        # set lonlat corner positions for outer image edges
        rows, cols = self.shape_fullArr[:2]
        CorPosXY = [(0, 0), (cols, 0), (0, rows), (cols, rows)]
        gt = self.mask_nodata.geotransform
        # using EPSG code ensures that exactly the same WKT code is used in case of in-mem and disk serialization
        prj = EPSG2WKT(self.mask_nodata.epsg)
        CorLatLon = pixelToLatLon(CorPosXY, geotransform=gt, projection=prj)
        self.corner_lonlat = [tuple(reversed(i)) for i in CorLatLon]

        # set true data corner positions (image coordinates)
        assert self.arr_shape == 'cube', 'The given GMS object must represent the full image cube for calculating ,' \
                                         'true corner posistions. Received %s.' % self.arr_shape
        assert hasattr(self,
                       'mask_nodata') and self.mask_nodata is not None, "The L1A object needs to have a nodata mask."
        self.logger.info('Calculating true data corner positions (image and world coordinates)...')

        # if re.search(r'ETM+', self.sensor) and self.acq_datetime > datetime.datetime(year=2003, month=5, day=31,
        #                                                                             tzinfo=datetime.timezone.utc):
        if is_dataset_provided_as_fullScene(self.GMS_identifier):
            kw = dict(algorithm='numpy', assert_four_corners=True)
        else:
            kw = dict(algorithm='shapely', assert_four_corners=False)
        self.trueDataCornerPos = calc_FullDataset_corner_positions(self.mask_nodata, **kw)

        # set true data corner positions (lon/lat coordinates)
        trueCorPosXY = [tuple(reversed(i)) for i in self.trueDataCornerPos]
        trueCorLatLon = pixelToLatLon(trueCorPosXY, geotransform=gt, projection=prj)
        self.trueDataCornerLonLat = [tuple(reversed(i)) for i in trueCorLatLon]

        # set true data corner positions (UTM coordinates)
        # calculate trueDataCornerUTM
        if isProjectedOrGeographic(prj) == 'projected':
            data_corners_utmYX = [imYX2mapYX(imYX, gt=gt) for imYX in self.trueDataCornerPos]
            self.trueDataCornerUTM = [(YX[1], YX[0]) for YX in data_corners_utmYX]

        # set full scene corner positions (image and lonlat coordinates)
        if is_dataset_provided_as_fullScene(self.GMS_identifier):
            assert len(self.trueDataCornerLonLat) == 4, \
                "Dataset %s (entity ID %s) is provided as full scene. Thus exactly 4 image corners must be present " \
                "within the dataset. Found %s corners instead."\
                % (self.scene_ID, self.entity_ID, len(self.trueDataCornerLonLat))
            self.fullSceneCornerPos = self.trueDataCornerPos
            self.fullSceneCornerLonLat = self.trueDataCornerLonLat

        else:

            if re.search(r'AVNIR', self.sensor):
                self.fullSceneCornerPos = calc_FullDataset_corner_positions(self.mask_nodata, algorithm='numpy',
                                                                            assert_four_corners=False)
                # set true data corner positions (lon/lat coordinates)
                trueCorPosXY = [tuple(reversed(i)) for i in self.trueDataCornerPos]
                trueCorLatLon = pixelToLatLon(trueCorPosXY, geotransform=gt, projection=prj)
                self.fullSceneCornerLonLat = [tuple(reversed(i)) for i in trueCorLatLon]

            else:
                # RapidEye or Sentinel-2 data

                if re.search(r'Sentinel-2', self.satellite):
                    # get fullScene corner coordinates by database query
                    # -> calculate footprints for all granules of the same S2 datatake
                    # -> merge them and calculate overall corner positions
                    self.fullSceneCornerPos = [tuple(reversed(i)) for i in CorPosXY]  # outer corner positions
                    self.fullSceneCornerLonLat = self.corner_lonlat  # outer corner positions
                else:
                    # RapidEye
                    raise NotImplementedError  # FIXME

    def calc_center_AcqTime(self):
        """Calculate scene acquisition time if not given in provider metadata."""

        if self.MetaObj.AcqTime == '':
            self.MetaObj.calc_center_acquisition_time(self.fullSceneCornerLonLat, self.logger)

        # update timestamp
        self.acq_datetime = self.MetaObj.AcqDateTime

    def calc_orbit_overpassParams(self):
        """Calculate orbit parameters."""

        if is_dataset_provided_as_fullScene(self.GMS_identifier):
            self.MetaObj.overpassDurationSec, self.MetaObj.scene_length = \
                self.MetaObj.get_overpassDuration_SceneLength(
                    self.fullSceneCornerLonLat, self.fullSceneCornerPos, self.shape_fullArr, self.logger)

    def add_rasterInfo_to_MetaObj(self, custom_rasObj=None):
        """
        Add the attributes 'rows','cols','bands','map_info','projection' and 'physUnit' to self.MetaObj
        """
        # TODO is this info still needed in MetaObj?
        project_dir = os.path.abspath(os.curdir)
        if self.MetaObj.Dataname.startswith('/vsi'):
            os.chdir(os.path.dirname(self.path_archive))

        rasObj = custom_rasObj if custom_rasObj else GEOP.GEOPROCESSING(self.MetaObj.Dataname, self.logger)
        self.MetaObj.add_rasObj_dims_projection_physUnit(rasObj, self.dict_LayerOptTherm, self.logger)

        prj_type = rasObj.get_projection_type()
        assert prj_type, "Projections other than LonLat or UTM are currently not supported. Got. %s." % prj_type
        if prj_type == 'LonLat':
            self.MetaObj.CornerTieP_LonLat = rasObj.get_corner_coordinates('LonLat')
        else:  # UTM
            self.MetaObj.CornerTieP_UTM = rasObj.get_corner_coordinates('UTM')

        if self.MetaObj.Dataname.startswith('/vsi'):  # only if everthing is kept in memory
            os.chdir(project_dir)
            self.MetaObj.bands = 1 if len(self.arr.shape) == 2 else self.arr.shape[2]

        self.arr.gt = mapinfo2geotransform(self.MetaObj.map_info)
        if not self.arr.prj:
            self.arr.prj = self.MetaObj.projection

        # must be set here because nodata mask has been computed from self.arr without geoinfos:
        self.mask_nodata.gt = self.arr.gt
        self.mask_nodata.prj = self.arr.prj

    def update_spec_vals_according_to_dtype(self, dtype=None):
        """Update self.MetaObj.spec_vals.

        :param dtype:   <str> or <numpy data type> The data type to be used for updating.
                        If not specified the data type of self.arr is used.
        """
        if dtype is None:
            if hasattr(self, 'arr') and isinstance(self.arr, np.ndarray):
                dtype = self.arr.dtype
            else:
                arr = gdalnumeric.LoadFile(self.arr, 0, 0, 1, 1) if hasattr(self, 'arr') and isinstance(self.arr,
                                                                                                        str) else \
                    gdalnumeric.LoadFile(self.MetaObj.Dataname, 0, 0, 1, 1)
                assert arr is not None
                dtype = arr.dtype

        self.MetaObj.spec_vals['fill'], self.MetaObj.spec_vals['zero'], self.MetaObj.spec_vals['saturated'] = \
            get_outFillZeroSaturated(dtype)
        self.arr.nodata = self.MetaObj.spec_vals['fill']

    def calc_mean_VAA(self):
        """Calculates mean viewing azimuth angle using sensor flight line derived from full scene corner coordinates."""

        if is_dataset_provided_as_fullScene(self.GMS_identifier):
            self.VAA_mean = \
                GEOP.calc_VAA_using_fullSceneCornerLonLat(self.fullSceneCornerLonLat, self.MetaObj.orbitParams)
        else:
            # e.g. Sentinel-2 / RapidEye
            self.logger.debug('No precise calculation of mean viewing azimuth angle possible because orbit track '
                              'cannot be reconstructed from dataset since full scene corner positions are unknown. '
                              'Mean VAA angle is filled with the mean value of the viewing azimuth array provided '
                              'in metadata.')
            self.VAA_mean = self.MetaObj.IncidenceAngle

        self.logger.info('Calculation of mean VAA...: %s' % round(self.VAA_mean, 2))
