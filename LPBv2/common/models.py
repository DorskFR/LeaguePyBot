from typing import Callable, List, Optional, Union, Any
from pydantic import BaseModel


class ClientResponse(BaseModel):
    data: Optional[Union[str, int, float, list, dict]]
    status_code: Optional[int]
    endpoint: Optional[str]


class WebSocketEvent(BaseModel):
    endpoint: str
    type: Union[str, List[str]]
    function: Callable
    arguments: Optional[Union[str, int, float, list, dict]]


class WebSocketEventResponse(BaseModel):
    type: str
    uri: str
    data: Optional[Union[str, int, float, list, dict]]


class Template(BaseModel):
    name: Optional[str]
    img: Any


class Match(BaseModel):
    name: Optional[str]
    x: Optional[int]
    y: Optional[int]
    team: Optional[str]


class MinimapZone(BaseModel):
    name: Optional[str]
    team: Optional[str]
    x: Optional[int]
    y: Optional[int]


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
    level: Optional[int] = 0
    currentGold: Optional[float]
    championName: Optional[str]
    isDead: Optional[bool]
    respawnTimer: Optional[float]
    position: Optional[str]  # TOP, JUNGLE, MIDDLE, BOTTOM and UTILITY
    team: Optional[str]  # ORDER or CHAOS
    x: Optional[int]
    y: Optional[int]
    zone: Optional[MinimapZone]


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


class TeamMember(BaseModel):
    summonerId: Optional[int]
    summonerName: Optional[str]
    championId: Optional[int]
    championName: Optional[str]
    team: Optional[str]
    level: Optional[int]
    position: Optional[str]
    isPlayerTeam: Optional[bool]
    isSelf: Optional[bool]
    isBot: Optional[bool]
    isDead: Optional[bool]
    x: Optional[int]
    y: Optional[int]
    zone: Optional[MinimapZone]


class Units(BaseModel):
    enemy_minions: Optional[List[Match]] = list()
    nb_enemy_minions: Optional[int] = 0
    enemy_champions: Optional[List[Match]] = list()
    nb_enemy_champions: Optional[int] = 0
    enemy_buildings: Optional[List[Match]] = list()
    nb_enemy_buildings: Optional[int] = 0
    ally_minions: Optional[List[Match]] = list()
    nb_ally_minions: Optional[int] = 0
    ally_champions: Optional[List[Match]] = list()
    nb_ally_champions: Optional[int] = 0
    ally_buildings: Optional[List[Match]] = list()
    nb_ally_buildings: Optional[int] = 0


class RolePreference(BaseModel):
    first: Optional[str] = "FILL"
    second: Optional[str] = "FILL"
    assigned: Optional[str] = "FILL"
