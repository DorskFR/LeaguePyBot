from .http_connection import HTTPConnection


class HTTPClient:
    def __init__(self):
        self.http = HTTP()

    async def request(self, **kwargs):
        response = await self.http.request(**kwargs)
        if response.status_code in [200, 201, 202, 203, 204, 205, 206]:
            return response
