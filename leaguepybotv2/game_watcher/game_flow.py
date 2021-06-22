from typing import List, Optional

from ..common.models import GameEvent


class GameFlow:
    def __init__(self):
        self.events: Optional[List[GameEvent]] = list()
        self.time: Optional[float] = 0.0
        self.is_ingame = False
        self.current_action: str = str()

    async def update(self, **kwargs):
        events_data = kwargs.pop("events_data")
        game_data = kwargs.pop("game_data")
        await self.update_events(events_data)
        await self.update_time(game_data)

    async def update_is_ingame(self, is_ingame=False):
        self.is_ingame = is_ingame

    async def update_events(self, events_data):
        self.events = [GameEvent(**event) for event in events_data]

    async def update_time(self, game_data):
        self.time = game_data.get("gameTime") or 0.0

    async def update_current_action(self, action: str):
        self.current_action = action
