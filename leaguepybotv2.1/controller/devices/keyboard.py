from time import sleep

from pynput.keyboard import Controller


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
        # Type a lower case A; this will work even if no key on the
        # physical keyboard is labelled 'A'
        sleep(self.sleep)
        self.keyboard.press(key)
        self.keyboard.release(key)
