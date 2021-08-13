from .http_request import HTTPRequest
from ...common import debug_coro, SummonerInfo
from json import dumps
import asyncio
from ...logger import get_logger

logger = get_logger("LPBv2.Summoner")


class Summoner(HTTPRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.info = None
        loop = asyncio.get_event_loop()
        loop.create_task(self.get_current_summoner())

    #@debug_coro
    async def get_current_summoner(self):
        resp = await self.http.request(
            method="GET", endpoint="/lol-summoner/v1/current-summoner"
        )
        self.info = SummonerInfo(**resp.data)
