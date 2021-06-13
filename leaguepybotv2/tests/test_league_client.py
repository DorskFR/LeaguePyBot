import pytest
from leaguepybotv2.league_client import LeagueClient


@pytest.fixture
def league_client():
    return LeagueClient()


def test_league_client_object(league_client):
    assert isinstance(league_client, LeagueClient)
