from datetime import time
import logging
from logging.handlers import TimedRotatingFileHandler

from panza.jobs import add_logger_handler

_handlers = []


def logger_for_driver(name: str, debug: bool = False):
    """
    Retrieve the logger for a given driver

    :param name:                the driver name
    :param debug:               whether debug output should be logged or not (default is False)
    :return:                    the initialized logger
    """
    logger = logging.getLogger(f"rocinante:{name}")
    logger.setLevel(logging.DEBUG if debug is True else logging.INFO)
    for handler in _handlers:
        logger.addHandler(handler)
    return logger


def _register_handlers(log_directory: str):
    formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
    console_handler = logging.StreamHandler()
    file_handler = TimedRotatingFileHandler(
        f"{log_directory}/rocinante.log",
        when='midnight',
        atTime=time(hour=2),
        backupCount=7
    )
    global _handlers
    _handlers = [console_handler, file_handler]

    for handler in _handlers:
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)


def init_logging(log_directory: str, debug: bool = False) -> logging.Logger:
    """
    Initialize logging for rocinante

    :param log_directory:       the log directory to use
    :param debug:               whether debug output should be logged or not (default is False)
    :return:                    the initialized logger
    """

    _register_handlers(log_directory)

    logger = logging.getLogger("rocinante")
    logger.setLevel(logging.DEBUG if debug is True else logging.INFO)

    for handler in _handlers:
        logger.addHandler(handler)
        add_logger_handler(handler)

    return logger
