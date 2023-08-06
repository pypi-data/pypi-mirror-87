************
Installation
************

Using Anaconda or Miniconda (recommended)
=========================================

Using conda_ (latest version recommended), gms_preprocessing is installed as follows:


1. Create virtual environment for gms_preprocessing (optional but recommended):

   .. code-block:: bash

    $ conda create -c conda-forge --name gms python=3
    $ conda activate gms


2. Then install gms_preprocessing itself:

   .. code-block:: bash

    $ conda install -c conda-forge gms_preprocessing


This is the preferred method to install gms_preprocessing, as it always installs the most recent stable release and
automatically resolves all the dependencies.


Using pip (not recommended)
===========================

There is also a `pip`_ installer for gms_preprocessing. However, please note that gms_preprocessing depends on some
open source packages that may cause problems when installed with pip. Therefore, we strongly recommend
to resolve the following dependencies before the pip installer is run:

    * gdal
    * geopandas
    * ipython
    * matplotlib
    * numpy
    * pyhdf
    * python-fmask
    * pyproj
    * scikit-image
    * scikit-learn=0.23.2
    * shapely
    * scipy

Then, the pip installer can be run by:

   .. code-block:: bash

    $ pip install gms_preprocessing


To enable lock functionality (needed for CPU / memory / disk IO management), install redis-server_:

.. code-block:: bash

    sudo apt-get install redis-server


If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.



.. note::

    The gms_preprocessing package has been tested with Python 3.4+. It should be fully compatible to all Python
    versions from 3.4 onwards.


.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _conda: https://conda.io/docs
.. _redis-server: https://www.rosehosting.com/blog/how-to-install-configure-and-use-redis-on-ubuntu-16-04/
