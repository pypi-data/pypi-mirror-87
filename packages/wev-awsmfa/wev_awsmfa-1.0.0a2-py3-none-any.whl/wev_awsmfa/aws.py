from datetime import datetime
from logging import Logger
from typing import Any, Tuple

from boto3 import client
from wev.sdk.exceptions import CannotResolveError


def discover_mfa_device_arn(logger: Logger) -> str:
    """
    Attempts to discover the ARN of the current identity's MFA device.

    Raises `CannotResolveError` if the device cannot found.
    """
    logger.debug("Requesting MFA devices...")
    iam = client("iam")

    response = iam.list_mfa_devices(MaxItems=2)
    mfa_devices = response.get("MFADevices", None)

    if mfa_devices is None:
        raise CannotResolveError(
            f'"list_mfa_devices" did not return "MFADevices": {response}'
        )

    if len(mfa_devices) == 0:
        raise CannotResolveError("IAM user has no registered MFA devices.")

    if len(mfa_devices) > 1:
        raise CannotResolveError('"list_mfa_devices" returned multiple devices')

    mfa_device = mfa_devices[0]
    serial = mfa_device.get("SerialNumber", None)
    if not serial:
        raise CannotResolveError(
            '"list_mfa_devices" returned a device without a serial number: '
            + str(mfa_device)
        )
    logger.debug("Found device: %s", serial)
    return str(serial)


def get_session_token(
    logger: Logger,
    duration: int,
    serial: str,
    token: str,
) -> Tuple[Tuple[str, str, str], datetime]:
    """
    Attempts to get a session token for the current identity with the given
    MFA token.

    Returns a tuple holding the access key, secret key and session token, and
    the credentials' expiration date.
    """
    sts = client("sts")
    logger.debug("Requesting session token...")
    try:
        response = sts.get_session_token(
            DurationSeconds=duration,
            SerialNumber=serial,
            TokenCode=token,
        )
    except sts.exceptions.ClientError as ex:
        raise CannotResolveError(ex)

    credentials = response.get("Credentials", None)
    if credentials is None:
        raise CannotResolveError(
            f'"get_session_token" did not return "Credentials": {response}'
        )

    return (
        (
            get_credential_str(credentials, "AccessKeyId"),
            get_credential_str(credentials, "SecretAccessKey"),
            get_credential_str(credentials, "SessionToken"),
        ),
        get_credential_datetime(credentials, "Expiration"),
    )


def get_credential_str(credentials: Any, key: str) -> str:
    if value := str(credentials.get(key, "")):
        return value

    raise CannotResolveError(
        f'"get_session_token" returned credentials without "{key}": {credentials}'
    )


def get_credential_datetime(credentials: Any, key: str) -> datetime:
    value = credentials.get(key, None)
    if value is None:
        raise CannotResolveError(
            f'"get_session_token" returned credentials without "{key}": {credentials}'
        )
    if not isinstance(value, datetime):
        raise CannotResolveError(
            f'"get_session_token" did not return credential key "{key}" as datetime: '
            + str(credentials)
        )
    return value
