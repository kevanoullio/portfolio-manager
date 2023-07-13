# Description: Configuration file for the application

# Standard Libraries
import logging

# Third-party Libraries

# Local Modules


# Logging configuration
DEBUG_MODE = True
LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = "[%(levelname)s] %(asctime)s (%(name)s) %(module)s - %(message)s"
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOGGING_FILENAME = "portfolio_manager.log"

def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG if DEBUG_MODE else LOGGING_LEVEL,
        format=LOGGING_FORMAT,
        datefmt=LOGGING_DATE_FORMAT,
        filename=LOGGING_FILENAME
    )
