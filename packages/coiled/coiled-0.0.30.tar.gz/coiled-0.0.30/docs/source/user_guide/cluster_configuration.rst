.. _cluster-config:

======================
Cluster configurations
======================

.. currentmodule:: coiled


When creating Dask clusters, there are a variety of ways in which you can customize
the cluster. For example, you can specify the resources (i.e. CPU and memory) available to the
workers in your cluster, the software environment used throughout the cluster, whether
or not to make GPUs available, etc.

Each of these parameters can be specified when creating a ``coiled.Cluster`` (see the
:ref:`cluster-creation` documentation for more details). Additionally, it's also
useful to be able to save these cluster options and share them with friends and colleagues.
Coiled uses the concept of a **cluster configuration** to specify the parameters that define
a Dask cluster, save them, and then share them with others.

.. note::

    It's important to note that creating a cluster configuration doesn't create a
    cluster or provision any resources. You can think of a cluster configuration as
    a template, or recipe, for a cluster that will be create later.


Creating cluster configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cluster configurations are created using the :meth:`coiled.create_cluster_configuration` function.
You must provide each cluster configuration you create with a name to identify the configuration,
along with a set of optional hardware and software parameters.

For example:

.. code-block:: python

    # Create a software environment named "my-conda-env"
    coiled.create_software_environment(
        name="my-conda-env", conda=["dask", "xarray==0.15.1", "numba"]
    )

    # Create a cluster configuration named "my-cluster-config"
    coiled.create_cluster_configuration(
        name="my-cluster-config",
        scheduler_cpu=2,
        scheduler_memory="8 GiB",
        worker_cpu=4,
        worker_memory="16 GiB",
        software="my-conda-env",
    )

creates a cluster configuration named "my-cluster-config" where the Dask scheduler
has 2 CPU / 8 GiB of memory, workers each have 4 CPUs / 16 GiB of memory, and
the "my-conda-env" software environment (also created in the above code snippet)
is used for the scheduler and all workers.

.. admonition:: Note
    :class: note

    Software environments used in cluster configurations must have ``distributed >= 2.23.0``
    installed as `Distributed <https://distributed.dask.org>`_ is required to
    launch Dask scheduler and worker processes.


Using cluster configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create a cluster from a cluster configuration, use the name of configuration for
the ``configuration`` keyword argument to ``coiled.Cluster``. For example:

.. code-block:: python

    # Create a cluster configuration named "my-cluster-config"
    coiled.create_cluster_configuration(
        name="my-cluster-config",
        worker_cpu=4,
        worker_memory="16 GiB",
    )

    # Created a cluster based on the "my-cluster-config" configuration
    # It will use worker_cpu=4 and worker_memory="16 GiB"
    cluster = coiled.Cluster(configuration="my-cluster-config")

Note that you can also use *both* a cluster configuration and pass keyword arguments directly to
``coiled.Cluster``. In this case, keywords which are directly passed will take
precedent over the values stored in the cluster configuration.

For example, in the snippet below ``worker_cpu`` is specified in both a cluster configuration
and passed directly to ``coiled.Cluster``. So the value passed directly to ``coiled.Cluster``
(i.e. ``worker_cpu=4``) will be used:

.. code-block::

    import coiled

    coiled.create_cluster_configuration(
        name="my-config",
        worker_cpu=2,
        worker_memory="16 GiB",
    )
    
    # Here worker_cpu=4 will be used
    cluster = coiled.Cluster(
        configuration="my-config",
        worker_cpu=4,
    )


Listing and deleting cluster configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to creating cluster configurations, you can also use the
:meth:`coiled.list_cluster_configurations` function to list all available
cluster configurations:

.. code-block:: python

    coiled.list_cluster_configurations()

There is also a ``account=`` keyword argument which lets you specify the account which you
want to list cluster configurations for.

Similarly, the :meth:`coiled.delete_cluster_configuration` function can be used to delete
individual configurations. For example:

.. code-block:: python

    coiled.delete_cluster_configuration(name="alice/my-cluster-config")

deletes the cluster configuration named "my-cluster-config" in the Coiled account named "alice".


.. _cluster-config-visibility:

Visibility
^^^^^^^^^^

By default, cluster configurations can be viewed and used by any coiled user.
If you want a cluster configuration to be visible only to members of your account,
call :meth:`coiled.create_cluster_configuration` with ``private=True``

.. code-block:: python

   import coiled

   coiled.create_cluster_configuration(
       name="my-config",
       worker_cpu=2,
       worker_memory="16 GiB",
       private=True,
   )
