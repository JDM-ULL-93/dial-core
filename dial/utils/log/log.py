# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# pylint: disable=global-statement

"""Logger functions used to display debug and execution information."""

import argparse
import logging
import logging.config
import sys
from io import StringIO

FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%H:%M:%S"
)

LOG_FILE = "dial.log"
LOG_STREAM = StringIO()

LOG_LEVEL = logging.INFO


def init_logs(args: argparse.Namespace):
    """
    Initialize logging system. Defines the formatting and logging levels for all Logger
    objects.
    """
    global LOG_LEVEL

    # Set specified log level
    try:
        LOG_LEVEL = getattr(logging, args.loglevel.upper())

    except AttributeError:
        raise ValueError("Invalid log level: %s" % args.loglevel)

    # If debug flag, change log level to DEBUG
    if args.debug:
        LOG_LEVEL = logging.DEBUG

    # Configure root logger
    add_handler_to_root(__get_console_handler())
    add_handler_to_root(__get_string_handler())

    module_logger().debug("Logging system initialized.")


def add_handler_to_root(handler: logging.Handler):
    """
    Add a new handler to the logger defined as ROOT
    """
    logging.getLogger().addHandler(handler)


def get_logger(logger_name: str) -> logging.Logger:
    """
    Configure and return a Logger with `logger_name` as name.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(LOG_LEVEL)

    return logger


def module_logger() -> logging.Logger:
    """Returns a configured Logger object using its module name as identifier."""
    return get_logger(__name__)


def __get_console_handler() -> logging.StreamHandler:
    """Returns a log handler that sends its output to the terminal (stdout)."""
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)

    return console_handler


def __get_string_handler() -> logging.StreamHandler:
    """Returns a log handler that sends its output to a string."""
    string_handler = logging.StreamHandler(LOG_STREAM)
    string_handler.setFormatter(FORMATTER)

    return string_handler