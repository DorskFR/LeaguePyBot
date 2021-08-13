from .actions import *
from .devices import *


class Controller:
    def __init__(self, *args, **kwargs):
        self.action = Action()
        self.combat = Combat(*args, **kwargs)
        self.movement = Movement(*args, **kwargs)
        self.usable = Usable(*args, **kwargs)
        self.shop = Shop(keyboard=Keyboard.get_instance(sleep=0.01), *args, **kwargs)
        self.listener = KeyboardListener()
