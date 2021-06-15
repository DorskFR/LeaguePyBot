from typing import List, Optional

from ..logger import get_logger
from .models import GameEvent

logger = get_logger()


class GameFlow:
    def __init__(self):
        self.events: Optional[List[GameEvent]]
        self.time: Optional[float]

    def update(self, events_data, game_data):
        self.events = [GameEvent(**event) for event in events_data]
        self.time = game_data.get("gameTime")
