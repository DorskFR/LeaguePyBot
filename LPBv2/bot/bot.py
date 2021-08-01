import os
import resource
from time import time
from asyncio import sleep

import psutil

from .. import *
from ..logger import Colors, get_logger

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
            installation_path=self.client.http.lockfile.installation_path
        )
        self.FPS = float()
        self.loop = LoopInNewThread()
        self.mem = None
        self.cpu = None
        self.loop.submit_async(self.bot_loop())

    async def bot_loop(self):
        loop_time = time()
        while True:

            if not await self.is_in_game():
                await self.reset()
                await sleep(0.01)
                continue

            await self.update_memory_usage()
            await self.update_cpu_usage()
            # await self.computer_vision()
            # await self.update_game_objects()
            # await self.decide_actions()
            # await self.execute_actions()
            self.FPS = round(float(1 / (time() - loop_time)), 2)
            loop_time = time()
            await sleep(0.01)

    async def is_in_game(self):
        return self.game.game_flow.is_ingame and self.game.members

    async def reset(self):
        if self.minimap.templates:
            await self.minimap.clear_templates()
        if self.screen.templates:
            await self.screen.clear_templates()
        if self.game.members:
            await self.game.clear_members()

    async def prepare_vision_objects(self):
        if not self.minimap.templates:
            names = await self.game.get_member_names()
            await self.minimap.load_templates(names=names, folder="champions_16x16")
        if not self.screen.templates:
            await self.screen.load_templates(
                names=["minion", "champion", "building_1", "building_2"],
                folder="units",
            )

    async def computer_vision(self):
        await self.prepare_vision_objects()
        await self.minimap.screenshot()
        await self.minimap.match(match_best_only=True)
        await self.screen.screenshot()
        await self.screen.match()

    async def update_member_location(self):
        for name in self.game.get_member_names():
            match = await self.minimap.get_match(name)
            if match:
                zone = await self.find_closest_zone(match.x, match.y)
                await self.game.update_member_location(name, match, zone)

    async def udpdate_units_position(self):
        await self.game.game_units.update(self.screen.matches)

    async def update_game_objects(self):
        await self.game.update_members(self.minimap.matches)
        await self.game.update_units(self.screen.matches)

    async def decide_actions(self):
        pass

    async def execute_actions(self):
        for action in self.actions:
            action.execute()

    async def update_memory_usage(self):
        # self.mem = round(psutil.Process().memory_info().rss / 1024 ** 2, 2)
        # peak memory usage in bytes on macos
        self.mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 ** 2

    async def update_cpu_usage(self):
        # self.cpu = psutil.Process().cpu_percent()
        # Getting loadover15 minutes
        load1, load5, load15 = psutil.getloadavg()
        self.cpu = round((load1 / os.cpu_count()) * 100, 2)

    async def recursive_buy(self, item_list):

        if (
            not item_list[0] in self.game.player.inventory
            and self.game.player.currentGold > item_list[0].price
        ):
            if (
                not all_items[item_list[0]].get("from")
                and len(self.game.player.inventory) > 6
            ):
                return
            await self.controller.shop.buy_item(item_list[0])

        if all_items[item_list[0]].get("from"):
            await self.recursive_buy(all_items[item_list[0]].get("from"))

        if len(item_list > 1):
            await self.recursive_buy(item_list[1:])

    async def buy_my_build(self):
        # 1. Check my build items order
        # build_items = [1,2,3,4,5,6]
        build_items = [1001, 2003, 3077, 3026, 3181, 3053, 3340]
        all_items = {}
        # 2. Check my inventory and the items I already bought
        # build_items_1 = OK, build_items_2 = OK, build_items_3 = NOT OK

        self.try_to_buy_list(build_items)

        for item in build_items:
            if item in self.game.player.inventory:
                continue
            if self.game.player.currentGold > item.price:
                # buy_item(item)
                pass
            else:
                components = all_items.get(item).get("from")
                for component in components:
                    if component in self.game.player.inventory:
                        continue
                    if self.game.player.currentGold > component.price:
                        # buy_item(component)
                        pass
                    else:
                        # stop_shopping
                        pass

        # 3. Check build_items_3 recipe (from) = [A, B, C, D]
        # 4. Check my inventory for the build_items_3 components
        # A = OK, B = OK, C = NOT OK
        # 5. Calculate remaining cost of build_items_3 and check if my gold is enough
        # If gold is not enough for build_items_3
        # If gold is enough for C buy C
        # If gold is not enough for D, stop shop interaction
        # Else if gold is enough, buy build_items_3
        # Then loop on the shop buying function
        # Exits from the shop buying function
        # Not enough gold for something in the case of a component (not combine)
        # Or not enough space in inventory in the case of a component (not combine)
        pass
