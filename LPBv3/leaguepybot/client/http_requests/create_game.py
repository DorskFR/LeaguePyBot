import asyncio
from random import choice

from leaguepybot.client.http_requests.http_request import HTTPRequest
from leaguepybot.common.bots import BOTS
from leaguepybot.common.champions import CHAMPIONS
from leaguepybot.common.logger import get_logger
from leaguepybot.common.models import WebSocketEventResponse
from leaguepybot.common.utils import get_key_from_value

logger = get_logger("LPBv3.CreateGame")


class CreateGame(HTTPRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = kwargs.get("role")

    async def create_ranked_game(self):
        queue = {"queueId": 420}
        response = await self.request(method="POST", endpoint="/lol-lobby/v2/lobby", payload=queue)
        if response:
            logger.debug("Created ranked game")

    async def create_normal_game(self):
        queue = {"queueId": 430}
        response = await self.request(method="POST", endpoint="/lol-lobby/v2/lobby", payload=queue)
        if response:
            logger.debug("Created normal game")

    async def create_coop_game(self):
        queue = {"queueId": 830}
        response = await self.request(method="POST", endpoint="/lol-lobby/v2/lobby", payload=queue)
        if response:
            logger.debug("Created Coop game")

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
            logger.debug("Custom lobby created")

    async def select_lane_position(self):
        position = {
            "firstPreference": self.role.first or "FILL",
            "secondPreference": self.role.second or "FILL",
        }
        response = await self.request(
            method="PUT",
            endpoint="/lol-lobby/v2/lobby/members/localMember/position-preferences",
            payload=position,
        )
        if response:
            logger.debug(
                f"Selected lane position {position.get('firstPreference')} and {position.get('secondPreference')}"
            )

    async def fill_with_bots(self, **kwargs):
        while True:
            if not await self.add_bot(champion_id=choice(BOTS), **kwargs):
                break

    async def add_bot(self, **kwargs):
        champion_id = kwargs.get("champion_id") or choice(BOTS)
        bot_difficulty = kwargs.get("bot_difficulty") or "EASY"
        team = kwargs.get("team") or "CHAOS"
        team_id = "100" if team == "ORDER" else "200"
        config = {"championId": champion_id, "botDifficulty": bot_difficulty, "teamId": team_id}

        response = await self.request(
            method="POST", endpoint="/lol-lobby/v1/lobby/custom/bots", payload=config
        )

        if response:
            logger.debug(
                f"Added bot {get_key_from_value(CHAMPIONS, champion_id).capitalize()} difficulty {bot_difficulty}, team {team}"
            )

            return True

    async def is_matchmaking(self):
        response = await self.request(
            method="GET", endpoint="/lol-lobby/v2/lobby/matchmaking/search-state"
        )
        return response.data.get("searchState") in ["Searching", "Found", "Accepted"]

    async def start_matchmaking(self):
        response = await self.request(
            method="POST", endpoint="/lol-lobby/v2/lobby/matchmaking/search"
        )
        if response:
            logger.debug("Matchmaking started")
        await asyncio.sleep(1)
        if not await self.is_matchmaking():
            await self.start_matchmaking()

    async def start_champ_selection(self):
        await self.request(method="POST", endpoint="/lol-lobby/v1/lobby/custom/start-champ-select")

    async def chain_game_at_eog(self, event: WebSocketEventResponse):
        if event.data == "EndOfGame":
            for coro in event.arguments:
                await coro()
