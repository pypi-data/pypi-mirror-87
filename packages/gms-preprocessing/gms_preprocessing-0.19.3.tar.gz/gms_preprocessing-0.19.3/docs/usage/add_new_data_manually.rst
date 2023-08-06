Add new data manually
^^^^^^^^^^^^^^^^^^^^^

You can also add datasets to the local GeoMultiSens data storage which you previously downloaded on your own
(e.g., via EarthExplorer_ or the `Copernicus Open Access Hub`_).

The following code snippet will exemplarily import two Landat-7 scenes into the GeoMultiSens database:

.. code-block:: python

    from gms_preprocessing.options.config import get_conn_database
    from gms_preprocessing.misc.database_tools import add_externally_downloaded_data_to_GMSDB

    add_externally_downloaded_data_to_GMSDB(
        conn_DB=get_conn_database('localhost'),
        src_folder='/path/to/your/downloaded_data_directory/',
        filenames=['LE71510322000093SGS00.tar.gz',
                   'LE71910232012294ASN00.tar.gz'],
        satellite'Landsat-7',
        sensor='ETM+'
        )

However, this currently only works for Landsat legacy data or if the given filenames are already known in the
GeoMultiSens metadata database.

In other cases, you have to:

1. copy the provider data archives to the GeoMultiSens data storage directory (choose the proper sub-directory
   corresponding to the right sensor)
2. register the new datasets in the GeoMultiSens metadata database as follows:

.. code-block:: python

    from gms_preprocessing.options.config import get_conn_database
    from gms_preprocessing.misc.database_tools import update_records_in_postgreSQLdb

    entityids = ["LE70450322008300EDC00",
                 "LE70450322008284EDC01"]
    filenames = ["LE07_L1TP_045032_20081026_20160918_01_T1.tar.gz",
                 "LE07_L1TP_045032_20081010_20160918_01_T1.tar.gz"]

    for eN, fN in zip(entityids, filenames):
        update_records_in_postgreSQLdb(conn_params=get_conn_database('localhost'),
                                       tablename='scenes',
                                       vals2update_dict={
                                            'filename': fN,
                                            'proc_level': 'DOWNLOADED'},
                                       cond_dict={
                                            'entityid': eN
                                            }
                                       )

.. _EarthExplorer: https://earthexplorer.usgs.gov/
.. _`Copernicus Open Access Hub`: https://scihub.copernicus.eu/
