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
import sklearn  # noqa # avoids a static TLS ImportError during runtime of SICOR (when importing sklearn there)
if 'MPLBACKEND' not in os.environ:
    os.environ['MPLBACKEND'] = 'Agg'

from . import algorithms  # noqa: E402
from . import io  # noqa: E402
from . import misc  # noqa: E402
from . import processing  # noqa: E402
from . import options  # noqa: F401 (imported but unused)
from .options import config  # noqa: F401 (imported but unused)
from .options.config import set_config  # noqa: F401 (imported but unused)
from .processing.process_controller import ProcessController  # noqa: E402
from .version import __version__, __versionalias__   # noqa (E402 + F401)

__author__ = """Daniel Scheffler"""
__email__ = 'daniel.scheffler@gfz-potsdam.de'
__all__ = ['__version__',
           '__versionalias__',
           'algorithms',
           'io',
           'misc',
           'processing',
           'config'  # noqa - only to keep compatibility with HU-INF codes
           'options',
           'set_config',
           'ProcessController',
           ]
