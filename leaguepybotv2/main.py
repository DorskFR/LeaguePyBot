import asyncio

import cv2

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

    while True:
        if bot.screen.sct_original is not None:
            cv2.imshow("Screen", bot.screen.sct_original)

            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
