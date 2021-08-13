from ..devices import Keyboard, Mouse
from ...common import debug_coro, riskiest_position


class Action:
    def __init__(self, mouse=Mouse(), keyboard=Keyboard(), *args, **kwargs):
        self.mouse = mouse
        self.keyboard = keyboard
        self.hotkeys = kwargs.get("hotkeys")
        self.game = kwargs.get("game")

    #@debug_coro
    async def attack_move(self, x: int, y: int):
        self.keyboard.press(self.hotkeys.attack_move)
        self.mouse.set_position_and_left_click(x, y)
        self.keyboard.release(self.hotkeys.attack_move)

    #@debug_coro
    async def get_riskiest_ally_position(self):
        minions = self.game.game_units.units.ally_minions
        if minions:
            return riskiest_position(minions)

    #@debug_coro
    async def skip_screen(self):
        self.keyboard.space()
