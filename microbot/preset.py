"""
preset.py
"""
import logging, threading

log = logging.getLogger(__name__)


class Preset(object):

    lock = threading.Lock()
    name = None
    _state = None

    def __init__(self, name=None):
        self.name = name if name is not None else self.name
        self._state = {}

    def __repr__(self):
        return "<{} at {} state={}>".format(
            self.__class__.__qualname__, hex(id(self)), self._state
        )

    def state(self, value_only=False):
        return self._state

    def assign(self, state):
        log.debug(f"Saving preset {self.name} state: {state}")
        with self.lock:
            self._state.update(state)
