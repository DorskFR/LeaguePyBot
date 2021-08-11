from ..common import LoopInNewThread, Caller, debug_coro
import time

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
        time.sleep(1)
        self.loop = LoopInNewThread()
        self.loop.submit_async(self.get_all_items())
        self.loop.submit_async(self.set_starter_build())
        self.loop.submit_async(self.set_item_build())
        

    @debug_coro
    async def get_version(self):
        url = f"https://ddragon.leagueoflegends.com/realms/{self.client.region}.json"
        versions = await self.caller.get(url)
        self.version = versions.get("n").get("item")

    @debug_coro
    async def get_all_items(self):
        if not self.version:
            await self.get_version()
        url = f"http://ddragon.leagueoflegends.com/cdn/{self.version}/data/{self.client.locale}/item.json"
        all_items = await self.caller.get(url)
        self.all_items = all_items.get("data")

    @debug_coro
    async def check_builds(self):
        logger.warning("Checking builds...")
        url = f"https://www.leaguepybot.dorsk.dev/api/builds"
        payload = {
            "region": self.client.region,
            "locale": self.client.locale,
            "champion": self.client.champ_select.champion_id,
            "summoner": self.game.player.info.name
        }
        call = await self.caller.post(url, payload)
        logger.warning(call)

    async def set_starter_build(self, build = ["1055", "2003", "3340"]):
        self.starter_build = build

    async def set_item_build(self, build = ["3074", "3006", "3508", "6692", "3072"]):
        self.item_build = build