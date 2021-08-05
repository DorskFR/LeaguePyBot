from ...common import (
    make_minimap_coords,
    ZONES,
    safest_position,
    find_closest_zone,
    debug_coro,
)
from . import Action
from ...logger import get_logger

logger = get_logger("LPBv2.Movement")


class Movement(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @debug_coro
    async def click_minimap(self, x: int, y: int):
        x, y = make_minimap_coords(x, y)
        self.mouse.set_position_and_right_click(x, y)

    @debug_coro
    async def recall(self):
        await self.game.game_flow.update_current_action("Recalling")
        self.keyboard.input_key(self.hotkeys.recall)

    @debug_coro
    async def go_to_lane(self):

        for zone in ZONES:
            if zone.name == "Bot T1" and zone.team == self.game.player.info.team:
                await self.click_minimap(zone.x, zone.y)
                await self.game.game_flow.update_current_action(
                    f"Going to lane {zone.name}"
                )

    @debug_coro
    async def find_closest_ally_zone(self):
        x = 0
        y = 210
        if self.game.player.info.zone:
            x = self.game.player.info.zone.x
            y = self.game.player.info.zone.y
        safe_zones = [zone for zone in ZONES if zone.team == self.game.player.info.team]
        closest = find_closest_zone(x, y, zones=safe_zones)
        return closest

    @debug_coro
    async def fall_back(self, reason: str = None):
        zone = await self.find_closest_ally_zone()
        await self.game.game_flow.update_current_action(
            f"Falling back to {zone.name}. (reason: {reason})"
        )
        await self.click_minimap(zone.x, zone.y)

    @debug_coro
    async def follow_allies(self):
        await self.game.game_flow.update_current_action("Following allies")
        pos = await self.get_riskiest_ally_position()
        if pos:
            await self.attack_move(*pos)

    @debug_coro
    async def get_safest_ally_position(self):
        minions = self.game.game_units.units.ally_minions
        if minions:
            return safest_position(minions)

    @debug_coro
    async def lock_camera(self):
        self.keyboard.input_key(self.hotkeys.camera_lock)
