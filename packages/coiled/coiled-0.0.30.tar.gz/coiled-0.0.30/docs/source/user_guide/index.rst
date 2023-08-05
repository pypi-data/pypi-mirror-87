:notoc:

.. _user-guide:

===========
Coiled Docs
===========

.. toctree::
   :maxdepth: 1
   :hidden:

   getting_started
   cluster
   software_environment
   teams
   backends
   notebooks
   api
   examples
   configuration
   jupyter
   gpu
   security
   faq
   community
   changelog
   oss-foundations


👋 Welcome to Coiled's documentation!

What is Coiled?
---------------

`Coiled <https://coiled.io>`_ is a deployment-as-a-service library for scaling Python. It takes the devops out of
data science to enable data professionals to spend less time setting up networking, managing fleets of
Docker images, creating AWS IAM roles, etc. and more time on their real job.

.. panels::
   :card: border-0
   :container: container-lg pb-3
   :column: col-md-4 col-md-4 col-md-4 p-2
   :body: text-center border-0
   :header: text-center border-0 h4 bg-white
   :footer: border-0 bg-white

   Hosted Dask Clusters
   ^^^^^^^^^^^^^^^^^^^^

   Securely deploy Dask clusters from anywhere you run Python.

   +++

   .. link-button:: cluster
      :type: ref
      :text: Learn more
      :classes: btn-outline-primary btn-block stretched-link

   ---


   Software Environments
   ^^^^^^^^^^^^^^^^^^^^^

   Build, manage, and share conda, pip, and Docker environments.
   Use them locally or in the cloud.

   +++

   .. link-button:: software_environment
      :type: ref
      :text: Learn more
      :classes: btn-outline-primary btn-block stretched-link

   ---

   Manage Teams & Costs
   ^^^^^^^^^^^^^^^^^^^^

   Manage teams, collaborate, set resource limits, and track costs.

   +++

   .. link-button:: teams
      :type: ref
      :text: Learn more
      :classes: btn-outline-primary btn-block stretched-link


Coiled at a glance
------------------

.. tabbed:: Create Dask clusters
   :selected:

   Coiled manages Dask clusters and everything you need to scale Python in
   the cloud robustly and easily. Learn more in the :doc:`Dask clusters docs <cluster>`.

   .. code-block:: python

      # Launch a cluster with Coiled
      import coiled

      cluster = coiled.Cluster(
          n_workers=5,
          worker_cpu=4,
          worker_memory="16 GiB",
      )

      # Connect Dask to your cluster
      from dask.distributed import Client

      client = Client(cluster)

.. tabbed:: Use custom software environments

   Coiled helps you manage software environments by building Docker images
   from `pip <https://pip.pypa.io/en/stable/>`_ and `conda <https://docs.conda.io/en/latest/>`_
   environment files for you. Learn more in the :doc:`software environment docs <software_environment>`.

   .. code-block:: python

      # Create a custom "ml-env" software environment
      # with the packages you want
      import coiled

      coiled.create_software_environment(
          name="ml-env",
          conda=["dask", "scikit-learn", "xgboost"],
      )

      # Create a Dask cluster which uses your "ml-env"
      # software environment
      cluster = coiled.Cluster(software="ml-env")



Beta Signup
-----------

Coiled is currently in beta and welcoming early users!
During this beta period **Coiled is free for all beta users**.
If you would like to join the beta, please
`sign up <https://cloud.coiled.io/login>`_.

.. link-button:: https://cloud.coiled.io/login
    :type: url
    :text: Sign up for the beta
    :classes: btn-outline-primary btn-block


Thank you for trying out Coiled!
