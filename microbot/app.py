"""
app.py
"""
import time, uuid, logging
from flask import Blueprint, current_app, render_template, url_for, jsonify, request
from flask_socketio import (
    SocketIO,
    send,
    emit,
    join_room,
    leave_room,
    close_room,
    rooms,
    disconnect,
)

from microbot.room import Room
from microbot.motor import Motor
from microbot.preset import Preset
from microbot.controller import Controller
from microbot.message import Message, MessageSchema

log = logging.getLogger(__name__)

bp = Blueprint("app", __name__)
socketio = SocketIO()

controller = Controller(
    motors={
        "X": Motor(
            name="X", control_pins=[0, 1, 2, 3], min_position=0, max_position=100
        ),
        "Y": Motor(
            name="Y", control_pins=[4, 5, 6, 7], min_position=0, max_position=100
        ),
        "Z": Motor(
            name="Z", control_pins=[8, 9, 10, 11], min_position=-45, max_position=45
        ),
    },
    presets={
        "A": Preset(name="A"),
        "B": Preset(name="B"),
    },
)
schema = MessageSchema()


def broadcast_state():
    # TODO: refactor into isolated events
    state = controller.get_motor_state()
    log.debug(f"Broadcasting motor state: {state}")
    reply = schema.dump(
        {
            "type": Room.MOTOR.value,
            "memo": f"Receiving broadcasted motor state: {state}",
            "data": state,
        }
    )
    emit(Room.MOTOR.value, reply)


@socketio.on(Room.PRESET_ASSIGN.value)
def handle_preset_assign(msg):
    """
    Incoming message .data property is a string corresponding to the preset
    key which should be updated using the current motor position state.
    """
    log.info(msg)
    msg = schema.load(msg)
    # TODO: error handling
    controller.assign_preset(msg.data)
    reply = schema.dump(
        {
            "type": Room.INFO.value,
            "memo": f"Preset {msg.data} assigned successfully",
        }
    )
    emit(
        Room.LOG.value,
        reply,
    )


@socketio.on(Room.PRESET_APPLY.value)
def handle_preset_apply(msg):
    """
    Incoming message .data property is a string corresponding to the preset
    key which should be applied using the stored motor position state.
    """
    log.info(msg)
    msg = schema.load(msg)
    # TODO: error handling
    controller.apply_preset(msg.data)
    reply = schema.dump(
        {"type": Room.INFO.value, "memo": f"Preset {msg.data} applied successfully"}
    )
    emit(
        Room.LOG.value,
        reply,
    )
    broadcast_state()


@socketio.on(Room.MOTOR.value)
def handle_motor_visit(msg):
    """
    Incoming message .data property is a key-value pair of the motor we wish to
    control and the target position to move it to.
    """
    msg = schema.load(msg)
    # TODO: error handling
    controller.visit_position(msg.data)
    reply = schema.dump(
        {"type": Room.INFO.value, "memo": f"Motor position updated: {msg.data}"}
    )
    emit(Room.LOG.value, reply)
    broadcast_state()


@bp.route("/")
def index():
    return render_template("index.html", motors=controller.get_motor_config())


@bp.route("/settings")
def settings():
    return jsonify(settings={})
