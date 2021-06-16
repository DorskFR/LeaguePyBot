import asyncio

from ..logger import get_logger, Colors
from .game_connector import GameConnector
from .game_flow import GameFlow
from ..common.loop import Loop
from .player import Player
from os import system

logger = get_logger("LPBv2.GameWatcher")


class GameWatcher:
    def __init__(self):
        self.loop = Loop()
        self.player = Player()
        self.game_flow = GameFlow()
        self.game_connector = GameConnector()
        self.is_ingame = False
        self.loop.submit_async(self.update())

    async def update(self):
        while True:
            try:
                self.is_ingame = True
                data = await self.game_connector.request("/liveclientdata/allgamedata")
                self.game_flow.update(
                    data.get("events").get("Events"), data.get("gameData")
                )
                self.player.update(data.get("activePlayer"), data.get("allPlayers"))
                self.log_info()
                await asyncio.sleep(1)
            except:
                self.is_ingame = False
                pass

    def log_info(self):
        system("clear")

        logger.debug(
            "======================================================================"
        )

        logger.info(
            f"{Colors.cyan}{self.player.info.name}{Colors.reset} playing {Colors.cyan}{self.player.info.championName}{Colors.reset} ({Colors.green}{self.player.info.level}{Colors.reset})"
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
                f"Player has {Colors.green}{self.player.championStats.currentHealth}{Colors.reset} HP and {Colors.red}{int(self.player.championStats.attackDamage)}{Colors.reset} AD"
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
        # logger.debug(self.player.__dict__)
        # logger.debug(self.game_flow.__dict__)
