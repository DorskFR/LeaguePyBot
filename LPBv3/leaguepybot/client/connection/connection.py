from aiohttp import BasicAuth, ClientSession

from leaguepybot.client.connection.lockfile import Lockfile
from leaguepybot.common.models import Runnable


class Connection(Runnable):
    def __init__(self) -> None:
        super().__init__()
        self.lockfile = Lockfile()
        self._session: ClientSession | None = None

    @property
    def url_base(self) -> str:
        return f"127.0.0.1:{self.lockfile.port}"

    def get_session(self) -> ClientSession:
        if not self._session:
            self._session = ClientSession(
                auth=BasicAuth("riot", self.lockfile.auth_key),
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            )
        return self._session

    async def async_stop(self) -> None:
        if self._session:
            await self._session.close()
