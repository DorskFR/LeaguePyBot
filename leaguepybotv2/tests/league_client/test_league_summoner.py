import pytest
from leaguepybotv2.league_client import LeagueSummoner


@pytest.fixture
def league_summoner():
    return LeagueSummoner()


def test_league_summoner_object(league_summoner):
    assert isinstance(league_summoner, LeagueSummoner)


@pytest.mark.asyncio
async def test_set_picks_per_role(league_summoner):
    await league_summoner.set_picks_per_role(
        picks=["Fiora", "Garen", "Nasus"], role="TOP"
    )
    assert league_summoner.picks["TOP"] == [114, 86, 75]


@pytest.mark.asyncio
async def test_set_bans_per_role(league_summoner):
    await league_summoner.set_bans_per_role(
        bans=["Thresh", "Tristana", "Trundle"], role="BOTTOM"
    )
    assert league_summoner.bans["BOTTOM"] == [412, 18, 48]


@pytest.mark.asyncio
async def test_set_role_preference(league_summoner):
    await league_summoner.set_role_preference(first="TOP", second="BOTTOM")
    assert league_summoner.first_role == "TOP"
    assert league_summoner.second_role == "BOTTOM"


@pytest.mark.asyncio
async def test_get_champions_to_pick(league_summoner):
    await league_summoner.set_picks_per_role(
        picks=["Fiora", "Garen", "Nasus"], role="TOP"
    )
    picks = await league_summoner.get_champions_to_pick(role="TOP")
    assert picks == [114, 86, 75]


@pytest.mark.asyncio
async def test_get_champions_to_pick_without_role(league_summoner):
    await league_summoner.set_picks_per_role(
        picks=["Fiora", "Garen", "Nasus"], role="TOP"
    )
    await league_summoner.set_picks_per_role(
        picks=["Ezreal", "DrMundo", "MissFortune"], role="BOT"
    )
    picks = await league_summoner.get_champions_to_pick()
    assert picks == [114, 86, 75, 81, 36, 21]


@pytest.mark.asyncio
async def test_get_champions_to_ban(league_summoner):
    await league_summoner.set_bans_per_role(
        bans=["Thresh", "Tristana", "Trundle"], role="BOTTOM"
    )
    bans = await league_summoner.get_champions_to_ban(role="BOTTOM")
    assert bans == [412, 18, 48]


@pytest.mark.asyncio
async def test_get_champions_to_ban_without_role(league_summoner):
    await league_summoner.set_bans_per_role(
        bans=["Thresh", "Tristana", "Trundle"], role="BOTTOM"
    )
    await league_summoner.set_bans_per_role(
        bans=["Gangplank", "Kennen", "MonkeyKing"], role="TOP"
    )
    bans = await league_summoner.get_champions_to_ban()
    assert bans == [412, 18, 48, 41, 85, 62]
