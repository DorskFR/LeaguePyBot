from .http_request import HTTPRequest


from ...logger import get_logger

logger = get_logger("LPBv2.Tricks")


class Tricks(HTTPRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def activate_skins(self):
        response = await self.request(
            method="POST",
            endpoint='/lol-login/v1/session/invoke?destination=lcdsServiceProxy&method=call&args=["","teambuilder-draft","activateBattleBoostV1",""]',
        )
        if response:
            logger.warning("Lobby boosted")
