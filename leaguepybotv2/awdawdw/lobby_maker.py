from random import randint

from leaguepybotv2.core.champions import CHAMPIONS
from leaguepybotv2.leagueclient.league_client import LeagueClient
from leaguepybotv2.logger.logger import get_logger

logger = get_logger()


class LobbyMaker(LeagueClient):
    def __init__(self, connection):
        super().__init__(connection)

    async def create_normal_game(self, *args, **kwargs):
        queue = {"queueId": 430}
        return await self._request(
            method="POST", endpoint="/lol-lobby/v2/lobby", data=queue
        )

    async def create_ranked_game(self, *args, **kwargs):
        queue = {"queueId": 420}
        await self._request(method="POST", endpoint="/lol-lobby/v2/lobby", data=queue)

    async def position_top_middle(self, *args, **kwargs):
        position = {"firstPreference": "TOP", "secondPreference": "MIDDLE"}
        await self._request(
            method="PUT",
            endpoint="/lol-lobby/v2/lobby/members/localMember/position-preferences",
            data=position,
        )

    async def create_custom_game(self, *args, **kwargs):
        custom = {
            "customGameLobby": {
                "configuration": {
                    "gameMode": "PRACTICETOOL",
                    "gameMutator": "",
                    "gameServerRegion": "",
                    "mapId": 11,
                    "mutators": {"id": 1},
                    "spectatorPolicy": "AllAllowed",
                    "teamSize": 5,
                },
                "lobbyName": "PRACTICETOOL",
                "lobbyPassword": "",
            },
            "isCustom": True,
        }
        await self._request(method="POST", endpoint="/lol-lobby/v2/lobby", data=custom)
        await self.add_bots({"botDifficulty": "EASY", "teamId": "100"})
        await self.add_bots_team2()

    async def add_bots(self, *args, **kwargs):
        while True:
            champion_id = randint(1, max(CHAMPIONS.values()))
            bot = {"championId": champion_id, **args}
            logger.warning(bot)
            response = await self._request(
                method="POST", endpoint="/lol-lobby/v1/lobby/custom/bots", data=bot
            )
            logger.info(response)
            if response.get("httpStatus") == 400:
                break
