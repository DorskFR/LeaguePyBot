import inspect
from json import JSONDecodeError, loads
from typing import List

from aiohttp import WSMsgType

from leaguepybot.client.connection.connection import Connection
from leaguepybot.common.logger import get_logger
from leaguepybot.common.models import Runnable, WebSocketEvent, WebSocketEventResponse

logger = get_logger("LPBv3.WebSocket")


class WebSocketClient(Runnable):
    def __init__(self, connection: Connection, events: list | None = None):
        super().__init__()
        self._connection = connection
        self.events: List[WebSocketEvent] = events or []

    def register_event(self, event: WebSocketEvent):
        logger.debug(f"Listening to event {event.endpoint}")
        self.events.append(event)

    async def listen_websocket(self):
        logger.debug("Starting websocket listening")
        session = self._connection.get_session()
        websocket = await session.ws_connect(f"wss://{self._connection.url_base}/", ssl=False)
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
            if (
                event.endpoint == data.get("uri")
                or event.endpoint.endswith("/")
                and data.get("uri").startswith(event.endpoint)
            ) and data.get("eventType").upper() in event.type:
                event_response = WebSocketEventResponse(
                    type=data.get("eventType"),
                    uri=data.get("uri"),
                    data=data.get("data"),
                    arguments=event.arguments,
                )
                if (
                    inspect.iscoroutinefunction(event.function)
                    or inspect.iscoroutine(event.function)
                    or inspect.isawaitable(event.function)
                ):
                    await event.function(event=event_response)
                else:
                    event.function(event=event_response)
