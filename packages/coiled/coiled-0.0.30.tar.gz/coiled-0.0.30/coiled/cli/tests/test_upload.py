import shutil
from unittest import mock

from click.testing import CliRunner
import pytest

import coiled
from coiled.cli.upload import upload
from ..utils import parse_conda_command, conda_command
from ...utils import ExperimentalFeatureWarning


if shutil.which("conda") is None:
    pytest.skip(
        "Conda is needed to upload local software environments", allow_module_level=True
    )


@pytest.mark.veryslow
def test_upload(sample_user):
    name = "coiled-test-foo"
    parse_conda_command(
        [conda_command(), "create", "-y", "-q", "--name", name, "--json", "toolz"]
    )

    assert name not in coiled.list_software_environments()

    runner = CliRunner()
    with pytest.warns(ExperimentalFeatureWarning):
        result = runner.invoke(upload, args=f"--name {name}")
    assert result.exit_code == 0

    assert name in coiled.list_software_environments()


@pytest.mark.xfail(reason="unknown")
def test_upload_raises():

    with mock.patch("os.environ"):
        runner = CliRunner()
        with pytest.warns(ExperimentalFeatureWarning):
            result = runner.invoke(upload)

    assert result.exit_code != 0
    err_msg = str(result.exception).lower()
    assert "cannot be determined" in err_msg
    assert "--name" in err_msg
    assert "activate" in err_msg
