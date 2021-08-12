from json import dumps
from .utils import debug_coro
from aiohttp import ClientSession
from ..logger import get_logger

logger = get_logger("LPBv2.Caller")


class Caller:
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.session = ClientSession(headers=self.headers)

    @debug_coro
    async def get(self, url):
        try:
            async with self.session.get(url) as response:
                response_json = await response.json()
                return response_json
        except Exception as e:
            logger.error(e)

    @debug_coro
    async def post(self, url, payload):
        try:
            async with self.session.post(
                url=url,
                json=payload,
            ) as response:
                response_json = await response.json()
                return response_json
        except Exception as e:
            logger.error(e)
