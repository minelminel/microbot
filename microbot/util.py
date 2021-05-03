"""
util.py
"""
import sys, logging, uuid, time

log = logging.getLogger(__name__)


def make_uuid():
    return str(uuid.uuid4())


def make_time():
    return int(time.time() * 1000)


def configure_logging(app):
    """
    Global logging configuration. Access in other modules using
    >>> import logging
    >>> log = logging.getLogger(__name__)
    """
    log_file = app.config.get("LOG_FILE", None)
    log_level = app.config.get("LOG_LEVEL", "INFO")

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(funcName)s:%(lineno)s - %(levelname)s - %(message)s"
    )
    handlers = []
    if log_file:
        file_handler = logging.FileHandler(filename=log_file, mode="a")
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(formatter)
    handlers.append(stream_handler)
    logging.basicConfig(
        datefmt="%m/%d/%Y %I:%M:%S %p", level=log_level, handlers=handlers
    )
    for _module, _level in app.config.get("LOG_OVERRIDES", {}).items():
        log.debug(f"Overriding module logging: {_module} --> {_level}")
        logging.getLogger(_module).setLevel(_level)
    return app
