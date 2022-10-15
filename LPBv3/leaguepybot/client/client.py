from collections.abc import Awaitable
from dataclasses import dataclass
from typing import Callable

from leaguepybot.client.connection.connection import Connection
from leaguepybot.client.connection.http_client import HttpClient
from leaguepybot.client.connection.websocket_client import WebSocketClient
from leaguepybot.client.http_requests.champ_select import ChampSelect
from leaguepybot.client.http_requests.create_game import CreateGame
from leaguepybot.client.http_requests.honor import Honor
from leaguepybot.client.http_requests.hotkeys import Hotkeys
from leaguepybot.client.http_requests.notifications import Notifications
from leaguepybot.client.http_requests.ready_check import ReadyCheck
from leaguepybot.client.http_requests.settings import Settings
from leaguepybot.client.http_requests.summoner import Summoner
from leaguepybot.common.enums import Champion, Role
from leaguepybot.common.logger import get_logger
from leaguepybot.common.models import Runnable, WebSocketEvent
from leaguepybot.common.tasks import Nursery

logger = get_logger("LPBv3.Client", log_to_file=True)


@dataclass
class ClientConfig:
    picks_per_role: dict[Role, list[Champion]] | None = None
    bans_per_role: dict[Role, list[Champion]] | None = None
    first_role: Role | None = None
    second_role: Role | None = None
    dismiss_notifications_at_eog: bool = False
    command_best_player_at_eog: bool = False
    command_random_player_at_eog: bool = False
    chain_game_at_eog: bool = False
    log_everything: bool = False


class Client(Runnable):
    def __init__(
        self,
        config: ClientConfig | None = None,
        connection: Connection | None = None,
        http_client: HttpClient | None = None,
        websocket_client: WebSocketClient | None = None,
        champ_select: ChampSelect | None = None,
        create_game: CreateGame | None = None,
        honor: Honor | None = None,
        hotkeys: Hotkeys | None = None,
        notifications: Notifications | None = None,
        ready_check: ReadyCheck | None = None,
        settings: Settings | None = None,
        summoner: Summoner | None = None,
        nursery: Nursery | None = None,
    ):
        super().__init__()
        self.config = config or ClientConfig()
        self.connection = connection or Connection()
        self.http_client = http_client or HttpClient(self.connection)
        self.websocket_client = websocket_client or WebSocketClient(self.connection)
        self.summoner = summoner or Summoner(self.http_client)
        self.champ_select = champ_select or ChampSelect(self.http_client, self.summoner)
        self.create_game = create_game or CreateGame(
            self.http_client, role_preference=self.champ_select.role_preference
        )
        self.honor = honor or Honor(self.http_client)
        self.hotkeys = hotkeys or Hotkeys(self.http_client)
        self.notifications = notifications or Notifications(self.http_client)
        self.ready_check = ready_check or ReadyCheck(self.http_client)
        self.settings = settings or Settings(self.http_client)
        self.nursery = nursery or Nursery()

        self._game_sequence: list[Callable] = []
        self.game_flow_phase: str = "None"
        self.region: str = ""
        self.locale: str = ""

    async def run(self, game_sequence: list[Callable]) -> None:
        self._game_sequence = game_sequence
        self.start()
        self.start_websocket()
        await self.hotkeys.run()
        await self.get_region_and_locale()

        if self.config.picks_per_role:
            self.champ_select.set_picks_per_role(self.config.picks_per_role)
        if self.config.bans_per_role:
            self.champ_select.set_bans_per_role(self.config.bans_per_role)
        if self.config.first_role and self.config.second_role:
            self.champ_select.set_role_preference(
                first=self.config.first_role,
                second=self.config.second_role,
            )

        for step in self._game_sequence:
            await step()
        await self.run_forever()

    def start_websocket(self):
        self.websocket_client.register_event(
            WebSocketEvent(
                endpoint="/lol-gameflow/v1/gameflow-phase",
                type=["CREATE", "UPDATE", "DELETE"],
                function=self.game_flow_update,
            ),
        )
        self.websocket_client.register_event(
            WebSocketEvent(
                endpoint="/lol-matchmaking/v1/search",
                type=["CREATE", "UPDATE"],
                function=self.ready_check.accept,
            )  # /lol-lobby/v2/lobby/matchmaking/search-state
        )
        self.websocket_client.register_event(
            WebSocketEvent(
                endpoint="/lol-champ-select/v1/session",
                type=["UPDATE"],
                function=self.champ_select.update,
            ),
        )
        self.websocket_client.register_event(
            WebSocketEvent(
                endpoint="/lol-chat/v1/conversations/",
                type=["UPDATE"],
                function=self.champ_select.get_chat_session_id,
            ),
        )
        if self.config.dismiss_notifications_at_eog:
            self.dismiss_notifications_at_eog()
        if self.config.command_best_player_at_eog:
            self.command_best_player_at_eog()
        if self.config.command_random_player_at_eog:
            self.command_random_player_at_eog()
        if self.config.chain_game_at_eog:
            self.chain_game_at_eog(game_sequence=self._game_sequence)
        if self.config.log_everything:
            self.log_everything()
        self.nursery.create_task(self.websocket_client.listen_websocket(), "listen_websocket")

    def game_flow_update(self, event):
        self.game_flow_phase = event.data
        logger.debug(f"The phase is now {self.game_flow_phase}")

    def log_everything(self, endpoint="/"):
        self.websocket_client.register_event(
            WebSocketEvent(
                endpoint=endpoint,
                type=["CREATE", "UPDATE", "DELETE"],
                function=self.loop_back_log,
            )
        )

    def command_best_player_at_eog(self):
        self.websocket_client.register_event(
            WebSocketEvent(
                endpoint="/lol-gameflow/v1/gameflow-phase",
                type=["UPDATE"],
                function=self.honor.command_best_player_at_eog,
            )
        )

    def command_random_player_at_eog(self):
        self.websocket_client.register_event(
            WebSocketEvent(
                endpoint="/lol-gameflow/v1/gameflow-phase",
                type=["UPDATE"],
                function=self.honor.command_random_player_at_eog,
            )
        )

    def chain_game_at_eog(self, game_sequence: list[Awaitable]):
        self.websocket_client.register_event(
            WebSocketEvent(
                endpoint="/lol-gameflow/v1/gameflow-phase",
                type=["UPDATE"],
                function=self.create_game.chain_game_at_eog,
                arguments=game_sequence,
            )
        )

    def dismiss_notifications_at_eog(self):
        self.websocket_client.register_event(
            WebSocketEvent(
                endpoint="/lol-gameflow/v1/gameflow-phase",
                type=["UPDATE"],
                function=self.notifications.dismiss_notifications_at_eog,
            )
        )

    def loop_back_log(self, event):
        logger.debug(event.uri)
        logger.debug(event.type)
        logger.debug(event.data)
        # logger.debug(f"{dumps(event.data, indent=4)}\n\n")

    async def get_region_and_locale(self):
        resp = await self.http_client.request(
            method="GET", endpoint="/riotclient/get_region_locale"
        )
        self.locale = resp.data.get("locale")
        self.region = resp.data.get("region").lower()
