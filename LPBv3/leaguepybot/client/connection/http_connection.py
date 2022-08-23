from json import dumps

from aiohttp import BasicAuth, ClientSession

from leaguepybot.client.connection.connection import Connection
from leaguepybot.common.logger import get_logger
from leaguepybot.common.models import ClientResponse

logger = get_logger("LPBv3.HTTPConnection")


class HTTPConnection(Connection):
    __instance = None

    @staticmethod
    def get_instance():
        if HTTPConnection.__instance is None:
            HTTPConnection()
        return HTTPConnection.__instance

    def __init__(self):
        if HTTPConnection.__instance is not None:
            raise Exception("This class is a Singleton")
        else:
            HTTPConnection.__instance = self
        super().__init__()

    async def request(self, **kwargs):
        async with ClientSession(
            auth=BasicAuth("riot", self.lockfile.auth_key),
            headers=self.headers,
        ) as session:
            endpoint = kwargs.pop("endpoint")
            params = {
                "method": kwargs.pop("method"),
                "url": self.make_url(endpoint),
            }
            if kwargs.get("payload"):
                params["data"] = dumps(kwargs.pop("payload"))
            try:
                response = await session.request(**params, ssl=False)
                data = await response.json()
                return ClientResponse(endpoint=endpoint, data=data, status_code=response.status)
            except Exception as e:
                logger.error(e)

    def make_url(self, endpoint):
        return f"https://127.0.0.1:{self.lockfile.port}{endpoint}"
