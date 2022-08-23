from leaguepybot.client.http_requests.http_request import HTTPRequest
from leaguepybot.common.models import WebSocketEventResponse


class Notifications(HTTPRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def get_endofgame_celebrations(self):
        response = await self.request(
            method="GET", endpoint="/lol-pre-end-of-game/v1/currentSequenceEvent"
        )
        celebration = response.data.get("name")
        return celebration

    async def skip_mission_celebrations(self):
        celebration = await self.get_endofgame_celebrations()
        await self.request(
            method="POST", endpoint=f"/lol-pre-end-of-game/v1/complete/{celebration}"
        )

    async def dismiss_notifications_at_eog(self, event: WebSocketEventResponse):
        if event.data in ["WaitingForStats", "PreEndOfGame"]:
            await self.skip_mission_celebrations()
