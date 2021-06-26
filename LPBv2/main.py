from LPBv2.bot import LeaguePyBot
import asyncio


async def main():
    bot = LeaguePyBot()

    # client config
    await bot.client.champ_select.set_picks_per_role(
        picks=["Fiora", "Garen"], role="TOP"
    )
    await bot.client.champ_select.set_picks_per_role(
        picks=["Sivir", "Tristana"], role="BOTTOM"
    )
    await bot.client.champ_select.set_bans_per_role(
        bans=["Shaco", "MonkeyKing"], role="TOP"
    )
    await bot.client.champ_select.set_bans_per_role(
        bans=["Thresh", "TahmKench"], role="BOTTOM"
    )
    await bot.client.champ_select.set_role_preference(first="TOP", second="BOTTOM")

    # create game
    await bot.client.create_game.create_custom_game()

    # post game sequence
    # await bot.client.honor.command_all_players()
    # await bot.client.honor.report_all_players()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
