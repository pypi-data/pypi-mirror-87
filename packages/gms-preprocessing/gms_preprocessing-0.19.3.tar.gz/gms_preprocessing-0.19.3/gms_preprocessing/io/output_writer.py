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

"""Output writer: Universal writer for all kinds of GeoMultiSens intermediate results."""

# from __future__ import (division, print_function, absolute_import)
# unicode literals cause writing errors
import collections
import datetime
import gzip
import os
from typing import TYPE_CHECKING
import pickle

import dill
import numpy as np
from osgeo import gdal_array
from spectral.io import envi
from spectral.io.envi import check_compatibility, check_new_filename, write_envi_header, _write_header_param

try:
    from osgeo import ogr
    from osgeo import osr
    from osgeo import gdal
    from osgeo import gdalnumeric
except ImportError:
    import ogr
    import osr
    import gdal
    import gdalnumeric
import builtins
from itertools import chain

from ..options.config import GMS_config as CFG
from ..misc import helper_functions as HLP_F
from ..misc.definition_dicts import \
    get_mask_classdefinition, get_mask_colormap, get_outFillZeroSaturated, dtype_lib_Python_IDL
from ..misc.logging import GMS_logger

if TYPE_CHECKING:
    from ..model.gms_object import GMS_object  # noqa F401  # flake8 issue

enviHdr_keyOrder = \
    ['ENVI', 'description', 'samples', 'lines', 'bands', 'header offset', 'file type', 'data type',
     'interleave', 'data ignore value', 'sensor type', 'byte order', 'file compression', 'version_gms_preprocessing',
     'versionalias_gms_preprocessing', 'reflectance scale factor', 'class lookup', 'classes', 'class names', 'map info',
     'coordinate system string', 'CS_TYPE', 'CS_EPSG', 'CS_DATUM', 'CS_UTM_ZONE', 'corner coordinates lonlat',
     'image_type', 'Satellite', 'Sensor', 'Subsystem', 'SceneID', 'EntityID', 'arr_pos', 'arr_shape', 'Metafile',
     'gResolution', 'AcqDate', 'AcqTime', 'wavelength', 'bandwidths', 'band names', 'LayerBandsAssignment',
     'data gain values', 'data offset values', 'reflectance gain values', 'reflectance offset values', 'ThermalConstK1',
     'ThermalConstK2', 'ProcLCode', 'PhysUnit', 'ScaleFactor', 'wavelength units', 'SunElevation', 'SunAzimuth',
     'SolIrradiance', 'EarthSunDist', 'ViewingAngle', 'IncidenceAngle', 'FieldOfView', 'scene length',
     'overpass duraction sec', 'Quality', 'Additional']


def silent_envi_write_image(hdr_file, data, header, **kwargs):
    """
    Monkeypatch for spectral.io.envi._write_image in order to silence output stream.
    """
    from ..misc.helper_functions import safe_str
    # force unicode strings
    header = dict((k, v) if not isinstance(v, str) else (k, safe_str(v)) for k, v in header.items())

    check_compatibility(header)
    force = kwargs.get('force', False)
    img_ext = kwargs.get('ext', '.img')

    (hdr_file, img_file) = check_new_filename(hdr_file, img_ext, force)
    write_envi_header(hdr_file, header, is_library=False)

    # bufsize = data.shape[0] * data.shape[1] * np.dtype(dtype).itemsize
    bufsize = data.shape[0] * data.shape[1] * data.dtype.itemsize
    fout = builtins.open(img_file, 'wb', bufsize)
    fout.write(data.tostring())
    fout.close()


def write_ordered_envi_header(fileName, header_dict, is_library=False):
    """
    Monkeypatch for spectral.io.envi.write_envi_header in order to write ordered output headers
    """
    fout = builtins.open(fileName, 'w')
    if isinstance(header_dict, collections.OrderedDict):
        d = header_dict
    else:
        d = {}
        d.update(header_dict)

    if is_library:
        d['file type'] = 'ENVI Spectral Library'
    elif 'file type' not in d:
        d['file type'] = 'ENVI Standard'
    fout.write('ENVI\n')
    # Write the standard parameters at the top of the file
    std_params = ['description', 'samples', 'lines', 'bands', 'header offset',
                  'file type', 'data type', 'interleave', 'sensor type',
                  'byte order', 'reflectance scale factor', 'map info']
    for k in std_params:
        if k in d.keys():
            _write_header_param(fout, k, d[k])
    for k in d.keys():
        if k not in std_params:
            _write_header_param(fout, k, d[k])
    fout.close()


# monkey patch header writer function by a version that respects item order in meta dict
envi.write_envi_header = write_ordered_envi_header


def write_ENVI_compressed(outPath_hdr, ndarray, meta, interleave='bsq'):
    assert interleave in ['bsq', 'bil', 'bip']
    if len(ndarray.shape) == 3:  # 3D
        if interleave == 'bsq':
            arr2write = np.rollaxis(ndarray, 2)  # => bands, rows, cols
        elif interleave == 'bil':
            arr2write = np.swapaxes(ndarray, 1, 2)  # => rows, bands, cols
        else:  # 'bip'
            arr2write = ndarray  # => rows, cols, bands
    else:  # 2D
        arr2write = ndarray

    # write array
    outpathBinary = os.path.join('%s.%s' % (os.path.splitext(outPath_hdr)[0], interleave))
    with gzip.open(outpathBinary, 'wb', compresslevel=1) as f:  # compresslevel can be increased until 9
        f.write(arr2write.tostring())

    # write header
    meta['file compression'] = 1
    write_ordered_envi_header(outPath_hdr, meta)

    # check if output is GDAL readable
    if gdalnumeric.LoadFile(outpathBinary, 0, 0, 1, 1) is None:
        return 0
    else:
        return 1


def HDR_writer(meta_dic, outpath_hdr, logger=None):
    if logger is not None:
        logger.info('Writing %s header ...' % os.path.basename(outpath_hdr))
    envi.write_envi_header(outpath_hdr, meta_dic)
    reorder_ENVI_header(outpath_hdr, enviHdr_keyOrder)


def Tiles_Writer(tileList_or_Array, out_path, out_shape, out_dtype, out_interleave, out_meta=None,
                 arr_pos=None, overwrite=True):
    """Write tiles to disk using numpy.memmap.

    :param tileList_or_Array:   <list of dicts> each dict has keys 'row_start','row_end','col_start','col_end','data'
                                <numpy array> representing a subset of a full array. requires arr_pos
    :param out_path:            <str> path to ENVI header file *.hdr
    :param out_shape:           <tuple or list> (rows,cols,bands)
    :param out_dtype:           <object> numpy data type object
    :param out_interleave:      <str> 'bsq','bil' or 'bip'
    :param out_meta:            <dict> metadata dictionary to be written to header
    :param arr_pos:             <tuple> ((row_start,row_end),(col_start,col_end))
    :param overwrite:           <bool>
    """

    assert isinstance(tileList_or_Array, (list, np.ndarray))
    if isinstance(tileList_or_Array, np.ndarray):
        assert arr_pos and isinstance(arr_pos, (list, tuple))

    oP_hdr = out_path
    oP_ext = os.path.splitext(oP_hdr)[0] + '.%s' % out_interleave
    rows, cols, bands = out_shape

    # write binary file
    if not os.path.exists(oP_ext):
        open(oP_ext, 'a').close()  # create empty binary file
    elif overwrite:
        open(oP_ext, 'w').close()  # overwrite binary file with empty one

    if out_interleave == 'bsq':
        memmap = np.memmap(oP_ext, dtype=out_dtype, mode='r+', offset=0, shape=(bands, rows, cols))
        memmap = np.swapaxes(np.swapaxes(memmap, 0, 2), 0, 1)  # rows,cols,bands
    elif out_interleave == 'bil':
        memmap = np.memmap(oP_ext, dtype=out_dtype, mode='r+', offset=0, shape=(rows, bands, cols))
        memmap = np.swapaxes(memmap, 1, 2)
    else:  # bip
        memmap = np.memmap(oP_ext, dtype=out_dtype, mode='r+', offset=0, shape=(rows, cols, bands))

    if isinstance(tileList_or_Array, list):
        tileList_or_Array = [dict(i) for i in tileList_or_Array]
        is_3D = True if len(tileList_or_Array[0]['data'].shape) == 3 else False
        for tile in tileList_or_Array:
            data = tile['data'] if is_3D else tile['data'][:, :, None]
            memmap[tile['row_start']:tile['row_end'] + 1, tile['col_start']:tile['col_end'] + 1, :] = data
    else:
        (rS, rE), (cS, cE) = arr_pos
        is_3D = True if len(tileList_or_Array.shape) == 3 else False
        data = tileList_or_Array if is_3D else tileList_or_Array[:, :, None]
        memmap[rS:rE + 1, cS:cE + 1, :] = data

    # write header
    std_meta = {'lines': rows, 'samples': cols, 'bands': bands, 'header offset': 0, 'byte order': 0,
                'interleave': out_interleave, 'data type': dtype_lib_Python_IDL[out_dtype]}
    out_meta = out_meta if out_meta else {}
    out_meta.update(std_meta)
    from ..model.metadata import metaDict_to_metaODict
    out_meta = metaDict_to_metaODict(out_meta)

    if not os.path.exists(oP_hdr) or overwrite:
        write_envi_header(oP_hdr, out_meta)


def reorder_ENVI_header(path_hdr, tgt_keyOrder):
    # type: (str,list) -> None
    """Reorders the keys of an ENVI header file according to the implemented order. Keys given in the target order list
    but missing the ENVI fileare skipped.
    This function is a workaround for envi.write_envi_header of Spectral Python Library that always writes the given
    metadata dictinary as an unordered dict.

    :param path_hdr:       <str> path of the target ENVI file
    :param tgt_keyOrder:    <list> list of target keys in the correct order
    """
    with open(path_hdr, 'r') as inF:
        items = inF.read().split('\n')
    HLP_F.silentremove(path_hdr)

    with open(path_hdr, 'w') as outFile:
        for paramName in tgt_keyOrder:
            for item in items:
                if item.startswith(paramName) or item.startswith(paramName.lower()):
                    outFile.write(item + '\n')
                    items.remove(item)
                    continue
        # write remaining header items
        [outFile.write(item + '\n') for item in items]


def mask_to_ENVI_Classification(InObj, maskname):
    # type: (GMS_object, str) -> (np.ndarray, dict, list, list)
    cd = get_mask_classdefinition(maskname, InObj.satellite)
    if cd is None:
        InObj.logger.warning("No class definition available for mask '%s'." % maskname)
    else:
        temp = np.empty_like(getattr(InObj, maskname))
        temp[:] = getattr(InObj, maskname)
        # deep copy: converts view to its own array in order to avoid overwriting of InObj.maskname
        classif_array = temp
        rows, cols = classif_array.shape[:2]
        bands = 1 if classif_array.ndim == 2 else classif_array.shape[2]

        mapI, CSS = InObj.MetaObj.map_info, InObj.MetaObj.projection
        mask_md = {'file type': 'ENVI Classification', 'map info': mapI, 'coordinate system string': CSS, 'lines': rows,
                   'samples': cols, 'bands': bands, 'header offset': 0, 'byte order': 0, 'interleave': 'bsq',
                   'data type': 1, 'data ignore value': get_outFillZeroSaturated(classif_array.dtype)[0]}

        pixelVals_in_mask = list(np.unique(classif_array))
        fillVal = get_outFillZeroSaturated(classif_array.dtype)[0]
        pixelVals_expected = sorted(list(cd.values()) + ([fillVal] if fillVal is not None else []))

        pixelVals_unexpected = [i for i in pixelVals_in_mask if i not in pixelVals_expected]
        if pixelVals_unexpected:
            InObj.logger.warning('The cloud mask contains unexpected pixel values: %s '
                                 % ', '.join(str(i) for i in pixelVals_unexpected))
        mask_md['classes'] = len(pixelVals_in_mask) + 1  # 1 class for no data pixels

        class_names = ['No data' if i == fillVal else
                       'Unknown Class' if i in pixelVals_unexpected else
                       list(cd.keys())[list(cd.values()).index(i)] for i in pixelVals_in_mask]

        clr_mp_allClasses = get_mask_colormap(maskname)
        class_colors = collections.OrderedDict(zip(class_names, [clr_mp_allClasses[cN] for cN in class_names]))

        # pixel values for object classes must be numbered like 0,1,2,3,4,...
        if fillVal is not None:
            classif_array[classif_array == fillVal] = 0
        if fillVal in pixelVals_in_mask:
            pixelVals_in_mask.remove(fillVal)
            remaining_pixelVals = range(1, len(pixelVals_in_mask) + 1)
        else:
            remaining_pixelVals = range(len(pixelVals_in_mask))
            del mask_md['data ignore value']
        for in_val, out_val in zip(pixelVals_in_mask, remaining_pixelVals):
            classif_array[classif_array == in_val] = out_val

        classif_array = classif_array.astype(np.uint8)  # contains only 0,1,2,3,4,...
        classif_meta = add_ENVIclassificationMeta_to_meta(mask_md, class_names, class_colors, classif_array)
        return classif_array, classif_meta


def add_ENVIclassificationMeta_to_meta(meta, class_names, class_colors=None, data=None):
    # type: (dict,list,dict,np.ndarray) -> dict
    """Prepare ENVI metadata dict. to be written as ENVI classification file by adding custom class names and colors.

    :param meta:            <dict> ENVI metadata dictionary
    :param class_names:     <list> of strings with the class names
    :param class_colors:    <dict> with keys representing class names and values representing 3-tuples with RGB codes
    :param data:            <numpy array> only used to estimate number of classes if class_names is None"""

    from spectral import spy_colors
    if class_names is None:
        assert data is not None, "'data' must be given if 'class_names' is None."
    meta['file type'] = "ENVI Classification"
    n_classes = len(class_names) if class_names else int(np.max(data) + 1)
    meta['classes'] = str(n_classes)
    meta['class names'] = class_names if class_names else \
        (['Unclassified'] + ['Class %s' % i for i in range(1, n_classes)])
    colors = list(chain.from_iterable([class_colors[class_name] for class_name in class_names])) \
        if class_colors else []
    meta['class lookup'] = colors if len(colors) == n_classes * 3 else \
        [list(spy_colors[i % len(spy_colors)]) for i in range(n_classes)]
    return meta


def check_header_not_empty(hdr):
    with open(hdr, 'r') as inF:
        content = inF.read()
    return True if content else False


def set_output_nodataVal(arr_path, nodataVal=None):
    """Sets the no data value of an already written file

    :param arr_path:
    :param nodataVal:
    :return:
    """
    ds = gdal.Open(arr_path)

    if nodataVal is None:
        dtype = gdal_array.GDALTypeCodeToNumericTypeCode(ds.GetRasterBand(1).DataType)
        nodataVal = get_outFillZeroSaturated(dtype)[0]

    for bandIdx in range(ds.RasterCount):
        band = ds.GetRasterBand(bandIdx + 1)
        band.SetNoDataValue(nodataVal)
        band.FlushCache()
        del band
    del ds


def add_attributes_to_ENVIhdr(attr2add_dict, hdr_path):
    Spyfileheader = envi.open(hdr_path)
    attr_dict = Spyfileheader.metadata
    attr_dict.update(attr2add_dict)
    HDR_writer(attr_dict, hdr_path)


def export_VZA_SZA_SAA_RAA_stats(L1A_object):
    outdict = collections.OrderedDict()
    for i in ['VZA', 'SZA', 'SAA', 'RAA']:
        if hasattr(L1A_object, i + '_arr'):
            arr = getattr(L1A_object, i + '_arr')
            outdict[i + '_mean'] = np.mean(arr[arr != -9999])
            outdict[i + '_std'] = np.std(arr[arr != -9999])
    with open(os.path.join(L1A_object.path_procdata, L1A_object.baseN + '_stats__VZA_SZA_SAA_RAA.dill'), 'wb') as outF:
        #        json.dump(outdict, outF,skipkeys=True,sort_keys=True,separators=(',', ': '),indent =4)
        dill.dump(outdict, outF)
    with open(os.path.join(L1A_object.path_procdata, L1A_object.baseN + '_stats__VZA_SZA_SAA_RAA.txt'), 'w') as outF:
        for k, v in outdict.items():
            outF.write(k + ' = ' + str(v) + '\n')


def write_global_benchmark_output(list__processing_time__all_runs, list__IO_time__all_runs, data_list):
    dict_sensorcodes2write = {}
    for i in data_list:
        sensorcode = '%s_%s_%s' % (i['satellite'], i['sensor'], i['subsystem']) if i['subsystem'] is not None \
            else '%s_%s' % (i['satellite'], i['sensor'])
        if sensorcode not in dict_sensorcodes2write.keys():
            dict_sensorcodes2write.update({sensorcode: 1})
        else:
            dict_sensorcodes2write[sensorcode] += 1
    str2write_sensors = ', '.join(['%s x %s' % (v, k) for k, v in dict_sensorcodes2write.items()])
    count_processed_data = len(data_list)
    str2write_totaltimes = '\t'.join([str(i) for i in list__processing_time__all_runs])
    str2write_IOtimes = '\t'.join([str(i) for i in list__IO_time__all_runs])
    list_mean_time_per_ds = [str(processing_time / count_processed_data) for processing_time in
                             list__processing_time__all_runs]
    str2write_times_per_ds = '\t'.join(list_mean_time_per_ds)
    str2write = '\t'.join([str(CFG.CPUs), str(count_processed_data), str2write_sensors, str2write_totaltimes,
                           str2write_IOtimes, str2write_times_per_ds, '\n'])
    if not os.path.isdir(CFG.path_benchmarks):
        os.makedirs(CFG.path_benchmarks)
    with open(os.path.join(CFG.path_benchmarks, CFG.ID), 'a') as outF:
        outF.write(str2write)


def write_shp_OLD(shapely_poly, path_out, prj=None):
    assert os.path.exists(os.path.dirname(path_out)), 'Directory %s does not exist.' % os.path.dirname(path_out)

    print('Writing %s ...' % path_out)
    HLP_F.silentremove(path_out)
    ds = ogr.GetDriverByName("Esri Shapefile").CreateDataSource(path_out)
    if prj is not None:
        srs = osr.SpatialReference()
        srs.ImportFromWkt(prj)
        layer = ds.CreateLayer('', srs, ogr.wkbPolygon)
    else:
        layer = ds.CreateLayer('', None, ogr.wkbPolygon)
    layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))  # Add one attribute
    defn = layer.GetLayerDefn()

    # Create a new feature (attribute and geometry)
    feat = ogr.Feature(defn)
    feat.SetField('id', 123)

    # Make a geometry, from Shapely object
    geom = ogr.CreateGeometryFromWkb(shapely_poly.wkb)
    feat.SetGeometry(geom)
    layer.CreateFeature(feat)

    # Save and close everything
    del ds, layer, feat, geom


def get_dtypeStr(val):
    is_numpy = 'numpy' in str(type(val))
    DType = \
        str(np.dtype(val)) if is_numpy else \
        'int' if isinstance(val, int) else \
        'float' if isinstance(val, float) else \
        'str' if isinstance(val, str) else \
        'complex' if isinstance(val, complex) else \
        'date' if isinstance(val, datetime.datetime) else None
    assert DType, 'data type not understood'
    return DType


def write_shp(path_out, shapely_geom, prj=None, attrDict=None):
    shapely_geom = [shapely_geom] if not isinstance(shapely_geom, list) else shapely_geom
    attrDict = [attrDict] if not isinstance(attrDict, list) else attrDict
    # print(len(shapely_geom))
    # print(len(attrDict))
    assert len(shapely_geom) == len(attrDict), "'shapely_geom' and 'attrDict' must have the same length."
    assert os.path.exists(os.path.dirname(path_out)), 'Directory %s does not exist.' % os.path.dirname(path_out)

    print('Writing %s ...' % path_out)
    if os.path.exists(path_out):
        os.remove(path_out)
    ds = ogr.GetDriverByName("Esri Shapefile").CreateDataSource(path_out)

    if prj is not None:
        srs = osr.SpatialReference()
        srs.ImportFromWkt(prj)
    else:
        srs = None

    geom_type = list(set([gm.type for gm in shapely_geom]))
    assert len(geom_type) == 1, 'All shapely geometries must belong to the same type. Got %s.' % geom_type

    layer = \
        ds.CreateLayer('', srs, ogr.wkbPoint) if geom_type[0] == 'Point' else \
        ds.CreateLayer('', srs, ogr.wkbLineString) if geom_type[0] == 'LineString' else \
        ds.CreateLayer('', srs, ogr.wkbPolygon) if geom_type[0] == 'Polygon' else \
        None  # FIXME

    if isinstance(attrDict[0], dict):
        for attr in attrDict[0].keys():
            assert len(attr) <= 10, "ogr does not support fieldnames longer than 10 digits. '%s' is too long" % attr
            DTypeStr = get_dtypeStr(attrDict[0][attr])
            FieldType = ogr.OFTInteger if DTypeStr.startswith('int') else ogr.OFTReal if DTypeStr.startswith(
                'float') else \
                ogr.OFTString if DTypeStr.startswith('str') else ogr.OFTDateTime if DTypeStr.startswith(
                    'date') else None
            FieldDefn = ogr.FieldDefn(attr, FieldType)
            if DTypeStr.startswith('float'):
                FieldDefn.SetPrecision(6)
            layer.CreateField(FieldDefn)  # Add one attribute

    for i in range(len(shapely_geom)):
        # Create a new feature (attribute and geometry)
        feat = ogr.Feature(layer.GetLayerDefn())
        feat.SetGeometry(ogr.CreateGeometryFromWkb(shapely_geom[i].wkb))  # Make a geometry, from Shapely object

        list_attr2set = attrDict[0].keys() if isinstance(attrDict[0], dict) else []

        for attr in list_attr2set:
            val = attrDict[i][attr]
            DTypeStr = get_dtypeStr(val)
            val = int(val) if DTypeStr.startswith('int') else float(val) if DTypeStr.startswith('float') else \
                str(val) if DTypeStr.startswith('str') else val
            feat.SetField(attr, val)

        layer.CreateFeature(feat)
        feat.Destroy()

    # Save and close everything
    del ds, layer


def dump_all_SRFs(outpath_dump=os.path.abspath(os.path.join(os.path.dirname(__file__), '../sandbox/out/SRF_DB.pkl')),
                  outpath_log=os.path.abspath(os.path.join(os.path.dirname(__file__), '../sandbox/out/SRF_DB.log'))):
    from .input_reader import SRF_Reader
    out_dict = {}
    logger = GMS_logger('log__SRF_DB', path_logfile=outpath_log, append=True)
    for sensorcode, out_sensorcode in zip(
        ['AST_V1', 'AST_V2', 'AST_S', 'AST_T', 'TM5', 'TM7', 'LDCM', 'RE5', 'S1', 'S4', 'S5'],
        ['ASTER_VNIR1', 'ASTER_VNIR2', 'ASTER_SWIR', 'ASTER_TIR', 'LANDSAT_TM5', 'LANDSAT_TM7', 'LANDSAT_LDCM',
         'RapidEye_5', 'Spot_1', 'Spot_4', 'Spot_5']):

        out_dict[out_sensorcode] = SRF_Reader(sensorcode, logger)

    with open(outpath_dump, 'wb') as outFile:
        pickle.dump(out_dict, outFile)

    print('Saved SRF dictionary to %s' % outpath_dump)

    with open(outpath_dump, 'rb') as inFile:
        readFile = pickle.load(inFile)

    print(readFile == out_dict)

    for i in readFile.items():
        print(i)
