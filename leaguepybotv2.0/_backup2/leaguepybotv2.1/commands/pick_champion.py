from .client_call import ClientCall
from typing import Optional


class PickChampion(ClientCall):
    def __init__(self):
        super().__init()
        self.player_cell_id: Optional[int]
        self.player_id: Optional[int]
        self.champion_id: Optional[int]

    async def condition(self):
        self.player_cell_id = self.event.data.get("localPlayerCellId")
        for array in self.event.data.get("actions"):
            for block in array:
                if block.get("actorCellId") == self.player_cell_id:
                    self.player_id = block.get("id")
                    if (
                        self.event.data.get("timer").get("phase") == "BAN_PICK"
                        and block.get("type") == "pick"
                        and cast_to_bool(block.get("completed")) != True
                        and cast_to_bool(block.get("isInProgress")) == True
                    ):
                        return True

    async def build(self):
        self.method = "PATCH"
        self.endpoint = f"/lol-champ-select/v1/session/actions/{self.player_id}"
        self.payload = {
            "actorCellId": self.player_cell_id,
            "championId": self.champion_id,
            "completed": True,
            "isAllyAction": True,
            "type": "pick",
        }

    async def action(self, response: WebsocketEventResponse):
        print("Picked champion")
