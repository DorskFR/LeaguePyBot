from ..devices import Keyboard, Mouse
from .hotkeys import Hotkeys


class Action:
    def __init__(self, mouse=Mouse(), keyboard=Keyboard(), hotkeys=Hotkeys(), *args, **kwargs):
        self.mouse = mouse
        self.keyboard = keyboard
        self.hotkeys = hotkeys
