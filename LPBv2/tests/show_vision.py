import cv2
from LPBv2.common import debug_coro

@debug_coro
async def show_screen_and_minimap(bot):
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


@debug_coro
async def show_screen(img):
    cv2.namedWindow("Screen")
    # cv2.moveWindow("Screen", -2560, 0)
    cv2.imshow("Screen", img)


@debug_coro
async def show_minimap(img):
    cv2.namedWindow("Minimap", cv2.WINDOW_NORMAL)
    # cv2.moveWindow("Minimap", -560, 0)
    cv2.resizeWindow("Minimap", 420, 420)
    cv2.imshow("Minimap", img)
