import asyncio
from typing import List

from ..common import (
    CHAMPIONS,
    Match,
    TeamMember,
    cast_to_bool,
    merge_dicts,
    find_closest_zone,
    debug_coro,
)
from .game_connector import GameConnector
from .game_flow import GameFlow
from .game_units import GameUnits
from .player import Player

from ..logger import get_logger

logger = get_logger("LPBv2.Game")


class Game:
    def __init__(self, *args, **kwargs):
        self.player = Player()
        self.members = dict()
        self.game_units = GameUnits()
        self.game_flow = GameFlow()
        self.game_connector = GameConnector()
        loop = asyncio.get_event_loop()

        loop.create_task(self.update())

    #@debug_coro
    async def update(self):
        while True:
            try:
                data = await self.game_connector.request("/liveclientdata/allgamedata")
                await self.game_flow.update(
                    events_data=data.get("events").get("Events"),
                    game_data=data.get("gameData"),
                )
                await self.update_player(
                    active_player_data=data.get("activePlayer"),
                    all_players_data=data.get("allPlayers"),
                )
                if not self.members:
                    await self.create_members(data.get("allPlayers"))
                await self.game_flow.update_is_ingame(True)
                await asyncio.sleep(1)
            except:
                await self.game_flow.update_is_ingame(False)

    #@debug_coro
    async def update_player(self, **kwargs):
        update_data = await self.get_merged_player_data(**kwargs)
        await self.player.update(update_data)

    #@debug_coro
    async def get_merged_player_data(self, **kwargs):
        active_player_data = kwargs.pop("active_player_data")
        all_players_data = kwargs.pop("all_players_data")
        for player_data in all_players_data:
            if player_data.get("summonerName") == active_player_data.get(
                "summonerName"
            ):
                return merge_dicts(player_data, active_player_data)

    #@debug_coro
    async def update_player_location(self):
        self_member = self.members.get(self.player.info.championName)
        if self_member:
            await self.player.update_location(self_member)

    #@debug_coro
    async def update_current_action(self, action: str):
        await self.game_flow.update_current_action(action)

    #@debug_coro
    async def clear_members(self):
        self.members = dict()

    #@debug_coro
    async def create_members(self, all_players_data: dict):
        for player in all_players_data:
            await self.create_member(player)

    #@debug_coro
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

    #@debug_coro
    async def get_member_names(self):
        return self.members.keys()

    #@debug_coro
    async def update_members(self, matches: List[Match]):
        for match in matches:
            member = self.members.get(match.name)
            member.x = match.x
            member.y = match.y
            zone = find_closest_zone(match.x, match.y)
            member.zone = zone

    #@debug_coro
    async def update_units(self, matches: List[Match]):
        await self.game_units.update(matches)
