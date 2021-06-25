import asyncio
import time

import cv2

from leaguepybotv2.bot import LeaguePyBot
from leaguepybotv2.console import Console
from leaguepybotv2.logger import get_logger

logger = get_logger("LPBv2.Bot")


async def show_screen_and_minimap(bot: LeaguePyBot):
    while True:
        if (
            bot.game.game_flow.is_ingame
            and bot.minimap.sct_original is not None
            and bot.screen.sct_original is not None
        ):
            await show_screen(bot.screen.sct_original)
            await show_minimap(bot.minimap.sct_original)

        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            cv2.destroyAllWindows()
            break


async def show_screen(img):
    cv2.namedWindow("Screen")
    cv2.moveWindow("Screen", -2560, 0)
    cv2.imshow("Screen", img)


async def show_minimap(img):
    cv2.namedWindow("Minimap", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Minimap", -560, 0)
    cv2.resizeWindow("Minimap", 420, 420)
    cv2.imshow("Minimap", img)


async def main():
    time.sleep(3)
    bot = LeaguePyBot()
    console = Console(bot=bot)
    await bot.client.champ_selector.set_bans_per_role(
        bans=["Shaco", "MonkeyKing"], role="TOP"
    )
    await bot.client.champ_selector.set_picks_per_role(
        picks=["Fiora", "Garen"], role="TOP"
    )
    await bot.client.champ_selector.set_role_preference(first="TOP", second="MIDDLE")

    # set picks per role
    # await bot.client.set_picks_per_role(picks=["Fiora", "Garen", "Nasus"], role="TOP")
    # await bot.client.set_picks_per_role(picks=["Sivir", "Tristana"], role="BOTTOM")
    # await bot.client.set_role_preference(first="BOT", second="TOP")

    # await bot.client.report_all_players()
    await bot.client.create_ranked_game()
    # await bot.client.create_coop_game()
    # await show_screen_and_minimap(bot)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
