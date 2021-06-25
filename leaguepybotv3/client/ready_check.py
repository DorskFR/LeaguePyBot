from .http_client import HTTPClient


class ReadyCheck(HTTPClient):
    def __init__(self):
        super().__init__()

    async def accept(self, event, *args, **kwargs):
        searchState = event.data.get("searchState")
        playerResponse = event.data.get("readyCheck").get("playerResponse")
        state = event.data.get("readyCheck").get("state")
        if (
            (searchState == "Found" or state == "InProgress")
            and state not in ["EveryoneReady", "Error"]
            and playerResponse != "Accepted"
        ):
            response = await self.request(
                method="POST",
                endpoint="/lol-matchmaking/v1/ready-check/accept",
            )
            if response:
                logger.warning("Match found: Accepted ready check")
