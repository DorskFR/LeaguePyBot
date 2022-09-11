from leaguepybot.client.connection.http_client import HttpClient
from leaguepybot.common.logger import get_logger
from leaguepybot.common.models import Runnable

logger = get_logger("LPBv3.Tricks")


class Tricks(Runnable):
    def __init__(self, http_client: HttpClient):
        self._http_client = http_client

    async def activate_skins(self):
        response = await self._http_client.request(
            method="POST",
            endpoint='/lol-login/v1/session/invoke?destination=lcdsServiceProxy&method=call&args=["","teambuilder-draft","activateBattleBoostV1",""]',
        )
        if response:
            logger.warning("Lobby boosted")
