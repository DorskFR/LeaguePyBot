from asyncio import create_task
from json import JSONDecodeError, loads
from typing import List

from aiohttp import BasicAuth, ClientSession, WSMsgType

from ...common import WebSocketEvent, WebSocketEventResponse, debug_coro
from ...logger import get_logger, Colors
from .connection import Connection

logger = get_logger("LPBv2.WebSocket")


class WebSocket(Connection):
    def __init__(self, events=list()):
        super().__init__()
        self.events: List[WebSocketEvent] = events

    @debug_coro
    async def register_event(self, event: WebSocketEvent):
        logger.info(f"Listening to event {Colors.cyan}{event.endpoint}{Colors.reset}")
        self.events.append(event)

    @debug_coro
    async def listen_websocket(self):
        logger.info("Starting websocket listening")
        async with ClientSession(
            auth=BasicAuth("riot", self.lockfile.auth_key),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
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

    @debug_coro
    async def match_websocket(self, data):
        for event in self.events:
            if event.endpoint == data.get("uri") or (
                event.endpoint.endswith("/")
                and data.get("uri").startswith(event.endpoint)
            ):
                if data.get("eventType").upper() in event.type:
                    event_response = WebSocketEventResponse(
                        type=data.get("eventType"),
                        uri=data.get("uri"),
                        data=data.get("data"),
                        arguments=event.arguments,
                    )
                    try:
                        create_task(event.function(event=event_response))
                    except Exception as e:
                        logger.warning(e)
