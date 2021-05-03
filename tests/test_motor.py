import pytest
from microbot.motor import Motor


def test_motor_constructor():
    motor = Motor(
        name="X", min_position=-5, max_position=5, control_pins=[0, 1, 2, 3], delay=0
    )
    assert motor.name == "X"
    assert motor.min_position == -5
    assert motor.max_position == 5
    assert motor.control_pins == [0, 1, 2, 3]
    assert motor.delay == 0


def test_motor_state():
    motor = Motor(
        name="X", min_position=-5, max_position=5, control_pins=[0, 1, 2, 3], delay=0
    )
    assert motor.state() == {"X": 0}


def test_motor_increment():
    motor = Motor(
        name="X", min_position=-5, max_position=5, control_pins=[0, 1, 2, 3], delay=0
    )
    motor.increment()
    assert motor.state() == {"X": 1}
    motor.increment()
    assert motor.state() == {"X": 2}


def test_motor_decrement():
    motor = Motor(
        name="X", min_position=-5, max_position=5, control_pins=[0, 1, 2, 3], delay=0
    )
    motor.decrement()
    assert motor.state() == {"X": -1}
    motor.decrement()
    assert motor.state() == {"X": -2}


def test_motor_visit_in_range():
    motor = Motor(
        name="X", min_position=-5, max_position=5, control_pins=[0, 1, 2, 3], delay=0
    )
    motor.visit(5)
    assert motor.state() == {"X": 5}
    motor.visit(-5)
    assert motor.state() == {"X": -5}


def test_motor_visit_outside_range():
    motor = Motor(
        name="X", min_position=-5, max_position=5, control_pins=[0, 1, 2, 3], delay=0
    )
    motor.visit(6)
    assert motor.state() == {"X": 5}
    motor.visit(-6)
    assert motor.state() == {"X": -5}


def test_motor_duplicate_pins():
    with pytest.raises(RuntimeError):
        motor = Motor(control_pins=[0, 0, 1, 2])


def test_motor_increment_outside_range():
    motor = Motor(
        name="X", min_position=-5, max_position=5, control_pins=[0, 1, 2, 3], delay=0
    )
    for _ in range(10):
        motor.increment()
    assert motor.state(value_only=True) == 5


def test_motor_decrement_outside_range():
    motor = Motor(
        name="X", min_position=-5, max_position=5, control_pins=[0, 1, 2, 3], delay=0
    )
    for _ in range(10):
        motor.decrement()
    assert motor.state(value_only=True) == -5
