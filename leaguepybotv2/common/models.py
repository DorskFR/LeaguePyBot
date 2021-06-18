from typing import Callable, List, Optional, Union, Any
from pydantic import BaseModel


class ClientResponse(BaseModel):
    data: Optional[Union[str, int, float, list, dict]]
    status_code: Optional[int]
    endpoint: Optional[str]


class WebsocketEvent(BaseModel):
    endpoint: str
    type: Union[str, List[str]]
    function: Callable
    arguments: Optional[Union[str, int, float, list, dict]]


class WebsocketEventResponse(BaseModel):
    type: str
    uri: str
    data: Optional[Union[str, int, float, list, dict]]


class Lockfile(BaseModel):
    lcu_pid: int
    pid: int
    port: int
    auth_key: str
    installation_path: str


class InventoryItem(BaseModel):
    canUse: Optional[bool]
    consumable: Optional[bool]
    count: Optional[int]
    displayName: Optional[str]
    itemID: Optional[int]
    price: Optional[int]
    rawDescription: Optional[str]
    rawDisplayName: Optional[str]
    slot: Optional[int]


class PlayerInfo(BaseModel):
    name: Optional[str]
    level: Optional[int]
    currentGold: Optional[float]
    championName: Optional[str]
    isDead: Optional[bool]
    respawnTimer: Optional[float]
    position: Optional[str]  # TOP, JUNGLE, MIDDLE, BOTTOM and UTILITY
    team: Optional[str]  # ORDER or CHAOS
    x: Optional[int]
    y: Optional[int]
    zone: Optional[int]


class PlayerScore(BaseModel):
    assists: Optional[int]
    creepScore: Optional[int]
    deaths: Optional[int]
    kills: Optional[int]
    wardScore: Optional[float]


class PlayerStats(BaseModel):
    abilityHaste: Optional[float]
    abilityHaste: Optional[float]
    abilityPower: Optional[float]
    armor: Optional[float]
    armorPenetrationFlat: Optional[float]
    armorPenetrationPercent: Optional[float]
    attackDamage: Optional[float]
    attackRange: Optional[float]
    attackSpeed: Optional[float]
    bonusArmorPenetrationPercent: Optional[float]
    bonusMagicPenetrationPercent: Optional[float]
    critChance: Optional[float]
    critDamage: Optional[float]
    currentHealth: Optional[float]
    healShieldPower: Optional[float]
    healthRegenRate: Optional[float]
    lifeSteal: Optional[float]
    magicLethality: Optional[float]
    magicPenetrationFlat: Optional[float]
    magicPenetrationPercent: Optional[float]
    magicResist: Optional[float]
    maxHealth: Optional[float]
    moveSpeed: Optional[float]
    omnivamp: Optional[float]
    physicalLethality: Optional[float]
    physicalVamp: Optional[float]
    resourceMax: Optional[float]
    resourceRegenRate: Optional[float]
    resourceType: Optional[str]
    resourceValue: Optional[float]
    spellVamp: Optional[float]
    tenacity: Optional[float]


class GameEvent(BaseModel):
    EventID: Optional[int]
    EventName: Optional[str]
    # GameStart, MinionsSpawning, FirstBrick, TurretKilled, InhibKilled
    # DragonKill, HeraldKill, BaronKill, ChampionKill, Multikill, Ace
    EventTime: Optional[float]
    TurretKilled: Optional[str]
    KillerName: Optional[str]
    Assisters: Optional[List[str]]
    InhibKilled: Optional[str]
    DragonType: Optional[str]
    Stolen: Optional[str]  # "False", "True"
    KillStreak: Optional[int]
    Acer: Optional[str]
    AcingTeam: Optional[str]


class Template(BaseModel):
    name: Optional[str]
    img: Any


class Match(BaseModel):
    name: Optional[str]
    x: Optional[int]
    y: Optional[int]


class Unit(BaseModel):
    name: Optional[str]
    x: Optional[int]
    y: Optional[int]
    team: Optional[str]


class MinimapZone(BaseModel):
    name: Optional[str]
    team: Optional[str]
    x: Optional[int]
    y: Optional[int]


class TeamMember(BaseModel):
    summonerId: Optional[int]
    summonerName: Optional[str]
    championId: Optional[int]
    championName: Optional[str]
    team: Optional[str]
    level: Optional[int]
    position: str
    isPlayerTeam: Optional[bool]
    isSelf: Optional[bool]
    isBot: Optional[bool]
    isDead: Optional[bool]
    x: Optional[int]
    y: Optional[int]
    zone: Optional[MinimapZone]
