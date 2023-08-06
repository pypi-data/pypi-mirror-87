*****
About
*****

The goal of the gms_preprocessing Python library is to provide a fully automatic
pre-precessing pipeline for spatial and spectral fusion (i.e., homogenization)
of multispectral satellite image data. Currently it offers compatibility to
Landsat-5, Landsat-7, Landsat-8, Sentinel-2A and Sentinel-2B.

* Free software: GNU General Public License v3 or later (GPLv3+) (`license details <https://gitext.gfz-potsdam.de/geomultisens/gms_preprocessing/blob/master/LICENSE>`_)
* Documentation: https://geomultisens.gitext-pages.gfz-potsdam.de/gms_preprocessing/doc/
* Code history: Release notes for the current and earlier versions of gms_preprocessing can be found `here <./HISTORY.rst>`_.
* OS compatibility: Linux


Feature overview
================

Level-1 processing:
-------------------

* data import and  metadata homogenization (compatibility: Landsat-5/7/8, Sentinel-2A/2B)
* equalization of acquisition- and illumination geometry
* atmospheric correction (using `SICOR <https://gitext.gfz-potsdam.de/EnMAP/sicor>`_)
* correction of geometric errors (using `AROSICS <https://gitext.gfz-potsdam.de/danschef/arosics>`_)

Level-2 processing:
-------------------

* spatial homogenization
* spectral homogenization (using `SpecHomo <https://gitext.gfz-potsdam.de/geomultisens/spechomo>`_)
* estimation of accuracy layers

=> application oriented analysis dataset
