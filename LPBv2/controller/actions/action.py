from ..devices import Keyboard, Mouse
from .hotkeys import Hotkeys


class Action:
    def __init__(self):
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.hotkeys = Hotkeys()
