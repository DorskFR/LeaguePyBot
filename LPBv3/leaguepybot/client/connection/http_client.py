from typing import Any

from aiohttp.client_exceptions import ClientResponseError

from leaguepybot.client.connection.connection import Connection
from leaguepybot.common.logger import get_logger
from leaguepybot.common.models import ClientApiResponse, Runnable

logger = get_logger("LPBv3.HTTPConnection")


class HttpClient(Runnable):
    def __init__(self, connection: Connection) -> None:
        super().__init__()
        self._connection = connection

    async def request(
        self, method: str, endpoint: str, payload: dict[str, Any] | None = None
    ) -> ClientApiResponse:
        session = self._connection.get_session()
        try:
            response = await session.request(
                method=method,
                url=f"https://{self._connection.url_base}{endpoint}",
                json=payload,
                ssl=False,
            )
            response.raise_for_status()
            data = await response.json()
            #  [200, 201, 202, 203, 204, 205, 206]
            return ClientApiResponse(endpoint=endpoint, data=data, status_code=response.status)
        except (ValueError, ClientResponseError) as error:
            logger.error(error)
            return ClientApiResponse(endpoint=endpoint, data={}, status_code=response.status)
