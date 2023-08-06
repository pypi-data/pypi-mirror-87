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

"""Level 2C Processor:  Quality layers"""

import numpy as np
from collections import OrderedDict

from geoarray import GeoArray

from ..misc.definition_dicts import bandslist_all_errors, get_outFillZeroSaturated
from .L2B_P import L2B_object
from ..options.config import GMS_config as CFG

__author__ = 'Daniel Scheffler'


class L2C_object(L2B_object):
    def __init__(self, L2B_obj=None):
        super(L2C_object, self).__init__()

        if L2B_obj:
            # populate attributes
            [setattr(self, key, value) for key, value in L2B_obj.__dict__.items()]

        self.proc_level = 'L2C'
        self.proc_status = 'initialized'


class AccuracyCube(GeoArray):
    def __init__(self, GMS_obj):
        self._GMS_obj = GMS_obj

        # privates
        self._layers = None

        if self.layers:
            GMS_obj.logger.info('Generating combined accuracy layers array..')
            super(AccuracyCube, self).__init__(self.generate_array(),
                                               geotransform=list(self.layers.values())[0].gt,
                                               projection=list(self.layers.values())[0].prj,
                                               bandnames=self.get_bandnames(),
                                               nodata=get_outFillZeroSaturated('int16')[0])

        else:
            raise ValueError('The given GMS_object contains no accuracy layers for combination.')

    @property
    def layers(self):
        # type: () -> OrderedDict
        if not self._layers:
            errs = OrderedDict((band, getattr(self._GMS_obj, band)) for band in bandslist_all_errors)
            self._layers = \
                OrderedDict((band, err) for band, err in errs.items() if isinstance(err, (np.ndarray, GeoArray)))

        return self._layers

    def get_bandnames(self):
        bandnames = []
        for errArrName, errArr in self.layers.items():
            if errArrName == 'ac_errors':
                if CFG.ac_bandwise_accuracy:
                    bandnames.extend(['AC errors %s' % bN for bN in errArr.bandnames])
                else:
                    bandnames.append('median of AC errors')

            elif errArrName == 'mask_clouds_confidence':
                bandnames.append('confidence of cloud mask')

            elif errArrName == 'spat_homo_errors':
                bandnames.append('shift reliability percentage')

            elif errArrName == 'spec_homo_errors':
                if CFG.spechomo_bandwise_accuracy:
                    bandnames.extend(['error of spectral homogenization %s' % bN for bN in errArr.bandnames])
                else:
                    bandnames.append('median error of spectral homogenization')

            else:
                raise RuntimeError('Error setting bandnames for %s.' % errArrName)

        return bandnames

    def generate_array(self):
        err_layers = self.layers.copy()  # copy OrdDict, otherwise attributes of GMS_object are overwritten

        # validate dimensionality of ac_errors array
        if 'ac_errors' in err_layers and not CFG.ac_bandwise_accuracy:
            assert err_layers['ac_errors'].ndim == 2, "Received a 3D 'ac_errors' array although CFG.ac_bandwise " \
                                                      "accuracy is False."

        # # validate dimensionality of spec_homo_errors array
        if 'spec_homo_errors' in err_layers and not CFG.spechomo_bandwise_accuracy:
            assert err_layers['spec_homo_errors'].ndim == 2, "Received a 3D 'spec_homo_errors' array although " \
                                                             "CFG.spechomo_bandwise_accuracy is False."

        # stack all accuracy layers together
        accArr = np.dstack(list(err_layers.values())).astype('int16')

        # apply int16 nodata value
        accArr[self._GMS_obj.arr.mask_nodata.astype(np.int8) == 0] = get_outFillZeroSaturated('int16')[0]

        return accArr
