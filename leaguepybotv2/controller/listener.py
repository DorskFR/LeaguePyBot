from pynput.keyboard import Listener, Key
import os
import signal
from ..common.loop import LoopInNewThread


class KeyboardListener:
    def __init__(self):
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.last_key = None
        self.loop = LoopInNewThread()
        self.loop.submit_async(self.listen())

    async def listen(self):
        with self.listener as listener:
            listener.join()

    def on_press(self, key):
        if key == Key.end:
            self.last_key = "end"
            os.kill(int(os.getpid()), signal.SIGKILL)
            return False

    def read_pressed(self, key):
        try:
            print(f"alphanumeric key {key.char} pressed with vk code {key.vk}")
        except AttributeError:
            print(f"special key {key} pressed")

    def on_release(self, key):
        pass
