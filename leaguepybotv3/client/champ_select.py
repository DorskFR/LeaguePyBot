from .http_client import HTTPClient


class ChampSelect(HTTPClient):
    def __init__(self):
        super().__init__()

    def intent(self):
        pass

    async def pick_champion(self, champion_id, player_cell_id, player_id):
        response = await self.request(
            method="PATCH",
            endpoint=f"/lol-champ-select/v1/session/actions/{player_id}",
            payload={
                "actorCellId": player_cell_id,
                "championId": champion_id,
                "completed": True,
                "isAllyAction": True,
                "type": "pick",
            },
        )
        if response:
            logger.warning(
                f"Picked champion champion_id: {Colors.cyan}{champion_id}{Colors.reset}, player_cell_id: {Colors.dark_grey}{player_cell_id}{Colors.reset}, player_id: {Colors.dark_grey}{player_id}{Colors.reset}"
            )

    async def ban_champion(self, champion_id, player_cell_id, player_id):
        response = await self.request(
            method="PATCH",
            endpoint=f"/lol-champ-select/v1/session/actions/{player_id}",
            payload={
                "actorCellId": player_cell_id,
                "championId": champion_id,
                "completed": True,
                "type": "ban",
            },
        )
        if response:
            logger.warning(
                f"Banned champion champion_id: {Colors.red}{champion_id}{Colors.reset}, player_cell_id: {Colors.dark_grey}{player_cell_id}{Colors.reset}, player_id: {Colors.dark_grey}{player_id}{Colors.reset}"
            )
