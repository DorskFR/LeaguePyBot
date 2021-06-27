from LPBv2.client import Honor
from .mock_http_connection import MockHTTPConnection
import pytest
from LPBv2.common import TeamMember


@pytest.fixture
def honor():
    return Honor(connection=MockHTTPConnection())


def test_honor_init(honor):
    assert isinstance(honor.http, MockHTTPConnection)


@pytest.mark.asyncio
async def test_get_command_ballot(honor):
    result = await honor.get_command_ballot()
    assert honor.http.endpoint[0] == "/lol-honor-v2/v1/ballot"
    assert result == ["Luke", "Leia", "Lando", "Chewbacca", "C3PO"]


@pytest.mark.asyncio
async def test_get_eog_player_list(honor):
    players = await honor.get_eog_player_list()
    assert isinstance(players, list)
    assert isinstance(players[0], TeamMember)
    assert players[0].summonerName == "MVPython"


@pytest.mark.asyncio
async def test_get_game_id(honor):
    game_id = await honor.get_game_id()
    assert game_id == 309453646


@pytest.mark.asyncio
async def test_command_player(honor):
    game_id = await honor.get_game_id()
    players = await honor.get_eog_player_list()
    await honor.command_player(game_id, players[0])
    assert honor.http.endpoint[2] == "/lol-honor-v2/v1/honor-player"
    assert honor.http.data[2]["summonerId"] == 2592564405913376

@pytest.mark.asyncio
async def test_command_random_player(honor):
    await honor.command_random_player()
    assert honor.http.endpoint[2] == "/lol-honor-v2/v1/honor-player"
    assert isinstance(honor.http.data[2]["summonerId"], int)


@pytest.mark.asyncio
async def test_command_all_players(honor):
    await honor.command_all_players()
    for i in range(2,7):
        assert honor.http.endpoint[i] == "/lol-honor-v2/v1/honor-player"
        assert isinstance(honor.http.data[i]["summonerId"], int)


@pytest.mark.asyncio
async def test_report_player(honor):
    game_id = await honor.get_game_id()
    players = await honor.get_eog_player_list()
    await honor.report_player(game_id, players[0])
    assert honor.http.endpoint[2] == "/lol-end-of-game/v2/player-complaints"
    assert honor.http.data[2]["gameId"] == 309453646
    assert honor.http.data[2]["reportedSummonerId"] == 2592564405913376



@pytest.mark.asyncio
async def test_report_all_players(honor):
    await honor.report_all_players()
    for i in range(2,11):
        assert honor.http.endpoint[i] == "/lol-end-of-game/v2/player-complaints"
        assert isinstance(honor.http.data[i]["reportedSummonerId"], int)
        assert honor.http.data[i]["reportedSummonerId"] != 2592564405913376

