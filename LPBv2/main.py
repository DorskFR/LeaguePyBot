from . import LeaguePyBot
import asyncio


async def main():
    bot = LeaguePyBot()

    # client config
    bot.client.champ_select.set_picks_per_role(["Fiora", "Garen"], role="TOP")
    bot.client.champ_select.set_picks_per_role(["Sivir", "Tristana"], role="BOTTOM")
    bot.client.champ_select.set_bans_per_role(["Shaco", "MonkeyKing"], role="TOP")
    bot.client.champ_select.set_bans_per_role(["Thresh", "TahmKench"], role="TOP")
    bot.client.champ_select.set_role_preference(first="TOP", second="BOTTOM")

    # create game
    bot.client.create_game.create_ranked_game()

    # post game sequence
    bot.client.honor.command_all_players()
    bot.client.honor.report_all_players()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
