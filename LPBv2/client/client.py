from .http_requests import *
from .connection import *
from ..common import WebSocketEvent, LoopInNewThread, debug_coro
from ..logger import get_logger
from json import dumps

logger = get_logger("LPBv2.Client")


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
        self.game_flow_phase: str = "None"
        self.loop = LoopInNewThread()
        self.loop.submit_async(self.start_websocket())
        self.region: str = None
        self.locale: str = None
        self.loop.submit_async(self.get_region_and_locale())
        self.loop.submit_async(self.settings.patch_settings())
        self.loop.submit_async(self.hotkeys.load_hotkeys())
        self.loop.submit_async(self.hotkeys.patch_hotkeys())

    @debug_coro
    async def start_websocket(self):
        await self.websocket.register_event(
            WebSocketEvent(
                endpoint="/lol-gameflow/v1/gameflow-phase",
                type=["CREATE", "UPDATE", "DELETE"],
                function=self.game_flow_update,
            ),
        )
        await self.websocket.register_event(
            WebSocketEvent(
                endpoint="/lol-matchmaking/v1/search",
                type=["CREATE", "UPDATE"],
                function=self.ready_check.accept,
            )  # /lol-lobby/v2/lobby/matchmaking/search-state
        )
        await self.websocket.register_event(
            WebSocketEvent(
                endpoint="/lol-champ-select/v1/session",
                type=["UPDATE"],
                function=self.champ_select.update,
            ),
        )

        await self.websocket.listen_websocket()

    @debug_coro
    async def game_flow_update(self, event):
        self.game_flow_phase = event.data

    @debug_coro
    async def log_everything(self, endpoint="/"):
        await self.websocket.register_event(
            WebSocketEvent(
                endpoint=endpoint,
                type=["CREATE", "UPDATE", "DELETE"],
                function=self.loop_back_log,
            )
        )

    @debug_coro
    async def command_random_player_at_eog(self):
        await self.websocket.register_event(
            WebSocketEvent(
                endpoint="/lol-gameflow/v1/gameflow-phase",
                type=["UPDATE"],
                function=self.honor.command_random_player_at_eog,
            )
        )

    @debug_coro
    async def chain_game_at_eog(self, *args, **kwargs):
        await self.websocket.register_event(
            WebSocketEvent(
                endpoint="/lol-gameflow/v1/gameflow-phase",
                type=["UPDATE"],
                function=self.create_game.chain_game_at_eog,
                arguments=args
            )
        )

    @debug_coro
    async def dismiss_notifications_at_eog(self, *args, **kwargs):
        await self.websocket.register_event(
            WebSocketEvent(
                endpoint="/lol-gameflow/v1/gameflow-phase",
                type=["UPDATE"],
                function=self.notifications.dismiss_notifications_at_eog,
                arguments=args
            )
        )

    @debug_coro
    async def loop_back_log(self, event):
        logger.warning(event.uri)
        logger.info(event.type)
        logger.debug(f"{dumps(event.data, indent=4)}\n\n")

    @debug_coro
    async def get_region_and_locale(self):
        resp = await self.http.request(
            method="GET", endpoint="/riotclient/get_region_locale"
        )
        self.locale = resp.data.get("locale")
        self.region = resp.data.get("region").lower()
