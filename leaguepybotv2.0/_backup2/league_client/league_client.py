import asyncio
from json import dumps
from random import choice, randint

from leaguepybotv2.logger import Colors, get_logger

from ..common.loop import LoopInNewThread
from ..common.models import TeamMember, WebsocketEvent
from .champ_selector import ChampSelector
from .core.bots import BOTS
from .core.champions import CHAMPIONS
from .core.utils import cast_to_bool, get_key_from_value
from .league_connector import LeagueConnector
from .league_summoner import LeagueSummoner

logger = get_logger("LPBv2.Client")


class LeagueClient:
    def __init__(self, *args, **kwargs):
        self.loop = LoopInNewThread()
        self.summoner = LeagueSummoner(*args, **kwargs)
        self.champ_selector = ChampSelector()
        self.default_events = [
            WebsocketEvent(
                endpoint="/lol-gameflow/v1/gameflow-phase",
                type=["CREATE", "UPDATE", "DELETE"],
                function=self.subscribe_game_phases,
            ),
            WebsocketEvent(
                endpoint="/lol-matchmaking/v1/search",
                type=["CREATE", "UPDATE", "DELETE"],
                function=self.subscribe_ready_check,
            ),
            WebsocketEvent(
                endpoint="/lol-champ-select/v1/session",
                type=["UPDATE"],
                function=self.subscribe_champ_selection,
                arguments={"ban": self.summoner.ban, "pick": self.summoner.pick},
            ),
        ]
        self.connector = LeagueConnector(
            parent=self, events=self.default_events, *args, **kwargs
        )
        self.loop.submit_async(self.connector.listen_websocket())

    def start(self):
        logger.info("LeagueClient started")

    async def request(self, *args, **kwargs):
        response = await self.connector.request(**kwargs)
        if response.status_code in [200, 201, 202, 203, 204, 205, 206]:
            return response

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
        response = await self.request(
            method="POST",
            url="/lol-login/v1/session",
            payload={"username": username, "password": password},
        )
        if response:
            logger.warning("Logged in")

    async def is_matchmaking(self):
        response = await self.request(
            method="GET", endpoint="/lol-lobby/v2/lobby/matchmaking/search-state"
        )
        logger.debug(response)
        return response.status_code == 200

    async def subscribe_game_phases(self, event, *args, **kwargs):
        if event.data:
            self.client_phase = event.data

    async def subscribe_ready_check(self, event, *args, **kwargs):
        if not event.data:
            logger.error("Queue interrupted")
            self.client_phase = "None"
            return
        searchState = event.data.get("searchState")
        playerResponse = event.data.get("readyCheck").get("playerResponse")
        state = event.data.get("readyCheck").get("state")
        if (
            (searchState == "Found" or state == "InProgress")
            and state not in ["EveryoneReady", "Error"]
            and playerResponse != "Accepted"
        ):
            response = await self.request(
                method="POST",
                endpoint="/lol-matchmaking/v1/ready-check/accept",
            )
            if response:
                logger.warning("Match found: Accepted ready check")

    async def update_local_player_cell_id(self, event):
        self.player_cell_id = event.data.get("localPlayerCellId")

    async def subscribe_champ_selection(self, event):
        await self.champ_selector.update(event)

    async def choose_lane_position(self):
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

    async def create_ranked_game(self):
        queue = {"queueId": 420}
        response = await self.request(
            method="POST", endpoint="/lol-lobby/v2/lobby", payload=queue
        )
        if response:
            logger.warning("Created ranked game")
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

    async def start_matchmaking(self):
        response = await self.request(
            method="POST", endpoint="/lol-lobby/v2/lobby/matchmaking/search"
        )
        if response:
            logger.warning("Matchmaking started")

    async def pick_champion(self, champion_id, player_cell_id, player_id):
        response = await self.request(
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
        if response:
            logger.warning(
                f"Picked champion champion_id: {Colors.cyan}{champion_id}{Colors.reset}, player_cell_id: {Colors.dark_grey}{player_cell_id}{Colors.reset}, player_id: {Colors.dark_grey}{player_id}{Colors.reset}"
            )

    async def ban_champion(self, champion_id, player_cell_id, player_id):
        response = await self.request(
            method="PATCH",
            endpoint=f"/lol-champ-select/v1/session/actions/{player_id}",
            payload={
                "actorCellId": player_cell_id,
                "championId": champion_id,
                "completed": True,
                "type": "ban",
            },
        )
        if response:
            logger.warning(
                f"Banned champion champion_id: {Colors.red}{champion_id}{Colors.reset}, player_cell_id: {Colors.dark_grey}{player_cell_id}{Colors.reset}, player_id: {Colors.dark_grey}{player_id}{Colors.reset}"
            )

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

    async def create_normal_game(self):
        queue = {"queueId": 430}
        response = await self.request(
            method="POST", endpoint="/lol-lobby/v2/lobby", payload=queue
        )
        if response:
            logger.warning("Created normal game")

        await self.start_matchmaking()

    async def get_command_ballot(self):
        response = await self.request(method="GET", endpoint="/lol-honor-v2/v1/ballot")
        if response:
            logger.info(response.data.get("eligiblePLayers"))

    async def command_random_player(self):
        players = await self.get_eog_player_list()
        game_id = await self.get_game_id()
        player = players[randint(0, len(players))]
        await self.command_player(game_id, player)

    async def command_all_players(self):
        await self.get_command_ballot()
        players = await self.get_eog_player_list()
        game_id = await self.get_game_id()
        for player in players:
            if player.get("isPlayerTeam"):
                await self.command_player(game_id, player)
                await asyncio.sleep(1)

    async def command_player(self, game_id, player):
        response = await self.request(
            method="POST",
            endpoint="/lol-honor-v2/v1/honor-player",
            payload={
                "gameId": game_id,
                "honorCategory": "HEART",
                "summonerId": player.summonerId,
            },
        )
        if response:
            logger.warning(f"Commanded {player.summonerName} ({player.championName})")

    async def report_all_players(self):
        players = await self.get_eog_player_list()
        game_id = await self.get_game_id()
        for player in players:
            if not player.isSelf:
                await self.report_player(game_id, player)
                await asyncio.sleep(0.1)

    async def report_player(self, game_id, player):
        response = await self.request(
            method="POST",
            endpoint="/lol-end-of-game/v2/player-complaints",
            payload={
                "gameId": game_id,
                "reportedSummonerId": player.summonerId,
            },
        )
        if response:
            logger.warning(f"Reported {player.summonerName} ({player.championName})")

    async def get_eog_player_list(self):
        response = await self.request(
            method="GET", endpoint="/lol-end-of-game/v1/eog-stats-block"
        )
        players = list()
        if response:
            my_id = response.data.get("summonerId")
            for team in response.data.get("teams"):
                for player in team.get("players"):
                    member = TeamMember(
                        summonerId=player.get("summonerId"),
                        summonerName=player.get("summonerName"),
                        championId=player.get("championId"),
                        championName=get_key_from_value(
                            CHAMPIONS, player.get("championId")
                        ).capitalize(),
                        isPlayerTeam=cast_to_bool(team.get("isPlayerTeam")),
                        isSelf=player.get("summonerId") == my_id,
                    )
                    players.append(member)
        return players

    async def get_game_id(self):
        response = await self.request(
            method="GET", endpoint="/lol-end-of-game/v1/eog-stats-block"
        )
        game_id = None
        if response:
            game_id = response.data.get("gameId")
        return game_id

    async def get_endofgame_celebrations(self):
        response = await self.request(
            method="GET", endpoint="/lol-pre-end-of-game/v1/currentSequenceEvent"
        )
        celebration = response.get("name")
        return celebration

    async def skip_mission_celebrations(self):
        celebration = await self.get_endofgame_celebrations()
        await self.request(
            method="POST", endpoint=f"/lol-pre-end-of-game/v1/complete/{celebration}"
        )

    async def create_coop_game(self):
        queue = {"queueId": 830}
        response = await self.request(
            method="POST", endpoint="/lol-lobby/v2/lobby", payload=queue
        )
        if response:
            logger.warning("Created Coop game")
        await self.start_matchmaking()