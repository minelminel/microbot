"""
config.py
"""
import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:

    SECRET_KEY = "nukethewhales"
    LOG_LEVEL = "DEBUG"
    LOG_FILE = None
    LOG_OVERRIDES = {"werkzeug": "WARNING"}
    MICROBOT_CONFIG = os.path.join(root, "config.json")
