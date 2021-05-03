import pytest
from microbot.controller import Controller
from microbot.motor import Motor
from microbot.preset import Preset


def test_controller_constructor():
    controller = Controller(
        motors={
            "X": Motor(
                name="X", control_pins=[0, 1, 2, 3], min_position=0, max_position=100
            ),
            "Y": Motor(
                name="Y", control_pins=[4, 5, 6, 7], min_position=0, max_position=100
            ),
            "Z": Motor(
                name="Z", control_pins=[8, 9, 10, 11], min_position=-45, max_position=45
            ),
        },
        presets={
            "A": Preset(name="A"),
            "B": Preset(name="B"),
        },
    )
    assert controller.get_motor_state() == {"X": 0, "Y": 0, "Z": 0}

    assert controller.get_motor_state("X") == 0
    assert controller.get_motor_state("Y") == 0
    assert controller.get_motor_state("Z") == 0

    assert controller.get_preset_state("A") == {"A": {}}
    assert controller.get_preset_state("A") == {"A": {}}

    assert controller.get_preset_state("B", value_only=True) == {}
    assert controller.get_preset_state("B", value_only=True) == {}


def test_controller_presets():
    controller = Controller(
        motors={
            "X": Motor(
                name="X", control_pins=[0, 1, 2, 3], min_position=0, max_position=100
            ),
            "Y": Motor(
                name="Y", control_pins=[4, 5, 6, 7], min_position=0, max_position=100
            ),
            "Z": Motor(
                name="Z", control_pins=[8, 9, 10, 11], min_position=-45, max_position=45
            ),
        },
        presets={
            "A": Preset(name="A"),
            "B": Preset(name="B"),
        },
    )

    controller.assign_preset("A", {"X": 1, "Y": 2, "Z": 3})
    assert controller.get_preset_state("A", value_only=True) == {"X": 1, "Y": 2, "Z": 3}


def test_controller_motors():
    controller = Controller(
        motors={
            "X": Motor(
                name="X", control_pins=[0, 1, 2, 3], min_position=0, max_position=100
            ),
            "Y": Motor(
                name="Y", control_pins=[4, 5, 6, 7], min_position=0, max_position=100
            ),
            "Z": Motor(
                name="Z", control_pins=[8, 9, 10, 11], min_position=-45, max_position=45
            ),
        },
        presets={
            "A": Preset(name="A"),
            "B": Preset(name="B"),
        },
    )

    controller.visit_position({"X": 1, "Y": 2, "Z": 3})
    # check internal state
    assert controller.motors["X"].state(value_only=True) == 1
    assert controller.motors["Y"].state(value_only=True) == 2
    assert controller.motors["Z"].state(value_only=True) == 3
    # check api state
    assert controller.get_motor_state("X") == 1
    assert controller.get_motor_state("Y") == 2
    assert controller.get_motor_state("Z") == 3
    assert controller.get_motor_state() == {"X": 1, "Y": 2, "Z": 3}


def test_controller_autonomy():
    controller = Controller(
        motors={
            "X": Motor(
                name="X", control_pins=[0, 1, 2, 3], min_position=0, max_position=100
            ),
            "Y": Motor(
                name="Y", control_pins=[4, 5, 6, 7], min_position=0, max_position=100
            ),
            "Z": Motor(
                name="Z", control_pins=[8, 9, 10, 11], min_position=-45, max_position=45
            ),
        },
        presets={
            "A": Preset(name="A"),
            "B": Preset(name="B"),
        },
    )
    controller.assign_preset("A", {"X": 1, "Y": 2, "Z": 3})
    controller.apply_preset("A")
    assert controller.get_motor_state() == {"X": 1, "Y": 2, "Z": 3}
