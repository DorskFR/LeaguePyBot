from . import Action


class Usable(Action):
    def __init__(self):
        super().init()

    async def use_item(self, slot: int):
        slots = {
            "0": self.hotkeys.item_slot_1,
            "1": self.hotkeys.item_slot_2,
            "2": self.hotkeys.item_slot_3,
            "3": self.hotkeys.item_slot_4,
            "4": self.hotkeys.item_slot_5,
            "5": self.hotkeys.item_slot_6,
        }
        if slots.get(slot):
            await self.keyboard.input_key(slots.get(slot))

    async def use_summoner_spell_1(self):
        await self.keyboard.input_key(self.hotkeys.summoner_spell_1)

    async def use_summoner_spell_2(self):
        await self.keyboard.input_key(self.hotkeys.summoner_spell_2)
