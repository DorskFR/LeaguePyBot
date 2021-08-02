from ..devices import Keyboard, Mouse
from ...common import debug_coro


class Action:
    def __init__(self, mouse=Mouse(), keyboard=Keyboard(), *args, **kwargs):
        self.mouse = mouse
        self.keyboard = keyboard
        self.hotkeys = kwargs.get("hotkeys")
        self.game = kwargs.get("game")

    @debug_coro
    async def attack_move(self, x: int, y: int):
        self.keyboard.press(self.hotkeys.attack_move)
        self.mouse.set_position_and_left_click(x, y)
        self.keyboard.release(self.hotkeys.attack_move)
