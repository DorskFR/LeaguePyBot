from .http_requests import *
from .connection import *
from ..common import WebsocketEvent


class Client:
    def __init__(self):
        self.http = HTTPConnection()
        self.websocket = WebSocket()
        self.create_game = CreateGame()
        self.champ_select = ChampSelect()
        self.honor = Honor()
        self.notifications = Notifications()
        self.ready_check = ReadyCheck()

    async def init(self):
        self.websocket.register_event(
            WebsocketEvent(
                endpoint="/lol-gameflow/v1/gameflow-phase",
                type=["CREATE", "UPDATE", "DELETE"],
                function=self.game_flow.update,
            ),
        )
        self.websocket.register_event(
            WebsocketEvent(
                endpoint="/lol-matchmaking/v1/search",
                type=["CREATE", "UPDATE", "DELETE"],
                function=self.ready_check.accept,
            )
        )
        self.websocket.register_event(
            WebsocketEvent(
                endpoint="/lol-champ-select/v1/session",
                type=["UPDATE"],
                function=self.champ_select.update,
            ),
        )
