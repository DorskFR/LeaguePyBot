from aiohttp import ClientSession, BasicAuth, WSMsgType
from .models import ClientResponse
from json import dumps, loads, JSONDecodeError
from .league_lockfile import Lockfile
from typing import List
from .models import WebsocketEvent, WebsocketEventResponse
from asyncio import create_task
from leaguepybotv2.logger import get_logger

logger = get_logger("LPBv2.Connector")


class LeagueConnector:
    def __init__(self, parent=None, *args, **kwargs):
        self.client = parent
        self.lockfile = Lockfile()
        self.events: List[WebsocketEvent] = kwargs.get("events") or list()
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def request(self, *args, **kwargs):
        async with ClientSession(
            auth=BasicAuth("riot", self.lockfile.auth_key),
            headers=self.headers,
        ) as session:
            params = {
                "method": kwargs.pop("method"),
                "url": self.make_url(kwargs.pop("endpoint")),
            }
            if kwargs.get("payload"):
                params["data"] = dumps(kwargs.pop("payload"))
            try:
                response = await session.request(**params, ssl=False)
                data = await response.json()
                return ClientResponse(data=data, status_code=response.status)
            except Exception as e:
                logger.error(e)

    def make_url(self, endpoint):
        return f"https://127.0.0.1:{self.lockfile.port}{endpoint}"

    async def register_event(self, event: WebsocketEvent):
        logger.debug(f"Adding event {event}")
        self.events.append(event)

    async def listen_websocket(self):
        async with ClientSession(
            auth=BasicAuth("riot", self.lockfile.auth_key),
            headers=self.headers,
        ) as session:
            websocket = await session.ws_connect(
                f"wss://127.0.0.1:{self.lockfile.port}/", ssl=False
            )
            await websocket.send_json([5, "OnJsonApiEvent"])
            _ = await websocket.receive()
            while True:
                msg = await websocket.receive()

                if msg.type == WSMsgType.TEXT:
                    try:
                        data = loads(msg.data)[2]
                        await self.match_websocket(data)
                    except JSONDecodeError:
                        logger.error(f"Error decoding the following JSON: {msg.data}")

                elif msg.type == WSMsgType.CLOSED:
                    break

    async def match_websocket(self, data):
        for event in self.events:
            if event.endpoint == data.get("uri") or (
                event.endpoint.endswith("/")
                and data.get("uri").startswith(event.endpoint)
            ):
                if data.get("eventType").upper() in event.type:
                    event_response = WebsocketEventResponse(
                        type=data.get("eventType"),
                        uri=data.get("uri"),
                        data=data.get("data"),
                    )
                    # First we try calling a method of the class instance if existing
                    try:
                        create_task(
                            self.client.__getattribute__(str(event.function.__name__))(
                                event=event_response
                            )
                        )
                    # If not existing (external function), we try calling the function directly
                    except:
                        try:
                            create_task(event.function(event=event_response))
                        except Exception as e:
                            logger.warning(e)
