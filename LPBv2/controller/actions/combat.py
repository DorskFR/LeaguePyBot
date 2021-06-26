from . import Action


class Combat(Action):
    def __init__(self):
        super().__init__()

    async def attack_move(self, x: int, y: int):
        self.keyboard.press(self.hotkeys.attack_move)
        self.mouse.set_position_and_left_click(x, y)
        self.keyboard.release(self.hotkeys.attack_move)

    async def cast_spell(self, key, x: int, y: int):
        self.mouse.set_position(x, y)
        self.keyboard.input_key(key)

    async def cast_spells(self, x: int, y: int, ultimate=False):
        await self.cast_spell(self.hotkeys.first_ability, x, y)
        await self.cast_spell(self.hotkeys.second_ability, x, y)
        await self.cast_spell(self.hotkeys.third_ability, x, y)
        if ultimate:
            await self.cast_spell(self.hotkeys.ultimate_ability, x, y)

    async def attack(self, x: int, y: int):
        await self.attack_move(x, y)

    async def attack_target(self, unit_type, localizer_function):
        pos = await localizer_function(unit_type)
        if pos:
            await self.attack_move(*pos)
