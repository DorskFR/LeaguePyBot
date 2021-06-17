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


def find_closest_point(x, y, points):
    distances = list()
    for point in points:
        calculate_distance_point(x, y, point)
    min(distances)


def calculate_distance_point(x1, y1, x2, y2):
    # pythagorean distance
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    distance = sqrt(pow(dx, 2) + pow(dy, 2))
    print(distance)
