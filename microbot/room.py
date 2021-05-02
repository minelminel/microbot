"""
room.py
"""
import logging
from enum import Enum

log = logging.getLogger(__name__)


class Rooms(Enum):
    # all motors use the same room with the motor specified in the 'data' property
    MOTOR: "motor"
    # these messages are used to push toast notifications in the interface
    INFO: "info"
    ERROR: "error"
