"""Logging utilities."""
import functools
import logging
import logging.handlers
import time

from opencensus.ext.azure.log_exporter import AzureLogHandler

from chris.app import settings


DEFAULT_LOG_SIZE = 5000000
DEFAULT_N_BACKUPS = 5


logger = logging.getLogger(__name__)


def _register_file_handler() -> None:
    file_handler = logging.handlers.RotatingFileHandler(
        settings.LOG_FILE_NAME, maxBytes=DEFAULT_LOG_SIZE, backupCount=DEFAULT_N_BACKUPS)
    file_formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d (%(levelname)s) %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def _register_azure_handler() -> None:
    key = settings.INSTRUMENTATION_KEY
    if key is None or key == '':
        logger.info("INSTRUMENTATION_KEY not set, logging locally")
    else:
        logger.info("INSTRUMENTATION_KEY set, starting to log remotely")
        azure_handler = AzureLogHandler(connection_string=f'InstrumentationKey={key}')
        azure_formatter = logging.Formatter('%(message)s')
        azure_handler.setFormatter(azure_formatter)
        logger.addHandler(azure_handler)


def initialize_logger() -> None:
    """Initialize the application logger."""
    logger.setLevel(logging.DEBUG)
    _register_file_handler()
    _register_azure_handler()


def log_context(name: str,
                tag: str = '='):
    """
    Decorate a function for logging activity.

    :param name: Name of the activity.
    :param tag: Tag for the kind of activity.
    """
    def decorator(function):
        @functools.wraps(function)
        def func_wrapper(*args, **kwargs):
            start_time = time.time()
            logger.info(f"[{tag}] Start:{name}")
            result = function(*args, **kwargs)
            total_time = round(time.time() - start_time, 5)
            logger.info(f"[{tag}] End:{name}, Time:{total_time}")
            return result
        return func_wrapper
    return decorator
