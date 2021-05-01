import time
from flask import Flask, session, render_template, url_for, jsonify
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room, rooms, disconnect

app = Flask(__name__)
app.config.update({
    "SECRET_KEY": "asdf1234"
})
socketio = SocketIO(app)

class State(object):
    min_position = 0
    max_position = 10
    current_position = 5

    def state(self):
        keys = ("min_position", "max_position", "current_position")
        return {key: getattr(self, key) for key in keys}

state = State()

LOCK = False

@socketio.on("my_event")  # namespace="/something"
def join_test(message):
    print("Joining room test!")
    print(message)
    join_room(message["room"])
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit("my_response", {
        "data": f"In rooms: {rooms()}",
        "count": session["receive_count"]
    })

@socketio.on("message")
def handle_message(msg):
    global LOCK
    if LOCK:
        print("!! LOCK ENABLED !!")
        return
    else:
        LOCK = True
    print(f"Message: {msg}, Type: {type(msg)}")
    # logic
    desired_position = int(msg)
    # how many steps do we need to take
    incr = [1, -1][desired_position < state.current_position]
    steps = abs(state.current_position - desired_position)
    for _ in range(steps):
        print(f"Stepping current position by: {incr}")
        state.current_position += incr
        time.sleep(0.01)
        send(state.current_position, broadcast=True)
    LOCK = False

@app.route("/")
def index():
    print(state.state())
    return render_template("index.html", state=state.state())

@app.route("/settings")
def settings():
    return jsonify(settings={})

if __name__ == "__main__":
    # TODO run this only in dev
    from werkzeug.debug import DebuggedApplication
    app.debug = True
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
    
    socketio.run(app)
