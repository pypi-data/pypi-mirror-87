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
Level 2B Processor: Spectral homogenization
"""

import numpy as np
from typing import Union  # noqa F401  # flake8 issue
from geoarray import GeoArray  # noqa F401  # flake8 issue
from spechomo.prediction import SpectralHomogenizer

from ..options.config import GMS_config as CFG
from ..misc.definition_dicts import datasetid_to_sat_sen, sat_sen_to_datasetid
from ..model.metadata import get_LayerBandsAssignment
from .L2A_P import L2A_object
from ..model.gms_object import GMS_identifier

__author__ = 'Daniel Scheffler'


class L2B_object(L2A_object):
    def __init__(self, L2A_obj=None):

        super(L2B_object, self).__init__()

        if L2A_obj:
            # populate attributes
            [setattr(self, key, value) for key, value in L2A_obj.__dict__.items()]

        self.proc_level = 'L2B'
        self.proc_status = 'initialized'

    def spectral_homogenization(self):
        """Apply spectral homogenization, i.e., prediction of the spectral bands of the target sensor."""
        #################################################################
        # collect some information specifying the needed homogenization #
        #################################################################

        method = CFG.spechomo_method
        src_dsID = sat_sen_to_datasetid(self.satellite, self.sensor)
        src_cwls = [float(self.MetaObj.CWL[bN]) for bN in self.MetaObj.LayerBandsAssignment]
        # FIXME exclude or include thermal bands; respect sorted CWLs in context of LayerBandsAssignment
        tgt_sat, tgt_sen = datasetid_to_sat_sen(CFG.datasetid_spectral_ref)
        # NOTE: get target LBA at L2A, because spectral characteristics of target sensor do not change after AC
        tgt_gmsid_kw = dict(satellite=tgt_sat,
                            sensor=tgt_sen,
                            subsystem='',
                            image_type='RSD',
                            dataset_ID=src_dsID,
                            logger=None)
        tgt_LBA = get_LayerBandsAssignment(GMS_identifier(proc_level='L2A', **tgt_gmsid_kw))

        if CFG.datasetid_spectral_ref is None:
            tgt_cwl = CFG.target_CWL
            tgt_fwhm = CFG.target_FWHM
        else:
            # exclude those bands from CFG.target_CWL and CFG.target_FWHM that have been removed after AC
            full_LBA = get_LayerBandsAssignment(GMS_identifier(proc_level='L1A', **tgt_gmsid_kw),
                                                no_thermal=True,
                                                no_pan=False,
                                                return_fullLBA=True,
                                                sort_by_cwl=True,
                                                proc_level='L1A')
            tgt_cwl = [dict(zip(full_LBA, CFG.target_CWL))[bN] for bN in tgt_LBA]
            tgt_fwhm = [dict(zip(full_LBA, CFG.target_FWHM))[bN] for bN in tgt_LBA]

        ####################################################
        # special cases where homogenization is not needed #
        ####################################################

        if self.dataset_ID == CFG.datasetid_spectral_ref:
            self.logger.info("Spectral homogenization has been skipped because the dataset id equals the dataset id of "
                             "the spectral reference sensor.")
            return

        if src_cwls == CFG.target_CWL or (self.satellite == tgt_sat and self.sensor == tgt_sen):
            # FIXME catch the case if LayerBandsAssignments are unequal with np.take
            self.logger.info("Spectral homogenization has been skipped because the current spectral characteristics "
                             "are already equal to the target sensor's.")
            return

        #################################################
        # perform spectral homogenization of image data #
        #################################################

        from ..processing.multiproc import is_mainprocess
        SpH = SpectralHomogenizer(classifier_rootDir=CFG.path_spechomo_classif,
                                  logger=self.logger,
                                  CPUs=CFG.CPUs if is_mainprocess() else 1)

        if method == 'LI' or CFG.datasetid_spectral_ref is None or self.arr_desc != 'BOA_Ref':
            # linear interpolation (if intended by user or in case of custom spectral characteristics of target sensor)
            # -> no classifier for that case available -> linear interpolation
            if self.arr_desc != 'BOA_Ref' and CFG.target_radunit_optical == 'BOA_Ref':
                self.logger.warning("Spectral homogenization with an '%s' classifier is not possible because the input "
                                    "image is not atmospherically corrected (BOA reflectance is needed). Falling back "
                                    "to linear spectral interpolation." % method)

            im = SpH.interpolate_cube(self.arr, src_cwls, tgt_cwl, kind='linear')

            if CFG.spechomo_estimate_accuracy:
                self.logger.warning("Unable to compute any error information in case spectral homogenization algorithm "
                                    "is set to 'LI' (Linear Interpolation).")

            errs = None

        else:
            # a known sensor has been specified as spectral reference => apply a machine learner
            im, errs = SpH.predict_by_machine_learner(self.arr,
                                                      method=method,
                                                      src_satellite=self.satellite,
                                                      src_sensor=self.sensor,
                                                      src_LBA=self.LayerBandsAssignment,
                                                      tgt_satellite=tgt_sat,
                                                      tgt_sensor=tgt_sen,
                                                      tgt_LBA=tgt_LBA,
                                                      n_clusters=CFG.spechomo_n_clusters,
                                                      classif_alg=CFG.spechomo_classif_alg,
                                                      kNN_n_neighbors=CFG.spechomo_kNN_n_neighbors,
                                                      src_nodataVal=self.arr.nodata,
                                                      out_nodataVal=self.arr.nodata,
                                                      compute_errors=CFG.spechomo_estimate_accuracy,
                                                      bandwise_errors=CFG.spechomo_bandwise_accuracy,
                                                      fallback_argskwargs=dict(
                                                          arrcube=self.arr,
                                                          source_CWLs=src_cwls,
                                                          target_CWLs=tgt_cwl,
                                                          kind='linear')
                                                      )

        ###################
        # update metadata #
        ###################

        self.LayerBandsAssignment = tgt_LBA
        self.MetaObj.CWL = dict(zip(tgt_LBA, tgt_cwl))
        self.MetaObj.FWHM = dict(zip(tgt_LBA, tgt_fwhm))
        self.MetaObj.bands = len(tgt_LBA)

        self.arr = im  # type: GeoArray
        self.spec_homo_errors = errs  # type: Union[np.ndarray, None]  # int16, None if ~CFG.spechomo_estimate_accuracy

        #########################################################################################
        # perform spectral homogenization of bandwise error information from earlier processors #
        #########################################################################################

        if self.ac_errors and self.ac_errors.ndim == 3:
            from scipy.interpolate import interp1d

            self.logger.info("Performing linear interpolation for 'AC errors' array to match target sensor bands "
                             "number..")
            outarr = interp1d(np.array(src_cwls), self.ac_errors,
                              axis=2, kind='linear', fill_value='extrapolate')(tgt_cwl)
            self.ac_errors = outarr.astype(self.ac_errors.dtype)
