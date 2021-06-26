from LPBv2.client import ChampSelect
from .mock_http_connection import MockHTTPConnection
from .mock_data_champ_select import event
from LPBv2.common import RolePreference
import pytest


@pytest.fixture
def champ_select():
    return ChampSelect(connection=MockHTTPConnection())


def test_champ_select_init(champ_select):
    assert isinstance(champ_select.http, MockHTTPConnection)
    assert isinstance(champ_select.role, RolePreference)
    assert isinstance(champ_select.picks, dict)
    assert isinstance(champ_select.is_picking, bool)
    assert isinstance(champ_select.bans, dict)
    assert isinstance(champ_select.is_banning, bool)


@pytest.mark.asyncio
async def test_set_role_preference(champ_select):
    await champ_select.set_role_preference(first="TOP", second="BOTTOM")
    assert champ_select.role.first == "TOP"
    assert champ_select.role.second == "BOTTOM"


@pytest.mark.asyncio
async def test_set_picks_per_role(champ_select):
    await champ_select.set_picks_per_role(picks=["Fiora", "Garen"], role="TOP")
    await champ_select.set_picks_per_role(picks=["Sivir", "Tristana"], role="BOTTOM")
    assert champ_select.picks.get("TOP") == [114, 86]
    assert champ_select.picks.get("BOTTOM") == [15, 18]


@pytest.mark.asyncio
async def test_set_bans_per_role(champ_select):
    await champ_select.set_bans_per_role(bans=["Shaco", "MonkeyKing"], role="TOP")
    await champ_select.set_bans_per_role(bans=["Thresh", "TahmKench"], role="BOTTOM")
    assert champ_select.bans.get("TOP") == [35, 62]
    assert champ_select.bans.get("BOTTOM") == [412, 223]


@pytest.mark.asyncio
async def test_get_player_cell_id(champ_select):
    await champ_select.get_player_cell_id(event)
    assert champ_select.player_cell_id == 3


@pytest.mark.asyncio
async def test_get_role(champ_select):
    await champ_select.get_player_cell_id(event)
    await champ_select.get_role(event)
    assert champ_select.role.assigned == "TOP"


@pytest.mark.asyncio
async def test_block_condition_ban(champ_select):
    await champ_select.get_player_cell_id(event)
    condition = await champ_select.block_condition(event, "ban")
    assert champ_select.player_id == 3
    assert isinstance(condition, bool)
    assert condition == True


@pytest.mark.asyncio
async def test_block_condition_pick(champ_select):
    await champ_select.get_player_cell_id(event)
    condition = await champ_select.block_condition(event, "pick")
    assert champ_select.player_id == 17
    assert isinstance(condition, bool)
    assert condition == True


@pytest.mark.asyncio
async def test_intent(champ_select):
    pass


@pytest.mark.asyncio
async def test_get_champions_to_pick(champ_select):
    await champ_select.set_picks_per_role(picks=["Fiora", "Garen"], role="TOP")
    await champ_select.set_picks_per_role(picks=["Sivir", "Tristana"], role="BOTTOM")
    assert champ_select.picks.get("TOP") == [114, 86]
    assert champ_select.picks.get("BOTTOM") == [15, 18]
    picks = await champ_select.get_champions_to_pick()
    assert picks == [114, 86, 15, 18]
    picks = await champ_select.get_champions_to_pick(role="BOTTOM")
    assert picks == [15, 18]
    picks = await champ_select.get_champions_to_pick(role="TOP")
    assert picks == [114, 86]


@pytest.mark.asyncio
async def test_get_champions_to_ban(champ_select):
    await champ_select.set_bans_per_role(bans=["Shaco", "MonkeyKing"], role="TOP")
    await champ_select.set_bans_per_role(bans=["Thresh", "TahmKench"], role="BOTTOM")
    assert champ_select.bans.get("TOP") == [35, 62]
    assert champ_select.bans.get("BOTTOM") == [412, 223]
    bans = await champ_select.get_champions_to_ban()
    assert bans == [35, 62, 412, 223]
    bans = await champ_select.get_champions_to_ban(role="BOTTOM")
    assert bans == [412, 223]
    bans = await champ_select.get_champions_to_ban(role="TOP")
    assert bans == [35, 62]


@pytest.mark.asyncio
async def test_pick(champ_select):
    await champ_select.get_player_cell_id(event)
    condition = await champ_select.block_condition(event, "pick")
    pick = await champ_select.pick(114)
    assert pick == True
    assert champ_select.http.endpoint[0] == "/lol-champ-select/v1/session/actions/17"
    assert champ_select.http.data[0]["actorCellId"] == 3
    assert champ_select.http.data[0]["championId"] == 114


@pytest.mark.asyncio
async def test_ban(champ_select):
    await champ_select.get_player_cell_id(event)
    condition = await champ_select.block_condition(event, "ban")
    ban = await champ_select.ban(35)
    assert ban == True
    assert champ_select.http.endpoint[0] == "/lol-champ-select/v1/session/actions/3"
    assert champ_select.http.data[0]["actorCellId"] == 3
    assert champ_select.http.data[0]["championId"] == 35


@pytest.mark.asyncio
async def test_pick_champion(champ_select):
    await champ_select.set_picks_per_role(picks=["Fiora", "Garen"], role="TOP")
    await champ_select.get_player_cell_id(event)
    condition = await champ_select.block_condition(event, "pick")
    await champ_select.pick_champion()
    picks = await champ_select.get_champions_to_pick()
    assert picks == [114, 86]
    assert champ_select.is_banning == False
    assert champ_select.is_picking == False
    assert champ_select.http.endpoint[0] == "/lol-champ-select/v1/session/actions/17"
    assert champ_select.http.data[0]["actorCellId"] == 3
    assert champ_select.http.data[0]["championId"] == 114


@pytest.mark.asyncio
async def test_ban_champion(champ_select):
    await champ_select.set_bans_per_role(bans=["Thresh", "TahmKench"], role="BOTTOM")
    await champ_select.get_player_cell_id(event)
    condition = await champ_select.block_condition(event, "ban")
    await champ_select.ban_champion()
    bans = await champ_select.get_champions_to_ban()
    assert bans == [412, 223]
    assert champ_select.is_banning == False
    assert champ_select.is_picking == False
    assert champ_select.http.endpoint[0] == "/lol-champ-select/v1/session/actions/3"
    assert champ_select.http.data[0]["actorCellId"] == 3
    assert champ_select.http.data[0]["championId"] == 412


@pytest.mark.asyncio
async def test_update(champ_select):
    await champ_select.set_picks_per_role(picks=["Fiora", "Garen"], role="TOP")
    await champ_select.set_picks_per_role(picks=["Sivir", "Tristana"], role="BOTTOM")
    await champ_select.set_bans_per_role(bans=["Shaco", "MonkeyKing"], role="TOP")
    await champ_select.set_bans_per_role(bans=["Thresh", "TahmKench"], role="BOTTOM")

    await champ_select.update(event)

    assert champ_select.player_cell_id == 3
    assert champ_select.role.assigned == "TOP"
    assert champ_select.player_id == 3
    picks = await champ_select.get_champions_to_pick()
    assert picks == [114, 86]
    bans = await champ_select.get_champions_to_ban()
    assert bans == [35, 62]
    assert champ_select.is_banning == False
    assert champ_select.is_picking == False
    assert champ_select.http.endpoint[0] == "/lol-champ-select/v1/session/actions/17"
    assert champ_select.http.data[0]["actorCellId"] == 3
    assert champ_select.http.data[0]["championId"] == 114
    assert champ_select.http.endpoint[1] == "/lol-champ-select/v1/session/actions/3"
    assert champ_select.http.data[1]["actorCellId"] == 3
    assert champ_select.http.data[1]["championId"] == 35
