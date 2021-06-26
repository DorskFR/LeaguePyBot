from . import Action


class Shop(Action):
    def __init__(self):
        super().__init__()

    async def toggle_shop(self):
        await self.keyboard.input_key(self.hotkeys.shop)

    async def buy_item(self, x: int, y: int):
        pass
