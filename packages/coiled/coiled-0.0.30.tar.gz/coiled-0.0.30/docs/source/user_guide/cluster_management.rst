.. _cluster-management:

=================
Managing clusters
=================

.. currentmodule:: coiled

You can manage your Coiled clusters in two ways: using the ``coiled`` Python package
or via Coiled's `web interface <https://cloud.coiled.io/clusters>`_.


Listing and deleting clusters
-----------------------------

The :meth:`coiled.list_clusters` method will list all active clusters:

.. code-block:: python

    coiled.list_clusters()

Note that when a cluster is created, by default, a unique name for the cluster
is automatically generated. You can provide your own cluster name using the
``name=`` keyword argument for ``coiled.Cluster``.

:meth:`coiled.delete_cluster` can be used to delete individual clusters.
For example:

.. code-block:: python

    coiled.delete_cluster(name="my-cluster")

deletes the cluster named "my-cluster".


Web interface
-------------

Coiled maintains a web interface where you can, among other things, view your recently created
Dask cluster along with other information like how many workers are in the cluster,
how much has running the cluster cost, etc. For more information, see https://cloud.coiled.io/clusters.

.. figure:: images/clusters-table.png
