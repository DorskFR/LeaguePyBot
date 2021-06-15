import logging
from .colors import Colors


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: Colors.dark_grey + format + Colors.reset,
        logging.INFO: Colors.grey + format + Colors.reset,
        logging.WARNING: Colors.yellow + format + Colors.reset,
        logging.ERROR: Colors.red + format + Colors.reset,
        logging.CRITICAL: Colors.bold_red + format + Colors.reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
