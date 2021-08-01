from ...common import make_minimap_coords, ZONES
from . import Action


class Movement(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def click_minimap(self, x: int, y: int):
        x, y = make_minimap_coords(x, y)
        self.mouse.set_position_and_right_click(x, y)

    async def recall(self):
        await self.keyboard.input_key(self.hotkeys.recall)

    async def go_to_lane(self):
        for zone in ZONES:
            if zone.name == "Top T1" and zone.team == self.game.player.info.team:
                await self.click_minimap(zone.x, zone.y)
