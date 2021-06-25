from leaguepybotv2.league_client.league_connector import LeagueConnector
from typing import Optional


class ClientCall:
    def __init__(self):
        self.connection = Connection()
        self.method: Optional[str]
        self.endpoint: Optional[str]
        self.payload: Optional[dict]
        self.event: Optional[WebsocketEventResponse]

    async def request(self):
        response = await self.connection.request(
            method=self.method, endpoint=self.endpoint, payload=self.payload
        )
        if response.status_code in [200, 201, 202, 203, 204, 205, 206]:
            return response

    async def execute(self, event: Optional[WebsocketEventResponse]):
        if event:
            self.event = event
        if await self.condition():
            await self.build()
            response = await self.request()
            if response:
                await self.action(response)

    async def build(self):
        raise NotImplementedError

    async def condition(self):
        return True

    async def action(self, response: ClientResponse):
        pass
