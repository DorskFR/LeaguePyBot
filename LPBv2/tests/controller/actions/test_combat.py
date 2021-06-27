from LPBv2.controller import Combat, Action, Keyboard, Mouse, Hotkeys

import pytest


@pytest.fixture
def combat():
    return Combat()


def test_action_init_without_injection(combat):
    assert isinstance(combat, Action)
    assert isinstance(combat.mouse, Mouse)
    assert isinstance(combat.keyboard, Keyboard)
    assert isinstance(combat.hotkeys, Hotkeys)
