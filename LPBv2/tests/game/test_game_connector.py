import pytest
from LPBv2.game import GameConnector
import aiohttp


@pytest.fixture
def get_connector():
    return GameConnector()


def test_game_connector_init(get_connector):
    assert get_connector
    assert get_connector.base_url
    assert get_connector.headers
    assert hasattr(get_connector, "request")
    assert isinstance(get_connector, GameConnector)


# only run if not in a game
# @pytest.mark.asyncio
# async def test_game_connector_request_not_connected(get_connector):
#     with pytest.raises(aiohttp.client_exceptions.ClientConnectorError):
#         assert await get_connector.request("/liveclientdata/allgamedata")
