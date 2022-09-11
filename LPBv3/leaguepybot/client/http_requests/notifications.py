from leaguepybot.client.connection.http_client import HttpClient
from leaguepybot.common.models import Runnable, WebSocketEventResponse


class Notifications(Runnable):
    def __init__(self, http_client: HttpClient):
        self._http_client = http_client

    async def get_endofgame_celebrations(self):
        response = await self._http_client.request(
            method="GET", endpoint="/lol-pre-end-of-game/v1/currentSequenceEvent"
        )
        celebration = response.data.get("name")
        return celebration

    async def skip_mission_celebrations(self):
        celebration = await self.get_endofgame_celebrations()
        await self._http_client.request(
            method="POST", endpoint=f"/lol-pre-end-of-game/v1/complete/{celebration}"
        )

    async def dismiss_notifications_at_eog(self, event: WebSocketEventResponse):
        if event.data in ["WaitingForStats", "PreEndOfGame"]:
            await self.skip_mission_celebrations()
