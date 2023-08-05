=============
API Reference
=============

.. panels::
   :body: text-center

    :opticon:`file-code,size=24`

    .. link-button:: python-api
        :type: ref
        :text: Python API Reference
        :classes: btn-outline-primary btn-block stretched-link

    ---

    :opticon:`terminal,size=24`

    .. link-button:: command-line-api
        :type: ref
        :text: Command Line API Reference
        :classes: btn-outline-primary btn-block stretched-link


.. _python-api:

Python API Reference
====================

.. currentmodule:: coiled

.. autosummary::
    coiled.create_software_environment
    coiled.create_cluster_configuration
    coiled.create_notebook
    coiled.list_software_environments
    coiled.list_cluster_configurations
    coiled.list_clusters
    coiled.delete_software_environment
    coiled.delete_cluster_configuration
    coiled.delete_cluster
    coiled.Cluster
    coiled.install

Software Environments
---------------------
.. autofunction:: coiled.create_software_environment
.. autofunction:: coiled.list_software_environments
.. autofunction:: coiled.delete_software_environment
.. autofunction:: coiled.install
.. autofunction:: coiled.inspect


Cluster Configurations
----------------------
.. autofunction:: coiled.create_cluster_configuration
.. autofunction:: coiled.list_cluster_configurations
.. autofunction:: coiled.delete_cluster_configuration


Clusters
--------
.. autoclass:: coiled.Cluster
    :members:
    :undoc-members:

.. autofunction:: coiled.list_clusters
.. autofunction:: coiled.delete_cluster


Notebooks
---------
.. autofunction:: coiled.create_notebook


.. _command-line-api:

Command Line API Reference
==========================

.. click:: coiled.cli.login:login
   :prog: coiled login
   :show-nested:

.. click:: coiled.cli.install:install
   :prog: coiled install
   :show-nested:

.. click:: coiled.cli.env:create
   :prog: coiled env create
   :show-nested:

.. click:: coiled.cli.env:delete
   :prog: coiled env delete
   :show-nested:

.. click:: coiled.cli.env:list
   :prog: coiled env list
   :show-nested:

.. click:: coiled.cli.env:inspect
   :prog: coiled env inspect
   :show-nested:
