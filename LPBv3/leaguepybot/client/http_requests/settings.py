import asyncio
from json import dumps

from leaguepybot.client.http_requests.http_request import HTTPRequest
from leaguepybot.common.logger import get_logger

logger = get_logger("LPBv3.Settings")


class Settings(HTTPRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        asyncio.create_task(self.patch_settings())

    async def get_settings(self):
        response = await self.request(
            method="GET",
            endpoint="/lol-game-settings/v1/game-settings",
        )
        if response:
            logger.debug(dumps(response.data, indent=4))

    async def patch_settings(self):
        bot_settings = {
            "HUD": {
                "AutoDisplayTarget": True,
                "CameraLockMode": 1,
                "ChatScale": 0,
                "GlobalScale": 0.0,
                "DrawHealthBars": True,
                "FlipMiniMap": False,
                "MinimapScale": 0.0,
                "MinimapMoveSelf": True,
                "MirroredScoreboard": True,
                "ShowTeamFramesOnLeft": True,
                "SmartCastOnKeyRelease": False,
                "SmartCastWithIndicator_CastWhenNewSpellSelected": True,
            },
            "General": {
                "AutoAcquireTarget": True,
                "EnableTargetedAttackMove": False,
                "RelativeTeamColors": True,
                # "WindowMode": 2,
            },
        }
        response = await self.request(
            method="PATCH",
            endpoint="/lol-game-settings/v1/game-settings",
            payload=bot_settings,
        )
        if response:
            logger.debug("Patched game settings")
