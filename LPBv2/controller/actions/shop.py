from . import Action


class Shop(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items: dict() = None
        self.version_items: str() = None

    async def toggle_shop(self):
        self.keyboard.input_key(self.hotkeys.shop)

    async def search_item(self):
        self.keyboard.input_key(self.hotkeys.search_shop)

    async def buy_item(self, item_name: str):
        await self.search_item()
        self.keyboard.input_word(item_name)
        self.keyboard.esc()
        self.keyboard.enter()
