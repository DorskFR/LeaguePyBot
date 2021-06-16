from .league_client import LeagueClient
from .game_watcher import GameWatcher
from .peripherals import Mouse, Keyboard, KeyboardListener, Vision

from threading import Thread


class LeaguePyBot:
    def __init__(self):

        self.client = LeagueClient()  # async
        self.game = GameWatcher()  # async
        self.vision = Vision()  # cpu bound
        self.mouse = Mouse()  # async?
        self.keyboard = Keyboard()  # async?
        self.listener = KeyboardListener()  # async?

        self.threads = list()

    async def start(self):
        self.threads.append(Thread(target=self.client.start))
        self.threads.append(Thread(target=self.game.start))
        self.threads.append(Thread(target=self.vision.start))
        self.threads.append(Thread(target=self.listener.start))

        for t in self.threads:
            t.start()

        for t in self.threads:
            t.join()
