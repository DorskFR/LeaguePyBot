import asyncio
import inspect
import time

from .common import LoopInNewThread, ZONES
from .common.utils import pythagorean_distance, average_position
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
        self.loop = LoopInNewThread()
        self.loop.submit_async(self.run_bot())

    async def run_bot(self):
        loop_time = time.time()
        while True:
            if not self.game.is_ingame or not self.game.members:
                await self.reset()
                continue

            try:

                # Load templates only once when the game starts
                if not self.minimap.templates:
                    for member in self.game.members.values():
                        await self.minimap.load_champion_template(member.championName)

                # if not self.screen.templates:
                #     await self.screen.load_game_templates()
                # await asyncio.sleep(0.01)

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

                # Units on screen update
                # await self.screen.shot_window(
                #     {"top": 0, "left": 0, "width": 1920, "height": 1080 - 420}
                # )
                # await self.locate_game_objects()

                # If in shop, lazy buy, wait full health and mana
                # if (
                #     self.game.player.info.zone
                #     and self.game.player.info.zone.name == "Shop"
                # ):
                #     if self.game.player.info.currentGold >= 500:
                #         await self.buy_recommended_items()

                # if self.game.player.stats.currentHealth > (
                #     self.game.player.stats.maxHealth * 0.9
                # ) and self.game.player.stats.resourceValue > (
                #     self.game.player.stats.resourceMax * 0.9
                # ):
                #     await self.go_to_lane()

                # if units on screen
                # if self.game.units_count.get("CHAOS") or self.game.units_count.get(
                #     "ORDER"
                # ):
                #     await self.farm_lane()

                # Then locate the safest minion and attack it
                # If the number of enemy minions > ally minions
                # Go to the safest ally minion and attack

                # we need to know what is happening
                # turrets destroyed
                # inhibs destroyed
                # nexus destroyed
                # champion kills

                self.game.FPS = round(1 / (time.time() - loop_time), 2)
                loop_time = time.time()
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
                zone = await self.find_closest_zone(match.x, match.y)
                await self.game.update_member_location(name, match, zone)

    async def find_closest_zone(self, x: int, y: int, zones=ZONES):
        # Use a distance function from specific points and the closest is the position
        distances = dict()
        for zone in zones:
            distance = pythagorean_distance((x, y), (zone.x, zone.y))
            distances[distance] = zone
            closest = min(list(distances))
        return distances[closest]

    async def find_closest_ally_zone(self, x: int, y: int):
        # Use a distance function from specific points and the closest is the position
        zones = [zone for zone in ZONES if zone.team == self.game.player.info.team]
        return await self.find_closest_zone(x, y, zones=zones)

    async def locate_game_objects(self):
        await self.screen.screen_match()
        await self.game.update_units(self.screen.matches)

    async def buy_recommended_items(self):
        self.keyboard.key("p")
        time.sleep(1)
        logger.error("Buying recommended items...")
        self.keyboard.key("p")
        time.sleep(1)

    async def go_to_free_lane(self):
        top = 0
        mid = 0
        bot = 0

        for member in self.game.members:
            if "top" in member.zone.name.lower():
                top += 1
            if "bot" in member.zone.name.lower():
                bot += 1
            if "mid" in member.zone.name.lower():
                mid += 1

        for zone in ZONES:
            if (
                zone.name == "Top T1"
                and zone.team == self.game.player.info.team
                and top < 2
            ):
                self.mouse.right_click(zone.x, zone.y)
            if (
                zone.name == "Mid T1"
                and zone.team == self.game.player.info.team
                and mid < 1
            ):
                self.mouse.right_click(zone.x, zone.y)
            if (
                zone.name == "Bot T1"
                and zone.team == self.game.player.info.team
                and bot < 2
            ):
                self.mouse.right_click(zone.x, zone.y)

    async def go_to_lane(self):
        await self.game.update_current_action("Going Toplane")
        for zone in ZONES:
            if zone.name == "Top T1" and zone.team == self.game.player.info.team:
                self.mouse.right_click(zone.x, zone.y)

    async def get_minion_position(self, team="CHAOS"):
        minions = [
            unit
            for unit in self.game.units
            if unit.name == "minion" and unit.team == team
        ]
        x, y = average_position(minions)
        return x, y

    async def farm_lane(self):
        x, y = await self.get_minion_position("CHAOS")
        await self.attack(x, y)
        x, y = await self.get_minion_position("ORDER")
        await self.fall_back(x, y)

    async def attack(self, x: int, y: int):
        await self.game.update_current_action(f"Attacking {x}, {y}")
        self.keyboard.press("a")
        self.mouse.set_position(x, y)
        self.mouse.right_click()
        self.keyboard.release("a")

    async def fall_back(self, x: int, y: int):
        await self.game.update_current_action(f"Falling back to {x}, {y}")
        self.mouse.set_position(x, y)
        self.mouse.right_click()

    async def heal(self):
        await self.game.update_current_action("Healing")
        # if summoner spell heal
        # if consumable
        self.keyboard.key("2")

    async def recall(self):
        zone = await self.find_closest_ally_zone(
            self.game.player.info.x, self.game.player.info.y
        )
        self.fall_back(zone.x, zone.y)
        await asyncio.sleep(8)
        await self.game.update_current_action("Recalling")
        self.keyboard.key("b")
        await asyncio.sleep(10)
