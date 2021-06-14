import logging
from .formatter import CustomFormatter


def get_logger():
    logger = logging.getLogger("LeaguePyBotV2")
    logger.setLevel(logging.DEBUG)

    # Removing duplicate handlers when instanciating the logger in multiple files
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.propagate = False

    # Logging to a file
    fh = logging.FileHandler("_client.log")
    fh.setLevel(logging.DEBUG)
    simpleFormatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )
    fh.setFormatter(simpleFormatter)
    logger.addHandler(fh)

    # Logging to console with color
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)

    return logger