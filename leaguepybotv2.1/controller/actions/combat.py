from . import Action


class Combat(Action):
    def __init__(self):
        super().init()

    async def attack_move(self, x: int, y: int):
        self.keyboard.press("a")
        self.mouse.set_position_and_left_click(x, y)
        self.keyboard.release("a")

    async def cast_ability(self, key, x: int, y: int):
        self.mouse.set_position(x, y)
        self.keyboard.input_key(key)

    async def cast_spells(self, x: int, y: int, r=False):
        await self.cast_spell("q", x, y)
        await self.cast_spell("e", x, y)
        await self.cast_spell("w", x, y)
        if r:
            await self.cast_spell("r", x, y)

    async def attack(self, x: int, y: int):
        await self.attack_move(x, y)

    async def attack_target(self, unit_type, localizer_function):
        pos = await localizer_function(unit_type)
        if pos:
            await self.attack_move(*pos)

    async def attack_building(self):
        pos = await self.get_closest_enemy_building_position()
        if pos:
            await self.attack(*pos)

    async def attack_champion(self):
        pos = await self.get_closest_enemy_champion_position()
        if pos:
            await self.attack(*pos)
            if await self.game.player.has_more_than_50_percent_mana() and pos:
                await self.cast_spells(*pos, r=True)

    async def attack_minions(self):
        pos = await self.get_closest_enemy_position()
        if pos:
            await self.attack(*pos)
        pos = await self.get_average_enemy_position()
        if await self.game.player.has_more_than_50_percent_mana() and pos:
            await self.cast_spells(*pos)
