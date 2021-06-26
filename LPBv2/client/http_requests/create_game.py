from .http_request import HTTPRequest
from ...common import get_key_from_value, CHAMPIONS, BOTS
from random import choice
from ...logger import get_logger

logger = get_logger("LPBv2.CreateGame")


class CreateGame(HTTPRequest):
    def __init__(self):
        super().__init__()

    async def create_ranked_game(self):
        queue = {"queueId": 420}
        response = await self.request(
            method="POST", endpoint="/lol-lobby/v2/lobby", payload=queue
        )
        if response:
            logger.warning("Created ranked game")
            await self.choose_lane_position()
            await self.start_matchmaking()

    async def create_normal_game(self):
        queue = {"queueId": 430}
        response = await self.request(
            method="POST", endpoint="/lol-lobby/v2/lobby", payload=queue
        )
        if response:
            logger.warning("Created normal game")

        await self.start_matchmaking()

    async def create_coop_game(self):
        queue = {"queueId": 830}
        response = await self.request(
            method="POST", endpoint="/lol-lobby/v2/lobby", payload=queue
        )
        if response:
            logger.warning("Created Coop game")
        await self.start_matchmaking()

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
        await self.add_bots(config={"botDifficulty": "EASY", "teamId": "100"})
        await self.add_bots(config={"botDifficulty": "MEDIUM", "teamId": "200"})
        await self.request(
            method="POST", endpoint="/lol-lobby/v1/lobby/custom/start-champ-select"
        )

    async def choose_role(self):
        position = {
            "firstPreference": self.summoner.first_role,
            "secondPreference": self.summoner.second_role,
        }
        response = await self.request(
            method="PUT",
            endpoint="/lol-lobby/v2/lobby/members/localMember/position-preferences",
            payload=position,
        )
        if response:
            logger.warning("Lane position chosen")

    async def add_bots(self, *args, **kwargs):
        while True:
            champion_id = choice(BOTS)
            bot = {"championId": champion_id}
            if kwargs.get("config"):
                for k, v in kwargs.get("config").items():
                    bot[k] = v
            response = await self.request(
                method="POST", endpoint="/lol-lobby/v1/lobby/custom/bots", payload=bot
            )
            if response:
                logger.warning(
                    f"Added bot {get_key_from_value(CHAMPIONS, bot.get('championId')).capitalize()} difficulty {bot.get('botDifficulty')}, team {bot.get('teamId')[0]}"
                )
            else:
                break

    async def is_matchmaking(self):
        response = await self.request(
            method="GET", endpoint="/lol-lobby/v2/lobby/matchmaking/search-state"
        )
        logger.debug(response)
        return response.status_code == 200

    async def start_matchmaking(self):
        if await self.is_matchmaking():
            return
        response = await self.request(
            method="POST", endpoint="/lol-lobby/v2/lobby/matchmaking/search"
        )
        if response:
            logger.warning("Matchmaking started")
