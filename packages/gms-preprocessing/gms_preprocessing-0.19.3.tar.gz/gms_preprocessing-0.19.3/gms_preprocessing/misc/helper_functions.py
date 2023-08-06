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

"""Collection of helper functions for GeoMultiSens."""

import collections
import errno
import gzip
from zipfile import ZipFile
import itertools
import math
import operator
import os
import re
import shlex
import warnings
from datetime import datetime

import numpy as np
import psycopg2
import shapely
from shapely.geometry import Polygon

try:
    from osgeo import ogr
except ImportError:
    import ogr
from multiprocessing import sharedctypes
from matplotlib import pyplot as plt
from subprocess import Popen, PIPE
from xml.etree.ElementTree import QName

from ..options.config import GMS_config as CFG
from . import database_tools as DB_T
from ..misc.definition_dicts import proc_chain

from py_tools_ds.geo.coord_trafo import mapXY2imXY, reproject_shapelyGeometry
from py_tools_ds.geo.coord_calc import corner_coord_to_minmax

__author__ = 'Daniel Scheffler'


def get_parentObjDict():
    from ..algorithms.L1A_P import L1A_object
    from ..algorithms.L1B_P import L1B_object
    from ..algorithms.L1C_P import L1C_object
    from ..algorithms.L2A_P import L2A_object
    from ..algorithms.L2B_P import L2B_object
    from ..algorithms.L2C_P import L2C_object

    return dict(L1A=L1A_object,
                L1B=L1B_object,
                L1C=L1C_object,
                L2A=L2A_object,
                L2B=L2B_object,
                L2C=L2C_object)


initArgsDict = {'L1A': (None,), 'L1B': (None,), 'L1C': (None,),
                'L2A': (None,), 'L2B': (None,), 'L2C': (None,)}


def silentremove(filename):
    # type: (str) -> None
    """Remove the given file without raising OSError exceptions, e.g. if the file does not exist."""

    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occured


def silentmkdir(path_dir_file):
    # type: (str) -> None
    while not os.path.isdir(os.path.dirname(path_dir_file)):
        try:
            os.makedirs(os.path.dirname(path_dir_file))
        except OSError as e:
            if e.errno != 17:
                raise
            else:
                pass


def gzipfile(iname, oname, compression_level=1, blocksize=None):
    blocksize = blocksize if blocksize else 1 << 16  # 64kB
    with open(iname, 'rb') as f_in:
        f_out = gzip.open(oname, 'wb', compression_level)
        while True:
            block = f_in.read(blocksize)
            if block == '':
                break
            f_out.write(block)
        f_out.close()


def get_zipfile_namelist(path_zipfile):
    with ZipFile(path_zipfile) as zF:
        namelist = zF.namelist()
    return namelist


def ENVIfile_to_ENVIcompressed(inPath_hdr, outPath_hdr=None):
    inPath_bsq = os.path.splitext(inPath_hdr)[0] + '.bsq'
    outPath_bsq = os.path.splitext(outPath_hdr)[0] + '.bsq' if outPath_hdr else inPath_bsq
    gzipfile(inPath_bsq, outPath_bsq)
    with open(inPath_hdr, 'r') as inF:
        items = inF.read().split('\n')  # FIXME use append write mode
    items.append('file compression = 1')
    with open(inPath_hdr, 'w') as outFile:
        [outFile.write(item + '\n') for item in items]
        # FIXME include file reordering


def subcall_with_output(cmd, no_stdout=False, no_stderr=False):
    """Execute external command and get its stdout, exitcode and stderr.
    :param cmd: a normal shell command including parameters
    """

    proc = Popen(shlex.split(cmd), stdout=None if no_stdout else PIPE, stderr=None if no_stderr else PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode

    return out, exitcode, err


def sorted_nicely(iterable):
    """ Sort the given iterable in the way that humans expect.
    :param iterable:
    """

    def convert(text): return int(text) if text.isdigit() else text

    def alphanum_key(key): return [convert(c) for c in re.split('([0-9]+)', key)]

    return sorted(iterable, key=alphanum_key)


def safe_str(obj):
    """Return a safe string that will not cause any UnicodeEncodeError issues."""
    return obj.encode('ascii', 'ignore').decode('ascii')


def is_proc_level_lower(current_lvl, target_lvl):
    # type: (str, str) -> bool
    """Return True if current_lvl is lower than target_lvl.

    :param current_lvl:     current processing level (to be tested)
    :param target_lvl:      target processing level (refernce)
    """
    return current_lvl is None or proc_chain.index(current_lvl) < proc_chain.index(target_lvl)


def convert_absPathArchive_to_GDALvsiPath(path_archive):
    assert path_archive.endswith(".zip") or path_archive.endswith(".tar") or path_archive.endswith(".tar.gz") or \
           path_archive.endswith(".tgz"), """*%s archives are not yet supported. Please provide .zip, .tar, .tar.gz or
        .tgz archives.""" % os.path.splitext(path_archive)[1]
    gdal_prefix_dict = {'.zip': '/vsizip', '.tar': '/vsitar', '.tar.gz': '/vsitar', '.tgz': '/vsitar',
                        '.gz': '/vsigzip'}
    file_suffix = os.path.splitext(path_archive)[1]
    file_suffix = '.tar.gz' if path_archive.endswith('.tar.gz') else file_suffix
    return os.path.join(gdal_prefix_dict[file_suffix], os.path.basename(path_archive))


class mp_SharedNdarray(object):
    """
    wrapper class, which collect all neccessary instances to make a numpy ndarray
    accessible as shared memory when using multiprocessing, it exposed the numpy
    array via three different views which can be used to access it globally

    _init provides the mechanism to make this array available in each worker,
    best used using the provided __initializer__
    """

    def __init__(self, dims):
        """
        dims : tuple of dimensions which is used to instantiate a ndarray using np.zero
        """
        # self.ct = np.ctypeslib.as_ctypes(np.zeros(dims, dtype=np.float))  # ctypes view on the new array
        self.ct = np.ctypeslib.as_ctypes(np.empty(dims, dtype=np.float))  # ctypes view on the new array
        self.sh = sharedctypes.Array(self.ct.type_, self.ct, lock=False)  # shared memory view on the array
        self.np = np.ctypeslib.as_array(self.sh)  # numpy view on the array

    def _init(self, globals, name):
        """
        This adds to globals while using
        the ctypes library view of [shared_ndaray instance].sh to make the numpy view
        of [shared_ndaray instance] globally available
        """
        globals[name] = np.ctypeslib.as_array(self.sh)


def mp_initializer(globals, globs):
    """
    globs shall be dict with name:value pairs, when executed value will be added to
    globals under the name name, if value provides a _init attribute this one is
    called instead.

    This makes most sense when called as initializer in a multiprocessing pool, e.g.:
    Pool(initializer=__initializer__,initargs=(globs,))
    :param globals:
    :param globs:
    """

    for name, value in globs.items():
        try:
            value._init(globals, name)
        except AttributeError:
            globals[name] = value


def group_objects_by_attributes(object_list, *attributes):
    get_attr = operator.attrgetter(*attributes)
    return [list(g) for k, g in itertools.groupby(sorted(object_list, key=get_attr), get_attr)]


def group_tuples_by_keys_of_tupleElements(tuple_list, tupleElement_index, key):
    unique_vals = set([tup[tupleElement_index][key] for tup in tuple_list])
    groups = []
    for val in unique_vals:
        groups.append([tup for tup in tuple_list if tup[tupleElement_index][key] == val])
    return groups


def group_dicts_by_key(dict_list, key):
    unique_vals = set([dic[key] for dic in dict_list])
    groups = [[dic for dic in dict_list if dic[key] == val] for val in unique_vals]
    return groups


def cornerLonLat_to_postgreSQL_poly(CornerLonLat):
    """Converts a coordinate list [UL_LonLat, UR_LonLat, LL_LonLat, LR_LonLat] to a postgreSQL polygon.
    :param CornerLonLat:    list of XY-coordinate tuples
    """

    return str(Polygon(CornerLonLat))


def postgreSQL_poly_to_cornerLonLat(pGSQL_poly):
    # type: (str) -> list
    """Converts a postgreSQL polygon to a coordinate list [UL_LonLat, UR_LonLat, LL_LonLat, LR_LonLat].
    :param pGSQL_poly:
    """

    if not pGSQL_poly.startswith('POLYGON'):
        raise ValueError("'pGSQL_poly' has to start with 'POLYGON...'. Got %s" % pGSQL_poly)
    fl = [float(i) for i in re.findall(r"[-+]?\d*\.\d+|\d+", pGSQL_poly)]
    CornerLonLat = [(fl[4], fl[5]), (fl[6], fl[7]), (fl[2], fl[3]), (fl[0], fl[1])]  # UL,UR,LL,LR
    return CornerLonLat


def postgreSQL_geometry_to_postgreSQL_poly(geom):
    # type: (str) -> str
    connection = psycopg2.connect(CFG.conn_database)
    if connection is None:
        return 'database connection fault'
    cursor = connection.cursor()
    cursor.execute("SELECT ST_AsText('%s')" % geom)
    pGSQL_poly = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return pGSQL_poly


def postgreSQL_geometry_to_shapelyPolygon(wkb_hex):
    return shapely.wkb.loads(wkb_hex, hex=True)


def shapelyPolygon_to_postgreSQL_geometry(shapelyPoly):
    # type: (Polygon) -> str
    return shapelyPoly.wkb_hex  # same result as "SELECT ST_GeomFromText('%s')" %shapelyPoly


def get_imageCoords_from_shapelyPoly(shapelyPoly, im_gt):
    # type: (Polygon,list) -> list
    """Converts each vertex coordinate of a shapely polygon into image coordinates corresponding to the given
    geotransform without respect to invalid image coordinates. Those must be filtered later.

    :param shapelyPoly:     <shapely.Polygon>
    :param im_gt:           <list> the GDAL geotransform of the target image
    """

    def get_coordsArr(shpPoly): return np.swapaxes(np.array(shpPoly.exterior.coords.xy), 0, 1)
    coordsArr = get_coordsArr(shapelyPoly)
    imCoordsXY = [mapXY2imXY((X, Y), im_gt) for X, Y in coordsArr.tolist()]
    return imCoordsXY


def get_valid_arrSubsetBounds(arr_shape, tgt_bounds, buffer=0):
    # type: (tuple, tuple, float) -> tuple
    """Validates a given tuple of image coordinates, by checking if each coordinate is within a given bounding box and
    replacing invalid coordinates by valid ones. This function is needed in connection with
    get_arrSubsetBounds_from_shapelyPolyLonLat().

    :param arr_shape:   <tuple of ints> the dimension of the bounding box where target coordinates are validated
                                -> (rows, cols,bands) or (rows,cols)
    :param tgt_bounds:  <tuple of floats>  the target image coordinates in the form (xmin, xmax, ymin, ymax)
    :param buffer:      <float> an optional buffer size (image pixel units)
    """

    rows, cols = arr_shape[:2]
    xmin, xmax, ymin, ymax = tgt_bounds
    if buffer:
        xmin, xmax, ymin, ymax = xmin - buffer, xmax + buffer, ymin - buffer, ymax + buffer

    xmin = int(xmin) if int(xmin) >= 0 else 0
    xmax = math.ceil(xmax) if math.ceil(xmax) <= cols - 1 else cols - 1
    ymin = int(ymin) if int(ymin) >= 0 else 0
    ymax = math.ceil(ymax) if math.ceil(ymax) <= rows - 1 else rows - 1

    outbounds = xmin, xmax, ymin, ymax
    return outbounds if (xmax > 0 or xmax < cols) and (ymax > 0 or ymax < rows) else None


def get_arrSubsetBounds_from_shapelyPolyLonLat(arr_shape, shpPolyLonLat, im_gt, im_prj, pixbuffer=0,
                                               ensure_valid_coords=True):
    # type: (tuple, Polygon, list, str, float, bool) -> tuple
    """Returns validated image coordinates, corresponding to the given shapely polygon. This function can be used to
    get the image coordines of e.g. MGRS tiles for a specific target image.

    :param arr_shape:       <tuple of ints> the dimensions of the target image  -> (rows, cols,bands) or (rows,cols)
    :param shpPolyLonLat:   <tuple of floats>  the shapely polygon to get image coordinates for
    :param im_gt:           <tuple> GDAL geotransform of the target image
    :param im_prj:          <str>  GDAL geographic projection (WKT string) of the target image
                                   (automatic reprojection is done if neccessary)
    :param pixbuffer:          <float> an optional buffer size (image pixel units)
    :param ensure_valid_coords:   <bool> whether to ensure that the returned values are all inside the original
                                         image bounding box
    """

    shpPolyImPrj = reproject_shapelyGeometry(shpPolyLonLat, 4326, im_prj)
    imCoordsXY = get_imageCoords_from_shapelyPoly(shpPolyImPrj, im_gt)
    bounds = corner_coord_to_minmax(imCoordsXY)
    outbounds = get_valid_arrSubsetBounds(arr_shape, bounds, buffer=pixbuffer) if ensure_valid_coords else bounds
    if outbounds:
        xmin, xmax, ymin, ymax = outbounds
        return xmin, xmax, ymin, ymax
    else:
        return None


def get_UL_LR_from_shapefile_features(path_shp):
    # type: (str) -> list
    """Returns a list of upper-left-lower-right coordinates ((ul,lr) tuples) for all features of a given shapefile.

    :param path_shp:   <str> the path of the shapefile
    """

    dataSource = ogr.Open(path_shp)
    layer = dataSource.GetLayer(0)
    ullr_list = []
    for feature in layer:
        e = feature.geometry().GetEnvelope()
        ul = e[0], e[3]
        lr = e[1], e[2]
        ullr_list.append((ul, lr))
    del dataSource, layer
    return ullr_list


def reorder_CornerLonLat(CornerLonLat):
    """Reorders corner coordinate lists from [UL,UR,LL,LR] to clockwise order: [UL,UR,LR,LL]"""

    if len(CornerLonLat) > 4:
        warnings.warn('Only 4 of the given %s corner coordinates were respected.' % len(CornerLonLat))
    return [CornerLonLat[0], CornerLonLat[1], CornerLonLat[3], CornerLonLat[2]]


def sceneID_to_trueDataCornerLonLat(scene_ID):
    """Returns a list of corner coordinates ordered like (UL,UR,LL,LR) corresponding to the given scene_ID by querying
    the database geometry field. """

    try:
        pgSQL_geom = DB_T.get_info_from_postgreSQLdb(CFG.conn_database, 'scenes_proc', 'bounds',
                                                     {'sceneid': scene_ID})[0][0]
    except IndexError:
        pgSQL_geom = DB_T.get_info_from_postgreSQLdb(CFG.conn_database, 'scenes', 'bounds', {'id': scene_ID})[0][0]

    assert shapely.wkb.loads(pgSQL_geom, hex=True).is_valid, \
        'Database error: Received an invalid geometry from the postgreSQL database!'
    return postgreSQL_poly_to_cornerLonLat(postgreSQL_geometry_to_postgreSQL_poly(pgSQL_geom))


def scene_ID_to_shapelyPolygon(scene_ID):
    # type: (int) -> Polygon
    """
    Returns a LonLat shapely.Polygon() object corresponding to the given scene_ID.
    """
    poly = Polygon(reorder_CornerLonLat(sceneID_to_trueDataCornerLonLat(scene_ID)))
    if not poly.is_valid:
        poly = poly.buffer(0)
        assert poly.is_valid
    return poly


def CornerLonLat_to_shapelyPoly(CornerLonLat):
    """Returns a shapely.Polygon() object based on the given coordinate list. """
    poly = Polygon(reorder_CornerLonLat(CornerLonLat))
    if not poly.is_valid:
        poly = poly.buffer(0)
        assert poly.is_valid
    return poly


def find_in_xml_root(namespace, xml_root, branch, *branches, findall=None):
    """
    S2 xml helper function, search from root. Get part of xml.
    :param namespace:
    :param xml_root:
    :param branch: first branch, is combined with namespace
    :param branches: repeated find's along these parameters
    :param findall: if given, at final a findall
    :return: found xml object, None if nothing was found
    """

    buf = xml_root.find(str(QName(namespace, branch)))
    for br in branches:
        buf = buf.find(br)
    if findall is not None:
        buf = buf.findall(findall)
    return buf


def find_in_xml(xml, *branch):
    """
    S2 xml helper function
    :param xml: xml object
    :param branch: iterate to branches using find
    :return: xml object, None if nothing was found
    """

    buf = xml
    for br in branch:
        buf = buf.find(br)
    return buf


def get_values_from_xml(leaf, dtype=np.float):
    """
    S2 xml helper function
    :param leaf: xml object which is searched for VALUES tag which are then composed into a numpy array
    :param dtype: dtype of returned numpy array
    :return: numpy array
    """

    return np.array([ele.text.split(" ") for ele in leaf.findall("VALUES")], dtype=dtype)


def stack_detectors(inp):
    warnings.filterwarnings(action='ignore', message=r'Mean of empty slice')
    res = {bandId: np.nanmean(np.dstack(tuple(inp[bandId].values())), axis=2) for bandId, dat in inp.items()}
    warnings.filterwarnings(action='default', message=r'Mean of empty slice')
    return res


class Landsat_entityID_decrypter(object):
    SenDict = {'C8': 'OLI_TIRS', 'O8': 'OLI', 'T8': 'TIRS', 'E7': 'ETM+', 'T5': 'TM', 'T4': 'TM', 'M1': 'MSS1'}
    SatDict = {'C8': 'Landsat-8', 'O8': 'Landsat-8', 'T8': 'Landsat-8',
               'E7': 'Landsat-7', 'T5': 'Landsat-5', 'T4': 'Landsat-4', 'M1': 'Landsat-1'}

    def __init__(self, entityID):
        self.entityID = entityID
        LDict = self.decrypt()

        SatSen = LDict['sensor'] + LDict['satellite']
        self.satellite = self.SatDict[SatSen]
        self.sensor = self.SenDict[SatSen]
        self.WRS_path = int(LDict['WRS_path'])
        self.WRS_row = int(LDict['WRS_row'])
        self.AcqDate = datetime.strptime(LDict['year'] + LDict['julian_day'], '%Y%j')
        if self.sensor == 'ETM+':
            self.SLCOnOff = 'SLC_ON' if self.AcqDate <= datetime.strptime('2003-05-31 23:46:34', '%Y-%m-%d %H:%M:%S') \
                else 'SLC_OFF'
            self.sensorIncSLC = '%s_%s' % (self.sensor, self.SLCOnOff)
        self.ground_station_ID = LDict['ground_station_identifier']
        self.archive_ver = LDict['archive_version_number']

    def decrypt(self):
        """LXSPPPRRRYYYYDDDGSIVV"""
        LDict = collections.OrderedDict()
        LDict['sensor'] = self.entityID[1]
        LDict['satellite'] = self.entityID[2]
        LDict['WRS_path'] = self.entityID[3:6]
        LDict['WRS_row'] = self.entityID[6:9]
        LDict['year'] = self.entityID[9:13]
        LDict['julian_day'] = self.entityID[13:16]
        LDict['ground_station_identifier'] = self.entityID[16:19]
        LDict['archive_version_number'] = self.entityID[19:21]
        return LDict


def subplot_2dline(XY_tuples, titles=None, shapetuple=None, grid=False):
    shapetuple = (1, len(XY_tuples)) if shapetuple is None else shapetuple
    assert titles is None or len(titles) == len(
        XY_tuples), 'List in titles keyword must have the same length as the passed XY_tuples.'
    fig = plt.figure(figsize=[
        plt.figaspect([.5, ] if shapetuple[1] >= shapetuple[0] else [2., ]) * (2 if len(XY_tuples) == 1 else 3)])
    for i, XY in enumerate(XY_tuples):
        ax = fig.add_subplot(shapetuple[0], shapetuple[1], i + 1)
        X, Y = XY
        ax.plot(X, Y, linestyle='-')
        if titles:
            ax.set_title(titles[i])
        if grid:
            ax.grid(which='major', axis='both', linestyle='-')
    plt.show()


def subplot_imshow(ims, titles=None, shapetuple=None, grid=False):
    ims = [ims] if not isinstance(ims, list) else ims
    assert titles is None or len(titles) == len(ims), 'Error: Got more or less titles than images.'
    shapetuple = (1, len(ims)) if shapetuple is None else shapetuple
    fig, axes = plt.subplots(shapetuple[0], shapetuple[1],
                             figsize=plt.figaspect(.5 if shapetuple[1] > shapetuple[0] else 2.) * 3)
    [axes[i].imshow(im, cmap='binary', interpolation='none', vmin=np.percentile(im, 2), vmax=np.percentile(im, 98)) for
     i, im in enumerate(ims)]
    if titles:
        [axes[i].set_title(titles[i]) for i in range(len(ims))]
    if grid:
        [axes[i].grid(which='major', axis='both', linestyle='-') for i in range(len(ims))]
    plt.show()


def subplot_3dsurface(ims, shapetuple=None):
    ims = [ims] if not isinstance(ims, list) else ims
    shapetuple = (1, len(ims)) if shapetuple is None else shapetuple
    fig = plt.figure(figsize=[plt.figaspect(.5 if shapetuple[1] >= shapetuple[0] else 2.) * 3])
    for i, im in enumerate(ims):
        ax = fig.add_subplot(shapetuple[0], shapetuple[1], i + 1, projection='3d')
        x = np.arange(0, im.shape[0], 1)
        y = np.arange(0, im.shape[1], 1)
        X, Y = np.meshgrid(x, y)
        Z = im.reshape(X.shape)
        ax.plot_surface(X, Y, Z, cmap=plt.cm.hot)
        ax.contour(X, Y, Z, zdir='x', cmap=plt.cm.coolwarm, offset=0)
        ax.contour(X, Y, Z, zdir='y', cmap=plt.cm.coolwarm, offset=im.shape[1])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
    plt.show()
