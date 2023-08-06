from logging import Logger
from typing import List, Optional

from wev.sdk import PluginBase, Resolution, ResolutionSupport

from wev_awsmfa.aws import discover_mfa_device_arn, get_session_token


class Plugin(PluginBase):
    """
    `wev-awsmfa` plugin.
    """

    def explain(self, logger: Logger) -> List[str]:
        """
        Gets a human-readable explanation of how this plugin will resolve the
        environment variable.

        `logger` should be used for logging debug information and not for
        returning the explanation.
        """
        if mfa_device_arn := self.get_mfa_device(logger=logger):
            msg = (
                "You will be prompted to enter your MFA token, then "
                f'authenticated via device "{mfa_device_arn}".'
            )
        else:
            msg = (
                "Your MFA device will be looked-up in AWS, then you will be "
                "prompted to enter your token."
            )

        duration = self.get_duration(logger=logger)

        return [
            msg,
            f"Your new session will be cached for {duration} seconds.",
        ]

    def resolve(self, support: ResolutionSupport) -> Resolution:
        """
        Resolves the environment variable.
        """
        mfa_device_arn = self.get_mfa_device(logger=support.logger)
        if not mfa_device_arn:
            mfa_device_arn = discover_mfa_device_arn(logger=support.logger)
        response = get_session_token(
            logger=support.logger,
            duration=self.get_duration(logger=support.logger),
            serial=mfa_device_arn,
            token=support.confidential_prompt("We need your token.", "Token:"),
        )

        return Resolution.make(value=response[0], expires_at=response[1])

    def get_duration(self, logger: Logger) -> int:
        """
        Gets the requested duration of the new session. Defaults to 15 minutes.
        """
        if value := self.get("duration", None):
            duration = int(value)
            logger.debug("Found duration in configuration: %s seconds", duration)
            return duration
        default_duration = 15 * 60
        logger.debug(
            "No duration in configuration. Defaulting to %s seconds.", default_duration
        )
        return default_duration

    def get_mfa_device(self, logger: Logger) -> Optional[str]:
        """
        Gets the MFA device ARN from the configuration, or `None` if the device
        is not configured.
        """
        if value := self.get("mfa_device", None):
            arn = str(value)
            logger.debug("Found MFA device in configuration: %s", arn)
            return arn
        logger.debug("No MFA device in configuration.")
        return None
