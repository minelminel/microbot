"""
room.py
"""
import logging
from enum import Enum

log = logging.getLogger(__name__)


class Room(Enum):
    # all motors use the same room with the motor specified in the 'data' property
    MOTOR = "motor"
    # these messages are used to push toast notifications in the interface
    INFO = "info"
    ERROR = "error"


# DRIVER
if __name__ == "__main__":
    print(Room)
    print(Room.MOTOR.value)
    print(Room.MOTOR)
    print(Room["MOTOR"])
