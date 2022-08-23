import asyncio

from leaguepybot.client.http_requests.http_request import HTTPRequest
from leaguepybot.common.logger import get_logger
from leaguepybot.common.models import SummonerInfo

logger = get_logger("LPBv3.Summoner")


class Summoner(HTTPRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.info = None
        asyncio.create_task(self.get_current_summoner())

    async def get_current_summoner(self):
        resp = await self.http.request(method="GET", endpoint="/lol-summoner/v1/current-summoner")
        self.info = SummonerInfo(**resp.data)
