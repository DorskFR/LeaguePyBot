from re import A
import pytest
from leaguepybotv2.game_watcher import *
from leaguepybotv2.common import LoopInNewThread
from leaguepybotv2.common.models import Match
import asyncio


@pytest.fixture
def get_game_watcher():
    gw = GameWatcher()
    yield gw


matches = [
    Match(name="minion", x=0, y=0, team="ORDER"),
    Match(name="minion", x=100, y=0, team="ORDER"),
    Match(name="minion", x=0, y=100, team="CHAOS"),
    Match(name="minion", x=100, y=100, team="CHAOS"),
]


def test_game_watcher_init(get_game_watcher):
    assert get_game_watcher
    assert isinstance(get_game_watcher.loop, LoopInNewThread)
    assert isinstance(get_game_watcher.player, Player)
    assert isinstance(get_game_watcher.members, dict)
    assert isinstance(get_game_watcher.units, list)
    assert isinstance(get_game_watcher.units_count, dict)
    assert isinstance(get_game_watcher.game_flow, GameFlow)
    assert isinstance(get_game_watcher.game_connector, GameConnector)
    assert isinstance(get_game_watcher, GameWatcher)


@pytest.mark.asyncio
async def test_game_watcher_clear_members(get_game_watcher):
    await get_game_watcher.clear_members()
    assert isinstance(get_game_watcher.members, dict)
    assert get_game_watcher.members == {}


@pytest.mark.asyncio
async def test_game_watcher_update_units(get_game_watcher):
    await get_game_watcher.update_units(matches)
    assert isinstance(get_game_watcher.units, list)
    assert len(get_game_watcher.units) == 4
    assert isinstance(get_game_watcher.units[0], Match)
    assert get_game_watcher.units[1].x == 100


@pytest.mark.asyncio
async def test_game_watcher_count_units(get_game_watcher):
    await get_game_watcher.update_units(matches)
    await get_game_watcher.count_units()
    assert get_game_watcher.units_count.get("ORDER").get("minion") == 2
    assert get_game_watcher.units_count.get("CHAOS").get("minion") == 2


@pytest.mark.asyncio
async def test_game_watcher_update_player_location(get_game_watcher):

    await get_game_watcher.update_player_location()


# @pytest.mark.asyncio
# async def test_game_watcher_update_member_location(get_game_watcher):
#     await get_game_watcher.update_member_location()
#     pass


# @pytest.mark.asyncio
# async def test_game_watcher_create_members(get_game_watcher):
#     await get_game_watcher.create_members()
#     pass


# @pytest.mark.asyncio
# async def test_game_watcher_log_info(get_game_watcher):
#     await get_game_watcher.log_info()
#     pass
