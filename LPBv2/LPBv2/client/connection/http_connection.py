from .connection import Connection
from aiohttp import ClientSession, BasicAuth
from json import dumps
from ...common import ClientResponse, debug_coro
from ...logger import get_logger

logger = get_logger("LPBv2.HTTPConnection")


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

    @debug_coro
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
                return ClientResponse(
                    endpoint=endpoint, data=data, status_code=response.status
                )
            except Exception as e:
                logger.error(e)

    def make_url(self, endpoint):
        return f"https://127.0.0.1:{self.lockfile.port}{endpoint}"
