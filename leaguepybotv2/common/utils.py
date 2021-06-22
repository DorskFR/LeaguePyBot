import base64
from distutils.util import strtobool
from math import sqrt


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


def merge_dicts(d1: dict, d2: dict):
    return d1 | d2
