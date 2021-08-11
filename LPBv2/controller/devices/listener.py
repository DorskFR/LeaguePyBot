import os
import signal
import asyncio
from pynput.keyboard import Key, Listener

from ...common import LoopInNewThread


class KeyboardListener:
    def __init__(self):
        self.listener = Listener(on_press=self.on_press)
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

