import asyncio

from ..logger import get_logger, Colors
from .game_connector import GameConnector
from .game_flow import GameFlow
from ..common.loop import Loop
from .player import Player
from ..common.models import TeamMember
from os import system
from typing import List, Optional
from ..common.champions import CHAMPIONS
from ..common.utils import cast_to_bool

logger = get_logger("LPBv2.GameWatcher")


class GameWatcher:
    def __init__(self):
        self.loop = Loop()
        self.player = Player()
        self.members = dict()
        self.game_flow = GameFlow()
        self.game_connector = GameConnector()
        self.is_ingame = False
        self.loop.submit_async(self.update())
        self.FPS = float()

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
                await self.log_info()
                await asyncio.sleep(1)
            except:
                self.is_ingame = False
                if self.members:
                    self.members = dict()
                pass

    async def create_members(self, all_players_data):
        for player in all_players_data:
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

    async def log_info(self):
        system("clear")

        logger.info(f"Capture FPS: {Colors.green}{self.FPS}{Colors.reset}")
        logger.info(
            f"{Colors.cyan}{self.player.info.name}{Colors.reset} playing {Colors.cyan}{self.player.info.championName}{Colors.reset} ({Colors.green}{self.player.info.level}{Colors.reset})"
        )
        logger.info(
            f"Currently in location: {Colors.yellow}{self.player.location}{Colors.reset}"
        )

        if self.player.info.team == "ORDER":
            logger.info(f"Team {Colors.cyan}{self.player.info.team}{Colors.reset}")
        else:
            logger.info(f"Team {Colors.red}{self.player.info.team}{Colors.reset}")

        if self.player.info.isDead:
            logger.error(
                f"Player is dead, respawn in {Colors.red}{round(self.player.info.respawnTimer,2)}{Colors.reset} s"
            )
        else:
            logger.info(
                f"Player has {Colors.green}{self.player.stats.currentHealth}{Colors.reset} HP and {Colors.red}{int(self.player.stats.attackDamage)}{Colors.reset} AD"
            )

        logger.info(
            f"Current CS is {Colors.green}{self.player.score.creepScore}{Colors.reset} ({Colors.dark_grey}{round(self.player.score.creepScore / ((self.game_flow.time) / 60))} CS/min){Colors.reset}"
        )
        logger.info(
            f"Current gold is {Colors.yellow}{int(self.player.info.currentGold)}{Colors.reset} and player has {Colors.yellow}{len(self.player.inventory)}{Colors.reset} items"
        )
        for item in self.player.inventory:
            logger.warning(
                f"{Colors.yellow}{item.displayName}{Colors.reset} in slot {Colors.cyan}{item.slot}{Colors.reset}"
            )
        for member in self.members:
            logger.info(member.championName)
