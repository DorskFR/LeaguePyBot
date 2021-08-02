from . import Action
from ...common import debug_coro
from ...logger import get_logger

logger = get_logger("LPBv2.Usable")


class Usable(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @debug_coro
    async def use_item(self, slot: int):
        slots = [
            self.hotkeys.item_slot_1,
            self.hotkeys.item_slot_2,
            self.hotkeys.item_slot_3,
            self.hotkeys.item_slot_4,
            self.hotkeys.item_slot_5,
            self.hotkeys.item_slot_6,
        ]
        self.keyboard.input_key(slots[slot])

    @debug_coro
    async def use_summoner_spell_1(self):
        self.keyboard.input_key(self.hotkeys.spell_1)

    @debug_coro
    async def use_summoner_spell_2(self):
        self.keyboard.input_key(self.hotkeys.spell_2)

    @debug_coro
    async def heal(self):
        slot = await self.game.player.get_consumable_slot()
        if slot:
            await self.use_item(slot)
        await self.use_summoner_spell_2()
