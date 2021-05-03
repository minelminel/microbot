"""
room.py
"""
import logging
from enum import Enum

log = logging.getLogger(__name__)


class Room(Enum):
    """
    This Enum needs to be kept synchronized with the JS object
    """

    # all motors use the same room with the motor specified in the 'data' property
    MOTOR = "motor"
    # updating the presets
    PRESET_ASSIGN = "preset.assign"
    PRESET_APPLY = "preset.apply"
    # these messages are used to push notifications in the interface
    LOG = "log"
    INFO = "info"
    ERROR = "error"


# DRIVER
if __name__ == "__main__":
    print(Room)
    print(Room.MOTOR.value)
    print(Room.MOTOR)
    print(Room["MOTOR"])
