# microbot

https://socket.io/docs/v3/rooms/
https://github.com/miguelgrinberg/Flask-SocketIO/blob/master/example/templates/index.html
https://overiq.com/flask-101/basics-of-jinja-template-language/ MACROS

- A. Input: live display of slider value
- B. Input *disabled*: live display of current position
- C. Slider: bind on slide, update (A) live
- D. Input *disabled*: display destination position
  - as (C) is moved, update (A)
  - when (C) is released fire "onchange" update value of (D)
  - on change of (D) send command to backend to MOVE
  - as MOVE is performed, update (B) with current position


Checklist:
- logging!
- start to build out unified app structure
- notifications
  - ~~add toast notification which subscribes to both "error" and "info" messages (regular messages are of type "message")~~
- presets
  - press & hold to assign presets
  - double click preset button to move to state
  - show indicator of preset button assignment (?)
- add 'sync' button to fetch latest state from backend (for now, just reload page)
- settings:
  - speed
  - delay
  - limits
  - pin settings
  - calibration/zero individual axes

- calibration mode sets min/max position to None, which must be considered in our checks

Data Model

```js

{
    // epoch milliseconds
    // ex. 1619829580766
    time: int,
    // corresponds to the topic
    // ex. "axis.motion"
    room: str,
    // description & context
    // ex. "x-axis slider update"
    memo: str,
    // json object
    // ex. { "X": 10 }
    data: object
    // random unique identifier
    // ex. "fa80d178-b87b-4360-ad90-83ca0888d41d"
    guid: str
}

```


```py
import threading

class LockingCounter():
    def __init__(self):
        self.lock = threading.Lock()
        self.count = 0
    def increment(self):
        with self.lock:
            self.count += 1
```

## Classes
`ConfigManager`
```py


```

`StepperMotor`
```py
sm = StepperMotor(name="X")

sm.visit(position)
sm.increment()
sm.decrement()

sm.state()

sm.zero()
sm.set_min_position(min_position)
sm.set_max_position(max_position)
sm.set_mode(1) # half-step, full-step

with sm.calibration_mode() as ctx:
  pass

repr(sm)
```

`RoomManager`
```py
# start as just an Enum class for room name strings
from enum import Enum

class Rooms(Enum):
  # Stepper Motors
  XAXIS
  YAXIS
  ZAXIS
  # Notifications
  INFO
  ERROR
  # Configuration
  CONFIG
  # Calibration
  CALIBRATION
  # Presets
  PRESET
```

`MotorManager`
```py
mm = MotorManager()

mm.visit({"X": 10})
mm.increment("X")
mm.decrement("X")

mm.state()

mm["X"]

repr(mm)
```

`PresetManager`
```py
pm = PresetManager()

pm.set({"A": {
  "X": 10
}})
pm.get("A")

pm.state()

repr(pm)
```

```py
controller = Controller(
  motors = {
    "X": Motor(name="X", control_pins=[0,1,2,3], min_position=0, max_position=100),
    "Y": Motor(name="Y", control_pins=[4,5,6,7], min_position=0, max_position=100),
    "Z": Motor(name="Z", control_pins=[8,9,10,11], min_position=-45, max_position=45),
  },
  presets = {
    "A": Preset(name="A"),
    "B": Preset(name="B"),
  }
)

controller.visit({"X": 5, "Y": 5, "Z": 0})

controller.presets["A"].state()
controller.presets["A"].assign({"X": 5, "Y": 5, "Z": 0})

controller.visit(
  controller.presets["A"].state()
)


```
