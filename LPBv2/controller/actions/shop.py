from . import Action
from ...common import debug_coro
from asyncio import sleep
from ...logger import get_logger

logger = get_logger("LPBv2.Shop")

class Shop(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build = kwargs.get("build")
        self.items: dict() = None
        self.version_items: str() = None

    @debug_coro
    async def toggle_shop(self):
        self.keyboard.input_key(self.hotkeys.shop)

    @debug_coro
    async def search_item(self):
        self.keyboard.input_key(self.hotkeys.search_shop)

    @debug_coro
    async def buy_item(self, item_name: str):
        await self.search_item()
        self.keyboard.input_word(item_name)
        self.keyboard.esc()
        self.keyboard.enter()

    @debug_coro
    async def recursive_buy(self, shop_list):
        player_items = [str(item.itemID) for item in self.game.player.inventory]
        composite = self.build.all_items.get(shop_list[0]).get("from")
        price = self.build.all_items.get(shop_list[0]).get("gold").get("total")
        name = self.build.all_items.get(shop_list[0]).get("name")

        logger.info(f"Trying to buy {shop_list[0]}")

        if composite:
            for component in composite:
                if component in player_items:
                    price -= (
                        self.build.all_items.get(component).get("gold").get("total")
                    )

        if (
            not shop_list[0] in player_items
            and self.game.player.info.currentGold >= price
            and len(player_items) < 7
        ):
            await self.buy_item(name)

        elif (
            not shop_list[0] in player_items
            and (self.game.player.info.currentGold < price or len(player_items) >= 7)
            and composite
        ):
            await self.recursive_buy(composite)

        if len(shop_list) <= 1 or (
            (self.game.player.info.currentGold < price or len(player_items) >= 7)
            and not composite
        ):
            return

        await self.recursive_buy(shop_list[1:])

    @debug_coro
    async def buy_build(self, build):
        await self.game.game_flow.update_current_action("Buying from shop")
        await self.toggle_shop()
        await sleep(1)
        await self.recursive_buy(build)
        await sleep(1)
        await self.toggle_shop()
