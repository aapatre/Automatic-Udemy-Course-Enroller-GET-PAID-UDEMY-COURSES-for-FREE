import asyncio
from functools import reduce
from typing import List

from udemy_enroller.scrapers.coursevania import CoursevaniaScraper
from udemy_enroller.scrapers.discudemy import DiscUdemyScraper
from udemy_enroller.scrapers.freebiesglobal import FreebiesglobalScraper
from udemy_enroller.scrapers.tutorialbar import TutorialBarScraper


class ScraperManager:
    def __init__(
        self,
        freebiesglobal_enabled,
        tutorialbar_enabled,
        discudemy_enabled,
        coursevania_enabled,
        max_pages,
    ):
        self.freebiesglobal_scraper = FreebiesglobalScraper(
            freebiesglobal_enabled, max_pages=max_pages
        )
        self.tutorialbar_scraper = TutorialBarScraper(
            tutorialbar_enabled, max_pages=max_pages
        )
        self.discudemy_scraper = DiscUdemyScraper(
            discudemy_enabled, max_pages=max_pages
        )
        self.coursevania_scraper = CoursevaniaScraper(
            coursevania_enabled, max_pages=max_pages
        )
        self._scrapers = (
            self.freebiesglobal_scraper,
            self.tutorialbar_scraper,
            self.discudemy_scraper,
            self.coursevania_scraper,
        )

    async def run(self) -> List:
        """
        Runs any enabled scrapers and returns a list of links

        :return: list
        """
        urls = []
        enabled_scrapers = self._enabled_scrapers()
        if enabled_scrapers:
            urls = reduce(
                list.__add__,
                await asyncio.gather(*map(lambda sc: sc.run(), enabled_scrapers)),
            )
        return urls

    def _enabled_scrapers(self) -> List:
        """
        Returns a list of scrapers that should run

        :return:
        """
        return list(filter(lambda sc: sc.should_run(), self._scrapers))
