ECMWF database
==============

The atmospheric correction implemented in gms_preprocessing (`SICOR <https://gitext.gfz-potsdam.de/EnMAP/sicor>`_)
uses `ECMWF  <https://www.ecmwf.int/>`_ data (European Centre for Medium-Range Weather Forecasts) to model the
atmospheric state for each scene processed.

These data are ...
  * either **downloaded during runtime** for the current scene to process,
  * or **downloaded in batch** for specific time intervals before running gms_preprocessing.

To be able to download the data, you need to create an account for the ECMWF Web API and save a file called
`.ecmwfapirc` to your home directory that contains your access token.
See `here <https://www.ecmwf.int/en/forecasts/access-forecasts/ecmwf-web-api>`__ for further details.

The file path of your local ECMWF database (which is automatically created by gms_preprocessing when downloading ECMWF
data) can be set with a configuration parameter of gms_preprocessing.
