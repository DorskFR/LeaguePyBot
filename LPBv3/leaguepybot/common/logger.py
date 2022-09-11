import logging
import os

from rich.logging import RichHandler


def get_logger(
    name: str = "LPBv3", level: int = logging.DEBUG, log_to_file: bool = False
) -> logging.Logger:
    logger = logging.getLogger(name)
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )

    if log_to_file:
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.propagate = False

        # preparing folder and file
        logfolder = "logs"
        if not os.path.exists(logfolder):
            os.makedirs(logfolder)
        logfile = f"{logfolder}/{name}.log"

        # Logging to a file
        fh = logging.FileHandler(logfile)
        fh.setLevel(level)
        simpleFormatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
        )
        fh.setFormatter(simpleFormatter)
        logger.addHandler(fh)

    return logger
