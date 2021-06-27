from LPBv2.client import ReadyCheck
from .mock_http_connection import MockHTTPConnection
from .mock_ready_check_event import ready_check_event
import pytest


@pytest.fixture
def ready_check():
    return ReadyCheck(connection=MockHTTPConnection())


def test_ready_check_init(ready_check):
    assert isinstance(ready_check.http, MockHTTPConnection)


@pytest.mark.asyncio
async def test_ready_check_accept(ready_check):
    await ready_check.accept(ready_check_event)
    assert ready_check.http.endpoint[0] == "/lol-matchmaking/v1/ready-check/accept"
