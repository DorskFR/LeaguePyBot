from aiohttp import ClientSession


class GameConnector:
    def __init__(self):
        self.base_url = "https://127.0.0.1:2999"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def request(self, endpoint):
        async with ClientSession(headers=self.headers) as session:
            url = self.base_url + endpoint
            response = await session.get(url, ssl=False)
            data = await response.json()
            return data