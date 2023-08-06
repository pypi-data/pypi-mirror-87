=========================================================================================
gms_preprocessing - Spatial and spectral homogenization of satellite remote sensing data.
=========================================================================================

The goal of the gms_preprocessing Python library is to provide a fully automatic
pre-precessing pipeline for spatial and spectral fusion (i.e., homogenization)
of multispectral satellite image data. Currently it offers compatibility to
Landsat-5, Landsat-7, Landsat-8, Sentinel-2A and Sentinel-2B.

* Free software: GNU General Public License v3 or later (GPLv3+) (`license details <https://gitext.gfz-potsdam.de/geomultisens/gms_preprocessing/blob/master/LICENSE>`_)
* Documentation: https://geomultisens.gitext-pages.gfz-potsdam.de/gms_preprocessing/doc/
* Code history: Release notes for the current and earlier versions of gms_preprocessing can be found `here <./HISTORY.rst>`_.
* OS compatibility: Linux


Status
------

.. .. image:: https://img.shields.io/travis/geomultisens/gms_preprocessing.svg
        :target: https://travis-ci.org/geomultisens/gms_preprocessing

.. .. image:: https://readthedocs.org/projects/gms_preprocessing/badge/?version=latest
        :target: https://gms_preprocessing.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. .. image:: https://pyup.io/repos/github/geomultisens/gms_preprocessing/shield.svg
     :target: https://pyup.io/repos/github/geomultisens/gms_preprocessing/
     :alt: Updates

.. image:: https://gitext.gfz-potsdam.de/geomultisens/gms_preprocessing/badges/master/pipeline.svg
        :target: https://gitext.gfz-potsdam.de/geomultisens/gms_preprocessing/commits/master
.. image:: https://gitext.gfz-potsdam.de/geomultisens/gms_preprocessing/badges/master/coverage.svg
        :target: https://geomultisens.gitext-pages.gfz-potsdam.de/gms_preprocessing/coverage/
.. image:: https://img.shields.io/pypi/v/gms_preprocessing.svg
        :target: https://pypi.python.org/pypi/gms_preprocessing
.. image:: https://img.shields.io/conda/vn/conda-forge/gms_preprocessing.svg
        :target: https://anaconda.org/conda-forge/gms_preprocessing
.. image:: https://img.shields.io/pypi/l/gms_preprocessing.svg
        :target: https://gitext.gfz-potsdam.de/danschef/gms_preprocessing/blob/master/LICENSE
.. image:: https://img.shields.io/pypi/pyversions/gms_preprocessing.svg
        :target: https://img.shields.io/pypi/pyversions/gms_preprocessing.svg

See also the latest coverage_ report and the nosetests_ HTML report.

Features
--------

Level-1 processing:
^^^^^^^^^^^^^^^^^^^

* data import and  metadata homogenization (compatibility: Landsat-5/7/8, Sentinel-2A/2B)
* equalization of acquisition- and illumination geometry
* atmospheric correction (using `SICOR <https://gitext.gfz-potsdam.de/EnMAP/sicor>`_)
* correction of geometric errors (using `AROSICS <https://gitext.gfz-potsdam.de/danschef/arosics>`_)

Level-2 processing:
^^^^^^^^^^^^^^^^^^^

* spatial homogenization
* spectral homogenization (using `SpecHomo <https://gitext.gfz-potsdam.de/geomultisens/spechomo>`_)
* estimation of accuracy layers

=> application oriented analysis dataset


Getting started
---------------

Usage via WebApp
^^^^^^^^^^^^^^^^

The recommended way to use gms_preprocessing is to setup the WebApp (see the
gms-vis_ repository) providing a UI for GeoMultiSens. Using this UI, existing
satellite data can be explored, filtered and selected for processing. New data
homogenization jobs (using gms_preprocessing) can be defined and started. All
configuration parameters of gms_preprocessing are accessible in the UI.


.. image:: https://gitext.gfz-potsdam.de/geomultisens/gms_preprocessing/raw/master/docs/images/webapp_screenshot_900x497.png
    :width: 900 px
    :height: 497 px
    :scale: 100 %
    :alt: WebApp Screenshot


Usage via console interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Homogenization jobs can also be created and started using the command line
interface. Documentation can be found `here <https://geomultisens.gitext-pages.gfz-potsdam.de/gms_preprocessing/doc/usage.html#gms-preprocessing-command-line-interface>`__.

Here is a small example:

.. code:: bash

    # start the job with the ID 123456 and override default configuration with the given one.
    >>> run_gms.py jobid 123456 --json_config /path/to/my/config.json

There is a default configuration file, called `options_default.json <https://gitext.gfz-potsdam.de/geomultisens/gms_preprocessing/blob/master/gms_preprocessing/options/options_default.json>`_.
This file contains the documentation for all the available configuration
parameters.


Usage via Python API
^^^^^^^^^^^^^^^^^^^^

There is also a Python API that allows to setup and start homogenization jobs
by a Python function call.

This is an example:

.. code:: python

    from gms_preprocessing import ProcessController

    configuration = dict(
        db_host='localhost',
        CPUs=20
        )

    PC = ProcessController(job_ID=123456, **configuration)
    PC.run_all_processors()

Possible configuration arguments can be found `here <https://gitext.gfz-potsdam.de/geomultisens/gms_preprocessing/blob/master/gms_preprocessing/options/options_schema.py>`__.


History / Changelog
-------------------

You can find the protocol of recent changes in the gms_preprocessing package
`here <https://gitext.gfz-potsdam.de/geomultisens/gms_preprocessing/-/blob/master/HISTORY.rst>`__.


License
-------

gms_preprocessing - Spatial and spectral homogenization of satellite remote sensing data.

Copyright 2020 Helmholtz Centre Potsdam GFZ German Research Centre for Geosciences, Potsdam, Germany

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version. This program is distributed in the hope
that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details. You should have received a copy
of the GNU General Public License along with this program.
If not, see <http://www.gnu.org/licenses/>.


Contact
-------

.. line-block::

    Daniel Scheffler
    eMail: daniel.scheffler@gfz-potsdam.de

    Helmholtz Centre Potsdam GFZ German Research Centre for Geoscienes
    Section 1.4 Remote Sensing
    Telegrafenberg
    14473 Potsdam
    Germany


Credits
-------

The development of the gms_preprocessing package was funded by the German Federal Ministry of Education and Research
(BMBF, project grant code: 01 IS 14 010 A-C).

The package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

Landsat-5/7/8 satellite data and SRTM/ASTER digital elevation models have been provided by the US Geological
Survey. Sentinel-2 data have been provided by ESA.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _coverage: https://geomultisens.gitext-pages.gfz-potsdam.de/gms_preprocessing/coverage/
.. _nosetests: https://geomultisens.gitext-pages.gfz-potsdam.de/gms_preprocessing/nosetests_reports/nosetests.html
.. _conda: https://conda.io/docs/
.. _redis-server: https://www.rosehosting.com/blog/how-to-install-configure-and-use-redis-on-ubuntu-16-04/
.. _gms-vis: https://gitext.gfz-potsdam.de/geomultisens/gms-vis
