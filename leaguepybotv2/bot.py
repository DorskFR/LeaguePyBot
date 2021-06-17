import asyncio
import concurrent.futures
from time import time

from .common import Loop
from .game_watcher import GameWatcher
from .league_client import LeagueClient
from .logger import get_logger
from .peripherals import Keyboard, KeyboardListener, Mouse, Vision

logger = get_logger("LPBv2.Bot")


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
        loop_time = time()
        while True:
            if not self.game.is_ingame:
                continue

            # now we are in game

            # if self.client.client_phase in ["GameStart", "InProgress"]:
            #     members = self.game.members
            #     self.vision.clear_templates()
            #     logger.error(members)
            #     for member in members:
            #         await self.vision.load_champion_template(member)

            try:
                if self.client.client_phase == "None":
                    await self.client.check_client_phase()

                if self.client.client_phase in ["GameStart", "InProgress"]:
                    members = self.game.members
                    self.vision.clear_templates()
                    for member in members:
                        await self.vision.load_champion_template(member)

                await asyncio.sleep(0.01)
                self.vision.shot_window(
                    {"top": 1080 - 420, "left": 1920 - 420, "width": 420, "height": 420}
                )

                # we need to know where we are:
                # await self.where_am_i()
                # await self.locate_champions_on_minimap()

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

                # if we are in lane, we need to know what is on the screen

                self.game.FPS = self.vision.FPS = round(1 / (time() - loop_time), 2)
                loop_time = time()
            except Exception as e:
                logger.error(e)

    async def locate_champions_on_minimap(self):
        for champion in self.vision.templates:
            await self.locate_champion_on_minimap(champion)

    async def locate_champion_on_minimap(self, champion):
        await self.vision.minimap_match()

    async def shop(self):
        x, y = self.vision.minimap_match()
        if x and y:
            self.game.player.location = f"x: {x}, y: {y}"
        else:
            self.game.player.location = "UNKNOWN"
        # fmt: off
