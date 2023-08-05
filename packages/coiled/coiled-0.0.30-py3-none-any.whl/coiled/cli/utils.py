import json
import os
import subprocess


CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


def conda_command():
    return os.environ.get("CONDA_EXE", "conda")


def parse_conda_command(cmd: list):
    if not any("json" in i for i in cmd):
        raise ValueError(
            "Attempting to parse conda command output with no json options specified"
        )
    output = subprocess.check_output(cmd)
    result = json.loads(output)
    return result


def conda_package_versions(name: str) -> dict:
    """Return pacakge name and version for each conda installed pacakge

    Parameters
    ----------
    name
        Name of conda environment

    Returns
    -------
    results
        Mapping that contains the name and version of each installed package
        in the environment
    """
    cmd = [conda_command(), "env", "export", "-n", name, "--no-build", "--json"]
    output = parse_conda_command(cmd)
    output = output.get("dependencies", [])
    results = {}
    for i in output:
        if isinstance(i, str):
            package, version = i.split("=")
            results[package] = version
        else:
            # TODO: Use pip installed package information which is currently ignored
            assert isinstance(i, dict), type(i)
            assert list(i.keys()) == ["pip"], list(i.keys())
    return results
