from pynput.keyboard import Listener, Key


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
