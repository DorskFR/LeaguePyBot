from typing import List, Optional

from .models import GameEvent


class GameFlow:
    def __init__(self):
        self.events: Optional[List[GameEvent]]
        self.time: Optional[float]

    def update(self, events_data, game_data):
        self.events = [GameEvent(**event) for event in events_data]
        self.time = game_data.get("gameTime")
