"""
motor.py
"""
import time, uuid, logging, threading
from functools import partial
from collections import defaultdict

from microbot.util import make_uuid

log = logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO
except Exception as exc:
    log.warning(f"{exc}, using no-op mock")

    class GPIO_MOCK(object):
        def __getattr__(self, prop):
            return lambda *args, **kwargs: None

    GPIO = GPIO_MOCK()


class Motor(object):

    lock = threading.Lock()

    name = None
    delay = 0.0001
    # control_pins = []
    # _state = {}  # debugging & testing, use .pins property

    position = 0
    min_position = None
    max_position = None
    sequence = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
    # 1=full, 2=half, 4=quarter step
    # mode = 1

    def __init__(
        self,
        name=None,
        control_pins=None,
        min_position=None,
        max_position=None,
        delay=None,
    ):
        # properties
        self.name = name
        self.control_pins = control_pins
        self.min_position = min_position
        self.max_position = max_position
        self.delay = delay if delay is not None else self.delay
        self._state = dict.fromkeys(self.control_pins, 0)
        # runtime checks
        if len(self._state.keys()) != len(self.control_pins):
            raise RuntimeError(f"Cannot assign duplicate control pins")
        if (self.min_position is not None) and (self.max_position is not None):
            if self.min_position > self.max_position:
                raise RuntimeError(
                    f"Minimum position cannot be greater than max position ({self.min_position} > {self.max_position})"
                )
        if len(self.control_pins) != 4:
            raise RuntimeError(
                f"Control pin array with length {len(self.control_pins)} will result in unexpected behavior"
            )
        # setup mode
        self._gpio(partial(GPIO.setmode, GPIO.BCM))
        self._gpio(partial(GPIO.setwarnings, False))
        # bulk setup pins
        self._gpio(partial(GPIO.setup, self.control_pins, GPIO.OUT, initial=GPIO.LOW))
        log.info(f"Finished initializing motor {self.name}")

    def __repr__(self):
        return "<{} at {} name={} position={}>".format(
            self.__class__.__qualname__, hex(id(self)), repr(self.name), self.position
        )

    #
    # Internal API
    #
    def _gpio(self, callback):
        # log.debug(callable)
        callback()
        pass

    def _clamp(self, target):
        if (self.min_position is not None) and (target < self.min_position):
            return self.min_position
        elif (self.max_position is not None) and (target > self.max_position):
            return self.max_position
        else:
            return target

    def _wait(self):
        time.sleep(self.delay)

    def _move(self, sequence, step):
        with self.lock:
            for seq in sequence:
                for pin, level in zip(self.control_pins, seq):
                    # level = [GPIO.LOW, GPIO.HIGH][level]  # optional?
                    self._gpio(partial(GPIO.output, pin, level))
                    self._state.update({pin: level})
                self._wait()
            self.position += step

    #
    # Public API
    #
    @property
    def pins(self):
        return self._state

    def increment(self):
        log.debug(f"Incrementing motor {self} by 1 step...")
        self._move(self.sequence, 1)
        return self.position

    def decrement(self):
        log.debug(f"Decrementing motor {self} by 1 step...")
        self._move(self.sequence[::], -1)
        return self.position

    def visit(self, position):
        # incoming websocket payload is most likely a string
        position = int(position)
        target = self._clamp(position)
        if position != target:
            log.warning(
                f"Cannot travel outside of bounds, limiting motor {self.name} position {position} to {target}"
            )
        distance = abs(target - self.position)
        operation = [self.increment, self.decrement][self.position > target]
        log.debug(f"Step distance: {distance} ({operation.__qualname__})")
        for _ in range(distance):
            operation()
        log.debug(f"Reached destination {target} for motor {self.name}")

    def state(self, value_only=False):
        if value_only:
            return self.position
        return {self.name: self.position}

    def zero(self):
        log.debug(f"Zeroing position of motor {self.name}")
        # should we set as min_position or as midpoint?
        self.position = 0
        return self.position

    # TODO: maybe change to to_dict()
    def config(self):
        return dict(
            name=self.name,
            delay=self.delay,
            position=self.position,
            min_position=self.min_position,
            max_position=self.max_position,
        )
