from logging import DEBUG, Logger, basicConfig, getLogger

from pytest import fixture


@fixture
def logger() -> Logger:
    basicConfig()
    getLogger("wev-awsmfa").level = DEBUG
    return getLogger("wev-awsmfa")
