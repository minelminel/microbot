"""
controller.py
"""
import json, logging

from microbot.motor import Motor
from microbot.preset import Preset

log = logging.getLogger(__name__)


class Controller(object):
    """
    Manager class for interaction with stepper motors and location presets.

        Controller(motors={}, presets={})

    Attributes
    ----------
        motors : dict
        presets : dict

    Methods
    -------
    Presets
        get_preset_state(preset: str)
        assign_preset(preset: str, state: dict)
        apply_preset(preset: str)
    Motors
        get_motor_state(motor: str)
        visit_position(state: dict)
        get_motor_config(motor: str)
    """

    _motors = None
    _presets = None

    def __init__(self, motors=None, presets=None) -> None:
        self._motors = motors if motors is not None else {}
        self._presets = presets if presets is not None else {}

    def __repr__(self) -> str:
        return "<{} at {} motors={}> presets={}>".format(
            self.__class__.__qualname__,
            hex(id(self)),
            tuple(self._motors.keys()),
            tuple(self._presets.keys()),
        )

    @classmethod
    def from_config(cls, filepath):
        log.info(f"Loading configuration file: {filepath}")
        with open(filepath, "r") as file:
            config = json.load(file)

        return cls(
            motors={
                key: Motor(**kwargs) for key, kwargs in config.get("motors", {}).items()
            },
            presets={
                key: Preset(**kwargs)
                for key, kwargs in config.get("presets", {}).items()
            },
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
        log.debug(f"Fetching preset state: {preset}")
        return self._presets[preset].state(value_only)

    def assign_preset(self, preset: str) -> None:
        log.debug(f"Assigning preset: {preset}")
        self._presets[preset].assign(self.get_motor_state())

    def apply_preset(self, preset: str) -> None:
        log.debug(f"Applying preset: {preset}")
        self.visit_position(self._presets[preset].state(value_only=True))

    def get_motor_state(self, motor=None):
        if motor:
            log.debug(f"Fetching motor state: {motor}")
            return self._motors[motor].state(value_only=True)
        log.debug(f"Fetching all motor states")
        return {k: v.state(value_only=True) for k, v in self._motors.items()}

    def visit_position(self, state: dict) -> None:
        log.debug(f"Visiting motor position: {state}")
        for motor, position in state.items():
            self._motors[motor].visit(position)

    # TODO: add test cases
    def get_motor_config(self, motor: str = None) -> dict:
        if motor:
            log.debug(f"Getting motor config: {motor}")
            return self._motors[motor].config()
        log.debug(f"Getting all motor configs")
        return {k: v.config() for k, v in self._motors.items()}
