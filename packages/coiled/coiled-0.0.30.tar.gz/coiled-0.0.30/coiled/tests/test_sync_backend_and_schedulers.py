import asyncio
from time import time
from channels.db import database_sync_to_async
import pytest

from cloud.models import Scheduler
import coiled


@pytest.mark.skip(reason="When closing we don't want to update status")
@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_ecs_backend_reconcile(
    cloud, cluster_configuration, backend, sample_user, settings
):
    settings.STARTUP_GRACE_PERIOD_SECONDS = 5
    settings.COILED_PERIODIC_CALLBACKS = [
        {
            "callable": "cloud.callbacks.SyncBackendStatus",
            "interval": settings.SYNC_BACKEND_STATUS_FREQUENCY_MS,
        }
    ]

    # Reinitialize our backend so that the periodic callbacks are set up
    from cloud.apps import CloudConfig

    CloudConfig.initialize_periodic_callbacks(CloudConfig.backend)

    cluster_name = "about-to-be-removed"

    # Using helper functions and not our actual methods, so that
    # we don't trigger any "desired" behavior. We're testing for when
    # clusters have gone wild.
    @database_sync_to_async
    def get_status(name):
        c = Scheduler.objects.get(name=name)
        return c.status

    @database_sync_to_async
    def set_status(name, status):
        c = Scheduler.objects.get(name=name)
        c.status = status
        c.save()

    async with coiled.Cluster(
        n_workers=0,
        configuration=cluster_configuration,
        asynchronous=True,
        name=cluster_name,
    ) as cluster:
        # confirming that our cluster is in there
        assert await cloud.list_clusters()
        cluster_info = await cloud._cluster_status(cluster.cluster_id)
        assert cluster_info["status"] == "running"

        # It's actually running in the backend, but let's put the db
        # table out of sync
        await set_status(cluster_name, "pending")

        # We eventually figure out the mismatch and correct it
        start = time()
        while await cloud.list_clusters():
            if (await get_status(cluster_name)) == "running":
                # it has been changed back successfully
                break
            await asyncio.sleep(0.1)
            assert (
                time() < start + 7
            ), "Backend and Scheduler status not put back in sync"
