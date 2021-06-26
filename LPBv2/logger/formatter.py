import logging
from .colors import Colors


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    timestamp = f"{Colors.dark_grey}%(asctime)s{Colors.reset} - "
    name = f"{Colors.green}%(name)s{Colors.reset} - "
    levelname = f"%(levelname)s{Colors.reset} - "
    message = f"%(message)s"
    filename = f" {Colors.dark_grey}(%(filename)s:%(lineno)d){Colors.reset}"

    before = timestamp + name
    after = message + filename

    FORMATS = {
        logging.DEBUG: before + Colors.dark_grey + levelname + Colors.dark_grey + after,
        logging.INFO: before + Colors.light_blue + levelname + Colors.reset + after,
        logging.WARNING: before
        + Colors.yellow
        + levelname
        + Colors.yellow
        + message
        + Colors.reset
        + filename,
        logging.ERROR: before
        + Colors.red
        + levelname
        + Colors.red
        + message
        + Colors.reset
        + filename,
        logging.CRITICAL: before
        + Colors.bold_red
        + levelname
        + Colors.bold_red
        + message
        + Colors.reset
        + filename,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
