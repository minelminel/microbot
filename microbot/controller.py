"""
controller.py
"""
import logging

log = logging.getLogger(__name__)


class Controller(object):

    _motors = {}
    _presets = {}

    def __init__(self, motors=None, presets=None) -> None:
        self._motors = motors if motors is not None else self._motors
        self._presets = presets if presets is not None else self._presets

    def __repr__(self) -> str:
        return "<{} at {} motors={}> presets={}>".format(
            self.__class__.__qualname__,
            hex(id(self)),
            tuple(self._motors.keys()),
            tuple(self._presets.keys()),
        )

    #
    # Internal API
    #

    #
    # External API
    #
    @property
    def motors(self):
        return self._motors

    @property
    def presets(self):
        return self._presets

    def get_preset_state(self, preset: str, value_only=False) -> dict:
        log.info(f"Fetching preset state: {preset}")
        return self._presets[preset].state(value_only)

    def assign_preset(self, preset: str, state: dict) -> None:
        log.info(f"Assigning preset: {preset}")
        self._presets[preset].assign(state)

    def apply_preset(self, preset: str) -> None:
        log.info(f"Applying preset: {preset}")
        self.visit_position(self._presets[preset].state(value_only=True))

    def get_motor_state(self, motor=None):
        log.info(f"Fetching motor state: {motor}")
        if motor:
            return self._motors[motor].state(value_only=True)
        return {k: v.state(value_only=True) for k, v in self._motors.items()}

    def visit_position(self, state: dict) -> None:
        log.info(f"Visiting motor position: {state}")
        for motor, position in state.items():
            self._motors[motor].visit(position)
