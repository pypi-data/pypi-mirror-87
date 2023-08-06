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

import shapely
from py_tools_ds.geo.coord_trafo import reproject_shapelyGeometry
from shapely.geometry import Polygon

from gms_preprocessing.options.config import GMS_config as CFG
from gms_preprocessing.misc import database_tools as DB_T
from gms_preprocessing.misc import helper_functions as HLP_F
from gms_preprocessing.algorithms import geoprocessing as GEOP

__author__ = 'Daniel Scheffler'


class MGRS_tile(object):
    def __init__(self, tile_ID=''):
        """

        :param tile_ID: <str> 5 digit tile ID, e.g. 32UUU
        """
        self._tile_ID = ''
        self._geom_wkb = ''
        self._poly_lonlat = Polygon()

        if tile_ID:
            self.tile_ID = tile_ID

    @property
    def tile_ID(self):
        return self._tile_ID

    @tile_ID.setter
    def tile_ID(self, tile_ID):
        assert isinstance(tile_ID, str) and len(tile_ID) == 5, \
            "'tile_ID' must be a 5 digit string code. Got %s." % tile_ID
        self._tile_ID = tile_ID

        res = DB_T.get_info_from_postgreSQLdb(CFG.conn_database, 'mgrs_tiles', ['geom'],
                                              {'grid1mil': self.grid1mil, 'grid100k': self.grid100k}, timeout=20000)
        assert res, "The tile ID '%s' does not exist in the database." % tile_ID

        self.geom_wkb = res[0][0]

    @property
    def grid1mil(self):
        return self.tile_ID[:3]

    @property
    def grid100k(self):
        return self.tile_ID[-2:]

    @property
    def UTMzone(self):
        return int(self.tile_ID[:2])

    @property
    def EPSG(self):
        is_south = self.poly_lonlat.centroid.xy[1][0] < 0
        return int(('327' if is_south else '326') + str(self.UTMzone))

    @property
    def geom_wkb(self):
        return self._geom_wkb

    @geom_wkb.setter
    def geom_wkb(self, geom_wkb):
        # FIXME should check whether geom_wkb is a valid geometry according to db
        self._geom_wkb = geom_wkb

    @property
    def poly_lonlat(self):
        return shapely.wkb.loads(self.geom_wkb, hex=True)

    @property
    def poly_utm(self):
        return reproject_shapelyGeometry(self.poly_lonlat, 4326, self.EPSG)

    def poly_specPrj(self, prj):
        """Returns a shapely.Polygon in a specific projection.

        :param prj: <str> WKT string of the target projection
        """
        return reproject_shapelyGeometry(self.poly_lonlat, 4326, prj)

    def get_bounds(self, prj=None):
        return self.poly_lonlat.bounds if not prj else self.poly_specPrj(prj).bounds  # xmin, ymin, xmax, ymax

    def to_image_bounds(self, im_prj, im_gt, arr_shape, pixbuffer=0, ensure_valid_coords=True):
        xmin, xmax, ymin, ymax = HLP_F.get_arrSubsetBounds_from_shapelyPolyLonLat(arr_shape, self.poly_lonlat, im_gt,
                                                                                  im_prj, pixbuffer,
                                                                                  ensure_valid_coords)
        return xmin, xmax, ymin, ymax

    def clip_array_using_mgrsBounds(self, array, im_prj, im_gt, nodataVal=0, pixbuffer=0):
        """

        :param array:
        :param im_prj:
        :param im_gt:
        :param nodataVal:
        :param pixbuffer:      <float> an optional buffer size (image pixel units)
        """

        buffMap = im_gt[1] * pixbuffer
        mgrs_bounds = self.poly_specPrj(im_prj).buffer(buffMap).bounds
        tgt_arr, tgt_gt, im_prj = GEOP.clip_array_using_mapBounds(array, mgrs_bounds, im_prj, im_gt, nodataVal)

        return tgt_arr, tgt_gt, im_prj
