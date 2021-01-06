import asyncio
from functools import reduce
from typing import List

from core.scrapers.comidoc import ComidocScraper
from core.scrapers.tutorialbar import TutorialBarScraper


class ScraperManager:
    def __init__(self, tutorialbar_enabled, comidoc_enabled, max_pages):
        self.tutorialbar_scraper = TutorialBarScraper(
            tutorialbar_enabled, max_pages=max_pages
        )
        self.comidoc_scraper = ComidocScraper(comidoc_enabled, max_pages=max_pages)
        self._scrapers = (self.tutorialbar_scraper, self.comidoc_scraper)

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
