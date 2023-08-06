from datetime import datetime
from logging import Logger

from mock import Mock, patch
from pytest import mark, raises
from wev.sdk.exceptions import CannotResolveError

from wev_awsmfa.aws import discover_mfa_device_arn, get_session_token


def test_discover_mfa_device_arn(logger: Logger) -> None:
    response = {"MFADevices": [{"SerialNumber": "foo"}]}
    with patch("wev_awsmfa.aws.client") as client_maker:
        client = Mock()
        client.list_mfa_devices = Mock(return_value=response)
        client_maker.return_value = client
        assert discover_mfa_device_arn(logger=logger) == "foo"


@mark.parametrize(
    "response, expect",
    [
        (
            {"foo": "bar"},
            "\"list_mfa_devices\" did not return \"MFADevices\": {'foo': 'bar'}",
        ),
        (
            {"MFADevices": []},
            "IAM user has no registered MFA devices.",
        ),
        (
            {"MFADevices": [{}, {}]},
            '"list_mfa_devices" returned multiple devices',
        ),
        (
            {"MFADevices": [{"foo": "bar"}]},
            (
                '"list_mfa_devices" returned a device without a serial number: '
                "{'foo': 'bar'}"
            ),
        ),
    ],
)
def test_discover_mfa_device_arn__fail(
    response: dict, expect: str, logger: Logger
) -> None:
    with raises(CannotResolveError) as ex:
        with patch("wev_awsmfa.aws.client") as client_maker:
            client = Mock()
            client.list_mfa_devices = Mock(return_value=response)
            client_maker.return_value = client
            discover_mfa_device_arn(logger=logger)
    assert str(ex.value) == expect


def test_get_session_token(logger: Logger) -> None:
    response = {
        "Credentials": {
            "AccessKeyId": "alpha",
            "SecretAccessKey": "beta",
            "SessionToken": "gamma",
            "Expiration": datetime.fromisoformat("2020-01-01 00:00:00"),
        }
    }
    with patch("wev_awsmfa.aws.client") as client_maker:
        client = Mock()
        client.get_session_token = Mock(return_value=response)
        client_maker.return_value = client
        actual = get_session_token(logger=logger, duration=0, serial="", token="")

    assert actual == (
        ("alpha", "beta", "gamma"),
        datetime.fromisoformat("2020-01-01 00:00:00"),
    )


@mark.parametrize(
    "response, expect",
    [
        (
            {"foo": "bar"},
            "\"get_session_token\" did not return \"Credentials\": {'foo': 'bar'}",
        ),
        (
            {"Credentials": {"foo": "bar"}},
            (
                '"get_session_token" returned credentials without '
                "\"AccessKeyId\": {'foo': 'bar'}"
            ),
        ),
        (
            {"Credentials": {"AccessKeyId": "alpha"}},
            (
                '"get_session_token" returned credentials without '
                "\"SecretAccessKey\": {'AccessKeyId': 'alpha'}"
            ),
        ),
        (
            {
                "Credentials": {
                    "AccessKeyId": "alpha",
                    "SecretAccessKey": "beta",
                    "SessionToken": "gamma",
                }
            },
            (
                '"get_session_token" returned credentials without '
                "\"Expiration\": {'AccessKeyId': 'alpha', 'SecretAccessKey': "
                "'beta', 'SessionToken': 'gamma'}"
            ),
        ),
        (
            {
                "Credentials": {
                    "AccessKeyId": "alpha",
                    "SecretAccessKey": "beta",
                    "SessionToken": "gamma",
                    "Expiration": "delta",
                }
            },
            (
                '"get_session_token" did not return credential key '
                "\"Expiration\" as datetime: {'AccessKeyId': 'alpha', "
                "'SecretAccessKey': 'beta', 'SessionToken': 'gamma', "
                "'Expiration': 'delta'}"
            ),
        ),
    ],
)
def test_get_session_token__fail(response: dict, expect: str, logger: Logger) -> None:
    with raises(CannotResolveError) as ex:
        with patch("wev_awsmfa.aws.client") as client_maker:
            client = Mock()
            client.get_session_token = Mock(return_value=response)
            client_maker.return_value = client
            get_session_token(logger=logger, duration=0, serial="", token="")
    assert str(ex.value) == expect
