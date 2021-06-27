from . import Action


class Usable(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def use_item(self, slot: int):
        slots = [
            self.hotkeys.item_slot_1,
            self.hotkeys.item_slot_2,
            self.hotkeys.item_slot_3,
            self.hotkeys.item_slot_4,
            self.hotkeys.item_slot_5,
            self.hotkeys.item_slot_6,
        ]
        await self.keyboard.input_key(slots[slot])

    async def use_summoner_spell_1(self):
        await self.keyboard.input_key(self.hotkeys.summoner_spell_1)

    async def use_summoner_spell_2(self):
        await self.keyboard.input_key(self.hotkeys.summoner_spell_2)
