from typing import List, Optional

from ..common import (
    InventoryItem,
    PlayerInfo,
    PlayerScore,
    PlayerStats,
    TeamMember,
    debug_coro,
)
from ..logger import get_logger, Colors

logger = get_logger("LPBv2.Player")


class Player:
    def __init__(self, *args, **kwargs):
        self.info = PlayerInfo()
        self.stats = PlayerStats()
        self.score = PlayerScore()
        self.inventory: Optional[List[InventoryItem]] = list()
        self.level_up: Optional[bool] = False
        self.taking_damage: Optional[bool] = False

    @debug_coro
    async def update(self, update_data):
        await self.update_info(update_data)
        await self.update_stats(update_data)
        await self.update_score(update_data)
        await self.update_inventory(update_data)

    @debug_coro
    async def update_info(self, update_data):
        if self.info.level != update_data.get("level"):
            self.level_up = True
        self.info = PlayerInfo(
            name=update_data.get("summonerName"),
            level=update_data.get("level"),
            currentGold=update_data.get("currentGold"),
            championName=update_data.get("rawChampionName").split("_")[-1],
            isDead=update_data.get("isDead"),
            respawnTimer=update_data.get("respawnTimer"),
            position=update_data.get("position"),
            team=update_data.get("team"),
        )

    @debug_coro
    async def update_stats(self, update_data):
        if self.stats.currentHealth and (
            self.stats.currentHealth
            - float(update_data.get("championStats").get("currentHealth"))
            > 100
        ):
            self.taking_damage = True
        self.stats = PlayerStats(**update_data.get("championStats"))

    @debug_coro
    async def update_score(self, update_data):
        self.score = PlayerScore(**update_data.get("scores"))

    @debug_coro
    async def update_inventory(self, update_data):
        self.inventory = [InventoryItem(**item) for item in update_data.get("items")]

    @debug_coro
    async def update_location(self, self_member: TeamMember):
        self.info.x = self_member.x
        self.info.y = self_member.y
        self.info.zone = self_member.zone

    @debug_coro
    async def has_more_than_50_percent_mana(self):
        return self.stats.resourceValue >= (self.stats.resourceMax * 0.5)

    @debug_coro
    async def has_more_than_25_percent_mana(self):
        return self.stats.resourceValue >= (self.stats.resourceMax * 0.25)

    @debug_coro
    async def is_low_life(self):
        return self.stats.currentHealth < (self.stats.maxHealth * 0.4)

    @debug_coro
    async def is_half_life(self):
        return self.stats.currentHealth < (self.stats.maxHealth * 0.6)

    @debug_coro
    async def is_rich(self):
        return self.info.currentGold > 3000

    @debug_coro
    async def get_consumable_slot(self):
        for item in self.inventory:
            if item.consumable:
                return item.slot
