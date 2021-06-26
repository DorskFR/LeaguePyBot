from LPBv2.client import Connection, Lockfile
import pytest


@pytest.fixture
def connection():
    return Connection()


def test_connection(connection):
    assert isinstance(connection, Connection)


def test_connection_lockfile(connection):
    assert isinstance(connection.lockfile, Lockfile)


def test_connection_headers(connection):
    assert connection.headers
