import random
from typing import Dict

from leaguepybot.client.connection.http_client import HttpClient
from leaguepybot.client.http_requests.summoner import Summoner
from leaguepybot.common.enums import Champion, Role
from leaguepybot.common.logger import get_logger
from leaguepybot.common.models import RolePreference, Runnable, WebSocketEventResponse
from leaguepybot.common.utils import cast_to_bool

logger = get_logger("LPBv3.ChampSelect")


class ChampSelect(Runnable):
    def __init__(self, http_client: HttpClient, summoner: Summoner):
        super().__init__()
        self._http_client = http_client

        self._summoner = summoner
        self._bans: Dict[Role, list[Champion]] = {}
        self._champion: Champion | None = None
        self._is_banning: bool = False
        self._is_picking: bool = False
        self._has_announced_role: bool = False
        self._pick_event: bool | None = False
        self._picks: Dict[Role, list[Champion]] = {}
        self._player_cell_id: int | None
        self._player_id: int | None
        self._chat_session_id: str = ""
        self._chat_id: str = "ecdbdacc-7556-538f-8e1b-1049bb10240a@jp1.pvp.net"
        self.role_preference = RolePreference()

    async def update(self, event: WebSocketEventResponse):
        phase = event.data.get("timer").get("phase")
        self.get_player_cell_id(event)
        self.set_role_assigned(event)
        # if phase == "PLANNING":
        #     await self.intent()
        if phase == "BAN_PICK":
            if self.block_condition(event, "pick") and not self._is_picking:
                await self.pick_champion()
            if self.block_condition(event, "ban") and not self._is_banning:
                await self.ban_champion()

    def set_role_preference(self, first: Role, second: Role) -> None:
        """
        Set the preferred roles for ranked / normal game with pick.
        """
        self.role_preference.first = first
        self.role_preference.second = second
        logger.debug(
            f"First role: {self.role_preference.first}, Second role: {self.role_preference.second}"
        )

    def set_picks_per_role(self, picks_per_role: dict[Role, list[Champion]]) -> None:
        """
        Define your picks per role and by order of preference.
        """
        for role, picks in picks_per_role.items():
            self._picks[role] = picks
            logger.debug(
                f"Set the following picks: {[p.name.capitalize() for p in picks]} for the following role: {role}"
            )

    def set_bans_per_role(self, bans_per_role: dict[Role, list[Champion]]) -> None:
        """
        Define your bans per role and by order of preference.
        """
        for role, bans in bans_per_role.items():
            self._bans[role] = bans
            logger.debug(
                f"Set the following bans: {[b.name.capitalize() for b in bans]} for the following role: {role}"
            )

    async def announce_role(self):
        if not self._chat_session_id or self._has_announced_role:
            return
        role = (
            self.role_preference.assigned
            if self.role_preference.assigned != Role.FILL
            else self.role_preference.first
        )
        for _ in range(3):
            await self._http_client.request(
                method="POST",
                endpoint=f"/lol-chat/v1/conversations/{self._chat_session_id}/messages",
                payload={
                    "body": role._name_.lower(),  # pylint: disable=protected-access
                    "fromId": self._chat_id,
                    "fromPid": self._chat_id,
                    "fromSummoner": self._summoner.info.summonerId,
                    "type": "groupchat",
                },
            )
            await self._sleep(0.3)
        self._has_announced_role = True

    def get_player_cell_id(self, event: WebSocketEventResponse):
        self._player_cell_id = event.data.get("localPlayerCellId")

    async def get_chat_session_id(self, event: WebSocketEventResponse):
        chat_session_id = event.uri.split("/lol-chat/v1/conversations/")[-1].split("/")[0]
        if "champ-select" in chat_session_id and chat_session_id != self._chat_session_id:
            logger.debug(f"New chat session id: {self._chat_session_id}")
            self._has_announced_role = False
            self._chat_session_id = chat_session_id
            await self.announce_role()

    def set_role_assigned(self, event: WebSocketEventResponse) -> None:
        """
        Set the role assigned based on what we got from the game as preferences are not always respected.
        """
        for block in event.data.get("myTeam"):
            if block.get("cellId") == self._player_cell_id:
                self.role_preference.assigned = (
                    Role[block["assignedPosition"].upper()]
                    if block.get("assignedPosition")
                    else Role.FILL
                )

    def block_condition(self, event: WebSocketEventResponse, block_type: str):
        for array in event.data.get("actions"):
            for block in array:
                if (
                    block.get("actorCellId") == self._player_cell_id
                    and block.get("type") == block_type
                    and cast_to_bool(block.get("completed")) != True
                    and cast_to_bool(block.get("isInProgress")) == True
                ):
                    self._player_id = block.get("id")
                    return True

    async def pick_champion(self):
        self._is_picking = True
        for champion in self.get_champions_to_pick():
            if await self.pick(champion):
                self._champion = champion
                self._pick_event = True
                logger.debug(f"Picked: {champion.name.capitalize()}")
                break
        self._is_picking = False

    async def ban_champion(self):
        self._is_banning = True
        bans = self.get_champions_to_ban()
        for champion in bans:
            if await self.ban(champion):
                logger.warning(f"Banned champion {champion.name.capitalize()}")
                break
        self._is_banning = False

    def get_champions_to_pick(self) -> list[Champion]:
        """
        For the assigned role, return a list of champion ids to pick.
        If there is no pick for the assigned role, randomize champions.
        """
        return (
            self._picks[self.role_preference.assigned]
            if self.role_preference.assigned in self._picks
            else random.sample(list(Champion), len(list(Champion)))
        )

    def get_champions_to_ban(self) -> list[Champion]:
        """
        For the assigned role, return a list of champion ids to ban.
        """
        return (
            []
            if self.role_preference.assigned == Role.FILL
            else self._bans[self.role_preference.assigned]
        )

    async def pick(self, champion: Champion) -> bool:
        """
        Send a request to the client API to pick a champion.
        Return True if succeeded and False otherwise.
        """
        return bool(
            await self._http_client.request(
                method="PATCH",
                endpoint=f"/lol-champ-select/v1/session/actions/{self._player_id}",
                payload={
                    "actorCellId": self._player_cell_id,
                    "championId": champion.value,
                    "completed": True,
                    "isAllyAction": True,
                    "type": "pick",
                },
            )
        )

    async def ban(self, champion: Champion) -> bool:
        """
        Send a request to the client API to ban a champion.
        Return True if succeeded and False otherwise.
        """
        return bool(
            await self._http_client.request(
                method="PATCH",
                endpoint=f"/lol-champ-select/v1/session/actions/{self._player_id}",
                payload={
                    "actorCellId": self._player_cell_id,
                    "championId": champion.value,
                    "completed": True,
                    "type": "ban",
                },
            )
        )
