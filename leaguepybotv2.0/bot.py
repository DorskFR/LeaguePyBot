import asyncio
import inspect
import time

from .common.loop import LoopInNewThread
from .common.zones import ZONES_210 as ZONES
from .common.utils import (
    pythagorean_distance,
    average_position,
    safest_position,
    riskiest_position,
)
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
                    await self.minimap.load_templates(
                        names=names, folder="champions_16x16"
                    )
                # if not self.screen.templates:
                #     await self.screen.load_templates(
                #         names=["minion", "champion", "building_1", "building_2"],
                #         folder="units",
                #     )
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
                # await self.screen.shot_window(
                #     {"top": 0, "left": 0, "width": 1920, "height": 1080 - 210}
                # )
                # await self.locate_game_objects()
                # await self.screen.mark_the_spot()

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
                # if not self.game.player.info.isDead:
                #     await self.farm_lane()

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

    async def find_closest_ally_zone(self):
        x = 0
        y = 210
        if self.game.player.info.zone:
            x = self.game.player.info.zone.x
            y = self.game.player.info.zone.y
        safe_zones = [zone for zone in ZONES if zone.team == self.game.player.info.team]
        return await self.find_closest_zone(x, y, zones=safe_zones)

    async def locate_game_objects(self):
        await self.screen.match()
        await self.game.game_units.update(self.screen.matches)

    async def buy_recommended_items(self):
        await self.game.game_flow.update_current_action("Buying Recommended Items")
        await self.controller.toggle_shop()
        time.sleep(5)
        await self.controller.toggle_shop()
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
                await self.controller.click_minimap(zone.x, zone.y)
            if (
                zone.name == "Mid T1"
                and zone.team == self.game.player.info.team
                and mid < 1
            ):
                await self.controller.click_minimap(zone.x, zone.y)
            if (
                zone.name == "Bot T1"
                and zone.team == self.game.player.info.team
                and bot < 2
            ):
                await self.controller.click_minimap(zone.x, zone.y)

    async def go_to_lane(self):
        await self.game.game_flow.update_current_action("Going Toplane")
        for zone in ZONES:
            if zone.name == "Top T1" and zone.team == self.game.player.info.team:
                await self.controller.click_minimap(zone.x, zone.y)

    async def follow_allies(self):
        await self.game.game_flow.update_current_action("Following ally minions")
        pos = await self.get_riskiest_ally_position()
        if pos:
            await self.controller.attack_move(*pos)

    async def get_riskiest_ally_position(self):
        minions = self.game.game_units.units.ally_minions
        if minions:
            return riskiest_position(minions)

    async def get_closest_enemy_position(self):
        minions = self.game.game_units.units.enemy_minions
        if minions:
            return safest_position(minions)

    async def get_safest_ally_position(self):
        minions = self.game.game_units.units.ally_minions
        if minions:
            return safest_position(minions)

    async def attack_minions(self):
        pos = await self.get_closest_enemy_position()
        if pos:
            await self.attack(*pos)
        pos = await self.get_average_enemy_position()
        if await self.game.player.has_more_than_50_percent_mana() and pos:
            await self.cast_spells(*pos)

    async def get_average_enemy_position(self):
        minions = self.game.game_units.units.enemy_minions
        if minions:
            return average_position(minions)

    async def attack_champion(self):
        pos = await self.get_closest_enemy_champion_position()
        if pos:
            await self.attack(*pos)
            if await self.game.player.has_more_than_50_percent_mana() and pos:
                await self.cast_spells(*pos, r=True)

    async def get_closest_enemy_champion_position(self):
        champions = self.game.game_units.units.enemy_champions
        if champions:
            return safest_position(champions)

    async def get_closest_enemy_building_position(self):
        buildings = self.game.game_units.units.enemy_buildings
        if buildings:
            return safest_position(buildings)

    async def attack(self, x: int, y: int):
        await self.game.game_flow.update_current_action(f"Attacking {x}, {y}")
        await self.controller.attack_move(x, y)

    async def cast_spells(self, x: int, y: int, r=False):
        await asyncio.sleep(1)
        await self.controller.cast_spell("q", x, y)
        await self.controller.cast_spell("e", x, y)
        await self.controller.cast_spell("w", x, y)
        if r:
            await self.controller.cast_spell("r", x, y)

    async def farm_lane(self):
        units = await self.game.game_units.get_game_units()

        allies = units.nb_ally_minions > 0 or units.nb_ally_champions > 0
        enemies = (
            units.nb_enemy_minions > 0
            or units.nb_enemy_champions > 0
            or units.nb_enemy_buildings > 0
        )

        if await self.game.player.is_half_life():
            await self.heal()

        if await self.game.player.is_low_life():
            await self.recall()

        if not allies and not enemies:
            await self.go_to_lane()

        if allies and not enemies:
            await self.follow_allies()

        if enemies and not allies:
            await self.fall_back()

        if enemies and allies:

            building_fight_condition = (
                units.nb_ally_minions > units.nb_enemy_minions
                and units.nb_ally_minions > 3
                and units.nb_enemy_champions == 0
                and units.nb_enemy_buildings > 0
            )

            minion_fight_condition = (
                (
                    units.nb_ally_minions > (units.nb_enemy_minions / 2)
                    or (units.nb_ally_minions > 0 and units.nb_ally_buildings > 0)
                    or (units.nb_ally_minions > 2 and units.nb_ally_champions > 0)
                )
                and units.nb_enemy_champions == 0
                and units.nb_enemy_buildings == 0
            )

            champion_fight_condition = (
                units.nb_enemy_champions > 0
                and (
                    (units.nb_ally_minions > 0 and units.nb_ally_buildings > 0)
                    or (units.nb_ally_minions > units.nb_enemy_minions)
                )
                and (
                    units.nb_enemy_champions < 3
                    or units.nb_ally_champions > units.nb_enemy_champions
                )
                and units.nb_enemy_buildings == 0
            )

            if building_fight_condition:
                logger.warning(f"Attacking because building_fight_condition is met")
                await self.attack_building()

            elif champion_fight_condition:
                logger.warning(f"Attacking because champion_fight_condition is met")
                await self.attack_champion()

            elif minion_fight_condition:
                logger.warning(f"Attacking because minion_fight_condition is met")
                await self.attack_minions()

            else:
                await self.fall_back()

    async def fall_back(self):
        zone = await self.find_closest_ally_zone()
        await self.game.game_flow.update_current_action(f"Falling back to {zone.name}")
        await self.controller.click_minimap(zone.x, zone.y)

    async def heal(self):
        await self.game.game_flow.update_current_action("Healing")
        slot = await self.game.player.get_consumable_slot()
        if slot:
            await self.controller.use_item(slot)
        await self.controller.use_summoner_spell_2()

    async def recall(self):
        await self.controller.use_summoner_spell_1()
        await self.fall_back()
        time.sleep(8)
        await self.game.game_flow.update_current_action("Recalling")
        await self.controller.recall()
        time.sleep(15)
