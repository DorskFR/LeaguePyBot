import base64
from distutils.util import strtobool


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
