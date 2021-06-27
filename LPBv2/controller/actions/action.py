from ..devices import Keyboard, Mouse, Hotkeys


class Action:
    def __init__(
        self, mouse=Mouse(), keyboard=Keyboard(), hotkeys=Hotkeys(), *args, **kwargs
    ):
        self.mouse = mouse
        self.keyboard = keyboard
        self.hotkeys = hotkeys
