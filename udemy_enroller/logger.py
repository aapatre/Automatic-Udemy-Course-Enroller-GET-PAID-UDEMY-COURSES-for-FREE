"""Logger utilities."""

import logging
import logging.handlers

from udemy_enroller.utils import get_app_dir

LOG_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
LOG_BACKUP_COUNT = 3


class CustomRotatingFileHandler(logging.handlers.RotatingFileHandler):
    """Allows us to log to the app directory with rotation."""

    def __init__(
        self,
        file_name: str = "app.log",
        mode: str = "a",
        max_bytes: int = LOG_MAX_BYTES,
        backup_count: int = LOG_BACKUP_COUNT,
    ):
        """Initialize."""
        log_file_path = get_app_dir() / file_name
        super().__init__(log_file_path, mode, maxBytes=max_bytes, backupCount=backup_count)


def load_logging_config() -> None:
    """Load logging configuration."""
    my_logger = logging.getLogger("udemy_enroller")
    my_logger.setLevel(logging.INFO)

    # Rotating file handler
    file_handler = CustomRotatingFileHandler()
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(module)s : %(message)s"
    formatter = logging.Formatter(fmt=log_format)
    file_handler.setFormatter(formatter)
    my_logger.addHandler(file_handler)

    # Basic format for streamhandler
    stream_handler = logging.StreamHandler()
    simple_format = logging.Formatter(fmt="%(message)s")
    stream_handler.setFormatter(simple_format)
    my_logger.addHandler(stream_handler)


def get_logger() -> logging.Logger:
    """
    Get the app logger.

    :return: An instance of the app logger
    """
    return logging.getLogger("udemy_enroller")
