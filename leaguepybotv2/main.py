from .bot import LeaguePyBot
import asyncio


async def main():
    bot = LeaguePyBot()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
