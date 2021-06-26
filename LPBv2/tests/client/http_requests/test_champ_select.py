from LPBv2.client import ChampSelect, HTTPConnection
import pytest


@pytest.fixture
def champ_select():
    return ChampSelect()


def test_champ_select_init(champ_select):
    assert isinstance(champ_select.http, HTTPConnection)
    assert isinstance(champ_select.first_role, str)
    assert isinstance(champ_select.second_role, str)
    assert isinstance(champ_select.role, str)
    assert isinstance(champ_select.picks, dict)
    assert isinstance(champ_select.is_picking, bool)
    assert isinstance(champ_select.bans, dict)
    assert isinstance(champ_select.is_banning, bool)


@pytest.mark.asyncio
async def test_set_role_preference(champ_select):
    await champ_select.set_role_preference(first="TOP", second="BOTTOM")
    assert champ_select.first_role == "TOP"
    assert champ_select.second_role == "BOTTOM"


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


from .test_champ_select_mock_data import event


@pytest.mark.asyncio
async def test_get_player_cell_id(champ_select):
    await champ_select.get_player_cell_id(event)
    assert champ_select.player_cell_id == 3


@pytest.mark.asyncio
async def test_get_role(champ_select):
    await champ_select.get_player_cell_id(event)
    await champ_select.get_role(event)
    assert champ_select.role == "TOP"


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
    assert pick == None  # No mockup interface


@pytest.mark.asyncio
async def test_ban(champ_select):
    await champ_select.get_player_cell_id(event)
    condition = await champ_select.block_condition(event, "pick")
    ban = await champ_select.ban(35)
    assert ban == None  # No mockup interface


@pytest.mark.asyncio
async def test_pick_champion(champ_select):
    pass


@pytest.mark.asyncio
async def test_ban_champion(champ_select):
    pass


# @pytest.mark.asyncio
# async def test_champ_select_player_cell(champ_select):
#     assert isinstance(champ_select.player_cell_id, int)
#     assert isinstance(champ_select.player_id, int)
#     assert isinstance(champ_select.champion_id, int)


@pytest.mark.asyncio
async def test_update(champ_select):
    pass
