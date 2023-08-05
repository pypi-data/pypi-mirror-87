import os
import pprint
import shutil
import stat
import yaml


import click
import dask
from distributed.utils import tmpfile

from .utils import (
    conda_package_versions,
    conda_command,
    CONTEXT_SETTINGS,
)
from ..core import Cloud
from ..utils import (
    parse_identifier,
    ParseIdentifierError,
    get_platform,
    run_command_in_subprocess,
)

DEFAULT_PIP_PACKAGES = ["coiled", "ipython", "ipykernel"]


@click.command(
    context_settings=CONTEXT_SETTINGS,
    help="Create Coiled conda software environment locally",
)
@click.argument("coiled_uri")
def install(coiled_uri: str):
    """Create a Coiled software environment locally

    Parameters
    ----------
    coiled_uri
        Identifier of the software environment to use, in the format (<account>/)<name>. If the software environment
        is owned by the same account as that passed into "account", the (<account>/) prefix is optional.

        For example, suppose your account is "wondercorp", but your friends at "friendlycorp" have an environment
        named "xgboost" that you want to use; you can specify this with "friendlycorp/xgboost". If you simply
        entered "xgboost", this is shorthand for "wondercorp/xgboost".

        The "name" portion of (<account>/)<name> can only contain ASCII letters, hyphens and underscores.

    Examples
    --------
    >>> import coiled
    >>> coiled.install("coiled/default")

    """

    if shutil.which("conda") is None:
        raise RuntimeError("Conda must be installed in order to use 'coiled install'")

    # Validate input coiled_uri
    try:
        account, name = parse_identifier(coiled_uri, "coiled_uri")
    except ParseIdentifierError:
        account, name = None, None

    account = account or dask.config.get("coiled.user")

    if account is None:
        raise Exception(
            f'Invalid coiled_uri, should be in the format of "<account>/<env_name>" but got "{coiled_uri}"'
        )

    software_env_name = f"{account}/{name}"
    local_env_name = remote_name_to_local_name(account, name)
    with Cloud() as cloud:
        spec = cloud.get_software_info(software_env_name)
        # Run on the Cloud's event loop runner to avoid "RuntimeError: This event loop is already running"
        cloud._loop_runner.run_sync(
            create_local_env, account, name, software_env_name, local_env_name, spec
        )


def remote_name_to_local_name(account, name):
    """Convert remote software environment name to name used locally"""
    return f"coiled-{account}-{name}"


async def create_local_env(account, name, software_env_name, local_env_name, spec):
    """Create local conda environment from Coiled software environment"""
    # Get conda packages installed locally
    local_packages = conda_package_versions(local_env_name)

    # Get packages installed remotely
    solved_spec = spec[f"conda_solved_{get_platform()}"]
    if solved_spec == "":  # Conda packages in spec, but not able to solve on platform
        raise ValueError(
            f"Could not find a solved conda environment for {software_env_name} "
            f"on {get_platform()}. The conda specification for {software_env_name} is:"
            f"\n\n{pprint.pformat(spec['conda'])}"
        )
    elif solved_spec is None:  # No conda packages in software spec
        # Note that even if no conda pacakages are in the remote software environment,
        # we still need to create a local conda environment
        solved_spec = {"dependencies": ["python", "pip"]}
        remote_packages = None
    else:
        remote_packages = spec_to_package_version(solved_spec)

    # Create local conda environment, if needed
    if remote_packages is None or any(
        local_packages.get(package) != version
        for package, version in remote_packages.items()
    ):
        print(f"Creating local conda environment for {software_env_name}")
        await create_conda_env(name=local_env_name, solved_spec=solved_spec)
    else:
        print(f"Local software environment for {software_env_name} found!")

    # Install pip packages
    if spec["pip"]:
        print("Installing pip packages")
        await install_pip_packages(name=local_env_name, pip_packages=spec["pip"])

    # Note we do two separate pip installs to avoid "Double requirement given" error
    await install_pip_packages(name=local_env_name, pip_packages=DEFAULT_PIP_PACKAGES)

    # Run post build commands
    if spec["post_build"]:
        print("Running post-build commands")
        await run_post_build(name=local_env_name, post_build=spec["post_build"])

    print(
        f"Created local conda environment for {software_env_name}"
        f"\n\nTo activate this environment, use"
        f"\n\n\tconda activate {local_env_name}\n"
    )

    # TODO: Activate local conda environment


def spec_to_package_version(spec: dict) -> dict:
    """Formats package version information

    Parameters
    ----------
    spec
        Solved Coiled conda software environment spec

    Returns
    -------
        Mapping that contains the name and version of each package
        in the spec
    """
    dependencies = spec.get("dependencies", {})
    result = {}
    for dep in dependencies:
        package, version = dep.split("=")
        result[package] = version
    return result


async def create_conda_env(name: str, solved_spec: dict):
    """Create a local conda environment from a solved Coiled conda spec

    Parameters
    ----------
    name
        Name of the local conda environment to create
    solved_spec
        Solved conda spec for Coiled software environment
    """
    # Run conda env create locally
    with tmpfile(extension="yml") as fn:
        with open(fn, mode="w") as f:
            yaml.dump(solved_spec, f)

        conda_create_cmd = f"{conda_command()} env create --force -n {name} -f {f.name}"
        async for line in run_command_in_subprocess(conda_create_cmd):
            print(line)


async def install_pip_packages(name: str, pip_packages: list):
    """Install pip packages into local conda environment

    Parameters
    ----------
    name
        Name of the local conda environment to create
    pip_packages
        List of pip packages to install
    """
    with tmpfile(extension="txt") as fn:
        with open(fn, mode="w") as f:
            f.write("\n".join(pip_packages))

        pip_install_cmd = f"{conda_command()} run -n {name} pip install -r {f.name}"
        async for line in run_command_in_subprocess(pip_install_cmd):
            print(line)


async def run_post_build(name: str, post_build: list):
    """Run post-build commands in local conda environment

    Parameters
    ----------
    name
        Name of the local conda environment to run post-build commands in
    post_build
        Contents of post-build script
    """
    with tmpfile(extension="postbuild") as fn:
        with open(fn, mode="w") as f:
            f.write("\n".join(post_build))
        # Make post-build script executable
        st = os.stat(f.name)
        os.chmod(f.name, st.st_mode | stat.S_IEXEC)
        # Run post-build script in conda environment
        command = f"{conda_command()} run -n {name} {f.name}"
        async for line in run_command_in_subprocess(command):
            print(line)
