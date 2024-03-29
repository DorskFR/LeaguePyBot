import logging
from .formatter import CustomFormatter
import os


def get_logger(name="LPBv2", log_to_file=False):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Removing duplicate handlers when instanciating the logger in multiple files
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.propagate = False

    if log_to_file:
        # preparing folder and file
        logfolder = "logs"
        if not os.path.exists(logfolder):
            os.makedirs(logfolder)
        logfile = f"{logfolder}/{name}.log"

        # Logging to a file
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.DEBUG)
        simpleFormatter = logging.Formatter(
            f"%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
        )

        fh.setFormatter(simpleFormatter)
        logger.addHandler(fh)

    # Logging to console with color
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)

    return logger
