import pytest
from leaguepybotv2.game_watcher import GameFlow
from leaguepybotv2.common.models import GameEvent


@pytest.fixture
def get_game_flow():
    return GameFlow()


events_data = [
    {"EventID": 0, "EventName": "GameStart", "EventTime": 0.01637154631316662},
    {"EventID": 1, "EventName": "MinionsSpawning", "EventTime": 65.038818359375},
    {
        "Assisters": [],
        "EventID": 2,
        "EventName": "ChampionKill",
        "EventTime": 194.25624084472656,
        "KillerName": "KillerChamp",
        "VictimName": "VictimChamp",
    },
    {
        "EventID": 3,
        "EventName": "FirstBlood",
        "EventTime": 194.25624084472656,
        "Recipient": "KillerChamp",
    },
]

game_data = {
    "gameMode": "CLASSIC",
    "gameTime": 300.0,
    "mapName": "Map11",
    "mapNumber": 11,
    "mapTerrain": "Default",
}


def test_game_flow_init(get_game_flow):
    assert get_game_flow
    assert isinstance(get_game_flow.events, list)
    assert isinstance(get_game_flow.time, float)
    assert isinstance(get_game_flow.is_ingame, bool)
    assert isinstance(get_game_flow.current_action, str)
    assert isinstance(get_game_flow, GameFlow)
    assert hasattr(get_game_flow, "update")
    assert hasattr(get_game_flow, "update_is_ingame")
    assert hasattr(get_game_flow, "update_events")
    assert hasattr(get_game_flow, "update_current_action")


@pytest.mark.asyncio
async def test_update_is_ingame(get_game_flow):
    await get_game_flow.update_is_ingame(True)
    assert get_game_flow.is_ingame == True


@pytest.mark.asyncio
async def test_update_events(get_game_flow):
    await get_game_flow.update_events(events_data)
    assert len(get_game_flow.events) == 4
    assert isinstance(get_game_flow.events[0], GameEvent)


@pytest.mark.asyncio
async def test_update_time(get_game_flow):
    await get_game_flow.update_time(game_data)
    assert get_game_flow.time == 300.0


@pytest.mark.asyncio
async def test_game_flow_update(get_game_flow):
    await get_game_flow.update(events_data, game_data)
    assert len(get_game_flow.events) == 4
    assert isinstance(get_game_flow.events[0], GameEvent)
    assert get_game_flow.time == 300.0
