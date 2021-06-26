from .http_requests import *
from .connection import *
from ..common import WebsocketEvent, LoopInNewThread
from ..logger import get_logger, Colors
from json import dumps

logger = get_logger("LPBv2.Client")


class Client:
    def __init__(self):
        self.http = HTTPConnection()
        self.websocket = WebSocket()
        self.create_game = CreateGame()
        self.champ_select = ChampSelect()
        self.honor = Honor()
        self.notifications = Notifications()
        self.ready_check = ReadyCheck()
        self.game_flow_phase: str = "None"
        self.loop = LoopInNewThread()
        self.loop.submit_async(self.start_websocket())

    async def start_websocket(self):
        await self.websocket.register_event(
            WebsocketEvent(
                endpoint="/lol-gameflow/v1/gameflow-phase",
                type=["CREATE", "UPDATE", "DELETE"],
                function=self.game_flow_update,
            ),
        )
        await self.websocket.register_event(
            WebsocketEvent(
                endpoint="/lol-matchmaking/v1/search",
                type=["CREATE", "UPDATE", "DELETE"],
                function=self.ready_check.accept,
            )
        )
        await self.websocket.register_event(
            WebsocketEvent(
                endpoint="/lol-champ-select/v1/session",
                type=["UPDATE"],
                function=self.champ_select.update,
            ),
        )
        await self.websocket.register_event(
            WebsocketEvent(
                endpoint="/",
                type=["CREATE", "UPDATE", "DELETE"],
                function=self.loop_back_log,
            )
        )
        await self.websocket.listen_websocket()

    async def game_flow_update(self, event):
        self.game_flow_phase = event.data

    async def loop_back_log(self, event):
        logger.warning(event.uri)
        logger.info(event.type)
        logger.debug(f"{dumps(event.data, indent=4)}\n\n")
