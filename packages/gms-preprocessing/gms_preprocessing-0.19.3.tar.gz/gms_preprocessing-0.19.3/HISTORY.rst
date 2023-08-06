=======
History
=======

0.19.3 (2020-12-03)
-------------------

* Fixed issue #107 by updating py_tools_ds to v0.16.3


0.19.2 (2020-11-28)
-------------------

* Revised MANIFEST.in to include options_default.json and the database directory.


0.19.1 (2020-11-28)
-------------------

* Added sorted LayerBandsAssignments for SPOT sensors.


0.19.0 (2020-11-27)
-------------------

* Revised the documentation layout.
* Added missing doc requirements.
* Added a minimally needed documentation to be able to run GMS preprocessing jobs (needs to be further improved).
* Activated 'pages' CI job also for enhancement/improve_docs.
* Removed installation section from README.rst.
* Added some documentation about the GMS infrastructure.
* Added some files to .gitignore.


0.18.12 (2020-11-27)
--------------------

* The clean-test rule no longer needs coverage as a requirement since this is a test requirement.
* Fixed error while dumping AC inputs (due to logger).
* Fixed FutureWarning regarding the use of GeoDataFrame and GeoSeries for data without geopandas geometry
  (switched to plain pandas classes).
* Fixed missing log messages regarding released locks.
* Fixed issue #103 ('struct.error: unpack requires a buffer of 4 bytes' within SpatialIndexMediator in case of various
  parallel database accesses) by adding a database lock that blocks parallel database queries.
* Fixed exception while closing AtmCorr.logger.
* Fixed issue #104 (FutureWarning: arrays to stack must be passed as a "sequence" type such as list or tuple.).
* Fixed some type hinting issues.
* GMS_object.get_subset_obj() now returns None in case the subset contains no data at all.
* Added missing MemoryReserver.logger.close() call.
* Fixed an issue causing the L2B/L2C output to contain wrong spectral bands in case the spectral homogenization is
  executed and sort_by_cwl is set to True (due to a wrong wavelength order if no_pan=False).
* SpatialIndexMediator.getFullSceneDataForDataset() now retries the query 10 times in case of a struct.error
  (relates to issue #103).
* Fixed issue #105 ('FileNotFoundError: Options file not found ...' when running run_gms.py -h after installing
  gms_preprocessing from pip or conda-forge.)
* MultiSlotLock and MemoryReserver now hold a default Logger instance in case no logger is passed. This makes the
  logger.close() call obsolete and fixes Test_DEM_Creator.test_index_mediator_query_equals_pgSQL_query().


0.18.11 (2020-11-03)
--------------------

* Bumped version to fix PyPI upload.


0.18.10 (2020-11-03)
--------------------

* Use Redis class instead of deprecated StrictRedis. Clarify name discrepancy of redis between PyPI and conda-forge.
* Adapted code to latest SICOR options files. Added minimal version of SICOR.
* Deactivated sicor check within GMSEnvironment._check_nonpip_packages() as this is now installed via conda-forge.
* Fixed DeprecationWarning (Using or importing the ABCs from 'collections' instead of from 'collections.abc' is
  deprecated since Python 3.3, and in 3.9 it will stop working).
* Added sklearn import in tests.__init__.py to avoid static TLS ImportError.
* Fixed linting in gms_preprocessing.__init__.py.
* Replaced deprecated 'source activate' by 'conda activate'.
* Added shebang to make run_gms.py executable.
* Added conda badges to README.rst.


0.18.9 (2020-10-13)
-------------------

* Added setup, test, doc, lint and dev requirements.
* First working release on PyPI.


0.18.8 (2020-10-13)
-------------------

* Added PyPI deployment job and updated setup.py accordingly.
* Added History/Changelog section to README.rst.
* History is now not appended to the PyPI README file anymore.


0.18.7 (2020-10-13)
-------------------

* Added missing requirement 'openpyxl'.
* Replaced deprecated 'source activate' by 'conda activate'.
* Removed ecmwf-api-client installation as this is now included in SICOR.
* Pinned scipy to 1.1.0 in environment_gms_preprocessing.yml to make CI work for now.
* Revised docker container setup files.


0.18.6 (2020-10-12)
-------------------

* Use SPDX license identifier and set all files to GLP3+ to be consistent with license headers in the source files.
* Excluded tests from being installed via 'pip install'.
* Set development status to 'stable'.


0.18.5 (2020-09-25)
-------------------

* Caught ValueError: I/O operation on closed file within GMS_logger.__del__.
* Fixed a static TLS ImportError during runtime of SICOR when scikit-learn>0.22 is imported.
* Added missing requirements numba and llvmlite to environment_gms_preprocessing.yml.


0.18.4 (2020-09-18)
-------------------

* Replaced calls of sorted_nicely with new dependency 'natsort'. Fixed circular imports.
* Fixed AssertionError caused by new version of pyproj.
* Fixed UnicodeEncodeError while writing ENVI headers.
* Moved scipy imports from module level to function level to avoid 'static TLS' ImportError.
* Fixed gdal_warp call within DEM_Creator class.
* Fixed issues while overwriting projections.
* Fixed logging issue.
* Pinned Python version to 3.7+.
* Fixed DeprecationsWarnings.
* Replaced GMS_object._numba_array_merger() with GMS_object._merge_arrays which does not use numba (and is much faster).
* Removed numba dependency.
* Recreated test dataset for Test_Landsat8_PreCollectionData.
* Replaced two os.system calls with subcall_with_out.
* Created a new job for Test_Landsat8_PreCollectionData.
* Updated minimal version of geoarray.


0.18.3 (2020-04-06)
-------------------

* Added .tar.gz-Files to Git LFS.
* Fixed fallback algorithm within spectral homogenization.
* Input radiometric unit of spectral homogenization is now checked. Linear interpolation is used if its not BOA_Ref.


0.18.2 (2020-04-02)
-------------------

* Pages now expire after 10 days instead of 30 days.
* Removed spechomo classifiers from gms_preprocessing/database as they are now included in external spechomo library.
* Removed parameter 'path_SRFs' from options file because SRFs are now provided by external pyrsr library.
* Removed 'RR' as possible spechomo_method.


0.18.1 (2020-03-31)
-------------------

* Fixed copy/paste error in license headers.
* Added .h5 files to GitLFS.
* Fixed missing bracket.


0.18.0 (2020-03-31)
-------------------

* Added pyrsr dependency.
* Removed anything related to spectral response functions (now part of pyrsr).
* Specified minimal version of pyrsr.


0.17.1 (2020-03-31)
-------------------

* Added license headers and updated LICENSE file with respect to tqdm.


0.17.0 (2020-03-30)
-------------------

New features:

* Spectral homogenization algorithm is now completely running from external SpecHomo library.


Fixes and improvements:

* Removed classification code (now included in external library 'specclassify').
* Fix pipeline badge.
* Added spechomo installation.
* Fixed multiprocessing issue (daemonic processes are not allowed to have children).
* Added SpecHomo to requirements.
* Updated HISTORY.rst.


0.16.6 (2019-07-22)
-------------------

Fixes and improvements:

* Moved spectral homogenization to new separate library 'spechomo'.
* Image classifiers MinDist, SAM and SID can now return distance metrics.
* Image classifiers MinDist, SAM and SID can now label pixels exceeding a given distance metric as unclassified.
* classify_image() now also supports labelling of unclassified pixels.
* Added _show_distances_histogram() and subclass methods. Bugfix.
* Bugfixes and speedup for MinimumDistance_Classifier.
* Fixed _ImageClassifier._label_unclassified_pixels() overwriting nodata values.
* Classification algorithms now ignore pixels with nodata in the input image. Image classification algorithms are now much faster.
* Improved show_cmap(), added _show_distance_metrics() and subclass methods.
* Fixed bug related to initialization value of euclidian distances.
* Classification maps are now returned as int16.
* Moved calc_sam() and calc_sid() to top-level of the module.
* Added FEDSA classifier + enhanced test for image classifiers.
* Updated classify_image().
* Added kNN_SAM_Classifier + tests. Revised SAM_Classifier.
* Added 'kNN_SAM' to classification.classify_image().
* Refactored 'k' parameter o 'n_neighbors'.
* The classification map of kNN_SAM_Classifier is now sorted by ascending SA in the z-dimension.
* Added kNN_MinimumDistance_Classifier + tests.
* Added kNN_FEDSA_Classifier + tests.
* Converted _calc _sam to staticmethod.
* Classification map is now unclassified only in case no match is found at all.
* Fixed missing cmap sorting.


0.16.5 (2019-03-04)
-------------------

Fixes and improvements:

* Fixed test_image_classifier.py.
* Fixed error message.
* Fixed issue #95 (DEM_Creator: passing only 2 UTM coordinates causes No-Data triangles at left and right side of DEM).
* Added random forest classifier to classification algorithms + tests.
* Added random_state to KMeansRSImage.get_random_spectra_from_each_cluster().
* Added kwargs to classify_image() to allow passing init args to classifiers.
* Fixed CFG.spechomo_n_clusters, CFG.spechomo_classif_alg and CFG.spechomo_kNN_n_neighbors ignored in spectral homogenization.
* Added test_predict_by_machine_learner__RFR_L8_S2().
* 'RFR' is currently rejected as method for harmonization due to still missing classifiers.
* Fixed Test_RF_Classifier.


0.16.4 (2018-11-14)
-------------------

Fixes and improvements:

* Added Random Forest Regression as new spectral homogenization method (uses 50 trees). Added test.
* Restricted tree depth of Random Forest Regressors to 10 to avoid overfitting and to drastically reduce file size of classifiers.
* Added logging to ClusterClassifier_Generator and RSImage_ClusterPredictor.
* Fixed dtype conversion issue within spectral resampling.
* Fixed linting.
* Updated classifiers for spectral homogenization.
* Replaced implementation of SAM classifier by own implementation.
* Revised SAM_Classifier.
* Added auto-normalization prior to SAM classification.
* Removed deprecated pysptools implementation of SAM classifier.
* Removed deprecated reference in tests.
* Revised image classification algorithms to speed them up in multiprocessing. Added multiprocessing tests for classification algorithms.
* Improved console output.
* Bugfix for kNN classification.
* Added SID_Classifier + tests.
* Revised nodata value handling of RSImage_ClusterPredictor.predict() and added possibility to statically set the nodata value of the predicted image.
* Fixed KMeansRSImage not using all CPU cores in case CPUs is set to None.


0.16.3 (2018-09-05)
-------------------

Fixes and improvements:

* Fixed comment.
* Added band names and center wavelengths to products of ReferenceCube_Generator.resample_image_spectrally().
* Changed format of band names.
* Added some bugfixing code related to a nodata issue.
* Fixed some type hints.
* No-data value of input/output image of spectral homogenization and no-data value of intermediate classification maps are now separately handled to solve nodata issue during spectral homogenization.
* Cleaned up.


0.16.2 (2018-08-15)
-------------------

Fixes and improvements:

* Added bandnames to predicted image.
* Reference cubes are now clustered separately; cluster map is not copied from Sentinel-2 anymore.
* Updated docker runner build script.
* Added wavelengths to classifiers.
* Bugfix for writing wring center wavelengths into L2B classifiers.
* Updated LR classifiers for spectral homogenization.
* Updated RR classifiers for spectral homogenization.
* Updated QR classifiers for spectral homogenization.
* Fixed division by 0 during computation of MAPE.
* Bugfix within test_spechomo_classifier.py. Fixed wrong version of pycodestyle. Fixed linting.
* Updated QR classifiers after fixing division by 0 bug.
* Improved log message.
* Adapted the changes of the current geoarray branch 'feature/improve_metadata_handling'.
* Bugfix for missing wavelength in reference cube headers.
* Updated minimal version of arosics.
* CI Python environment is now separate from base env. Added defaults channels below conda-forge in environment.yml
* Added explicit conda channels configuration to docker file.
* Try to force conda-forge channel for libgdal.
* CI setup now updates ci_env environment installed via docker_pyenvs instead of creating an independent environment.
* Updated spectral homogenization classifiers.
* Fixed CI setup.


0.16.1 (2018-06-15)
-------------------

* Moved L2B_P.RSImage_ClusterPredictor.classify_image to classification module.


0.16.0 (2018-05-28)
-------------------

New features:

* Added Quadratic Regression as possible algorithm for spectral homogenization.
* Added more Ridge Regression classifiers for different alpha values.
* Added class 'ClusterClassifier_Generator' for generating classifiers with separate transformation parameters for spectral cluster of an image.
* Added 'Test_ClusterClassifier_Generator'.
* Added first working algorithm for cluster homogenization (must improved (slow, complex code). Added tests.
* Added drafts for revised prediction methods.
* Added wavelengths to RefCube metadata.
* Added pysptools to dependencies.
* Added new config parameters 'spechomo_n_clusters', 'spechomo_classif_alg', 'spechomo_kNN_n_neighbors' to control spectral homogenization through cluster learner prediction.
* Added Test_MinimumDistance_Classifier and Test_kNN_Classifier.
* Added docs.
* Added git-lfs installation to .gitlab_ci.yml

Fixes and improvements:

* Update README.rst
* Fixed typo.
* Removed deprecated code, added documentation.
* Improved imports, fixed typing issues.
* Fixed typing issues.
* Fixed creation of Ridge classifiers.
* Revised image classifiers. Added MinimumDistance_Classifier. Revised RSImage_ClusterPredictor and Cluster_Learner.
* Revised Test_SAM_Classifier.
* Removed a lot of deprecated code.
* RefCubes are now saved as integer arrays.
* Test cluster homogenization is now done from Landsat-8 without cirrus band.
* Cluster classifier are now saved with float32 data instead of float64 to save memory.
* Moved image classifiers from L2B_P to new module 'classification'.
* Removed classes 'Classifier_Generator' and 'RSImage_Predictor'.
* Homogenization without clustering is now done with RSImage_ClusterPredictor with n_clusters=1.
* Updated classifier database.
* Moved Test_SAM_Classifier to new module test_image_classifier.
* Moved git-lfs installation to 'before_script'.
* Removed git-lfs installation as it is already installed.
* Bugfix for homogenization exception in case the source image tile consists only of no data values.
* Bugfix for invalid no data value.


0.15.5 (2018-03-28)
-------------------

Fixes and improvements:

* Refactored class process_controller to ProcessController.
* Merged ProcessController.run_all_processors and ProcessController.run_all_processors_OLD.
* Added note to locks module.


0.15.4 (2018-03-28)
-------------------

Fixes and improvements:

* Pipeline 'run_complete_preprocessing' now returns processing reports only (may fix deadlock after large reference jobs).
* Updated example notebooks.
* Update README.rst
* Update LICENSE
* Added WebApp screenshot.


0.15.3 (2018-03-28)
-------------------

* Fixed too short title underline in HISTORY.rst.


0.15.2 (2018-03-28)
-------------------

* Fixed issue #93 (ValueError: I/O operation on closed file). Updated version info (v0.15.2).


0.15.1 (2018-03-28)
-------------------

* Fixed tests. Deleted deprecated GMS_system_setup.py.


0.15.0 (2018-03-27)
-------------------

New features:

* Added additional tests to test_cli.py and test_config.py.
* Job config is now automatically saved as JSON file.


Fixes and improvements:

* Updated defaults for some config parameters.
* Fixed issue #90 (pandas.errors.ParserError: Expected 2 fields in line 31, saw 3)
* Fixed missing bandnames in written accuracy layers.
* Updated minimal version of GeoArray to 0.7.13.
* Enabled accuracy layer generation during tests.
* Fixed incorrect parsing of configuration parameters given by WebUI or CLI parser.
* Revised config and fixed unexpected behaviour of CLI parser (parameters did not override  previously set WebUI configuration).
* Spectral homogenization from Sentinel-2 to Landsat-8 works properly now.
* Fixed "AssertionError: Number of given bandnames does not match number of bands in array."
* Simplified config. Bugfix options_schema.
* Added code for more securely closing loggers.
* Bugfix '.fuse_hidden' files.
* Removed ASCII_writer (deprecated).
* Pipeline 'run_complete_preprocessing' now returns processing reports only (may fix deadlock after large reference jobs).
* RSImage_Predictor.predict now applies predition in tiles to save memory.
* Simplified process controller. GMS jobs now delete their own GMS_mem_acquire_lock during shutdown.
* Fixed deadlock during acquisition of MemoryReserver.
* Moved computation of medium ac_errors for datasets with multiple subsystems from L2C to L2A to avoid memory overflows in L2B or L2C.
* Added number of waiting processes to redis.
* Bugfix. Improved some log messages.
* Fix for exception in record_stats_memusage() in case processing is not started with L1A but continued from a higher processing level.
* Added Test_ProcessContinuing_CompletePipeline.test_continue_from_L2C().


0.14.0 (2018-03-15)
-------------------

New features:

* Added first running version out accuracy layers + writers.
* Added options 'ac_bandwise_accuracy', ''spechomo_bandwise_accuracy'.
* Added IO locks for array reader and writer.
* Added config parameter 'max_parallel_reads_writes' to limit number of read/writes or to enable/disable IO locks, respectively.
* Implemented process locks to avoid CPU/RAM overload on case multiple GMS jobs are running on the same host.
* Implemented accuracy layer for geometric homogenization.
* Added extra validation of MGRS tiles to avoid writing empty tiles. Updated minimal version of geoarray.
* Added option 'write_ENVIclassif_cloudmask' (fixes issue #72).
* Added ECMWF download lock -> fixes feature request #71 ([ECMWF downloads] Add lock to avoid too many connections to ECMWF download API).
* Added version.py which is from now on the only file containing the package version.
* Added version of gms_preprocessing to written header files and job log (fixes feature request #67).
* Added possibility to run test job via CLI argparser.
* Added recording of memory usage via new database table 'stats_mem_usage_homo'. Allows to intelligently estimation of memory usage.
* Added system overload blocking.


Fixes and improvements:

* Added ECMWF credentials check to environment module.
* Added timeout to ECMWF download.
* Bugfix process_controller.shutdown().
* Replaced spatial query within DEMCreator by SpatialIndexMediator query.
* Revised DEM_Creator to fix TimeoutErrors during spatial query.
* Fix for missing ac_errors and mask_clouds_confidence arrays in processing levels L2B, L2C and any MGRS tiles.
* Added some more logging to join functions of AC.
* Increased database timeout for job statistics update (might fix issue #61).
* Fix for MaybeEncodingError. Fix for IndexError within locks module.
* Revised locks.MultiSlotLock. Added locks.IOLock. Added test_locks.py.
* Added logging to L1B_P.L1B_object.get_opt_bands4matching().
* Improved logging during L1B processor.
* Revised logging to job logfile (now contains full log output of the job).
* Changed default directory for job logs.
* Fixed issue #61 ([AC]: RuntimeWarning: All-NaN slice encountered).
* Progress bars during MGRS tiling are now only shown in log level 'DEBUG'.
* Fixed issue #66 (Number of wavelengths does not match number bands in L2C header file).
* Fixed issue #68 (Cloud mask is not applied equally to all bands when filling clouds with no data values).
* Fixed ExceptionHandler.handle_failed() not raising exceptions that occur during handle_failed().
* Fixed 'str' object has no attribute 'month'.
* Merged module 'dataset' into module 'gms_object'.
* Fix for completely failed scenes in case co-registration fails.
* Fix for not continuing processing from L2B.
* Fix for not referencing accuracy layers on disk if L2C object is created from disk.
* Fixed RuntimeError 'Tried to instanciate L1A_object although kwargs...'.
* Revised GMS_obj.GMS_identifier.
* Fixed issue #69 (Spatial homogenization leaves resampling artifacts at the image edges).
* Fixed issue #75 (Black border around L2B products).
* Fixed issue #76 (Cloud mask within .masks.bsq contains no data values at non-clear positions).
* Fixed issue #74 (Small holes in L2C products).
* Removed GMS_object.meta_odict. All metadata is now held in MetaObj.
* Fixed issue # 81 (Wavelength metadata of homogenized product do not match target sensor wavelengths).
* SIGTERM (kill/pkill commands) is now properly handled (locks are closed, etc.).
* Revised default resource limits.
* Added some options to options_default.json
* Fixed issue #89.


0.13.0 (2018-02-08)
-------------------

New features:

* Added code to check proper activation of GDAL.
* Added Test_Classifier_Generator.
* Added first implementation of errors for spectral homogenization.
* Added tests to test_exception_handler.
* Added tests for properly finding already written datasets by subsequent jobs.
* Added test Test_ProcessContinuing_CompletePipeline.
* Added config options 'spatial_index_server_host' and 'spatial_index_server_port'.
* Added tempdir deletion to controller shutdown.
* Added shutdown method to process controller.


Fixes and improvements:

* Removed hardcoded database host from tests.
* Bugfix for test_spectral_resampler.
* Moved environment checks to options.config.set_config().
* Revised paths configs and removed deprecated paths settings.
* Refactored CFG.exec_mode to CFG.inmem_serialization.
* Fixed incorrect handling of previously failed GMS_objects by exception_handler.
* Bugfix for issue #57 (Atmospheric correction fails if no DEM is available).
* Bugfix exception handler.
* Fixed issue #50 (Invalid job progress statistics in case a subsystem fails after another one of the same scene ID
  already succeeded in the same mapper).
* Revised exception handler. Improved test_exception_handler module.
* Fixed a severe bug that copied the same dataset list to all subsequent process controllers.
* Pipeline now returns processed GMS_objects without array data.
* Fixed job summaries.
* Previously processed L2A and L2B Sentinel-2 datasets are now properly found by subsequent jobs (issue #58).
* Fixed issue #9 (L2C MGRS output has no logfile).
* Fix for not recognizing already processed L2A+ datasets if there is a L1C dataset.
* Fixed config. Set Pool(CPUs, maxtasksperchild=1).
* Continued implementation of error array config options.
* Catched ConnectionRefusedError during connection to index server.
* Bugfix SpatialIndexMediatorServer.status.
* Fixed test_cli.py.


0.12.0 (2017-12-14)
-------------------

New features:

* First running version of Spectral Homogenization via Linear Regression.
* Added a lot of docstrings.


Fixes and improvements:

* Spectral homogenization via Linear Regression now working with proper handling of LayerBandsAssignments.


0.11.0 (2017-12-05)
-------------------

New features:

* Added options: coreg_max_shift_allowed, coreg_window_size, ac_scale_factor_errors, path_custom_sicor_options, ac_fillnonclear_areas, ac_clear_area_labels, ac_max_ram_gb
* Added tests for command line argparser.
* Added some srf data.
* Added an option to delete old output through console argparser.
* Added Sentinel-2B compatibility.
* Added Sentinel-2B test. Added Sentinel-2B test data.


Fixes and improvements:

* Revised command line argparser.
* added api changes to the py index mediator implementation
* Fixed validate_exec_configs.
* Fixed exceptions during parsing of most recent Sentinel-2A metadata XMLs.
* Replaced Sentinel-2A new style test data.


0.10.0 (2017-11-28)
-------------------

New features:

* Added tests for exception handler.
* KMeansRSImage: Added functions and properties to apply clustering, plot cluster centers, plot cluster histogram, plot clustered image + Tests.
* KMeansRSImage: Added get_random_spectra_from_each_cluster() and _im2spectra().
* Added L2A_P.SpecHomo_Classifier + test_spechomo_classifier.py.
* Further developed L2B processor.
* Further developed L2B_P.SpecHomo_Classifier.
* Generation of reference cubes now works in multiprocessing.
* Added L2B_P._MachineLearner_RSImage(), L2B_P.LinearRegression_RSImage(), L2B_P.RidgeRegression_RSImage()
* Added options_default.json.
* Added parser functions for options_default.json.
* Added test_config.py.
* Added options schema and activated options validation.
* Added function to get jsonable dict from config.
* new submodule 'options'.
* Added validation test for JobConfig.to_dict().
* Added options: spatial_ref_min_overlap, spatial_ref_min_cloudcov, spatial_ref_max_cloudcov, spatial_ref_plusminus_days, spatial_ref_plusminus_years, band_wavelength_for_matching, spatial_resamp_alg, clip_to_extent, mgrs_pixel_buffer, output_data_compression.


Fixes and improvements:

* Fixed invalid polygons. Fixed wrong call within run_gms.sh
* Fixed AssertionError 'exactly 4 image corners must be present within the dataset'.
* Unified L1A_object inputs.
* Fixed reshape error within KMeansRSImage.
* Changed workflow to get SICOR options and to pass paths of tables and persistence files after sicor issue #6 has been fixed.
* Fixed matplotlib.use() issue.
* Revised spectral response functions database.
* Bugfix for unexpected peaks in SRFs for ASTER, Landsat 5 and 7.


0.9.0 (2017-10-23)
------------------

New features:

* Revised L1B_P.Scene_finder() and L1B_P.L1B_object.get_spatial_reference_scene()
* Added config parameter to disable auto-download of ECMWF data.
* Added config parameter to skip coregistration.
* Added auto-download for AC tables.
* Added additional logging.
* Added generic run script.


Fixes and improvements:

* Revised L1B_P.L1B_object.get_opt_bands4matching().
* Global co-registration now works again.
* Revised environment and spatial_index_mediator modules.
* Revised SRF object.
* Revised exception handler


0.8.0 (2017-09-27)
------------------

New features:

* Revised SICOR wrapper to get Landsat AC to work.


Fixes and improvements:

* Fixed some bugs and added docstrings within L1B_P.Scene_finder().


0.7.0 (2017-09-22)
------------------

New features:

* Test nosetests colored output.
* Added documentation for command line interface.
* Added first version of SpectralResampler1D incl. test module 'test_spectral_resampler'.
* added hyperspectral test data
* cloud masking is now implemented in SICOR.


Fixes and improvements:

* Bugfix within test configuration of config.Job
* Renamed project from 'GeoMultiSens' to 'gms_preprocessing'.
* PEP8 editing.
* Added optional AC input dumping.
* Updated path to sicor.
* Deleted a lot of deprecated/unused code
* Deleted deprecated cloud masking algorithms based on py_tools_ah/classical_bayesian
* Updated sicor_options files.


0.6.0 (2017-07-26)
------------------

New features:

* Implemented FMASK cloud masking for Landsat and Sentinel-2 (called from atmospheric correction) + corresponding tests.
* New test data and test functions (Test_MultipleDatasetsInOneJob); improved test documentation
* Revised DEM creation; Added io.Input_Reader.DEM_Creator (now with fallback to ASTER)
* Added test_input_reader.py. Added ASTER DEM test data.
* Added nosetests including HTML report.
* Rebuilt docker test runner
* Added exceptions module
* Added attribute 'cloud_masking_algorithm' to GMS_object
* Added environment checks for not pip-installable dependencies
* added colored nosetests output


Fixes and improvements:

* fixed wrong folder name for coverage html results
* removed deprecated io.Input_Reader.get_dem_by_extent()
* Fixed issue during job information retrieval from database (Issue #29)
* Removed deprecated install statements from CI setup.
* Enabled full traceback during 'make docs'.
* Fixed warning during 'make docs'.
* Edited .coveragerc
* Deactivated call of L1A_obj.calc_cloud_mask() during L1A processing.
* Fixed missing cloud mask above L1C.
* Removed duplicate line within docker setup.
* removed deprecated attribute 'path_ac_options' from GMS_config.job
* cleaned deprecated entries in .gitignore
* Added temporary workaround for missing options files of sicor (sicor issue #6).
* Revised config.Job -> now features an own configuration for test mode. Passing arguments from outside is now much easier.
* Refactored some attributes of config.Job.
* added cloud classifiers for the included test data
* misc.exceptions: added GMSConfigParameterError
* misc.path_generator: revised get_path_cloud_class_obj(): merged subfolders for cloud classifiers on disk
* processing.pipeline: refactored exec __... to exec _...
* tests.test_gms_preprocessing: removed superfluous paths configs
* removed cloud_classifiers from .gitignore


0.5.0 (2017-07-10)
------------------

New features:

* new test data and test functions (Landsat-8 collection data, Landsat-7 SLC-on pre-collection data and Landsat-5 pre-collection data)
* Coverage now working in multiprocessing.


Fixes and improvements:

* Added auto-deletion of previously created test job output.
* Changed source and target folders of test data.
* Bugfix for not existing archive path on test machine.
* Bugfix for installation errors of PyEphem.
* Removed environment variable settings for deprecated libraries.
* Added 'is_test' attribute to config.Job; revised requirements.txt
* Revised docker builder.
* Fix for job creation issues in case of Landsat ETM+ SLC-ON
* Fix for exception during reading of AC options file.
* removed installer of ecmwf-api-client since this is now done in SICOR directly
* Fix for FileNotFoundError during DEM generation in test mode.
* Updated setup requirements.
* Renamed some test cases.
* Updated some links in the docs and the setup requirements.
* Modified Makefile in order to catch coverage results in multiprocessing.
* Added .coveragerc
* Modified coverage section in Makefile
* Removed pyhdf from automatically installed setup requirements
* Converted all regular expression strings to raw strings.
* Revised code style in metadata.py.


0.4.0 (2017-06-26)
------------------

New features:

* Working CI system
* Added submodules to setup.py
* New test data and test functions.
* Added ECMWF API setup to CI builder.
* Added test case for Sentinel-2A.


Fixes and improvements:

* Updated deprecated import statements. Updated deprecated link to controller file of of SpatialIndexMediator.
* Updated run-scipts.
* Modified .gitignore
* Updated badges
* Fixed corrupt repository references.
* Added pyhdf to CI builder.
* Added python-fmask and psycopg2 to CI builder.
* Revised SICOR implementation.
* Replaced CoReg_Sat implementation by arosics.
* Bugfix within tests.
* Bugfix AC.


0.3.0 (2017-06-01)
------------------

New features:

* Added console parser functionality to run GMS job from a list of archive filenames.


0.1.0 (2017-05-23)
------------------

* Package restructured with cookie-cutter



