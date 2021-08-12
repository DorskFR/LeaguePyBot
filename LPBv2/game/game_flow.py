from typing import List, Optional

from ..common import GameEvent, debug_coro


class GameFlow:
    def __init__(self):
        self.events: Optional[List[GameEvent]] = list()
        self.time: Optional[float] = 0.0
        self.is_ingame = False
        self.game_start = False
        self.current_action: str = str()

    #@debug_coro
    async def update(self, **kwargs):
        events_data = kwargs.pop("events_data")
        game_data = kwargs.pop("game_data")
        await self.update_events(events_data)
        await self.update_time(game_data)

    #@debug_coro
    async def update_is_ingame(self, is_ingame=False):
        if self.is_ingame != is_ingame and is_ingame:
            self.game_start = True
        self.is_ingame = is_ingame

    #@debug_coro
    async def update_events(self, events_data):
        self.events = [GameEvent(**event) for event in events_data]

    #@debug_coro
    async def update_time(self, game_data):
        self.time = game_data.get("gameTime") or 0.0

    #@debug_coro
    async def update_current_action(self, action: str):
        self.current_action = action
