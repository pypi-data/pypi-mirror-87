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
import glob
import itertools
import os
import re
import shutil
import sys
import traceback
import warnings
from datetime import datetime
from typing import Union, TYPE_CHECKING  # noqa F401  # flake8 issue
from pkg_resources import parse_version

import numpy as np
import pandas as pd
from pandas.io.sql import pandasSQL_builder, SQLTable, DataFrame, Series
import psycopg2
from shapely.wkb import loads as wkb_loads
from geoalchemy2.types import Geometry as GEOMETRY
from geopandas import GeoDataFrame
from shapely.geometry import Polygon, box, MultiPolygon
from sqlalchemy import create_engine
from sqlalchemy.types import to_instance, TypeEngine

from ..options.config import GMS_config as CFG
from . import path_generator as PG
from .definition_dicts import proc_chain

if TYPE_CHECKING:
    from ..model.gms_object import GMS_object  # noqa F401  # flake8 issue

# + misc.helper_functions.cornerLonLat_to_postgreSQL_poly: (left out here in order to avoid circular dependencies)

__author__ = 'Daniel Scheffler'


def execute_pgSQL_query(cursor, query_command):
    """Executes a postgreSQL query catches the full error message if there is one.
    """

    try:
        cursor.execute(query_command)
    except psycopg2.ProgrammingError as e:
        raise psycopg2.ProgrammingError(e.pgerror + 'Query failed. Command was:\n%s' % query_command)


def get_scene_and_dataset_infos_from_postgreSQLdb(sceneid):
    # type: (int) -> collections.OrderedDict
    """Creates an OrderedDict containing further information about a given scene ID by querying the pgSQL database.

    :param sceneid:   <int> the GMS scene ID to get information for
    """

    def query(tablename, vals2return, cond_dict, records2fetch=0):
        return get_info_from_postgreSQLdb(CFG.conn_database, tablename, vals2return, cond_dict, records2fetch)
    resultset = query('scenes', ['datasetid', 'satelliteid', 'sensorid', 'subsystemid', 'acquisitiondate', 'entityid',
                                 'filename'], {'id': sceneid})
    if len(resultset) == 0:
        sys.stderr.write("Scene with id %s not found. Skipping.." % sceneid)

    scenedata = resultset[0]
    ds = collections.OrderedDict()
    proc_level_tmp = query('scenes_proc', 'proc_level', {'sceneid': sceneid})
    ds.update({'proc_level': 'L0A' if proc_level_tmp == [] else proc_level_tmp[0][0]})
    ds.update({'scene_ID': sceneid})
    ds.update({'datasetid': scenedata[0]})
    ds.update({'image_type': query('datasets', 'image_type', {'id': scenedata[0]})[0][0]})
    ds.update({'satellite': query('satellites', 'name', {'id': scenedata[1]})[0][0]})
    ds.update({'sensor': query('sensors', 'name', {'id': scenedata[2]})[0][0]})
    ds.update({'subsystem': query('subsystems', 'name', {'id': scenedata[3]})[0][0] if scenedata[3] else None})
    ds.update({'acq_datetime': scenedata[4]})
    ds.update({'entity_ID': scenedata[5]})
    ds.update({'filename': scenedata[6]})
    return ds


def get_postgreSQL_value(value):
    # type: (any) -> str
    """Converts Python variable to a postgreSQL value respecting postgreSQL type casts.
    The resulting value can be directly inserted into a postgreSQL query."""

    assert type(value) in [int, float, bool, str, Polygon, datetime, list, tuple] or value is None, \
        "Unsupported value type within postgreSQL matching expression. Got %s." % type(value)
    if isinstance(value, int):
        pgV = value
    elif isinstance(value, float):
        pgV = value
    elif isinstance(value, bool):
        pgV = value
    elif value is None:
        pgV = 'NULL'
    elif isinstance(value, str):
        pgV = "'%s'" % value.replace("'", "")
    elif isinstance(value, Polygon):
        pgV = "'%s'" % value.wkb_hex
    elif isinstance(value, datetime):
        pgV = "TIMESTAMP '%s'" % str(value)
    else:  # list or tuple in value
        if not value:  # empty list/tuple
            pgV = 'NULL'
        else:
            dTypes_in_value = list(set([type(i) for i in value]))
            assert len(dTypes_in_value) == 1, \
                'Mixed data types in postgreSQL matching expressions are not supported. Got %s.' % dTypes_in_value
            assert dTypes_in_value[0] in [int, str, float, np.int64, bool]
            pgList = ",".join(["'%s'" % i if isinstance(value[0], str) else "%s" % i for i in value])
            pgV = "'{%s}'" % pgList
    return pgV


def get_postgreSQL_matchingExp(key, value):
    # type: (str,any) -> str
    """Converts a key/value pair to a postgreSQL matching expression in the form "column=value" respecting postgreSQL
    type casts. The resulting string can be directly inserted into a postgreSQL query.
    """
    pgVal = get_postgreSQL_value(value)
    if isinstance(pgVal, str) and pgVal.startswith("'{") and pgVal.endswith("}'"):
        return '%s in %s' % (key, pgVal.replace("'{", '(').replace("}'", ')'))  # '{1,2,3}' => (1,2,3)
    elif pgVal == 'NULL':
        return '%s is NULL' % key
    else:
        return '%s=%s' % (key, pgVal)


def get_info_from_postgreSQLdb(conn_params, tablename, vals2return, cond_dict=None, records2fetch=0, timeout=15000):
    # type: (str, str, Union[list, str], dict, int, int) -> Union[list, str]
    """Queries a postgreSQL database for the given parameters.

    :param conn_params:     <str> connection parameters as provided by CFG.conn_params
    :param tablename:       <str> name of the table within the database to be queried
    :param vals2return:     <list or str> a list of strings containing the column titles of the values to be returned
    :param cond_dict:       <dict> a dictionary containing the query conditions in the form {'column_name':<value>}
                            HINT: <value> can also be a list or a tuple of elements to match, BUT note that the order
                                  of the list items is NOT respected!
    :param records2fetch:   <int> number of records to be fetched (default=0: fetch unlimited records)
    :param timeout:         <int> allows to set a custom statement timeout (milliseconds)
    """

    if not isinstance(vals2return, list):
        vals2return = [vals2return]
    assert isinstance(records2fetch, int), "get_info_from_postgreSQLdb: Expected an integer for the argument " \
                                           "'records2return'. Got %s" % type(records2fetch)
    cond_dict = cond_dict if cond_dict else {}
    conn_params = "%s options = '-c statement_timeout=%s'" % (conn_params, timeout)
    connection = psycopg2.connect(conn_params)
    if connection is None:
        warnings.warn('database connection fault')
        return 'database connection fault'
    cursor = connection.cursor()
    condition = "WHERE " + " AND ".join([get_postgreSQL_matchingExp(k, v) for k, v in cond_dict.items()]) \
        if cond_dict else ""
    cmd = "SELECT " + ','.join(vals2return) + " FROM " + tablename + " " + condition
    execute_pgSQL_query(cursor, cmd)

    records2return = cursor.fetchall() if records2fetch == 0 else [cursor.fetchone()] if records2fetch == 1 else \
        cursor.fetchmany(size=records2fetch)  # e.g. [('LE71950282003121EDC00',), ('LE71950282003105ASN00',)]
    cursor.close()
    connection.close()
    return records2return


def update_records_in_postgreSQLdb(conn_params, tablename, vals2update_dict, cond_dict=None, timeout=15000):
    # type: (str, str, dict, dict, int) -> Union[None, str]
    """Queries a postgreSQL database for the given parameters and updates the given columns of the query result.

    :param conn_params:       <str> connection parameters as provided by CFG.conn_params
    :param tablename:         <str> name of the table within the database to be updated
    :param vals2update_dict:  <dict> a dictionary containing keys and values to be set in the form {'col_name':<value>}
    :param cond_dict:         <dict> a dictionary containing the query conditions in the form {'column_name':<value>}
                              HINT: <value> can also be a list or a tuple of elements to match
    :param timeout:           <int> allows to set a custom statement timeout (milliseconds)
    """

    cond_dict = cond_dict if cond_dict else {}
    conn_params = "%s options = '-c statement_timeout=%s'" % (conn_params, timeout)
    connection = psycopg2.connect(conn_params)
    if connection is None:
        warnings.warn('database connection fault')
        return 'database connection fault'
    cursor = connection.cursor()
    condition = "WHERE " + " AND ".join([get_postgreSQL_matchingExp(k, v) for k, v in cond_dict.items()]) \
        if cond_dict else ""
    update_cond = "SET " + ', '.join(['%s=%s' % (k, get_postgreSQL_value(vals2update_dict[k]))
                                      for k in vals2update_dict.keys()])
    execute_pgSQL_query(cursor, "SELECT EXISTS(SELECT 1 FROM scenes %s);" % condition)
    if cursor.fetchone()[0] == 0:
        warnings.warn("No record found fulfilling this condition: \n'%s'." % condition)
    else:
        execute_pgSQL_query(cursor, "UPDATE " + tablename + " " + update_cond + " " + condition)

    if 'connection' in locals():
        connection.commit()
        connection.close()


def append_item_to_arrayCol_in_postgreSQLdb(conn_params, tablename, vals2append_dict, cond_dict=None, timeout=15000):
    # type: (str, str, dict, dict, int) -> Union[None, str]
    """Queries a postgreSQL database for the given parameters
    and appends the given value to the specified column of the query result.

    :param conn_params:       <str> connection parameters as provided by CFG.conn_params
    :param tablename:         <str> name of the table within the database to be updated
    :param vals2append_dict:  <dict> a dictionary containing keys and value(s) to be set in the form
                              {'col_name':[<value>,<value>]}
    :param cond_dict:         <dict> a dictionary containing the query conditions in the form {'column_name':<value>}
                              HINT: <value> can also be a list or a tuple of elements to match
    :param timeout:           <int> allows to set a custom statement timeout (milliseconds)
    """

    assert len(vals2append_dict) == 1, 'Values can be appended to only one column at once.'
    if type(list(vals2append_dict.values())[0]) in [list, tuple]:
        raise NotImplementedError('Appending multiple values to one column at once is not yet supported.')
    cond_dict = cond_dict if cond_dict else {}
    conn_params = "%s options = '-c statement_timeout=%s'" % (conn_params, timeout)
    connection = psycopg2.connect(conn_params)
    if connection is None:
        warnings.warn('database connection fault')
        return 'database connection fault'
    cursor = connection.cursor()
    condition = "WHERE " + " AND ".join([get_postgreSQL_matchingExp(k, v) for k, v in cond_dict.items()]) \
        if cond_dict else ""
    col2update = list(vals2append_dict.keys())[0]
    pgSQL_val = get_postgreSQL_value(vals2append_dict[col2update])
    pgSQL_val = pgSQL_val if type(vals2append_dict[col2update]) in [list, tuple] else '{%s}' % pgSQL_val
    append_cond = "SET %s = array_cat(%s, '%s')" % (col2update, col2update, pgSQL_val)
    execute_pgSQL_query(cursor, "SELECT EXISTS(SELECT 1 FROM scenes %s);" % condition)
    if cursor.fetchone()[0] == 0:
        warnings.warn("No record found fulfilling this condition: \n'%s'." % condition)
    else:
        execute_pgSQL_query(cursor, "UPDATE " + tablename + " " + append_cond + " " + condition + ';')
    if 'connection' in locals():
        connection.commit()
        connection.close()


def remove_item_from_arrayCol_in_postgreSQLdb(conn_params, tablename, vals2remove_dict, cond_dict=None, timeout=15000):
    # type: (str, str, dict, dict, int) -> Union[None, str]
    """Queries a postgreSQL database for the given parameters
    and removes the given value from the specified column of the query result.

    :param conn_params:       <str> connection parameters as provided by CFG.conn_params
    :param tablename:         <str> name of the table within the database to be updated
    :param vals2remove_dict:  <dict> a dictionary containing keys and value(s) to be set in the form
                              {'col_name':[<value>,<value>]}
    :param cond_dict:         <dict> a dictionary containing the query conditions in the form {'column_name':<value>}
                              HINT: <value> can also be a list or a tuple of elements to match
    :param timeout:           <int> allows to set a custom statement timeout (milliseconds)
    """

    assert len(vals2remove_dict) == 1, 'Values can be removed from only one column at once.'
    if type(list(vals2remove_dict.values())[0]) in [list, tuple]:
        raise NotImplementedError('Removing multiple values from one column at once is not yet supported.')
    cond_dict = cond_dict if cond_dict else {}
    conn_params = "%s options = '-c statement_timeout=%s'" % (conn_params, timeout)
    connection = psycopg2.connect(conn_params)
    if connection is None:
        warnings.warn('database connection fault')
        return 'database connection fault'
    cursor = connection.cursor()
    condition = "WHERE " + " AND ".join([get_postgreSQL_matchingExp(k, v) for k, v in cond_dict.items()]) \
        if cond_dict else ""
    col2update = list(vals2remove_dict.keys())[0]
    pgSQL_val = get_postgreSQL_value(vals2remove_dict[col2update])
    pgSQL_val = pgSQL_val if type(vals2remove_dict[col2update]) in [list, tuple] else '{%s}' % pgSQL_val
    remove_cond = "SET %s = array_remove(%s, '%s')" % (col2update, col2update, pgSQL_val)
    execute_pgSQL_query(cursor, "SELECT EXISTS(SELECT 1 FROM scenes %s);" % condition)
    if cursor.fetchone()[0] == 0:
        warnings.warn("No record found fulfilling this condition: \n'%s'." % condition)
    else:
        execute_pgSQL_query(cursor, "UPDATE " + tablename + " " + remove_cond + " " + condition + ';')
    if 'connection' in locals():
        connection.commit()
        connection.close()


def increment_decrement_arrayCol_in_postgreSQLdb(conn_params, tablename, col2update, idx_val2decrement=None,
                                                 idx_val2increment=None, cond_dict=None, timeout=15000):
    # type: (str, str, str, int, int, dict, int) -> Union[None, str]
    """Updates an array column of a specific postgreSQL table in the form that it increments or decrements the elements
    at a given position. HINT: The column must have values like that: [52,0,27,10,8,0,0,0,0]

    :param conn_params:         <str> connection parameters as provided by CFG.conn_params
    :param tablename:           <str> name of the table within the database to be update
    :param col2update:          <str> column name of the column to be updated
    :param idx_val2decrement:   <int> the index of the array element to be decremented (starts with 1)
    :param idx_val2increment:   <int> the index of the array element to be incremented (starts with 1)
    :param cond_dict:           <dict> a dictionary containing the query conditions in the form {'column_name':<value>}
                                HINT: <value> can also be a list or a tuple of elements to match
    :param timeout:             <int> allows to set a custom statement timeout (milliseconds)
    :return:
    """

    cond_dict = cond_dict if cond_dict else {}
    conn_params = "%s options = '-c statement_timeout=%s'" % (conn_params, timeout)
    connection = psycopg2.connect(conn_params)
    if connection is None:
        warnings.warn('database connection fault')
        return 'database connection fault'
    cursor = connection.cursor()
    condition = "WHERE " + " AND ".join([get_postgreSQL_matchingExp(k, v) for k, v in cond_dict.items()]) \
        if cond_dict else ""

    dec_str = '' if idx_val2decrement is None else \
        "%s[%s] = %s[%s]-1" % (col2update, idx_val2decrement, col2update, idx_val2decrement)
    inc_str = '' if idx_val2increment is None else \
        "%s[%s] = %s[%s]+1" % (col2update, idx_val2increment, col2update, idx_val2increment)

    if dec_str or inc_str:
        dec_inc_str = ','.join([dec_str, inc_str])
        execute_pgSQL_query(cursor, "UPDATE %s SET %s %s" % (tablename, dec_inc_str, condition))

    if 'connection' in locals():
        connection.commit()
        connection.close()


def create_record_in_postgreSQLdb(conn_params, tablename, vals2write_dict, timeout=15000):
    # type: (str, str, dict, int) -> Union[int, str]
    """Creates a single new record in a postgreSQL database and pupulates its columns with the given values.

    :param conn_params:       <str> connection parameters as provided by CFG.conn_params
    :param tablename:         <str> name of the table within the database to be updated
    :param vals2write_dict:   <dict> a dictionary containing keys and values to be set in the form {'col_name':<value>}
    :param timeout:           <int> allows to set a custom statement timeout (milliseconds)
    """

    conn_params = "%s options = '-c statement_timeout=%s'" % (conn_params, timeout)
    connection = psycopg2.connect(conn_params)
    if connection is None:
        warnings.warn('database connection fault')
        return 'database connection fault'
    cursor = connection.cursor()

    keys, vals = zip(*[(k, str(get_postgreSQL_value(v))) for k, v in vals2write_dict.items()])

    execute_pgSQL_query(cursor, "INSERT INTO %s (%s) VALUES (%s);" % (tablename, ','.join(keys), ','.join(vals)))
    execute_pgSQL_query(cursor, "SELECT id FROM %s ORDER BY id DESC LIMIT 1" % tablename)
    newID = cursor.fetchone()[0]

    if 'connection' in locals():
        connection.commit()
        connection.close()

    return newID


def delete_record_in_postgreSQLdb(conn_params, tablename, record_id, timeout=15000):
    # type: (str, str, dict, int) -> Union[int, str]
    """Delete a single record in a postgreSQL database.

    :param conn_params:       <str> connection parameters as provided by CFG.conn_params
    :param tablename:         <str> name of the table within the database to be updated
    :param record_id:         <dict> ID of the record to be deleted
    :param timeout:           <int> allows to set a custom statement timeout (milliseconds)
    """

    conn_params = "%s options = '-c statement_timeout=%s'" % (conn_params, timeout)
    connection = psycopg2.connect(conn_params)
    if connection is None:
        warnings.warn('database connection fault')
        return 'database connection fault'
    cursor = connection.cursor()

    execute_pgSQL_query(cursor, "DELETE FROM %s WHERE id=%s;" % (tablename, record_id))
    execute_pgSQL_query(cursor, "SELECT id FROM %s WHERE id=%s" % (tablename,  record_id))

    res = cursor.fetchone()

    if 'connection' in locals():
        connection.commit()
        connection.close()

    return 'success' if res is None else 'fail'


def get_pgSQL_geospatial_query_cond(conn_params, table2query, geomCol2use='bounds', tgt_corners_lonlat=None,
                                    scene_ID=None, queryfunc='ST_Intersects', crossing_dateline_check=True):
    assert tgt_corners_lonlat if scene_ID is None else scene_ID, "Provide eihter scene_ID or tgt_corners_lonlat!"

    if tgt_corners_lonlat:
        # handle coordinates crossing the 180 degress meridian (dateline)
        # FIXME in that case the polygone has to be split at the dateline. otherwise pgSQL may yield wrong results
        if crossing_dateline_check:
            xvals = [x for x, y in tgt_corners_lonlat]
            if max(xvals) - min(xvals) > 180:
                tgt_corners_lonlat = [(x, y) if x > 0 else (x + 360, y) for x, y in tgt_corners_lonlat]

        from .helper_functions import cornerLonLat_to_postgreSQL_poly
        pGSQL_poly = cornerLonLat_to_postgreSQL_poly(tgt_corners_lonlat)
        src_geom = "'SRID=4326;%s'::geometry" % pGSQL_poly  # source geometry is given
        # FIXME scenes tabelle hat "geography" geoinfos -> eigener Index wird bei "geometry" nicht genutzt:
        tgt_geom = "%s.%s::geometry" % (table2query, geomCol2use)
        geocond = "%s(%s, %s)" % (queryfunc, src_geom, tgt_geom)
    else:  # scene_ID is not None:
        connection = psycopg2.connect(conn_params)
        if connection is None:
            return 'database connection fault'
        cursor = connection.cursor()
        cmd = "SELECT ST_AsText(bounds) FROM scenes WHERE scenes.id = %s" % scene_ID
        execute_pgSQL_query(cursor, cmd)
        res = cursor.fetchone()
        cursor.close()
        connection.close()
        if len(res):
            src_geom = "'SRID=4326;%s'::geometry" % res
        else:
            print('The scene with the ID %s does not exist in the scenes table.')
            return []
        geocond = "%s(%s, %s.%s::geometry)" % (queryfunc, src_geom, table2query, geomCol2use)
    return geocond


def get_overlapping_scenes_from_postgreSQLdb(conn_params, table='scenes_proc', scene_ID=None,
                                             tgt_corners_lonlat=None, conditions=None, add_cmds='', timeout=15000):
    # type: (str, str, int, list, Union[list, str], str, int) -> Union[list, str]

    """Queries the postgreSQL database in order to find those scenes of a specified reference satellite (Landsat-8 or
    Sentinel-2) that have an overlap to the given corner coordinates AND that fulfill the given conditions.

    :param conn_params:             <str> connection parameters as provided by CFG.conn_params
    :param table:                   <str> name of the table within the database to be updated
    :param scene_ID:                <int> a sceneID to get the target geographical extent from
                                        (needed if tgt_corners_lonlat is not provided)
    :param tgt_corners_lonlat:      <list> a list of coordinates defining the target geographical extent
                                           (needed if scene_ID is not provided)
    :param conditions:              <list> a list of additional query conditions
    :param add_cmds:                <str> additional pgSQL commands to be added to the pgSQL query
    :param timeout:                 <int> allows to set a custom statement timeout (milliseconds)
    """

    conditions = [] if conditions is None else conditions if isinstance(conditions, list) else [conditions]
    conn_params = "%s options = '-c statement_timeout=%s'" % (conn_params, timeout)
    connection = psycopg2.connect(conn_params)
    if connection is None:
        return 'database connection fault'
    datasetids = [int(d.split('=')[1].strip()) for d in conditions if d.startswith('datasetid')]
    datasetid = datasetids[0] if datasetids else 104  # Landsat-8
    # FIXME: use Landsat-8 instead of Sentinel-2 as long as S2 L1A_P is not working:
    datasetid = 104 if datasetid == 249 else datasetid

    if table != 'scenes_proc':
        assert datasetid, "filtdsId is needed if table is not 'scenes_proc'"
    if scene_ID is None:
        assert tgt_corners_lonlat, "Provide either scene_ID or tgt_corners_lonlat!"
    if tgt_corners_lonlat is None:
        assert scene_ID, "Provide either scene_ID or tgt_corners_lonlat!"

    val2get = "scenes.id" if table == 'scenes' else "%s.sceneid" % table
    # refcond  = ['scenes_proc.georef = True'] if not datasetids else ['scenes.datasetid = %s' %datasetid]
    refcond = ['scenes.datasetid = %s' % datasetid]

    geocond = [get_pgSQL_geospatial_query_cond(conn_params, table, tgt_corners_lonlat=tgt_corners_lonlat,
                                               scene_ID=scene_ID, queryfunc='ST_Intersects',
                                               crossing_dateline_check=True)]

    join = "INNER JOIN scenes ON (%s.sceneid = scenes.id) " % table if table != 'scenes' and datasetids else ''
    conditions = [c for c in conditions if not c.startswith('datasetid')]
    where = "WHERE %s" % " AND ".join(geocond + refcond + conditions)
    usedtbls = "scenes" if table == 'scenes' else "%s, scenes" % table if 'scenes.' in where and join == '' else table
    query = "SELECT %s FROM %s %s%s %s" % (val2get, usedtbls, join, where, add_cmds)
    cursor = connection.cursor()
    execute_pgSQL_query(cursor, query)
    records2return = cursor.fetchall()
    cursor.close()
    connection.close()
    return records2return


def get_overlapping_MGRS_tiles(conn_params, scene_ID=None, tgt_corners_lonlat=None, timeout=15000):
    """In contrast to pgSQL 'Overlapping' here means that both geometries share some spatial area.
    So it combines ST_Overlaps and ST_Contains."""
    assert tgt_corners_lonlat if scene_ID is None else scene_ID, "Provide eihter scene_ID or tgt_corners_lonlat!"

    conn_params = "%s options = '-c statement_timeout=%s'" % (conn_params, timeout)
    connection = psycopg2.connect(conn_params)
    if connection is None:
        return 'database connection fault'

    vals2get = ['grid100k', 'grid1mil', 'geom']
    # FIXME this is covered by ST_Intersects:
    # geocond1 = get_pgSQL_geospatial_query_cond(conn_params, 'mgrs_tiles', geomCol2use='geom', queryfunc='ST_Overlaps',
    #                                            tgt_corners_lonlat=tgt_corners_lonlat, scene_ID=scene_ID)
    # geocond2 = get_pgSQL_geospatial_query_cond(conn_params, 'mgrs_tiles', geomCol2use='geom', queryfunc='ST_Contains',
    #                                            tgt_corners_lonlat=tgt_corners_lonlat, scene_ID=scene_ID)
    # geocond3 = get_pgSQL_geospatial_query_cond(conn_params, 'mgrs_tiles', geomCol2use='geom', queryfunc='ST_Within',
    #                                            tgt_corners_lonlat=tgt_corners_lonlat, scene_ID=scene_ID)
    geocond = get_pgSQL_geospatial_query_cond(conn_params, 'mgrs_tiles', geomCol2use='geom', queryfunc='ST_Intersects',
                                              tgt_corners_lonlat=tgt_corners_lonlat, scene_ID=scene_ID,
                                              crossing_dateline_check=True)
    # query = "SELECT %s FROM %s WHERE %s OR %s OR %s"
    #     % (', '.join(vals2get), 'mgrs_tiles', geocond1, geocond2, geocond3)
    query = "SELECT %s FROM %s WHERE %s" % (', '.join(vals2get), 'mgrs_tiles', geocond)
    cursor = connection.cursor()
    execute_pgSQL_query(cursor, query)
    records = cursor.fetchall()
    cursor.close()
    connection.close()

    GDF = GeoDataFrame(records, columns=['grid100k', 'grid1mil', 'wkb_hex'])

    GDF['shapelyPoly_LonLat'] = list(GDF['wkb_hex'].map(lambda wkb_hex: wkb_loads(wkb_hex, hex=True)))
    GDF['granuleid'] = GDF['grid1mil'].str.cat(GDF['grid100k'])
    return GDF[['granuleid', 'shapelyPoly_LonLat']]


def get_overlapping_MGRS_tiles2(conn_params, scene_ID=None, tgt_corners_lonlat=None, timeout=15000):
    assert tgt_corners_lonlat if scene_ID is None else scene_ID, "Provide eihter scene_ID or tgt_corners_lonlat!"

    conn_params = "%s options = '-c statement_timeout=%s'" % (conn_params, timeout)
    connection = psycopg2.connect(conn_params)
    if connection is None:
        return 'database connection fault'

    vals2get = ['granuleid', 'footprint_wgs84']
    geocond = get_pgSQL_geospatial_query_cond(conn_params, 'footprints_sentinel2_granules',
                                              geomCol2use='footprint_wgs84',
                                              tgt_corners_lonlat=tgt_corners_lonlat, scene_ID=scene_ID)
    query = "SELECT %s FROM %s WHERE %s" % (', '.join(vals2get), 'footprints_sentinel2_granules', geocond)

    cursor = connection.cursor()
    execute_pgSQL_query(cursor, query)
    records = cursor.fetchall()
    cursor.close()
    connection.close()

    GDF = GeoDataFrame(records, columns=['granuleid', 'wkb_hex'])

    GDF['shapelyPoly_LonLat'] = list(GDF['wkb_hex'].map(lambda wkb_hex: wkb_loads(wkb_hex, hex=True)))

    return GDF[['granuleid', 'shapelyPoly_LonLat']]


def get_dict_satellite_name_id(conn_params):
    # type: (str) -> dict
    """Returns a dictionary with satellite names as keys and satellite IDs as values as read from pgSQL database.

    :param conn_params:     <str> pgSQL database connection parameters
    """

    res = get_info_from_postgreSQLdb(conn_params, 'satellites', ['name', 'id'])
    assert len(res) > 0, 'Error getting satellite names from postgreSQL database.'
    arr = np.array(res)
    return dict(zip(list(arr[:, 0]), list(arr[:, 1])))


def get_dict_sensor_name_id(conn_params):
    # type: (str) -> dict
    """Returns a dictionary with sensor names as keys and sensor IDs as values as read from pgSQL database.
    :param conn_params:     <str> pgSQL database connection parameters """

    res = get_info_from_postgreSQLdb(conn_params, 'sensors', ['name', 'id'])
    assert len(res) > 0, 'Error getting sensor names from postgreSQL database.'
    arr = np.array(res)
    return dict(zip(list(arr[:, 0]), list(arr[:, 1])))


def get_entityIDs_from_filename(conn_DB, filename):
    # type: (str, str) -> list
    """Returns entityID(s) for the given filename. In case of Sentinel-2 there can be more multiple entity IDs if
    multiple granules are saved in one .zip file.

    :param conn_DB:     <str> pgSQL database connection parameters
    :param filename:    <str> the filename to get the corresponding entity ID(s) for
    """

    if filename[:2] in ['LE', 'LC', 'LO'] and filename.endswith('.tar.gz'):  # Landsat
        entityIDs = [filename.split('.tar.gz')[0]]
    else:
        print('Querying database in order to get entityIDs for %s...' % filename)
        res = get_info_from_postgreSQLdb(conn_DB, 'scenes', ['entityid'], {'filename': filename}, timeout=40000)
        entityIDs = [subres[0] for subres in res] if len(res) > 0 else []
    return entityIDs


def get_filename_by_entityID(conn_DB, entityid, satellite):
    # type: (str,str,str) -> str
    """Returns the filename for the given entity ID.

    :param conn_DB:     <str> pgSQL database connection parameters
    :param entityid:    <str> entity ID
    :param satellite:   <str> satellite name to which the entity ID is belonging
    """

    if re.search(r'Landsat', satellite, re.I):
        filename = '%s.tar.gz' % entityid
    elif re.search(r'Sentinel-2', satellite, re.I):
        filename = get_info_from_postgreSQLdb(conn_DB, 'scenes', ['filename'],
                                              {'entityid': entityid}, records2fetch=1)[0][0]
    else:
        raise NotImplementedError
    return filename


def get_notDownloadedsceneIDs(conn_DB, entityIDs, satellite, sensor, src_folder):
    # type: (str,list,str,str,str) -> np.ndarray
    """Takes a list of entity IDs and extracts those records that have the corresponding archive file in the given
    source folder and that have the processing level 'METADATA' in the pgSQL database. Based on this subset a numpy
    array containing the corresponding scene IDs and the target filenames for the fileserver is returned.

    :param conn_DB:     <str> pgSQL database connection parameters
    :param entityIDs:   <list> a list of entity IDs
    :param satellite:   <str> the name of the satellite to restrict the query on
    :param sensor:      <str> the name of the sensor to restrict the query on
    :param src_folder:  <str> the source directory where archive files are saved
    """

    columns = ['id', 'entityid', 'satelliteid', 'sensorid', 'filename', 'proc_level']
    result = get_info_from_postgreSQLdb(conn_DB, 'scenes', columns, {'entityid': entityIDs})
    df = pd.DataFrame(result, columns=columns)

    satNameID_dic = get_dict_satellite_name_id(conn_DB)
    satID = satNameID_dic[satellite]
    target_folder = os.path.join(CFG.path_archive, satellite, sensor)

    def get_fName(entityid): return get_filename_by_entityID(conn_DB, entityid, satellite)

    def tgt_exists(fileName): return os.path.exists(os.path.join(target_folder, fileName))

    def src_exists(entityid):
        return os.path.exists(os.path.join(src_folder, get_filename_by_entityID(conn_DB, entityid, satellite)))
    df['tgt_fileName'] = list(df['entityid'].map(get_fName))
    df['tgtFile_exists'] = list(df['tgt_fileName'].map(tgt_exists))
    df['srcFile_exists'] = list(df['entityid'].map(src_exists))
    tgt_satID = (df.satelliteid == float(satID))
    # isDL = (df.proc_level == 'DOWNLOADED')
    isMET = (df.proc_level == 'METADATA')
    # tgtE = (df.tgtFile_exists == True)
    srcE = df.srcFile_exists  # (df.srcFile_exists == True)
    # sceneIDs_notDL_tgtE = df[tgt_satID & (isDL == 0) & tgtE]  # maybe needed later
    # sceneIDs_DL_tgtNE = df[tgt_satID & isDL & (tgtE == 0)]  # maybe needed later
    # sceneIDs_DL_tgtE = df[tgt_satID & isDL & tgtE]  # maybe needed later
    sceneIDs_isMET_srcE = df[tgt_satID & isMET & srcE]
    return sceneIDs_isMET_srcE[['id', 'tgt_fileName']].values


class GMS_JOB(object):
    """gms_preprocessing job manager"""

    def __init__(self, conn_db):
        # type: (str) -> None
        """
        :param conn_db: <str> the database connection parameters as given by CFG.conn_params
        """
        # privates
        self._virtualsensorid = None

        # defaults
        self.conn = conn_db
        self.dataframe = DataFrame()
        self.scene_counts = {}  # set by self.create()

        self.exists_in_db = False
        self.id = None  #: int
        self.creationtime = datetime.now()  # default, needed to create new job
        self.finishtime = None
        self.sceneids = []
        self.timerange_start = datetime.min
        self.timerange_end = datetime.max
        self.bounds = box(-180, -90, 180, 90)  # default, needed to create new job
        self.distribution_index = None
        self.progress = None
        self.feedback = None
        self.failed_sceneids = []
        self.ref_job_id = None
        self.datacube_mgrs_tiles_proc = []
        self.non_ref_datasetids = []
        self.max_cloudcover = None
        self.season_code = None  # type: int
        self.path_analysis_script = ''  # TODO
        self.job_mode = 'processing_only'  # FIXME download/processing/...
        self.jobs_table_columns = ['id', 'creationtime', 'finishtime', 'sceneids', 'timerange_start',
                                   'timerange_end', 'bounds', 'distribution_index', 'progress', 'feedback',
                                   'failed_sceneids', 'datasetid_spatial_ref',
                                   'virtualsensorid', 'ref_job_id', 'datacube_mgrs_tiles_proc', 'comment',
                                   'non_ref_datasetids', 'max_cloudcover', 'season_code', 'status',
                                   'path_analysis_script', 'analysis_parameter', 'statistics', 'job_mode']
        self.datasetid_spatial_ref = 249  # this is overwritten if existing job is read from DB but needed to create new
        self.datasetname_spatial_ref = 'SENTINEL-2A'  # same here
        self.status = None
        self.statistics = []
        self.comment = None
        self.epsg = None  # set by self._set_target_sensor_specs()
        self.ground_spatial_sampling = None  # set by self._set_target_sensor_specs()
        self.analysis_parameter = None

    def __repr__(self):
        return 'GMS job:\n\n' + Series(self.db_entry).to_string()

    @property
    def virtualsensorid(self):
        return self._virtualsensorid

    @virtualsensorid.setter
    def virtualsensorid(self, value):
        """Set virtual sensor ID but continue if no data value is received
        NOTE:  set by self._set_target_sensor_specs() and self.from_ID()"""
        if value != -1:  # no data value
            self._virtualsensorid = value

    def _set_target_sensor_specs(self, virtual_sensor_id, datasetid_spatial_ref):
        self.virtualsensorid = virtual_sensor_id

        if not isinstance(datasetid_spatial_ref, int):
            raise ValueError(datasetid_spatial_ref)

        res = get_info_from_postgreSQLdb(self.conn, 'virtual_sensors', ['spatial_resolution',
                                                                        "projection_epsg"], {'id': virtual_sensor_id})
        assert res, \
            "'virtual_sensor_id'=%s does not exist in the table 'virtual_sensors' of the database." % virtual_sensor_id
        target_gsd = res[0][0]
        self.ground_spatial_sampling = [target_gsd, target_gsd] if type(target_gsd) in [int, float] else target_gsd
        self.epsg = int(res[0][1])

        self.datasetid_spatial_ref = datasetid_spatial_ref
        res = get_info_from_postgreSQLdb(self.conn, 'datasets', ['name'], {'id': datasetid_spatial_ref})
        assert res, \
            "'datasetid_spatial_ref'=%s does not exist in the table 'datasets' of the database." % datasetid_spatial_ref
        self.datasetname_spatial_ref = res

    @property
    def db_entry(self):
        """Returns an OrderedDict containing keys and values of the database entry.
        """

        db_entry = collections.OrderedDict()
        for i in self.jobs_table_columns:
            val = getattr(self, i)

            if i == 'virtualsensorid' and val is None:
                val = -1  # nodata value

            db_entry[i] = val

        return db_entry

    def from_dictlist(self, dictlist_data2process, virtual_sensor_id, datasetid_spatial_ref=249, comment=None):
        # type: (list, int, int, str) -> GMS_JOB
        """
        :param dictlist_data2process:  <list> a list of dictionaries containing the keys "satellite", "sensor" and
                                        "filenames",
                                        e.g. [{'satellite:'Landsat-8,'sensor':'OLI_TIRS','filenames':file.tar.gz},{...}]
        :param virtual_sensor_id :     <int> a valid ID from the 'virtual_sensors' table of the postgreSQL database
        :param datasetid_spatial_ref:  <int> a valid dataset ID of the dataset to be chosen as spatial reference
                                        (from the 'datasets' table of the postgreSQL database)
                                        (default:249 - Sentinel-2A), 104=Landsat-8
        :param comment:                <str> a comment describing the job (e.g. 'Beta job')
        """

        self._set_target_sensor_specs(virtual_sensor_id, datasetid_spatial_ref)
        self.comment = comment

        dictlist_data2process = dictlist_data2process if dictlist_data2process else []

        for idx, datadict in enumerate(dictlist_data2process):
            assert isinstance(datadict, dict), "Expected only dictionaries within 'dictlist_data2process'. " \
                                               "Got %s in there." % type(datadict)
            assert False not in [i in datadict for i in ['satellite', 'sensor', 'filenames']]
            assert type(datadict['filenames']) in [list, str]

            if isinstance(datadict['filenames'], str):
                if datadict['filenames'].endswith('.csv'):
                    assert os.path.exists(datadict['filenames'])
                else:
                    datadict['filenames'] = [datadict['filenames']]

        # find all duplicates in input datadicts and build common dataframe
        all_dfs = []
        for datadict in dictlist_data2process:
            assert isinstance(datadict, dict)

            if isinstance(datadict['filenames'], str) and datadict['filenames'].endswith('.csv'):
                datadict['filenames'] = None  # TODO implement csv reader here
                raise NotImplementedError

            else:
                temp_df = DataFrame(datadict, columns=['satellite', 'sensor', 'filenames'])

                if re.search(r'Landsat-7', datadict['satellite'], re.I) and \
                   re.search(r'ETM+', datadict['sensor'], re.I):

                    from .helper_functions import Landsat_entityID_decrypter as LED

                    def get_L7_sensor(fN):
                        return LED(fN.split('.tar.gz')[0]).sensorIncSLC

                    temp_df['sensor'] = list(temp_df['filenames'].map(get_L7_sensor))

                all_dfs.append(temp_df)

        df = DataFrame(pd.concat(all_dfs)).drop_duplicates()
        df.columns = ['satellite', 'sensor', 'filename']

        # run self.from_dictlist
        sceneInfoDF = self._get_validated_sceneInfoDFs(df)

        # populate attributes
        self._populate_jobAttrs_from_sceneInfoDF(sceneInfoDF)

        return self

    def from_sceneIDlist(self, list_sceneIDs, virtual_sensor_id, datasetid_spatial_ref=249, comment=None):
        # type: (list, int, int, str) -> object
        """
        Create a GMS_JOB instance based on the given list of scene IDs.

        :param list_sceneIDs:          <list> of scene IDs, e.g. [26781907, 26781917, 26542650, 26542451, 26541679]
        :param virtual_sensor_id :     <int> a valid ID from the 'virtual_sensors' table of the postgreSQL database
        :param datasetid_spatial_ref:  <int> a valid dataset ID of the dataset to be chosen as spatial reference
                                        (from the 'datasets' table of the postgreSQL database)
                                        (default:249 - Sentinel-2A), 104=Landsat-8
        :param comment:                <str> a comment describing the job (e.g. 'Beta job')
        """

        self._set_target_sensor_specs(virtual_sensor_id, datasetid_spatial_ref)
        self.comment = comment

        list_sceneIDs = list(list_sceneIDs)

        # query 'satellite', 'sensor', 'filename' from database and summarize in DataFrame
        with psycopg2.connect(self.conn) as conn:
            with conn.cursor() as cursor:
                execute_pgSQL_query(cursor,
                                    """SELECT scenes.id, satellites.name, sensors.name, scenes.filename FROM scenes
                                    LEFT JOIN satellites on scenes.satelliteid=satellites.id
                                    LEFT JOIN sensors on scenes.sensorid=sensors.id
                                    WHERE scenes.id in (%s)""" % ','.join([str(i) for i in list_sceneIDs]))
                df = DataFrame(cursor.fetchall(), columns=['sceneid', 'satellite', 'sensor', 'filename'])

        # FIXME overwriting 'ETM+_SLC_OFF' with 'ETM+' causes _get_validated_sceneInfoDFs() to fail because the
        # FIXME sensorid for ETM+_SLC_OFF cannot be retrieved
        # df['sensor'] = df['sensor'].apply(lambda senN: senN if senN != 'ETM+_SLC_OFF' else 'ETM+')
        df = df.drop_duplicates()

        if df.empty:
            raise ValueError('None of the given scene IDs could be found in the GeoMultiSens database. '
                             'Job creation failed.')
        else:
            missing_IDs = [i for i in list_sceneIDs if i not in df['sceneid'].values]
            if missing_IDs:
                warnings.warn('The following scene IDs could not been found in the GeoMultiSens database: \n%s'
                              % '\n'.join([str(i) for i in missing_IDs]))

            # run self.from_dictlist
            sceneInfoDF = self._get_validated_sceneInfoDFs(df)

            # populate attributes
            self._populate_jobAttrs_from_sceneInfoDF(sceneInfoDF)

        return self

    def from_entityIDlist(self, list_entityids, virtual_sensor_id, datasetid_spatial_ref=249, comment=None):
        """Create a GMS_JOB instance based on the given list of entity IDs.

        :param list_entityids:
        :param virtual_sensor_id:
        :param datasetid_spatial_ref:
        :param comment:
        :return:
        """

        res_sceneIDs = get_info_from_postgreSQLdb(self.conn, 'scenes', ['id', ], {'entityid': list_entityids})
        if not res_sceneIDs:
            raise ValueError('No matching database entries found for the given entity IDs.')

        list_sceneIDs = np.array(res_sceneIDs)[:, 0].tolist()
        count_no_match = len(list_entityids) - len(list_sceneIDs)

        if count_no_match:
            warnings.warn('%s datasets could not be found the database. They cannot be processed.' % count_no_match)

        return self.from_sceneIDlist(list_sceneIDs, virtual_sensor_id,
                                     datasetid_spatial_ref=datasetid_spatial_ref, comment=comment)

    def from_filenames(self, list_filenames, virtual_sensor_id, datasetid_spatial_ref=249, comment=None):
        """Create a GMS_JOB instance based on the given list of provider archive filenames.

        :param list_filenames:
        :param virtual_sensor_id:
        :param datasetid_spatial_ref:
        :param comment:
        :return:
        """

        res_sceneIDs = get_info_from_postgreSQLdb(self.conn, 'scenes', ['id', ], {'filename': list_filenames})
        if not res_sceneIDs:
            raise ValueError('No matching database entries found for the given filenames.')

        list_sceneIDs = np.array(res_sceneIDs)[:, 0].tolist()
        count_no_match = len(list_filenames) - len(list_sceneIDs)

        if count_no_match:
            warnings.warn('%s datasets could not be found the database. They cannot be processed.')

        return self.from_sceneIDlist(list_sceneIDs, virtual_sensor_id,
                                     datasetid_spatial_ref=datasetid_spatial_ref, comment=comment)

    def _get_validated_sceneInfoDFs(self, DF_SatSenFname):
        # type: (DataFrame) -> DataFrame
        """

        :param DF_SatSenFname:
        :return:
        """

        df = DF_SatSenFname

        # loop through all satellite-sensor combinations and get scene information from database
        all_df_recs, all_df_miss = [], []
        all_satellites, all_sensors = zip(
            *[i.split('__') for i in (np.unique(df['satellite'] + '__' + df['sensor']))])

        for satellite, sensor in zip(all_satellites, all_sensors):
            cur_df = df.loc[(df['satellite'] == satellite) & (df['sensor'] == sensor)]
            filenames = list(cur_df['filename'])

            satID_res = get_info_from_postgreSQLdb(self.conn, 'satellites', ['id'], {'name': satellite})
            senID_res = get_info_from_postgreSQLdb(self.conn, 'sensors', ['id'], {'name': sensor})
            assert len(satID_res), "No satellite named '%s' found in database." % satellite
            assert len(senID_res), "No sensor named '%s' found in database." % sensor

            # append sceneid and wkb_hex bounds
            if 'sceneid' in df.columns:
                sceneIDs = list(cur_df['sceneid'])
                conddict = dict(id=sceneIDs, satelliteid=satID_res[0][0], sensorid=senID_res[0][0])
            else:
                conddict = dict(filename=filenames, satelliteid=satID_res[0][0], sensorid=senID_res[0][0])

            records = get_info_from_postgreSQLdb(
                self.conn, 'scenes', ['filename', 'id', 'acquisitiondate', 'bounds'], conddict)
            records = DataFrame(records, columns=['filename', 'sceneid', 'acquisitiondate', 'geom'])
            if 'sceneid' in df.columns:
                del records['sceneid']

            cur_df = cur_df.merge(records, on='filename', how="outer", copy=False)

            # separate records with valid matches in database from invalid matches (filename not found in database)
            df_recs = cur_df[
                cur_df.sceneid.notnull()].copy()  # creates a copy (needed to be able to apply maps later)
            df_miss = cur_df[cur_df.sceneid.isnull()]  # creates a view

            # convert scene ids from floats to integers
            df_recs['sceneid'] = list(df_recs.sceneid.map(lambda sceneid: int(sceneid)))

            # wkb_hex bounds to shapely polygons
            df_recs['polygons'] = list(df_recs.geom.map(lambda wkb_hex: wkb_loads(wkb_hex, hex=True)))

            all_df_recs.append(df_recs)
            all_df_miss.append(df_miss)

        # merge all dataframes of all satellite-sensor combinations
        df_recs_compl = DataFrame(pd.concat(all_df_recs))
        df_miss_compl = DataFrame(pd.concat(all_df_miss))

        # populate attributes
        if not df_miss_compl.empty:
            warnings.warn('The following scene filenames could not been found in the GeoMultiSens database: \n%s'
                          % '\n'.join(list(df_miss_compl['filename'])))

        return df_recs_compl

    def _populate_jobAttrs_from_sceneInfoDF(self, sceneInfoDF):
        # type: (DataFrame) -> None
        """

        :param sceneInfoDF:
        :return:
        """

        if not sceneInfoDF.empty:
            self.dataframe = sceneInfoDF
            self.sceneids = list(self.dataframe['sceneid'])
            self.statistics = [len(self.sceneids)] + [0] * 8
            self.bounds = box(*MultiPolygon(list(self.dataframe['polygons'])).bounds)
            self.timerange_start = self.dataframe.acquisitiondate.min().to_pydatetime()
            self.timerange_end = self.dataframe.acquisitiondate.max().to_pydatetime()

    def from_job_ID(self, job_ID):
        # type: (int) -> GMS_JOB
        """
        Create a GMS_JOB instance by querying the database for a specific job ID.
        :param job_ID:  <int> a valid id from the database table 'jobs'
        """

        res = get_info_from_postgreSQLdb(self.conn, 'jobs', self.jobs_table_columns, {'id': job_ID})
        if not res:
            raise ValueError("No job with ID %s found in 'jobs' table of the database." % job_ID)

        self.exists_in_db = True
        [setattr(self, attrName, res[0][i]) for i, attrName in enumerate(self.jobs_table_columns)]
        self.bounds = wkb_loads(self.bounds, hex=True)

        # fill self.dataframe
        records = get_info_from_postgreSQLdb(self.conn, 'scenes', ['satelliteid', 'sensorid', 'filename',
                                                                   'id', 'acquisitiondate', 'bounds'],
                                             {'id': self.sceneids})
        df = DataFrame(records,
                       columns=['satelliteid', 'sensorid', 'filename', 'sceneid', 'acquisitiondate', 'geom'])
        all_satIDs = df.satelliteid.unique().tolist()
        all_senIDs = df.sensorid.unique().tolist()
        satName_res = get_info_from_postgreSQLdb(self.conn, 'satellites', ['name'], {'id': all_satIDs})
        senName_res = get_info_from_postgreSQLdb(self.conn, 'sensors', ['name'], {'id': all_senIDs})
        all_satNames = [i[0] for i in satName_res]
        all_senNames = [i[0] for i in senName_res]
        id_satName_dict = dict(zip(all_satIDs, all_satNames))
        id_senName_dict = dict(zip(all_senIDs, all_senNames))
        df.insert(0, 'satellite', list(df.satelliteid.map(lambda satID: id_satName_dict[satID])))
        df.insert(1, 'sensor', list(df.sensorid.map(lambda senID: id_senName_dict[senID])))
        df['polygons'] = list(df.geom.map(lambda wkb_hex: wkb_loads(wkb_hex, hex=True)))

        self.dataframe = df[['satellite', 'sensor', 'filename', 'sceneid', 'acquisitiondate', 'geom', 'polygons']]

        return self

    def reset_job_progress(self):
        """Resets everthing in the database entry that has been written during the last run of the job..
        """

        self.finishtime = None
        self.failed_sceneids = []
        self.progress = None
        self.status = 'pending'
        self.statistics = [len(self.sceneids)] + [0] * 8

        self.update_db_entry()

    def _get_dataframe(self, datadict):  # FIXME deprecated
        df = DataFrame(datadict, columns=['satellite', 'sensor', 'filenames'])
        df.columns = ['satellite', 'sensor', 'filename']

        satID_res = get_info_from_postgreSQLdb(self.conn, 'satellites', ['id'], {'name': datadict['satellite']})
        senID_res = get_info_from_postgreSQLdb(self.conn, 'sensors', ['id'], {'name': datadict['sensor']})
        assert len(satID_res), "No satellite named '%s' found in database." % datadict['satellite']
        assert len(senID_res), "No sensor named '%s' found in database." % datadict['sensor']

        # append sceneid and wkb_hex bounds
        records = get_info_from_postgreSQLdb(self.conn, 'scenes', ['filename', 'id', 'acquisitiondate', 'bounds'],
                                             {'filename': datadict['filenames'],
                                              'satelliteid': satID_res[0][0], 'sensorid': senID_res[0][0]})
        records = DataFrame(records, columns=['filename', 'sceneid', 'acquisitiondate', 'geom'])
        df = df.merge(records, on='filename', how="outer")

        # separate records with valid matches in database from invalid matches (filename not found in database)
        df_recs = df[df.sceneid.notnull()].copy()  # creates a copy (needed to be able to apply maps later)
        df_miss = df[df.sceneid.isnull()]  # creates a view

        # convert scene ids from floats to integers
        df_recs['sceneid'] = list(df_recs.sceneid.map(lambda sceneid: int(sceneid)))

        # wkb_hex bounds to shapely polygons
        df_recs['polygons'] = list(df_recs.geom.map(lambda wkb_hex: wkb_loads(wkb_hex, hex=True)))

        return df_recs, df_miss

    def create(self):
        # type: () -> int
        """
        Add the job to the 'jobs' table of the database
        :return:  <int> the job ID of the newly created job
        """

        if not self.dataframe.empty:
            all_sat, all_sen = \
                zip(*[i.split('__') for i in
                      (np.unique(self.dataframe['satellite'] + '__' + self.dataframe['sensor']))])
            counts = [self.dataframe[(self.dataframe['satellite'] == sat) &
                                     (self.dataframe['sensor'] == sen)]['sceneid'].count()
                      for sat, sen in zip(all_sat, all_sen)]
            self.scene_counts = {'%s %s' % (sat, sen): cnt for sat, sen, cnt in zip(all_sat, all_sen, counts)}
            self.statistics = [len(self.sceneids)] + [0] * 8

            db_entry = self.db_entry
            del db_entry['id']

            newID = create_record_in_postgreSQLdb(self.conn, 'jobs', db_entry)
            assert isinstance(newID, int)

            SatSen_CountTXT = ['%s %s %s scene' % (cnt, sat, sen) if cnt == 1 else '%s %s %s scenes' % (cnt, sat, sen)
                               for sat, sen, cnt in zip(all_sat, all_sen, counts)]
            print('New job created successfully. job-ID: %s\nThe job contains:' % newID)
            [print('\t- %s' % txt) for txt in SatSen_CountTXT]

            self.exists_in_db = True
            self.id = newID
            return self.id
        else:
            print('No job created because no matching scene could be found in database!')

    def update_db_entry(self):
        """Updates the all values of current database entry belonging to the respective job ID. New values are taken
        from the attributes of the GMS_JOB instance.
        """

        assert self.exists_in_db
        db_entry = self.db_entry
        del db_entry['id']  # primary key of the record cannot be overwritten
        update_records_in_postgreSQLdb(self.conn, 'jobs', db_entry, {'id': self.id})

    def delete_procdata_of_failed_sceneIDs(self, proc_level='all', force=False):
        """Deletes all data where processing failed within the current job ID.

        :param proc_level:  <str> delete only results that have the given processing level
        :param force:
        """

        self.__delete_procdata(self.failed_sceneids, 'failed', proc_level=proc_level, force=force)

    def delete_procdata_of_entire_job(self, proc_level='all', force=False):
        """Deletes all scene data processed by the current job ID.

        :param proc_level:  <str> delete only results that have the given processing level
        :param force:
        """

        self.__delete_procdata(self.sceneids, 'processed', proc_level=proc_level, force=force)

    def __delete_procdata(self, list_sceneIDs, scene_desc, proc_level='all', force=False):
        """Applies delete_processing_results on each scene given in list_sceneIDs.

        :param list_sceneIDs:  <list> a list of scene IDs
        :param scene_desc:     <str> a description like 'succeeded' or 'failed'
        :param proc_level:     <str> delete only results that have the given processing level
        :param force:
        """

        if self.exists_in_db:
            if list_sceneIDs:
                delete = 'J'
                if not force:
                    delete = input("Do you really want to delete the processing results of %s scenes? (J/n)"
                                   % len(list_sceneIDs))
                if delete == 'J':
                    [delete_processing_results(ScID, proc_level=proc_level, force=force) for ScID in list_sceneIDs]
            else:
                warnings.warn(
                    '\nAccording to the database the job has no %s scene IDs. Nothing to delete.' % scene_desc)
        else:
            warnings.warn('The job with the ID %s does not exist in the database. Thus there are no %s scene IDs.'
                          % (scene_desc, self.id))


def delete_processing_results(scene_ID, proc_level='all', force=False):
    """Deletes the processing results of a given scene ID

    :param scene_ID:    <int> the scene ID to delete results from
    :param proc_level:  <str> delete only results that have the given processing level
    :param force:       <bool> force deletion without user interaction
    """

    if proc_level not in ['all'] + proc_chain:
        raise ValueError("'%s' is not a supported processing level." % proc_level)

    path_procdata = PG.path_generator(scene_ID=scene_ID).get_path_procdata()
    if not os.path.isdir(path_procdata):
        print('The folder %s does not exist. Nothing to delete.' % path_procdata)
    else:
        delete = 'J'
        if not force:
            dir_list = os.listdir(path_procdata) if proc_level == 'all' else \
                glob.glob(os.path.join(path_procdata, '*%s*' % proc_level))
            count_files = len([i for i in dir_list if os.path.isfile(os.path.join(path_procdata, i))])
            count_dirs = len([i for i in dir_list if os.path.isdir(os.path.join(path_procdata, i))])
            if count_files or count_dirs:
                delete = input("Do you really want to delete the folder %s? It contains %s files and %s directories"
                               " to delete. (J/n)" % (path_procdata, count_files, count_dirs))
            else:
                print('The folder %s does not not contain any files that match the given deletion criteria. '
                      'Nothing to delete.' % path_procdata)
        if delete == 'J':
            try:
                if proc_level == 'all':
                    try:
                        shutil.rmtree(path_procdata)
                    except OSError:  # directory not deletable because it is not empty
                        if [F for F in os.listdir(path_procdata) if not os.path.basename(F).startswith('.fuse_hidden')]:
                            raise  # raise OSError if there are other files than .fuse_hidden... remaining
                else:
                    files2delete = glob.glob(os.path.join(path_procdata, '*%s*' % proc_level))
                    errors = False  # default
                    for F in files2delete:
                        try:
                            os.remove(F)
                        except OSError:
                            if not os.path.basename(F).startswith('.fuse_hidden'):
                                errors = True
                    if errors:
                        raise OSError('Not all files deleted properly.')

            except OSError:
                msg = '\nNot all files of scene %s could be deleted properly. Remaining files:\n%s\n\nThe following ' \
                      'error occurred:\n%s' % (scene_ID, '\n'.join(os.listdir(path_procdata)), traceback.format_exc())
                warnings.warn(msg)


def add_externally_downloaded_data_to_GMSDB(conn_DB, src_folder, filenames, satellite, sensor):
    # type: (str,str,list,str,str) -> None
    """Adds externally downloaded satellite scenes to GMS fileserver AND updates the corresponding postgreSQL records
    by adding a filename and setting the processing level to 'DOWNLOADED'.:

    :param conn_DB:     <str> pgSQL database connection parameters
    :param src_folder:  <str> the source directory where externally provided archive files are saved
    :param filenames:   <list> a list of filenames to be added to the GMS database
    :param satellite:   <str> the name of the satellite to which the filenames are belonging
    :param sensor:      <str> the name of the sensor to which the filenames are belonging
    """

    # FIXME this method only works for Landsat archives or if filename is already set in database
    # FIXME (not always the case for S2A)!
    res = [get_entityIDs_from_filename(conn_DB, fName) for fName in filenames]
    entityIDs = list(itertools.chain.from_iterable(res))

    sceneID_fName_arr = get_notDownloadedsceneIDs(conn_DB, entityIDs, satellite, sensor, src_folder)

    files2copy = list(set(sceneID_fName_arr[:, 1]))
    target_folder = os.path.join(CFG.path_archive, satellite, sensor)
    assert os.path.exists(target_folder), 'Target folder not found: %s.' % target_folder
    print('Copying %s files to %s.' % (len(files2copy), target_folder))

    for i in range(sceneID_fName_arr.shape[0]):
        sceneID, fName = sceneID_fName_arr[i, :]
        src_P = os.path.join(src_folder, fName)
        if os.path.exists(os.path.join(target_folder, os.path.basename(src_P))):
            print("File '%s' already exists in the target folder. Skipped." % os.path.basename(src_P))
        else:
            print('copying %s...' % src_P)
            shutil.copy(src_P, target_folder)

        print("Setting proc_level for scene ID '%s' to 'DOWNLOADED' and adding filename..." % sceneID)
        update_records_in_postgreSQLdb(conn_DB, 'scenes', {'filename': fName, 'proc_level': 'DOWNLOADED'},
                                       {'id': sceneID})


def add_missing_filenames_in_pgSQLdb(conn_params):  # FIXME
    res = get_info_from_postgreSQLdb(conn_params, 'scenes', ['id', 'entityid', 'satelliteid', 'sensorid', 'filename'],
                                     {'filename': None, 'proc_level': 'DOWNLOADED', 'sensorid': 8}, timeout=120000)
    gdf = GeoDataFrame(res, columns=['sceneid', 'entityid', 'satelliteid', 'sensorid', 'filename'])

    def get_fName(sceneid): return PG.path_generator(scene_ID=sceneid).get_local_archive_path_baseN()

    def get_fName_if_exists(path): return os.path.basename(path) if os.path.exists(path) else None

    gdf['archive_path'] = list(gdf['sceneid'].map(get_fName))
    gdf['filename'] = list(gdf['archive_path'].map(get_fName_if_exists))

    print(gdf)


def pdDataFrame_to_sql_k(engine, frame, name, if_exists='fail', index=True,
                         index_label=None, schema=None, chunksize=None, dtype=None, **kwargs):
    # type: (any,pd.DataFrame,str,str,bool,str,str,int,dict,any) -> None
    """Extends the standard function pandas.io.SQLDatabase.to_sql() with 'kwargs' which allows to set the primary key
    of the target table for example. This is usually not possible with the standard to_sql() function.

    :param engine:      SQLAlchemy engine (created by sqlalchemy.create_engine)
    :param frame:       the pandas.DataFrame or geopandas.GeoDataFrame to be exported to SQL-like database
    :param name:        <str> Name of SQL table
    :param if_exists:   <str> {'fail', 'replace', 'append'} the action to be executed if target table already exists
    :param index:       <bool> Write DataFrame index as a column.
    :param index_label: <str> Column label for index column(s).
    :param schema:      <str> Specify the schema (if database flavor supports this). If None, use default schema.
    :param chunksize:   <int> If not None, then rows will be written in batches of this size at a time.
                        If None, all rows will be written at once.
    :param dtype:       <dict> a dictionary of column names and corresponding postgreSQL types
                        The types should be a SQLAlchemy or GeoSQLAlchemy2 type,
    :param kwargs:      keyword arguments to be passed to SQLTable
    """

    pandas_sql = pandasSQL_builder(engine, schema=None, flavor=None)
    if dtype is not None:
        for col, my_type in dtype.items():
            if not isinstance(to_instance(my_type), TypeEngine):
                raise ValueError('The type of %s is not a SQLAlchemy type ' % col)

    table = SQLTable(name, pandas_sql, frame=frame, index=index, if_exists=if_exists, index_label=index_label,
                     schema=schema, dtype=dtype, **kwargs)
    table.create()
    table.insert(chunksize)


def import_shapefile_into_postgreSQL_database(path_shp, tablename, cols2import=None, dtype_dic=None,
                                              if_exists='fail', index_label=None, primarykey=None):
    # type: (str,str,list,dict,str,str,str) -> None
    """Imports all features of shapefile into the specified table of the postgreSQL database. Geometry is automatically
    converted to postgreSQL geometry data type.
    :param path_shp:    <str> path of the shapefile to be imported
    :param tablename:   <str> name of the table within the postgreSQL database where records shall be added
    :param cols2import: <list> a list of column names to be imported
    :param dtype_dic:   <dict> a dictionary of column names and corresponding postgreSQL types
                        The types should be a SQLAlchemy or GeoSQLAlchemy2 type,
                        or a string for sqlite3 fallback connection.
    :param if_exists:   <str> {'fail', 'replace', 'append'} the action to be executed if target table already exists
    :param index_label: <str> Column label for index column(s).
    :param primarykey:  <str> the name of the column to be set as primary key of the target table
    """

    print('Reading shapefile %s...' % path_shp)
    GDF = GeoDataFrame.from_file(path_shp)
    GDF['geom'] = list(GDF['geometry'].map(str))
    # GDF['geom'] = [*GDF['geometry'].map(lambda shapelyPoly: "'SRID=4326;%s'::geometry" %shapelyPoly)]
    # GDF['geom'] = [*GDF['geometry'].map(lambda shapelyPoly: "'SRID=4326;%s'" % shapelyPoly)]
    # GDF['geom'] = [*GDF['geometry'].map(lambda shapelyPoly: shapelyPoly.wkb_hex)]
    # GDF['geom'] = [*GDF['geometry'].map(lambda shapelyPoly: str(from_shape(shapelyPoly, srid=4326)))]
    # from geoalchemy2.shape import from_shape

    cols2import = cols2import + ['geom'] if cols2import else list(GDF.columns)
    subGDF = GDF[cols2import]
    dtype_dic = dtype_dic if dtype_dic else {}
    dtype_dic.update({'geom': GEOMETRY})
    # import geoalchemy2
    # dtype_dic.update({'geom': geoalchemy2.types.Geometry(geometry_type='POLYGON',srid=4326)})
    print('Adding shapefile geometries to postgreSQL table %s...' % tablename)
    engine = create_engine('postgresql://gmsdb:gmsdb@%s/geomultisens' % CFG.db_host)
    pdDataFrame_to_sql_k(engine, subGDF, tablename, index_label=index_label,
                         keys=primarykey, if_exists=if_exists, dtype=dtype_dic)
    # set SRID
    conn = psycopg2.connect(CFG.conn_database)
    cursor = conn.cursor()
    cursor.execute("UPDATE %s SET geom  = ST_SetSRID(geom, 4326);" % tablename)
    conn.commit()
    cursor.close()
    conn.close()


def data_DB_updater(obj_dict):
    # type: (dict) -> None
    """Updates the table "scenes_proc" or "mgrs_tiles_proc within the postgreSQL database
    according to the given dictionary of a GMS object.

    :param obj_dict:    <dict> a copy of the dictionary of the respective GMS object
    """

    assert isinstance(obj_dict, dict), 'The input for data_DB_updater() has to be a dictionary.'

    def list2str(list2convert): return ''.join([str(val) for val in list2convert])

    connection = psycopg2.connect(CFG.conn_database)
    if connection is None:
        print('Database connection could not be established. Database entry could not be created or updated.')
    else:
        if obj_dict['arr_shape'] != 'MGRS_tile':
            table2update = 'scenes_proc'
            dict_dbkey_objkey = {'sceneid': obj_dict['scene_ID'],
                                 'georef': True if obj_dict['georef'] else False,
                                 'proc_level': obj_dict['proc_level'],
                                 'layer_bands_assignment': ''.join(obj_dict['LayerBandsAssignment']),
                                 'bounds': Polygon(obj_dict['trueDataCornerLonLat'])}

            matchExp = 'WHERE ' + get_postgreSQL_matchingExp('sceneid', dict_dbkey_objkey['sceneid'])
            keys2update = ['georef', 'proc_level', 'layer_bands_assignment', 'bounds']

        else:  # MGRS_tile
            table2update = 'mgrs_tiles_proc'

            def get_tile_bounds_box(bnds): return box(bnds[0], bnds[2], bnds[1], bnds[3])
            dict_dbkey_objkey = {'sceneid': obj_dict['scene_ID'],
                                 'scenes_proc_id': obj_dict['scenes_proc_ID'],
                                 'mgrs_code': obj_dict['MGRS_info']['tile_ID'],
                                 'virtual_sensor_id': CFG.virtual_sensor_id,
                                 'proc_level': obj_dict['proc_level'],
                                 'coreg_success': obj_dict['coreg_info']['success'],
                                 'tile_bounds': get_tile_bounds_box(obj_dict['bounds_LonLat']),
                                 'data_corners': Polygon(obj_dict['trueDataCornerLonLat'])}

            matchExp = 'WHERE ' + ' AND '.join([get_postgreSQL_matchingExp(k, dict_dbkey_objkey[k])
                                                for k in ['sceneid', 'mgrs_code', 'virtual_sensor_id']])
            keys2update = ['scenes_proc_id', 'proc_level', 'coreg_success', 'tile_bounds', 'data_corners']
            if obj_dict['scenes_proc_ID'] is None:
                keys2update.remove('scenes_proc_id')

        cursor = connection.cursor()

        # check if record exists
        execute_pgSQL_query(cursor, "SELECT EXISTS(SELECT 1 FROM %s %s)" % (table2update, matchExp))

        # create new entry
        if cursor.fetchone()[0] == 0:
            keys, vals = zip(*[(k, str(get_postgreSQL_value(v))) for k, v in dict_dbkey_objkey.items()])
            execute_pgSQL_query(cursor,
                                "INSERT INTO %s (%s) VALUES (%s);" % (table2update, ','.join(keys), ','.join(vals)))
        # or update existing entry
        else:
            setExp = 'SET ' + ','.join(
                ['%s=%s' % (k, get_postgreSQL_value(dict_dbkey_objkey[k])) for k in keys2update])
            execute_pgSQL_query(cursor, "UPDATE %s %s %s;" % (table2update, setExp, matchExp))

    if 'connection' in locals():
        connection.commit()
        connection.close()


def postgreSQL_table_to_csv(conn_db, path_csv, tablename):
    # GeoDataFrame.to_csv(path_csv, index_label='id')
    raise NotImplementedError  # TODO


def archive_exists_on_fileserver(conn_DB, entityID):
    # type: (str,str) -> bool
    """Queries the postgreSQL database for the archive filename of the given entity ID and checks if the
    corresponding archive file exists in the archive folder.

    :param conn_DB:     <str> pgSQL database connection parameters
    :param entityID:    <str> entity ID to be checked
    """

    records = get_info_from_postgreSQLdb(conn_DB, 'scenes', ['satelliteid', 'sensorid'], {'entityid': entityID})
    records_filt = [rec for rec in records if rec[0] is not None and rec[1] is not None]
    if len(records_filt) == 1:
        satID, senID = records_filt[0]
        satellite = get_info_from_postgreSQLdb(conn_DB, 'satellites', ['name'], {'id': satID})[0][0]
        sensor = get_info_from_postgreSQLdb(conn_DB, 'sensors', ['name'], {'id': senID})[0][0]
        sensor = sensor if sensor != 'ETM+_SLC_OFF' else 'ETM+'  # join sensors 'ETM+' and 'ETM+_SLC_OFF'
        archive_fold = os.path.join(CFG.path_archive, satellite, sensor)
        assert os.path.exists(archive_fold), 'Archive folder not found: %s.' % archive_fold

        if re.search(r'Landsat', satellite, re.I):
            exists = os.path.exists(os.path.join(archive_fold, entityID + '.tar.gz'))
        else:
            raise NotImplementedError
    elif len(records_filt) == 0:
        warnings.warn("No database record found for entity ID '%s'. Dataset skipped." % entityID)
        exists = False
    else:
        warnings.warn("More than one database records found for entity ID '%s'. Dataset skipped." % entityID)
        exists = False

    return exists


def record_stats_memusage(conn_db, GMS_obj):
    # type: (str, GMS_object) -> bool
    if list(sorted(GMS_obj.mem_usage.keys())) != ['L1A', 'L1B', 'L1C', 'L2A', 'L2B', 'L2C']:
        GMS_obj.logger.info('Unable to record memory usage statistics because statistics are missing for some '
                            'processing levels. ')
        return False

    vals2write_dict = dict(
        creationtime=datetime.now(),
        software_version=CFG.version,
        datasetid=GMS_obj.dataset_ID,
        virtual_sensor_id=CFG.virtual_sensor_id,
        target_gsd=CFG.target_gsd[0],  # respects only xgsd
        target_nbands=len(CFG.target_CWL),
        inmem_serialization=CFG.inmem_serialization,
        target_radunit_optical=CFG.target_radunit_optical,
        skip_coreg=CFG.skip_coreg,
        ac_estimate_accuracy=CFG.ac_estimate_accuracy,
        ac_bandwise_accuracy=CFG.ac_bandwise_accuracy,
        spathomo_estimate_accuracy=CFG.spathomo_estimate_accuracy,
        spechomo_estimate_accuracy=CFG.spechomo_estimate_accuracy,
        spechomo_bandwise_accuracy=CFG.spechomo_bandwise_accuracy,
        parallelization_level=CFG.parallelization_level,
        skip_thermal=CFG.skip_thermal,
        skip_pan=CFG.skip_pan,
        mgrs_pixel_buffer=CFG.mgrs_pixel_buffer,
        cloud_masking_algorithm=CFG.cloud_masking_algorithm[GMS_obj.satellite],
        used_mem_l1a=GMS_obj.mem_usage['L1A'],
        used_mem_l1b=GMS_obj.mem_usage['L1B'],
        used_mem_l1c=GMS_obj.mem_usage['L1C'],
        used_mem_l2a=GMS_obj.mem_usage['L2A'],
        used_mem_l2b=GMS_obj.mem_usage['L2B'],
        used_mem_l2c=GMS_obj.mem_usage['L2C'],
        dims_x_l2a=GMS_obj.arr.cols,
        dims_y_l2a=GMS_obj.arr.rows,
        is_test=CFG.is_test,
        sceneid=GMS_obj.scene_ID
    )

    # get all existing database records matching the respective config
    # NOTE: those columns that do not belong the config specification are ignored
    vals2get = list(vals2write_dict.keys())
    df_existing_recs = pd.DataFrame(
        get_info_from_postgreSQLdb(conn_db, 'stats_mem_usage_homo',
                                   vals2return=vals2get,
                                   cond_dict={k: v for k, v in vals2write_dict.items()
                                              if k not in ['creationtime', 'used_mem_l1a', 'used_mem_l1b',
                                                           'used_mem_l1c', 'used_mem_l2a', 'used_mem_l2b',
                                                           'used_mem_l2c', 'dims_x_l2a', 'dims_y_l2b', 'sceneid']}),
        columns=vals2get)

    # filter the existing records by gms_preprocessing software version number
    # (higher than CFG.min_version_mem_usage_stats)
    vers = list(df_existing_recs.software_version)
    vers_usable = [ver for ver in vers if parse_version(ver) >= parse_version(CFG.min_version_mem_usage_stats)]
    df_existing_recs_usable = df_existing_recs.loc[df_existing_recs.software_version.isin(vers_usable)]

    # add memory stats to database
    # (but skip if there are already 10 records matching the respective config and software version number
    #  or if the current scene ID is already among the matching records)
    if len(df_existing_recs_usable) < 10 and GMS_obj.scene_ID not in list(df_existing_recs_usable.sceneid):
        create_record_in_postgreSQLdb(conn_db, 'stats_mem_usage_homo', vals2write_dict=vals2write_dict)
        return True
    else:
        return False
