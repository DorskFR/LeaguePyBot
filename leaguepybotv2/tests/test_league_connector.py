import pytest
from leaguepybotv2.league_client import LeagueConnector
from .league_client.lockfile import LockFile


@pytest.fixture
def league_connector():
    return LeagueConnector()


def test_league_connector_object(league_connector):
    assert isinstance(league_connector, LeagueConnector)


def test_league_connector_lockfile(league_connector):
    assert isinstance(league_connector.lockfile, Lockfile)
