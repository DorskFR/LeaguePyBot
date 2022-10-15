from leaguepybot.client.connection.http_client import HttpClient
from leaguepybot.common.logger import get_logger
from leaguepybot.common.models import Runnable

logger = get_logger("LPBv3.ReadyCheck")


class ReadyCheck(Runnable):
    def __init__(self, http_client: HttpClient):
        super().__init__()
        self._http_client = http_client

    async def accept(self, event):
        searchState = event.data.get("searchState")
        playerResponse = event.data.get("readyCheck").get("playerResponse")
        state = event.data.get("readyCheck").get("state")
        if (
            (searchState == "Found" or state == "InProgress")
            and state not in ["EveryoneReady", "Error"]
            and playerResponse != "Accepted"
        ):
            response = await self._http_client.request(
                method="POST",
                endpoint="/lol-matchmaking/v1/ready-check/accept",
            )
            if response:
                logger.warning("Match found: Accepted ready check")
