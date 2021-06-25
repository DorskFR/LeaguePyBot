from .http_client import HTTPClient


class Notifications(HTTPClient):
    def __init__(self):
        super().__init__()

    async def get_endofgame_celebrations(self):
        response = await self.request(
            method="GET", endpoint="/lol-pre-end-of-game/v1/currentSequenceEvent"
        )
        celebration = response.get("name")
        return celebration

    async def skip_mission_celebrations(self):
        celebration = await self.get_endofgame_celebrations()
        await self.request(
            method="POST", endpoint=f"/lol-pre-end-of-game/v1/complete/{celebration}"
        )
