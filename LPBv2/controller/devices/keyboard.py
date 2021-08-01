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
        if "Ctrl" in key:
            with self.keyboard.pressed(Key.ctrl):
                self.keyboard.tap(key.replace("Ctrl", ""))
        if "Alt" in key:
            with self.keyboard.pressed(Key.alt):
                self.keyboard.tap(key.replace("Alt", ""))

    def input_word(self, word: str):
        sleep(self.sleep)
        for letter in word:
            self.keyboard.tap(letter)

    def esc(self):
        sleep(self.sleep)
        self.keyboard.tap(Key.esc)

    def enter(self):
        sleep(self.sleep)
        self.keyboard.tap(Key.enter)
