from LPBv2.bot import LeaguePyBot
from LPBv2.console import Console
from LPBv2.common import debug_coro, cls
import asyncio

@debug_coro
async def main():
    cls()
    bot = LeaguePyBot(autoplay=True)
    console = Console(bot)

    # client config
    cs = bot.client.champ_select
    await cs.set_picks_per_role(picks=["Garen", "Darius"], role="TOP")
    await cs.set_picks_per_role(picks=["MissFortune", "Tristana"], role="BOTTOM")
    await cs.set_bans_per_role(bans=["Shaco", "MonkeyKing"], role="TOP")
    await cs.set_bans_per_role(bans=["Thresh", "TahmKench"], role="BOTTOM")
    await cs.set_role_preference(first="TOP", second="BOTTOM")

    # to log everything (spam!)
    # await bot.client.log_everything()

    # items config (will be automatic someday)
    await bot.build.set_starter_build(build=["1055", "2003", "3340"])
    await bot.build.set_item_build(build=["3074", "3006", "3508", "6692", "3072"])

    # Sample melee build
    # await bot.build.set_starter_build(build=["1055", "2003", "3340"])
    # await bot.build.set_item_build(build=["3074", "3006", "3508", "6692", "3072"])

    # Sample mage build
    # await bot.build.set_starter_build(build=["1082", "2003", "3340"])
    # await bot.build.set_item_build(build=["6653", "3020", "4637", "3089"])

    # Sample ADC build
    # await bot.build.set_starter_build(build=["3070", "2003", "3340"])
    # await bot.build.set_item_build(build=["6632", "3158", "3004", "3110", "6694", "3074"])

    # create game functions
    cg = bot.client.create_game

    # register these functions to run at End of Game
    await bot.client.dismiss_notifications_at_eog()
    await bot.client.command_best_player_at_eog()
    await bot.client.chain_game_at_eog(
        coros=[cg.create_custom_game, cg.fill_with_bots, cg.start_champ_selection]
    )

    # custom game
    await cg.create_custom_game()
    await cg.fill_with_bots()
    await cg.start_champ_selection()

    # ranked game
    # await cg.create_ranked_game()
    # await cg.select_lane_position()
    # await cg.start_matchmaking()

    # coop game
    # await cg.create_coop_game()
    # await cg.start_matchmaking()

    # normal game
    # await cg.create_normal_game()
    # await cg.start_matchmaking()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(main())
        loop.run_forever()
    finally:
        loop.close()
