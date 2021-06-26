from .http_request import HTTPRequest
from ...common import get_key_from_value, CHAMPIONS, BOTS
from random import choice
from ...logger import get_logger

logger = get_logger("LPBv2.CreateGame")


class CreateGame(HTTPRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = kwargs.get("role")

    async def create_ranked_game(self):
        queue = {"queueId": 420}
        response = await self.request(
            method="POST", endpoint="/lol-lobby/v2/lobby", payload=queue
        )
        if response:
            logger.warning("Created ranked game")

    async def create_normal_game(self):
        queue = {"queueId": 430}
        response = await self.request(
            method="POST", endpoint="/lol-lobby/v2/lobby", payload=queue
        )
        if response:
            logger.warning("Created normal game")

    async def create_coop_game(self):
        queue = {"queueId": 830}
        response = await self.request(
            method="POST", endpoint="/lol-lobby/v2/lobby", payload=queue
        )
        if response:
            logger.warning("Created Coop game")

    async def create_custom_game(self):
        custom_lobby = {
            "customGameLobby": {
                "configuration": {
                    "category": "Custom",
                    "gameMode": "CLASSIC",
                    "banMode": "StandardBanStrategy",
                    "banTimerDuration": 38,
                    "maxAllowableBans": 6,
                    "pickMode": "DraftModeSinglePickStrategy",
                    "gameMutator": "",
                    "gameServerRegion": "",
                    "mapId": 11,
                    "mutators": {"id": 1},
                    "spectatorPolicy": "AllAllowed",
                    "teamSize": 5,
                },
                "lobbyName": "PRACTICE_TOOL",
                "lobbyPassword": "",
            },
            "isCustom": True,
        }
        response = await self.request(
            method="POST", endpoint="/lol-lobby/v2/lobby", payload=custom_lobby
        )
        if response:
            logger.info("Custom lobby created")

    async def select_lane_position(self):
        position = {
            "firstPreference": self.role.first or "FILL",
            "secondPreference": self.role.second or "FILL",
        }
        logger.error(position)
        response = await self.request(
            method="PUT",
            endpoint="/lol-lobby/v2/lobby/members/localMember/position-preferences",
            payload=position,
        )
        if response:
            logger.warning("Lane position chosen")

    async def fill_with_bots(self, **kwargs):
        while True:
            if not await self.add_bot(champion_id=choice(BOTS), **kwargs):
                break

    async def add_bot(self, **kwargs):
        champion_id = kwargs.get("champion_id") or choice(BOTS)
        bot_difficulty = kwargs.get("bot_difficulty") or "EASY"
        team = kwargs.get("team")
        team_id = "200"
        if team == "ORDER":
            team_id = "100"
        config = {
            "championId": champion_id,
            "botDifficulty": bot_difficulty,
            "teamId": team_id,
        }
        response = await self.request(
            method="POST",
            endpoint="/lol-lobby/v1/lobby/custom/bots",
            payload=config,
        )
        if response:
            logger.warning(
                f"Added bot {get_key_from_value(CHAMPIONS, champion_id).capitalize()} difficulty {bot_difficulty}, team {team}"
            )
            return True

    async def is_matchmaking(self):
        response = await self.request(
            method="GET", endpoint="/lol-lobby/v2/lobby/matchmaking/search-state"
        )
        return response.status_code == 200

    async def start_matchmaking(self):
        response = await self.request(
            method="POST", endpoint="/lol-lobby/v2/lobby/matchmaking/search"
        )
        if response:
            logger.warning("Matchmaking started")
        if not await self.is_matchmaking():
            await self.start_matchmaking()

    async def start_champ_selection(self):
        await self.request(
            method="POST", endpoint="/lol-lobby/v1/lobby/custom/start-champ-select"
        )