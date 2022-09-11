import time
from contextlib import suppress
from typing import Dict, Generator

from psutil import NoSuchProcess, Process, ZombieProcess, process_iter

from leaguepybot.common.logger import get_logger

logger = get_logger("LPBv3.Lockfile")


class Lockfile:
    def __init__(self):
        self.lcu_pid: int
        self.pid: int
        self.port: int
        self.auth_key: str
        self.installation_path: str
        self.get_lockfile()

    def get_lockfile(self):
        while not (process := next(self.return_ux_process(), None)):
            logger.debug("Process not found, start the client")
            time.sleep(1)
        process_args = self.parse_cmdline_args(process.cmdline())
        self.lcu_pid = process.pid
        self.pid = int(process_args["app-pid"])
        self.port = int(process_args["app-port"])
        self.auth_key = process_args["remoting-auth-token"]
        self.installation_path = process_args["install-directory"]
        logger.debug(f"auth_key: {self.auth_key}, port: {self.port}")

    def return_ux_process(self) -> Generator[Process, None, None]:
        for process in process_iter():
            with suppress(NoSuchProcess, ZombieProcess):
                if process.name() in ["LeagueClientUx.exe", "LeagueClientUx"]:
                    yield process

    def parse_cmdline_args(self, cmdline_args) -> Dict[str, str]:
        cmdline_args_parsed = {}
        for cmdline_arg in cmdline_args:
            if len(cmdline_arg) > 0 and "=" in cmdline_arg:
                key, value = cmdline_arg[2:].split("=")
                cmdline_args_parsed[key] = value
        return cmdline_args_parsed
