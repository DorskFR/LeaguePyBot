import os
import signal
from pynput.keyboard import Key, Listener
import threading


class KeyboardListener:
    def __init__(self):
        self.listener = Listener(on_press=self.on_press)
        threading.Thread(target=self.listen).start()

    def listen(self):
        with self.listener as listener:
            listener.join()

    def on_press(self, key):
        if key == Key.end:
            os.kill(int(os.getpid()), signal.SIGKILL)
            return False
