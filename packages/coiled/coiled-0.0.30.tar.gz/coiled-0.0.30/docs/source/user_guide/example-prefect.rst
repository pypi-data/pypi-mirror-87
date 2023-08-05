Prefect for Workflow Automation
===============================

Prefect automates data engineering workflows.
Coiled helps scale Prefect on cloud resources.
It's easy to use both together.


Prefect in a nutshell
---------------------

`Prefect <https://www.prefect.io/>`_ is a popular workflow management system.
At it's core, Prefect has the concept of a ``Task``, ``Flow``, and ``Executor``:

- A `Task <https://docs.prefect.io/core/concepts/tasks.html>`_ is an individual step in a Prefect workflow
- A `Flow <https://docs.prefect.io/core/concepts/flows.html>`_ is a collection of tasks that represent the entire workflow
- An `Executor <https://docs.prefect.io/core/concepts/engine.html#executors>`_ is a class that's responsible for running a ``Flow``

Using Prefect's ``DaskExecutor`` you can run workflows on a Dask cluster, including
Coiled clusters.


Prefect + Coiled 
----------------

The example below uses Prefect and Coiled to read NYC Taxi data and find some
of the most generous tippers in historical data. It does this by reading a
CSV file on Amazon S3, breaking it into many small pieces (one DataFrame for
each hour of data), cleans the data, and then finds rows in the data with exceptional
values for tipping and logs those rows.

We highlight a few of the features that Prefect provides:

1.  We intentionally add some random failures into the cleaning process to show off how
    Prefect can provide automatic retry logic
2.  We return lists of objects to show how Prefect can map over collections of outputs
3.  At the end of the computation we send a report to a public Slack channel
    (sign up for the `Coiled Community Slack <https://join.slack.com/t/coiled-users/shared_invite/zt-gqiukhua-rJ4QKxJyO3OYTPR7w_xeOQ>`_
    and then navigate to the ``prefect-example`` channel to see results)
4.  Easy scalability by connecting with a Dask cluster,
    in this case provided by Coiled.

.. literalinclude:: recipes/example-prefect.py


Click :download:`here <recipes/example-prefect.py>` to download the above example script.

How Coiled helps
----------------

Coiled comes into play in these lines:

.. code-block:: python

    import coiled

    executor = DaskExecutor(
        cluster_class=coiled.Cluster,
        cluster_kwargs={
            "software": "jrbourbeau/prefect",
            "shutdown_on_close": False,
            "name": "prefect-play",
        },
    )

where we setup a ``DaskExecutor`` so Prefect can run our workflow on a
``coiled.Cluster`` with the provided arguments. This let's us easily scale
the resources available to Prefect for running our workflow.


Best practices
--------------

Software environments
~~~~~~~~~~~~~~~~~~~~~

You will want to make sure that the Coiled cluster running on the cloud has
Prefect installed, along with any other libraries that you might need in order
to complete the work, like Pandas or S3Fs in this case.  For more information
on, see :doc:`documentation on constructing software environments <software_environment>`.

Reusing clusters
~~~~~~~~~~~~~~~~

It's also common to run several flows one after the other.  For example we may
want to run this same flow on data for many months of data, rather than just
the one file in this example.

In this case spinning up a new Coiled cluster for every flow may be cumbersome
(it takes about a minute to start a cluster).  Instead, we recommend using
the ``shutdown_on_close=False`` keyword, along with a specific name for your
cluster, like ``"prefect-play"`` or ``"production"``.  This tells Coiled
that you want to :ref:`reuse a specific cluster <reusing-clusters>` for many
different workflows.

Coiled will automatically shutdown your cluster after twenty minutes of inactivity by
default. So if you run your flow again after this period that's ok, you will just
have to wait the one minute startup time.

