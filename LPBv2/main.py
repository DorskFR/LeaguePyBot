from LPBv2.bot import LeaguePyBot
from LPBv2.console import Console
import asyncio
import cv2


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
    bot = LeaguePyBot()
    console = Console(bot)

    # client config
    cs = bot.client.champ_select
    await cs.set_picks_per_role(picks=["Fiora", "Garen"], role="TOP")
    await cs.set_picks_per_role(picks=["MissFortune", "Tristana"], role="BOTTOM")
    await cs.set_bans_per_role(bans=["Shaco", "MonkeyKing"], role="TOP")
    await cs.set_bans_per_role(bans=["Thresh", "TahmKench"], role="BOTTOM")
    await cs.set_role_preference(first="TOP", second="BOTTOM")

    await bot.client.honor.report_all_players()

    # create game
    cg = bot.client.create_game

    # await cg.create_ranked_game()
    # await cg.select_lane_position()
    # await cg.start_matchmaking()

    await cg.create_custom_game()
    await cg.fill_with_bots(team="ORDER")
    await cg.fill_with_bots()
    await cg.start_champ_selection()

    # vision
    # await show_screen_and_minimap(bot)

    # post game sequence
    # await bot.client.honor.command_all_players()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
