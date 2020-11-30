import logging.config

from .cache import CourseCache
from .settings import Settings
from .tutorialbar import TutorialBarScraper
from .udemy import UdemyActions

logging.config.fileConfig("logconfig.ini", disable_existing_loggers=False)
