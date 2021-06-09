from pynput.mouse import Button, Controller
from time import sleep


class Mouse:
    def __init__(self, sleep=0):
        self.mouse = Controller()
        self.sleep = sleep

    def get_position(self):
        sleep(self.sleep)
        return self.mouse.position

    def set_position(self, x: int, y: int):
        sleep(self.sleep)
        self.mouse.position = (x, y)

    def move(self, x: int, y: int):
        sleep(self.sleep)
        self.mouse.move(x, y)

    def click(self):
        sleep(self.sleep)
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)

    def double_click(self):
        sleep(self.sleep)
        self.mouse.click(Button.left, 2)

    def scroll(self, x: int, y: int):
        sleep(self.sleep)
        self.mouse.scroll(x, y)

    def set_position_and_click(self, x: int, y: int):
        self.set_position(x, y)
        self.click()
