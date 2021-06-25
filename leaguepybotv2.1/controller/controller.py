from .actions import *
from .devices import KeyboardListener
import time


class Controller:
    def __init__(self):
        self.combat = Combat()
        self.movement = Movement()
        self.usable = Usable()
        self.shop = Shop()
        self.listener = KeyboardListener()

    async def fall_back(self):
        zone = await self.find_closest_ally_zone()
        await self.controller.click_minimap(zone.x, zone.y)

    async def heal(self):
        slot = await self.game.player.get_consumable_slot()
        if slot:
            await self.controller.use_item(slot)
        await self.controller.use_summoner_spell_2()

    async def recall(self):
        await self.controller.use_summoner_spell_1()
        await self.fall_back()
        time.sleep(8)
        await self.controller.recall()
        time.sleep(15)
