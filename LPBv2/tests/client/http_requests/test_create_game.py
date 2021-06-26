from LPBv2.client import CreateGame
from .mock_http_connection import MockHTTPConnection, TeamFullException
from LPBv2.common import RolePreference
import pytest


@pytest.fixture
def create_game():
    return CreateGame(role=RolePreference(), connection=MockHTTPConnection())


def test_create_game_init(create_game):
    assert isinstance(create_game.http, MockHTTPConnection)
    assert isinstance(create_game.role, RolePreference)


lobby = "/lol-lobby/v2/lobby"


@pytest.mark.asyncio
async def test_create_ranked_game(create_game):
    await create_game.create_ranked_game()
    assert create_game.http.endpoint[0] == lobby
    assert create_game.http.data[0] == {"queueId": 420}


@pytest.mark.asyncio
async def test_create_normal_game(create_game):
    await create_game.create_normal_game()
    assert create_game.http.endpoint[0] == lobby
    assert create_game.http.data[0] == {"queueId": 430}


@pytest.mark.asyncio
async def test_create_coop_game(create_game):
    await create_game.create_coop_game()
    assert create_game.http.endpoint[0] == lobby
    assert create_game.http.data[0] == {"queueId": 830}


@pytest.mark.asyncio
async def test_create_custom_game(create_game):
    await create_game.create_custom_game()
    assert create_game.http.endpoint[0] == lobby
    assert create_game.http.data[0]["isCustom"] == True


@pytest.mark.asyncio
async def test_select_lane_position_empty(create_game):
    preferences = "/lol-lobby/v2/lobby/members/localMember/position-preferences"
    await create_game.select_lane_position()
    assert create_game.http.endpoint[0] == preferences
    assert create_game.http.data[0]["firstPreference"] == "FILL"
    assert create_game.http.data[0]["secondPreference"] == "FILL"


@pytest.mark.asyncio
async def test_select_lane_position_partial():
    create_game = CreateGame(
        role=RolePreference(first="TOP"),
        connection=MockHTTPConnection(),
    )
    preferences = "/lol-lobby/v2/lobby/members/localMember/position-preferences"
    await create_game.select_lane_position()
    assert create_game.http.endpoint[0] == preferences
    assert create_game.http.data[0]["firstPreference"] == "TOP"
    assert create_game.http.data[0]["secondPreference"] == "FILL"


@pytest.mark.asyncio
async def test_select_lane_position_full():
    create_game = CreateGame(
        role=RolePreference(first="TOP", second="MIDDLE"),
        connection=MockHTTPConnection(),
    )
    preferences = "/lol-lobby/v2/lobby/members/localMember/position-preferences"
    await create_game.select_lane_position()
    assert create_game.http.endpoint[0] == preferences
    assert create_game.http.data[0]["firstPreference"] == "TOP"
    assert create_game.http.data[0]["secondPreference"] == "MIDDLE"


@pytest.mark.asyncio
async def test_select_lane_position_assigned_later():
    role_pref = RolePreference()
    create_game = CreateGame(
        role=role_pref,
        connection=MockHTTPConnection(),
    )
    role_pref.first = "TOP"
    role_pref.second = "MIDDLE"
    preferences = "/lol-lobby/v2/lobby/members/localMember/position-preferences"
    await create_game.select_lane_position()
    assert create_game.http.endpoint[0] == preferences
    assert create_game.http.data[0]["firstPreference"] == "TOP"
    assert create_game.http.data[0]["secondPreference"] == "MIDDLE"


bots = "/lol-lobby/v1/lobby/custom/bots"


@pytest.mark.asyncio
async def test_add_bot_with_config(create_game):
    await create_game.add_bot(champion_id=55, bot_difficulty="EASY", team="CHAOS")
    assert create_game.http.endpoint[0] == bots
    assert create_game.http.data[0]["championId"] == 55
    assert create_game.http.data[0]["botDifficulty"] == "EASY"
    assert create_game.http.data[0]["teamId"] == "200"


@pytest.mark.asyncio
async def test_add_bot_with_partial_config(create_game):
    await create_game.add_bot(bot_difficulty="DOOM")
    assert create_game.http.endpoint[0] == bots
    assert isinstance(create_game.http.data[0]["championId"], int)
    assert create_game.http.data[0]["botDifficulty"] == "DOOM"
    assert create_game.http.data[0]["teamId"] == "200"


@pytest.mark.asyncio
async def test_add_bot_without_config(create_game):
    await create_game.add_bot()
    assert create_game.http.endpoint[0] == bots
    assert isinstance(create_game.http.data[0]["championId"], int)
    assert create_game.http.data[0]["botDifficulty"] == "EASY"
    assert create_game.http.data[0]["teamId"] == "200"


@pytest.mark.asyncio
async def test_fill_with_bots_with_config(create_game):
    with pytest.raises(TeamFullException):
        await create_game.fill_with_bots(bot_difficulty="EASY", team="ORDER")
    assert isinstance(create_game.http.data[0]["championId"], int)
    assert create_game.http.data[0]["botDifficulty"] == "EASY"
    assert create_game.http.data[0]["teamId"] == "100"
    assert len(create_game.http.data) == 5


@pytest.mark.asyncio
async def test_fill_with_bots_without_config(create_game):
    with pytest.raises(TeamFullException):
        await create_game.fill_with_bots()
    assert isinstance(create_game.http.data[0]["championId"], int)
    assert create_game.http.data[0]["botDifficulty"] == "EASY"
    assert create_game.http.data[0]["teamId"] == "200"
    assert len(create_game.http.data) == 5


is_matchmaking = "/lol-lobby/v2/lobby/matchmaking/search-state"
matchmaking = "/lol-lobby/v2/lobby/matchmaking/search"


@pytest.mark.asyncio
async def test_is_matchmaking(create_game):
    await create_game.is_matchmaking()
    assert create_game.http.endpoint[0] == is_matchmaking


@pytest.mark.asyncio
async def test_start_matchmaking(create_game):
    await create_game.start_matchmaking()
    assert create_game.http.endpoint[0] == matchmaking
    assert create_game.http.endpoint[1] == is_matchmaking


champ_selection = "/lol-lobby/v1/lobby/custom/start-champ-select"


@pytest.mark.asyncio
async def test_start_champ_selection(create_game):
    await create_game.start_champ_selection()
    assert create_game.http.endpoint[0] == champ_selection
