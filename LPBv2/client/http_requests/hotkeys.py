from typing import Optional
import re
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

    #@debug_coro
    async def load_hotkeys(self):
        response = await self.request(
            method="GET", endpoint="/lol-game-settings/v1/input-settings"
        )

        self.item_slot_1 = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtUseItem1") or "z"
        )
        self.item_slot_2 = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtUseItem2") or "x"
        )
        self.item_slot_3 = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtUseItem3") or "c"
        )
        self.item_slot_4 = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtUseItem4") or "v"
        )
        self.item_slot_5 = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtUseItem5") or "n"
        )
        self.item_slot_6 = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtUseItem6") or "m"
        )
        self.spell_1 = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtCastAvatarSpell1") or "d"
        )
        self.spell_2 = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtCastAvatarSpell2") or "f"
        )
        self.recall = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtUseItem7") or "b"
        )
        self.ward = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtUseVisionItem") or "4"
        )
        self.shop = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtOpenShop") or "p"
        )
        self.search_shop = remove_non_alphanumeric(
            response.data.get("ShopEvents").get("evtShopFocusSearch") or "l"
        )
        self.first_ability = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtCastSpell1") or "q"
        )
        self.second_ability = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtCastSpell2") or "w"
        )
        self.third_ability = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtCastSpell3") or "e"
        )
        self.ultimate_ability = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtCastSpell4") or "r"
        )
        self.attack_move = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtPlayerAttackMove") or "a"
        )
        self.camera_lock = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtCameraLockToggle") or "y"
        )
        self.champion_only = remove_non_alphanumeric(
            response.data.get("GameEvents").get("evtChampionOnly") or "`"
        )
        logger.info("Loaded hotkeys")

    #@debug_coro
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
        response = await self.request(
            method="PATCH",
            endpoint="/lol-game-settings/v1/input-settings",
            payload=hotkeys_settings,
        )
        if response:
            logger.info("Patched hotkeys settings")
