from typing import List, Optional

from ..common.utils import merge_dicts
from ..common.models import (
    InventoryItem,
    PlayerInfo,
    PlayerScore,
    PlayerStats,
    TeamMember,
)


class Player:
    def __init__(self):
        self.info = PlayerInfo()
        self.stats = PlayerStats()
        self.score = PlayerScore()
        self.inventory: Optional[List[InventoryItem]] = list()
        self.location: Optional[str] = "UNKNOWN"

    async def update(self, update_data):
        await self.update_info(update_data)
        await self.update_stats(update_data)
        await self.update_score(update_data)
        await self.update_inventory(update_data)

    async def update_info(self, update_data):
        self.info = PlayerInfo(
            name=update_data.get("summonerName"),
            level=update_data.get("level"),
            currentGold=update_data.get("currentGold"),
            championName=update_data.get("abilities").get("E").get("id")[:-1],
            isDead=update_data.get("isDead"),
            respawnTimer=update_data.get("respawnTimer"),
            position=update_data.get("position"),
            team=update_data.get("team"),
        )

    async def update_stats(self, update_data):
        self.stats = PlayerStats(**update_data.get("championStats"))

    async def update_score(self, update_data):
        self.score = PlayerScore(**update_data.get("scores"))

    async def update_inventory(self, update_data):
        self.inventory = [InventoryItem(**item) for item in update_data.get("items")]

    async def update_location(self, self_member: TeamMember):
        self.info.x = self_member.x
        self.info.y = self_member.y
        self.info.zone = self_member.zone
