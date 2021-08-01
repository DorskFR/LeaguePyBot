from json import dumps

from aiohttp import ClientSession


class Caller:
    async def get(self, url):
        try:
            async with ClientSession() as session:
                response = await session.get(url)
                response_json = await response.json()
                return response_json
        except Exception as e:
            print(e)

    async def post(self, url, payload):
        async with self.session.post(url=url, data=dumps(payload)) as response:
            response_json = await response.json()
            return response_json
