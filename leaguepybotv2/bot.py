from .league_client import LeagueClient
from .game_watcher import GameWatcher
from .peripherals import Mouse, Keyboard, KeyboardListener, Vision
from .common import Loop
from .logger import get_logger
import cv2

logger = get_logger("LeaguePyBotV2")


class LeaguePyBot:
    def __init__(self):

        logger.warning("Welcome to LeaguePyBotV2")

        self.client = LeagueClient()  # async
        self.game = GameWatcher()  # async
        self.vision = Vision()  # cpu bound
        self.mouse = Mouse()  # async?
        self.keyboard = Keyboard()  # async?
        self.listener = KeyboardListener()  # async?
        self.loop = Loop()
        self.loop.submit_async(self.run_bot())

    async def run_bot(self):
        # loop_time = time()
        while True:
            if not self.game.is_ingame:
                continue

            self.vision.capture_window()
            self.vision.draw_grid(text=True)
            cv2.imshow("screen", self.vision.sct_img)
            # print("FPS {}".format(round(1 / (time() - loop_time), 2)))
            # loop_time = time()

            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                cv2.destroyAllWindows()
                break

            # fmt: off
            # now we are in game

            # we need to know where we are:
                # shop
                # where on the map

            # we need to know how we are
                # self.game.player.info.currentGold
                # self.game.player.info.isDead
                # self.game.player.stats.currentHealth
                # self.game.player.stats.maxHealth
                # self.game.player.info.level
                # self.game.player.info.team

            # we need to know what is happening
                # turrets destroyed
                # inhibs destroyed
                # nexus destroyed
                # champion kills

            # we need to know what we have in inventory
            # we need to know what to buy
