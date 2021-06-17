class LeagueSummoner:
    def __init__(self, *args, **kwargs):
        self.name: str = str()
        self.puuid: str = str()
        self.summoner_id: str = str()
        self.account_level: int = int()
        self.pick: int = int()
        self.ban: int = int()
        self.first_role: str = "FILL"
        self.second_role: str = "FILL"
