import os
import time
from asyncio import sleep

import psutil
from LPBv2.common import debug_coro

from .. import *
from ..logger import Colors, get_logger
from ..common import find_closest_zone, MinimapZone

logger = get_logger("LPBv2.Bot")


class LeaguePyBot:
    def __init__(self):
        logger.info(f"Welcome to {Colors.yellow}LeaguePyBotV2{Colors.reset}")
        self.client = Client()
        self.game = Game()
        self.build = Build(
            client=self.client,
            champion_id=114,
        )
        self.minimap = Vision(
            bounding_box={
                "top": 1080 - 210,
                "left": 1920 - 210,
                "width": 210,
                "height": 210,
            }
        )
        self.screen = Vision()
        self.controller = Controller(
            game=self.game,
            build=self.build,
            hotkeys=self.client.hotkeys,
        )
        self.FPS = float()
        self.loop = LoopInNewThread()
        self.mem = None
        self.cpu = None
        time.sleep(5)
        self.loop.submit_async(self.bot_loop())

    @debug_coro
    async def bot_loop(self):
        loop_time = time.time()

        while True:

            if not await self.is_in_game():
                await self.reset()
                await sleep(0.01)
                continue

            await self.update_memory_usage()
            await self.update_cpu_usage()
            await self.computer_vision()
            await self.update_game_objects()
            await self.execute_actions()
            self.FPS = round(float(1 / (time.time() - loop_time)), 2)
            loop_time = time.time()

    @debug_coro
    async def is_in_game(self):
        return self.game.game_flow.is_ingame and self.game.members

    @debug_coro
    async def reset(self):
        if self.minimap.templates:
            await self.minimap.clear_templates()
        if self.screen.templates:
            await self.screen.clear_templates()
        if self.game.members:
            await self.game.clear_members()

    @debug_coro
    async def prepare_vision_objects(self):
        if not self.minimap.templates:
            names = await self.game.get_member_names()
            await self.minimap.load_templates(names=names, folder="champions_16x16")
        if not self.screen.templates:
            await self.screen.load_templates(
                names=["minion", "champion", "building_1", "building_2"],
                folder="units",
            )

    @debug_coro
    async def computer_vision(self):
        await self.prepare_vision_objects()
        await self.minimap.screenshot()
        await self.minimap.match(match_best_only=True)
        await self.screen.screenshot()
        await self.screen.match()

    @debug_coro
    async def update_member_location(self):
        for name in self.game.get_member_names():
            match = await self.minimap.get_match(name)
            if match:
                zone = find_closest_zone(match.x, match.y)
                await self.game.update_member_location(name, match, zone)

    @debug_coro
    async def udpdate_units_position(self):
        await self.game.game_units.update(self.screen.matches)

    @debug_coro
    async def update_game_objects(self):
        await self.game.update_members(self.minimap.matches)
        await self.game.update_units(self.screen.matches)

    @debug_coro
    async def update_memory_usage(self):
        self.mem = round(psutil.Process().memory_info().rss / 1024 ** 2, 2)

    @debug_coro
    async def update_cpu_usage(self):
        load1, load5, load15 = psutil.getloadavg()
        self.cpu = round((load1 / os.cpu_count()) * 100, 2)

    @debug_coro
    async def execute_actions(self):
        units = await self.game.game_units.get_game_units()

        allies = units.nb_ally_minions > 0 or units.nb_ally_champions > 0
        enemies = (
            units.nb_enemy_minions > 0
            or units.nb_enemy_champions > 0
            or units.nb_enemy_buildings > 0
        )

        if self.game.player.info.level == 1 and self.game.game_flow.time < 15.0:
            await sleep(5)
            await self.controller.shop.buy_build(self.build.starter_build)
            await sleep(10)

        if self.game.player.level_up:
            await self.controller.combat.level_up_abilities()
            self.game.player.level_up = False

        if self.game.player.info.isDead or (
            self.game.player.info.zone and self.game.player.info.zone.name == "Shop"
        ):
            await self.controller.shop.buy_build(self.build.item_build)
            await sleep(1)

        if await self.game.player.is_half_life():
            await self.controller.usable.heal()

        if await self.game.player.is_low_life():
            await self.controller.usable.use_summoner_spell_1()

        if await self.game.player.is_low_life() or await self.game.player.is_rich():
            await self.controller.movement.fall_back(reason="Low life or rich")
            await sleep(8)
            await self.controller.movement.recall()
            await sleep(15)
            await self.controller.shop.buy_build(self.build.item_build)

        if self.game.player.taking_damage:
            await self.controller.movement.fall_back(reason="Taking heavy damage")
            self.game.player.taking_damage = False
            await sleep(2)

        if not allies and not enemies:
            await self.controller.movement.go_to_lane()
            await sleep(3)

        if allies and not enemies:
            await self.controller.movement.follow_allies()

        if enemies and not allies:
            await self.controller.movement.fall_back(reason="No allies around")

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
                await self.controller.combat.attack_building()

            elif champion_fight_condition:
                logger.warning(f"Attacking because champion_fight_condition is met")
                await self.controller.combat.attack_champion()

            elif minion_fight_condition:
                logger.warning(f"Attacking because minion_fight_condition is met")
                await self.controller.combat.attack_minions()

            else:
                await self.controller.movement.fall_back(reason="Lost")
