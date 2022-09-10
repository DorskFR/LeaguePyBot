from dataclasses import dataclass
from typing import Any, Callable, List, Union

from pydantic import BaseModel

from leaguepybot.common.enums import Role


class ClientResponse(BaseModel):
    data: Union[str, int, float, list, dict] | None
    status_code: int | None
    endpoint: str | None


class WebSocketEvent(BaseModel):
    endpoint: str
    type: Union[str, List[str]]
    function: Callable
    arguments: Union[str, int, float, list, dict] | None


class WebSocketEventResponse(BaseModel):
    type: str
    uri: str
    data: Union[str, int, float, list, dict] | None
    arguments: Union[str, int, float, list, dict] | None


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
    Assisters: List[str] | None
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
    ally_buildings: List[Match] | None = []
    ally_champions: List[Match] | None = []
    ally_minions: List[Match] | None = []
    enemy_buildings: List[Match] | None = []
    enemy_champions: List[Match] | None = []
    enemy_minions: List[Match] | None = []
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
