import asyncio

from leaguepybot.client.connection.http_client import HttpClient
from leaguepybot.common.logger import get_logger
from leaguepybot.common.models import Runnable, SummonerInfo

logger = get_logger("LPBv3.Summoner")


class Summoner(Runnable):
    def __init__(self, http_client: HttpClient):
        self._http_client = http_client
        self.info = None
        asyncio.create_task(self.get_current_summoner())

    async def get_current_summoner(self):
        resp = await self._http_client.request(
            method="GET", endpoint="/lol-summoner/v1/current-summoner"
        )
        self.info = SummonerInfo(**resp.data)
