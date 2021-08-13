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
            pid = int(os.getpid())
            try:
                os.kill(pid, signal.SIGKILL)
            except:
                os.system(f"taskkill /f /pid {pid}")
            return False
