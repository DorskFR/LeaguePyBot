import pytest
from ..league_client import LeagueClient, LeagueConnector, LeagueSummoner
from ..common.loop import Loop
from ..common.models import WebsocketEvent


@pytest.fixture
def league_client():
    return LeagueClient()


@pytest.mark.asyncio
async def test_league_client_object(league_client):
    assert isinstance(league_client, LeagueClient)


@pytest.mark.asyncio
async def test_league_client_loop(league_client):
    assert isinstance(league_client.loop, Loop)


@pytest.mark.asyncio
async def test_league_client_default_events(league_client):
    assert isinstance(league_client.default_events, list)
    assert len(league_client.default_events) > 0
    assert isinstance(league_client.default_events[0], WebsocketEvent)


@pytest.mark.asyncio
async def test_league_client_connector(league_client):
    assert isinstance(league_client.connector, LeagueConnector)
    assert isinstance(league_client.connector.events, list)
    assert len(league_client.connector.events) > 0
    assert isinstance(league_client.connector.events[0], WebsocketEvent)


@pytest.mark.asyncio
async def test_league_client_summoner(league_client):
    assert isinstance(league_client.summoner, LeagueSummoner)


@pytest.mark.asyncio
async def test_league_client_start(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_log_everything(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_loop_back_log(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_is_matchmaking(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_subscribe_game_phases(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_subscribe_ready_check(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_subscribe_champ_selection(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_set_pickban_and_role(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_choose_lane_position(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_create_ranked_game(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_create_custom_game(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_start_matchmaking(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_pick_champion(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_ban_champion(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_add_bots(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_create_normal_game(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_command_random_player(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_report_all_players(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_report_player(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_get_player_list(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_get_game_id(league_client):
    pass


@pytest.mark.asyncio
async def test_league_client_(league_client):
    pass
