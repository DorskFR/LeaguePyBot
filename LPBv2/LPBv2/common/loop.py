import asyncio
import threading
from ..logger import get_logger

logger = get_logger("LPBv2.LoopInNewThread")


class LoopInNewThread:
    def __init__(self):
        self.loop = self.start_async()

    def start_async(self):
        loop = asyncio.new_event_loop()
        threading.Thread(target=loop.run_forever).start()
        return loop

    # Submits awaitable to the event loop, but *doesn't* wait for it to
    # complete. Returns a concurrent.futures.Future which *may* be used to
    # wait for and retrieve the result (or exception, if one was raised)
    def submit_async(self, awaitable):
        return asyncio.run_coroutine_threadsafe(awaitable, self.loop)

    def stop_async(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
