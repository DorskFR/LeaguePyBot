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
                    {
                        "top": 1080 - 420,
                        "left": 1920 - 420,
                        "width": 420,
                        "height": 420,
                    }
                )
                await self.locate_champions_on_minimap()
                await self.game.update_player_location()
                # await self.minimap.mark_the_spot()

                # Screen update
                await self.screen.shot_window(
                    {"top": 0, "left": 0, "width": 1920, "height": 1080 - 420}
                )
                await self.locate_game_objects()
                # await self.screen.mark_the_spot()

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
        for name in list(self.game.members):
            match = await self.minimap.get_match(name)
            if match:
                zone = await self.find_closest_zone(match)
                await self.game.update_member_location(name, match, zone)

    async def find_closest_zone(self, match):
        # Use a distance function from specific points and the closest is the position
        distances = dict()
        for zone in ZONES:
            distance = pythagorean_distance((match.x, match.y), (zone.x, zone.y))
            distances[distance] = zone
            closest = min(list(distances))
        return distances[closest]

    async def locate_game_objects(self):
        await self.screen.screen_match()
        await self.game.update_units(self.screen.matches)
