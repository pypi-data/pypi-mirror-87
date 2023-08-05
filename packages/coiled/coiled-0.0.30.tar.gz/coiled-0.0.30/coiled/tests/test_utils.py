import sys
from typing import Tuple

import pytest

from coiled.utils import (
    parse_identifier,
    ParseIdentifierError,
    get_platform,
    normalize_server,
)


@pytest.mark.parametrize(
    "identifier,expected",
    [
        ("coiled/xgboost", ("coiled", "xgboost")),
        ("xgboost", (None, "xgboost")),
        ("coiled/xgboost-py37", ("coiled", "xgboost-py37")),
        ("xgboost_py38", (None, "xgboost_py38")),
    ],
)
def test_parse_good_names(identifier, expected: Tuple[str, str]):
    account, name = parse_identifier(identifier, "name_that_would_be_printed_in_error")
    assert (account, name) == expected


@pytest.mark.parametrize(
    "identifier",
    [
        "coiled/dan/xgboost",
        "coiled/dan?xgboost",
        "dan\\xgboost",
        "jimmy/xgbóst",
        "",
    ],
)
def test_parse_bad_names(identifier):
    with pytest.raises(ParseIdentifierError) as e:
        parse_identifier(identifier, "software_environment")
    assert "software_environment" in e.value.args[0]


def test_get_platform(monkeypatch):
    with monkeypatch.context() as m:
        monkeypatch.setattr(sys, "platform", "linux")
        assert get_platform() == "linux"

    with monkeypatch.context() as m:
        m.setattr(sys, "platform", "darwin")
        assert get_platform() == "osx"

    with monkeypatch.context() as m:
        m.setattr(sys, "platform", "win32")
        assert get_platform() == "windows"

    with monkeypatch.context() as m:
        m.setattr(sys, "platform", "bad-platform")
        with pytest.raises(ValueError) as result:
            assert get_platform() == "windows"

        err_msg = str(result).lower()
        assert "invalid" in err_msg
        assert "bad-platform" in err_msg


def test_normalize_server():
    assert normalize_server("http://beta.coiledhq.com") == "https://cloud.coiled.io"
    assert normalize_server("https://beta.coiled.io") == "https://cloud.coiled.io"
