from time import sleep
import os
from .keyboard_pynput import KeyboardPynput
from .keyboard_pydirectinput import KeyboardPyDirectInput



class Keyboard:
    def __init__(self, sleep=0):
        if os.name == "nt":
            self.keyboard = KeyboardPyDirectInput()
        else:
            self.keyboard = KeyboardPynput()
        self.sleep=sleep

    def input_key(self, key):
        sleep(self.sleep)
        self.keyboard.input_key(key)

    def input_word(self, word: str):
        sleep(self.sleep)
        self.keyboard.input_word(word)

    def esc(self):
        sleep(self.sleep)
        self.keyboard.esc()

    def enter(self):
        sleep(self.sleep)
        self.keyboard.enter()

    def space(self):
        sleep(self.sleep)
        self.keyboard.space()
