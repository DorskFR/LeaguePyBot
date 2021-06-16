from typing import Dict, Generator

from psutil import process_iter, Process


def return_ux_process() -> Generator[Process, None, None]:
    for process in process_iter():
        if process.name() in ["LeagueClientUx.exe", "LeagueClientUx"]:
            yield process


def parse_cmdline_args(cmdline_args) -> Dict[str, str]:
    cmdline_args_parsed = {}
    for cmdline_arg in cmdline_args:
        if len(cmdline_arg) > 0 and "=" in cmdline_arg:
            key, value = cmdline_arg[2:].split("=")
            cmdline_args_parsed[key] = value
    return cmdline_args_parsed


p1 = return_ux_process()
print(p1)
p2 = next(p1, None)
print(p2)
p3 = p2.cmdline()
print(p3)
p4 = parse_cmdline_args(p3)
print(p4)
