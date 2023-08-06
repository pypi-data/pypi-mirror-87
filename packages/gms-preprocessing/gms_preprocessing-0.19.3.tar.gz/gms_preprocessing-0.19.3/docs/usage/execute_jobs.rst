Execute jobs
------------

Once a job is created (see :ref:`ref__create_new_jobs`), it can be executed as follows:

.. code-block:: python

    from gms_preprocessing import ProcessController

    configuration = dict(
        db_host='localhost',
        CPUs=20
        )

    PC = ProcessController(job_ID=123456, **configuration)
    PC.run_all_processors()

This runs the job with the ID 123456 with the configuration parameters as given in the configuration dictionary.
There is a default configuration file, called `options_default.json`_. options_default.json where all the available
configuration parameters are documented.

.. _`options_default.json`: https://gitext.gfz-potsdam.de/geomultisens/gms_preprocessing/blob/master/gms_preprocessing/options/options_default.json
