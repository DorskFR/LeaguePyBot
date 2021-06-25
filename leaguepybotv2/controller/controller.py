from .mouse import Mouse
from .keyboard import Keyboard
from ..common.utils import make_minimap_coords
from .listener import KeyboardListener
from ..common.models import Hotkeys


class Controller:
    def __init__(self):
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.listener = KeyboardListener()
        self.hotkeys = Hotkeys()

    async def attack_move(self, x: int, y: int):
        self.keyboard.press("a")
        self.mouse.set_position(x, y)
        self.mouse.click()
        self.keyboard.release("a")

    async def click_minimap(self, x: int, y: int):
        x, y = make_minimap_coords(x, y)
        self.mouse.set_position(x, y)
        self.mouse.right_click()

    async def right_click(self, x: int, y: int):
        self.mouse.set_position(x, y)
        self.mouse.right_click()

    async def cast_spell(self, key, x: int, y: int):
        self.mouse.set_position(x, y)
        self.keyboard.key(key)

    async def press_key(self, key):
        self.keyboard.key(key)

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
            await self.press_key(slots.get(slot))

    async def use_summoner_spell_1(self):
        await self.press_key(self.hotkeys.summoner_spell_1)

    async def use_summoner_spell_2(self):
        await self.press_key(self.hotkeys.summoner_spell_2)

    async def recall(self):
        await self.press_key(self.hotkeys.recall)

    async def toggle_shop(self):
        await self.press_key(self.hotkeys.shop)
