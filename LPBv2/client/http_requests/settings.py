from .http_request import HTTPRequest
from ...logger import get_logger
from ...common import debug_coro
logger = get_logger("LPBv2.Settings")


class Settings(HTTPRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @debug_coro
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
                "EnableTargetedAttackMove": True,
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
            logger.info("Patched input settings")
