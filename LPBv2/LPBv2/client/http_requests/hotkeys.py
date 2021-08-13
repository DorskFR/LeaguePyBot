from typing import Optional
import re
import asyncio
from ...common import remove_non_alphanumeric, debug_coro
from .http_request import HTTPRequest
from ...logger import get_logger
from json import dumps

logger = get_logger("LPBv2.Hotkeys")


class Hotkeys(HTTPRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hotkeys: Optional[dict] = dict()
        self.item_slot_1: Optional[str] = "1"
        self.item_slot_2: Optional[str] = "2"
        self.item_slot_3: Optional[str] = "3"
        self.item_slot_4: Optional[str] = "4"
        self.item_slot_5: Optional[str] = "5"
        self.item_slot_6: Optional[str] = "6"
        self.spell_1: Optional[str] = "d"
        self.spell_2: Optional[str] = "f"
        self.recall: Optional[str] = "b"
        self.ward: Optional[str] = "4"
        self.shop: Optional[str] = "p"
        self.search_shop: Optional[str] = "l"
        self.first_ability: Optional[str] = "q"
        self.second_ability: Optional[str] = "w"
        self.third_ability: Optional[str] = "e"
        self.ultimate_ability: Optional[str] = "r"
        self.attack_move: Optional[str] = "a"
        self.camera_lock: Optional[str] = "y"
        self.champion_only: Optional[str] = "`"
        loop = asyncio.get_event_loop()
        loop.create_task(self.patch_hotkeys())
        loop.create_task(self.load_hotkeys())

    @debug_coro
    async def load_hotkey(self, category, key, hotkey, default):
        cleaned = remove_non_alphanumeric(hotkey)
        if cleaned.lower() == "unbound" or cleaned is None:
            payload = {category: {key: f"[{default}]"}}
            logger.warning(payload)
            await self.patch_hotkey(payload={category: {key: f"[{default}]"}})
            return default
        return cleaned

    @debug_coro
    async def load_hotkeys(self):
        response = await self.request(
            method="GET", endpoint="/lol-game-settings/v1/input-settings"
        )
        self.item_slot_1 = await self.load_hotkey(
            key="evtUseItem1",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtUseItem1"),
            default="z",
        )
        self.item_slot_2 = await self.load_hotkey(
            key="evtUseItem2",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtUseItem2"),
            default="x",
        )
        self.item_slot_3 = await self.load_hotkey(
            key="evtUseItem3",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtUseItem3"),
            default="c",
        )
        self.item_slot_4 = await self.load_hotkey(
            key="evtUseItem4",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtUseItem4"),
            default="v",
        )
        self.item_slot_5 = await self.load_hotkey(
            key="evtUseItem5",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtUseItem5"),
            default="n",
        )
        self.item_slot_6 = await self.load_hotkey(
            key="evtUseItem6",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtUseItem6"),
            default="m",
        )
        self.spell_1 = await self.load_hotkey(
            key="evtCastAvatarSpell1",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtCastAvatarSpell1"),
            default="d",
        )
        self.spell_2 = await self.load_hotkey(
            key="evtCastAvatarSpell2",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtCastAvatarSpell2"),
            default="f",
        )
        self.recall = await self.load_hotkey(
            key="evtUseItem7",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtUseItem7"),
            default="b",
        )
        self.ward = await self.load_hotkey(
            key="evtUseVisionItem",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtUseVisionItem"),
            default="4",
        )
        self.shop = await self.load_hotkey(
            key="evtOpenShop",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtOpenShop"),
            default="p",
        )
        self.search_shop = await self.load_hotkey(
            key="evtShopFocusSearch",
            category="ShopEvents",
            hotkey=response.data.get("ShopEvents").get("evtShopFocusSearch"),
            default="l",
        )
        self.search_shop = await self.load_hotkey(
            key="evtCastSpell1",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtCastSpell1"),
            default="q",
        )
        self.search_shop = await self.load_hotkey(
            key="evtCastSpell2",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtCastSpell2"),
            default="w",
        )
        self.search_shop = await self.load_hotkey(
            key="evtCastSpell3",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtCastSpell3"),
            default="e",
        )
        self.search_shop = await self.load_hotkey(
            key="evtCastSpell4",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtCastSpell4"),
            default="r",
        )
        self.search_shop = await self.load_hotkey(
            key="evtPlayerAttackMove",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtPlayerAttackMove"),
            default="a",
        )
        self.search_shop = await self.load_hotkey(
            key="evtCameraLockToggle",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtCameraLockToggle"),
            default="y",
        )
        self.search_shop = await self.load_hotkey(
            key="evtChampionOnly",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtChampionOnly"),
            default="`",
        )
        logger.info("Loaded hotkeys")

    @debug_coro
    async def patch_hotkey(self, payload):
        return await self.request(
            method="PATCH",
            endpoint="/lol-game-settings/v1/input-settings",
            payload=payload,
        )

    @debug_coro
    async def patch_hotkeys(self):
        hotkeys_settings = {
            "GameEvents": {
                "evtUseItem1": "[z]",
                "evtUseItem2": "[x]",
                "evtUseItem3": "[c]",
                "evtUseItem4": "[v]",
                "evtUseItem5": "[n]",
                "evtUseItem6": "[m]",
            },
            "Quickbinds": {
                "evtCastAvatarSpell1smart": True,
                "evtCastAvatarSpell2smart": True,
                "evtCastSpell1smart": True,
                "evtCastSpell2smart": True,
                "evtCastSpell3smart": True,
                "evtCastSpell4smart": True,
                "evtUseItem1smart": True,
                "evtUseItem2smart": True,
                "evtUseItem3smart": True,
                "evtUseItem4smart": True,
                "evtUseItem5smart": True,
                "evtUseItem6smart": True,
                "evtUseVisionItemsmart": True,
            },
        }
        response = await self.patch_hotkey(hotkeys_settings)
        if response:
            logger.info("Patched hotkeys settings")
