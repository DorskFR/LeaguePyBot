import asyncio
import os
from contextlib import suppress

import sentry_sdk

from leaguepybot.client.client import Client
from leaguepybot.common.enums import Champion, Role
from leaguepybot.common.logger import get_logger

logger = get_logger(__name__)
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1,
    environment=os.getenv("ENVIRONMENT", "development"),
)


async def main() -> None:
    client = Client()

    # options are all sync methods
    client.champ_select.set_picks_per_role(
        picks=[Champion.FIORA, Champion.GAREN, Champion.DARIUS], role=Role.TOP
    )
    client.champ_select.set_picks_per_role(
        picks=[Champion.MISSFORTUNE, Champion.TRISTANA], role=Role.BOTTOM
    )
    client.champ_select.set_picks_per_role(picks=[Champion.LEONA], role=Role.UTILITY)
    client.champ_select.set_bans_per_role(bans=[Champion.SHACO, Champion.MONKEYKING], role=Role.TOP)
    client.champ_select.set_bans_per_role(
        bans=[Champion.THRESH, Champion.TAHMKENCH], role=Role.BOTTOM
    )
    client.champ_select.set_role_preference(first=Role.TOP, second=Role.BOTTOM)
    client.dismiss_notifications_at_eog()
    client.command_best_player_at_eog()
    client.chain_game_at_eog(
        coros=[
            client.create_game.create_normal_game,
            client.create_game.start_matchmaking,
        ]
    )

    await client.run()
    await client.create_game.create_normal_game()
    await client.create_game.start_matchmaking()

    while True:
        await asyncio.sleep(0)


if __name__ == "__main__":
    logger.info("Starting...")
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
    logger.info("Goodbye!...")
