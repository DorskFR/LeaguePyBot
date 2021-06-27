from LPBv2.controller import Action, Keyboard, Mouse, Hotkeys

import pytest


@pytest.fixture
def action():
    return Action()


def test_action_init_without_injection(action):
    assert isinstance(action.mouse, Mouse)
    assert isinstance(action.keyboard, Keyboard)
    assert isinstance(action.hotkeys, Hotkeys)


class Fake:
    pass


def test_action_init_with_injection():
    action = Action(mouse=Fake(), keyboard=Fake(), hotkeys=Fake())
    assert isinstance(action.mouse, Fake)
    assert isinstance(action.keyboard, Fake)
    assert isinstance(action.hotkeys, Fake)
