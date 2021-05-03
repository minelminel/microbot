import pytest
from microbot.preset import Preset


def test_preset_constructor():
    preset = Preset(name="A")
    assert preset.name == "A"
    assert preset.state() == {}


def test_preset_assignment():
    preset = Preset(name="A")
    preset.assign({"X": 1, "Y": 2, "Z": 3})
    assert preset.state() == {"X": 1, "Y": 2, "Z": 3}
    preset.assign({"X": 4, "Y": 5, "Z": 6})
    assert preset.state() == {"X": 4, "Y": 5, "Z": 6}
