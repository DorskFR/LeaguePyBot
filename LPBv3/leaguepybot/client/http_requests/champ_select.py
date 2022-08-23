from typing import Dict, List, Optional

from leaguepybot.client.http_requests.http_request import HTTPRequest
from leaguepybot.common.champions import CHAMPIONS
from leaguepybot.common.logger import get_logger
from leaguepybot.common.models import RolePreference, WebSocketEventResponse
from leaguepybot.common.utils import cast_to_bool, get_key_from_value

logger = get_logger("LPBv3.ChampSelect")


class ChampSelect(HTTPRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bans: Dict[str, List[int]] = {}
        self.champion_id: Optional[int] = 0
        self.is_banning: bool = False
        self.is_picking: bool = False
        self.pick_event: Optional[bool] = False
        self.picks: Dict[str, List[int]] = {}
        self.player_cell_id: Optional[int]
        self.player_id: Optional[int]
        self.role = RolePreference()

    async def update(self, event: WebSocketEventResponse):
        phase = event.data.get("timer").get("phase")
        self.get_player_cell_id(event)
        self.get_role(event)
        if phase == "PLANNING":
            self.intent()
        if phase == "BAN_PICK":
            if self.block_condition(event, "pick") and not self.is_picking:
                await self.pick_champion()
            if self.block_condition(event, "ban") and not self.is_banning:
                await self.ban_champion()

    def set_role_preference(self, **kwargs):
        self.role.first = kwargs.get("first")
        self.role.second = kwargs.get("second")
        logger.debug(f"First role: {self.role.first}, Second role: {self.role.second}")

    def set_picks_per_role(self, **kwargs):
        picks = kwargs.get("picks", [])
        role = kwargs.get("role", "FILL")
        self.picks[role] = [CHAMPIONS.get(pick.lower()) for pick in picks]
        logger.debug(f"Set the following picks: {picks} for the following role: {role}")

    def set_bans_per_role(self, **kwargs):
        bans = kwargs.get("bans")
        role = kwargs.get("role")
        self.bans[role] = [CHAMPIONS.get(ban.lower()) for ban in bans]
        logger.debug(f"Set the following bans: {bans} for the following role: {role}")

    def intent(self):
        pass

    def get_player_cell_id(self, event: WebSocketEventResponse):
        self.player_cell_id = event.data.get("localPlayerCellId")

    def get_role(self, event: WebSocketEventResponse):
        for block in event.data.get("myTeam"):
            if block.get("cellId") == self.player_cell_id:
                try:
                    self.role.assigned = block.get("assignedPosition").upper()
                except:
                    self.role.assigned = "FILL"

    def block_condition(self, event: WebSocketEventResponse, block_type: str):
        for array in event.data.get("actions"):
            for block in array:
                if (
                    block.get("actorCellId") == self.player_cell_id
                    and block.get("type") == block_type
                    and cast_to_bool(block.get("completed")) != True
                    and cast_to_bool(block.get("isInProgress")) == True
                ):
                    self.player_id = block.get("id")
                    return True

    async def pick_champion(self):
        self.is_picking = True
        picks = self.get_champions_to_pick()
        for champion_id in picks:
            if await self.pick(champion_id):
                self.champion_id = champion_id
                self.pick_event = True
                break
        self.is_picking = False

    async def ban_champion(self):
        self.is_banning = True
        bans = self.get_champions_to_ban()
        for champion_id in bans:
            if await self.ban(champion_id):
                break
        self.is_banning = False

    def get_champions_to_pick(self, **kwargs):
        role = kwargs.get("role") or self.role.assigned
        if role and role != "FILL":
            return self.picks.get(role)
        return [pick for picks in self.picks.values() for pick in picks]

    def get_champions_to_ban(self, **kwargs):
        role = kwargs.get("role") or self.role.assigned
        if role and role != "FILL":
            return self.bans.get(role)
        return [ban for bans in self.bans.values() for ban in bans]

    async def pick(self, champion_id):
        response = await self.request(
            method="PATCH",
            endpoint=f"/lol-champ-select/v1/session/actions/{self.player_id}",
            payload={
                "actorCellId": self.player_cell_id,
                "championId": champion_id,
                "completed": True,
                "isAllyAction": True,
                "type": "pick",
            },
        )
        if response:
            logger.debug(f"Picked: {get_key_from_value(CHAMPIONS, champion_id).capitalize()}")
            return True

    async def ban(self, champion_id):
        response = await self.request(
            method="PATCH",
            endpoint=f"/lol-champ-select/v1/session/actions/{self.player_id}",
            payload={
                "actorCellId": self.player_cell_id,
                "championId": champion_id,
                "completed": True,
                "type": "ban",
            },
        )
        if response:
            logger.warning(
                f"Banned champion champion_id: {champion_id}, player_cell_id: {self.player_cell_id}, player_id: {self.player_id}"
            )
            return True
