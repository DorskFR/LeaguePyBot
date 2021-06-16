import logging
from .formatter import CustomFormatter
import os
import time


def get_logger(name="LPBv2"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Removing duplicate handlers when instanciating the logger in multiple files
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.propagate = False

    # preparing folder and file
    logfolder = "leaguepybotv2/logs"
    if not os.path.exists(logfolder):
        os.makedirs(logfolder)
    logfile = logfolder + "/client_" + str(time.time()) + ".log"

    # Logging to a file
    fh = logging.FileHandler(logfile)
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
