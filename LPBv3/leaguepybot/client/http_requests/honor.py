from random import randint

from leaguepybot.client.http_requests.http_request import HTTPRequest
from leaguepybot.common.champions import CHAMPIONS
from leaguepybot.common.logger import get_logger
from leaguepybot.common.models import TeamMember, WebSocketEventResponse
from leaguepybot.common.utils import cast_to_bool, get_key_from_value

logger = get_logger("LPBv3.Honor")


class Honor(HTTPRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def get_command_ballot(self):
        response = await self.request(method="GET", endpoint="/lol-honor-v2/v1/ballot")
        if response:
            return response.data.get("eligiblePLayers")

    async def get_eog_player_list(self):
        response = await self.request(method="GET", endpoint="/lol-end-of-game/v1/eog-stats-block")
        players = []
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
                        kills=player.get("stats").get("CHAMPIONS_KILLED"),
                        gold=player.get("stats").get("GOLD_EARNED"),
                    )
                    players.append(member)
        return players

    async def get_game_id(self):
        response = await self.request(method="GET", endpoint="/lol-end-of-game/v1/eog-stats-block")
        return response.data.get("gameId") if response else None

    async def command_random_player(self):
        players = await self.get_eog_player_list()
        game_id = await self.get_game_id()
        player = players[randint(0, len(players) - 1)]
        await self.command_player(game_id, player)

    async def command_best_player_at_eog(self, event: WebSocketEventResponse):
        if event.data == "PreEndOfGame":
            await self.command_best_player()

    async def command_best_player(self):
        players = await self.get_eog_player_list()
        game_id = await self.get_game_id()
        my_team = [player for player in players if player.isPlayerTeam and not player.isSelf]
        best_player = max(my_team, key=lambda player: player.kills + player.gold / 1000)
        await self.command_player(game_id, best_player)

    async def command_random_player_at_eog(self, event: WebSocketEventResponse):
        if event.data == "PreEndOfGame":
            await self.command_random_player()

    async def command_all_players(self):
        players = await self.get_eog_player_list()
        game_id = await self.get_game_id()
        for player in players:
            if player.isPlayerTeam:
                await self.command_player(game_id, player)

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
