.. _getting-started:

===============
Getting Started
===============

Welcome to the getting started guide for Coiled! This page
covers installing and setting up Coiled as well as running your first computation
using Coiled.


Install
-------

Coiled can be installed from PyPI using ``pip`` or from the conda-forge
channel using ``conda``:


.. panels::
    :body: text-center
    :header: text-center h5 bg-white

    Install with pip
    ^^^^^^^^^^^^^^^^

    .. code-block:: bash

        pip install coiled

    ---

    Install with conda
    ^^^^^^^^^^^^^^^^^^

    .. code-block:: bash

        conda install -c conda-forge coiled

.. _coiled-setup:

Setup
-----

Coiled comes with a ``coiled login`` command line tool to configure
your account credentials. From the command line enter:

.. code-block:: bash

    $ coiled login


You'll then be asked to navigate to https://cloud.coiled.io/profile to log in and
retrieve your Coiled token.

.. code-block:: bash

    Please login to https://cloud.coiled.io/profile to get your token
    Token:

Upon entering your token, your credentials will be saved to Coiled's local
configuration file. Coiled will then pull credentials from the configuration
file when needed.


.. _first-computation:

Run your first computation
--------------------------

When performing computations on remote Dask clusters, it's important to have the same libraries
installed both in your local Python environment (e.g. on your laptop), as well as on the remote
Dask workers in your cluster.

Coiled helps you seamlessly synchronize these software environments.
While there's more detailed information on this topic is available in the :doc:`software_environment` section,
for now we'll just use the ``coiled install`` command line tool for creating a standard
conda environment locally. From the command line:

.. code-block:: bash

    # Create local version of the coiled/default software environment
    $ coiled install coiled/default
    $ conda activate coiled-coiled-default
    $ ipython

The above snippet will create a local conda environment named "coiled-coiled-default",
activate it, and then launch an IPython session. Note that while we're creating a local software
environment, all Dask computations will happen on remote Dask workers on AWS, *not* on your
local machine (for more information on why local software environments
are needed, see our :ref:`FAQ page <why-local-software>`).

Now that we have our software environment set up, we can walk through the following example:

.. code-block:: python

    # Create a remote Dask cluster with Coiled
    import coiled

    cluster = coiled.Cluster(configuration="coiled/default")

    # Connect Dask to that cluster
    import dask.distributed

    client = dask.distributed.Client(cluster)
    print("Dask Dashboard:", client.dashboard_link)

Make sure to check out the
`cluster dashboard <https://docs.dask.org/en/latest/diagnostics-distributed.html>`_
(link can be found at ``client.dashboard_link``) which has real-time information about
the state of your cluster including which tasks are currently running, how much memory and CPU workers
are using, profiling information, etc.

.. note::

    Note that when creating a ``coiled.Cluster``, resources for our Dask cluster are
    provisioned on AWS. This provisioning process takes about a minute to complete


.. code-block:: python

    # Perform computations with data on the cloud

    import dask.dataframe as dd

    df = dd.read_csv(
        "s3://nyc-tlc/trip data/yellow_tripdata_2019-01.csv",
        parse_dates=["tpep_pickup_datetime", "tpep_dropoff_datetime"],
        dtype={
            "payment_type": "UInt8",
            "VendorID": "UInt8",
            "passenger_count": "UInt8",
            "RatecodeID": "UInt8",
            "store_and_fwd_flag": "category",
            "PULocationID": "UInt16",
            "DOLocationID": "UInt16",
        },
        storage_options={"anon": True},
        blocksize="16 MiB",
    ).persist()

    df.groupby("passenger_count").tip_amount.mean().compute()

The example above goes through the following steps:

- Spins up a remote Dask cluster by creating a :class:`coiled.Cluster` instance.
- Connects a Dask ``Client`` to the cluster.
- Submits a Dask DataFrame computation for execution on the cluster.


Next steps
----------

.. panels::
   :body: text-center
   :header: text-center h5 bg-white
   :footer: border-0 bg-white

   Coiled in action!
   ^^^^^^^^^^^^^^^^^

   Check out easy-to-run example notebooks using Coiled

   +++

   .. link-button:: https://cloud.coiled.io/examples/notebooks
      :type: url
      :text: See Coiled example notebooks
      :classes: btn-outline-primary btn-block stretched-link

   ---

   Software environments
   ^^^^^^^^^^^^^^^^^^^^^

   Learn how you can manage software environments with Coiled

   +++

   .. link-button:: software_environment
      :type: ref
      :text: Go to software environments page
      :classes: btn-outline-primary btn-block stretched-link

   ---

   Dask clusters
   ^^^^^^^^^^^^^

   Learn to launch Dask clusters with Coiled

   +++

   .. link-button:: cluster
      :type: ref
      :text: Go to clusters page
      :classes: btn-outline-primary btn-block stretched-link

   ---

   Teams
   ^^^^^

   Learn how to manage teams, set resource limits, and track costs with Coiled

   +++

   .. link-button:: teams
      :type: ref
      :text: Go to teams page
      :classes: btn-outline-primary btn-block stretched-link
