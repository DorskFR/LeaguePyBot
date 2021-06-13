import pytest
from ..league_summoner import LeagueSummoner


@pytest.fixture
def league_summoner():
    return LeagueSummoner()


def test_league_summoner_object(league_summoner):
    assert isinstance(league_summoner, LeagueSummoner)
