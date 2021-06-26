from LPBv2.common.utils import *
from LPBv2.common import CHAMPIONS, Match


def test_cast_to_bool_true():
    assert cast_to_bool("true") == True


def test_cast_to_bool_false():
    assert cast_to_bool("false") == False


def test_get_key_from_value():
    assert get_key_from_value(CHAMPIONS, 114) == "fiora"


def test_get_key_from_value_not_existing():
    assert get_key_from_value(CHAMPIONS, 999) == "Not found"


def test_atob():
    assert atob("Hello") == "SGVsbG8="


def test_pythagorean_distance_1():
    x = (0, 0)
    y = (0, 200)
    assert pythagorean_distance(x, y) == 200


def test_pythagorean_distance_1():
    x = (100, 200)
    y = (200, 200)
    assert pythagorean_distance(x, y) == 141.4213562373095


def test_pythagorean_distance_1():
    x = (0, 0)
    y = (200, 0)
    assert pythagorean_distance(x, y) == 200


def test_average_position():
    units = [Match(x=0, y=0), Match(x=100, y=0), Match(x=0, y=100), Match(x=100, y=100)]
    assert average_position(units) == (50, 50)


def test_safest_position():
    units = [Match(x=100, y=50), Match(x=200, y=100), Match(x=150, y=50)]
    assert safest_position(units) == (50, 100)


def test_riskiest_position():
    units = [Match(x=100, y=50), Match(x=200, y=100), Match(x=150, y=50)]
    assert riskiest_position(units) == (200, 100)


def test_merge_dicts():
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = {"b": 2, "d": 4, "e": 5}
    result = merge_dicts(dict1, dict2)
    assert isinstance(result, dict)
    assert result.get("a") == 1
    assert result.get("b") == 2
    assert result.get("e") == 5


def test_make_minimap_coods():
    assert make_minimap_coords(210, 210) == (1920, 1080)
