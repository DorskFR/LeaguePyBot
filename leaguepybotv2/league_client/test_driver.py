from leaguepybotv2.league_client import LeagueClient
from leaguepybotv2.logger import get_logger
import asyncio

logger = get_logger()


async def main():
    client = LeagueClient()
    await client.set_pickban_and_role(
        pick="Fiora", ban="Shaco", first="TOP", second="MIDDLE"
    )

    # await client.log_everything()

    # await client.create_custom_game()
    # await client.create_normal_game()
    await client.create_ranked_game()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
