from typing import Optional


class Hotkeys:
    def __init__(self):
        self.item_slot_1: Optional[str] = "1"
        self.item_slot_2: Optional[str] = "2"
        self.item_slot_3: Optional[str] = "3"
        self.item_slot_4: Optional[str] = "4"
        self.item_slot_5: Optional[str] = "5"
        self.item_slot_6: Optional[str] = "6"
        self.summoner_spell_1: Optional[str] = "d"
        self.summoner_spell_2: Optional[str] = "f"
        self.recall: Optional[str] = "b"
        self.shop: Optional[str] = "p"
        self.first_ability: Optional[str] = "q"
        self.second_ability: Optional[str] = "w"
        self.third_ability: Optional[str] = "e"
        self.ultimate_ability: Optional[str] = "r"
        self.attack_move: Optional[str] = "a"

    def load_hotkeys_from_file(self):
        pass
