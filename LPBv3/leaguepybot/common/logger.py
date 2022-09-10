import logging
import os

from rich.logging import RichHandler

FORMAT = "%(message)s"


def get_logger(
    name: str = "LPBv3", level: int = logging.DEBUG, log_to_file: bool = False
) -> logging.Logger:
    logger = logging.getLogger(name)
    logging.basicConfig(level=level, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

    # Removing duplicate handlers when instanciating the logger in multiple files
    # if logger.hasHandlers():
    #     logger.handlers.clear()
    # logger.propagate = False

    if log_to_file:
        # preparing folder and file
        logfolder = "logs"
        if not os.path.exists(logfolder):
            os.makedirs(logfolder)
        logfile = f"{logfolder}/{name}.log"

        # Logging to a file
        fh = logging.FileHandler(logfile)
        fh.setLevel(level)
        simpleFormatter = logging.Formatter(FORMAT)
        fh.setFormatter(simpleFormatter)
        logger.addHandler(fh)

    return logger
