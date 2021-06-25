from ...common import Hotkeys
from ..devices import Keyboard, Mouse


class Action:
    def __init__(self):
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.hotkeys = Hotkeys()
