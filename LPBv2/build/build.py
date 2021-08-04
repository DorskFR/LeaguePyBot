from ..common import LoopInNewThread, Caller
import time


class Build:
    def __init__(self, client, champion_id):
        self.caller = Caller()
        self.client = client
        self.champion_id = champion_id
        self.version: str = None
        self.runes: list = list()
        self.spells: list = list()
        self.starter_build: list = list()
        self.item_build: list = list()
        self.all_items: list = list()
        time.sleep(1)
        self.loop = LoopInNewThread()
        self.loop.submit_async(self.get_all_items())
        self.loop.submit_async(self.get_starter_build())
        self.loop.submit_async(self.get_item_build())
        

    async def get_version(self):
        url = f"https://ddragon.leagueoflegends.com/realms/{self.client.region}.json"
        versions = await self.caller.get(url)
        self.version = versions.get("n").get("item")

    async def get_all_items(self):
        if not self.version:
            await self.get_version()
        url = f"http://ddragon.leagueoflegends.com/cdn/{self.version}/data/{self.client.locale}/item.json"
        all_items = await self.caller.get(url)
        self.all_items = all_items.get("data")

    async def get_starter_build(self):
        self.starter_build = ["1055", "2003", "3340"]

    async def get_item_build(self):
        self.item_build = ["3074", "3006", "3508", "6692", "3072"]