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


def find_closest_point(origin, points):
    distances = list()
    for point in points:
        pythagorean_distance(origin, point)
    min(distances)


def pythagorean_distance(pt1: tuple, pt2: tuple) -> float:
    dx = abs(pt1[0] - pt2[0])
    dy = abs(pt1[1] - pt2[1])
    return sqrt(pow(dx, 2) + pow(dy, 2))
