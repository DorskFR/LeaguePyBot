from ..common.champions import CHAMPIONS
from typing import Dict, List


class LeagueSummoner:
    def __init__(self, *args, **kwargs):
        self.name: str = str()
        self.puuid: str = str()
        self.summoner_id: str = str()
        self.account_level: int = int()

    async def update(self, *args, **kwargs):
        pass
