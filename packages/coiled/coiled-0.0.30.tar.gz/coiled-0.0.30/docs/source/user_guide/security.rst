==================
Security & Privacy
==================

This page outlines Coiled's security and privacy policies.


Security policies
-----------------

Coiled credentials
^^^^^^^^^^^^^^^^^^

When you :ref:`set up Coiled <coiled-setup>` with the ``coiled login`` command line utility, your account username
and token are stored in a local configuration file. This username and token combination gives access to run computations
from a Coiled account and should be treated like a password.

Communication
^^^^^^^^^^^^^

Coiled generates TLS certificates on a per-cluster basis which are used to manage access to each cluster's Dask scheduler
and workers. These certificates are stored in our database and are available to our development teams.
Additionally, the scheduler and workers for a cluster use
`secure communication between them <https://distributed.dask.org/en/latest/tls.html>`_ and are isolated by
AWS networking security groups.

If a higher level of security is required for your application, please contact sales@coiled.io to inquire about deploying
Coiled on your internal systems.

AWS credentials
^^^^^^^^^^^^^^^

Often Dask workers in a cluster will need AWS permissions to access private data or private AWS services.
To address this need, Coiled will use your local AWS credentials to generate a session token and then forward
that token to the Dask workers in your cluster.

Note that having local AWS credentials is not required to use use Coiled. However, in this case only publicly
accessible data and services will be available to your cluster.


Privacy policies
----------------

Sharing by default
^^^^^^^^^^^^^^^^^^

Information like your software environments, cluster configurations, and notebooks are publicly accessible by default to promote
sharing and collaboration. However, you may also create private software environments and cluster configurations if
you prefer. See the :ref:`software visibility <software-visibility>` and
:ref:`cluster configuration visibility <cluster-config-visibility>` sections for more information on private
software environments and cluster configurations, respectively.

Note that information about any cluster running on your account is *not* publicly accessible and is only available
to users which are members of the account.


Data collection
^^^^^^^^^^^^^^^

Coiled collects basic user data when you create an account, like your name, e-mail address, username, and social login.
Additionally, Coiled collects and stores telemetry data from your Dask clusters, similar to the information that is
displayed in the Dask dashboard. We are working to expose this aggregated information to you across several runs in our
web interface.

A full description of what information is collected, as well as how we use and do not use this information, is listed
on our `privacy policy <https://coiled.io/privacy>`_.
