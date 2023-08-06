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
GEOPROCESSING OBJECT
"GIS operations to manipulate spatial data.
Takes an input dataset, performs an operation on that dataset
and returns the result of the operation as an output dataset.
"""

import collections
import datetime
import math
import os
import re
import subprocess
import time
import warnings

import numpy as np
from matplotlib import dates as mdates

# custom
try:
    from osgeo import osr
    from osgeo import gdal
    from osgeo import gdalnumeric
except ImportError:
    import osr
    import gdal
    import gdalnumeric
from gdalconst import GA_ReadOnly

import pyproj
from pyorbital import astronomy
import ephem
from shapely.geometry import MultiPoint, Polygon
from shapely.ops import cascaded_union

from geoarray import GeoArray
from py_tools_ds.geo.coord_grid import snap_bounds_to_pixGrid
from py_tools_ds.geo.coord_trafo import transform_utm_to_wgs84, transform_wgs84_to_utm, mapXY2imXY, imXY2mapXY

from ..options.config import GMS_config as CFG
from ..misc.definition_dicts import get_outFillZeroSaturated
from ..misc.logging import close_logger

__author__ = 'Daniel Scheffler', 'Robert Behling'


class GEOPROCESSING(object):

    def __init__(self, geodata, logger, workspace=None, subset=None, v=None):
        self.logger = logger
        self.subset = subset
        self.target_radunit_optical = ''
        self.target_radunit_thermal = ''
        self.outpath_conv = None
        # check gdal environment
        if v is not None:
            self.logger.debug("\n--")
            self.logger.debug("GDAL Environment:")
            self.logger.debug("\tGDAL-version: ", gdal.VersionInfo())
            self.logger.debug("\tmaximum amount of memory (as bytes) for caching within GDAL: ", gdal.GetCacheMax())
            self.logger.debug("\tthe amount of memory currently used for caching within GDAL: ", gdal.GetCacheUsed())
            self.logger.debug("\tPopFinderLocation: ", gdal.PopFinderLocation())

            # load Raster file to an GDAL Object
        # ----register drivers
        # • A driver is an object that knows how to interact with a certain data type (such as a shapefile)
        # • Need an appropriate driver in order to read or write data (need it explicitly for write)
        # register all drivers for reading

        gdal.AllRegister()

        assert type(geodata) in [str, gdal.Dataset], \
            "GEOP: The argument 'geodata' has to be a path or a gdal.Dataset. Got %s." % type(geodata)
        if isinstance(geodata, str):
            # ----open files Open(<filename>, <GDALAccess>)
            # open raster to gdal object
            self.inDs = (gdal.Open(geodata, GA_ReadOnly))
            self.filepath, self.filename = os.path.split(geodata)
            self.shortname, self.extension = os.path.splitext(self.filename)
            if v:
                self.logger.debug("\n--")
                self.logger.debug("load data to GDAL:\n\tfilepath: %s\n\tfilename: %s" % (self.filepath, self.filename))
            if not geodata.startswith('/vsi'):
                path2check = geodata
            else:
                # gdal_prefix_dict = {'/vsizip': '.zip', '/vsitar': '.tar', '/vsitar': '.tar.gz',
                #                     '/vsitar' '.gz': '/vsigzip'}
                p1 = [geodata.split(i)[0] + i for i in ['.zip', '.tar', '.tar.gz', '.gz', '.tgz']
                      if len(geodata.split(i)) > 1 and geodata.split(i)[1].startswith('/')][0]
                path2check = os.path.abspath('.' + re.search(r'/vsi[\s\S]*(/[\s\S,.]*)', p1, re.I).group(1))
            assert os.path.exists(path2check), "ERROR: data %s does not exist!" % path2check
            assert self.inDs is not None, "ERROR: Could not open %s!" % self.filename
        elif isinstance(geodata, gdal.Dataset):
            self.inDs = geodata
            del geodata
            self.filepath, self.filename = None, self.inDs.GetDescription()
            self.shortname, self.extension = os.path.splitext(self.filename)

        # ****OBJECT ATTRIBUTES***************************************************
        self.workspace = os.path.join(CFG.path_tempdir, 'GEOPROCESSING_temp') if workspace is None else workspace
        if v:
            self.logger.debug("\n--")
            self.logger.debug("\ttemporary geoprocessing workspace", self.workspace)

        # --Getting columns, rows and number of bands of inputdataset
        self.desc = self.inDs.GetDescription()
        if self.subset is None or self.subset[0] == 'cube':
            self.cols = self.inDs.RasterXSize
            self.rows = self.inDs.RasterYSize
            self.bands = self.inDs.RasterCount
            self.colStart = 0
            self.rowStart = 0
            self.bandStart = 0
            self.colEnd = self.cols - 1
            self.rowEnd = self.rows - 1
            self.bandEnd = self.bands - 1
            self.bandsList = range(self.bandStart, self.bandEnd + 1)
        else:
            assert isinstance(self.subset, list) and len(self.subset) == 2, \
                "Unable to initialize GEOP object due to bad arguments at subset keyword. Got %s." % self.subset
            self.subset_kwargs_to_cols_rows_bands_colStart_rowStart_bandStart()

        self.DataProp = [self.cols, self.rows, self.bands, self.colStart, self.rowStart, self.bandStart]
        if v is not None:
            self.logger.info("""--\nproperties of the inputdataset\n\tcolumns[cols]: %s\n\trows[rows]:
            %s\n\tbands[bands]: %s\n\tDescription[desc]: %s""" % (self.cols, self.rows, self.bands, self.desc))

        # --Getting driver infos of inputdataset
        self.drname_s = self.inDs.GetDriver().ShortName
        self.drname_l = self.inDs.GetDriver().LongName
        self.drhelp = self.inDs.GetDriver().HelpTopic
        self.DriverProp = [self.drname_s, self.drname_l, self.drhelp]

        if v is not None:
            self.logger.info(
                "\tDriverShortName[drname_s]: %s\n\tDriverLongName[drnam_l]: %s\n\tDriverHelpWebsite[drhelp]: %s" % (
                    self.drname_s, self.drname_l, self.drhelp))

        # --Getting Georeference info of inputdataset
        self.geotransform = self.inDs.GetGeoTransform()
        self.projection = self.inDs.GetProjection()
        self.originX = self.geotransform[0]
        self.originY = self.geotransform[3]
        self.pixelWidth = self.geotransform[1]
        self.pixelHeight = self.geotransform[5]
        self.rot1 = self.geotransform[2]
        self.rot2 = self.geotransform[4]
        self.extent = [self.originX, self.originY, self.originX + (self.cols * self.pixelWidth),
                       self.originY + (self.rows * self.pixelHeight)]  # [ulx, uly, lrx, lry]
        self.GeoProp = [self.originX, self.originY, self.pixelWidth, self.pixelHeight, self.rot1, self.rot2]

        if v is not None:
            self.logger.info("\toriginX[originX]:", self.originX, "\n\toriginY[originY]:", self.originY,
                             "\n\tresolution: X[pixelWidth]:" + str(self.pixelWidth),
                             "Y[pixelHeight]:" + str(self.pixelHeight), "\n\trotation: a[rot1]:" + str(self.rot1),
                             "b[rot2]:" + str(self.rot2))

        self.Prop = {'DataProp': self.DataProp, 'DriverProp': self.DriverProp, 'GeoProp': self.GeoProp}

    """****OBJECT METHODS******************************************************"""

    def __getstate__(self):
        """Defines how the attributes of GEOPROCESSING instances are pickled."""
        close_logger(self.logger)
        self.logger = None

        return self.__dict__

    def __del__(self):
        close_logger(self.logger)
        self.logger = None

    def subset_kwargs_to_cols_rows_bands_colStart_rowStart_bandStart(self):
        shape_fullArr = [self.inDs.RasterYSize, self.inDs.RasterXSize, self.inDs.RasterCount]
        self.rows, self.cols, self.bands, self.rowStart, self.rowEnd, self.colStart, self.colEnd, self.bandStart, \
            self.bandEnd, self.bandsList = get_subsetProps_from_subsetArg(shape_fullArr, self.subset).values()
        self.subset = self.subset if self.subset[0] != 'cube' else None

    def update_dataset_related_attributes(self):
        self.desc = self.inDs.GetDescription()
        self.filepath, self.filename = os.path.split(self.desc)
        self.shortname, self.extension = os.path.splitext(self.filename)

        if self.subset is None or self.subset == 'cube':
            self.cols = self.inDs.RasterXSize
            self.rows = self.inDs.RasterYSize
            self.bands = self.inDs.RasterCount
            self.colStart = 0
            self.rowStart = 0
            self.bandStart = 0
            self.colEnd = self.cols - 1
            self.rowEnd = self.rows - 1
            self.bandEnd = self.bands - 1
            self.bandsList = range(self.bandStart, self.bandEnd + 1)
        else:
            self.subset_kwargs_to_cols_rows_bands_colStart_rowStart_bandStart()

        self.DataProp = [self.cols, self.rows, self.bands, self.colStart, self.rowStart, self.bandStart]
        self.drname_s = self.inDs.GetDriver().ShortName
        self.drname_l = self.inDs.GetDriver().LongName
        self.drhelp = self.inDs.GetDriver().HelpTopic
        self.DriverProp = [self.drname_s, self.drname_l, self.drhelp]

        self.geotransform = self.inDs.GetGeoTransform()
        self.projection = self.inDs.GetProjection()
        self.originX = self.geotransform[0]
        self.originY = self.geotransform[3]
        self.pixelWidth = self.geotransform[1]
        self.pixelHeight = self.geotransform[5]
        self.rot1 = self.geotransform[2]  # FIXME check
        self.rot2 = self.geotransform[4]
        self.extent = [self.originX, self.originY, self.originX + (self.cols * self.pixelWidth),
                       self.originY + (self.rows * self.pixelHeight)]  # [ulx, uly, lrx, lry]
        self.GeoProp = [self.originX, self.originY, self.pixelWidth, self.pixelHeight, self.rot1, self.rot2]

        self.Prop = {'DataProp': self.DataProp, 'DriverProp': self.DriverProp, 'GeoProp': self.GeoProp}

    def gdalinfo(self):
        """get properties of the Inputdatasets via gdalinfo

        (die Infos die er hier ausschreibt in subrocess.Popen können einer variable als Text übergeben werden. Aus
        diesem Text kann ich dann die Infos als Attribute ausschreiben.
        als ersatz für die jetzige Attributerzeugung
        Muss die Attributerzeugung wirklich sein? kann ich nicht alle irgendwie über das GDAL-objekt abfragen!
        bis jetzt hab ich aber nur die Infos die oben stehen als Abfrage ermöglichen können
        """
        subprocess.Popen(["gdalinfo", os.path.join(self.filepath, self.filename)]).wait()

    def add_GeoTransform_Projection_using_MetaData(self, CornerTieP_LonLat, CS_EPSG=None, CS_TYPE=None, CS_DATUM=None,
                                                   CS_UTM_ZONE=None, gResolution=None, shape_fullArr=None):
        """ Method assumes that north is up. Map rotations are not respected.

        :param CornerTieP_LonLat:
        :param CS_EPSG:
        :param CS_TYPE:
        :param CS_DATUM:
        :param CS_UTM_ZONE:
        :param gResolution:
        :param shape_fullArr:
        """
        if CornerTieP_LonLat == [] or CornerTieP_LonLat is None:
            self.logger.error('Failed to add projection. L1A object must have corner coordinates.')
        else:
            # Projection
            srs = osr.SpatialReference()
            if CS_EPSG is not None:
                srs.ImportFromEPSG(CS_EPSG)
                self.inDs.SetProjection(srs.ExportToWkt())
            elif CS_TYPE is not None and CS_DATUM is not None:
                if CS_TYPE == 'UTM' and CS_DATUM == 'WGS84':
                    UTM_zone = int(1 + (CornerTieP_LonLat[0][0] + 180.0) / 6.0) if CS_UTM_ZONE is None else CS_UTM_ZONE
                    EPSG_code = int('326' + str(UTM_zone)) if CornerTieP_LonLat[0][1] > 0.0 else int(
                        '327' + str(UTM_zone))
                elif CS_TYPE == 'LonLat' and CS_DATUM == 'WGS84':
                    EPSG_code = 4326
                else:
                    self.logger.error('Coordinate system type %s is not yet implemented. Since corner coordinates in '
                                      'Lon/Lat are available, it has been set to Lon/Lat.' % CS_TYPE)
                    EPSG_code, CS_TYPE, CS_DATUM = (4326, 'LonLat', 'WGS84')
                srs.ImportFromEPSG(EPSG_code)
                self.inDs.SetProjection(srs.ExportToWkt())
            else:
                CS_TYPE, CS_DATUM, CS_EPSG = ('LonLat', 'WGS84', 4326)
                srs.ImportFromEPSG(CS_EPSG)
                self.inDs.SetProjection(srs.ExportToWkt())
            self.projection = self.inDs.GetProjection()
            # GeoTransform
            self.originX, self.originY = CornerTieP_LonLat[0] if CS_TYPE == 'LonLat' else transform_wgs84_to_utm(
                CornerTieP_LonLat[0][0], CornerTieP_LonLat[0][1])
            if gResolution is None or gResolution == -99.:
                if shape_fullArr is None:
                    self.logger.error("Failed to add projection. Please provide at least one of the arguments "
                                      "'gResolution' or 'shape_fullArr'!")
                else:
                    gResolution = float(pyproj.Geod(ellps=CS_DATUM).inv(CornerTieP_LonLat[0][0],
                                                                        CornerTieP_LonLat[0][1],
                                                                        CornerTieP_LonLat[1][0],
                                                                        CornerTieP_LonLat[1][1])[2]) / shape_fullArr[1]
                    # distance in [m]/cols
                    self.logger.info(
                        "While adding projection the ground sampling distance had to be calculated. It has "
                        "been set to %s meters." % gResolution)
            self.pixelWidth, self.pixelHeight, self.rot1, self.rot2 = (gResolution, gResolution * -1., 0, 0)
            GT = [self.originX, self.pixelWidth, self.rot1, self.originY, self.rot2, self.pixelHeight]
            self.inDs.SetGeoTransform(GT)
            self.geotransform = self.inDs.GetGeoTransform()

    def georeference_by_TieP_or_inherent_GCPs(self, use_inherent_GCPs=False, TieP=None, dst_EPSG_code=None,
                                              dst_CS='UTM', dst_CS_datum='WGS84', mode='GDAL', use_workspace=True,
                                              inFill=None):
        """Warp image to new Projection.

        :param use_inherent_GCPs:
        :param TieP:                Corner Tie Points - always LonLat.
        :param dst_EPSG_code:       EPSG-Code defines LonLat or UTM coordinates.
        :param dst_CS:
        :param dst_CS_datum:
        :param mode:
        :param use_workspace:
        :param inFill:
        """
        if use_inherent_GCPs and TieP is None:
            self.logger.info('Georeferencing dataset using inherent GCP list...')
        if use_inherent_GCPs and TieP:
            self.logger.info("\n\nWARNING: User defined tie points are provided though 'use_inherent_GCPs' is true. "
                             "Georeferencing dataset using inherent GCP list...")
        if not use_inherent_GCPs and TieP:
            self.logger.info('Georeferencing dataset by given tiepoints...')
            gcp_ul = [1, 1, TieP[0][0], TieP[0][1]]  # col/row/map_x/map_y
            gcp_ur = [self.cols, 1, TieP[1][0], TieP[1][1]]
            gcp_ll = [1, self.rows, TieP[2][0], TieP[2][1]]
            gcp_lr = [self.cols, self.rows, TieP[3][0], TieP[3][1]]

        if dst_EPSG_code is None or dst_EPSG_code == -99.:
            if dst_CS == 'UTM' and dst_CS_datum == 'WGS84':
                UTM_zone = int(1 + (TieP[0][0] + 180.0) / 6.0)
                dst_EPSG_code = int('326' + str(UTM_zone)) if TieP[0][1] > 0.0 else int('327' + str(UTM_zone))
            if dst_CS == 'LonLat' and dst_CS_datum == 'WGS84':
                dst_EPSG_code = 4326

        assert mode in ['rasterio', 'GDAL'], "The 'mode' argument must be set to 'rasterio' or 'GDAL'."

        if mode == 'rasterio':
            """needs no temporary files but does not support multiprocessing"""
            raise NotImplementedError()
            # out_prj = EPSG2WKT(dst_EPSG_code)
            # proj_geo = isProjectedOrGeographic(self.projection)
            #
            # assert proj_geo in ['projected', 'geographic']
            # TieP = TieP if proj_geo == 'geographic' else \
            #     [transform_wgs84_to_utm(LonLat[0], LonLat[1], get_UTMzone(prj=self.projection)) for LonLat in TieP]
            # xmin, xmax, ymin, ymax = HLP_F.corner_coord_to_minmax(TieP)
            # t0 = time.time()
            # in_arr = np.swapaxes(np.swapaxes(gdalnumeric.LoadFile(self.desc), 0, 2), 0, 1)
            # print('reading time', time.time() - t0)
            # if inFill is None:
            #     inFill = get_outFillZeroSaturated(in_arr.dtype)[0]
            # out_nodataVal = get_outFillZeroSaturated(in_arr.dtype)[0]
            # t0 = time.time()

            # warped, gt, prj = warp_ndarray(in_arr, self.geotransform, self.projection, out_prj,
            #                                out_bounds=([xmin, ymin, xmax, ymax]), rspAlg='cubic',
            #                                in_nodata=inFill, out_nodata=out_nodataVal)[0]

            # multiprocessing: not implemented further because multiproceesing within Python Mappers is not possible
            # args = [(in_arr[:,:,i],self.geotransform,self.projection,out_prj,([xmin, ymin, xmax, ymax]),
            #        2,in_nodataVal) for i in range(in_arr.shape[2])]
            # import multiprocessing
            # with multiprocessing.Pool() as pool:
            #    results = pool.map(warp_mp,args)

            # print('warping time', time.time() - t0)
            # from spectral.io import envi
            # envi.save_image('/dev/shm/test_warped.hdr',warped,dtype=str(np.dtype(warped.dtype)),
            #                force=True,ext='.bsq',interleave='bsq')

        else:  # mode == 'GDAL'
            """needs temporary files but does support multiprocessing and configuring cache size"""
            t0 = time.time()
            in_dtype = gdalnumeric.LoadFile(self.desc, 0, 0, 1, 1).dtype
            if inFill is None:
                inFill = get_outFillZeroSaturated(in_dtype)[0]
            out_nodataVal = get_outFillZeroSaturated(in_dtype)[0]
            gcps = ' '.join(['-gcp %s %s %s %s' % tuple(gcp) for gcp in [gcp_ul, gcp_ur, gcp_ll, gcp_lr]])

            if use_workspace:
                inFile = self.desc
                translatedFile = os.path.splitext(inFile)[0] + '_translate' if not use_inherent_GCPs else inFile
                warpedFile = os.path.splitext(inFile)[0] + '_warp'
                if not use_inherent_GCPs:
                    os.system('gdal_translate -of ENVI %s \
                        -a_srs EPSG:%s -q %s %s' % (gcps, dst_EPSG_code, inFile, translatedFile))

                    # os.system('gdalwarp -of ENVI --config GDAL_CACHEMAX 2048 -wm 2048 -ot Int16 -t_srs EPSG:%s -tps
                    #   -r cubic -srcnodata -%s -dstnodata %s -overwrite -q %s %s' \
                    #   %(dst_EPSG_code, in_nodataVal,out_nodataVal, translatedFile, warpedFile))
                    os.system('gdalwarp -of ENVI --config GDAL_CACHEMAX 2048 -wm 2048 -t_srs EPSG:%s -tps -r \
                        cubic -srcnodata %s -dstnodata %s -multi -overwrite -wo NUM_THREADS=%s -q %s %s'
                              % (dst_EPSG_code, inFill, out_nodataVal, CFG.CPUs, translatedFile, warpedFile))
                    # import shutil
                    # only for bugfixing:
                    # shutil.copy(translatedFile, \
                    #     '//misc/hy5/scheffler/Skripte_Models/python/gms_preprocessing/sandbox/out/')
                    # shutil.copy(translatedFile+'.hdr',\
                    #     '//misc/hy5/scheffler/Skripte_Models/python/gms_preprocessing/sandbox/out/')
                    # shutil.copy(warpedFile, \
                    #     '//misc/hy5/scheffler/Skripte_Models/python/gms_preprocessing/sandbox/out/')
                    # shutil.copy(warpedFile+'.hdr', \
                    #     '//misc/hy5/scheffler/Skripte_Models/python/gms_preprocessing/sandbox/out/')
            else:
                VRT_name = os.path.splitext(os.path.basename(self.desc))[0] + '.vrt'
                # dst_ds = gdal.GetDriverByName('VRT').CreateCopy(VRT_name, self.inDs, 0)
                # del dst_ds
                inFile = VRT_name
                translatedFile = os.path.splitext(inFile)[0] + '_translate.vrt' if not use_inherent_GCPs else self.desc
                warpedFile = os.path.splitext(inFile)[0] + '_warp.vrt'
                if not use_inherent_GCPs:
                    os.system('gdal_translate -of VRT %s \
                        -a_srs EPSG:%s -q %s %s' % (gcps, dst_EPSG_code, inFile, translatedFile))
                    # os.system('gdalwarp -of VRT --config GDAL_CACHEMAX 500 -wm 500 -ot Int16 -t_srs EPSG:%s -tps -r \
                    #     cubic -srcnodata %s -dstnodata %s -multi -overwrite -wo NUM_THREADS=10 -q %s %s' \
                    #     %(dst_EPSG_code,in_nodataVal,out_nodataVal,translatedFile,warpedFile))
                    os.system('gdalwarp -of VRT --config GDAL_CACHEMAX 2048 -wm 2048 -ot Int16 -t_srs EPSG:%s -tps -r \
                        cubic -srcnodata %s -dstnodata %s -overwrite -multi -wo NUM_THREADS=%s -q %s %s'
                              % (dst_EPSG_code, inFill, out_nodataVal, CFG.CPUs, translatedFile, warpedFile))
                    # print('warped')
            print('GDAL warping time', time.time() - t0)

            self.inDs = gdal.OpenShared(warpedFile, GA_ReadOnly) \
                if inFile.endswith('.vrt') else gdal.Open(warpedFile, GA_ReadOnly)
            # print('read successful')
            self.update_dataset_related_attributes()

    # def get_row_column_bounds(self,arr_shape = None, arr_pos = None):
    #    if arr_shape == None and arr_pos == None:
    #        arr_shape = 'cube'
    #    try:
    #        if arr_shape == 'row': # arr_pos = int
    #            row_start,row_end,col_start,col_end, rows,cols = arr_pos,arr_pos+1,0,self.cols, 1,self.cols
    #        elif arr_shape == 'col': # arr_pos = int
    #            row_start,row_end,col_start,col_end, rows,cols = 0,self.rows,arr_pos,arr_pos+1, self.rows,1
    #        elif arr_shape == 'band' or arr_shape == 'cube': # arr_pos = None
    #            row_start,row_end,col_start,col_end, rows,cols = 0,self.rows-1,0,self.cols-1, self.rows,self.cols
    #        elif arr_shape == 'block' or arr_shape == 'custom':
    #            # arr_pos = [ (row_start,row_end),(col_start,col_end),(band_start,band_end) ]
    #            row_start,row_end,col_start,col_end, rows,cols = \
    #                arr_pos[0][0],arr_pos[0][1],arr_pos[1][0],arr_pos[1][1], \
    #                arr_pos[0][1]+1-arr_pos[0][0],arr_pos[1][1]+1-arr_pos[1][0]
    #        elif arr_shape == 'pixel': # arr_pos = (x,y)
    #            row_start,row_end,col_start,col_end, rows,cols = arr_pos[0],arr_pos[0]+1,arr_pos[1],arr_pos[1]+1, 1,1
    #        return row_start,row_end,col_start,col_end,rows,cols
    #    except:
    #        self.logger.error(
    #            'Error while setting row and column bounds. Got arr_shape = %s and arr_pos = %s' %(arr_shape,arr_pos))

    def get_projection_type(self):
        return 'LonLat' if osr.SpatialReference(self.projection).IsGeographic() else 'UTM' if osr.SpatialReference(
            self.projection).IsProjected() else None

    def get_corner_coordinates(self, targetProj):
        """Returns corner coordinates of the entire GEOP object in lon/lat or UTM.

        ATTENTION: coordinates represent PIXEL CORNERS:
            UL=UL-coordinate of (0,0)
            UR=UR-coordinate of (0,self.cols-1)
            => lonlat_arr always contains UL-coordinate of each pixel

        :param targetProj: 'LonLat' or 'UTM'
        """
        UL_LonLat = self.pixelToWorldCoord_using_geotransform_and_projection((0, 0), targetProj)
        # self.cols statt self.cols-1, um Koordinate am rechten Pixelrand zu berechnen:
        UR_LonLat = self.pixelToWorldCoord_using_geotransform_and_projection((0, self.cols), targetProj)
        LL_LonLat = self.pixelToWorldCoord_using_geotransform_and_projection((self.rows, 0), targetProj)
        LR_LonLat = self.pixelToWorldCoord_using_geotransform_and_projection((self.rows, self.cols), targetProj)
        UL_LonLat = tuple([round(i, 10) for i in UL_LonLat])
        UR_LonLat = tuple([round(i, 10) for i in UR_LonLat])
        LL_LonLat = tuple([round(i, 10) for i in LL_LonLat])
        LR_LonLat = tuple([round(i, 10) for i in LR_LonLat])
        return [UL_LonLat, UR_LonLat, LL_LonLat, LR_LonLat]

    def calc_mask_data_nodata(self, array=None, custom_nodataVal=-9999):
        """Berechnet den Bildbereich, der von allen Kanälen abgedeckt wird.

        :param array:               input numpy array to be used for mask calculation (otherwise read from disk)
        :param custom_nodataVal:
        """
        nodataVal = get_outFillZeroSaturated(np.int16)[0] if custom_nodataVal is None else custom_nodataVal
        in_arr = array if array is not None else np.swapaxes(np.swapaxes(gdalnumeric.LoadFile(self.desc), 0, 2), 0, 1)
        return np.all(np.where(in_arr == nodataVal, 0, 1), axis=2)

    def pixelToWorldCoord_using_geotransform_and_projection(self, Pixel_row_col, targetProj):
        if targetProj not in ['UTM', 'LonLat']:
            self.logger.error("Failed to calculate world coordinates of true data corners. Target projection must be "
                              "'UTM' or 'LonLat'. Got %s" % targetProj)
        row, col = Pixel_row_col
        XWorld = self.geotransform[0] + col * self.geotransform[1]
        YWorld = self.geotransform[3] + row * self.geotransform[5]
        src_srs = osr.SpatialReference()
        src_srs.ImportFromWkt(self.projection)
        if src_srs.IsGeographic() and targetProj == 'LonLat' or src_srs.IsProjected() and targetProj == 'UTM':
            return XWorld, YWorld
        elif src_srs.IsProjected() and targetProj == 'LonLat':
            return transform_utm_to_wgs84(XWorld, YWorld, src_srs.GetUTMZone())  # [Lon,Lat]
        else:  # geographic to UTM
            return transform_wgs84_to_utm(XWorld, YWorld)  # [HW,RW]

    def tondarray(self, direction=1, startpix=None, extent=None, UL=None, LR=None, v=0):
        """Convert gdalobject to 3dimensional ndarray stack ([x,y,z]).

        :param direction:   1: shape: [bands, rows, cols]
                                -> same as theres read envi structure ([band1],[band2],..[bandn])
                            2: shape: [rows, bands, cols]
                            3: shape: [rows, cols, bands]
                                -> Structure used in PIL and IDL for example
                                ([pixband1,pixband2,..,pixbandn],[pixband1,pixband2,..,pixbandn],...)
        :param startpix:    [x,y] pixels->UL:pixelcoordinates for subset generation
        :param extent:      [cols, rows] -> number of pixels in x and y-direction
        :param UL:          [x,y] map coordinates -> UL map coordinates for subset generation
        :param LR:          [x,y] map coordinates -> LR map coordinates for subset generation
        :param v:
        """
        # -- test of given inputparameter
        test = [startpix is not None, extent is not None, UL is not None, LR is not None]

        if test == [False, False, False, False]:
            startpix = [0, 0]
            extent = [self.cols, self.rows]

        # only startpixel coordinates given. extent set to startcoordinates to LR of the image
        elif test == [True, False, False, False]:
            assert len(startpix) == 2 and startpix[0] < self.cols and startpix[1] < self.rows, \
                "XXX-ERROR-XXX: Start coordinates x: %i, y: %i out of range" % (startpix[0], startpix[1])
            extent = [self.cols - startpix[0], self.rows - startpix[1]]

        # startpix and extent given
        elif test == [True, True, False, False]:
            assert len(startpix) == 2 and startpix[0] < self.cols and startpix[1] < self.rows and len(extent) == 2, \
                "XXX-ERROR-XXX: Start coordinates x: %i, y: %i out of range" % (startpix[0], startpix[1])
            if extent[0] > self.cols - startpix[0]:
                extent[0] = self.cols - startpix[0]
            elif extent[1] > self.rows - startpix[1]:
                extent[1] = self.rows - startpix[1]

        # extent and UL given
        elif test == [False, True, True, False]:
            pass
        # only UL coordinates given. extent set to startcoordinates to LR of the image (use UL coordnates if they are
        # within the image otherwise UL=origin of the image)
        elif test == [False, False, True, False]:
            assert len(UL) == 2, "XXX-ERROR-XXX: A list of 2 arguments (numbers) for UL required"
            # convert coordinates to float
            UL = [float(UL[0]), float(UL[1])]
            # Test if x of UL is within the image
            if not self.originX <= UL[0] <= (self.originX + self.cols * self.pixelWidth):
                UL[0] = self.originX
            # Test if y of UL is within the image
            if not self.originY >= UL[1] >= (self.originY + self.rows * self.pixelHeight):
                UL[1] = self.originY
            # convert UL in pixelcoordinates
            startpix = [int(float((UL[0] - self.originX)) / float(self.pixelWidth)),
                        int(float((UL[1] - self.originY)) / float(self.pixelHeight))]
            extent = [self.cols - startpix[0], self.rows - startpix[1]]

        # UL and LR coordinates given (use UL and LR coordinates if they are within the image otherwise use the whole
        # image)
        elif test == [False, False, True, True]:
            assert len(UL) == 2 and len(LR) == 2, \
                "XXX-ERROR-XXX: A list of 2 arguments (numbers) for UL and for LR is required"
            # convert coordinates to float
            UL = [float(UL[0]), float(UL[1])]
            LR = [float(LR[0]), float(LR[1])]
            # Test if x of UL is within the image
            if not self.originX <= UL[0] <= (self.originX + self.cols * self.pixelWidth):
                UL[0] = self.originX
            # Test if y of UL is within the image
            if not self.originY >= UL[1] >= (self.originY + self.rows * self.pixelHeight):
                UL[1] = self.originY
            # Test if x of LR is within the image
            if not self.originX <= LR[0] <= (self.originX + self.cols * self.pixelWidth):
                LR[0] = self.originX + self.cols * self.pixelWidth
            # Test if y of UL is within the image
            if not self.originY >= LR[1] >= (self.originY + self.rows * self.pixelHeight):
                LR[1] = self.originY + self.rows * self.pixelHeight
            # convert UL in pixelcoordinates
            startpix = [int(float((UL[0] - self.originX)) / float(self.pixelWidth)),
                        int(float((UL[1] - self.originY)) / float(self.pixelHeight))]
            # get extent
            extent = [int(float((LR[0] - UL[0])) / self.pixelWidth + 0.5),
                      int(float((LR[1] - UL[1])) / self.pixelHeight + 0.5)]

            # if UL or LR are the same. only one pixel selected
            if extent[0] == 0:
                extent[0] = 1
            if extent[1] == 0:
                extent[1] = 1
        if v:
            print("\t startpix:", startpix)
            print("\t extent:", extent)

        if self.subset is not None and self.subset != 'cube':  # rasObj instanced as subset
            if [self.inDs.RasterYSize, self.inDs.RasterXSize] != [self.rows,
                                                                  self.cols]:  # inDs does not represent subset
                startpix = [startpix[0] + self.colStart, startpix[1] + self.rowStart]
                extent = [self.cols, self.rows]

        if self.subset is not None and self.subset[0] == 'custom' and \
                self.target_radunit_optical == '' and self.target_radunit_thermal == '':
            # conversion to Rad or Ref overwrites self.inDs
            # => custom bandsList contains bands that are NOT in range(self.bands)
            bands2process = self.bandsList
        else:  # normal case
            bands2process = range(self.bands)

        np_dtype = convertGdalNumpyDataType(gdal.GetDataTypeName(self.inDs.GetRasterBand(1).DataType))
        im = np.empty((self.rows, self.cols, len(bands2process)), np_dtype)
        for out_idx, x in enumerate(bands2process):
            im[:, :, out_idx] = self.inDs.GetRasterBand(x + 1).ReadAsArray(startpix[0], startpix[1], extent[0],
                                                                           extent[1])
        if direction == 1:  # bands, rows, cols;  so wie Theres es gebastelt hat
            im = np.rollaxis(im, 2)
        elif direction == 2:  # rows, bands, cols
            im = np.swapaxes(im, 1, 2)
        elif direction == 3:  # rows, cols, bands;  so wie in PIL bzw. IDL benötigt
            pass  # bands, rows,cols
        return im

    def Layerstacking(self, layers_pathlist, path_output=None):
        rows, cols, bands = self.rows, self.cols, len(layers_pathlist)

        if path_output is None:
            dtype = gdalnumeric.LoadFile(layers_pathlist[0], 0, 0, 1, 1).dtype
            stacked = np.empty((self.rows, self.cols, len(layers_pathlist)), dtype)

            for i, p in enumerate(layers_pathlist):
                self.logger.info('Adding band %s to Layerstack..' % os.path.basename(p))
                if self.subset is None or self.subset[0] == 'cube':
                    stacked[:, :, i] = gdalnumeric.LoadFile(p)
                else:
                    stacked[:, :, i] = gdalnumeric.LoadFile(p, self.colStart, self.rowStart, cols, rows)

            return stacked

        elif path_output == 'MEMORY':  # CFG.inmem_serialization is True
            stack_in_mem = gdal.GetDriverByName("MEM").Create("stack.mem", cols, rows, bands)

            for idx, layer in enumerate(layers_pathlist):
                current_band = gdal.Open(layer, GA_ReadOnly)
                stack_in_mem.AddBand()  # data type is dynamically assigned
                band_in_stack = stack_in_mem.GetRasterBand(idx + 1)

                if [self.rows, self.cols] == [current_band.RasterYSize, current_band.RasterXSize]:
                    self.logger.info('Adding band %s to Layerstack..' % os.path.basename(layer))

                    if self.subset is None or self.subset[0] == 'cube':
                        band_in_stack.WriteArray(current_band.GetRasterBand(1).ReadAsArray(), 0, 0)
                    else:
                        band_in_stack.WriteArray(current_band.GetRasterBand(1)
                                                 .ReadAsArray(self.colStart, self.rowStart, self.cols, self.rows), 0, 0)
                else:
                    self.logger.info(
                        'Band %s skipped due to incompatible geometrical resolution.' % os.path.basename(layer))
                del current_band, band_in_stack

            self.bands = bands
            self.inDs = stack_in_mem

        else:  # CFG.inmem_serialization is False
            from ..misc.helper_functions import subcall_with_output

            self.logger.info('Adding the following bands to Layerstack:')
            [self.logger.info(os.path.basename(i)) for i in layers_pathlist]

            if not os.path.isdir(os.path.dirname(path_output)):
                os.makedirs(os.path.dirname(path_output))
            if os.path.exists(path_output):
                os.remove(path_output)
            if os.path.exists(os.path.splitext(path_output)[0] + '.hdr'):
                os.remove(os.path.splitext(path_output)[0] + '.hdr')

            str_layers_pathlist = ' '.join(layers_pathlist)

            if self.subset is None:
                cmd = "gdal_merge.py -q -o %s -of ENVI -seperate %s" % (path_output, str_layers_pathlist)
                output, exitcode, err = subcall_with_output(cmd)
                if exitcode:
                    raise RuntimeError(err)
                if output:
                    return output.decode('UTF-8')
                # FIXME this changes the format of the projection (maybe a GDAL bug?)
                # FIXME normalize by EPSG2WKT(WKT2EPSG(WKT))
            else:
                # convert Pixel Coords to Geo Coords
                orig_ds = gdal.Open(layers_pathlist[0], GA_ReadOnly)
                GT, PR = orig_ds.GetGeoTransform(), orig_ds.GetProjection()
                UL_Xgeo = GT[0] + self.colStart * GT[1] + self.rowStart * GT[2]
                UL_Ygeo = GT[3] + self.colStart * GT[4] + self.rowStart * GT[5]
                LR_Xgeo = GT[0] + self.colEnd * GT[1] + self.rowEnd * GT[2]
                LR_Ygeo = GT[3] + self.colEnd * GT[4] + self.rowEnd * GT[5]
                ullr = '%s %s %s %s' % (UL_Xgeo, UL_Ygeo, LR_Xgeo, LR_Ygeo)

                cmd = "gdal_merge.py -q -o %s -ul_lr %s -of ENVI -seperate %s" \
                      % (path_output, ullr, str_layers_pathlist)
                output, exitcode, err = subcall_with_output(cmd)
                if exitcode:
                    raise RuntimeError(err)
                if output:
                    return output.decode('UTF-8')

                if [GT, PR] == [(0.0, 1.0, 0.0, 0.0, 0.0, 1.0), '']:
                    # delete output map info in case of arbitrary coordinate system
                    with open(os.path.splitext(path_output)[0] + '.hdr', 'r') as inF:
                        lines = inF.readlines()

                    outContent = ''.join([i for i in lines if not re.search(r'map info', i, re.I)])
                    with open(os.path.splitext(path_output)[0] + '.hdr', 'w') as outF:
                        outF.write(outContent)

            assert os.path.exists(path_output) and os.path.exists(os.path.splitext(path_output)[0] + '.hdr'), \
                "Layerstacking failed because output cannot be found."

            # validate the written format of the projection and change it if needed
            # NOT NEEDED ANYMORE (GeoArray always validates projection when reading from disk)
            # prj_written = GeoArray(path_output).prj
            # if self.projection != prj_written and WKT2EPSG(prj_written) == WKT2EPSG(self.projection):
            #
            #     with open(os.path.splitext(path_output)[0] + '.hdr', 'r') as inF:
            #         lines      = inF.readlines()
            #         outContent = ''.join([line if not re.search(r'coordinate system string', line, re.I) else
            #                               'coordinate system string = %s' % self.projection for line in lines])
            #
            #     with open(os.path.splitext(path_output)[0] + '.hdr', 'w') as outF:
            #         outF.write(outContent)
            #
            #     self.inDs = gdal.Open(path_output)

            count_outBands = GeoArray(path_output).bands
            assert count_outBands == len(layers_pathlist), "Layerstacking failed because its output has only %s " \
                                                           "instead of %s bands." % (
                                                               count_outBands, len(layers_pathlist))

        self.update_dataset_related_attributes()

        # writing via envi memmap (tiling-fähig)
        # FileObj = envi.create_image(os.path.splitext(path_output)[0]+'.hdr',shape=(self.rows,self.cols,
        # len(layers_pathlist)),dtype='int16',interleave='bsq',ext='.bsq', force=True) # 8bit for muliple masks
        # in one file
        # File_memmap = FileObj.open_memmap(writable=True)
        # File_memmap[:,:,idx] = current_band.GetRasterBand(1).ReadAsArray()


"""********Help_functions**************************************************"""


def ndarray2gdal(ndarray, outPath=None, importFile=None, direction=1, GDAL_Type="ENVI", geotransform=None,
                 projection=None, v=0):
    """Converts a numpy array to a Georasterdataset (default envi bsq).

    bis jetzt nur georeferenzierung und projectionszuweisung durch import aus anderem file möglich

    :param ndarray:         [bands, rows, cols]
    :param outPath:         Path were to store the outputFile
    :param importFile:      path of a file, where to import the projection and mapinfos
    :param direction:
    :param GDAL_Type:
    :param geotransform:    gdal list for geotransformation [originX, pixelWidth, rot1, originY, pixelHeight, rot2]
    :param projection:      a gdal compatible projection string
                            -> if importFile is not availabele geotransform and projection need to be set,
                            otherwise a gdaldata set without coordinate system will be created
    :param v:
    :return:                GDAL data File
    """

    if v:
        print("\n--------GEOPROCESSING--------\n##Function##"
              "\n**ndarray2gdal**")
    assert outPath is not None, "\n   >>> ERROR: Name of outputfile required"
    if importFile is not None:
        assert os.path.isfile(importFile), \
            "\n   >>> ERROR: File for importing mapprojections does not exists: -> GEOPROCESSING.ndarray2gdal"
    if GDAL_Type != 'MEM':
        if not os.path.isdir(os.path.dirname(outPath)):
            os.makedirs(os.path.dirname(outPath))
        if os.path.exists(outPath):
            os.remove(outPath)

    # main
    if len(ndarray.shape) == 2:  # convert 2 dimensional array to 3 dimensional array
        ndarray = np.reshape(ndarray, (1, ndarray.shape[0], ndarray.shape[1]))

    if direction == 1:  # [bands, rows, cols]
        pass
    if direction == 2:  # [rows, bands, cols]
        ndarray = np.swapaxes(ndarray, 0, 1)
    if direction == 3:  # [rows, cols, bands]
        ndarray = np.rollaxis(ndarray, 2)

    bands, rows, cols = ndarray.shape

    # get gdal dataType depending on numpy datatype
    gdal_dtype_name = convertGdalNumpyDataType(ndarray.dtype.type)
    gdal_dtype = gdal.GetDataTypeByName(gdal_dtype_name)

    if v:
        print("\n\tnew dataset:\n\t  name: %s\n\t  bands: %s\n\t  rows %s\n\t  cols: %s\n\t  GDALtype: %s" % (
            os.path.split(outPath)[1], str(bands), str(rows), str(cols), gdal_dtype_name))
    # register outputdriver
    driver = gdal.GetDriverByName(GDAL_Type)
    driver.Register()
    # Create new gdalfile:  Create(<filename>, <xsize>, <ysize>, [<bands>], [<GDALDataType>]) bands is optional and
    # defaults to 1 GDALDataType is optional and defaults to GDT_Byte
    outDs = driver.Create(outPath, cols, rows, bands, gdal_dtype)
    assert outDs is not None, 'Could not create OutputData'

    for i in range(bands):
        # write outputband
        outBand = outDs.GetRasterBand(i + 1)
        outBand.WriteArray(ndarray[i, :, :], 0, 0)

        # flush data to disk, set the NoData value and calculate stats
        outBand.FlushCache()
        del outBand

    # import georeference and projection from other dataset
    if importFile is not None:
        gdal.AllRegister()
        inDs = gdal.Open(importFile, GA_ReadOnly)
        outDs.SetGeoTransform(inDs.GetGeoTransform())
        outDs.SetProjection(inDs.GetProjection())
    elif geotransform is not None and projection is not None:
        outDs.SetGeoTransform(geotransform)
        outDs.SetProjection(projection)
    if GDAL_Type == 'MEM':  # FIXME geändert von GDAL_Type != 'MEM' (sinnlos!) -> checken, ob L1AP noch läuft
        del outDs
    else:
        return outDs


def convertGdalNumpyDataType(dType):
    """convertGdalNumpyDataType
    input:
        dType: GDALdataType string or numpy dataType
    output:
        corresponding dataType
    """
    # dictionary to translate GDAL data types (strings) in corresponding numpy data types
    dTypeDic = {"Byte": np.uint8, "UInt16": np.uint16, "Int16": np.int16, "UInt32": np.uint32, "Int32": np.int32,
                "Float32": np.float32, "Float64": np.float64, "GDT_UInt32": np.uint32}
    outdType = None

    if dType in dTypeDic:
        outdType = dTypeDic[dType]
    elif dType in dTypeDic.values():
        for i in dTypeDic.items():
            if dType == i[1]:
                outdType = i[0]
    elif dType in [np.int8, np.int64, np.int]:
        outdType = "Int32"
        print(">>>  Warning: %s is converted to GDAL_Type 'Int_32'\n" % dType)
    elif dType in [np.bool, np.bool_]:
        outdType = "Byte"
        print(">>>  Warning: %s is converted to GDAL_Type 'Byte'\n" % dType)
    elif dType in [np.float]:
        outdType = "Float32"
        print(">>>  Warning: %s is converted to GDAL_Type 'Float32'\n" % dType)
    elif dType in [np.float16]:
        outdType = "Float32"
        print(">>>  Warning: %s is converted to GDAL_Type 'Float32'\n" % dType)
    else:
        raise Exception('GEOP.convertGdalNumpyDataType: Unexpected input data type %s.' % dType)
    return outdType


def get_point_bounds(points):
    mp_points = MultiPoint(points)
    (min_lon, min_lat, max_lon, max_lat) = mp_points.bounds
    return min_lon, min_lat, max_lon, max_lat


def get_common_extent(list_extentcoords, alg='outer', return_box=True):
    """Returns the common extent coordinates of all given coordinate extents.
    NOTE: this function asserts that all input coordinates belong to the same projection!

    :param list_extentcoords:   a list of coordinate sets, e.g. [ [ULxy1,URxy1,LRxy1,LLxy1], ULxy2,URxy2,LRxy2,LLxy2],]
    :param alg:                 'outer': return the outer Polygon extent
                                'inner': return the inner Polygon extent
    :param return_box:          whether to return a coordinate box/envelope of the output Polygon
    :return:    [ULxy,URxy,LRxy,LLxy]
    """
    if alg != 'outer':
        raise NotImplementedError  # TODO apply shapely intersection

    allPolys = [Polygon(extentcoords).envelope for extentcoords in list_extentcoords]
    common_extent = cascaded_union(allPolys)

    def get_coordsXY(shpPoly): return np.swapaxes(np.array(shpPoly.exterior.coords.xy), 0, 1).tolist()

    return get_coordsXY(common_extent) if not return_box else get_coordsXY(common_extent.envelope)


def zoom_2Darray_to_shapeFullArr(arr2D, shapeFullArr, meshwidth=1, subset=None, method='linear'):
    from scipy.interpolate import RegularGridInterpolator

    assert method in ['linear', 'nearest']
    rS, rE, cS, cE = list(get_subsetProps_from_subsetArg(shapeFullArr, subset).values())[3:7]
    rowpos = np.linspace(0, shapeFullArr[0] - 1, arr2D.shape[0])
    colpos = np.linspace(0, shapeFullArr[1] - 1, arr2D.shape[1])

    rgi = RegularGridInterpolator([rowpos, colpos], arr2D, method=method)
    out_rows_grid, out_cols_grid = np.meshgrid(range(rS, rE, meshwidth), range(cS, cE, meshwidth), indexing='ij')
    return rgi(np.dstack([out_rows_grid, out_cols_grid]))


def adjust_acquisArrProv_to_shapeFullArr(arrProv, shapeFullArr, meshwidth=1, subset=None, bandwise=False):
    assert isinstance(arrProv, dict) and isinstance(arrProv[list(arrProv.keys())[0]], list), \
        'Expected a dictionary with band names (from LayerbandsAssignment) as keys and lists as ' \
        'values. Got %s.' % type(arrProv)

    arrProv = {k: np.array(v) for k, v in arrProv.items()}
    shapes = [v.shape for v in arrProv.values()]

    assert len(
        list(set(shapes))) == 1, 'The arrays contained in the values of arrProv have different shapes. Got %s.' % shapes

    if bandwise:
        outDict = {k: zoom_2Darray_to_shapeFullArr(arr, shapeFullArr, meshwidth, subset) for k, arr in arrProv.items()}
        return outDict
    else:
        arr2interp = np.mean(np.dstack(list(arrProv.values())), axis=2)
        interpolated = zoom_2Darray_to_shapeFullArr(arr2interp, shapeFullArr, meshwidth, subset).astype(np.float32)
        return interpolated


def DN2Rad(ndarray, offsets, gains, inFill=None, inZero=None, inSaturated=None, cutNeg=True):
    # type: (np.ndarray,list,list,int,int,int,bool) -> np.ndarray
    """Convert DN to Radiance [W * m-2 * sr-1 * micrometer-1].

    NOTE: InputGains and Offsets should be in [W * m-2 * sr-1 * micrometer-1]!!!

    :param ndarray:     <np.ndarray> array of DNs to be converted into radiance
    :param offsets:     [W * m-2 * sr-1 * micrometer-1]:
                        list that includes the offsets of the individual rasterbands [offset_band1, offset_band2,
                        ... ,offset_bandn] or optional input as number if Dataset has only 1 Band
    :param gains:       [W * m-2 * sr-1 * micrometer-1]:
                        list that includes the gains of the individual rasterbands [gain_band1, gain_band2, ... ,
                        gain_bandn] or optional input as number if Dataset has only 1 Band
    :param inFill:      pixelvalues allocated to background/dummy/fill pixels
    :param inZero:      pixelvalues allocated to zero radiance
    :param inSaturated: pixelvalues allocated to saturated pixels
    :param cutNeg:      cutNegvalues -> all negative values set to 0
    """
    assert isinstance(offsets, list) and isinstance(gains, list), \
        "Offset and Gain parameters have to be provided as two lists containing gains and offsets for \
        each band in ascending order. Got offsets as type '%s' and gains as type '%s'." % (type(offsets), type(gains))

    bands = 1 if ndarray.ndim == 2 else ndarray.shape[2]
    for arg, argname in zip([offsets, gains], ['offsets', 'gains']):
        assert len(arg) == bands, """Argument '%s' does not match the number of bands.
            Expected a list of %s %s values for each band in ascending order. Got %s.""" \
                                  % (argname, bands, argname, len(arg))
        for i in arg:
            assert isinstance(i, float) or isinstance(i, int), \
                "DN2Rad: Expected float or integer values from argument '%s'. Got %s" % (argname, type(i))

    if [inFill, inZero, inSaturated] == [None, None, None]:
        inFill, inZero, inSaturated = get_outFillZeroSaturated(ndarray.dtype)
    # --Define default for Special Values of reflectanceband
    outFill, outZero, outSaturated = get_outFillZeroSaturated('int16')

    off, gai = [np.array(param).reshape(1, 1, bands) for param in [offsets, gains]]
    rad = (10 * (off + ndarray * gai)).astype(np.int16)
    rad = np.where(rad < 0, 0, rad) if cutNeg else rad
    rad = np.where(ndarray == inFill, outFill, rad) if inFill is not None else rad
    rad = np.where(ndarray == inSaturated, outSaturated, rad) if inSaturated is not None else rad
    rad = np.where(ndarray == inZero, outZero, rad) if inZero is not None else rad
    # rad = np.piecewise(rad,[ndarray==inFill,ndarray==inSaturated,ndarray==inZero],[outFill,outSaturated,outZero])

    return rad


def DN2TOARef(ndarray, offsets, gains, irradiances, zenith, earthSunDist,
              inFill=None, inZero=None, inSaturated=None, cutNeg=True):
    # type: (np.ndarray,list,list,list,float,float,int,int,int,bool) -> np.ndarray
    """Converts DN data to TOA Reflectance.

    :param ndarray:         <np.ndarray> array of DNs to be converted into TOA reflectance
    :param offsets:         list: of offsets of each rasterband [W * m-2 * sr-1 * micrometer-1]
                            [offset_band1, offset_band2, ... ,offset_bandn] or optional as number if Dataset has
                            only 1 Band
    :param gains:           list: of gains of each rasterband [W * m-2 * sr-1 * micrometer-1]
                            [gain_band1, gain_band2, ... ,gain_bandn] or optional as number if Dataset has
                            only 1 Band
    :param irradiances:     list: of irradiance of each band [W * m-2 * micrometer-1]
                            [irradiance_band1, irradiance_band2, ... ,irradiance_bandn]
    :param zenith:          number: sun zenith angle
    :param earthSunDist:    earth-sun- distance for a certain day
    :param inFill:          number: pixelvalues allocated to background/dummy/fill pixels
    :param inZero:          number: pixelvalues allocated to zero radiance
    :param inSaturated:     number: pixelvalues allocated to saturated pixles
    :param cutNeg:          bool:   if true. all negative values turned to zero. default: True
    :return:                Int16 TOA_Reflectance in [0-10000]
    """
    assert isinstance(offsets, list) and isinstance(gains, list) and isinstance(irradiances, list), \
        "Offset, Gain, Irradiance parameters have to be provided as three lists containing gains, offsets and " \
        "irradiance for each band in ascending order. Got offsets as type '%s', gains as type '%s' and irradiance as " \
        "type '%s'." % (type(offsets), type(gains), type(irradiances))

    bands = 1 if len(ndarray.shape) == 2 else ndarray.shape[2]
    for arg, argname in zip([offsets, gains, irradiances], ['offsets', 'gains', 'irradiance']):
        assert len(arg) == bands, "Argument '%s' does not match the number of bands. Expected a list of %s %s values " \
                                  "for each band in ascending order. Got %s." % (argname, bands, argname, len(arg))
        for i in arg:
            assert isinstance(i, float) or isinstance(i, int), \
                "DN2TOARef: Expected float or integer values from argument '%s'. Got %s" % (argname, type(i))

    if [inFill, inZero, inSaturated] == [None, None, None]:
        inFill, inZero, inSaturated = get_outFillZeroSaturated(ndarray.dtype)
    # --Define default for Special Values of reflectanceband
    outFill, outZero, outSaturated = get_outFillZeroSaturated('int16')

    constant = 10000 * math.pi * earthSunDist ** 2 / math.cos(math.radians(zenith))
    off, gai, irr = [np.array(param).reshape(1, 1, bands) for param in [offsets, gains, irradiances]]
    TOA_ref = (constant * (off + ndarray * gai) / irr).astype(np.int16)
    TOA_ref = np.where(TOA_ref < 0, 0, TOA_ref) if cutNeg else TOA_ref
    TOA_ref = np.where(ndarray == inFill, outFill, TOA_ref) if inFill is not None else TOA_ref
    TOA_ref = np.where(ndarray == inSaturated, outSaturated, TOA_ref) if inSaturated is not None else TOA_ref
    TOA_ref = np.where(ndarray == inZero, outZero, TOA_ref) if inZero is not None else TOA_ref
    # TOA_ref = \
    #     np.piecewise(TOA_ref,[ndarray==inFill,ndarray==inSaturated,ndarray==inZero],[outFill,outSaturated,outZero])

    return TOA_ref


def TOARad2Kelvin_fastforward(ndarray, K1, K2, emissivity=0.95, inFill=None, inZero=None, inSaturated=None):
    # type: (np.ndarray,list,list,float,int,int,int) -> np.ndarray
    """Convert top-of-atmosphere radiances of thermal bands to temperatures in Kelvin
    by applying the inverse of the Planck function.

    :param ndarray:         <np.ndarray> array of TOA radiance values to be converted into Kelvin
    :param K1:
    :param K2:
    :param emissivity:
    :param inFill:
    :param inZero:
    :param inSaturated:
    """
    bands = 1 if len(ndarray.shape) == 2 else ndarray.shape[2]
    for arg, argname in zip([K1, K2], ['K1', 'K2']):
        assert isinstance(arg[0], float) or isinstance(arg[0], int), "TOARad2Kelvin_fastforward: Expected float or " \
                                                                     "integer values from argument '%s'. Got type %s" \
                                                                     % (argname, type(arg))
        assert len(arg) == bands, """Argument '%s' does not match the number of bands. Expected a list of %s %s values
            for each band in ascending order. Got %s.""" % (argname, bands, argname, len(arg))
        for i in arg:
            assert isinstance(i, float) or isinstance(i, int), "TOARad2Kelvin_fastforward: Expected float or \
                integer values from argument '%s'. Got %s." % (argname, type(i))
    assert type(emissivity) in [float, int], "TOARad2Kelvin_fastforward: Expected float or integer \
        values from argument emissivity. Got %s" % type(emissivity)

    if [inFill, inZero, inSaturated] == [None, None, None]:
        inFill, inZero, inSaturated = get_outFillZeroSaturated(ndarray.dtype)
    # --Define default for Special Values of reflectanceband
    outFill, outZero, outSaturated = get_outFillZeroSaturated('int16')

    K1, K2 = [np.array(param).reshape(1, 1, bands) for param in [K1, K2]]
    Kelvin = (K2 / np.log(K1 / ndarray + 1)).astype(np.int16)
    Kelvin = np.where(ndarray == inFill, outFill, Kelvin) if inFill is not None else Kelvin
    Kelvin = np.where(ndarray == inSaturated, outSaturated, Kelvin) if inSaturated is not None else Kelvin
    Kelvin = np.where(ndarray == inZero, outZero, Kelvin) if inZero is not None else Kelvin
    # Kelvin = \
    #     np.piecewise(Kelvin,[ndarray==inFill,ndarray==inSaturated,ndarray==inZero],[outFill,outSaturated,outZero])

    return Kelvin


def DN2DegreesCelsius_fastforward(ndarray, offsets, gains, K1, K2, emissivity=0.95,
                                  inFill=None, inZero=None, inSaturated=None):
    """Convert thermal DNs to temperatures in degrees Celsius
    by calculating TOARadiance and applying the inverse of the Planck function.

    :param ndarray:     <np.ndarray> array of DNs to be converted into Degrees Celsius
    :param offsets:
    :param gains:
    :param K1:
    :param K2:
    :param emissivity:
    :param inFill:
    :param inZero:
    :param inSaturated:
    """
    bands = 1 if len(ndarray.shape) == 2 else ndarray.shape[2]
    for arg, argname in zip([offsets, gains, K1, K2], ['Offset', 'Gain', 'K1', 'K2']):
        assert isinstance(offsets, list) and isinstance(gains, list), \
            "%s parameters have to be provided as a list containing individual values for each band in \
            ascending order. Got type '%s'." % (argname, type(arg))
        assert len(arg) == bands, """Argument '%s' does not match the number of bands. Expected a list of %s %s values
            for each band in ascending order. Got %s.""" % (argname, bands, argname, len(arg))
        for i in arg:
            assert isinstance(i, float) or isinstance(i, int), "DN2DegreesCelsius_fastforward: Expected float or \
                integer values from argument '%s'. Got %s." % (argname, type(i))
    assert type(emissivity) in [float, int], "DN2DegreesCelsius_fastforward: Expected float or integer \
        values from argument emissivity. Got %s" % type(emissivity)

    if [inFill, inZero, inSaturated] == [None, None, None]:
        inFill, inZero, inSaturated = get_outFillZeroSaturated(ndarray.dtype)
    # --Define default for Special Values of reflectanceband
    outFill, outZero, outSaturated = get_outFillZeroSaturated('int16')

    off, gai, K1, K2 = [np.array(param).reshape(1, 1, bands) for param in [offsets, gains, K1, K2]]
    degCel = (100 * ((K2 / np.log(K1 * emissivity / (off + ndarray * gai) + 1)) - 273.15)).astype(np.int16)
    degCel = np.where(ndarray == inFill, outFill, degCel) if inFill is not None else degCel
    degCel = np.where(ndarray == inSaturated, outSaturated, degCel) if inSaturated is not None else degCel
    degCel = np.where(ndarray == inZero, outZero, degCel) if inZero is not None else degCel
    # degCel = \
    #     np.piecewise(degCel,[ndarray==inFill,ndarray==inSaturated,ndarray==inZero],[outFill,outSaturated,outZero])
    return degCel


def is_granule(trueCornerPos):  # TODO
    """Idee: testen, ob es sich um Granule handelt oder um die volle Szene -
    dazu Winkel der Kanten zu Nord oder Ost berechnen"""

    pass


# def get_corner_coordinates(gt, prj, rows, cols, targetProj=None):
#    """Returns corner coordinates of the entire GEOP object in lon/lat or UTM.
#       ATTENTION: coordinates represent PIXEL CORNERS:
#            UL=UL-coordinate of (0,0)
#            UR=UR-coordinate of (0,self.cols-1)
#            => lonlat_arr always contains UL-coordinate of each pixel
#    :param targetProj: 'LonLat' or 'UTM' """#
#
#    assert targetProj in [None,'LonLat','UTM'], "Target projection %s currently not supported." %targetProj
#    ULxy,URxy,LLxy,LRxy = [(0,0),(cols,0),(0,rows),(cols,rows)]
#    LonLat    = [tuple(reversed(pixelToLatLon(XY,geotransform=gt,projection=prj))) for XY in [ULxy,URxy,LLxy,LRxy]]
#    return LonLat if targetProj in [None,'LonLat'] else \
#        [transform_wgs84_to_utm(LL[0],LL[1],get_UTMzone(prj=prj)) for LL in LonLat]


def get_lonlat_coord_array(shape_fullArr, arr_pos, geotransform, projection, meshwidth=1, nodata_mask=None,
                           outFill=None):
    """Returns numpy array containing longitude pixel coordinates (band 0) and latitude pixel coordinates (band 1).

    :param shape_fullArr:
    :param arr_pos:
    :param geotransform:
    :param projection:
    :param meshwidth:       <int> defines the density of the mesh used for generating the output
                            (1: full resolution; 10: one point each 10 pixels)
    :param nodata_mask:     <numpy array>, used for declaring nodata values in the output lonlat array
    :param outFill:         the value that is assigned to nodata area in the output lonlat array
    """
    rows, cols, bands, rowStart, rowEnd, colStart, colEnd = get_subsetProps_from_shapeFullArr_arrPos(shape_fullArr,
                                                                                                     arr_pos)

    xcoord_arr, ycoord_arr = np.meshgrid(range(colStart, colStart + cols, meshwidth),
                                         range(rowStart, rowStart + rows, meshwidth))
    xcoord_arr = xcoord_arr * geotransform[1] + geotransform[0]
    ycoord_arr = ycoord_arr * geotransform[5] + geotransform[3]

    assert projection, 'Unable to calculate LonLat array. Invalid projection. Got %s.' % projection
    src_srs = osr.SpatialReference()
    src_srs.ImportFromWkt(projection)
    assert src_srs.IsProjected() or src_srs.IsGeographic(), \
        'Unable to calculate LonLat array. Unsupported projection (got %s)' % projection

    if src_srs.IsProjected():
        proj = pyproj.Proj(src_srs.ExportToProj4())
        xcoord_arr, ycoord_arr = proj(xcoord_arr, ycoord_arr, inverse=True)

    xcoord_ycoord_arr = np.dstack((xcoord_arr, ycoord_arr))

    if nodata_mask is not None:
        outFill = outFill if outFill else get_outFillZeroSaturated('float32')[0]
        xcoord_ycoord_arr[nodata_mask.astype(np.int8) == 0] = outFill

    UL_lonlat = (round(xcoord_ycoord_arr[0, 0, 0], 10), round(xcoord_ycoord_arr[0, 0, 1], 10))
    UR_lonlat = (round(xcoord_ycoord_arr[0, -1, 0], 10), round(xcoord_ycoord_arr[0, -1, 1], 10))
    # TODO validate that coordinate:
    LL_lonlat = (round(xcoord_ycoord_arr[-1, 0, 0], 10), round(xcoord_ycoord_arr[-1, 0, 1], 10))
    # TODO validate that coordinate:
    LR_lonlat = (round(xcoord_ycoord_arr[-1, -1, 0], 10), round(xcoord_ycoord_arr[-1, -1, 1], 10))
    # self.logger.info(self.filename)
    # self.logger.info('UL', UL_lat)
    # self.logger.info('UR', UR_lat)
    # self.logger.info('LL', LL_lat)
    # self.logger.info('LR', LR_lat)
    # self.logger.info('1000/1000', round(xcoord_ycoord_arr[999,999,0],10),round(xcoord_ycoord_arr[999,999,1],10))
    return xcoord_ycoord_arr.astype(np.float32), [UL_lonlat, UR_lonlat, LL_lonlat, LR_lonlat]


def calc_VAA_using_fullSceneCornerLonLat(fullSceneCornerLonLat, orbit_params):
    # type: (list, list) -> float
    """Calculates the Viewing azimuth angle (defined as 90 degrees from the flight line),
    e.g. if flight line is 8 degrees from North -> VAA will be 98 degrees.

    :param fullSceneCornerLonLat:   UL, UR, LL, LR
    :param orbit_params:    list of [altitude, inclination, period] => inclination is used as fallback
    """
    assert len(fullSceneCornerLonLat) == 4, \
        'VAA can only be calculated with fullSceneCornerLonLat representing 4 coordinates (UL, UR, LL, LR).'

    UL_LonLat, UR_LonLat, LL_LonLat, LR_LonLat = fullSceneCornerLonLat
    forward_az_left = pyproj.Geod(ellps='WGS84').inv(*LL_LonLat, *UL_LonLat)[0]
    forward_az_right = pyproj.Geod(ellps='WGS84').inv(*LR_LonLat, *UR_LonLat)[0]
    VAA_mean = float(np.mean([forward_az_left, forward_az_right])) + 90

    # validation:
    if abs(VAA_mean - 90) < 1:
        # fullSceneCornerLonLat obviously don't belong to a full scene but a granule
        assert orbit_params
        warnings.warn('Derivation of mean VAA angle from flight line delivered a non reasonable value (%s degrees).'
                      'Using sensor inclination (%s degrees) as fallback.' % (VAA_mean, orbit_params[1]))
        VAA_mean = float(orbit_params[1])  # inclination # FIXME is this correct?

    return VAA_mean


def calc_VZA_array(shape_fullArr, arr_pos, fullSceneCornerPos, viewing_angle, FOV, logger, meshwidth=1,
                   nodata_mask=None, outFill=None):
    """Calculate viewing zenith angles for each pixel in the dataset.

    By solving an equation system with 4 variables for each image corner: VZA = a + b*col + c*row + d*col*row.

    :param shape_fullArr:
    :param arr_pos:
    :param fullSceneCornerPos:
    :param viewing_angle:
    :param FOV:
    :param logger:
    :param meshwidth:       <int> defines the density of the mesh used for generating the output
                            (1: full resolution; 10: one point each 10 pixels)
    :param nodata_mask:     <numpy array>, used for declaring nodata values in the output VZA array
    :param outFill:         the value that is assigned to nodata area in the output VZA array
    """
    # FIXME in case of Sentinel-2 the viewing_angle corresponds to the center point of the image footprint
    # FIXME (trueDataCornerPos)
    # FIXME => the algorithm must use the center viewing angle + orbit inclination and must calculate the FOV to be used
    # FIXME     via the widths of the footprint at the center position
    # FIXME since S2 brings its own VZA array this is only relevant other scenes provided as granules (e.g. RapidEye)

    if nodata_mask is not None:
        assert isinstance(nodata_mask, (GeoArray, np.ndarray)), \
            "'nodata_mask' must be a numpy array or an instance of GeoArray. Got %s" % type(nodata_mask)
    colsFullArr, rowsFullArr, bandsFullArr = shape_fullArr
    rows, cols, bands, rowStart, rowEnd, colStart, colEnd = get_subsetProps_from_shapeFullArr_arrPos(shape_fullArr,
                                                                                                     arr_pos)
    ul, ur, ll, lr = fullSceneCornerPos

    cols_arr, rows_arr = np.meshgrid(range(colStart, colStart + cols, meshwidth),
                                     range(rowStart, rowStart + rows, meshwidth))

    if list(fullSceneCornerPos) == list(
       ([0, 0], [0, colsFullArr - 1], [rowsFullArr - 1, 0], [rowsFullArr - 1, colsFullArr - 1])):
        logger.warning('No precise calculation of VZA array possible because orbit track cannot be '
                       'reconstructed from dataset since full scene corner positions are unknown. VZA array is '
                       'filled with the value provided in metadata.')
        VZA_array = np.full(cols_arr.shape, viewing_angle, np.int64)  # respects meshwidth
    else:
        coeff_matrix = np.array([[1, ul[1], ul[0], ul[1] * ul[0]],
                                 [1, ur[1], ur[0], ur[1] * ur[0]],
                                 [1, ll[1], ll[0], ll[1] * ll[0]],
                                 [1, lr[1], lr[0], lr[1] * lr[0]]])
        const_matrix = np.array(
            [viewing_angle + FOV / 2.,  # VZA@UL # +- aligning seems to match with Sentinel-2 # TODO correct?
             viewing_angle - FOV / 2.,  # VZA@UR
             viewing_angle + FOV / 2.,  # VZA@LL
             viewing_angle - FOV / 2.])  # VZA@LR
        factors = np.linalg.solve(coeff_matrix, const_matrix)

        VZA_array = (factors[0] + factors[1] * cols_arr + factors[2] * rows_arr + factors[3] *
                     cols_arr * rows_arr).astype(np.float32)

    if nodata_mask is not None:
        outFill = outFill if outFill else get_outFillZeroSaturated('float32')[0]
        VZA_array[nodata_mask.astype(np.int8) == 0] = outFill

    return VZA_array


def calc_AcqTime_array(shape_fullArr, arr_pos, AcqDate, CenterAcqTime, fullSceneCornerPos, overpassDurationSec,
                       meshwidth=1):
    ul, ur, ll, lr = fullSceneCornerPos

    rows, cols, bands, rowStart, rowEnd, colStart, colEnd = get_subsetProps_from_shapeFullArr_arrPos(shape_fullArr,
                                                                                                     arr_pos)

    cols_arr, rows_arr = np.meshgrid(range(colStart, colStart + cols, meshwidth),
                                     range(rowStart, rowStart + rows, meshwidth))

    time_center = datetime.datetime.strptime('%s %s' % (AcqDate, CenterAcqTime), '%Y-%m-%d %H:%M:%S')
    time_start = time_center - datetime.timedelta(seconds=overpassDurationSec)
    time_end = time_center + datetime.timedelta(seconds=overpassDurationSec)

    coeff_matrix = np.array([[1, ul[1], ul[0], ul[1] * ul[0]],
                             [1, ur[1], ur[0], ur[1] * ur[0]],
                             [1, ll[1], ll[0], ll[1] * ll[0]],
                             [1, lr[1], lr[0], lr[1] * lr[0]]])
    const_matrix = np.array([mdates.date2num(time_end),  # AcqTime@UL
                             mdates.date2num(time_end),  # AcqTime@UR
                             mdates.date2num(time_start),  # AcqTime@LL
                             mdates.date2num(time_start)])  # AcqTime@LR

    factors = np.linalg.solve(coeff_matrix, const_matrix)

    mdate_numarray = factors[0] + factors[1] * cols_arr + factors[2] * rows_arr + factors[3] * cols_arr * rows_arr
    flat_mdate_arr = np.array(mdates.num2date(mdate_numarray.flatten()))
    datetime_arr = np.array([flat_mdate_arr[i].replace(tzinfo=None)
                             for i in range(len(flat_mdate_arr))]).reshape(-1, cols)
    return datetime_arr


def calc_SZA_SAA(date, lon, lat):  # not used anymore since pyorbital is more precise
    """Calculates solar zenith and azimuth angle using pyephem.

    :param date:
    :param lon:
    :param lat:
    """
    obsv = ephem.Observer()
    obsv.lon, obsv.lat = str(lon), str(lat)
    obsv.date = date
    sun = ephem.Sun()
    sun.compute(obsv)
    alt, az = [("%s" % i).split(':') for i in [sun.alt, sun.az]]
    SZA = np.float32(90 - float(alt[0]) + float(alt[1]) / 60. + float(alt[2]) / 3600.)
    SAA = np.float32(float(az[0]) + float(az[1]) / 60. + float(az[2]) / 3600.)
    return SZA, SAA


def calc_SZA_SAA_array(shape_fullArr, arr_pos, AcqDate, CenterAcqTime, fullSceneCornerPos, fullSceneCornerLonLat,
                       overpassDurationSec, logger, meshwidth=1, nodata_mask=None, outFill=None, accurracy='coarse',
                       lonlat_arr=None):
    """Calculates solar zenith and azimuth angles for each pixel in the dataset using pyorbital.

    :param shape_fullArr:
    :param arr_pos:
    :param AcqDate:
    :param CenterAcqTime:
    :param fullSceneCornerPos:
    :param fullSceneCornerLonLat:   UL, UR, LL, LR
    :param overpassDurationSec:
    :param logger:
    :param meshwidth:       <int> defines the density of the mesh used for generating the output
                            (1: full resolution; 10: one point each 10 pixels)
    :param nodata_mask:             <numpy array>, used for declaring nodata values in the output SZA/SAA array
    :param outFill:                 the value that is assigned to nodata area in the output SZA/SAA array
    :param accurracy:               'fine' or 'coarse'
                                    - 'fine' : pixelwise acquisition time is used to calculate SZA/SAA
                                        - requires lonlat_arr to be specified
                                    - 'coarse: SZA/SAA is calculated for image corners then interpolated by solving
                                               an equation system with 4 variables for each image corner:
                                               SZA/SAA = a + b*col + c*row + d*col*row.
    :param lonlat_arr:
    """
    if nodata_mask is not None:
        assert isinstance(nodata_mask, (GeoArray, np.ndarray)), \
            "'nodata_mask' must be a numpy array or an instance of GeoArray. Got %s" % type(nodata_mask)
    if accurracy == 'fine':
        assert lonlat_arr is not None, "Calculating SZA/SAA with accurracy set to 'fine' requires lonlat_arr to be " \
                                       "specified. SZA/SAA is calculated with accurracy = 'coarse'."
    assert accurracy in ['fine', 'coarse'], "The keyword accuracy accepts only 'fine' or 'coarse'. Got %s" % accurracy

    ul, ur, ll, lr = fullSceneCornerPos
    colsFullArr, rowsFullArr, bandsFullArr = shape_fullArr

    if list(fullSceneCornerPos) == list(
       ([0, 0], [0, colsFullArr - 1], [rowsFullArr - 1, 0], [rowsFullArr - 1, colsFullArr - 1])):
        logger.warning('No precise calculation of SZA/SAA array possible because orbit track cannot '
                       'be reconstructed from dataset since full scene corner positions are unknown. Same '
                       'acquisition time for each pixel is assumed for SZA/SAA calculation.')
        time_center = datetime.datetime.strptime('%s %s' % (AcqDate, CenterAcqTime), '%Y-%m-%d %H:%M:%S')
        time_start = time_center
        time_end = time_center
    else:
        # overpassDurationSec = self.get_overpass_duration(fullSceneCornerLonLat, orbitParams)[0]
        time_center = datetime.datetime.strptime('%s %s' % (AcqDate, CenterAcqTime), '%Y-%m-%d %H:%M:%S')
        time_start = time_center - datetime.timedelta(seconds=float(overpassDurationSec) / 2)
        time_end = time_center + datetime.timedelta(seconds=float(overpassDurationSec) / 2)

    if accurracy == 'fine':
        datetime_arr = calc_AcqTime_array(shape_fullArr, arr_pos, AcqDate, CenterAcqTime,
                                          fullSceneCornerPos, overpassDurationSec, meshwidth)
        sol_alt_rad, sol_az_rad = astronomy.get_alt_az(datetime_arr, lonlat_arr[:, :, 0], lonlat_arr[:, :, 1])
        SZA_array, SAA_array = 90 - (180 * sol_alt_rad / math.pi), 180 * sol_az_rad / math.pi

    else:  # accurracy == 'coarse'
        rows, cols, bands, rowStart, rowEnd, colStart, colEnd = \
            get_subsetProps_from_shapeFullArr_arrPos(shape_fullArr, arr_pos)

        cols_arr, rows_arr = np.meshgrid(range(colStart, colStart + cols, meshwidth),
                                         range(rowStart, rowStart + rows, meshwidth))

        alt_UL_rad, az_UL_rad = astronomy.get_alt_az(time_end, fullSceneCornerLonLat[0][0], fullSceneCornerLonLat[0][1])
        alt_UR_rad, az_UR_rad = astronomy.get_alt_az(time_end, fullSceneCornerLonLat[1][0], fullSceneCornerLonLat[1][1])
        alt_LL_rad, az_LL_rad = astronomy.get_alt_az(time_start, fullSceneCornerLonLat[2][0],
                                                     fullSceneCornerLonLat[2][1])
        alt_LR_rad, az_LR_rad = astronomy.get_alt_az(time_start, fullSceneCornerLonLat[3][0],
                                                     fullSceneCornerLonLat[3][1])

        SZA_UL, SAA_UL = 90 - (180 * alt_UL_rad / math.pi), 180 * az_UL_rad / math.pi
        SZA_UR, SAA_UR = 90 - (180 * alt_UR_rad / math.pi), 180 * az_UR_rad / math.pi
        SZA_LL, SAA_LL = 90 - (180 * alt_LL_rad / math.pi), 180 * az_LL_rad / math.pi
        SZA_LR, SAA_LR = 90 - (180 * alt_LR_rad / math.pi), 180 * az_LR_rad / math.pi
        SZA_SAA_coeff_matrix = np.array([[1, ul[1], ul[0], ul[1] * ul[0]],
                                         [1, ur[1], ur[0], ur[1] * ur[0]],
                                         [1, ll[1], ll[0], ll[1] * ll[0]],
                                         [1, lr[1], lr[0], lr[1] * lr[0]]])
        SZA_const_matrix = np.array([SZA_UL, SZA_UR, SZA_LL, SZA_LR])
        SZA_factors = np.linalg.solve(SZA_SAA_coeff_matrix, SZA_const_matrix)
        SZA_array = (SZA_factors[0] + SZA_factors[1] * cols_arr + SZA_factors[2] * rows_arr +
                     SZA_factors[3] * cols_arr * rows_arr).astype(np.float32)

        SAA_const_matrix = np.array([SAA_UL, SAA_UR, SAA_LL, SAA_LR])
        SAA_factors = np.linalg.solve(SZA_SAA_coeff_matrix, SAA_const_matrix)
        SAA_array = (SAA_factors[0] + SAA_factors[1] * cols_arr + SAA_factors[2] * rows_arr +
                     SAA_factors[3] * cols_arr * rows_arr).astype(np.float32)

    if nodata_mask is not None:
        SZA_array[nodata_mask.astype(np.int8) == 0] = outFill
        SAA_array[nodata_mask.astype(np.int8) == 0] = outFill
    return SZA_array, SAA_array


def calc_RAA_array(SAA_array, VAA_array, nodata_mask=None, outFill=None):
    """Calculate relative azimuth angle between solar azimuth and viewing azimuth in degrees.

    :param SAA_array:
    :param VAA_array:
    :param nodata_mask:
    :param outFill:     the value to be used to fill areas outside the actual image bounds
    :return:
    """
    if nodata_mask is not None:
        assert isinstance(nodata_mask, (GeoArray, np.ndarray)), \
            "'nodata_mask' must be a numpy array or an instance of GeoArray. Got %s" % type(nodata_mask)

    RAA_array = SAA_array - VAA_array

    if nodata_mask is not None:
        RAA_array[nodata_mask.astype(np.int8) == 0] = outFill
    return RAA_array


def get_subsetProps_from_shapeFullArr_arrPos(shape_fullArr, arr_pos):
    """Returns array dims with respect to possible subsetting."""

    rows, cols, bands = shape_fullArr
    rows, cols = [arr_pos[0][1] - arr_pos[0][0] + 1, arr_pos[1][1] - arr_pos[1][0] + 1] if arr_pos else (rows, cols)
    rowStart, colStart = [arr_pos[0][0], arr_pos[1][0]] if arr_pos else [0, 0]
    rowEnd, colEnd = rowStart + rows, colStart + cols
    return rows, cols, bands, rowStart, rowEnd, colStart, colEnd


def get_subsetProps_from_subsetArg(shape_fullArr, subset):
    if subset:
        assert subset[0] in ['cube', 'row', 'col', 'band', 'block', 'pixel', 'custom'], \
            'Unexpected subset shape %s.' % subset[0]
    else:
        subset = ('cube', None)
    if subset is None or subset[0] == 'cube':
        rows, cols, bands = shape_fullArr
        rowStart, colStart, bandStart = 0, 0, 0
        rowEnd, colEnd, bandEnd = rows - 1, cols - 1, bands - 1
    elif subset[0] == 'row':
        cols, rows, bands = shape_fullArr[1], 1, shape_fullArr[2]
        colStart, rowStart, bandStart = 0, subset[1], 0
        colEnd, rowEnd, bandEnd = cols - 1, subset[1], bands - 1
    elif subset[0] == 'col':
        cols, rows, bands = 1, shape_fullArr[0], shape_fullArr[2]
        colStart, rowStart, bandStart = subset[1], 0, 0
        colEnd, rowEnd, bandEnd = subset[1], rows - 1, bands - 1
    elif subset[0] == 'band':
        cols, rows, bands = shape_fullArr[1], shape_fullArr[0], 1
        colStart, rowStart, bandStart = 0, 0, subset[1]
        colEnd, rowEnd, bandEnd = cols - 1, rows - 1, subset[1]
    elif subset[0] == 'block':
        cols, rows, bands = subset[1][1][1] - subset[1][1][0] + 1, subset[1][0][1] - \
                            subset[1][0][0] + 1, shape_fullArr[2]
        colStart, rowStart, bandStart = subset[1][1][0], subset[1][0][0], 0
        colEnd, rowEnd, bandEnd = subset[1][1][1], subset[1][0][1], bands - 1
    elif subset[0] == 'pixel':
        cols, rows, bands = 1, 1, shape_fullArr[2]
        colStart, rowStart, bandStart = subset[1][1], subset[1][0], 0
        colEnd, rowEnd, bandEnd = subset[1][1], subset[1][0], bands - 1
    else:  # subset[0] == 'custom'
        cols, rows, bands = subset[1][1][1] - subset[1][1][0] + 1, subset[1][0][1] - subset[1][0][0] + 1, \
                            len(subset[1][2])
        colStart, rowStart, bandStart = subset[1][1][0], subset[1][0][0], min(subset[1][2])
        colEnd, rowEnd, bandEnd = subset[1][1][1], subset[1][0][1], max(subset[1][2])
    bandsList = subset[1][2] if subset[0] == 'custom' else range(bands)

    return collections.OrderedDict(zip(
        ['rows', 'cols', 'bands', 'rowStart', 'rowEnd', 'colStart', 'colEnd', 'bandStart', 'bandEnd', 'bandsList'],
        [rows, cols, bands, rowStart, rowEnd, colStart, colEnd, bandStart, bandEnd, bandsList]))


def clip_array_using_mapBounds(array, bounds, im_prj, im_gt, fillVal=0):
    """

    :param array:
    :param bounds:
    :param im_prj:
    :param im_gt:
    :param fillVal:
    """
    print(bounds)
    # get target bounds on the same grid like the input array
    tgt_xmin, tgt_ymin, tgt_xmax, tgt_ymax = snap_bounds_to_pixGrid(bounds, im_gt)
    print(tgt_xmin, tgt_ymax, tgt_xmax, tgt_ymin)

    # get target dims
    tgt_rows = int(abs((tgt_ymax - tgt_ymin) / im_gt[5])) + 1
    tgt_cols = int(abs((tgt_xmax - tgt_xmin) / im_gt[1])) + 1
    tgt_bands = array.shape[2] if len(array.shape) == 3 else None
    tgt_shape = (tgt_rows, tgt_cols, tgt_bands) if len(array.shape) == 3 else (tgt_rows, tgt_cols)

    # get array pos to fill
    R, C = array.shape[:2]
    tgt_gt = [tgt_xmin, im_gt[1], 0., tgt_ymax, 0., im_gt[5]]
    cS, rS = [int(i) for i in mapXY2imXY(imXY2mapXY((0, 0), im_gt), tgt_gt)]
    cE, rE = [int(i) for i in mapXY2imXY(imXY2mapXY((C - 1, R - 1), im_gt), tgt_gt)]
    print(rS, rE, cS, cE)

    # create target array and fill it with the given pixel values at the correct geo position
    tgt_arr = np.full(tgt_shape, fillVal, array.dtype)
    tgt_arr[rS:rE + 1, cS:cE + 1] = array

    return tgt_arr, tgt_gt, im_prj
