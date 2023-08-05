=============
Release Notes
=============

0.0.30
======

Released on November 30, 2020.

- Update API to support generalized backend options
- Enable ``coiled.inspect`` and ``coiled.install`` inside Jupyter


0.0.29
======

Released on November 24, 2020.

- Add informative error message when AWS GPU capacity is low
- Fix bug in software environment creation which caused conda packages to be uninstalled
- Add notebook creation functionality and documentation
- Generalize backend options
- Add support for AWS Fargate spot instances


0.0.28
======

Released on November 9, 2020.

- Expose ``private`` field in list/create/update
- More docs for running in users' AWS accounts
- Add Dask-SQL example
- Use examples account instead of coiled-examples
- Add list of permissions for users AWS accounts
- Add example to software environment usage section
- Update ``conda_env_name`` description
- Set default TOC level for sphinx theme


0.0.27
======

Released on October 9, 2020.

- Fix AWS credentials error when running in Coiled notebooks


0.0.26
======

Released on October 8, 2020.

- Handle AWS STS session credentials
- Fix coiled depending on older aiobotocore
- Only use proxied dashboard address in Jobs
- Improve invalid fargate resources error message
- Mention team accounts
- Support AWS credentials to launch resources on other AWS accounts
- Update FAQ with a note on notebooks and Azure support
- Add GPU docs
- Add jupyterlab example
- Add community page
- Add tabbed code snippets to doc landing page
- Ensure job configuration description and software envs are updated


0.0.25
======

Released on September 22, 2020.

- Handle redirecting from ``beta.coiled.io`` to ``cloud.coiled.io``
- Add Prefect example
- Update dashboards to go through our proxy
- Add descriptions to notebooks
- Update cluster documentation
- Add Optuna example


0.0.24
======

Released on September 16, 2020.

- Support overriding cluster configuration settings in ``coiled.Cluster``
- Don't require region on cluster creation
- Add links to OSS licenses
- Add ability to upload files
- Add access token for private repos


0.0.23
======

Released on September 4, 2020.

- Fixed bug where specifying ``name`` in a conda spec would cause clusters to not be launched
- Open external links in a separate browser tab in the docs
- Explicitly set the number of worker threads to the number of CPUs requested if not otherwise specified
- Improvements to Coiled login behavior
- Update to using ``coiled/default`` as our default base image for software environments
- Several documentation updates


0.0.22
======

Released on August 27, 2020.

- Add AWS multi-region support
- Log informative message when rebuilding a software environment Docker image
- Remove link to Getting Started guide from ``coiled login`` output
- Update ``distributed`` version pinning
- Add support for running non-Dask code through Coiled ``Jobs``
- Several documentation updates


0.0.21
======

- Add logs to web UI
- Verify worker count during cluster creation
- Raise more informative error when a solve conda spec is not available
- Improve docker caching when building environments


0.0.20
======

- Allow 'target' conda env in creating software environment (#664)
- Start EC2 instances in the right subnets (#689)


0.0.19
======

- Added support for installing pip packages with ``coiled install``
- Support Python 3.8 on Windows with explicit ``ProactorEventLoop``
- Updated default ``coiled.Cluster`` configuration to use the current Python version
- Updated dependencies to include more flexible version checking in ``distributed``
- Don't scale clusters that we're re-connecting to
- Added support for using custom worker and scheduler classes


0.0.18
======

Released August 8, 2020.

- Add ``--token`` option to ``coiled login``
- Add ``post_build=`` option to ``coiled.create_software_environment``
- Add back support for Python 3.6
- Remove extra newline from websocket output
- Remove ``coiled upload`` from public API
- Add ``coiled env`` CLI command group
- Several documentation updates


0.0.17
======

Released July 31, 2020.

- Move documentation page to docs.coiled.io
- Added ``--version`` flag to ``coiled`` CLI
- Raise an informative error when using an outdated version of the ``coiled`` Python API
- Several documentation updates
- Added ``coiled.Cluster.get_logs`` method
- Added top-level ``coiled.config`` attribute
- Use fully qualified ``coiled.Cluster`` name in the cluster interactive IPython repr


0.0.16
======

Released July 27, 2020.

- Added getting started video to docs.
- Added support GPU enabled workers.
- Added new documentation page on configuring JupyterLab.
- Added support for specifying pip, conda, and/or container inputs when creating software environments.
- Remove account argument from ``coiled.delete_software_environment``.
- Added cost and feedback FAQs.


0.0.15
======

Released July 22, 2020.

- Removed "cloud" namespace in configuration values.
- Several documentation updates.
- Added new security and privacy page to the docs.
- Added ``coiled upload`` command for creating a Coiled software environment
  from a local conda environment.
- Added tests for command line tools.


0.0.14
======

Released July 17, 2020.


0.0.13
======

Released July 16, 2020.

- Update "Getting Started" documentation page.
- Update ``coiled.create_software_environment`` to use name provided by ``conda=`` input, if provided.
- Send AWS credentials when making a ``Cluster`` object.


0.0.12
======

Released July 14, 2020.

- Switch to using full ``coiled`` Python namespace and rename ``CoiledCluster`` to ``coiled.Cluster``
- Raise informative error when attempting to create a cluster with a non-existent cluster configuration
- Bump supported ``aiobotocore`` version to ``aiobotocore>=1.0.7``
- Add ``coiled install`` command to create conda software environments locally
- Repeated calls to ``Cloud.create_cluster_configuration`` will now update an existing configuration

0.0.11
======

Released July 9, 2020.

-  Don't shut down clusters if we didn't create them
-  Slim down the outputs of ``list_software_environments`` and ``list_cluster_configurations``

0.0.10
======

Released July 8, 2020.

-  Use websockets to create clusters due to long-running requests
-  Avoid excess endlines when printing out status in the CLI
-  Allow calling coiled env create repeatedly on the same environment

0.0.9
=====

Released July 7, 2020.

-  Change default to coiled/default
-  Add ``coiled login`` CLI command
-  Use account namespaces everywhere, remove ``account=`` keyword
-  Allow the use of public environments and configurations

0.0.8
=====

Released on July 1, 2020.

- Update to use new API endpoint scheme
- Adds ``conda env create`` command line interface


0.0.7
=====

Released on June 29, 2020.

- Adds ``Cloud.create_software_environment``, ``Cloud.delete_software_environment``, and ``Cloud.list_software_environments`` methods
- Adds ``Cloud.create_cluster_configuration``, ``Cloud.delete_cluster_configuration``, and ``Cloud.list_cluster_configurations`` methods
- Update ``Cloud`` object to use a token rather than a password
- Changed name of package from ``coiled_cloud`` to ``coiled``


0.0.6
=====

Released on May 26, 2020.

- Includes ``requirements.txt`` in ``MANIFEST.in``


0.0.5
=====

Released on May 26, 2020.

- Includes versioneer in ``MANIFEST.in``


0.0.4
=====

Released on May 26, 2020.

- Adds ``LICENSE`` to project


0.0.3
=====

Released on May 21, 2020.

Deprecations
------------

- Renamed ``Cluster`` to ``CoiledCluster``
