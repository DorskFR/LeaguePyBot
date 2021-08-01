from typing import Optional
import re


class Hotkeys:
    def __init__(self, *args, **kwargs):
        self.installation_path: Optional[str] = kwargs.get("installation_path")
        self.hotkeys: Optional[dict] = dict()
        if self.installation_path:
            self.load_hotkeys_from_file()
        self.item_slot_1: Optional[str] = self.hotkeys.get("evtUseItem1") or "1"
        self.item_slot_2: Optional[str] = self.hotkeys.get("evtUseItem2") or "2"
        self.item_slot_3: Optional[str] = self.hotkeys.get("evtUseItem3") or "3"
        self.item_slot_4: Optional[str] = self.hotkeys.get("evtUseItem4") or "4"
        self.item_slot_5: Optional[str] = self.hotkeys.get("evtUseItem5") or "5"
        self.item_slot_6: Optional[str] = self.hotkeys.get("evtUseItem6") or "6"
        self.spell_1: Optional[str] = self.hotkeys.get("evtCastAvatarSpell1") or "d"
        self.spell_2: Optional[str] = self.hotkeys.get("evtCastAvatarSpell2") or "f"
        self.recall: Optional[str] = self.hotkeys.get("evtUseItem7") or "b"
        self.ward: Optional[str] = self.hotkeys.get("evtUseVisionItem") or "4"
        self.shop: Optional[str] = self.hotkeys.get("evtOpenShop") or "p"
        self.search_shop: Optional[str] = self.hotkeys.get("evtShopFocusSearch") or "l"
        self.first_ability: Optional[str] = self.hotkeys.get("evtCastSpell1") or "q"
        self.second_ability: Optional[str] = self.hotkeys.get("evtCastSpell2") or "w"
        self.third_ability: Optional[str] = self.hotkeys.get("evtCastSpell3") or "e"
        self.ultimate_ability: Optional[str] = self.hotkeys.get("evtCastSpell4") or "r"
        self.attack_move: Optional[str] = self.hotkeys.get("evtPlayerAttackMove") or "a"
        self.camera_lock: Optional[str] = self.hotkeys.get("evtCameraLockToggle") or "y"
        self.camera_snap: Optional[str] = self.hotkeys.get("evtCameraSnap") or "space"

    def load_hotkeys_from_file(self):
        with open(self.installation_path + "/Config/input.ini") as hkfile:
            for row in hkfile:
                if not "=" in row:
                    continue
                row_array = row.split("=")
                if len(row_array) < 2:
                    continue

                self.hotkeys[row_array[0]] = re.sub(
                    r"\W+", "", row_array[1].split(",")[0].strip()
                )
