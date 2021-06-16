from typing import List, Optional

from .models import InventoryItem, PlayerInfo, PlayerScore, PlayerStats


class Player:
    def __init__(self):
        self.info: Optional[PlayerInfo]
        self.stats: Optional[PlayerStats]
        self.score: Optional[PlayerScore]
        self.inventory: Optional[List[InventoryItem]]

    def update(self, active_player_data, all_players_data):
        for player_data in all_players_data:
            if player_data.get("summonerName") == active_player_data.get(
                "summonerName"
            ):
                self.info = PlayerInfo(
                    name=active_player_data.get("summonerName"),
                    level=active_player_data.get("level"),
                    currentGold=active_player_data.get("currentGold"),
                    championName=player_data.get("championName"),
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
