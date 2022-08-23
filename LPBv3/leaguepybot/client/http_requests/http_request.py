from leaguepybot.client.connection.http_connection import HTTPConnection


class HTTPRequest:
    def __init__(self, *args, **kwargs):
        self.http = HTTPConnection.get_instance()

    async def request(self, **kwargs):
        response = await self.http.request(**kwargs)
        if response.status_code in [200, 201, 202, 203, 204, 205, 206]:
            return response
