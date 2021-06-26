from LPBv2.common import ClientResponse
from typing import List


class MockHTTPConnection:
    def __init__(self):
        self.endpoint: List[str] = list()
        self.data: List[str] = list()

    async def request(self, **kwargs):
        endpoint = kwargs.pop("endpoint")
        data = kwargs.get("payload")

        self.endpoint.append(endpoint)
        self.data.append(data)

        return ClientResponse(endpoint=endpoint, data=data, status_code=200)
