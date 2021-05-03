import pytest, json, tempfile
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

    assert controller.get_preset_state("A") == {}
    assert controller.get_preset_state("B") == {}


def test_controller_from_config():
    data = {
        "motors": {
            "X": {"name": "X", "control_pins": [0, 1, 2, 3]},
            "Y": {"name": "Y", "control_pins": [4, 5, 6, 7]},
            "Z": {"name": "Z", "control_pins": [8, 9, 10, 11]},
        },
        "presets": {"A": {"name": "A"}, "B": {"name": "B"}},
    }
    with tempfile.NamedTemporaryFile(mode="w") as temp:
        with open(temp.name, "w") as file:
            json.dump(data, file)
        controller = Controller.from_config(temp.name)
    assert isinstance(controller, Controller)


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
    controller.visit_position({"X": 1, "Y": 2, "Z": 3})
    controller.assign_preset("A")
    assert controller.get_preset_state("A") == {"X": 1, "Y": 2, "Z": 3}


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


def test_controller_workflow():
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
    # check baseline states
    assert controller.presets["A"].state() == {}
    assert controller.presets["B"].state() == {}
    assert controller.get_motor_state() == {"X": 0, "Y": 0, "Z": 0}
    # move to new position
    controller.visit_position({"X": 1, "Y": 2, "Z": 3})
    assert controller.get_motor_state() == {"X": 1, "Y": 2, "Z": 3}
    assert controller.presets["A"].state() == {}
    assert controller.presets["B"].state() == {}
    # assign preset, make sure other is not affected
    controller.assign_preset("A")
    assert controller.presets["A"].state() == {"X": 1, "Y": 2, "Z": 3}
    assert controller.presets["B"].state() == {}
    # apply preset, check position
    controller.apply_preset("A")
    assert controller.get_motor_state() == {"X": 1, "Y": 2, "Z": 3}
    assert controller.presets["A"].state() == {"X": 1, "Y": 2, "Z": 3}
    assert controller.presets["B"].state() == {}
