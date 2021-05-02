"""
preset.py
"""
import logging, threading

log = logging.getLogger(__name__)


class Presets(object):

    KEYS = ("A", "B")
    lock = threading.Lock()
    store = dict.fromkeys(KEYS, None)

    def __init__(self):
        pass

    def __repr__(self):
        return "<{} at {} store={}>".format(
            self.__class__.__qualname__, hex(id(self)), self.store
        )

    def __getitem__(self, key):
        if key not in self.store:
            log.error(f"No preset located with key {key}")
            raise KeyError(f"No preset located with key {key}")
        return self.store[key]

    def state(self):
        return self.store

    def save(self, state):
        log.debug(f"Saving state: {state}")
        with self.lock:
            self.store.update(state)


# DRIVER
if __name__ == "__main__":
    presets = Presets()
    print(presets)
    print(presets.state())
    print(presets["A"])

    presets.save({"A": {"X": 5}})
    print(presets.state())
    print(presets["A"])
