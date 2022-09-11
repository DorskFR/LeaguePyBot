import base64
import os
import time
from math import sqrt
from re import sub

from leaguepybot.common.logger import get_logger
from leaguepybot.common.zones import ZONES_210 as ZONES

logger = get_logger("LPBv3.Utils")


cls = lambda: os.system("cls" if os.name == "nt" else "clear") or None


def cast_to_bool(value: str | int | float) -> bool:
    match str(value).lower():
        case "yes" | "true" | "t" | "y" | "1":
            return True
        case "no" | "false" | "f" | "n" | "0":
            return False
        case _:
            raise ValueError(f"Invalid boolean string: {value}")


def get_key_from_value(dictionary, lookup_value):
    return next((key for key, value in dictionary.items() if value == lookup_value), "Not found")


def atob(message):
    message_bytes = message.encode("utf-8")
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode("utf-8")


def pythagorean_distance(pt1: tuple, pt2: tuple) -> float:
    dx = abs(pt1[0] - pt2[0])
    dy = abs(pt1[1] - pt2[1])
    return sqrt(pow(dx, 2) + pow(dy, 2))


# Needed to calculate the average position of a group of units
def average_position(units: list):
    number_of_units = len(units)
    average_x = int(sum(unit.x for unit in units) / number_of_units)
    average_y = int(sum(unit.y for unit in units) / number_of_units)
    return average_x, average_y


def safest_position(units: list):
    safest_unit = min(units, key=lambda item: item.x - item.y)
    return safest_unit.x - 50, safest_unit.y + 50


def riskiest_position(units: list):
    riskiest_unit = max(units, key=lambda item: item.x - item.y)
    return riskiest_unit.x, riskiest_unit.y


def merge_dicts(d1: dict, d2: dict):
    return d1 | d2


def make_minimap_coords(x: int, y: int):
    return 1920 - 210 + x, 1080 - 210 + y


def find_closest_zone(x: int, y: int, zones=ZONES):
    distances = {}
    for zone in zones:
        distance = pythagorean_distance((x, y), (zone.x, zone.y))
        distances[distance] = zone
        closest = min(list(distances))
    return distances[closest]


def measure_time(func):
    def time_it(*args, **kwargs):
        time_started = time.time()
        result = func(*args, **kwargs)
        time_elapsed = time.time()
        logger.debug(
            f"{func.__name__} running time is {round(time_elapsed - time_started, 4)} seconds."
        )
        return result

    return time_it


def debug_coro(func):
    async def add_exception(*args, **kwargs):
        coro = func(*args, **kwargs)
        try:
            # logger.debug(f"Running {coro.__name__}")
            return await coro
        except Exception as e:
            logger.error(f"In {coro.__name__}: {e}")

    return add_exception


def remove_non_alphanumeric(client_value):
    if client_value:
        return sub(r"\W+", "", client_value.split(",")[0].strip())
