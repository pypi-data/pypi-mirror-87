.. _ref__create_new_jobs:

Create new jobs
---------------

There are multiple ways to create new jobs depending on what you have. The section below gives a brief overview.

.. note::

    Only those datasets that were correctly added to the local GeoMultiSens data storage before can be used to create a
    new GeoMultiSens preprocessing job (see :ref:`ref__add_new_data_to_the_database`).


Create a job from a list of filenames
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The list of filenames refers to the filenames of the previously downloaded provider archive data.

.. code-block:: python

    from gms_preprocessing.options.config import get_conn_database
    from gms_preprocessing.misc.database_tools import GMS_JOB

    job = GMS_JOB(conn_db=get_conn_database('localhost'))

    job.from_filenames(
        list_filenames=['LE07_L1TP_045032_20081026_20160918_01_T1.tar.gz',
                        'LE07_L1TP_045032_20081010_20160918_01_T1.tar.gz'],
        virtual_sensor_id=1,
        comment='Two exemplary Landsat-7 scenes for application XY.')

    # write the job into the GeoMultiSens metadata database
    job.create()


.. code-block:: bash

    OUT:
    New job created successfully. job-ID: 26193017
    The job contains:
        - 2 Landsat-7 ETM+_SLC_OFF scenes


Create a job from a list of entity IDs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- TODO


Create a job from a list of scene IDs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- TODO


Create a job from a dictionary
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- TODO
