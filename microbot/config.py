"""
config.py
"""


class Config:

    SECRET_KEY = "nukethewhales"
    LOG_LEVEL = "DEBUG"
    LOG_FILE = None
    LOG_OVERRIDES = {"werkzeug": "WARNING"}
