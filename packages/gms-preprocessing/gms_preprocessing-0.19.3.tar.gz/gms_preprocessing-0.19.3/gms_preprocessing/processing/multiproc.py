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


from multiprocessing import Pool, current_process
from itertools import chain

from ..options.config import GMS_config as CFG

__author__ = 'Daniel Scheffler'


def MAP(func, args, CPUs=None, flatten_output=False):
    # type: (any, list, int, bool) -> list
    """Parallelize the execution of the given function.
    NOTE: if Job.CPUs in config is 1, execution is not parallelized.

    :param func:            function to parallelize
    :param args:            function arguments
    :param CPUs:            number of CPUs to use
    :param flatten_output:  whether to flatten output list,
                            e.g. [ [ Tile1Scene1, Tile2Scene1], Tile1Scene2, Tile2Scene2] to
                            [ Tile1Scene1, Tile2Scene1, Tile1Scene2, Tile2Scene2 ]
    """

    CPUs = CPUs or CFG.CPUs
    CPUs = CPUs if CPUs <= CFG.CPUs else CFG.CPUs  # treat CFG.CPUs as maximum number of CPUs

    if CPUs and CPUs > 1 and len(args) > 1:
        with Pool(CPUs) as pool:
            results = pool.map(func, args)  # always returns a list
    else:
        results = [func(argset) for argset in args]  # generator does not always work properly here

    if flatten_output:
        try:
            ch = chain.from_iterable(results)
            return list(ch)
        except TypeError:  # if elements of chain are not iterable
            ch = chain.from_iterable([results])
            return list(ch)
    else:
        return results


def imap_unordered(func, args, CPUs=None, flatten_output=False):
    # type: (any, list, int, bool) -> list
    """Parallelize the execution of the given function.
    NOTE: if Job.CPUs in config is 1, execution is not parallelized.

    :param func:            function to parallelize
    :param args:            function arguments
    :param CPUs:            number of CPUs to use
    :param flatten_output:  whether to flatten output list,
                            e.g. [ [ Tile1Scene1, Tile2Scene1], Tile1Scene2, Tile2Scene2] to
                            [ Tile1Scene1, Tile2Scene1, Tile1Scene2, Tile2Scene2 ]
    """

    CPUs = CPUs or CFG.CPUs
    CPUs = CPUs if CPUs <= CFG.CPUs else CFG.CPUs  # treat CFG.CPUs as maximum number of CPUs

    if CPUs and CPUs > 1 and len(args) > 1:
        with Pool(CPUs) as pool:
            results = list(pool.imap_unordered(func, args))  # returns an iterator
    else:
        results = [func(argset) for argset in args]  # generator does not always work properly here

    if flatten_output:
        try:
            ch = chain.from_iterable(results)
            return list(ch)
        except TypeError:  # if elements of chain are not iterable
            ch = chain.from_iterable([results])
            return list(ch)
    else:
        return list(results)


def is_mainprocess():
    # type: () -> bool
    """Return True if the current process is the main process and False if it is a multiprocessing child process."""
    return current_process().name == 'MainProcess'
