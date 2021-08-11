from .http_request import HTTPRequest
from ...common import (
    CHAMPIONS,
    cast_to_bool,
    WebSocketEventResponse,
    get_key_from_value,
    RolePreference,
    debug_coro,
)
from ...logger import get_logger, Colors
from typing import Dict, List, Optional

logger = get_logger("LPBv2.ChampSelect")


class ChampSelect(HTTPRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = RolePreference()
        self.picks: Dict[str, List[int]] = dict()
        self.is_picking: bool = False
        self.bans: Dict[str, List[int]] = dict()
        self.is_banning: bool = False
        self.player_cell_id: Optional[int]
        self.player_id: Optional[int]
        self.champion_id: Optional[int] = 0

    @debug_coro
    async def update(self, event: WebSocketEventResponse):
        phase = event.data.get("timer").get("phase")
        await self.get_player_cell_id(event)
        await self.get_role(event)
        if phase == "PLANNING":
            await self.intent()
        if phase == "BAN_PICK":
            if await self.block_condition(event, "pick") and not self.is_picking:
                await self.pick_champion()
            if await self.block_condition(event, "ban") and not self.is_banning:
                await self.ban_champion()

    @debug_coro
    async def set_role_preference(self, **kwargs):
        self.role.first = kwargs.get("first")
        self.role.second = kwargs.get("second")
        logger.info(
            f"First role: {Colors.yellow}{self.role.first}{Colors.reset}, Second role: {Colors.yellow}{self.role.second}{Colors.reset}"
        )

    @debug_coro
    async def set_picks_per_role(self, **kwargs):
        picks = kwargs.get("picks") or list()
        role = kwargs.get("role") or "FILL"
        self.picks[role] = [CHAMPIONS.get(pick.lower()) for pick in picks]
        logger.info(
            f"Set the following picks: {Colors.green}{picks}{Colors.reset} for the following role: {Colors.cyan}{role}{Colors.reset}"
        )

    @debug_coro
    async def set_bans_per_role(self, **kwargs):
        bans = kwargs.get("bans")
        role = kwargs.get("role")
        self.bans[role] = [CHAMPIONS.get(ban.lower()) for ban in bans]
        logger.info(
            f"Set the following bans: {Colors.red}{bans}{Colors.reset} for the following role: {Colors.cyan}{role}{Colors.reset}"
        )

    @debug_coro
    async def intent(self):
        pass

    @debug_coro
    async def get_player_cell_id(self, event: WebSocketEventResponse):
        self.player_cell_id = event.data.get("localPlayerCellId")

    @debug_coro
    async def get_role(self, event: WebSocketEventResponse):
        for block in event.data.get("myTeam"):
            if block.get("cellId") == self.player_cell_id:
                try:
                    self.role.assigned = block.get("assignedPosition").upper()
                except:
                    self.role.assigned = "FILL"

    @debug_coro
    async def block_condition(self, event: WebSocketEventResponse, block_type: str):
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

    @debug_coro
    async def pick_champion(self):
        self.is_picking = True
        picks = await self.get_champions_to_pick()
        for champion_id in picks:
            if await self.pick(champion_id):
                self.champion_id = champion_id
                break
        self.is_picking = False

    @debug_coro
    async def ban_champion(self):
        self.is_banning = True
        bans = await self.get_champions_to_ban()
        for champion_id in bans:
            if await self.ban(champion_id):
                break
        self.is_banning = False

    @debug_coro
    async def get_champions_to_pick(self, **kwargs):
        role = kwargs.get("role") or self.role.assigned
        if role and role != "FILL":
            return self.picks.get(role)
        return [pick for picks in self.picks.values() for pick in picks]

    @debug_coro
    async def get_champions_to_ban(self, **kwargs):
        role = kwargs.get("role") or self.role.assigned
        if role and role != "FILL":
            return self.bans.get(role)
        return [ban for bans in self.bans.values() for ban in bans]

    @debug_coro
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
            logger.warning(
                f"Picked: {Colors.cyan}{get_key_from_value(CHAMPIONS, champion_id).capitalize()}{Colors.reset}"
            )
            return True

    @debug_coro
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
                f"Banned champion champion_id: {Colors.red}{champion_id}{Colors.reset}, player_cell_id: {Colors.dark_grey}{self.player_cell_id}{Colors.reset}, player_id: {Colors.dark_grey}{self.player_id}{Colors.reset}"
            )
            return True
