import pydirectinput

pydirectinput.FAILSAFE = False
pydirectinput.PAUSE = 0.01

class KeyboardPyDirectInput:
    def __init__(self):
        pass

    def input_key(self, key: str):
        if "Shift" in key:
            pydirectinput.keyDown("shift")
            pydirectinput.press(key.replace("Shift", ""))
            pydirectinput.keyUp("shift")
        elif "Ctrl" in key:
            pydirectinput.keyDown("ctrl")
            pydirectinput.press(key.replace("Ctrl", ""))
            pydirectinput.keyUp("ctrl")
        elif "Alt" in key:
            pydirectinput.keyDown("alt")
            pydirectinput.press(key.replace("Alt", ""))
            pydirectinput.keyUp("alt")
        else:
            pydirectinput.press(key)

    def input_word(self, word: str):
        for letter in word.lower():
            pydirectinput.press(letter)

    def esc(self):
        pydirectinput.press("esc")

    def enter(self):
        pydirectinput.press("enter")

    def space(self):
        pydirectinput.press("space")
