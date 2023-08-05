import asyncio
from distutils.util import strtobool
import io
import os
import yaml

import pytest
from distributed.utils_test import loop  # noqa: F401
from dask.distributed import Client

from cloud.models import SoftwareEnvironment
import coiled


def test_please_dont_ignore_software_environment_hash():
    specs_and_hashes = [
        (
            {
                "conda_solved_linux": {
                    "channels": ["conda-forge", "defaults"],
                    "dependencies": [
                        "bokeh>=2.1.1",
                        "bottleneck",
                    ],
                },
            },
            "845ba53dbc",
        ),
        (
            {
                "container": None,
                "pip": ["pandas"],
                "post_build": ["do stuff"],
            },
            "40cb0dfcbd",
        ),
    ]
    for spec, expected_hash in specs_and_hashes:
        hash = SoftwareEnvironment.compute_hash(spec)
        assert hash == expected_hash, "So you've affected the hash! Read more"
    """
    When we create clusters, if the hash doesn't match, the software environment
    will be recreated. This can be a very expensive operation for a user. If this is unnecessary
    (i.e. there was just some change in the code and there's no reason to make
    everyone rebuild), please write a Django migration to update the hash in the
    db. If that's not possible, consider manually rebuilding people's software environments
    when you deploy, otherwise they'll just have to wait for their stuff to rebuild the next time
    they try to create a cluster.

    Either way, update the expected_hash values in this test to expect the new value.

    Sample migration:

    python manage.py makemigrations --empty
    ```
    from django.db import migrations

    from cloud.serializers import SoftwareEnvironmentSerializer
    import dask

    ...copy-pasted code...

    def update_software_environment_hash(apps, schema_editor):
        SoftwareEnvironment = apps.get_model("cloud",  "SoftwareEnvironment")
        for se in SoftwareEnvironment.objects.all():
            # You might want to copy-paste whatever hash code into the migration
            # for posterity, in case, for example SoftwareEnvironments.compute_hash()
            # changes.
            se.content_hash = compute_hash(se)
            se.save()

    class Migration(migrations.Migration):

        dependencies = [
            ('cloud', '0014_remove_scheduler_preload_key'),
        ]

        operations = [
            migrations.RunPython(update_software_environment_hash),
        ]
    ```
    """


@pytest.mark.asyncio
async def test_update_software_environment_conda(cloud, cleanup, sample_user, tmp_path):
    # below is what yaml.load(<env-file>) gives
    out = io.StringIO()
    conda_env = {
        "channels": ["defaults"],
        "dependencies": ["python=3.8"],
    }

    await cloud.create_software_environment(name="env-1", conda=conda_env)
    while True:
        # I fear there are race conditions afoot...
        if await cloud.list_software_environments():
            break
        await asyncio.sleep(0.5)
    await cloud.create_software_environment(
        name="env-1", conda=conda_env, log_output=out
    )

    out.seek(0)
    assert "Found built software environment" in out.read().strip()

    conda_env = {
        "channels": ["defaults"],
        "dependencies": ["python=3.8", "toolz"],
    }

    await cloud.create_software_environment(
        name="env-1", conda=conda_env, log_output=out
    )

    out.seek(0)
    text = out.read()
    assert "conda" in text.lower()
    assert "success" in text.lower() or "solved" in text.lower()


@pytest.mark.asyncio
async def test_update_software_environment_pip_doesnt_overwrite_conda(
    cloud, cleanup, sample_user, tmp_path
):
    # below is what yaml.load(<env-file>) gives
    out = io.StringIO()
    conda_env = {
        "channels": ["defaults"],
        "dependencies": ["python=3.8", "toolz", "aiobotocore"],
    }

    await cloud.create_software_environment(name="env-1", conda=conda_env)
    while True:
        # I fear there are race conditions afoot...
        if await cloud.list_software_environments():
            break
        await asyncio.sleep(0.5)
    await cloud.create_software_environment(
        name="env-1", conda=conda_env, pip=["botocore"], log_output=out
    )

    out.seek(0)
    text = out.read()
    assert "conda" in text.lower()
    assert "requirements.txt" in text.lower()


@pytest.mark.asyncio
async def test_update_software_environment_failure_doesnt_change_db(
    cloud, cleanup, sample_user, tmp_path
):
    before_envs = await cloud.list_software_environments()
    out = io.StringIO()
    conda_env = {
        "channels": ["defaults"],
        "dependencies": [
            "dask",
            "not-a-package",
            "pandas",
        ],
    }
    with pytest.raises(Exception):
        await cloud.create_software_environment(
            name="env-1", conda=conda_env, log_output=out
        )
    out.seek(0)
    text = out.read()
    assert "failed" in text.lower()
    after_envs = await cloud.list_software_environments()
    assert before_envs == after_envs


@pytest.mark.asyncio
async def test_software_environment_pip(cloud, cleanup, sample_user, tmp_path):

    packages = ["toolz", "dask"]
    # Provide a list of packages
    await cloud.create_software_environment(name="env-1", pip=packages)

    while True:
        result = await cloud.list_software_environments()
        if result:
            break
        await asyncio.sleep(0.5)

    # Check output is formatted properly
    assert len(result) == 1
    assert result["env-1"]["account"] == sample_user.user.username
    assert result["env-1"]["container"] is None
    assert result["env-1"]["conda"] is None
    assert result["env-1"]["pip"] == sorted(packages)

    # Provide a local requirements file
    requirements_file = tmp_path / "requirements.txt"
    with requirements_file.open(mode="w") as f:
        f.write("\n".join(packages))

    await cloud.create_software_environment(name="env-2", pip=requirements_file)

    while True:
        result = await cloud.list_software_environments()
        if len(result) == 2:
            break
        await asyncio.sleep(0.5)

    # Check output is formatted properly
    assert len(result) == 2
    assert result["env-2"]["account"] == sample_user.user.username
    assert result["env-2"]["container"] is None
    assert result["env-2"]["conda"] is None
    assert result["env-2"]["pip"] == sorted(packages)


@pytest.mark.asyncio
async def test_software_environment_pip_private(cloud, cleanup, sample_user, tmp_path):

    packages = ["dask==2.15", "git+https://GIT_TOKEN@github.com/coiled/cloud.git"]
    # Provide a list of packages
    out = io.StringIO()
    with pytest.raises(Exception):
        await cloud.create_software_environment(
            name="env-1", pip=packages, log_output=out
        )
    out.seek(0)
    text = out.read()
    assert "setting up private repository" in text.lower()


@pytest.mark.asyncio
async def test_software_environment_conda(cloud, cleanup, sample_user, tmp_path):
    # below is what yaml.load(<env-file>) gives
    conda_env = {
        "channels": ["defaults"],
        "dependencies": ["python=3.8", {"pip": ["toolz"]}],
    }

    # Provide a data structure
    await cloud.create_software_environment(name="env-1", conda=conda_env)

    while True:
        result = await cloud.list_software_environments()
        if result:
            break
        await asyncio.sleep(0.5)

    # Check output is formatted properly
    assert len(result) == 1
    assert result["env-1"]["account"] == sample_user.user.username
    assert result["env-1"]["container"] is None
    assert "python=3.8" in result["env-1"]["conda"]["dependencies"]
    assert "toolz" in result["env-1"]["pip"]

    # Provide a local environment file
    environment_file = tmp_path / "environment.yml"
    with environment_file.open(mode="w") as f:
        f.writelines(yaml.dump(conda_env))

    await cloud.create_software_environment(name="env-2", conda=environment_file)

    while True:
        result = await cloud.list_software_environments()
        if len(result) == 2:
            break
        await asyncio.sleep(0.5)

    # Check output is formatted properly
    assert len(result) == 2
    assert result["env-2"]["account"] == sample_user.user.username
    assert result["env-2"]["container"] is None
    assert "python=3.8" in result["env-2"]["conda"]["dependencies"]
    assert "toolz" in result["env-2"]["pip"]


@pytest.mark.asyncio
async def test_software_environment_container(cloud, cleanup, sample_user, tmp_path):

    # Provide docker image URI
    await cloud.create_software_environment(
        name="env-1", container="daskdev/dask:latest"
    )

    result = await cloud.list_software_environments()

    assert "env-1" in result
    assert "daskdev/dask:latest" in str(result)
    assert "container" in str(result)
    assert sample_user.user.username in str(result)


@pytest.mark.asyncio
async def test_software_environment_multiple_specifications(
    cloud, cleanup, sample_user, tmp_path
):
    container = "continuumio/miniconda:latest"
    conda = {
        "channels": ["defaults"],
        "dependencies": ["python=3.8", {"pip": ["toolz"]}],
    }
    pip = ["requests"]

    # Provide a data structure
    env_name = "env-1"
    await cloud.create_software_environment(
        name=env_name, container=container, conda=conda, pip=pip
    )

    while True:
        result = await cloud.list_software_environments()
        if result:
            break
        await asyncio.sleep(0.5)

    assert result[env_name]["container"] == container
    assert "python=3.8" in result[env_name]["conda"]["dependencies"]
    assert "toolz" in result[env_name]["pip"]
    assert "requests" in result[env_name]["pip"]

    # Provide local environment / requirements files
    environment_file = tmp_path / "environment.yml"
    with environment_file.open(mode="w") as f:
        f.writelines(yaml.dump(conda))

    requirements_file = tmp_path / "requirements.txt"
    with requirements_file.open(mode="w") as f:
        f.write("\n".join(pip))

    env_name = "env-2"
    await cloud.create_software_environment(
        name=env_name,
        container=container,
        conda=environment_file,
        pip=requirements_file,
    )

    while True:
        result = await cloud.list_software_environments()
        if len(result) == 2:
            break
        await asyncio.sleep(0.5)

    assert result[env_name]["container"] == container
    assert "python=3.8" in result[env_name]["conda"]["dependencies"]
    assert "toolz" in result[env_name]["pip"]
    assert "requests" in result[env_name]["pip"]


@pytest.mark.asyncio
async def test_software_environment_post_build(cloud, cleanup, sample_user, tmp_path):

    container = "daskdev/dask:latest"
    post_build = ["export FOO=BAR--BAZ", "echo $FOO"]
    await cloud.create_software_environment(
        name="env-1", container=container, post_build=post_build
    )

    while True:
        results = await cloud.list_software_environments()
        print("WARNING: create_software_environment returned early")
        if results:
            break
        await asyncio.sleep(0.5)

    assert results["env-1"]["post_build"][1:] == post_build

    post_build_file = tmp_path / "postbuild"
    with post_build_file.open(mode="w") as f:
        contents = ["#!/bin/bash"] + post_build
        f.write("\n".join(contents))

    await cloud.create_software_environment(
        name="env-2", container=container, post_build=post_build
    )

    while True:
        results = await cloud.list_software_environments()
        print("WARNING: create_software_environment returned early")
        if len(results) == 2:
            break
        await asyncio.sleep(0.5)

    assert results["env-2"]["post_build"][1:] == post_build


@pytest.mark.asyncio
async def test_delete_software_environment(cloud, cleanup, sample_user):
    # Initially no software environments
    result = await cloud.list_software_environments()
    assert not result

    packages = ["toolz"]

    # Create two configurations
    await cloud.create_software_environment(name="env-1", pip=packages)
    await cloud.create_software_environment(name="env-2", pip=packages)

    while True:
        result = await cloud.list_software_environments()
        print("WARNING: create_software_environment returned early")
        if len(result) == 2:
            break
        await asyncio.sleep(0.5)

    assert len(result) == 2

    # Delete one of the configurations
    await cloud.delete_software_environment(name="env-1")
    result = await cloud.list_software_environments()
    assert len(result) == 1
    assert "env-2" in result


@pytest.mark.skipif(
    not strtobool(os.environ.get("TEST_AGAINST_AWS", "n")),
    reason="ECS only test?",
)
@pytest.mark.asyncio
async def test_docker_images(cloud, cleanup, sample_user, tmp_path, backend):
    spec = {
        "channels": ["defaults"],
        "dependencies": ["python=3.8", "dask", "nomkl"],
    }
    await cloud.create_software_environment(
        pip=["sparse"],
        name="env-1",
        conda=spec,
    )
    while True:
        if await cloud.list_software_environments():
            break
        await asyncio.sleep(0.5)
    await cloud.create_cluster_configuration(
        name="my-config",
        software="env-1",
        worker_cpu=1,
        worker_memory="2 GiB",
    )

    async with coiled.Cluster(asynchronous=True, configuration="my-config") as cluster:
        async with Client(cluster, asynchronous=True) as client:

            def test_import():
                try:
                    import sparse  # noqa: F401

                    return True
                except ImportError:
                    return False

            result = await client.run_on_scheduler(test_import)
            assert result


@pytest.mark.asyncio
async def test_conda_raises(cloud, cleanup, sample_user, tmp_path):
    conda_env = {
        "channels": ["defaults"],
        "dependencies": ["dask", "not-a-package", "pandas", "nomkl"],
    }

    out = io.StringIO()
    with pytest.raises(Exception):
        await cloud.create_software_environment(
            name="env-1", conda=conda_env, log_output=out
        )
    out.seek(0)
    text = out.read()
    assert "failed" in text.lower()
    assert "not-a-package" in text.lower()


@pytest.mark.asyncio
async def test_conda_uses_name(cloud, cleanup):
    conda_env = {
        "name": "my-env",
        "channels": ["defaults"],
        "dependencies": ["python=3.8", "toolz"],
    }

    await cloud.create_software_environment(conda=conda_env)
    while True:
        result = await cloud.list_software_environments()
        if result:
            break
        await asyncio.sleep(0.5)

    assert len(result) == 1
    assert "my-env" in result


@pytest.mark.asyncio
async def test_no_name_raises(cloud, cleanup):
    conda_env = {
        "channels": ["conda-forge"],
        "dependencies": ["toolz"],
    }

    with pytest.raises(ValueError, match="provide a name"):
        await cloud.create_software_environment(conda=conda_env)


@pytest.mark.skipif(
    not strtobool(os.environ.get("TEST_AGAINST_AWS", "n")),
    reason="ECS only test?",
)
@pytest.mark.slow
@pytest.mark.asyncio
async def test_conda_env_name(cloud, cleanup, backend):
    # Ensure that specifying conda_env_name works as expected
    # Regression test for https://github.com/coiled/cloud/issues/779

    conda_env = {
        "name": "foobar",
        "channels": ["conda-forge"],
        "dependencies": ["toolz", "dask>=2.25.0"],
    }

    await cloud.create_software_environment(
        name="test-conda-env-name",
        container="coiled/test-conda-env-name:latest",
        conda=conda_env,
        conda_env_name="foo",
    )
    while True:
        result = await cloud.list_software_environments()
        if result:
            break
        await asyncio.sleep(5)

    await cloud.create_cluster_configuration(
        name="test-conda-env-name", software="test-conda-env-name"
    )
    async with coiled.Cluster(
        asynchronous=True, configuration="test-conda-env-name"
    ) as cluster:
        async with Client(cluster, asynchronous=True) as client:

            def test_import():
                try:
                    import toolz  # noqa: F401

                    return True
                except ImportError:
                    return False

            result = await client.run_on_scheduler(test_import)
            assert result


@pytest.mark.xfail(reason="this actually works if you have OpenGL available")
@pytest.mark.skipif(
    not strtobool(os.environ.get("TEST_AGAINST_AWS", "n")),
    reason="only fails on containers without OpenGL",
)
@pytest.mark.asyncio
async def test_docker_build_reports_failure(cloud, cleanup, sample_user, tmp_path):
    """ Sometime the docker build can fail, even if the conda solve works """
    before_envs = await cloud.list_software_environments()
    out = io.StringIO()
    conda_env = {
        "channels": ["conda-forge"],
        "dependencies": ["napari"],
    }
    with pytest.raises(Exception):
        await cloud.create_software_environment(
            name="env-1", conda=conda_env, log_output=out
        )
    out.seek(0)
    text = out.read()
    assert "Missing OpenGL driver" in text
    assert "failed" in text.lower()

    after_envs = await cloud.list_software_environments()
    assert before_envs == after_envs


@pytest.mark.skipif(
    not strtobool(os.environ.get("TEST_AGAINST_AWS", "n")),
    reason="ECS only test?",
)
@pytest.mark.slow
@pytest.mark.asyncio
async def test_rebuild_docker(cloud, cleanup, sample_user, tmp_path, backend):
    await cloud.create_software_environment(
        name="env-1234",
        conda={
            "channels": ["defaults"],
            "dependencies": ["python=3.8", "dask", "nomkl"],
        },
    )

    await cloud.create_cluster_configuration(
        name="my-config",
        software="env-1234",
        worker_cpu=1,
        worker_memory="2 GiB",
    )

    # Remove image sneakily
    async with backend.session.create_client("ecr") as ecr:
        response = await ecr.list_images(
            repositoryName=SoftwareEnvironment.repo_name(
                sample_user.user.username,
                "env-1234",
            ),
        )
        await ecr.batch_delete_image(
            repositoryName=SoftwareEnvironment.repo_name(
                sample_user.user.username,
                "env-1234",
            ),
            imageIds=response["imageIds"],
        )

    async with coiled.Cluster(asynchronous=True, configuration="my-config") as cluster:
        async with Client(cluster, asynchronous=True):
            pass


@pytest.mark.asyncio
async def test_update_software_environment_privacy(
    cloud, cleanup, sample_user, tmp_path
):
    await cloud.create_software_environment(
        name="env-1", container="daskdev/dask:latest"
    )

    result = await cloud.list_software_environments()
    assert "env-1" in result
    assert result["env-1"]["private"] is False

    await cloud.create_software_environment(
        name="env-1",
        container="daskdev/dask:latest",
        private=True,
    )
    result = await cloud.list_software_environments()

    assert "env-1" in result
    assert result["env-1"]["private"] is False
