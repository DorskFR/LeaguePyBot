from LPBv2.common import ClientResponse
from typing import List


class TeamFullException(Exception):
    pass


class MockHTTPConnection:
    def __init__(self, *args, **kwargs):
        self.endpoint: List[str] = list()
        self.data: List[str] = list()

    async def request(self, **kwargs):
        endpoint = kwargs.pop("endpoint")
        data = kwargs.get("payload")

        if len(self.endpoint) + 1 > 5:
            raise TeamFullException

        self.endpoint.append(endpoint)
        self.data.append(data)

        return ClientResponse(endpoint=endpoint, data=data, status_code=200)
