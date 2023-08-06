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

"""Definition of gms options schema (as used by cerberus library)."""


gms_schema_input = dict(
    global_opts=dict(
        type='dict', required=False,
        schema=dict(
            inmem_serialization=dict(type='boolean', required=False),
            parallelization_level=dict(type='string', required=False, allowed=['scenes', 'tiles']),
            spatial_index_server_host=dict(type='string', required=False),
            spatial_index_server_port=dict(type='integer', required=False),
            CPUs=dict(type='integer', required=False, nullable=True),
            CPUs_all_jobs=dict(type='integer', required=False, nullable=True),
            max_mem_usage=dict(type='integer', required=False, min=0, max=100),
            critical_mem_usage=dict(type='integer', required=False, min=0, max=100),
            max_parallel_reads_writes=dict(type='integer', required=False, min=0),
            allow_subMultiprocessing=dict(type='boolean', required=False),
            delete_old_output=dict(type='boolean', required=False),
            disable_exception_handler=dict(type='boolean', required=False),
            disable_IO_locks=dict(type='boolean', required=False),
            disable_CPU_locks=dict(type='boolean', required=False),
            disable_DB_locks=dict(type='boolean', required=False),
            disable_memory_locks=dict(type='boolean', required=False),
            min_version_mem_usage_stats=dict(type='string', required=False),
            log_level=dict(type='string', required=False, allowed=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']),
            tiling_block_size_XY=dict(type='list', required=False, schema=dict(type="integer"), minlength=2,
                                      maxlength=2),
            is_test=dict(type='boolean', required=False),
            profiling=dict(type='boolean', required=False),
            benchmark_global=dict(type='boolean', required=False),
        )),
    paths=dict(
        type='dict', required=False,
        schema=dict(
            path_fileserver=dict(type='string', required=False),
            path_archive=dict(type='string', required=False),
            path_procdata_scenes=dict(type='string', required=False),
            path_procdata_MGRS=dict(type='string', required=False),
            path_tempdir=dict(type='string', required=False),
            path_benchmarks=dict(type='string', required=False),
            path_job_logs=dict(type='string', required=False),
            path_spatIdxSrv=dict(type='string', required=False),
            path_SNR_models=dict(type='string', required=False),
            path_dem_proc_srtm_90m=dict(type='string', required=False),
            path_earthSunDist=dict(type='string', required=False),
            path_solar_irr=dict(type='string', required=False),
            path_cloud_classif=dict(type='string', required=False),
            path_custom_sicor_options=dict(type='string', required=False, nullable=True),
            path_ECMWF_db=dict(type='string', required=False),
            path_spechomo_classif=dict(type='string', required=False, nullable=True),
        )),
    processors=dict(
        type='dict', required=False,
        schema=dict(
            general_opts=dict(type='dict', required=False, schema=dict(
                skip_thermal=dict(type='boolean', required=False),
                skip_pan=dict(type='boolean', required=False),
                sort_bands_by_cwl=dict(type='boolean', required=False),
                target_radunit_optical=dict(type='string', required=False, allowed=['Rad', 'TOA_Ref', 'BOA_Ref']),
                target_radunit_thermal=dict(type='string', required=False, allowed=['Rad', 'Temp']),
                scale_factor_TOARef=dict(type='integer', required=False),
                scale_factor_BOARef=dict(type='integer', required=False),
                mgrs_pixel_buffer=dict(type='integer', required=False),
                output_data_compression=dict(type='boolean', required=False),
                write_ENVIclassif_cloudmask=dict(type='boolean', required=False),
                )),
            L1A=dict(type='dict', required=False, schema=dict(
                run_processor=dict(type='boolean', required=False),
                write_output=dict(type='boolean', required=False),
                delete_output=dict(type='boolean', required=False),
                SZA_SAA_calculation_accurracy=dict(type='string', required=False, allowed=['coarse', 'fine']),
                export_VZA_SZA_SAA_RAA_stats=dict(type='boolean', required=False),
                )),
            L1B=dict(type='dict', required=False, schema=dict(
                run_processor=dict(type='boolean', required=False),
                write_output=dict(type='boolean', required=False),
                delete_output=dict(type='boolean', required=False),
                skip_coreg=dict(type='boolean', required=False),
                spatial_ref_min_overlap=dict(type='float', required=False, min=0, max=100),
                spatial_ref_min_cloudcov=dict(type='float', required=False, min=0, max=100),
                spatial_ref_max_cloudcov=dict(type='float', required=False, min=0, max=100),
                spatial_ref_plusminus_days=dict(type='integer', required=False),
                spatial_ref_plusminus_years=dict(type='integer', required=False),
                coreg_band_wavelength_for_matching=dict(type='integer', required=False, min=350, max=2500),
                coreg_max_shift_allowed=dict(type='float', required=False, min=0),
                coreg_window_size=dict(type='list', required=False, minlength=0, maxlength=2,
                                       schema=dict(type='integer', required=False, min=8)),
                )),
            L1C=dict(type='dict', required=False, schema=dict(
                run_processor=dict(type='boolean', required=False),
                write_output=dict(type='boolean', required=False),
                delete_output=dict(type='boolean', required=False),
                cloud_masking_algorithm=dict(type='dict', required=False, schema={
                    'Landsat-4': dict(type='string', required=False, allowed=['FMASK', 'Classical Bayesian', 'SICOR']),
                    'Landsat-5': dict(type='string', required=False, allowed=['FMASK', 'Classical Bayesian', 'SICOR']),
                    'Landsat-7': dict(type='string', required=False, allowed=['FMASK', 'Classical Bayesian', 'SICOR']),
                    'Landsat-8': dict(type='string', required=False, allowed=['FMASK', 'Classical Bayesian', 'SICOR']),
                    'Sentinel-2A': dict(type='string', required=False, allowed=['FMASK', 'Classical Bayesian',
                                                                                'SICOR']),
                    'Sentinel-2B': dict(type='string', required=False, allowed=['FMASK', 'Classical Bayesian',
                                                                                'SICOR']),
                    }),
                export_L1C_obj_dumps=dict(type='boolean', required=False),
                auto_download_ecmwf=dict(type='boolean', required=False),
                ac_fillnonclear_areas=dict(type='boolean', required=False),
                ac_clear_area_labels=dict(type='list', required=False, schema=dict(type='string', allowed=[
                    "Clear", "Snow", "Water", "Shadow", "Cirrus", "Cloud"])),
                ac_scale_factor_errors=dict(type='integer', required=False),
                ac_max_ram_gb=dict(type='integer', required=False),
                ac_estimate_accuracy=dict(type='boolean', required=False),
                ac_bandwise_accuracy=dict(type='boolean', required=False),
                )),
            L2A=dict(type='dict', required=False, schema=dict(
                run_processor=dict(type='boolean', required=False),
                write_output=dict(type='boolean', required=False),
                delete_output=dict(type='boolean', required=False),
                align_coord_grids=dict(type='boolean', required=False),
                match_gsd=dict(type='boolean', required=False),
                spatial_resamp_alg=dict(type='string', required=False,
                                        allowed=['nearest', 'bilinear', 'cubic', 'cubic_spline', 'lanczos', 'average',
                                                 'mode', 'max', 'min', 'med', 'q1', 'q3']),
                clip_to_extent=dict(type='boolean', required=False),
                spathomo_estimate_accuracy=dict(type='boolean', required=False),
                )),
            L2B=dict(type='dict', required=False, schema=dict(
                run_processor=dict(type='boolean', required=False),
                write_output=dict(type='boolean', required=False),
                delete_output=dict(type='boolean', required=False),
                spechomo_method=dict(type='string', required=False, allowed=['LI', 'LR', 'QR', 'RFR']),
                spechomo_n_clusters=dict(type='integer', required=False, allowed=[1, 5, 10, 15, 20, 30, 40, 50]),
                spechomo_classif_alg=dict(type='string', required=False, allowed=['MinDist', 'kNN', 'SAM', 'SID']),
                spechomo_kNN_n_neighbors=dict(type='integer', required=False, min=0),
                spechomo_estimate_accuracy=dict(type='boolean', required=False),
                spechomo_bandwise_accuracy=dict(type='boolean', required=False),
                )),
            L2C=dict(type='dict', required=False, schema=dict(
                run_processor=dict(type='boolean', required=False),
                write_output=dict(type='boolean', required=False),
                delete_output=dict(type='boolean', required=False),
                )),
        )),
    usecase=dict(
        type='dict', required=False, schema=dict(
            virtual_sensor_id=dict(type='integer', required=False),  # TODO add possible values
            datasetid_spatial_ref=dict(type='integer', required=False, nullable=True),
            datasetid_spectral_ref=dict(type='integer', required=False, nullable=True),
            target_CWL=dict(type='list', required=False, schema=dict(type='float')),
            target_FWHM=dict(type='list', required=False, schema=dict(type='float')),
            target_gsd=dict(type='list', required=False, schema=dict(type='float'),  maxlength=2),
            target_epsg_code=dict(type='integer', required=False, nullable=True),
            spatial_ref_gridx=dict(type='list', required=False, schema=dict(type='float'), maxlength=2),
            spatial_ref_gridy=dict(type='list', required=False, schema=dict(type='float'), maxlength=2),
        )),
)


def get_updated_schema(source_schema, key2update, new_value):
    def deep_update(schema, key2upd, new_val):
        """Return true if update, else false"""

        for key in schema:
            if key == key2upd:
                schema[key] = new_val
            elif isinstance(schema[key], dict):
                deep_update(schema[key], key2upd, new_val)

        return schema

    from copy import deepcopy
    tgt_schema = deepcopy(source_schema)
    return deep_update(tgt_schema, key2update, new_value)


gms_schema_config_output = get_updated_schema(gms_schema_input, key2update='required', new_value=True)


parameter_mapping = dict(
    # global opts
    inmem_serialization=('global_opts', 'inmem_serialization'),
    parallelization_level=('global_opts', 'parallelization_level'),
    spatial_index_server_host=('global_opts', 'spatial_index_server_host'),
    spatial_index_server_port=('global_opts', 'spatial_index_server_port'),
    CPUs=('global_opts', 'CPUs'),
    CPUs_all_jobs=('global_opts', 'CPUs_all_jobs'),
    max_mem_usage=('global_opts', 'max_mem_usage'),
    critical_mem_usage=('global_opts', 'critical_mem_usage'),
    max_parallel_reads_writes=('global_opts', 'max_parallel_reads_writes'),
    allow_subMultiprocessing=('global_opts', 'allow_subMultiprocessing'),
    delete_old_output=('global_opts', 'delete_old_output'),
    disable_exception_handler=('global_opts', 'disable_exception_handler'),
    disable_IO_locks=('global_opts', 'disable_IO_locks'),
    disable_CPU_locks=('global_opts', 'disable_CPU_locks'),
    disable_DB_locks=('global_opts', 'disable_DB_locks'),
    disable_memory_locks=('global_opts', 'disable_memory_locks'),
    min_version_mem_usage_stats=('global_opts', 'min_version_mem_usage_stats'),
    log_level=('global_opts', 'log_level'),
    tiling_block_size_XY=('global_opts', 'tiling_block_size_XY'),
    is_test=('global_opts', 'is_test'),
    profiling=('global_opts', 'profiling'),
    benchmark_global=('global_opts', 'benchmark_global'),

    # paths
    path_fileserver=('paths', 'path_fileserver'),
    path_archive=('paths', 'path_archive'),
    path_procdata_scenes=('paths', 'path_procdata_scenes'),
    path_procdata_MGRS=('paths', 'path_procdata_MGRS'),
    path_tempdir=('paths', 'path_tempdir'),
    path_benchmarks=('paths', 'path_benchmarks'),
    path_job_logs=('paths', 'path_job_logs'),
    path_spatIdxSrv=('paths', 'path_spatIdxSrv'),
    path_SNR_models=('paths', 'path_SNR_models'),
    path_dem_proc_srtm_90m=('paths', 'path_dem_proc_srtm_90m'),
    path_earthSunDist=('paths', 'path_earthSunDist'),
    path_solar_irr=('paths', 'path_solar_irr'),
    path_cloud_classif=('paths', 'path_cloud_classif'),
    path_custom_sicor_options=('paths', 'path_custom_sicor_options'),
    path_ECMWF_db=('paths', 'path_ECMWF_db'),
    path_spechomo_classif=('paths', 'path_spechomo_classif'),

    # processors > general opts
    skip_thermal=('processors', 'general_opts', 'skip_thermal'),
    skip_pan=('processors', 'general_opts', 'skip_pan'),
    sort_bands_by_cwl=('processors', 'general_opts', 'sort_bands_by_cwl'),
    target_radunit_optical=('processors', 'general_opts', 'target_radunit_optical'),
    target_radunit_thermal=('processors', 'general_opts', 'target_radunit_thermal'),
    scale_factor_TOARef=('processors', 'general_opts', 'scale_factor_TOARef'),
    scale_factor_BOARef=('processors', 'general_opts', 'scale_factor_BOARef'),
    mgrs_pixel_buffer=('processors', 'general_opts', 'mgrs_pixel_buffer'),
    output_data_compression=('processors', 'general_opts', 'output_data_compression'),
    write_ENVIclassif_cloudmask=('processors', 'general_opts', 'write_ENVIclassif_cloudmask'),

    # processors > L1A
    exec_L1AP=('processors', 'L1A', ['run_processor', 'write_output', 'delete_output']),
    SZA_SAA_calculation_accurracy=('processors', 'L1A', 'SZA_SAA_calculation_accurracy'),
    export_VZA_SZA_SAA_RAA_stats=('processors', 'L1A', 'export_VZA_SZA_SAA_RAA_stats'),

    # processors > L1B
    exec_L1BP=('processors', 'L1B', ['run_processor', 'write_output', 'delete_output']),
    skip_coreg=('processors', 'L1B', 'skip_coreg'),
    spatial_ref_min_overlap=('processors', 'L1B', 'spatial_ref_min_overlap'),
    spatial_ref_min_cloudcov=('processors', 'L1B', 'spatial_ref_min_cloudcov'),
    spatial_ref_max_cloudcov=('processors', 'L1B', 'spatial_ref_max_cloudcov'),
    spatial_ref_plusminus_days=('processors', 'L1B', 'spatial_ref_plusminus_days'),
    spatial_ref_plusminus_years=('processors', 'L1B', 'spatial_ref_plusminus_years'),
    coreg_band_wavelength_for_matching=('processors', 'L1B', 'coreg_band_wavelength_for_matching'),
    coreg_max_shift_allowed=('processors', 'L1B', 'coreg_max_shift_allowed'),
    coreg_window_size=('processors', 'L1B', 'coreg_window_size'),

    # processors > L1C
    exec_L1CP=('processors', 'L1C', ['run_processor', 'write_output', 'delete_output']),
    cloud_masking_algorithm=('processors', 'L1C', 'cloud_masking_algorithm'),
    export_L1C_obj_dumps=('processors', 'L1C', 'export_L1C_obj_dumps'),
    auto_download_ecmwf=('processors', 'L1C', 'auto_download_ecmwf'),
    ac_fillnonclear_areas=('processors', 'L1C', 'ac_fillnonclear_areas'),
    ac_clear_area_labels=('processors', 'L1C', 'ac_clear_area_labels'),
    ac_scale_factor_errors=('processors', 'L1C', 'ac_scale_factor_errors'),
    ac_max_ram_gb=('processors', 'L1C', 'ac_max_ram_gb'),
    ac_estimate_accuracy=('processors', 'L1C', 'ac_estimate_accuracy'),
    ac_bandwise_accuracy=('processors', 'L1C', 'ac_bandwise_accuracy'),

    # processors > L2A
    exec_L2AP=('processors', 'L2A', ['run_processor', 'write_output', 'delete_output']),
    align_coord_grids=('processors', 'L2A', 'align_coord_grids'),
    match_gsd=('processors', 'L2A', 'match_gsd'),
    spatial_resamp_alg=('processors', 'L2A', 'spatial_resamp_alg'),
    clip_to_extent=('processors', 'L2A', 'clip_to_extent'),
    spathomo_estimate_accuracy=('processors', 'L2A', 'spathomo_estimate_accuracy'),

    # processors > L2B
    exec_L2BP=('processors', 'L2B', ['run_processor', 'write_output', 'delete_output']),
    spechomo_method=('processors', 'L2B', 'spechomo_method'),
    spechomo_n_clusters=('processors', 'L2B', 'spechomo_n_clusters'),
    spechomo_classif_alg=('processors', 'L2B', 'spechomo_classif_alg'),
    spechomo_kNN_n_neighbors=('processors', 'L2B', 'spechomo_kNN_n_neighbors'),
    spechomo_estimate_accuracy=('processors', 'L2B', 'spechomo_estimate_accuracy'),
    spechomo_bandwise_accuracy=('processors', 'L2B', 'spechomo_bandwise_accuracy'),

    # processors > L2C
    exec_L2CP=('processors', 'L2C', ['run_processor', 'write_output', 'delete_output']),

    # usecase
    virtual_sensor_id=('usecase', 'virtual_sensor_id'),
    datasetid_spatial_ref=('usecase', 'datasetid_spatial_ref'),
    virtual_sensor_name=('usecase', 'virtual_sensor_name'),
    datasetid_spectral_ref=('usecase', 'datasetid_spectral_ref'),
    target_CWL=('usecase', 'target_CWL'),
    target_FWHM=('usecase', 'target_FWHM'),
    target_gsd=('usecase', 'target_gsd'),
    target_epsg_code=('usecase', 'target_epsg_code'),
    spatial_ref_gridx=('usecase', 'spatial_ref_gridx'),
    spatial_ref_gridy=('usecase', 'spatial_ref_gridy'),
)


def get_param_from_json_config(paramname, json_config):
    keymap = parameter_mapping[paramname]  # tuple

    dict2search = json_config
    for i, k in enumerate(keymap):
        if i < len(keymap) - 1:
            # not the last element of the tuple -> contains a sub-dictionary
            dict2search = dict2search[k]
        elif isinstance(k, list):
            return [dict2search[sk] for sk in k]
        else:
            return dict2search[k]
