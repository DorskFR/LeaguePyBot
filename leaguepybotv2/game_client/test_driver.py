from leaguepybotv2.game_client.game_watcher import GameWatcher
import asyncio


async def main():
    watcher = GameWatcher()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
