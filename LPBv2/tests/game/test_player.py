import pytest
from LPBv2.common import (
    InventoryItem,
    PlayerInfo,
    PlayerScore,
    PlayerStats,
    TeamMember,
    MinimapZone,
    merge_dicts,
)
from LPBv2.game import Player


update_data = {
    "abilities": {
        "E": {
            "abilityLevel": 0,
            "displayName": "\u9b42\u306e\u8a66\u7df4",
            "id": "IllaoiE",
            "rawDescription": "GeneratedTip_Spell_IllaoiE_Description",
            "rawDisplayName": "GeneratedTip_Spell_IllaoiE_DisplayName",
        },
        "Passive": {
            "displayName": "\u65e7\u795e\u306e\u9810\u8a00\u8005",
            "id": "IllaoiPassive",
            "rawDescription": "GeneratedTip_Passive_IllaoiPassive_Description",
            "rawDisplayName": "GeneratedTip_Passive_IllaoiPassive_DisplayName",
        },
        "Q": {
            "abilityLevel": 0,
            "displayName": "\u89e6\u624b\u306e\u9244\u69cc",
            "id": "IllaoiQ",
            "rawDescription": "GeneratedTip_Spell_IllaoiQ_Description",
            "rawDisplayName": "GeneratedTip_Spell_IllaoiQ_DisplayName",
        },
        "R": {
            "abilityLevel": 0,
            "displayName": "\u4fe1\u4ef0\u9707",
            "id": "IllaoiR",
            "rawDescription": "GeneratedTip_Spell_IllaoiR_Description",
            "rawDisplayName": "GeneratedTip_Spell_IllaoiR_DisplayName",
        },
        "W": {
            "abilityLevel": 0,
            "displayName": "\u904e\u9177\u306a\u308b\u6559\u8a13",
            "id": "IllaoiW",
            "rawDescription": "GeneratedTip_Spell_IllaoiW_Description",
            "rawDisplayName": "GeneratedTip_Spell_IllaoiW_DisplayName",
        },
    },
    "championStats": {
        "abilityHaste": 0.0,
        "abilityPower": 0.0,
        "armor": 41.0,
        "armorPenetrationFlat": 0.0,
        "armorPenetrationPercent": 1.0,
        "attackDamage": 73.4000015258789,
        "attackRange": 125.0,
        "attackSpeed": 0.5709999799728394,
        "bonusArmorPenetrationPercent": 1.0,
        "bonusMagicPenetrationPercent": 1.0,
        "cooldownReduction": 0.0,
        "critChance": 0.0,
        "critDamage": 175.0,
        "currentHealth": 601.0,
        "healthRegenRate": 1.899999976158142,
        "lifeSteal": 0.0,
        "magicLethality": 0.0,
        "magicPenetrationFlat": 0.0,
        "magicPenetrationPercent": 1.0,
        "magicResist": 32.0,
        "maxHealth": 601.0,
        "moveSpeed": 340.0,
        "physicalLethality": 0.0,
        "resourceMax": 300.0,
        "resourceRegenRate": 1.5,
        "resourceType": "MANA",
        "resourceValue": 300.0,
        "spellVamp": 0.0,
        "tenacity": 0.0,
    },
    "currentGold": 888.6270751953125,
    "level": 1,
    "summonerName": "Supername",
    "championName": "\u30a4\u30e9\u30aa\u30a4",
    "isBot": False,
    "isDead": False,
    "items": [
        {
            "canUse": False,
            "consumable": False,
            "count": 1,
            "displayName": "\u92fc\u306e\u30b7\u30e7\u30eb\u30c0\u30fc\u30ac\u30fc\u30c9",
            "itemID": 3854,
            "price": 400,
            "rawDescription": "GeneratedTip_Item_3854_Description",
            "rawDisplayName": "Item_3854_Name",
            "slot": 0,
        },
        {
            "canUse": False,
            "consumable": False,
            "count": 1,
            "displayName": "\u30d7\u30ec\u30fc\u30c8 \u30b9\u30c1\u30fc\u30eb\u30ad\u30e3\u30c3\u30d7",
            "itemID": 3047,
            "price": 500,
            "rawDescription": "GeneratedTip_Item_3047_Description",
            "rawDisplayName": "Item_3047_Name",
            "slot": 1,
        },
        {
            "canUse": False,
            "consumable": False,
            "count": 1,
            "displayName": "\u30ad\u30f3\u30c9\u30eb\u30b8\u30a7\u30e0",
            "itemID": 3067,
            "price": 400,
            "rawDescription": "GeneratedTip_Item_3067_Description",
            "rawDisplayName": "Item_3067_Name",
            "slot": 2,
        },
        {
            "canUse": True,
            "consumable": False,
            "count": 1,
            "displayName": "\u30b9\u30c6\u30eb\u30b9 \u30ef\u30fc\u30c9",
            "itemID": 3340,
            "price": 0,
            "rawDescription": "GeneratedTip_Item_3340_Description",
            "rawDisplayName": "Item_3340_Name",
            "slot": 6,
        },
    ],
    "position": "",
    "rawChampionName": "game_character_displayname_Illaoi",
    "respawnTimer": 0.0,
    "runes": {
        "keystone": {
            "displayName": "\u4e0d\u6b7b\u8005\u306e\u63e1\u6483",
            "id": 8437,
            "rawDescription": "perk_tooltip_GraspOfTheUndying",
            "rawDisplayName": "perk_displayname_GraspOfTheUndying",
        },
        "primaryRuneTree": {
            "displayName": "\u4e0d\u6ec5",
            "id": 8400,
            "rawDescription": "perkstyle_tooltip_7204",
            "rawDisplayName": "perkstyle_displayname_7204",
        },
        "secondaryRuneTree": {
            "displayName": "\u9b54\u9053",
            "id": 8200,
            "rawDescription": "perkstyle_tooltip_7202",
            "rawDisplayName": "perkstyle_displayname_7202",
        },
    },
    "scores": {
        "assists": 0,
        "creepScore": 100,
        "deaths": 0,
        "kills": 0,
        "wardScore": 0.0,
    },
    "skinID": 0,
    "summonerSpells": {
        "summonerSpellOne": {
            "displayName": "\u30af\u30ec\u30f3\u30ba",
            "rawDescription": "GeneratedTip_SummonerSpell_SummonerBoost_Description",
            "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerBoost_DisplayName",
        },
        "summonerSpellTwo": {
            "displayName": "\u30a4\u30b0\u30be\u30fc\u30b9\u30c8",
            "rawDescription": "GeneratedTip_SummonerSpell_SummonerExhaust_Description",
            "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerExhaust_DisplayName",
        },
    },
    "team": "ORDER",
}

test_zone = MinimapZone(x=90, y=90, name="TestZone")
test_member = TeamMember(x=100, y=100, zone=test_zone)


@pytest.fixture
def get_player():
    return Player()


def test_player_init(get_player):
    assert get_player
    assert isinstance(get_player.info, PlayerInfo)
    assert isinstance(get_player.stats, PlayerStats)
    assert isinstance(get_player.score, PlayerScore)
    assert isinstance(get_player.inventory, list)
    assert isinstance(get_player.location, str)
    assert isinstance(get_player, Player)


@pytest.mark.asyncio
async def test_player_update_info(get_player):
    await get_player.update_info(update_data)
    assert get_player.info.name == "Supername"
    assert get_player.info.level == 1
    assert isinstance(get_player.info, PlayerInfo)


@pytest.mark.asyncio
async def test_player_update_stats(get_player):
    await get_player.update_stats(update_data)
    assert get_player.stats.maxHealth == 601.0
    assert isinstance(get_player.stats, PlayerStats)


@pytest.mark.asyncio
async def test_player_update_score(get_player):
    await get_player.update_score(update_data)
    assert get_player.score.creepScore == 100
    assert isinstance(get_player.score, PlayerScore)


@pytest.mark.asyncio
async def test_player_update_inventory(get_player):
    await get_player.update_inventory(update_data)
    assert isinstance(get_player.inventory, list)
    assert len(get_player.inventory) > 0
    assert isinstance(get_player.inventory[0], InventoryItem)
    assert get_player.inventory[0].itemID == 3854


@pytest.mark.asyncio
async def test_player_update_location(get_player):
    await get_player.update_location(test_member)
    assert get_player.info.x == 100
    assert get_player.info.y == 100
    assert get_player.info.zone == test_zone
    assert isinstance(get_player.info.zone, MinimapZone)
    assert isinstance(get_player.info, PlayerInfo)


@pytest.mark.asyncio
async def test_player_update(get_player):
    await get_player.update(update_data)

    assert get_player.info.name == "Supername"
    assert get_player.info.level == 1
    assert isinstance(get_player.info, PlayerInfo)

    assert get_player.stats.maxHealth == 601.0
    assert isinstance(get_player.stats, PlayerStats)

    assert get_player.score.creepScore == 100
    assert isinstance(get_player.score, PlayerScore)

    assert isinstance(get_player.inventory, list)
    assert len(get_player.inventory) > 0
    assert isinstance(get_player.inventory[0], InventoryItem)
    assert get_player.inventory[0].itemID == 3854
