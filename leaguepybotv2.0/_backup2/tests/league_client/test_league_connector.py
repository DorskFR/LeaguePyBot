import pytest
from ..league_client import LeagueConnector, Lockfile
from ..common.models import ClientResponse, WebsocketEvent


@pytest.fixture
def league_connector():
    return LeagueConnector()


def test_league_connector_object(league_connector):
    assert isinstance(league_connector, LeagueConnector)


def test_league_connector_lockfile(league_connector):
    assert isinstance(league_connector.lockfile, Lockfile)


def test_league_connector_make_url(league_connector):
    league_connector.lockfile.port = 1234
    url = league_connector.make_url("/test")
    assert url == "https://127.0.0.1:1234/test"


@pytest.mark.asyncio
async def test_league_connector_request_get(league_connector):
    response = await league_connector.request(
        method="GET", endpoint="/lol-summoner/v1/current-summoner"
    )
    assert isinstance(response, ClientResponse)
    assert isinstance(response.status_code, int)
    assert response


@pytest.mark.asyncio
async def test_league_connector_request_post(league_connector):
    response = await league_connector.request(
        method="POST",
        endpoint="/lol-lobby/v2/matchmaking/quick-search",
        payload={"lobbyChange": "true"},
    )
    assert isinstance(response, ClientResponse)
    assert isinstance(response.status_code, int)
    assert response


@pytest.mark.asyncio
async def test_league_connector_empty_events(league_connector):
    assert isinstance(league_connector.events, list)
    assert len(league_connector.events) == 0


def say_hello():
    print("Hello")


@pytest.mark.asyncio
async def test_league_connector_event():
    league_connector = LeagueConnector(
        events=[WebsocketEvent(endpoint="/", type="UPDATE", function=say_hello)]
    )
    assert isinstance(league_connector.events, list)
    assert len(league_connector.events) > 0
    assert isinstance(league_connector.events[0], WebsocketEvent)
