from LPBv2.client import Lockfile
import pytest


@pytest.fixture
def lockfile():
    return Lockfile()


def test_lockfile_init(lockfile):
    assert isinstance(lockfile.lcu_pid, int)
    assert isinstance(lockfile.pid, int)
    assert isinstance(lockfile.port, int)
    assert isinstance(lockfile.auth_key, str)
    assert isinstance(lockfile.installation_path, str)


def test_get_lockfile(lockfile):
    lockfile.get_lockfile()
    assert lockfile.port != 0


def test_return_ux_process(lockfile):
    process = next(lockfile.return_ux_process(), None)
    while not process:
        process = next(lockfile.return_ux_process(), None)
    assert process.name() in ["LeagueClientUx.exe", "LeagueClientUx"]


def test_parse_cmdline_args(lockfile):
    process = next(lockfile.return_ux_process(), None)
    while not process:
        process = next(lockfile.return_ux_process(), None)
    parse = lockfile.parse_cmdline_args(process.cmdline())
    assert isinstance(parse, dict)
    assert isinstance(parse["app-port"], str)
