import pytest
from LPBv2.client import HTTPConnection, Lockfile
from LPBv2.common import ClientResponse


@pytest.fixture
def http_connection():
    return HTTPConnection()


def test_http_connection_object(http_connection):
    assert isinstance(http_connection, HTTPConnection)


def test_http_connection_lockfile(http_connection):
    assert isinstance(http_connection.lockfile, Lockfile)


def test_http_connection_make_url(http_connection):
    http_connection.lockfile.port = 1234
    url = http_connection.make_url("/test")
    assert url == "https://127.0.0.1:1234/test"


@pytest.mark.asyncio
async def test_http_connection_request_get(http_connection):
    response = await http_connection.request(
        method="GET", endpoint="/lol-summoner/v1/current-summoner"
    )
    assert isinstance(response, ClientResponse)
    assert isinstance(response.status_code, int)
    assert response


@pytest.mark.asyncio
async def test_http_connection_request_post(http_connection):
    response = await http_connection.request(
        method="POST",
        endpoint="/lol-lobby/v2/matchmaking/quick-search",
        payload={"lobbyChange": "true"},
    )
    assert isinstance(response, ClientResponse)
    assert isinstance(response.status_code, int)
    assert response
