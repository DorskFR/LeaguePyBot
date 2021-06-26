from ..connection.http_connection import HTTPConnection


class HTTPRequest:
    def __init__(self, connection=HTTPConnection()):
        self.http = connection

    async def request(self, **kwargs):
        response = await self.http.request(**kwargs)
        if response.status_code in [200, 201, 202, 203, 204, 205, 206]:
            return response
