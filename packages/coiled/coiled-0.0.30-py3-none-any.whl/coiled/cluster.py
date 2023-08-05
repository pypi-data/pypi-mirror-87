from typing import Tuple, List, Dict, Optional
import os
import asyncio
import aiobotocore
import botocore
import sys
import time
import uuid
import warnings

import dask
import dask.distributed
import distributed.deploy

from .core import Cloud
from .utils import parse_identifier


class Cluster(distributed.deploy.Cluster):
    """Create a Dask cluster with Coiled

    Parameters
    ----------
    n_workers
        Number of workers in this cluster. Defaults to 4.
    configuration
        Name of cluster configuration to create cluster from.
        If not specified, defaults to ``coiled/default`` for the
        current Python version.
    name
        Name to use for identifying this cluster. Defaults to ``None``.
    software
        Identifier of the software environment to use, in the format (<account>/)<name>. If the software environment
        is owned by the same account as that passed into "account", the (<account>/) prefix is optional.

        For example, suppose your account is "wondercorp", but your friends at "friendlycorp" have an environment
        named "xgboost" that you want to use; you can specify this with "friendlycorp/xgboost". If you simply
        entered "xgboost", this is shorthand for "wondercorp/xgboost".

        The "name" portion of (<account>/)<name> can only contain ASCII letters, hyphens and underscores.
    worker_cpu
        Number of CPUs allocated for each worker. Defaults to 2.
    worker_gpu
        Number of GPUs allocated for each worker. Defaults to 0 (no GPU support). Note that this will _always_
        allocate GPU-enabled workers, so is expensive.
    worker_memory
        Amount of memory to allocate for each worker. Defaults to 8 GiB.
    worker_class
        Worker class to use. Defaults to "dask.distributed.Nanny".
    worker_options
        Mapping with keyword arguments to pass to ``worker_class``. Defaults to ``{}``.
    scheduler_cpu
        Number of CPUs allocated for the scheduler. Defaults to 1.
    scheduler_memory
        Amount of memory to allocate for the scheduler. Defaults to 4 GiB.
    scheduler_class
        Scheduler class to use. Defaults to "dask.distributed.Scheduler".
    scheduler_options
        Mapping with keyword arguments to pass to ``scheduler_class``. Defaults to ``{}``.
    asynchronous
        Set to True if using this Cloud within ``async``/``await`` functions or
        within Tornado ``gen.coroutines``. Otherwise this should remain
        ``False`` for normal use. Default is ``False``.
    cloud
        Cloud object to use for interacting with Coiled.
    account
        Name of Coiled account to use. If not provided, will
        default to the user account for the ``cloud`` object being used.
    shutdown_on_close
        Whether or not to shut down the cluster when it finishes.
        Defaults to True, unless name points to an existing cluster.
    region
        Name of the AWS region to create the cluster in (e.g. "us-east-2").
        If not specified, will check the ``coiled.aws.region``
        configuration value.
        Warning: ``region`` is deprecated and will be remove soon.
    backend_options
        Dictionary of backend specific options (e.g. ``{'region': 'us-east-2'}``)
    """

    def __init__(
        self,
        n_workers: int = 4,
        configuration: str = None,
        software: str = None,
        worker_cpu: int = None,
        worker_gpu: int = None,
        worker_memory: str = None,
        worker_class: str = None,
        worker_options: dict = None,
        scheduler_cpu: int = None,
        scheduler_memory: str = None,
        scheduler_class: str = None,
        scheduler_options: dict = None,
        name: str = None,
        asynchronous: bool = False,
        cloud: Cloud = None,
        account: str = None,
        shutdown_on_close=None,
        region: str = None,
        backend_options: Optional[Dict] = None,
    ):
        # we really need to call this first before any of the below code errors
        # out; otherwise because of the fact that this object inherits from
        # deploy.Cloud __del__ (and perhaps __repr__) will have AttributeErrors
        # because the gc will run and attributes like `.status` and
        # `.scheduler_comm` will not have been assigned to the object's instance
        # yet
        super().__init__(asynchronous=asynchronous)

        self.cloud = cloud or Cloud.current(asynchronous=asynchronous)
        if configuration is None:
            v = "".join(map(str, sys.version_info[:2]))
            configuration = f"coiled/default-py{v}"
        self.configuration = configuration
        self.software = software
        self.worker_cpu = worker_cpu
        self.worker_gpu = worker_gpu
        self.worker_memory = worker_memory
        self.worker_class = worker_class
        self.worker_options = worker_options
        self.scheduler_cpu = scheduler_cpu
        self.scheduler_memory = scheduler_memory
        self.scheduler_class = scheduler_class
        self.scheduler_options = scheduler_options
        self.name = name
        self.account = account
        self._start_n_workers = n_workers
        self._lock = None
        self._asynchronous = asynchronous
        self.shutdown_on_close = shutdown_on_close
        self.region = region
        # Start repackaging things like region into backend_options
        self.backend_options = backend_options or {}
        if region:
            warnings.warn(
                "Please use ``backend_options`` for backend specific options like region."
                "region is deprecated and will be removed soon.",
                DeprecationWarning,
            )
            self.backend_options.update({"region": region})
        self.cluster_id = None

        self._name = "coiled.Cluster"  # Used in Dask's Cluster._ipython_display_

        if not self.asynchronous:
            self.sync(self._start)

    @property
    def loop(self):
        return self.cloud.loop

    async def _start(self):
        self.cloud = await self.cloud
        should_create = True

        if self.name:
            self.cluster_id = await self.cloud._get_cluster_by_name(
                name=self.name,
                account=self.account,
                backend_options=self.backend_options,
            )
            if self.cluster_id:
                print(f"Using existing cluster: {self.name}")  # TODO: add timer
                should_create = False
                if self.shutdown_on_close is None:
                    self.shutdown_on_close = False

        self.name = self.name or self.cloud.user + "-" + str(uuid.uuid4())[:10]

        if should_create:
            # TODO: should this check also be upstream on the server?
            acct, name = parse_identifier(self.configuration, "configuration")  # type: ignore
            available_configs = await self.cloud.list_cluster_configurations(  # type: ignore
                account=acct or self.account
            )
            if name not in available_configs:
                error_msg = f"Cluster configuration '{self.configuration}' not found."
                if name in await self.cloud.list_software_environments():  # type: ignore
                    error_msg += (
                        "\n"
                        f"We did find a software environment '{self.configuration}'.\n"
                        "You may need to make a cluster configuration with this \n"
                        "software environment:\n\n"
                        f"  coiled.create_cluster_configuration(name='{self.configuration}', software='{self.configuration}')"  # noqa: E501
                    )
                raise ValueError(error_msg)

            self.cluster_id = await self.cloud.create_cluster(
                account=self.account,
                configuration=self.configuration,  # type: ignore
                name=self.name,
                workers=self._start_n_workers,
                backend_options=self.backend_options,
                software=self.software,
                worker_cpu=self.worker_cpu,
                worker_gpu=self.worker_gpu,
                worker_memory=self.worker_memory,
                worker_class=self.worker_class,
                worker_options=self.worker_options,
                scheduler_cpu=self.scheduler_cpu,
                scheduler_memory=self.scheduler_memory,
                scheduler_class=self.scheduler_class,
                scheduler_options=self.scheduler_options,
            )
            if self._start_n_workers:
                await self._scale(self._start_n_workers)

        self.security, info = await self.cloud.security(
            cluster_id=self.cluster_id, account=self.account  # type: ignore
        )
        self._dashboard_address = info["dashboard_address"]

        self.scheduler_comm = dask.distributed.rpc(
            info["public_address"],
            connection_args=self.security.get_connection_args("client"),
        )

        # If we are lunching a Cluster withing a Coiled Job/Notebook,
        # don't even try to send credentials along
        # TODO: Figure out a way to do this in a clean way

        if "DASK_COILED__JOB_ID" not in os.environ:
            creds = {}
            aws_creds = await self.cloud.get_aws_credentials(self.account)
            session = aiobotocore.get_session()
            async with session.create_client("sts", **aws_creds) as sts:
                try:
                    credentials = await sts.get_session_token()
                    credentials = credentials["Credentials"]
                    creds = {
                        k: credentials[k]
                        for k in ["AccessKeyId", "SecretAccessKey", "SessionToken"]
                    }
                except botocore.errorfactory.ClientError as e:
                    if "session credentials" in str(e):
                        # STS session. Can't request a new session token
                        credentials = await session.get_credentials()
                        credentials = await credentials.get_frozen_credentials()
                        creds = {
                            "AccessKeyId": credentials.access_key,
                            "SecretAccessKey": credentials.secret_key,
                            "SessionToken": credentials.token,
                        }
                except Exception:
                    pass
                if creds:
                    # TODO: set up TTL, and update these credentials periodically
                    await self.scheduler_comm.aws_update_credentials(
                        credentials={
                            k: creds.get(k)
                            for k in ["AccessKeyId", "SecretAccessKey", "SessionToken"]
                        }
                    )

        await super()._start()

        # TODO: Come up with a better long-term solution. Below we raise an informative error message
        # when workers with GPUs take a long time to arrive (due to GPU availability on AWS)
        if (
            should_create
            and self._start_n_workers
            and (self.worker_gpu or available_configs[name]["worker"]["gpu"])  # type: ignore
        ):
            try:
                err_msg = (
                    "GPU workers are not being created. This happens when there is limited GPU availability "
                    "in your AWS region. For example, the default region, us-east-2, often runs out of GPUs while "
                    "other regions like us-west-1 still have capacity. You may want to try moving regions:\n\n"
                    "cluster = coiled.Cluster(..., backend_options={'region': 'us-west-1'}"
                )
                await self._wait_for_workers(1, timeout="10 minutes", err_msg=err_msg)
            except TimeoutError as e:
                await self._close()
                raise e

    async def _wait_for_workers(self, n_workers, timeout=None, err_msg=None):
        if timeout is None:
            deadline = None
        else:
            timeout = dask.utils.parse_timedelta(timeout, "s")
            deadline = time.time() + timeout
        while n_workers and len(self.scheduler_info["workers"]) < n_workers:
            if deadline and time.time() > deadline:
                err_msg = (
                    err_msg
                    or "Timed out after {timeout} seconds waiting for {n_workers} workers to arrive"
                )
                raise TimeoutError(err_msg)
            await asyncio.sleep(1)

    def __await__(self):
        async def _():
            if self._lock is None:
                self._lock = asyncio.Lock()
            async with self._lock:
                if self.status == "created":
                    await self._start()
                assert self.status == "running"
            return self

        return _().__await__()

    async def _close(self):
        if self.shutdown_on_close in (True, None):
            await self.cloud.delete_cluster(
                account=self.account,
                cluster_id=self.cluster_id,  # type: ignore
            )
        await super()._close()

    async def _scale(self, n: int) -> Tuple[List[Dict], List[Dict]]:
        return await self.cloud.scale(
            account=self.account,
            cluster_id=self.cluster_id,  # type: ignore
            n=n,
        )

    def scale(self, n: int) -> Tuple[List[Dict], List[Dict]]:
        """Scale cluster to ``n`` workers

        Parameters
        ----------
        n
            Number of workers to scale cluster size to.
        """
        return self.sync(self._scale, n=n)

    def __enter__(self):
        return self.sync(self.__aenter__)

    def __exit__(self, *args, **kwargs):
        return self.sync(self.__aexit__, *args, **kwargs)

    def get_logs(self, scheduler: bool = True, workers: bool = True) -> dict:
        """Return logs for the scheduler and workers
        Parameters
        ----------
        scheduler : boolean
            Whether or not to collect logs for the scheduler
        workers : boolean
            Whether or not to collect logs for the workers
        Returns
        -------
        logs: Dict[str]
            A dictionary of logs, with one item for the scheduler and one for
            the workers
        """
        return self.sync(self._get_logs, scheduler=scheduler, workers=workers)

    async def _get_logs(self, scheduler: bool = True, workers: bool = True) -> dict:
        return await self.cloud.logs(
            account=self.account, cluster_id=self.cluster_id, scheduler=scheduler, workers=workers  # type: ignore
        )

    @property
    def dashboard_link(self):
        # Only use proxied dashboard address if we're in a hosted notebook
        # Otherwise fall back to the non-proxied address
        if dask.config.get("coiled.dashboard.proxy", False):
            return f"{self.cloud.server}/dashboard/{self.cluster_id}/status"
        else:
            return self._dashboard_address
