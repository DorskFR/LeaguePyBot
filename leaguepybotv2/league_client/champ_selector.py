from ..common.champions import CHAMPIONS
from ..common.utils import cast_to_bool
from typing import Dict, List


class ChampSelector:
    def __init__(self):
        self.picks: Dict[str, List[int]] = dict()
        self.bans: Dict[str, List[int]] = dict()
        self.first_role: str = "FILL"
        self.second_role: str = "FILL"
        self.phase: str = str()
        self.player_cell_id: str = str()
        self.player_id: str = str()
        self.role: str = str
        self.is_picking: bool = False
        self.is_banning: bool = False

    async def update(self, event):
        await self.update_champ_select_phase(event)
        await self.update_local_player_cell_id(event)

        if self.phase == "PLANNING":
            await self.show_intent(event)

        if (
            self.phase == "BAN_PICK"
            and await self.is_ban_turn(event)
            and not self.is_banning
        ):
            await self.pick_champion(event)

        if (
            self.phase == "BAN_PICK"
            and await self.is_pick_turn(event)
            and not self.is_picking
        ):
            await self.ban_champion(event)

    async def show_intent(self, event):
        pass

    async def is_ban_turn(self, event):
        for array in event.data.get("actions"):
            for block in array:
                if block.get("actorCellId") == self.player_cell_id:
                    self.player_id = block.get("id")
                    if (
                        block.get("type") == "ban"
                        and cast_to_bool(block.get("completed")) != True
                        and cast_to_bool(block.get("isInProgress")) == True
                    ):
                        return True

    async def is_pick_turn(self, event):
        for array in event.data.get("actions"):
            for block in array:
                if block.get("actorCellId") == self.player_cell_id:
                    self.player_id = block.get("id")
                    if (
                        block.get("type") == "pick"
                        and cast_to_bool(block.get("completed")) != True
                        and cast_to_bool(block.get("isInProgress")) == True
                    ):
                        return True

    async def update_champ_select_phase(self, event):
        phase = event.data.get("timer").get("phase")
        if self.phase != phase:
            self.phase = phase

    async def update_local_player_cell_id(self, event):
        self.player_cell_id = event.data.get("localPlayerCellId")

    async def set_role_preference(self, *args, **kwargs):
        self.first_role = kwargs.get("first")
        self.second_role = kwargs.get("second")

    async def set_picks_per_role(self, *args, **kwargs):
        picks = kwargs.get("picks")
        role = kwargs.get("role")
        self.picks[role] = [CHAMPIONS.get(pick.lower()) for pick in picks]

    async def set_bans_per_role(self, *args, **kwargs):
        bans = kwargs.get("bans")
        role = kwargs.get("role")
        self.bans[role] = [CHAMPIONS.get(ban.lower()) for ban in bans]

    async def get_champions_to_pick(self, *args, **kwargs):
        role = kwargs.get("role")
        if role:
            return self.picks.get(role)
        return [pick for picks in self.picks.values() for pick in picks]

    async def get_champions_to_ban(self, *args, **kwargs):
        role = kwargs.get("role")
        if role:
            return self.bans.get(role)
        return [ban for bans in self.bans.values() for ban in bans]

    async def pick_champion(self, event):
        self.is_picking = True
        picks = await self.get_champions_to_pick()
        for pick in picks:
            await self.pick(pick)

    async def ban_champion(self, event):
        pass

    async def pick(self, pick):
        pass

    async def ban(self, ban):
        pass
