import asyncio
import inspect
from time import time

from .common import Loop, ZONES
from .common.utils import pythagorean_distance
from .game_watcher import GameWatcher
from .league_client import LeagueClient
from .logger import get_logger
from .peripherals import Keyboard, KeyboardListener, Mouse, Vision
from .common.models import Unit

logger = get_logger("LPBv2.Bot")


class LeaguePyBot:
    def __init__(self):

        logger.warning("Welcome to LeaguePyBotV2")

        self.client = LeagueClient()
        self.game = GameWatcher()
        self.minimap = Vision()
        self.screen = Vision()
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.listener = KeyboardListener()
        self.loop = Loop()
        self.loop.submit_async(self.run_bot())

    async def run_bot(self):
        loop_time = time()
        while True:
            if not self.game.is_ingame or not self.game.members:
                await self.reset()
                continue

            try:

                # Load templates only once when the game starts
                if not self.minimap.templates:
                    for member in self.game.members.values():
                        await self.minimap.load_champion_template(member.championName)

                if not self.screen.templates:
                    await self.screen.load_game_templates()

                await asyncio.sleep(0.01)

                # Minimap update
                await self.minimap.shot_window(
                    {"top": 1080 - 420, "left": 1920 - 420, "width": 420, "height": 420}
                )
                await self.locate_champions_on_minimap()
                await self.update_player_location()

                # Screen update
                await self.screen.shot_window(
                    {"top": 100, "left": 100, "width": 1920 - 200, "height": 1920 - 420}
                )
                await self.locate_game_objects()

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

                # TODO: Ignored for now because the game auto-buys in coop
                # we need to know what we have in inventory
                # we need to know what to buy

                self.game.FPS = round(1 / (time() - loop_time), 2)
                loop_time = time()
            except Exception as e:
                logger.error(f"{e} - {inspect.stack[1][3]}")

    async def reset(self):
        if self.minimap.templates:
            await self.minimap.clear_templates()
        if self.screen.templates:
            await self.screen.clear_templates()
        if self.game.members:
            await self.game.clear_members()

    async def locate_champions_on_minimap(self):
        await self.minimap.minimap_match()
        # then update the position of each champion
        for member_name in list(self.game.members):
            member = self.game.members.get(member_name)
            match = await self.minimap.get_match(member_name)
            if match:
                member.x = match.x
                member.y = match.y
            if member.x and member.y:
                member.zone = await self.find_closest_zone(member)

    async def update_player_location(self):
        self_member = self.game.members.get(self.game.player.info.championName)
        self.game.player.info.x = self_member.x
        self.game.player.info.y = self_member.y
        self.game.player.info.zone = self_member.zone

    async def find_closest_zone(self, member):
        # Use a distance function from specific points and the closest is the position
        distances = dict()
        for zone in ZONES:
            distance = pythagorean_distance((member.x, member.y), (zone.x, zone.y))
            distances[distance] = zone
            closest = min(list(distances))
        return distances[closest]

    async def locate_game_objects(self):
        await self.screen.screen_match()
        for match in self.screen.matches:
            self.game.units.append(Unit(type=match.name, x=match.x, y=match.y))
