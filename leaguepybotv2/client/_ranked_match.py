from lcu_driver import Connector
from leaguepybotv2.logger.logger import get_logger
import asyncio
from random import randint
import time

logger = get_logger()

# ---------------------------------------------
# Get Summoner Data
# ---------------------------------------------
async def get_summoner_data(connection):
    summoner = await connection.request("GET", "/lol-summoner/v1/current-summoner")
    data = await summoner.json()
    logger.info(f"displayName:    {data['displayName']}")
    logger.info(f"summonerId:     {data['summonerId']}")
    logger.info(f"puuid:          {data['puuid']}")
    logger.info("-")


# ---------------------------------------------
# Create Lobby
# ---------------------------------------------
async def create_lobby(connection):
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
    await connection.request("POST", "/lol-lobby/v2/lobby", data=custom)


async def is_matchmaking(connection):

    response = await connection.request(
        "GET", "/lol-lobby/v2/lobby/matchmaking/search-state"
    )
    response = await response.json()
    return response.get("httpStatus") == 200


# ---------------------------------------------
# Add Team1 Bots By Champion ID
# ---------------------------------------------
async def add_bots_team1(connection):
    soraka = {"championId": 16, "botDifficulty": "EASY", "teamId": "100"}
    await connection.request("POST", "/lol-lobby/v1/lobby/custom/bots", data=soraka)


# ---------------------------------------------
# Add Team2 Bots By Champion Name
# ---------------------------------------------
async def add_bots_team2(connection):
    available_bots = await connection.request(
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
        await connection.request("POST", "/lol-lobby/v1/lobby/custom/bots", data=bot)


# ---------------------------------------------
#  lockfile
# ---------------------------------------------
async def get_lockfile(connection):
    import os

    path = os.path.join(
        connection.installation_path.encode("gbk").decode("utf-8"), "lockfile"
    )
    if os.path.isfile(path):
        file = open(path, "r")
        text = file.readline().split(":")
        file.close()
        logger.info(connection.address)
        logger.info(f"riot    {text[3]}")
        return text[3]
    return None


# ---------------------------------------------
# Websocket Listening
# ---------------------------------------------

connector = Connector()

import json


ROUTES = [
    {"method": "GET", "url": "/lol-lobby-team-builder/v1/matchmaking"},
    {
        "method": "POST",
        "url": "/lol-lobby-team-builder/v1/matchmaking/low-priority-queue/abandon",
    },
    {"method": "POST", "url": "/lol-lobby-team-builder/v1/matchmaking/search"},
    {
        "method": "POST",
        "url": "/lol-lobby-team-builder/v1/position-preferences",
    },
    {"method": "GET", "url": "/lol-lobby-team-builder/v1/ready-check"},
    {"method": "POST", "url": "/lol-lobby-team-builder/v1/ready-check/accept"},
    {"method": "POST", "url": "/lol-lobby-team-builder/v1/ready-check/decline"},
    {"method": "GET", "url": "/lol-lobby-team-builder/v1/tb-enabled-features"},
    {
        "method": "POST",
        "url": "/lol-lobby-team-builder/v2/position-preferences",
    },
    {"method": "GET", "url": "/lol-lobby/v1/autofill-displayed"},
    {"method": "PUT", "url": "/lol-lobby/v1/autofill-displayed"},
    {
        "method": "POST",
        "url": "/lol-lobby/v2/matchmaking/quick-search",
        "payload": {"lobbyChange": "true"},
    },
]


async def make_request(connection, method: str, url: str, payload: str = None):
    try:
        if payload:
            response = await connection.request(
                method=method, endpoint=url, data=payload
            )
        else:
            response = await connection.request(method=method, endpoint=url)
        response_json = await response.json()
        logger.info(url)
        logger.warning(json.dumps(response_json, indent=4))
    except Exception as e:
        logger.error(e)


async def login(connection):
    await make_request(
        connection,
        method="POST",
        url="/lol-login/v1/session",
        payload={"username": "FioraJapan3016", "password": "fiorajapan3016"},
    )
    logger.error("Logged in")


async def check_logged_in(connection):
    try:
        response = await connection.request("GET", "/lol-login/v1/session")
        logger.warning("Already logged in")
    except:
        logger.warning("Logging in")
        await login(connection)


async def check_loadouts(connection):
    """
    loadouts are the emotes, banner, etc.
    """
    await make_request(connection, method="GET", url="/lol-loadouts/v1/loadouts-ready")
    # -> true


async def pre_end_of_game(connection):
    await make_request(
        connection,
        method="GET",
        url="/lol-pre-end-of-game/v1/currentSequenceEvent",
    )


async def get_notifications(connection):
    await make_request(
        connection,
        method="GET",
        url="/player-notifications/v1/notifications",
    )


async def delete_notifications(connection):
    await make_request(
        connection,
        method="DELETE",
        url="/player-notifications/v1/notifications",
    )


async def gameflow_available(connection):
    await make_request(
        connection,
        method="GET",
        url="/lol-gameflow/v1/availability",
    )


async def gameflow_metadata(connection):
    await make_request(
        connection,
        method="GET",
        url="/lol-gameflow/v1/gameflow-metadata/player-status",
    )


async def gameflow_phase(connection):
    await make_request(
        connection,
        method="GET",
        url="/lol-gameflow/v1/gameflow-phase",
    )


async def check_player_notifications(connection):
    await make_request(
        connection,
        method="GET",
        url="/player-notifications/v1/notifications",
    )


async def delete_player_notification(connection, id: int):
    await make_request(
        connection,
        method="DELETE",
        url=f"/player-notifications/v1/notifications/{id}",
    )


async def create_normal_game(connection):
    queue = {"queueId": 430}
    await connection.request("POST", "/lol-lobby/v2/lobby", data=queue)


async def create_ranked_game(connection):
    queue = {"queueId": 420}
    await connection.request("POST", "/lol-lobby/v2/lobby", data=queue)


async def position_top_middle(connection):
    position = {"firstPreference": "TOP", "secondPreference": "MIDDLE"}
    await connection.request(
        "PUT",
        "/lol-lobby/v2/lobby/members/localMember/position-preferences",
        data=position,
    )


async def start_matchmaking(connection):
    await connection.request("POST", "/lol-lobby/v2/lobby/matchmaking/search")


async def stop_matchmaking(connection):
    await connection.request("DELETE", "/lol-lobby/v2/lobby/matchmaking/search")


async def start_champ_select(connection):
    await connection.request("POST", "/lol-lobby/v1/lobby/custom/start-champ-select")


async def quit_lobby(connection):
    await connection.request("DELETE", "/lol-lobby/v2/lobby")


async def get_lobby_members(connection):
    await make_request(connection, "GET", "/lol-lobby/v2/lobby/members")


async def get_pickable_champions(connection):
    await make_request(connection, "GET", "/lol-champ-select/v1/pickable-champion-ids")


async def get_current_champion(connection):
    await make_request(connection, "GET", "/lol-champ-select/v1/current-champion")


async def choose_champion(connection):
    await make_request(
        connection,
        method="POST",
        url="/lol-champ-select/v1/grid-champions/114",
        payload={"selectionStatus": {"selectedByMe": "true"}},
    )


async def pick_fiora(connection):
    payload = {"championId": 114, "completed": True, "type": "string"}
    await connection.request(
        "PATCH",
        "/lol-champ-select/v1/session/actions/1",
        data=payload,
    )


async def get_session(connection):
    await make_request(connection, method="GET", url="/lol-champ-select/v1/session")


@connector.ready
async def connect(connection):
    await get_lockfile(connection)
    await check_logged_in(connection)
    await get_summoner_data(connection)
    # await get_reported_players(connection)
    # await create_ranked_game(connection)

    # await create_normal_game(connection)
    # await asyncio.sleep(5)
    # await stop_matchmaking(connection)
    # await check_player_notifications(connection)
    # await delete_player_notification(connection, 4)
    # await start_matchmaking(connection)
    # await get_matchmaking_state(connection)
    # await create_lobby(connection)
    # await start_champ_select(connection)
    # await asyncio.sleep(1)
    # await get_pickable_champions(connection)
    # await asyncio.sleep(1)
    # await get_session(connection)
    # await asyncio.sleep(1)
    # await pick_fiora(connection)
    # await choose_champion(connection)
    # await asyncio.sleep(1)
    # await get_current_champion(connection)
    # await get_lobby_members(connection)
    # await asyncio.sleep(5)
    # await quit_lobby(connection)
    # await add_bots_team2(connection)
    # await add_bots_team1(connection)

    # await make_request(
    #     connection,
    #     method="POST",
    #     url="/lol-lobby/v2/matchmaking/quick-search",
    #     payload={"queueId": 420},
    # )

    # await make_request(
    #     connection,
    #     method="GET",
    #     url="/lol-gameflow/v1/battle-training",
    # )
    # -> []

    # for route in ROUTES:
    #     await make_request(
    #         connection, route.get("method"), route.get("url"), route.get("payload")
    #     )
    #     await asyncio.sleep(1)


# @connector.ws.register(
#     "/lol-matchmaking/v1/ready-check", event_types=("CREATE", "UPDATE")
# )
# async def subscribe_ready_check(connection, event):
#     # playerResponse Accepted, state InProgress
#     # state StrangerNotReady
#     # state EveryoneReady
#     player_response = event.data.get("playerResponse")
#     state = event.data.get("state")


async def command_random_player(connection):
    player_ids = await get_player_list(connection)
    game_id = await get_game_id(connection)
    commanded_player = player_ids[randint(0, len(player_ids))]
    await connection.request(
        "POST",
        "/lol-honor-v2/v1/honor-player",
        data={
            "gameId": game_id,
            "honorCategory": "HEART",
            "summonerId": commanded_player,
        },
    )
    logger.warning(f"Commanded {commanded_player}")


@connector.ws.register(
    "/lol-gameflow/v1/gameflow-phase", event_types=("CREATE", "UPDATE", "DELETE")
)
async def subscribe_game_phases(connection, event):
    phases = [
        "None",
        "Lobby",
        "Matchmaking",
        "ReadyCheck",
        "ChampSelect",
        "InProgress",
        "WaitingForStats",
        "PreEndOfGame",
        "EndOfGame",
    ]
    logger.error(event.data)
    if event.data in ["None", "Lobby"]:
        if not await is_matchmaking(connection):
            await create_ranked_game(connection)
            await position_top_middle(connection)
            await start_matchmaking(connection)

    if event.data in ["PreEndOfGame"]:
        await command_random_player(connection)

    if event.data in ["EndOfGame"]:
        await report_all_players(connection)
        await create_ranked_game(connection)
        await position_top_middle(connection)
        await start_matchmaking(connection)

    await asyncio.sleep(1)


async def accept_ready_check(connection):
    await connection.request(
        "POST",
        "/lol-matchmaking/v1/ready-check/accept",
    )
    logger.error("Accepted ready check")


@connector.ws.register("/lol-matchmaking/v1/search", event_types=("CREATE", "UPDATE"))
async def subscribe_matchmaking(connection, event):
    # create = searchState searching, playerResponse none, state invalid
    searchState = event.data.get("searchState")
    playerResponse = event.data.get("readyCheck").get("playerResponse")
    state = event.data.get("readyCheck").get("state")

    if (
        (searchState == "Found" or state == "InProgress")
        and state not in ["EveryoneReady", "Error"]
        and playerResponse != "Accepted"
    ):
        logger.warning("Accepting ready check")
        await accept_ready_check(connection)

    await asyncio.sleep(1)


@connector.ws.register("/lol-champ-select/v1/session", event_types=("UPDATE",))
async def subscribe_matchmaking(connection, event):
    # phases = ["PLANNING", "BAN_PICK", "FINALIZATION", "GAME_STARTING"]
    player_cell_id = event.data.get("localPlayerCellId")
    phase = event.data.get("timer").get("phase")

    logger.error(f"Phase: {phase}")

    if phase == "PLANNING":
        for array in event.data.get("actions"):
            for block in array:
                if block.get("actorCellId") == player_cell_id:
                    player_id = block.get("id")
                    await intent_champion(connection, 55, player_cell_id, player_id)

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
                        # while True:
                        #     champ_to_ban = randint(0, 154)
                        #     if randint != 114:
                        #         break
                        champ_to_ban = 35
                        await ban_champion(
                            connection, champ_to_ban, player_cell_id, player_id
                        )

                    if (
                        block.get("type") == "pick"
                        and block.get("completed") != True
                        and block.get("isInProgress") == True
                    ):
                        logger.warning("Pick Champion")
                        await pick_champion(connection, 114, player_cell_id, player_id)

    await asyncio.sleep(1)


async def pick_champion(connection, champion_id, player_cell_id, player_id):
    response = await connection.request(
        "PATCH",
        f"/lol-champ-select/v1/session/actions/{player_id}",
        data={
            "actorCellId": player_cell_id,
            "championId": champion_id,
            "completed": True,
            "isAllyAction": True,
            "type": "pick",
        },
    )
    response = await response.json()
    logger.warning(response)
    logger.error(
        f"Picked champion champion_id: {champion_id}, player_cell_id: {player_cell_id}, player_id: {player_id}"
    )


async def ban_champion(connection, champion_id, player_cell_id, player_id):
    response = await connection.request(
        "PATCH",
        f"/lol-champ-select/v1/session/actions/{player_id}",
        data={
            "actorCellId": player_cell_id,
            "championId": champion_id,
            "completed": True,
            "type": "ban",
        },
    )
    response = await response.json()
    logger.warning(response)
    logger.error(
        f"Banned champion champion_id: {champion_id}, player_cell_id: {player_cell_id}, player_id: {player_id}"
    )


async def intent_champion(connection, champion_id, player_cell_id, player_id):
    response = await connection.request(
        "PATCH",
        f"/lol-champ-select/v1/session/actions/{player_id}",
        data={
            # "cellId": player_cell_id,
            "championPickIntent": champion_id,
        },
    )
    response = await response.json()
    logger.warning(response)
    logger.error(
        f"Intent champion champion_id: {champion_id}, player_cell_id: {player_cell_id}, player_id: {player_id}"
    )


async def get_reported_players(connection):
    response = await connection.request("GET", "/lol-end-of-game/v1/reported-players")
    response = await response.json()
    logger.debug(response)


async def get_player_list(connection):
    response = await connection.request("GET", "/lol-end-of-game/v1/eog-stats-block")
    response = await response.json()
    my_id = response.get("summonerId")
    player_ids = list()

    for team in response.get("teams"):
        for player in team.get("players"):
            player_id = player.get("summonerId")
            if player_id != my_id:
                player_ids.append(player.get("summonerId"))

    return player_ids


async def get_game_id(connection):
    response = await connection.request("GET", "/lol-end-of-game/v1/eog-stats-block")
    response = await response.json()
    game_id = response.get("gameId")
    logger.warning(game_id)
    return game_id


async def report_player(connection, game_id, player_id):
    response = await connection.request(
        "POST",
        "/lol-end-of-game/v2/player-complaints",
        data={
            "gameId": game_id,
            "reportedSummonerId": player_id,
        },
    )
    response = await response.json()
    logger.warning(f"Reported {response.get('reportedSummonerId')}")


async def get_endofgame_celebrations(connection):
    response = await connection.request(
        "GET", "/lol-pre-end-of-game/v1/currentSequenceEvent"
    )
    response = await response.json()
    celebration = response.get("name")
    return celebration


async def skip_mission_celebrations(connection):
    celebration = await get_endofgame_celebrations(connection)
    await connection.request("POST", f"/lol-pre-end-of-game/v1/complete/{celebration}")


async def report_all_players(connection):
    player_ids = await get_player_list(connection)
    game_id = await get_game_id(connection)
    for player_id in player_ids:
        await report_player(connection, game_id, player_id)


@connector.close
async def disconnect(connection):
    logger.info("The client was closed")
    await connector.stop()


@connector.ws.register(
    "/lol-lobby/v2/lobby/session", event_types=("CREATE", "UPDATE", "DELETE")
)
async def lobby_created(connection, event):
    logger.info(f"Recorded new event:")
    logger.debug(f"    Type: {event.type}")
    logger.error(f"    URI: {event.uri}")
    logger.warning(f"    Data: {json.dumps(event.data, indent=4)}")


# DELETE /lol-lobby/v2/lobby = quitter le lobby


# ---------------------------------------------
# main
# ---------------------------------------------
connector.start()
