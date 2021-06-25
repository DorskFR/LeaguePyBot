from .http_client import HTTPClient


class Honor(HTTPClient):
    def __init__(self):
        super().__init__()

    async def get_command_ballot(self):
        response = await self.request(method="GET", endpoint="/lol-honor-v2/v1/ballot")
        if response:
            logger.info(response.data.get("eligiblePLayers"))

    async def command_random_player(self):
        players = await self.get_eog_player_list()
        game_id = await self.get_game_id()
        player = players[randint(0, len(players))]
        await self.command_player(game_id, player)

    async def command_all_players(self):
        await self.get_command_ballot()
        players = await self.get_eog_player_list()
        game_id = await self.get_game_id()
        for player in players:
            if player.get("isPlayerTeam"):
                await self.command_player(game_id, player)
                await asyncio.sleep(1)

    async def command_player(self, game_id, player):
        response = await self.request(
            method="POST",
            endpoint="/lol-honor-v2/v1/honor-player",
            payload={
                "gameId": game_id,
                "honorCategory": "HEART",
                "summonerId": player.summonerId,
            },
        )
        if response:
            logger.warning(f"Commanded {player.summonerName} ({player.championName})")

    async def report_all_players(self):
        players = await self.get_eog_player_list()
        game_id = await self.get_game_id()
        for player in players:
            if not player.isSelf:
                await self.report_player(game_id, player)
                await asyncio.sleep(0.1)

    async def report_player(self, game_id, player):
        response = await self.request(
            method="POST",
            endpoint="/lol-end-of-game/v2/player-complaints",
            payload={
                "gameId": game_id,
                "reportedSummonerId": player.summonerId,
            },
        )
        if response:
            logger.warning(f"Reported {player.summonerName} ({player.championName})")

    async def get_eog_player_list(self):
        response = await self.request(
            method="GET", endpoint="/lol-end-of-game/v1/eog-stats-block"
        )
        players = list()
        if response:
            my_id = response.data.get("summonerId")
            for team in response.data.get("teams"):
                for player in team.get("players"):
                    member = TeamMember(
                        summonerId=player.get("summonerId"),
                        summonerName=player.get("summonerName"),
                        championId=player.get("championId"),
                        championName=get_key_from_value(
                            CHAMPIONS, player.get("championId")
                        ).capitalize(),
                        isPlayerTeam=cast_to_bool(team.get("isPlayerTeam")),
                        isSelf=player.get("summonerId") == my_id,
                    )
                    players.append(member)
        return players

    async def get_game_id(self):
        response = await self.request(
            method="GET", endpoint="/lol-end-of-game/v1/eog-stats-block"
        )
        game_id = None
        if response:
            game_id = response.data.get("gameId")
        return game_id
