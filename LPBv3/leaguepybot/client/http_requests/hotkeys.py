import json
import os
from contextlib import suppress
from typing import Any

from leaguepybot.client.connection.http_client import HttpClient
from leaguepybot.common.logger import get_logger
from leaguepybot.common.models import Runnable
from leaguepybot.common.utils import remove_non_alphanumeric

logger = get_logger("LPBv3.Hotkeys")


class Hotkeys(Runnable):
    def __init__(self, http_client: HttpClient):
        self._http_client = http_client

        self.hotkeys: dict = {}
        self.item_slot_1: str = "1"
        self.item_slot_2: str = "2"
        self.item_slot_3: str = "3"
        self.item_slot_4: str = "4"
        self.item_slot_5: str = "5"
        self.item_slot_6: str = "6"
        self.spell_1: str = "d"
        self.spell_2: str = "f"
        self.recall: str = "b"
        self.ward: str = "4"
        self.shop: str = "p"
        self.search_shop: str = "Ctrll"
        self.first_ability: str = "q"
        self.second_ability: str = "w"
        self.third_ability: str = "e"
        self.ultimate_ability: str = "r"
        self.attack_move: str = "a"
        self.camera_lock: str = "y"
        self.champion_only: str = "`"

    async def run(self) -> None:
        await self.backup_hotkeys()
        await self.patch_custom_hotkeys()
        await self.load_hotkeys()
        await self.restore_hotkeys()

    async def backup_hotkeys(self) -> None:
        hotkeys: dict[str, Any] = (await self.fetch_hotkeys()).data
        with open("backup.json", "w") as f:
            json.dump(hotkeys, f)
        logger.debug("Hotkeys backed up to backup.json")

    async def restore_hotkeys(self) -> None:
        with open("backup.json", encoding="utf-8") as f:
            hotkeys = json.load(f)
        await self.patch_hotkeys(hotkeys)
        logger.debug("Hotkeys restored from backup.json")

    async def load_hotkey(self, category, key, hotkey, default):
        cleaned = remove_non_alphanumeric(hotkey)
        if not cleaned or cleaned.lower() == "unbound":
            payload = {category: {key: f"[{default}]"}}
            await self.patch_hotkeys(payload=payload)
            return default
        return cleaned

    async def fetch_hotkeys(self) -> dict[str, Any]:
        return await self._http_client.request(
            method="GET", endpoint="/lol-game-settings/v1/input-settings"
        )

    async def load_hotkeys(self):
        response = await self._http_client.request(
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
            default="Ctrll",
        )
        self.first_ability = await self.load_hotkey(
            key="evtCastSpell1",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtCastSpell1"),
            default="q",
        )
        self.second_ability = await self.load_hotkey(
            key="evtCastSpell2",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtCastSpell2"),
            default="w",
        )
        self.third_ability = await self.load_hotkey(
            key="evtCastSpell3",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtCastSpell3"),
            default="e",
        )
        self.ultimate_ability = await self.load_hotkey(
            key="evtCastSpell4",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtCastSpell4"),
            default="r",
        )
        self.attack_move = await self.load_hotkey(
            key="evtPlayerAttackMove",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtPlayerAttackMove"),
            default="a",
        )
        self.camera_lock = await self.load_hotkey(
            key="evtCameraLockToggle",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtCameraLockToggle"),
            default="y",
        )
        self.champion_only = await self.load_hotkey(
            key="evtChampionOnly",
            category="GameEvents",
            hotkey=response.data.get("GameEvents").get("evtChampionOnly"),
            default="`",
        )
        logger.debug("Loaded hotkeys")

    async def patch_hotkeys(self, payload):
        return await self._http_client.request(
            method="PATCH",
            endpoint="/lol-game-settings/v1/input-settings",
            payload=payload,
        )

    async def patch_custom_hotkeys(self):
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
        await self.patch_hotkeys(hotkeys_settings)
        logger.debug("Patched hotkeys settings")

    async def async_stop(self) -> None:
        await self.restore_hotkeys()
        with suppress(FileNotFoundError):
            os.remove("backup.json")
            logger.debug("backup.json deleted")
