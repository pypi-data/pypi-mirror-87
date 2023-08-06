from datetime import datetime
from logging import Logger
from typing import Iterable, List

from _pytest.fixtures import fixture
from mock import Mock, patch
from pytest import mark

from wev_awsmfa import Plugin


@mark.parametrize(
    "values, expect",
    [
        (
            {},
            [
                "Your MFA device will be looked-up in AWS, then you will be "
                "prompted to enter your token.",
                "Your new session will be cached for 900 seconds.",
            ],
        ),
        (
            {"mfa_device": "foo"},
            [
                "You will be prompted to enter your MFA token, then "
                'authenticated via device "foo".',
                "Your new session will be cached for 900 seconds.",
            ],
        ),
        (
            {"duration": 901},
            [
                "Your MFA device will be looked-up in AWS, then you will be "
                "prompted to enter your token.",
                "Your new session will be cached for 901 seconds.",
            ],
        ),
    ],
)
def test_explain(values: dict, expect: List[str], logger: Logger) -> None:
    assert Plugin(values).explain(logger=logger) == expect


@fixture
def discover_mfa_device_arn() -> Iterable[Mock]:
    with patch(
        "wev_awsmfa.plugin.discover_mfa_device_arn", return_value="bar"
    ) as patched:
        yield patched


@fixture
def get_session_token() -> Iterable[Mock]:
    response = (
        ("alpha", "beta", "gamma"),
        datetime.fromisoformat("2020-01-01 00:00:00"),
    )
    with patch("wev_awsmfa.plugin.get_session_token", return_value=response) as patched:
        yield patched


@fixture
def resolution_make() -> Iterable[Mock]:
    with patch("wev_awsmfa.plugin.Resolution.make") as patched:
        yield patched


def test_resolve(
    discover_mfa_device_arn: Mock,
    get_session_token: Mock,
    resolution_make: Mock,
) -> None:
    plugin = Plugin({})
    plugin.resolve(support=Mock())
    resolution_make.assert_called_with(
        value=("alpha", "beta", "gamma"),
        expires_at=datetime.fromisoformat("2020-01-01 00:00:00"),
    )
