.. _ref__add_new_data_to_the_database:

Add new data to the database
----------------------------

There are three ways to add new satellite data to the locally stored database. You can use the **WebUI**,
you can run the **data downloader** from the command line or you **add the data manually**.

In each case, two steps have to be carried out:

* the downloaded provider archive data need to be physically copied to the **data storage directory** on disk
* the respective metadata entries need to be added to the GeoMultiSens **metadata database**

.. hint::

    Regarding the metadata entry, these conditions must be fulfilled to make GeoMultiSens recognize a dataset as properly
    added:

    * the **'scenes' table** of the GeoMultiSens metadata database **must contain a corresponding entry** at all
      (if the entry is not there, the database needs to be updated by the metadata crawler which has to
      be done by the database administrator)
    * the **'filename' column** of the respective entry in the 'scenes' table must contain a **valid filename string**
    * the **'proc_status' column** of the respective entry in the 'scenes' table must at least be **'DOWNLOADED'**


.. include:: ./using_the_data_downloader.rst
.. include:: ./add_new_data_manually.rst
