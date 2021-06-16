from pynput.keyboard import Key, Controller, Listener
from time import sleep


class Keyboard:
    def __init__(self, sleep=0):
        self.keyboard = Controller()
        self.sleep = sleep

    def space(self):
        # Press and release space
        sleep(self.sleep)
        self.keyboard.press(Key.space)
        self.keyboard.release(Key.space)

    def enter(self):
        # Press and release enter
        sleep(self.sleep)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

    def escape(self):
        # Press and release enter
        sleep(self.sleep)
        self.keyboard.press(Key.esc)
        self.keyboard.release(Key.esc)

    def key(self, key):
        # Type a lower case A; this will work even if no key on the
        # physical keyboard is labelled 'A'
        sleep(self.sleep)
        self.keyboard.press(key)
        self.keyboard.release(key)

    def shift(self, key):
        # Type two upper case As
        sleep(self.sleep)
        with self.keyboard.pressed(Key.shift):
            self.key(key)

    def write(self, text):
        # Type 'Hello World' using the shortcut type methodQ
        sleep(self.sleep)
        self.keyboard.type(text)

    def quit(self):
        with self.keyboard.pressed(Key.alt):
            with self.keyboard.pressed(Key.cmd):
                self.key("q")

    def end(self):
        sleep(self.sleep)
        self.keyboard.press(Key.end)
        self.keyboard.release(Key.end)


class KeyboardListener:
    def __init__(self):
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.last_key = None

    def listen(self):
        with self.listener as listener:
            listener.join()

    def on_press(self, key):
        if key == Key.end:
            self.last_key = "end"
            return False
        if key == Key.home:
            self.last_key = "home"
            return False

    def read_pressed(self, key):
        try:
            print(f"alphanumeric key {key.char} pressed with vk code {key.vk}")
        except AttributeError:
            print(f"special key {key} pressed")

    def on_release(self, key):
        pass
