import datetime
import logging
from abc import ABC, abstractmethod
from enum import Enum

logger = logging.getLogger("udemy_enroller")


class ScraperStates(Enum):
    DISABLED = "DISABLED"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"


class BaseScraper(ABC):
    def __init__(self):
        self._state = None
        self.scraper_name = None

    @abstractmethod
    async def run(self):
        return

    @abstractmethod
    async def get_links(self):
        return

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if any([ss for ss in ScraperStates if ss.value == value]):
            self._state = value

    def set_state_disabled(self):
        self.state = ScraperStates.DISABLED.value
        logger.info(f"{self.scraper_name} scraper disabled")

    def set_state_running(self):
        self.state = ScraperStates.RUNNING.value
        logger.info(f"{self.scraper_name} scraper is running")

    def set_state_complete(self):
        self.state = ScraperStates.COMPLETE.value
        logger.info(f"{self.scraper_name} scraper complete")

    def is_disabled(self):
        return self.state == ScraperStates.DISABLED.value

    def is_complete(self):
        return self.state == ScraperStates.COMPLETE.value

    def should_run(self):
        should_run = not self.is_disabled() and not self.is_complete()
        if should_run:
            self.set_state_running()
        return should_run

    @staticmethod
    def time_run(func):
        async def wrapper(self):
            start_time = datetime.datetime.utcnow()
            try:
                response = await func(self)
            except Exception as e:
                logger.error(f"Error while running {self.scraper_name} scrapper: {e}")
                self.is_complete()
                return []
            end_time = datetime.datetime.utcnow()
            logger.info(
                f"Got {len(response)} links from {self.DOMAIN} in {(end_time - start_time).total_seconds():.2f} seconds"
            )
            return response

        return wrapper
