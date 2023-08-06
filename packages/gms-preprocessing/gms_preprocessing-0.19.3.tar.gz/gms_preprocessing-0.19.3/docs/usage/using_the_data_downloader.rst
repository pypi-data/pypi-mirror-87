Using the data downloader
^^^^^^^^^^^^^^^^^^^^^^^^^

The GeoMultiSens data downloader downloads the requested data and makes sure that the new dataset is properly added to
the local GeoMultiSens data storage directory as well as to the metadata database.

All you need to do is:

.. code-block:: bash

    cd /opt/gms-modules  # default installation path of gms-modules
    bash gms-cli-frontend --download 13552123

This downloads the satellite provider archive that belongs to scene 13552123 of the GeoMultiSens metadata database.
When using the WebUI, these scene IDs are automatically passed to downloader module. However, when running the data
downloader from command line as shown above, you need to know the scene IDs of the scenes you want to download.

To **find out these scene IDs**, you can query the GeoMultiSens metadata database as follows:

.. code-block:: python

    from gms_preprocessing.options.config import get_conn_database
    from gms_preprocessing.misc.database_tools import get_info_from_postgreSQLdb

    get_info_from_postgreSQLdb(
        conn_params=get_conn_database('localhost'),
        tablename='scenes',
        vals2return=['id'],
        cond_dict={
            'entityid': ['LE70450322008300EDC00',
                         'LE70450322008284EDC01'
            }
        )

This returns the scene IDs of two Landsat-7 scenes
with the entity IDs 'LE70450322008300EDC00' and 'LE70450322008284EDC01':

.. code-block::

    OUT:
    [(13547246,), (13552123,)]
