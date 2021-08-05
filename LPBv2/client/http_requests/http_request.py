from ..connection.http_connection import HTTPConnection
from ...common import debug_coro


class HTTPRequest:
    def __init__(self, connection=HTTPConnection(), *args, **kwargs):
        self.http = connection

    @debug_coro
    async def request(self, **kwargs):
        response = await self.http.request(**kwargs)
        if response.status_code in [200, 201, 202, 203, 204, 205, 206]:
            return response
