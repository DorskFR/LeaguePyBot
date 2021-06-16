import asyncio
from json import dumps
from random import choice, randint

from leaguepybotv2.logger import get_logger

from .core.bots import BOTS
from .core.champions import CHAMPIONS
from .core.utils import cast_to_bool, get_key_from_value
from .league_connector import LeagueConnector
from .league_summoner import LeagueSummoner
from ..common.loop import Loop
from .models import WebsocketEvent

logger = get_logger("LPBv2.Client")


class LeagueClient:
    def __init__(self, *args, **kwargs):
        self.loop = Loop()
        self.default_events = [
            # WebsocketEvent(
            #     endpoint="/lol-gameflow/v1/gameflow-phase",
            #     type=["CREATE", "UPDATE", "DELETE"],
            #     function=self.subscribe_game_phases,
            # ),
            WebsocketEvent(
                endpoint="/lol-matchmaking/v1/search",
                type=["CREATE", "UPDATE", "DELETE"],
                function=self.subscribe_ready_check,
            ),
            WebsocketEvent(
                endpoint="/lol-champ-select/v1/session",
                type=["UPDATE"],
                function=self.subscribe_champ_selection,
                arguments={"ban": 35, "pick": 114},
            ),
        ]
        self.connector = LeagueConnector(
            parent=self, events=self.default_events, *args, **kwargs
        )
        self.summoner = LeagueSummoner(*args, **kwargs)
        self.loop.submit_async(self.start())

    async def start(self):
        self.loop.submit_async(self.connector.listen_websocket())

    async def log_everything(self, endpoint="/"):
        await self.connector.register_event(
            WebsocketEvent(
                endpoint=endpoint,
                type=["CREATE", "UPDATE", "DELETE"],
                function=self.loop_back_log,
            )
        )

    async def loop_back_log(self, event, *args, **kwargs):
        logger.warning(event.uri)
        logger.info(event.type)
        logger.debug(f"{dumps(event.data, indent=4)}\n\n")

    async def login(self, username, password, *args, **kwargs):
        response = await self.connector.request(
            method="POST",
            url="/lol-login/v1/session",
            payload={"username": username, "password": password},
        )
        if response.status_code == 200:
            logger.warning("Logged in")
        else:
            logger.error("Could not login")
            logger.debug(response)

    async def is_matchmaking(self):
        response = await self.connector.request(
            method="GET", endpoint="/lol-lobby/v2/lobby/matchmaking/search-state"
        )
        logger.debug(response)
        return response.status_code == 200

    async def subscribe_game_phases(self, event, *args, **kwargs):
        if event.data in ["None", "Lobby"]:
            # if not await self.is_matchmaking():
            await self.create_ranked_game()

        if event.data in ["PreEndOfGame"]:
            await self.command_all_players()

        if event.data in ["EndOfGame"]:
            await self.report_all_players()
            await self.create_ranked_game()

    async def subscribe_ready_check(self, event, *args, **kwargs):
        if not event.data:
            logger.error("Queue interrupted")
            return
        searchState = event.data.get("searchState")
        playerResponse = event.data.get("readyCheck").get("playerResponse")
        state = event.data.get("readyCheck").get("state")
        if (
            (searchState == "Found" or state == "InProgress")
            and state not in ["EveryoneReady", "Error"]
            and playerResponse != "Accepted"
        ):
            response = await self.connector.request(
                method="POST",
                endpoint="/lol-matchmaking/v1/ready-check/accept",
            )
            if response.status_code == 200:
                logger.warning("Match found: Accepted ready check")
            else:
                logger.error("Could not accept ready check")
                logger.debug(response)

    async def subscribe_champ_selection(self, event, *args, **kwargs):
        player_cell_id = event.data.get("localPlayerCellId")
        phase = event.data.get("timer").get("phase")

        logger.debug(f"Phase: {phase}")

        # if phase == "PLANNING":
        #     for array in event.data.get("actions"):
        #         for block in array:
        #             if block.get("actorCellId") == player_cell_id:
        #                 player_id = block.get("id")
        #                 await intent_champion(connection, 55, player_cell_id, player_id)

        if phase in "BAN_PICK":
            for array in event.data.get("actions"):
                for block in array:
                    if block.get("actorCellId") == player_cell_id:
                        player_id = block.get("id")
                        if (
                            block.get("type") == "ban"
                            and block.get("completed") != True
                            and block.get("isInProgress") == True
                        ):
                            logger.warning("Ban Champion")
                            await self.ban_champion(
                                self.summoner.ban, player_cell_id, player_id
                            )

                        if (
                            block.get("type") == "pick"
                            and block.get("completed") != True
                            and block.get("isInProgress") == True
                        ):
                            logger.warning("Pick Champion")
                            await self.pick_champion(
                                self.summoner.pick, player_cell_id, player_id
                            )

    async def set_pickban_and_role(self, *args, **kwargs):
        """
        pick = name of the champ. ex: "Darius", "Garen, "Velkoz"...
        ban = same
        case does not matter, spelling does

        first = first role (lane)
        second = second role
        options: TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY

        example: set_pickban_and_role(
            pick="Fiora", ban="Shaco", first="TOP", second="MIDDLE"
        )
        """
        if kwargs.get("pick"):
            self.summoner.pick = CHAMPIONS.get(kwargs.get("pick").lower())
        if kwargs.get("ban"):
            self.summoner.ban = CHAMPIONS.get(kwargs.get("ban").lower())
        self.summoner.first_role = kwargs.get("first")
        self.summoner.second_role = kwargs.get("second")

    async def choose_lane_position(self):
        position = {
            "firstPreference": self.summoner.first_role,
            "secondPreference": self.summoner.second_role,
        }
        response = await self.connector.request(
            method="PUT",
            endpoint="/lol-lobby/v2/lobby/members/localMember/position-preferences",
            payload=position,
        )
        if response.status_code == 201:
            logger.warning("Lane position chosen")
        else:
            logger.error("Fail choose_lane_position")
            logger.debug(response)

    async def create_ranked_game(self):
        queue = {"queueId": 420}
        response = await self.connector.request(
            method="POST", endpoint="/lol-lobby/v2/lobby", payload=queue
        )
        if response.status_code == 200:
            logger.warning("Created ranked game")
        else:
            logger.error("Fail create_ranked_game")
            logger.debug(response)
        await self.choose_lane_position()
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

        response = await self.connector.request(
            method="POST", endpoint="/lol-lobby/v2/lobby", payload=custom_lobby
        )
        logger.info(response)

        await self.add_bots(config={"botDifficulty": "EASY", "teamId": "100"})
        await self.add_bots(config={"botDifficulty": "MEDIUM", "teamId": "200"})

        await self.connector.request(
            method="POST", endpoint="/lol-lobby/v1/lobby/custom/start-champ-select"
        )

    async def start_matchmaking(self):
        response = await self.connector.request(
            method="POST", endpoint="/lol-lobby/v2/lobby/matchmaking/search"
        )
        if response.status_code == 204:
            logger.warning("Matchmaking started")
        else:
            logger.error("Fail start_matchmaking")
            logger.debug(response)

    async def pick_champion(self, champion_id, player_cell_id, player_id):
        response = await self.connector.request(
            method="PATCH",
            endpoint=f"/lol-champ-select/v1/session/actions/{player_id}",
            payload={
                "actorCellId": player_cell_id,
                "championId": champion_id,
                "completed": True,
                "isAllyAction": True,
                "type": "pick",
            },
        )
        if response.status_code == 200:
            logger.warning(
                f"Picked champion champion_id: {champion_id}, player_cell_id: {player_cell_id}, player_id: {player_id}"
            )
        else:
            logger.error("Could not pick champion")
            logger.debug(response)

    async def ban_champion(self, champion_id, player_cell_id, player_id):
        response = await self.connector.request(
            method="PATCH",
            endpoint=f"/lol-champ-select/v1/session/actions/{player_id}",
            payload={
                "actorCellId": player_cell_id,
                "championId": champion_id,
                "completed": True,
                "type": "ban",
            },
        )
        if response.status_code == 200:
            logger.warning(
                f"Banned champion champion_id: {champion_id}, player_cell_id: {player_cell_id}, player_id: {player_id}"
            )
        else:
            logger.error("Could not ban champion")
            logger.debug(response)

    async def add_bots(self, *args, **kwargs):
        while True:
            champion_id = choice(BOTS)
            bot = {"championId": champion_id}
            if kwargs.get("config"):
                for k, v in kwargs.get("config").items():
                    bot[k] = v
            logger.warning(bot)
            response = await self.connector.request(
                method="POST", endpoint="/lol-lobby/v1/lobby/custom/bots", payload=bot
            )
            logger.info(response)
            if response.status_code != 204:
                break

    async def create_normal_game(self):
        queue = {"queueId": 430}
        response = await self.connector.request(
            method="POST", endpoint="/lol-lobby/v2/lobby", payload=queue
        )
        if response.status_code == 200:
            logger.warning("Created normal game")
        else:
            logger.error("Fail create_normal_game")
            logger.debug(response)
        await self.start_matchmaking()

    async def get_command_ballot(self):
        response = self.connector.request(
            method="GET", endpoint="/lol-honor-v2/v1/ballot"
        )
        if response.status_code == 200:
            logger.info(response.data.get("eligiblePLayers"))
        else:
            logger.error("Failed to get command ballot")

    async def command_random_player(self):
        players = await self.get_player_list()
        game_id = await self.get_game_id()
        player = players[randint(0, len(players))]
        await self.command_player(game_id, player)

    async def command_all_players(self):
        await self.get_command_ballot()
        players = await self.get_player_list()
        game_id = await self.get_game_id()
        for player in players:
            if player.get("isPlayerTeam"):
                await self.command_player(game_id, player)
                await asyncio.sleep(1)

    async def command_player(self, game_id, player):
        response = await self.connector.request(
            method="POST",
            endpoint="/lol-honor-v2/v1/honor-player",
            payload={
                "gameId": game_id,
                "honorCategory": "HEART",
                "summonerId": player.get("id"),
            },
        )
        if response.status_code == 200:
            logger.warning(f"Commanded {player.get('name')} ({player.get('champion')})")
        else:
            logger.error(
                f"Could not command {player.get('name')} ({player.get('champion')})"
            )
            logger.debug(response)

    async def report_all_players(self):
        players = await self.get_player_list()
        game_id = await self.get_game_id()
        for player in players:
            if not player.get("isSelf"):
                await self.report_player(game_id, player)
                await asyncio.sleep(1)

    async def report_player(self, game_id, player):
        response = await self.connector.request(
            method="POST",
            endpoint="/lol-end-of-game/v2/player-complaints",
            payload={
                "gameId": game_id,
                "reportedSummonerId": player.get("id"),
            },
        )
        if response.status_code == 200:
            logger.warning(f"Reported {player.get('name')} ({player.get('champion')})")
        else:
            logger.error(
                f"Could not report player {player.get('name')} ({player.get('champion')})"
            )
            logger.debug(response)

    async def get_player_list(self):
        response = await self.connector.request(
            method="GET", endpoint="/lol-end-of-game/v1/eog-stats-block"
        )

        players = list()

        if response.status_code == 200:
            my_id = response.data.get("summonerId")
            for team in response.data.get("teams"):
                for player in team.get("players"):
                    d = {
                        "id": player.get("summonerId"),
                        "name": player.get("summonerName"),
                        "champion": get_key_from_value(
                            CHAMPIONS, player.get("championId")
                        ).capitalize(),
                        "isPlayerTeam": cast_to_bool(team.get("isPlayerTeam")),
                        "isSelf": False,
                    }
                    if player.get("summonerId") == my_id:
                        d["isSelf"] = True
                    players.append(d)
        else:
            logger.error("Could not get player list")
            logger.debug(response)

        return players

    async def get_game_id(self):
        response = await self.connector.request(
            method="GET", endpoint="/lol-end-of-game/v1/eog-stats-block"
        )
        game_id = None
        if response.status_code == 200:
            game_id = response.data.get("gameId")
        else:
            logger.error("Could not get game id")
            logger.debug(response)
        return game_id

    async def get_endofgame_celebrations(self):
        response = await self.connector.request(
            method="GET", endpoint="/lol-pre-end-of-game/v1/currentSequenceEvent"
        )
        celebration = response.get("name")
        return celebration

    async def skip_mission_celebrations(self):
        celebration = await self.get_endofgame_celebrations()
        await self.connector.request(
            method="POST", endpoint=f"/lol-pre-end-of-game/v1/complete/{celebration}"
        )

    async def create_coop_game(self):
        queue = {"queueId": 830}
        response = await self.connector.request(
            method="POST", endpoint="/lol-lobby/v2/lobby", payload=queue
        )
        if response.status_code == 200:
            logger.warning("Created Coop game")
        else:
            logger.error("Fail create_coop_game")
            logger.debug(response)
        await self.start_matchmaking()
