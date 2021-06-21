from os import system
from ..logger import Colors, get_logger


logger = get_logger("LPBv2.Console")


class Console:
    def __init__(self):
        pass

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
