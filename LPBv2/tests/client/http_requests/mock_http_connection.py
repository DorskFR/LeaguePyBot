from LPBv2.common import ClientResponse
from typing import List
from .mock_eog_stats_block import eog_stats


class TeamFullException(Exception):
    pass


class MockHTTPConnection:
    def __init__(self, *args, **kwargs):
        self.endpoint: List[str] = list()
        self.data: List[str] = list()

    async def request(self, **kwargs):
        endpoint = kwargs.pop("endpoint")
        data = kwargs.get("payload")

        if len(self.endpoint) + 1 > 5 and endpoint == "/lol-lobby/v1/lobby/custom/bots":
            raise TeamFullException

        self.endpoint.append(endpoint)
        self.data.append(data)

        if endpoint == "/lol-honor-v2/v1/ballot":
            data = {"eligiblePLayers": ["Luke", "Leia", "Lando", "Chewbacca", "C3PO"]}

        if endpoint == "/lol-end-of-game/v1/eog-stats-block":
            data = eog_stats

        return ClientResponse(endpoint=endpoint, data=data, status_code=200)
