import asyncio
import inspect
import time

from .common.loop import LoopInNewThread
from .common.zones import ZONES_210 as ZONES
from .common.utils import pythagorean_distance, average_position
from .game_watcher import GameWatcher
from .league_client import LeagueClient
from .controller import Controller
from .logger import get_logger
from .vision import Vision

logger = get_logger("LPBv2.Bot")


class LeaguePyBot:
    def __init__(self):

        logger.warning("Welcome to LeaguePyBotV2")

        self.client = LeagueClient()
        self.game = GameWatcher()
        self.minimap = Vision()
        self.screen = Vision()
        self.controller = Controller()
        self.loop = LoopInNewThread()
        self.loop.submit_async(self.run_bot())
        self.FPS = float()

    async def run_bot(self):
        loop_time = time.time()
        while True:
            if not self.game.game_flow.is_ingame or not self.game.members:
                await self.reset()
                continue

            try:
                # Load templates only once when the game starts
                if not self.minimap.templates:
                    names = [
                        member.championName for member in self.game.members.values()
                    ]
                    logger.info(names)
                    await self.minimap.load_templates(
                        names=names, folder="champions_16x16"
                    )

                if not self.screen.templates:
                    await self.screen.load_templates(
                        names=["minion", "champion", "building"], folder="units"
                    )
                await asyncio.sleep(0.01)

                # Minimap update
                await self.minimap.shot_window(
                    {
                        "top": 1080 - 210,
                        "left": 1920 - 210,
                        "width": 210,
                        "height": 210,
                    }
                )
                await self.locate_champions_on_minimap()
                await self.minimap.mark_the_spot()
                await self.game.update_player_location()

                # Units on screen update
                await self.screen.shot_window(
                    {"top": 0, "left": 0, "width": 1920, "height": 1080 - 420}
                )
                await self.locate_game_objects()
                await self.screen.mark_the_spot()

                # if (
                #     self.game.player.info.zone
                #     and self.game.player.info.zone.name == "Shop"
                #     and self.game.player.info.currentGold >= 500
                # ):
                #     await self.buy_recommended_items()

                # if self.game.player.stats.currentHealth > (
                #     self.game.player.stats.maxHealth * 0.9
                # ) and self.game.player.stats.resourceValue > (
                #     self.game.player.stats.resourceMax * 0.9
                # ):
                #     await self.go_to_lane()

                # if units on screen
                if self.game.game_units.is_minions_present():
                    await self.farm_lane()

                # Then locate the safest minion and attack it
                # If the number of enemy minions > ally minions
                # Go to the safest ally minion and attack

                # we need to know what is happening
                # turrets destroyed
                # inhibs destroyed
                # nexus destroyed
                # champion kills

                await self.update_FPS(1 / (time.time() - loop_time))
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

    async def update_FPS(self, value):
        self.FPS = round(float(value), 2)

    async def locate_champions_on_minimap(self):
        await self.minimap.match(match_best_only=True)
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
        await self.screen.match()
        await self.game.game_units.update(self.screen.matches)

    async def buy_recommended_items(self):
        await self.game.game_flow.update_current_action("Buying Recommended Items")
        self.keyboard.key("p")
        time.sleep(5)
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
                self.controller.click_minimap(zone.x, zone.y)
            if (
                zone.name == "Mid T1"
                and zone.team == self.game.player.info.team
                and mid < 1
            ):
                self.controller.click_minimap(zone.x, zone.y)
            if (
                zone.name == "Bot T1"
                and zone.team == self.game.player.info.team
                and bot < 2
            ):
                self.controller.click_minimap(zone.x, zone.y)

    async def go_to_lane(self):
        await self.game.game_flow.update_current_action("Going Toplane")
        for zone in ZONES:
            if zone.name == "Top T1" and zone.team == self.game.player.info.team:
                self.controller.click_minimap(zone.x, zone.y)

    async def get_minion_position(self, team="CHAOS"):
        if team == "CHAOS":
            minions = self.game.game_units.units.enemy_minions
        else:
            minions = self.game.game_units.units.ally_minions
        if minions:
            x, y = average_position(minions)
            return x, y

    async def farm_lane(self):

        units = await self.game.game_units.get_game_units()

        minion_advantage = False
        if units.nb_ally_minions > units.nb_enemy_minions:
            minion_advantage = True

        champion_advantage = False
        if units.nb_ally_champions > units.nb_enemy_champions:
            champion_advantage = True

        building_advantage = False
        if units.nb_ally_buildings > units.nb_enemy_buildings:
            building_advantage = True

        advantage = False
        if minion_advantage and champion_advantage or building_advantage:
            advantage = True

        if advantage:
            pos = await self.get_minion_position("CHAOS")
            if pos:
                await self.attack(*pos)
            else:
                advantage = False

        if not advantage:
            pos = await self.get_minion_position("ORDER")
            if pos:
                await self.fall_back(*pos)
            else:
                await self.go_to_lane()

    async def attack(self, x: int, y: int):
        await self.game.game_flow.update_current_action(f"Attacking {x}, {y}")
        self.controller.attack_move(x, y)

    async def fall_back(self, x: int, y: int):
        await self.game.game_flow.update_current_action(f"Falling back to {x}, {y}")
        self.controller.right_click(x, y)

    async def heal(self):
        await self.game.game_flow.update_current_action("Healing")
        # if summoner spell heal
        # if consumable
        self.keyboard.key("2")

    async def recall(self):
        zone = await self.find_closest_ally_zone(
            self.game.player.info.x, self.game.player.info.y
        )
        self.fall_back(zone.x, zone.y)
        await asyncio.sleep(8)
        await self.game.game_flow.update_current_action("Recalling")
        self.keyboard.key("b")
        await asyncio.sleep(10)
