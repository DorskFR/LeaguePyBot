from .actions import *
from .devices import *
import time


class Controller:
    def __init__(self, *args, **kwargs):
        self.hotkeys = Hotkeys(*args, **kwargs)
        self.combat = Combat(*args, **kwargs)
        self.movement = Movement(*args, **kwargs)
        self.usable = Usable(*args, **kwargs)
        self.shop = Shop(
            keyboard=Keyboard(sleep=0.1), hotkeys=self.hotkeys, *args, **kwargs
        )
        self.listener = KeyboardListener()
