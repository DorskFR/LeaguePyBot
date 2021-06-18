import asyncio

from leaguepybotv2.bot import LeaguePyBot
from leaguepybotv2.logger import get_logger

logger = get_logger("LPBv2.Bot")


async def main():
    bot = LeaguePyBot()
    await bot.client.set_pickban_and_role(
        pick="Fiora", ban="Shaco", first="TOP", second="MIDDLE"
    )
    # await bot.client.log_everything("/lol-lobby/v2/lobby")
    await bot.client.create_custom_game()

    # while True:
    #     try:
    #         cv2.imshow("Minimap", bot.vision.sct_original)
    #     except:
    #         continue


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
