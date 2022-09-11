import asyncio
import functools
import signal
from asyncio.events import AbstractEventLoop
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Callable

from pydantic import BaseModel

from leaguepybot.common.enums import Role
from leaguepybot.common.logger import get_logger

logger = get_logger()


class Runnable:
    def __init__(self) -> None:
        self.is_running = False

    def __enter__(self) -> "Runnable":
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:  # type: ignore
        self.stop()

    def start(self) -> None:
        self.is_running = True
        self.add_signal_handler()

    def stop(self) -> None:
        self.is_running = False

    async def __aenter__(self) -> "Runnable":
        self.start()
        await self.async_start()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:  # type: ignore
        self.stop()
        await self.async_stop()

    async def async_start(self) -> None:
        ...

    async def async_stop(self) -> None:
        ...

    async def run_forever(self) -> None:
        while self.is_running:
            await asyncio.sleep(0)

    async def _sleep(self, sleep_timer: float = 0) -> None:
        """sleep 0.1 sec at a time, non blocking for graceful shutdown"""
        while self.is_running and sleep_timer > 0:
            await asyncio.sleep(0.1)
            sleep_timer -= 0.1

    def add_signal_handler(self) -> None:
        def _signal_handler(signum: str, _loop: AbstractEventLoop) -> None:
            """Signal handler used to gracefully shut down the application"""
            logger.warning(f"[{self.__class__}] Received signal {signum}. Shutting down...")
            self.stop()

        loop = asyncio.get_running_loop()
        for signame in ["SIGINT", "SIGTERM"]:
            loop.add_signal_handler(
                getattr(signal, signame),
                functools.partial(_signal_handler, signame, loop),
            )


class ClientApiResponse(BaseModel):
    data: Any
    status_code: int | None
    endpoint: str | None


class WebSocketEvent(BaseModel):
    endpoint: str
    type: str | list[str]
    function: Callable
    arguments: Any


class WebSocketEventResponse(BaseModel):
    type: str
    uri: str
    data: Any
    arguments: Any


class Template(BaseModel):
    name: str | None
    img: Any


class Match(BaseModel):
    name: str | None
    x: int | None
    y: int | None
    team: str | None


class MinimapZone(BaseModel):
    name: str | None
    team: str | None
    x: int | None
    y: int | None


class InventoryItem(BaseModel):
    canUse: bool | None
    consumable: bool | None
    count: int | None
    displayName: str | None
    itemID: int | None
    price: int | None
    rawDescription: str | None
    rawDisplayName: str | None
    slot: int | None


class PlayerInfo(BaseModel):
    name: str | None
    level: int | None = 1
    currentGold: float | None
    championName: str | None
    isDead: bool | None
    respawnTimer: float | None
    position: str | None  # TOP, JUNGLE, MIDDLE, BOTTOM and UTILITY
    team: str | None  # ORDER or CHAOS
    x: int | None
    y: int | None
    zone: MinimapZone | None


class PlayerScore(BaseModel):
    assists: int | None
    creepScore: int | None
    deaths: int | None
    kills: int | None
    wardScore: float | None


class PlayerStats(BaseModel):
    abilityHaste: float | None
    abilityPower: float | None
    armor: float | None
    armorPenetrationFlat: float | None
    armorPenetrationPercent: float | None
    attackDamage: float | None
    attackRange: float | None
    attackSpeed: float | None
    bonusArmorPenetrationPercent: float | None
    bonusMagicPenetrationPercent: float | None
    critChance: float | None
    critDamage: float | None
    currentHealth: float | None
    healShieldPower: float | None
    healthRegenRate: float | None
    lifeSteal: float | None
    magicLethality: float | None
    magicPenetrationFlat: float | None
    magicPenetrationPercent: float | None
    magicResist: float | None
    maxHealth: float | None
    moveSpeed: float | None
    omnivamp: float | None
    physicalLethality: float | None
    physicalVamp: float | None
    resourceMax: float | None
    resourceRegenRate: float | None
    resourceType: str | None
    resourceValue: float | None
    spellVamp: float | None
    tenacity: float | None


class GameEvent(BaseModel):
    EventID: int | None
    EventName: str | None
    # GameStart, MinionsSpawning, FirstBrick, TurretKilled, InhibKilled
    # DragonKill, HeraldKill, BaronKill, ChampionKill, Multikill, Ace
    EventTime: float | None
    TurretKilled: str | None
    KillerName: str | None
    Assisters: list[str] | None
    InhibKilled: str | None
    DragonType: str | None
    Stolen: str | None  # "False", "True"
    KillStreak: int | None
    Acer: str | None
    AcingTeam: str | None


class TeamMember(BaseModel):
    summonerId: int | None
    summonerName: str | None
    championId: int | None
    championName: str | None
    team: str | None
    level: int | None
    position: str | None
    isPlayerTeam: bool | None
    isSelf: bool | None
    isBot: bool | None
    isDead: bool | None
    x: int | None
    y: int | None
    zone: MinimapZone | None
    kills: int | None
    gold: int | None


class Units(BaseModel):
    ally_buildings: list[Match] | None = []
    ally_champions: list[Match] | None = []
    ally_minions: list[Match] | None = []
    enemy_buildings: list[Match] | None = []
    enemy_champions: list[Match] | None = []
    enemy_minions: list[Match] | None = []
    nb_ally_buildings: int | None = 0
    nb_ally_champions: int | None = 0
    nb_ally_minions: int | None = 0
    nb_enemy_buildings: int | None = 0
    nb_enemy_champions: int | None = 0
    nb_enemy_minions: int | None = 0


@dataclass
class RolePreference:
    assigned: Role = Role.FILL
    first: Role = Role.FILL
    second: Role = Role.FILL


class SummonerInfo(BaseModel):
    accountId: str | None
    displayName: str | None
    internalName: str | None
    puuid: str | None
    summonerId: str | None
    summonerLevel: int | None
