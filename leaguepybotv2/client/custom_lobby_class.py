from lcu_driver import Connector
from leaguepybotv2.logger.logger import get_logger
import asyncio

logger = get_logger()

# ---------------------------------------------
# Get Summoner Data
# ---------------------------------------------


class LeagueLobby:
    def __init__(self):
        self.connector = Connector()
        self.connector.start()

    async def connect(self):
        await self.get_summoner_data()
        # await self.get_lockfile()
        # await self.create_lobby()
        # await self.add_bots_team1()
        # await self.add_bots_team2()

    async def disconnect(self):
        logger.info("The client was closed")
        await self.connector.stop()

    async def lobby_created(self, event):
        logger.info(
            f"The summoner {event.data['localMember']['summonerName']} created a lobby."
        )

    async def get_summoner_data(self):
        summoner = await self.connector.connection.request(
            "GET", "/lol-summoner/v1/current-summoner"
        )
        data = await summoner.json()
        logger.info(f"displayName:    {data['displayName']}")
        logger.info(f"summonerId:     {data['summonerId']}")
        logger.info(f"puuid:          {data['puuid']}")
        logger.info("-")

    # ---------------------------------------------
    # Create Lobby
    # ---------------------------------------------
    async def create_lobby(self):
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
        await self.connector.connection.request(
            "POST", "/lol-lobby/v2/lobby", data=custom
        )

    # ---------------------------------------------
    # Add Team1 Bots By Champion ID
    # ---------------------------------------------
    async def add_bots_team1(self):
        soraka = {"championId": 16, "botDifficulty": "EASY", "teamId": "100"}
        await self.connector.connection.request(
            "POST", "/lol-lobby/v1/lobby/custom/bots", data=soraka
        )

    # ---------------------------------------------
    # Add Team2 Bots By Champion Name
    # ---------------------------------------------
    async def add_bots_team2(self):
        available_bots = await self.connector.connection.request(
            "GET", "/lol-lobby/v2/lobby/custom/available-bots"
        )
        champions = {bot["name"]: bot["id"] for bot in await available_bots.json()}

        team2 = ["Caitlyn", "Blitzcrank", "Darius", "Morgana", "Lux"]

        for name in team2:
            bot = {
                "championId": champions[name],
                "botDifficulty": "MEDIUM",
                "teamId": "200",
            }
            await self.connector.connection.request(
                "POST", "/lol-lobby/v1/lobby/custom/bots", data=bot
            )

    # ---------------------------------------------
    #  lockfile
    # ---------------------------------------------
    async def get_lockfile(self):
        import os

        path = os.path.join(
            self.connector.connection.installation_path.encode("gbk").decode("utf-8"),
            "lockfile",
        )
        if os.path.isfile(path):
            file = open(path, "r")
            text = file.readline().split(":")
            file.close()
            logger.info(self.connector.connection.address)
            logger.info(f"riot    {text[3]}")
            return text[3]
        return None

    # ---------------------------------------------
    # Websocket Listening
    # ---------------------------------------------

    # ---------------------------------------------
    # main
    # ---------------------------------------------


async def main():
    lobby = LeagueLobby()
    print(lobby)
    print(lobby.connector)
    lobby.connector.start()
    await asyncio.sleep(2)
    print(lobby.connector.connection)


if __name__ == "__main__":
    asyncio.run(main())
