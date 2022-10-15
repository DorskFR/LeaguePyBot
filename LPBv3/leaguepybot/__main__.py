import asyncio
import os
from contextlib import suppress

import sentry_sdk

from leaguepybot.client.client import Client, ClientConfig
from leaguepybot.client.connection.connection import Connection
from leaguepybot.client.connection.http_client import HttpClient
from leaguepybot.client.connection.websocket_client import WebSocketClient
from leaguepybot.client.http_requests.champ_select import ChampSelect
from leaguepybot.client.http_requests.create_game import CreateGame
from leaguepybot.client.http_requests.honor import Honor
from leaguepybot.client.http_requests.hotkeys import Hotkeys
from leaguepybot.client.http_requests.notifications import Notifications
from leaguepybot.client.http_requests.ready_check import ReadyCheck
from leaguepybot.client.http_requests.settings import Settings
from leaguepybot.client.http_requests.summoner import Summoner
from leaguepybot.common.enums import Champion, Role
from leaguepybot.common.logger import get_logger
from leaguepybot.common.tasks import Nursery

logger = get_logger(__name__)
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1,
    environment=os.getenv("ENVIRONMENT", "development"),
)


async def main() -> None:

    async with (
        Connection() as connection,
        HttpClient(connection) as http_client,
        WebSocketClient(connection) as websocket_client,
        Summoner(http_client) as summoner,
        ChampSelect(http_client, summoner) as champ_select,
        CreateGame(http_client, champ_select.role_preference) as create_game,
        Honor(http_client) as honor,
        Hotkeys(http_client) as hotkeys,
        Notifications(http_client) as notifications,
        ReadyCheck(http_client) as ready_check,
        Settings(http_client) as settings,
        Nursery() as nursery,
    ):
        config = ClientConfig(
            picks_per_role={
                Role.TOP: [Champion.FIORA, Champion.GAREN, Champion.DARIUS],
                Role.BOT: [Champion.MISSFORTUNE, Champion.TRISTANA],
                Role.SUP: [Champion.LEONA],
                Role.FILL: [Champion.FIORA],
            },
            bans_per_role={
                Role.TOP: [Champion.SHACO, Champion.MONKEYKING],
                Role.BOT: [Champion.THRESH, Champion.TAHMKENCH],
            },
            first_role=Role.TOP,
            second_role=Role.BOT,
            dismiss_notifications_at_eog=True,
            command_best_player_at_eog=True,
            chain_game_at_eog=True,
            log_everything=True,
        )
        async with Client(
            config=config,
            connection=connection,
            http_client=http_client,
            websocket_client=websocket_client,
            champ_select=champ_select,
            create_game=create_game,
            honor=honor,
            hotkeys=hotkeys,
            notifications=notifications,
            ready_check=ready_check,
            settings=settings,
            summoner=summoner,
            nursery=nursery,
        ) as client:
            await client.run(
                game_sequence=[
                    client.create_game.create_normal_game,
                    client.create_game.start_matchmaking,
                ],
            )


if __name__ == "__main__":
    logger.info("Starting...")
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
    logger.info("Goodbye!...")
