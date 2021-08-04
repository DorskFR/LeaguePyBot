from LPBv2.common import WebSocketEventResponse, debug_coro
from .http_request import HTTPRequest


class Notifications(HTTPRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @debug_coro
    async def get_endofgame_celebrations(self):
        response = await self.request(
            method="GET", endpoint="/lol-pre-end-of-game/v1/currentSequenceEvent"
        )
        celebration = response.data.get("name")
        return celebration

    @debug_coro
    async def skip_mission_celebrations(self):
        celebration = await self.get_endofgame_celebrations()
        await self.request(
            method="POST", endpoint=f"/lol-pre-end-of-game/v1/complete/{celebration}"
        )

    @debug_coro
    async def dismiss_notifications_at_eog(self, event: WebSocketEventResponse):
        if event.data in ["WaitingForStats", "PreEndOfGame"]:
            await self.skip_mission_celebrations()
            

