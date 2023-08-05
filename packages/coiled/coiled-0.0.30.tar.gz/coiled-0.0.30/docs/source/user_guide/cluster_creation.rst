.. _cluster-creation:

=================
Creating clusters
=================

.. currentmodule:: coiled


Spinning up Dask clusters with Coiled is done by creating a :class:`coiled.Cluster` instance.
``coiled.Cluster`` objects manage a Dask cluster much like other cluster object you may
have seen before like :class:`distributed.LocalCluster` or :class:`dask_kubernetes.KubeCluster`.

Simple example
--------------

In a simple case, you can create a cluster with five Dask workers with:

.. code-block:: python

    import coiled

    cluster = coiled.Cluster(n_workers=5)


.. note::

    Creating a cluster involves provisioning various resources on cloud-based
    infrastructure. This process takes about a minute in most cases.

Once a cluster has been created, you can connect Dask to the cluster by creating a
:class:`distributed.Client` instance:

.. code-block:: python

    from dask.distributed import Client

    client = Client(cluster)

To view the
`Dask diagnostic dashboard <https://docs.dask.org/en/latest/diagnostics-distributed.html>`_
for your cluster, navigate to the cluster's ``dashboard_link``:

.. code-block:: python

    cluster.dashboard_link

which should output an address along the lines of
``"https://ec2-...compute.amazonaws.com:8787/status"``.


.. tip::

    Any Coiled cluster you create will automatically shut down after 20 minutes of
    inactivity. No more large bills from leaving a cluster running over the weekend 🎉!
    You can also customize this idle timeout if needed -- see the :ref:`customize-cluster`
    section for an example that does this.


The ``coiled.Cluster`` class has several keyword arguments you can use to further specify
the details of your cluster. These parameters are discussed in the following sections.


Hardware resources
------------------

The hardware resources your cluster is launched on (e.g. number of CPUs, amount of RAM, etc.)
can be configured with the following ``coiled.Cluster`` keyword arguments:

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Parameter
     - Description
     - Default
   * - ``worker_cpu``
     - Number of CPUs allocated for each worker
     - ``4``
   * - ``worker_gpu``
     - Number of GPUs allocated for each worker. Note that GPU
       access is disabled by default. If you would like access to GPUs,
       please contact sales@coiled.io.
     - ``0``
   * - ``worker_memory``
     - Amount of memory to allocate for each worker
     - ``"16 GiB"``
   * - ``scheduler_cpu``
     - Number of CPUs allocated for the scheduler
     - ``1``
   * - ``scheduler_memory``
     - Amount of memory to allocate for the scheduler
     - ``"8 GiB"``

For example, the following creates a cluster with five workers, each with 2 CPUs and 8 GiB of memory
available, and a scheduler with 2 CPUs (default value) and 16 GiB of memory available:

.. code-block:: python

    import coiled

    cluster = coiled.Cluster(
        n_workers=5,
        worker_cpu=2,
        worker_memory="8 GiB",
        scheduler_memory="16 GiB",
    )

Note that while specifying ``worker_gpu`` will give your cluster workers access to GPUs,
there are some additional best practices to ensure GPU-accelerated hardware is
fully utilized. See the :doc:`GPU best practices <gpu>` documentation
for more information.

Software environment
--------------------

The scheduler and each worker in a Coiled cluster are all launched with the same software environment.
By default, they will use a software environment with Python, Dask, Distributed, NumPy, Pandas, and a
few more commonly used libraries. This default environment is great for basic tasks, but you'll
also want to create your own custom software environments with the packages you need on your cluster.

Coiled supports building and managing custom software environments using pip and conda environment files.
For more details on custom software environments, see the :ref:`software-envs` documentation page.
Once you have a custom software environment you can use the ``software`` keyword argument for ``coiled.Cluster``
to use that software environment on your cluster.

For example, the following uses a custom software environment with XGBoost installed:

.. code-block:: python

    import coiled

    cluster = coiled.Cluster(software="examples/scaling-xgboost")


.. _customize-cluster:

Custom workers and scheduler
----------------------------

Dask supports using custom worker and scheduler classes in a cluster which allows for increased flexibility
and functionality in some use cases (e.g. Dask-CUDA's `CUDAWorker <https://dask-cuda.readthedocs.io/en/latest/worker.html>`_
class for running Dask workers on NVIDIA GPUs). Additionally, worker and scheduler classes
also have keyword arguments that can be specified to control their behavior (for an example, see
`Dask's worker class API documentation <https://distributed.dask.org/en/latest/worker.html#distributed.worker.Worker>`_).

The worker and scheduler class used in a Coiled cluster, as well as the keyword arguments, passed to those
classes can be specified with the following ``coiled.Cluster`` keyword arguments:

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Parameter
     - Description
     - Default
   * - ``worker_class``
     - Class to use for cluster workers
     - ``"distributed.Nanny"``
   * - ``worker_options``
     - Mapping with keyword arguments to pass to ``worker_class``
     - ``{}``
   * - ``scheduler_class``
     - Class to use for the cluster scheduler
     - ``"distributed.Scheduler"``
   * - ``scheduler_options``
     - Mapping with keyword arguments to pass to ``scheduler_class``
     - ``{}``

For example, the following creates a cluster which uses Distributed's ``Worker`` class for workers (instead of the
default ``Nanny`` class) and specifies ``idle_timeout="2 hours"`` when creating the cluster's scheduler:

.. code-block:: python

    import coiled

    cluster = coiled.Cluster(
        worker_class="distributed.Worker",
        scheduler_options={"idle_timeout": "2 hours"},
    )


.. _reusing-clusters:

Reusing clusters
----------------

Once you're created a cluster, it's sometimes useful to be able to connect to the same running cluster
in a different Python process. This can be done by specifying a unique name for the cluster and whether
or not to shutdown a cluster when it's ``close()`` method is called with the following keyword arguments:

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Parameter
     - Description
     - Default
   * - ``name``
     - Name to use for identifying this cluster
     - Randomly generated name
   * - ``shutdown_on_close``
     - Whether or not to shut down the cluster when it finishes
     - ``True`` unless ``name`` points to an existing cluster

For example, the following creates a cluster named "production":

.. code-block:: python

    import coiled

    cluster = coiled.Cluster(
        name="production",
        n_workers=5,
        worker_cpu=2,
        worker_memory="8 GiB",
    )

which we can then, say in another Python session, connect to the same running "production"
cluster by passing ``name="production"`` to ``coiled.Cluster``:

.. code-block:: python

    import coiled

    # Connects to the existing "production" cluster
    cluster = coiled.Cluster(
        name="production",
    )


Cluster configurations
----------------------

As seen in the previous sections, there are a variety of ways in which you can customize your clusters.
In some cases it's useful to save the various parameters that define a cluster (e.g. ``worker_memory``,
``scheduler_options``, etc.) so they can be easily reused or shared with colleagues.

Coiled supports this through the concept of a **cluster configuration**. A cluster configuration is a group
of cluster parameters (e.g. ``worker_memory``, ``scheduler_cpu``, ``software``, etc.) that can be saved
and then reused by yourself or other Coiled users. When creating a cluster, you can use the ``configuration``
keyword argument for ``coiled.Cluster`` to specify a cluster configuration to use.

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Parameter
     - Description
     - Default
   * - ``configuration``
     - Name of cluster configuration to create cluster from
     - ``"coiled/default"``

Cluster configurations are discussed in detail on the :ref:`cluster-config` documentation page.
