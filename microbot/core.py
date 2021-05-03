"""
core.py
"""
import logging
from flask import Flask
from flask_socketio import SocketIO

from microbot.config import Config
from microbot.util import configure_logging

log = logging.getLogger(__name__)


def create_app(config=None):
    """
    Main application factory
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    configure_logging(app)

    from microbot.app import bp as blueprint

    app.register_blueprint(blueprint)

    from microbot.app import socketio

    socketio.init_app(app)

    return app
