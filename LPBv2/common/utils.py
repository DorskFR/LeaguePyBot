import base64
from distutils.util import strtobool
from math import sqrt
import time
from ..logger import Colors, get_logger
from .zones import ZONES_210 as ZONES

logger = get_logger("LPBv2.Timer")


def cast_to_bool(value):
    return bool(strtobool(str(value)))


def get_key_from_value(dictionary, lookup_value):
    for key, value in dictionary.items():
        if value == lookup_value:
            return key

    return "Not found"


def atob(message):
    message_bytes = message.encode("utf-8")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode("utf-8")
    return base64_message


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
    safest_unit = min(units, key=lambda item: item.x)
    return safest_unit.x - 50, safest_unit.y + 50


def riskiest_position(units: list):
    riskiest_unit = max(units, key=lambda item: item.x)
    return riskiest_unit.x, riskiest_unit.y


def merge_dicts(d1: dict, d2: dict):
    return d1 | d2


def make_minimap_coords(x: int, y: int):
    return 1920 - 210 + x, 1080 - 210 + y


def find_closest_zone(x: int, y: int, zones=ZONES):
    distances = dict()
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
            f"{Colors.blue}{func.__name__}{Colors.reset} running time is {Colors.cyan}{round(time_elapsed - time_started, 4)}{Colors.reset} seconds."
        )
        return result

    return time_it


def debug_coro(func):
    async def add_exception(*args, **kwargs):
        coro = func(*args, **kwargs)
        try:
            return await coro
        except Exception as e:
            logger.error(f"In {Colors.cyan}{coro.__name__}{Colors.reset}: {e}")

    return add_exception
