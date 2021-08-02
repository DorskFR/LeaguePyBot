import os
import time
from asyncio import sleep

import psutil
from LPBv2.common import debug_func
from LPBv2.game import player

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
        time.sleep(5)
        self.loop.submit_async(self.bot_loop())

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
            # await self.decide_actions()
            # await self.execute_actions()
            self.FPS = round(float(1 / (time.time() - loop_time)), 2)
            loop_time = time.time()

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
        self.mem = round(psutil.Process().memory_info().rss / 1024 ** 2, 2)

    async def update_cpu_usage(self):
        load1, load5, load15 = psutil.getloadavg()
        self.cpu = round((load1 / os.cpu_count()) * 100, 2)

    async def recursive_buy(self, shop_list):
        player_items = [str(item.itemID) for item in self.game.player.inventory]
        composite = self.build.all_items.get(shop_list[0]).get("from")
        price = self.build.all_items.get(shop_list[0]).get("gold").get("total")
        name = self.build.all_items.get(shop_list[0]).get("name")

        if composite:
            for component in composite:
                if component in player_items:
                    price -= (
                        self.build.all_items.get(component).get("gold").get("total")
                    )

        if (
            not shop_list[0] in player_items
            and self.game.player.info.currentGold >= price
            and len(player_items) < 6
        ):
            await self.controller.shop.buy_item(name)

        elif (
            not shop_list[0] in player_items
            and (self.game.player.info.currentGold < price or len(player_items) >= 6)
            and composite
        ):
            await self.recursive_buy(composite)

        if len(shop_list) <= 1 or (
            (self.game.player.info.currentGold < price or len(player_items) >= 6)
            and not composite
        ):
            return

        await self.recursive_buy(shop_list[1:])

    async def buy_build(self):
        build = ["3077", "1001", "2003", "3026", "3181", "3053"]
        await self.controller.shop.toggle_shop()
        await self.recursive_buy(build)
        await self.controller.shop.toggle_shop()
