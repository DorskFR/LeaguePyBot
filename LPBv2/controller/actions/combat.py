from . import Action
from ...common import safest_position, average_position, debug_coro
from asyncio import sleep
from ...logger import get_logger, Colors

logger = get_logger("LPBv2.Combat")


class Combat(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset_x = 50
        self.offset_y = 50

    @debug_coro
    async def cast_spell(self, key, x: int, y: int):
        self.mouse.set_position(x + self.offset_x, y + self.offset_y)
        self.keyboard.input_key(key)

    @debug_coro
    async def level_up_abilities(self):
        if self.game.player.info.level in [1, 4, 5, 7, 9]:
            self.keyboard.input_key("Ctrl" + self.hotkeys.first_ability)
        elif self.game.player.info.level in [2, 14, 15, 17, 18]:
            self.keyboard.input_key("Ctrl" + self.hotkeys.second_ability)
        elif self.game.player.info.level in [3, 8, 10, 12, 13]:
            self.keyboard.input_key("Ctrl" + self.hotkeys.third_ability)
        else:
            self.keyboard.input_key("Ctrl" + self.hotkeys.ultimate_ability)

    @debug_coro
    async def cast_spells(self, x: int, y: int, ultimate=False):
        if ultimate:
            await self.cast_spell(self.hotkeys.ultimate_ability, x, y)
        await self.cast_spell(self.hotkeys.first_ability, x, y)
        await self.cast_spell(self.hotkeys.second_ability, x, y)
        await self.cast_spell(self.hotkeys.third_ability, x, y)

    @debug_coro
    async def attack(self, x: int, y: int):
        await self.attack_move(x + self.offset_x, y + self.offset_y)

    @debug_coro
    async def get_closest_enemy_position(self):
        minions = self.game.game_units.units.enemy_minions
        if minions:
            return safest_position(minions)

    @debug_coro
    async def get_average_enemy_position(self):
        minions = self.game.game_units.units.enemy_minions
        if minions:
            return average_position(minions)

    @debug_coro
    async def attack_minions(self):
        await self.game.game_flow.update_current_action("Attacking minions")
        pos = await self.get_closest_enemy_position()
        if pos:
            await self.attack(*pos)
        pos = await self.get_average_enemy_position()
        if await self.game.player.has_more_than_50_percent_mana() and pos:
            sleep(1)
            await self.cast_spells(*pos)

    @debug_coro
    async def get_closest_enemy_champion_position(self):
        champions = self.game.game_units.units.enemy_champions
        if champions:
            return safest_position(champions)

    @debug_coro
    async def attack_champion(self):
        await self.game.game_flow.update_current_action("Attacking champion")
        pos = await self.get_closest_enemy_champion_position()
        if pos:
            await self.attack(*pos)
            if await self.game.player.has_more_than_25_percent_mana() and pos:
                await self.cast_spells(*pos, ultimate=True)

    @debug_coro
    async def get_closest_enemy_building_position(self):
        buildings = self.game.game_units.units.enemy_buildings
        if buildings:
            return safest_position(buildings)

    @debug_coro
    async def attack_building(self):
        await self.game.game_flow.update_current_action("Attacking building")
        pos = await self.get_closest_enemy_building_position()
        pos_ally = await self.get_riskiest_ally_position()
        if pos and pos_ally:
            distance = ((pos[0] + self.offset_x) - (pos[1] + self.offset_y * 2)) - (
                pos_ally[0] - pos_ally[1]
            )
            logger.warning(f"Distance tower: {distance}")
            if distance < 300:
                await self.attack(*pos)
