from time import sleep
import os


class Keyboard:
    __instance = None

    @staticmethod
    def get_instance(*args, **kwargs):
        if Keyboard.__instance is None:
            Keyboard(*args, **kwargs)
        return Keyboard.__instance

    def __init__(self, sleep=0):
        if Keyboard.__instance is not None:
            raise Exception("This class is a Singleton")
        else:
            Keyboard.__instance = self

        if os.name == "nt":
            from .keyboard_pydirectinput import KeyboardPyDirectInput
            self.keyboard = KeyboardPyDirectInput()
        else:
            from .keyboard_pynput import KeyboardPynput
            self.keyboard = KeyboardPynput()
        self.sleep = sleep

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
