import pytest
from leaguepybotv2.league_client import LeagueConnection


@pytest.fixture
def league_connection():
    return LeagueConnection()


def test_league_connection_object(league_connection):
    assert isinstance(league_connection, LeagueConnection)
