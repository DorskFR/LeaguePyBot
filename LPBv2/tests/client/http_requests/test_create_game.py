from LPBv2.client import CreateGame
from .mock_http_connection import MockHTTPConnection
import pytest


@pytest.fixture
def create_game():
    return CreateGame(connection=MockHTTPConnection())


def test_create_game_init(create_game):
    assert isinstance(create_game.http, MockHTTPConnection)


lobby = "/lol-lobby/v2/lobby"
is_matchmaking = "/lol-lobby/v2/lobby/matchmaking/search-state"
start_matchmaking = "/lol-lobby/v2/lobby/matchmaking/search"


@pytest.mark.asyncio
async def test_create_ranked_game(create_game):
    await create_game.create_ranked_game()
    assert create_game.http.endpoint[0] == lobby
    assert create_game.http.data[0] == {"queueId": 420}
    assert create_game.http.endpoint[1] == is_matchmaking
    # assert create_game.http.endpoint[0] == start_matchmaking


@pytest.mark.asyncio
async def test_create_normal_game(create_game):
    pass


@pytest.mark.asyncio
async def test_choose_lane_position(create_game):
    pass


@pytest.mark.asyncio
async def test_start_matchmaking(create_game):
    pass


@pytest.mark.asyncio
async def test_create_coop_game(create_game):
    pass


@pytest.mark.asyncio
async def test_create_custom_game(create_game):
    pass


@pytest.mark.asyncio
async def test_add_bots(create_game):
    pass


@pytest.mark.asyncio
async def test_is_matchmaking(create_game):
    pass


@pytest.mark.asyncio
async def test_start_matchmaking(create_game):
    pass
