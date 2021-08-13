from pynput.keyboard import Controller, Key


class KeyboardPynput:
    def __init__(self):
        self.keyboard = Controller()

    def input_key(self, key):
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
        self.keyboard.type(word)

    def esc(self):
        self.keyboard.tap(Key.esc)

    def enter(self):
        self.keyboard.tap(Key.enter)

    def space(self):
        self.keyboard.tap(Key.space)
