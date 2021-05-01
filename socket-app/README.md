https://socket.io/docs/v3/rooms/
https://github.com/miguelgrinberg/Flask-SocketIO/blob/master/example/templates/index.html

- A. Input: live display of slider value
- B. Input *disabled*: live display of current position
- C. Slider: bind on slide, update (A) live
- D. Input *disabled*: display destination position
  - as (C) is moved, update (A)
  - when (C) is released fire "onchange" update value of (D)
  - on change of (D) send command to backend to MOVE
  - as MOVE is performed, update (B) with current position


Checklist:
- add toast notification which subscribes to both "error" and "info" messages (regular messages are of type "message")
- should we have a SPA with view control, or multiple pages? can configuration be a modal?
- press & hold to assign presets
- double click preset button to move to state
- show indicator of preset button assignment
- disable slider while in motion (or use Lock on backend)
- add 'sync' button to fetch latest state from backend
- settings:
  - speed
  - delay
  - limits
  - pin settings
  - calibration/zero individual axes

- How do we want to handle global info/error messages? Should these be a specific channel or should we use a minimal router?

Data Model

```js

{
    // is this a message or error
    // ex. "message" | "info" | "error"
    type: str,
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
    // who sent the message
    // ex. "client" | "server"
    from: str
}

```
