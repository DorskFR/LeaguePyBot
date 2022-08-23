import asyncio
from json import dumps

from leaguepybot.client.connection.http_connection import HTTPConnection
from leaguepybot.client.connection.websocket import WebSocket
from leaguepybot.client.http_requests.champ_select import ChampSelect
from leaguepybot.client.http_requests.create_game import CreateGame
from leaguepybot.client.http_requests.honor import Honor
from leaguepybot.client.http_requests.hotkeys import Hotkeys
from leaguepybot.client.http_requests.notifications import Notifications
from leaguepybot.client.http_requests.ready_check import ReadyCheck
from leaguepybot.client.http_requests.settings import Settings
from leaguepybot.client.http_requests.summoner import Summoner
from leaguepybot.common.logger import get_logger
from leaguepybot.common.models import WebSocketEvent

logger = get_logger("LPBv3.Client")


class Client:
    def __init__(self):
        self.http = HTTPConnection()
        self.websocket = WebSocket()
        self.champ_select = ChampSelect()
        self.create_game = CreateGame(role=self.champ_select.role)
        self.honor = Honor()
        self.notifications = Notifications()
        self.ready_check = ReadyCheck()
        self.settings = Settings()
        self.hotkeys = Hotkeys()
        self.summoner = Summoner()
        self.game_flow_phase: str = "None"
        self.region: str = None
        self.locale: str = None

    async def run(self) -> None:
        self.start_websocket()
        await self.hotkeys.start()
        await self.get_region_and_locale()

    def start_websocket(self):
        self.websocket.register_event(
            WebSocketEvent(
                endpoint="/lol-gameflow/v1/gameflow-phase",
                type=["CREATE", "UPDATE", "DELETE"],
                function=self.game_flow_update,
            ),
        )
        self.websocket.register_event(
            WebSocketEvent(
                endpoint="/lol-matchmaking/v1/search",
                type=["CREATE", "UPDATE"],
                function=self.ready_check.accept,
            )  # /lol-lobby/v2/lobby/matchmaking/search-state
        )
        self.websocket.register_event(
            WebSocketEvent(
                endpoint="/lol-champ-select/v1/session",
                type=["UPDATE"],
                function=self.champ_select.update,
            ),
        )
        asyncio.create_task(self.websocket.listen_websocket())

    def game_flow_update(self, event):
        self.game_flow_phase = event.data

    def log_everything(self, endpoint="/"):
        self.websocket.register_event(
            WebSocketEvent(
                endpoint=endpoint,
                type=["CREATE", "UPDATE", "DELETE"],
                function=self.loop_back_log,
            )
        )

    def command_best_player_at_eog(self):
        self.websocket.register_event(
            WebSocketEvent(
                endpoint="/lol-gameflow/v1/gameflow-phase",
                type=["UPDATE"],
                function=self.honor.command_best_player_at_eog,
            )
        )

    def chain_game_at_eog(self, *args, **kwargs):
        self.websocket.register_event(
            WebSocketEvent(
                endpoint="/lol-gameflow/v1/gameflow-phase",
                type=["UPDATE"],
                function=self.create_game.chain_game_at_eog,
                arguments=kwargs.get("coros"),
            )
        )

    def dismiss_notifications_at_eog(self, *args, **kwargs):
        self.websocket.register_event(
            WebSocketEvent(
                endpoint="/lol-gameflow/v1/gameflow-phase",
                type=["UPDATE"],
                function=self.notifications.dismiss_notifications_at_eog,
            )
        )

    def loop_back_log(self, event):
        logger.debug(event.uri)
        logger.debug(event.type)
        logger.debug(f"{dumps(event.data, indent=4)}\n\n")

    async def get_region_and_locale(self):
        resp = await self.http.request(method="GET", endpoint="/riotclient/get_region_locale")
        self.locale = resp.data.get("locale")
        self.region = resp.data.get("region").lower()
