from .actions import *
from .devices import *


class Controller:
    def __init__(self, *args, **kwargs):
        self.action = Action(*args, **kwargs)
        self.combat = Combat(*args, **kwargs)
        self.movement = Movement(*args, **kwargs)
        self.usable = Usable(*args, **kwargs)
        self.shop = Shop(*args, **kwargs)
        self.listener = KeyboardListener()
