from ..logger import Colors, get_logger
import asyncio
from ..common import debug_coro, cls

logger = get_logger("LPBv2.Console")


class Console:
    def __init__(self, bot):
        self.bot = bot
        self.game = bot.game
        loop = asyncio.get_event_loop()
        loop.create_task(self.print_loop())

    @debug_coro
    async def print_loop(self):
        while True:
            await asyncio.sleep(1)
            if self.game.game_flow.is_ingame:
                await self.print_info()

    @debug_coro
    async def print_info(self):
        cls()
        await self.print_system_info()
        await self.print_player_info()
        await self.print_player_team()
        await self.print_player_dead()
        await self.print_player_cs()
        await self.print_player_gold()
        await self.print_player_inventory()
        await self.print_players_position()
        await self.print_ally_units_on_screen()
        await self.print_enemy_units_on_screen()
        await self.print_current_action()

    @debug_coro
    async def print_system_info(self):
        logger.info(
            f"Capture FPS: {Colors.yellow}{self.bot.FPS}{Colors.reset} - Memory: {Colors.yellow}{self.bot.mem}{Colors.reset} - CPU: {Colors.yellow}{self.bot.cpu}{Colors.reset} - Game Time: {Colors.yellow}{round(self.game.game_flow.time, 2)}{Colors.reset}"
        )

    @debug_coro
    async def print_player_info(self):
        logger.info(
            f"{Colors.cyan}{self.game.player.info.name}{Colors.reset} playing {Colors.cyan}{self.game.player.info.championName}{Colors.reset} ({Colors.green}{self.game.player.info.level}{Colors.reset})"
        )

    @debug_coro
    async def print_player_team(self):
        if self.game.player.info.team == "ORDER":
            logger.info(f"Team {Colors.cyan}{self.game.player.info.team}{Colors.reset}")
        else:
            logger.info(f"Team {Colors.red}{self.game.player.info.team}{Colors.reset}")

    @debug_coro
    async def print_player_dead(self):
        if self.game.player.info.isDead:
            logger.error(
                f"Player is dead, respawn in {Colors.red}{round(self.game.player.info.respawnTimer,2)}{Colors.reset} s"
            )
        else:
            logger.info(
                f"Player has {Colors.green}{round(self.game.player.stats.currentHealth, 0)}{Colors.reset} HP and {Colors.red}{int(self.game.player.stats.attackDamage)}{Colors.reset} AD"
            )

    @debug_coro
    async def print_player_cs(self):
        logger.info(
            f"Current CS is {Colors.green}{self.game.player.score.creepScore}{Colors.reset} ({Colors.dark_grey}{round(self.game.player.score.creepScore / ((self.game.game_flow.time) / 60))} CS/min){Colors.reset}"
        )

    @debug_coro
    async def print_player_gold(self):
        logger.info(
            f"Current gold is {Colors.yellow}{int(self.game.player.info.currentGold)}{Colors.reset} and player has {Colors.yellow}{len(self.game.player.inventory)}{Colors.reset} items"
        )

    @debug_coro
    async def print_player_inventory(self):
        for item in self.game.player.inventory:
            logger.info(
                f"Item {Colors.yellow}{item.displayName} ({item.itemID}){Colors.reset} in slot {Colors.cyan}{item.slot}{Colors.reset} price = {Colors.green}{item.price}{Colors.reset}, consumable = {Colors.cyan}{item.consumable}{Colors.reset}"
            )

    @debug_coro
    async def print_players_position(self):
        for member in self.game.members.values():
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

    @debug_coro
    async def print_ally_units_on_screen(self):
        units = self.game.game_units.units
        logger.info(
            f"{Colors.cyan}Order: {units.nb_ally_minions} minions, {units.nb_ally_champions} champions, {units.nb_ally_buildings} buildings{Colors.reset}"
        )

    @debug_coro
    async def print_enemy_units_on_screen(self):
        units = self.game.game_units.units
        logger.info(
            f"{Colors.red}Chaos: {units.nb_enemy_minions} minions, {units.nb_enemy_champions} champions, {units.nb_enemy_buildings} buildings{Colors.reset}"
        )

    @debug_coro
    async def print_current_action(self):
        logger.info(f"Current action: {self.game.game_flow.current_action}")
