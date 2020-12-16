import logging
import logging.config
import os

from core.utils import get_app_dir


class CustomFileHandler(logging.FileHandler):
    """
    Allows us to log to the app directory
    """

    def __init__(self, file_name, mode):
        log_file_path = os.path.join(get_app_dir(), file_name)
        super(CustomFileHandler, self).__init__(log_file_path, mode)


def load_logging_config() -> None:
    """
    Load logging configuration from file

    :return: None
    """
    logging.config.fileConfig("logconfig.ini", disable_existing_loggers=False)


def get_logger() -> logging.Logger:
    """
    Convenience method to load the app logger

    :return: An instance of the app logger
    """
    return logging.getLogger("udemy_enroller")
