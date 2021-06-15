from leaguepybotv2.league_client import LeagueClient
from leaguepybotv2.logger import get_logger
import asyncio

logger = get_logger()


async def main():
    client = LeagueClient()
    await client.command_myself()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
