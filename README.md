# microbot 🎤 🤖


### TODO:
- spend some time working-out how we want to handle return types, focusing on reducing the cases where we perform an action and then immediately query for the state
- broadcase more logs to the interface with specific values for visual verification
- expand test cases to cover recognized issues, especially with applying/assigning presets
- create some basic documentation and expand the readme to look nice at a glance
- need some way of showing the user which state values are associated with each preset button
- settings page which allows runtime adjustment of properties such as delay, step mode, min/max, etc
- calibration workflow and code, including test cases


- A. Input: live display of slider value
- B. Input *disabled*: live display of current position
- C. Slider: bind on slide, update (A) live
- D. Input *disabled*: display destination position
  - as (C) is moved, update (A)
  - when (C) is released fire "onchange" update value of (D)
  - on change of (D) send command to backend to MOVE
  - as MOVE is performed, update (B) with current position


Websocket Message - Data Model

```js

{
    // what is the purpose of the message?
    // ex. "info" | "error" | "message"
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
    // arbitrary payload
    // ex. { "X": 10 } | "A"
    data: any
    // random unique identifier
    // ex. "fa80d178-b87b-4360-ad90-83ca0888d41d"
    guid: str
}
```
