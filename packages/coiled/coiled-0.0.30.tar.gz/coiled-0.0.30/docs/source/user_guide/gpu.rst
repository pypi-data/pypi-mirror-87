.. _gpus:

GPUs
====

Coiled supports running computations with GPU-enabled machines.
In theory, all that is necessary to get things running is to use the
``worker_gpus=`` keyword in the ``coiled.Cluster`` constructor:

.. code-block:: python

   import coiled

   cluster = coiled.Cluster(
       ...,
       worker_gpus=1,
   )

But in practice things can get more complicated.

This document provides best practices to smooth operation of GPU accelerated workloads.

Example
-------

.. code-block:: python

   import coiled

   # Create a software environment with GPU accelerated libraries
   # and CUDA drivers installed
   coiled.create_software_environment(
       name="gpu-test",
       container="gpuci/miniconda-cuda:10.2-runtime-ubuntu18.04",
       conda={
           "channels": ["rapidsai", "conda-forge", "defaults"],
           "dependencies": ["dask", "dask-cuda", "xgboost", "pytorch"],
       },
   )

   # Create a Coiled cluster that uses Dask-CUDA's CUDAWorker
   # and a GPU-compatible software environment
   cluster = coiled.Cluster(
       n_workers=4,
       software="gpu-test",
       worker_gpu=1,
       worker_class="dask_cuda.CUDAWorker",
   )


Software Environments
---------------------

The first problem people usually run into is creating a software environment
with their desired software stack.  We will need to both install the GPU
accelerated libraries that we want to use (e.g. PyTorch, RAPIDS, XGBoost,
Numba, etc.) and also make sure that the container that we are running on has the
correct CUDA drivers installed.

Coiled infrastructure generally runs with CUDA version 10.2.
If you already have a Docker image with your desired software and the drivers
match, then you should be good to go.

If you plan to make a software environment with conda or pip packages then we recommend
basing your software environment off of the container with the correct drivers
installed, like ``gpuci/miniconda-cuda:10.2-runtime-ubuntu18.04``.

See a functioning example here:

.. code-block:: python

   import coiled

   coiled.create_software_environment(
       name="gpu-test",
       container="gpuci/miniconda-cuda:10.2-runtime-ubuntu18.04",
       conda={
           "channels": ["conda-forge", "defaults"],
           "dependencies": ["dask", "dask-cuda", "xgboost", "pytorch"],
       },
   )


Using dask_cuda.CUDAWorker
--------------------------

The `Dask-CUDA <https://github.com/rapidsai/dask-cuda>`_ project maintains an
alternative ``CUDAWorker`` class that adds a variety of configuration to Dask
workers to better handle GPU workloads.  You may consider using this class for
your cluster's ``worker_class``, instead of the default ``dask.distributed.Nanny``
class:

.. code-block:: python

   worker_class = "dask_cuda.CUDAWorker"

You will also want to ensure that the ``dask-cuda`` is installed in your software
environment.

.. note::

   Coiled requires `dask_cuda>=0.16`


Set the worker_gpu flag
-----------------------

When creating a cluster you will want to specify the number of GPUs per worker
with the ``worker_gpu=`` keyword to the ``coiled.Cluster`` constructor.  We
recommend using a single GPU per worker.

.. code-block:: python

   worker_gpu = 1


Current Hardware
----------------

Currently Coiled mostly deploys cost efficient T4 GPUs by default.
If you are interested in using higher performance GPUs then please `contact us`_.

Account Access
--------------

Free individual accounts do not have GPU access turned on by default.
If you are interested in testing out GPU access then please `contact us`_.

If you have been granted access it may be as part of a team account.  If so,
please be aware that you will have to specify the account under which you want
to create your cluster in the ``coiled.Cluster`` constructor:

.. code-block:: python

   cluster = coiled.Cluster(
       software="gpu-test",
       worker_gpu=1,
       worker_class="dask_cuda.CUDAWorker",
       account="MY-TEAM-ACCOUNT",
   )

.. _contact us: sales@coiled.io
