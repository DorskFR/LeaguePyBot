from LPBv2.client import Honor
from .mock_http_connection import MockHTTPConnection
import pytest


@pytest.fixture
def honor():
    return Honor(connection=MockHTTPConnection())


@pytest.mark.asyncio
async def test_get_command_ballot(honor):
    pass


@pytest.mark.asyncio
async def test_command_random_player(honor):
    pass


@pytest.mark.asyncio
async def test_command_all_players(honor):
    pass


@pytest.mark.asyncio
async def test_command_player(honor):
    pass


@pytest.mark.asyncio
async def test_report_all_players(honor):
    pass


@pytest.mark.asyncio
async def test_report_player(honor):
    pass


@pytest.mark.asyncio
async def test_get_eog_player_list(honor):
    pass


@pytest.mark.asyncio
async def test_get_game_id(honor):
    pass
