import asyncio
import inspect
from time import time

from .common import Loop, ZONES
from .common.utils import pythagorean_distance
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
            if not self.game.is_ingame or not self.game.members:
                if self.vision.templates:
                    self.vision.clear_templates()
                if self.game.members:
                    self.game.clear_members()
                continue

            # now we are in game

            # if self.client.client_phase in ["GameStart", "InProgress"]:
            #     members = self.game.members
            #     self.vision.clear_templates()
            #     logger.error(members)
            #     for member in members:
            #         await self.vision.load_champion_template(member)

            try:
                if not self.vision.templates:
                    for member in self.game.members.values():
                        await self.vision.load_champion_template(member.championName)

                await asyncio.sleep(0.01)
                self.vision.shot_window(
                    {"top": 1080 - 420, "left": 1920 - 420, "width": 420, "height": 420}
                )
                # we need to know where everyone is:
                await self.locate_champions_on_minimap()
                # await self.update_player_location()
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
                logger.error(f"{e} - {inspect.stack[1][3]}")

    async def locate_champions_on_minimap(self):
        await self.vision.minimap_match()
        # then update the position of each champion
        for member_name in list(self.game.members):
            member = self.game.members.get(member_name)
            member.x = self.vision.templates.get(member_name).x
            member.y = self.vision.templates.get(member_name).y
            if member.x and member.y:
                member.zone = await self.find_closest_zone(member)

    async def update_player_location(self):
        x = self.game.members.get(self.game.player.info.championName).x
        y = self.game.members.get(self.game.player.info.championName).y

    async def find_closest_zone(self, member):
        # Use a distance function from specific points and the closest is the position
        distances = dict()
        for zone in ZONES:
            distance = pythagorean_distance((member.x, member.y), (zone.x, zone.y))
            distances[distance] = zone
            closest = min(list(distances))
        return distances[closest]
