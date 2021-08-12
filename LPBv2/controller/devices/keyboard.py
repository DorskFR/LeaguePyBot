from time import sleep

from pynput.keyboard import Controller, Key


class Keyboard:
    def __init__(self, sleep=0):
        self.keyboard = Controller()
        self.sleep = sleep

    def press(self, key):
        sleep(self.sleep)
        self.keyboard.press(key)

    def release(self, key):
        sleep(self.sleep)
        self.keyboard.release(key)

    def input_key(self, key):
        sleep(self.sleep)
        if "Shift" in key:
            with self.keyboard.pressed(Key.shift):
                self.keyboard.tap(key.replace("Shift", ""))
        elif "Ctrl" in key:
            with self.keyboard.pressed(Key.ctrl):
                self.keyboard.tap(key.replace("Ctrl", ""))
        elif "Alt" in key:
            with self.keyboard.pressed(Key.alt):
                self.keyboard.tap(key.replace("Alt", ""))
        else:
            self.keyboard.tap(key)

    def input_word(self, word: str):
        sleep(self.sleep)
        self.keyboard.type(word)

    def esc(self):
        sleep(self.sleep)
        self.keyboard.tap(Key.esc)

    def enter(self):
        sleep(self.sleep)
        self.keyboard.tap(Key.enter)

    def space(self):
        sleep(self.sleep)
        self.keyboard.tap(Key.space)
