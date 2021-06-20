import asyncio
from os import system
from typing import List

from ..common.champions import CHAMPIONS
from ..common.loop import LoopInNewThread
from ..common.models import Match, TeamMember
from ..common.utils import cast_to_bool
from ..logger import Colors, get_logger
from .game_connector import GameConnector
from .game_flow import GameFlow
from .player import Player

logger = get_logger("LPBv2.GameWatcher")


class GameWatcher:
    def __init__(self):
        self.loop = LoopInNewThread()
        self.player = Player()
        self.members = dict()
        self.units = list()
        self.units_count = dict()
        self.game_flow = GameFlow()
        self.game_connector = GameConnector()
        self.is_ingame = False
        self.FPS = float()
        self.current_action: str = str()
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

    async def print_info(self):
        system("clear")
        await self.print_fps()
        await self.print_player_team()
        await self.print_player_dead()
        await self.print_player_cs()
        await self.print_player_gold()
        await self.print_player_inventory()
        await self.print_players_position()
        await self.print_units_on_screen("CHAOS")
        await self.print_units_on_screen("ORDER")
        await self.print_current_action()

    async def print_fps(self):
        logger.info(f"Capture FPS: {Colors.green}{self.FPS}{Colors.reset}")
        logger.info(
            f"{Colors.cyan}{self.player.info.name}{Colors.reset} playing {Colors.cyan}{self.player.info.championName}{Colors.reset} ({Colors.green}{self.player.info.level}{Colors.reset})"
        )

    async def print_player_team(self):
        if self.player.info.team == "ORDER":
            logger.info(f"Team {Colors.cyan}{self.player.info.team}{Colors.reset}")
        else:
            logger.info(f"Team {Colors.red}{self.player.info.team}{Colors.reset}")

    async def print_player_dead(self):
        if self.player.info.isDead:
            logger.error(
                f"Player is dead, respawn in {Colors.red}{round(self.player.info.respawnTimer,2)}{Colors.reset} s"
            )
        else:
            logger.info(
                f"Player has {Colors.green}{self.player.stats.currentHealth}{Colors.reset} HP and {Colors.red}{int(self.player.stats.attackDamage)}{Colors.reset} AD"
            )

    async def print_player_cs(self):
        logger.info(
            f"Current CS is {Colors.green}{self.player.score.creepScore}{Colors.reset} ({Colors.dark_grey}{round(self.player.score.creepScore / ((self.game_flow.time) / 60))} CS/min){Colors.reset}"
        )

    async def print_player_gold(self):
        logger.info(
            f"Current gold is {Colors.yellow}{int(self.player.info.currentGold)}{Colors.reset} and player has {Colors.yellow}{len(self.player.inventory)}{Colors.reset} items"
        )

    async def print_player_inventory(self):
        for item in self.player.inventory:
            logger.warning(
                f"{Colors.yellow}{item.displayName}{Colors.reset} in slot {Colors.cyan}{item.slot}{Colors.reset}"
            )

    async def print_players_position(self):
        for member in self.members.values():
            if not member.zone:
                continue
            if member.team == "ORDER":
                champion_name = f"{Colors.cyan}{member.championName}{Colors.reset}"
            else:
                champion_name = f"{Colors.red}{member.championName}{Colors.reset}"
            if member.isSelf:
                champion_name = f"{Colors.green}{member.championName}{Colors.reset}"
            if member.zone.team == "ORDER":
                zone = f"{Colors.cyan}{member.zone.name}{Colors.reset}"
            elif member.zone.team == "CHAOS":
                zone = f"{Colors.red}{member.zone.name}{Colors.reset}"
            else:
                zone = f"{Colors.yellow}{member.zone.name}{Colors.reset}"
            logger.info(f"{champion_name} last seen zone is {zone}")

    async def print_units_on_screen(self, team: str):
        color = {"ORDER": Colors.cyan, "CHAOS": Colors.red}
        logger.info(
            f"{color[team]}{team}: {self.units_count.get(team).get('minion')} minions, {self.units_count.get(team).get('champion')} champions, {self.units_count.get(team).get('building')} buildings{Colors.reset}"
        )

    async def print_current_action(self):
        logger.info(f"Current action: {self.current_action}")
