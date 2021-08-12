from ..common import Caller, debug_coro
import asyncio
from ..logger import get_logger

logger = get_logger("LPBv2.Build")


class Build:
    def __init__(self, client, game):
        self.caller = Caller()
        self.client = client
        self.game = game
        self.version: str = None
        self.runes: list = list()
        self.spells: list = list()
        self.starter_build: list = list()
        self.item_build: list = list()
        self.all_items: list = list()
        loop = asyncio.get_event_loop()
        loop.create_task(self.init_build())

    #@debug_coro
    async def init_build(self):
        while True:
            if (
                self.client.locale 
                and self.client.region 
            ):
                await self.get_all_items()
                if not self.starter_build :
                    await self.set_starter_build()
                if not self.item_build:
                    await self.set_item_build()
                logger.info(f"Builds loaded (starter: {self.starter_build}, items: {self.item_build})")
                break
            await asyncio.sleep(0.1)

    #@debug_coro
    async def get_all_items(self):
        if not self.version:
            await self.get_version()
        url = f"http://ddragon.leagueoflegends.com/cdn/{self.version}/data/{self.client.locale}/item.json"
        all_items = await self.caller.get(url)
        self.all_items = all_items.get("data")

    #@debug_coro
    async def get_version(self):
        url = f"https://ddragon.leagueoflegends.com/realms/{self.client.region}.json"
        versions = await self.caller.get(url)
        self.version = versions.get("n").get("item")

    #@debug_coro
    async def check_builds(self):
        url = f"https://www.leaguepybot.dorsk.dev/api/builds"
        payload = dict(**self.client.summoner.info.__dict__)
        payload["region"] = self.client.region
        payload["locale"] = self.client.locale
        payload["champion"] = self.client.champ_select.champion_id
        call = await self.caller.post(url, payload)

    #@debug_coro
    async def set_starter_build(self, build = ["1055", "2003", "3340"]):
        self.starter_build = build

    #@debug_coro
    async def set_item_build(self, build = ["3074", "3006", "3508", "6692", "3072"]):
        self.item_build = build
