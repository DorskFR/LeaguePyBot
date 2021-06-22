from .mouse import Mouse
from .keyboard import Keyboard
from .listener import KeyboardListener
from ..common.utils import make_minimap_coords


class Controller:
    def __init__(self):
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.listener = KeyboardListener()

    def attack_move(self, x: int, y: int):
        self.keyboard.press("a")
        self.mouse.set_position(x, y)
        self.mouse.click()
        self.keyboard.release("a")

    def click_minimap(self, x: int, y: int):
        x, y = make_minimap_coords(x, y)
        self.mouse.set_position(x, y)
        self.mouse.right_click

    def right_click(self, x: int, y: int):
        self.mouse.set_position(x, y)
        self.mouse.right_click()
