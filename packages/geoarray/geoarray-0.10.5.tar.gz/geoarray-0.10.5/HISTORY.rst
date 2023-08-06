=======
History
=======

0.10.4 (2020-11-02)
-------------------

* Replaced deprecated osgeo imports.


0.10.3 (2020-10-28)
-------------------

* Fixed issue #29 (Exception: Cannot label gridlines on a _EPSGProjection plot.
  Only PlateCarree and Mercator plots are currently supported.)


0.10.2 (2020-10-27)
-------------------

* Removed cartopy pinning and added a warning about the missing grid labels in GeoArray.show() with cartopy<0.18.0.


0.10.2 (2020-10-27)
-------------------

* Added pyepsg to requirements as it is now an optional requirement of cartopy and it is used in geoarray.


0.10.1 (2020-10-27)
-------------------

* Updated the minimal version of cartopy.


0.10.0 (2020-10-19)
-------------------

* Added 'flag' parameter to GeoArray.calc_nodata_mask() + tests.
* Fixed type hints and some issues in test_geoarray.py.
* The geoarray package is now on conda-forge! Updated the installation instructions accordingly.
* Revised environment_geoarray.yml
* Replaced deprecated 'source activate' by 'conda activate'.


0.9.3 (2020-10-12)
------------------

* Use SPDX license identifier and set all files to GLP3+ to be consistent with license headers in the source files.
* Excluded tests from being installed via 'pip install'.


0.9.2 (2020-10-08)
------------------

* Bugfix for not setting nodata values transparent in GeoArray.show().
* Moved cartopy import from module level to class level.
* Filled HISTORY.rst.


0.9.1 (2020-10-06)
------------------

* Bumped version.


0.9.0 (2020-10-06)
------------------

* Fixed missing comma.
* Merge branch 'enhancement/replace_basemap_with_cartopy' into 'master'
* Added cartopy setup o test_geoarray to make CI work.
* Revised GeoArray.show_map() and replaced basemap by cartopy. Dropped mpld3 requirement. Fixed issue #28.
* Added GeoArray._get_cmap_vmin_vmax() and moved code from .show(), .show_map() and .show_map_utm() there.

0.8.37 (2020-10-02)
-------------------

* Fixed broken pip installation of basemap within setup.py.


0.8.36 (2020-09-30)
-------------------

* Revised previous commit.
* Replaced requirement 'basemap' by ssh link in setup.py to fix exception during 'pip install'.


0.8.35 (2020-09-29)
-------------------

* Basemap is now no longer optional as it is easily installable via conda-forge. Holoviews is now officially optional.


0.8.34 (2020-09-28)
-------------------

* Removed dask frm dependencies as it was only an indirect dependency.


0.8.33 (2020-09-18)
-------------------

* Removed restriction that GeoArray.projection cannot be set if the associated file on disk has another projection.


0.8.32 (2020-08-22)
-------------------

* Updated deprecated HTTP links.
* Avoid to update conda base environment with the defaults channel.
* Added environment update before installing geoarray env.
* Fixed syntax in build_testsuite_image.sh. geoarray_ci.docker now inherits from ci_base_centos:0.1.
* Removed channel 'ioam' for holoviews.
* Updated CI setup files and .gitlab.ci.yml.


0.8.31 (2020-08-21)
-------------------

* Moved matplotlib imports to class method level to avoid static TLS import issues.
* Added Python 3.8 and 3.9 to setup.py classifiers.


0.8.30 (2020-08-21)
-------------------

* Fixed .gitlab-ci.yml
* Updated installation instructions.
* Updated minimal version of geoarray.
* Added tolerance in GeoArray.footprint_poly to avoid wrong return values due to float uncertainties.
* Updated minimal version of py_tools_ds.


0.8.29 (2020-08-17)
-------------------

* Adapted code to latest changes in py_tools_ds.
* Bugfix for not setting nodata values transparent in GeoArray.show().
* Fixed a deprecation warning related to matplotlib colormaps.
* Updated minimal version of py_tools_ds.


0.8.28 (2020-03-19)
-------------------

* Merge branch 'enhancement/speed_up_nodatamask' into 'master'
* The algorithm to compute the nodata mask is now much faster, especially for datasets with many spectral bands.


0.8.27 (2020-01-08)
-------------------

* The geopandas dependency is not needed anymore.
* Updated conda environment.
* Updated minimal version of py_tools_ds.


0.8.26 (2020-01-08)
-------------------

* Disabled Python update in test_geoarray_install.
* Added conda and Python update to test_geoarray_install.
* Removed pyresample from dependencies (not needed anymore).
* Revised dependencies and test_geoarray_install job.
* Fixed broken badge.
* Added downloads badge.


0.8.25 (2019-10-10)
-------------------

* Merge branch 'bugfix/fix_bandname_types' into 'master'
* Fixed mixed types of band names.


0.8.24 (2019-10-10)
-------------------

* Merge branch 'bugfix/fix_band_names' into 'master'
* Fixed band names not properly read (fixed issue #26).


0.8.23 (2019-10-04)
-------------------

* Fixed typing issue.


0.8.22 (2019-08-14)
-------------------

* Replaced deprecated PyPi upload commands by twine.


0.8.21 (2019-07-22)
-------------------

* Merge branch 'enhancement/add_license_texts' into 'master'
* Added license texts.
* Merge branch 'enhancement/allow_lists_in_get_subset' into 'master'


0.8.20 (2019-07-09)
-------------------

* Lists are now allowed in zslice parameter for GeoArray.get_subset().
* Merge branch 'bugfix/fix_ensure_np_shape_consistency_3D_2D' into 'master'


0.8.19 (2019-05-22)
-------------------

* Bugfix.


0.8.18 (2019-05-14)
-------------------

* Bugfix.
* Added ignore_rotation to GeoArray.show().


0.8.17 (2019-05-10)
-------------------

* Merge branch 'bugfix/fix_issue24_and_25' into 'master'
* Fixed issue #24 (TypeError: function takes exactly 1 argument (0 given)).
* Fixed issue #25 (RuntimeError: b'major axis or radius = 0 or not given').


0.8.16 (2019-04-29)
-------------------

* Merge branch 'bugfix/fix_stretching' into 'master'
* Fixed gray value stretching issue in case of rotated ENVI images without inherent nodata value.


0.8.15 (2019-04-29)
-------------------

* Merge branch 'bugfix/fix_rotation_issue23' into 'master'
* Fix.
* Fix for issue #23 (GeoArray.show_map does not respect ENVI rotation in map info if image has less than
  1.000.000 pixels per band).


0.8.14 (2019-03-29)
-------------------

* Merge branch 'enhancement/improve_nodata_value_handling' into 'master'
* Fixed linting.
* Nodata values are now properly written to ENVI header files.


0.8.13 (2019-03-29)
-------------------

* Updated requirements.
* Fixed issue #22 (GeoArray[slice, slice, np.integer] returns the full array instead of a single band).


0.8.12 (2019-03-29)
-------------------

* Merge branch 'bugfix/fix_np_integer_indexing' into 'master'


0.8.11 (2019-03-29)
-------------------

* Fixed issue #22 (GeoArray[slice, slice, np.integer] returns the full array instead of a single band).
* Fixed FutureWarning regarding the use of a non-tuple sequence for multidimensional indexing.


0.8.10 (2018-12-15)
-------------------

* Fixed corrupted makefile.
* Fixed AssertionError in case GeoArray is instanced with a file from disk without map information and projection
  is set afterwards.

0.8.9 (2018-12-13)
------------------

* Added 'is_map_geo' attribute to GeoArray.

0.8.8 (2018-12-05)
------------------

* Replaced 'importlib.util.find_spec' with 'pkgutil.find_loader' to ensure Python 2.7 compatibility.
* Added some type hints.


0.8.7 (2018-09-17)
------------------

* Bugfix for wrong shape of return value when GeoArray instance is indexed with an instance of np.integer.
* Improved colormap handling within GeoArray.show().


0.8.6 (2018-09-13)
------------------

* Refactored function name and updated docstring.
* Fixed behaviour of GeoArray.__getitem__() unequal to numpy behaviour (caused issue #18).
* Added tests.


0.8.5 (2018-09-11)
------------------

* GeoArray.show() now returns the matplotlib object in non-interactive mode.

0.8.4 (2018-09-11)
------------------

* Fixed deploy_pypi CI job.
* Fixed GeoArray.show_histogram() (issue #17).


0.8.3 (2018-09-11)
------------------

* Added parameter 'ax' to GeoArray.show().


0.8.2 (2018-08-31)
------------------

* Changed behaviour of calc_mask_nodata() recognizing pixels as nodata that contain the nodata value in any band.
* Now they need to contain it in ALL bands.


0.8.1 (2018-08-27)
------------------

* Fixed TypeError within metadata module.
* Try to fix ncurses issue.
* Force libgdal to use conda-forge.
* Docker image now inherits from gms_base_centos:0.2.
* CI setup now updates ci_env environment installed via docker_pyenvs instead of creating an independent environment.
* Fix test_geoarray_install.
* Fix test_geoarray_install.
* Fix test_geoarray_install.
* Fix.
* Fix.
* Fix for CI issue.
* CI Python environment is now separate from base env. Added defaults channels below conda-forge in environment.yml
* Updated README.
* Updated README.
* Updated cell output.
* Updated cell output.
* Updated cell output.
* Updated cell output.
* Removed interactive map from notebook.
* Cleaned up.
* Changed link.
* Revised example notebook.
* Added some readme files.
* Added some readme files.
* Added example notebook.

0.8.0 (2018-08-10)
------------------

* Added tests for test_get_subset_2D.
* Bugfixes. Added tests for get_subset.
* Fix for broken GeoArray.get_subset() in case GeoArray.is_inmem == True.
* Fixed linting.
* GeoArray.get_subset() now properly returns GeoArray instance subsets with all metadata and attributes inherited
  from the full GeoArray.
* Added .copy() t make sure metadata.band_meta is really copied.
* Fixed GeoArray.save() for other formats than ENVI.
* Fixed code style issue.
* Fixed metadata setter. Removed deprecated code.
* GDAL_Metadata instances are now subscriptable.
* Bugfix for not updating GeoArray.metadata.bands within GeoArray.get_subset().
* Fixed issue that bandnames are not written to ENVI header by GeoArray.save().
* Bugfixes.
* Enhanced setters, added test data, added tests.
* Band names and description are now correctly saved in ENVI format.
* First implementation of metadata class in GeoArray.
* Added a first prototype of a metadata class.
* Added GDAL cache flushing.
* Added GDAL cache flushing.
* GDAL metadata values are now forced to be strings.
* Updated docker runner build script.


0.7.16 (2018-05-07)
-------------------

* Fixed linting.
* Fixed issue #19 (GeoArray.tiles() fails in case of 2D array).


0.7.15 (2018-04-09)
-------------------

* Fix.


0.7.14 (2018-04-09)
-------------------

* Added version.py.
* Fixed unequal return value of __getitem__ depending on is_inmem.


0.7.13 (2018-03-15)
-------------------

* Fixed wrong copying of bandnames from GeoArray instance within GeoArray.__init__().


0.7.12 (2018-02-22)
-------------------

* Merged branch 'bugfix/issue15' into 'master'.
* Fixed issue #15 (ValueError: 'axis' entry is out of bounds).


0.7.11 (2018-01-17)
-------------------

* Merge branch 'bugfix/fix_GeoArray_save'
* Fixed GeoArray.save()


0.7.10 (2018-01-17)
-------------------

* Fixed GeoArray.save()


0.7.9 (2017-12-11)
------------------

* Fixed GeoArray.get_subset().


0.7.8 (2017-11-30)
------------------

* Improved GeoArray.get_subset().


0.7.7 (2017-11-30)
------------------

* Bugfix for GeoArray.get_subset()


0.7.6 (2017-11-27)
------------------

* Bugfix for GeoArray.get_subset()


0.7.5 (2017-11-24)
------------------

* Fix.


0.7.4 (2017-11-22)
------------------

* Merge branch 'bugfix/fix_subset_zsclice'
* Added tests for plotting functions.
* Revised GeoArray.get_subset(). Added bandnames deleter. Renamed some test functions.
* Added test___getitem__() and test_get_subset().

0.7.3 (2017-11-20)
------------------

* Removed duplicate.
* Revised docker setup workflow.
* Replaced pandas  by geopandas within CI installer test.
* Merge branch 'bugfix/fix_incorrect_footprint'

0.7.2 (2017-11-16)
------------------

* Fixed issue #12 (incorrect footprint polygon).
* Updated README.
* Updated README. Moved geopandas to conda dependencies.


0.7.1 (2017-11-07)
------------------

* Bugfix
* GeoArray.tiles now has a length (added __len__).


0.7.0 (2017-11-03)
------------------

* Fixed linting issue.
* Fixed bad handling of local projections in GeoArray.set_gdalDataset_meta().
* Updated docker container version tag.
* Updated minimum version of py_tools_ds.
* Added docstring to GeoArray.tiles() and corresponding tests.
* Added function GeoArray.tiles().
* Added requirements_pip.txt.


0.6.16 (2017-10-19)
-------------------

* Fixed mpld3 exception. Revised availability checks for optional libs.


0.6.15 (2017-10-12)
-------------------

* Updated minimal version of py_tools_ds.


0.6.14 (2017-10-12)
-------------------

* Speedup for GeoArray.footprint_poly and GeoArray.mask_nodata.
* Updated minimal version of py_tools_ds.
* Updated README.rst


0.6.13 (2017-10-11)
-------------------

* Excluded some funcs from coverage.
* Reverted previous commit.
* Excluded installation of numpy, scikit-image and matplotlib from test_geoarray_install CI job.
* Renamed CI job 'deploy_pages' tp 'pages'.
* Fixed missing lib within docker setup.
* Updated deploy_pages CI job to make pages work again.
* Updated deploy_pages CI job to make pages work again.
* test_geoarray_install now runs on latest Python 3.
* test_geoarray_install is now only executed for master branch.
* Removed installation of testing libs from CI job.


0.6.12 (2017-10-10)
-------------------

* Updated Anaconda version within docker builder.
* Changed upgrade of py_tools_ds within CI job.
* Updated docker builder.
* Added auto-update of py_tools_ds within CI job.


0.6.11 (2017-10-10)
-------------------

* Simplified optional dependency check.
* Updated minimal version of py_tools_ds.


0.6.10 (2017-10-10)
-------------------

* GeoArray.geotransform.setter: Improved input validation.


0.6.9 (2017-10-06)
------------------

* Added parameters 'pmax' and 'pmin' to GeoArray.show().


0.6.8 (2017-10-06)
------------------

* GeoArray.geotransform now always returns a list.
* GeoArray.set_gdalDataset_meta(): Bugfix for returning gt with positive ygsd in case of arbitrary coordinates.


0.6.7 (2017-10-06)
------------------

* GeoArray.clip_to_poly(): Fix for not updating self._footprint_poly.
* Added GeoArray.clip_to_footprint() and GeoArray.clip_to_poly(). Simplified GeoArray.get_mapPos().


0.6.6 (2017-09-20)
------------------

* Suppressed flake8 warning.
* Disabled matplotlib figure popups during unittests.
* Fix for computing wrong footprint poly if nodata value is NaN.


0.6.5 (2017-09-20)
------------------

* Fixed wring stretching of GeoArray.show() in case image contains np.nan.
* Fixed wrong nodata value detection in case nodata is np.nan.


0.6.4 (2017-09-17)
------------------

* Updated version info.


0.6.3 (2017-09-17)
------------------

* Suppressed code compatibility check.
* Added type hints.
* Added style libs to docker container setup. Updated .gitlab_ci.yml.
* Removed explicit typing to avoid circular dependency.
* PEP8 editing. Added linting.


0.6.2 (2017-09-17)
------------------

* Added dask to setup_requirements.


0.6.1 (2017-09-17)
------------------

* Updated installation instructions within README.rst.


0.6.0 (2017-09-12)
------------------

* Fix holoviews import error.
* Added test for geoarray installer. Removed fixed version of holoviews within docker container setup.
* Activated artifacts for failed pipelines.
* Revised test requirements.


0.5.14 (2017-09-11)
-------------------

* Fix pandas bug.


0.5.13 (2017-09-11)
-------------------

* Updated minimal py_tools_ds version.
* Cleaned up .gitlab_ci.yml
* Updated docker container setup and cleaned-up gitlab_ci.yml.
* Added LD_LIBARY_PATH to gitlab_ci.yml.
* Fixed gitlab_ci.yml. danschef 9/11/17, 7:30 PM
* Fixed gitlab_ci.yml.
* Updated docker container setup and adjusted gitlab_ci.yml
* Updated docker container version tag.
* Validated Python 2.7 support.


0.5.12 (2017-09-11)
-------------------

* Updated minimal version of py_tools_ds.
* Fixed some Windows-incompatible paths within test_geoarray. PEP8-editing for the tests.


0.5.11 (2017-09-01)
-------------------

* Updated README.rst.
* Merge remote-tracking branch 'origin/master'
* Merge branch 'Tests'
* Updated pip package setups within docker container setup.
* minor changes
* Adding comments to the test script.
* Extending the test-script: testing the save-function and several plot-functions.
* Extending the test-script: testing the save-function and several plot-functions.
* Commiting a BadDataMask for the tested .tif-Image. Extending the test-functions test_NoDataValueOfTiff and
  test_MaskBaddataOffTiff (before: test_MaskBaddataIsNone).


0.5.10 (2017-08-30)
-------------------

* Fixed bug related to matplotlib backend (issue #8).
* Merge branch 'coverage_report' into 'master'
* Extent the files Makefile and .gitlab-ci.yml for a more detailed coverage report.


0.5.9 (2017-08-23)
------------------

* Bugfix
* Merge branch 'master' into dev
* Bugfixes and minor improvements.
* Improved error handling within GeoArray.from_path().


0.5.8 (2017-08-20)
------------------

* Adjusted code according to changes within py_tools_ds.


0.5.7 (2017-08-19)
------------------

* Specified minimal version for py_tools_ds.
* Updated docker setup (disabled caching).
* Updated makefile.
* Fixed double installation of coverage during docker container setup; added python-devel to docker setup to
  speed up coverage.
* Fixed wrong references in test_geoarray.py
* Added py_tools_ds to docker container setup to avoid circular dependencies.
* Updated build_testsuite_image.sh.
* Fixed osr import error.
* Fix setup.py; rebuilt docker container.
* Added new test requirements to docker container setup.

0.5.6 (2017-07-26)
------------------

* updated subsetting._clip_array_at_mapPos()


0.5.5 (2017-07-24)
------------------

* Added GeoArray.show_histogram().
* Tracebacks are now printed in case of exception during 'make docs'.


0.5.4 (2017-07-19)
------------------

* Merge branch 'dev'
* Clearer error message in case the optional library Basemap is missing.


0.5.2 (2017-07-19)
------------------

* Added dummy function.
* Updated setup.py and added scikit-image to setup requirements.
* Added basemap setup and to docker builder ant to setup requirements.


0.5.1 (2017-07-05)
------------------

* Revised badges.


0.5.0 (2017-07-05)
------------------

* Added auto-deploy to PyPI; revised badges.


0.4.7 (2017-07-03)
------------------

* Updated setup requirements.


0.4.6 (2017-07-03)
------------------

* Added py_tools_ds to external dependencies within setup.py.


0.4.5 (2017-07-03)
------------------

* First release on PyPI.


0.4.4 (2017-07-03)
------------------

* Updated README.rst.


0.4.3 (2017-07-03)
------------------

* Updated HISTORY.rst.
* Updated docker builder and setup requirements.
* Updated docker builder.
* Updated setup requirements to fix holoviews installation issue.
* Updated installation instructions within README.rst; Updated CONTRIBUTING.rst, installation.rst, HISTORY.rst
* Added holoviews setup to docker builder; updated setup.py.


0.4.0 (2017-06-28)
------------------

* Updated setup.py
* Added requirements.txt
* Revised CI setup.
* Updated README.rst
* Updated setup.py
* Updated README.rst
* Updated README.rst
* Updated README.rst
* Updated CI system builder.
* Updated metadata handling (not yet completely working).
* Updated build_testsuite_image.sh
* Passed metadata through to GeoArray subset that comes out of GeoArray.get_subset()
* Added first version of CI files (not yet working).
* Bugfix Issue #7: GeoArray.get_subset()
* Bugfix
* Updated README.
* Updated README.
* Added submodules to setup.py.


0.3.0 (2017-06-09)
------------------

* Merge branch 'master' into Tests
* Merge branch 'master' into Tests
* Updated deprecated import statements. Merged branch Tests into master.
* Biggest changes: Corrected the relative path to an absolute path, added the beginning of the second test case and
  extended the test suite to execute the second test case, only when the first test case was successful.
* updated some docstrings
* Merge https://gitext.gfz-potsdam.de/danschef/geoarray into Tests
* The new test case for the basic functions of geoarray.
* Commiting the first part of the new test case
* Fixed insufficient input validation in GeoArray.
* Fixed a bug in GeoArray.show()
* Merge remote-tracking branch 'origin/Tests' into Tests
* Commiting the first part of the new test case


0.2.0 (2017-05-29)
------------------

* Merge branch 'Tests'
* fixed FileNotFoundError within Test_GeoarrayAppliedOnTiffPath.setUpClass
* added a function to get a subset GeoArray
* Commiting the first part of the new test case
* Commiting the first part of the new test case
* Trail: Commiting changes through the new branch "Tests"
* Trail: Commiting changes through the new branch "Tests"
* updated README
* changed package name in accordance to PEP8
* updated README
* renamed README
* adjusted some imports, modified README
* added first compilation of GeoArray source codes
* First commit of boilerplate code and cut cookies...


0.1.0 (2017-03-31)
------------------

* Package creation.
