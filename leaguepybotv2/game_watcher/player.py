from typing import List, Optional

from ..common.models import (
    InventoryItem,
    PlayerInfo,
    PlayerScore,
    PlayerStats,
    TeamMember,
)


class Player:
    def __init__(self):
        self.info: Optional[PlayerInfo]
        self.stats: Optional[PlayerStats]
        self.score: Optional[PlayerScore]
        self.inventory: Optional[List[InventoryItem]]

        self.location: Optional[str] = "UNKNOWN"

    async def update(self, active_player_data, all_players_data):
        for player_data in all_players_data:
            if player_data.get("summonerName") == active_player_data.get(
                "summonerName"
            ):
                self.info = PlayerInfo(
                    name=active_player_data.get("summonerName"),
                    level=active_player_data.get("level"),
                    currentGold=active_player_data.get("currentGold"),
                    championName=active_player_data.get("abilities")
                    .get("E")
                    .get("id")[:-1],
                    isDead=player_data.get("isDead"),
                    respawnTimer=player_data.get("respawnTimer"),
                    position=player_data.get("position"),
                    team=player_data.get("team"),
                )

                self.stats = PlayerStats(**active_player_data.get("championStats"))

                self.score = PlayerScore(**player_data.get("scores"))
                self.inventory = [
                    InventoryItem(**item) for item in player_data.get("items")
                ]

    async def update_location(self, self_member: TeamMember):
        self.info.x = self_member.x
        self.info.y = self_member.y
        self.info.zone = self_member.zone
