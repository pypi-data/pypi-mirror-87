:notoc:

.. _software-envs:

=====================
Software Environments
=====================

.. currentmodule:: coiled

.. toctree::
   :maxdepth: 1
   :hidden:

   software_environment_creation
   software_environment_management
   software_environment_local
   software_environment_cli


A crucial part of doing your work is making sure you have the software packages
you need. Coiled helps you manage software environments by building Docker images
from `pip <https://pip.pypa.io/en/stable/>`_ and `conda <https://docs.conda.io/en/latest/>`_
environment files for you. You can then use these environments locally, remotely in a Dask cluster,
and can share them with your friends and colleagues.


Supported software specifications
---------------------------------

Coiled supports publicly accessible conda packages, pip packages, and/or Docker images
for creating software environments. You can also compose these steps by, for example, conda installing
packages into a custom Docker image.


Design
------

Coiled uses packaging conventions you're already familiar with. You can point Coiled
at a list of conda or pip pacakges:

.. code-block::

    import coiled

    coiled.create_software_environment(
        name="my-software-env",
        conda=["dask", "xarray=0.15.1", "numba"],
    )

or to a local conda ``environment.yml`` or pip ``requirements.txt`` file:

.. code-block::

    coiled.create_software_environment(
        name="my-software-env",
        conda="environment.yml",
    )

to have custom Docker images built and stored for later use. Note that
you do not need to have Docker installed for Coiled to build Docker images for you!


Usage
-----

Coiled software environments can be used both locally by :ref:`installing the software
environment on your machine <local-software>` and on remote Dask clusters (e.g. running on AWS):

.. code-block::

    import coiled

    # Create a cluster that uses the custom "my-software-env" software environment
    cluster = coiled.Cluster(software="my-software-env")

You can also collaborate with your friends and colleagues by easily sharing software environments.
