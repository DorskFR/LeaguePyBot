from leaguepybotv2.bot import LeaguePyBot
import asyncio


async def main():
    bot = LeaguePyBot()
    await bot.client.set_pickban_and_role(
        pick="Fiora", ban="Shaco", first="TOP", second="MIDDLE"
    )
    await bot.client.create_custom_game()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
