import asyncio
from typing import List

from ..common.champions import CHAMPIONS
from ..common.loop import LoopInNewThread
from ..common.models import Match, TeamMember
from ..common.utils import cast_to_bool
from .game_connector import GameConnector
from .game_flow import GameFlow
from .player import Player


class GameWatcher:
    def __init__(self):
        self.loop = LoopInNewThread()
        self.player = Player()
        self.members = dict()
        self.units = list()
        self.units_count = dict()
        self.game_flow = GameFlow()
        self.game_connector = GameConnector()
        self.loop.submit_async(self.update())

    async def update(self):
        while True:
            try:
                self.is_ingame = True
                data = await self.game_connector.request("/liveclientdata/allgamedata")
                await self.game_flow.update(
                    data.get("events").get("Events"), data.get("gameData")
                )
                await self.player.update(
                    data.get("activePlayer"), data.get("allPlayers")
                )
                if not self.members:
                    await self.create_members(data.get("allPlayers"))
                await self.count_units()
                await self.print_info()
                await asyncio.sleep(1)
            except:
                self.is_ingame = False

    async def clear_members(self):
        self.members = dict()

    async def update_units(self, matches: List[Match]):
        self.units = matches

    async def count_units(self):
        self.units_count = {"ORDER": {}, "CHAOS": {}}
        for unit in self.units:
            try:
                self.units_count[unit.team][unit.name] += 1
            except:
                self.units_count[unit.team][unit.name] = 1

    async def update_player_location(self):
        self_member = self.members.get(self.player.info.championName)
        await self.player.update_location(self_member)

    async def update_member_location(self, name: str, match: Match, zone: str):
        member = self.members.get(name)
        member.x = match.x
        member.y = match.y
        member.zone = zone

    async def update_current_action(self, action: str):
        self.current_action = action

    async def create_members(self, all_players_data: dict):
        for player in all_players_data:
            await self.create_member(player)

    async def create_member(self, player: dict):
        champion_name = player.get("rawChampionName").rsplit("_")[-1]
        self.members[champion_name] = TeamMember(
            summonerName=player.get("summonerName"),
            championId=CHAMPIONS.get(champion_name.lower()),
            championName=champion_name,
            team=player.get("team"),
            level=player.get("level"),
            position=player.get("position"),
            isPlayerTeam=bool(player.get("team") == self.player.info.team),
            isSelf=bool(player.get("summonerName") == self.player.info.name),
            isBot=cast_to_bool(player.get("isBot")),
            isDead=cast_to_bool(player.get("isDead")),
        )
