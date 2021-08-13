from aiohttp import ClientSession
from ..common import debug_coro


class GameConnector:
    def __init__(self):
        self.base_url = "https://127.0.0.1:2999"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.session = ClientSession(headers=self.headers)

    async def request(self, endpoint):
        url = self.base_url + endpoint
        async with self.session.get(url, ssl=False) as response:
            data = await response.json()
            return data
