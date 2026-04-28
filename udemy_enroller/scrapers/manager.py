"""Manager for scrapers."""

import asyncio
from functools import reduce

from udemy_enroller.scrapers.coursevania import CoursevaniaScraper
from udemy_enroller.scrapers.discudemy import DiscUdemyScraper
from udemy_enroller.scrapers.freebiesglobal import FreebiesglobalScraper
from udemy_enroller.scrapers.idownloadcoupon import IDownloadCouponScraper
from udemy_enroller.scrapers.tutorialbar import TutorialBarScraper


class ScraperManager:
    """Manages the scrapers."""

    def __init__(
        self,
        idownloadcoupon_enabled: bool,
        freebiesglobal_enabled: bool,
        tutorialbar_enabled: bool,
        discudemy_enabled: bool,
        coursevania_enabled: bool,
        max_pages: int | None,
    ):
        """Initialize."""
        self.idownloadcoupons_scraper = IDownloadCouponScraper(
            idownloadcoupon_enabled, max_pages=max_pages
        )

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
            self.idownloadcoupons_scraper,
            self.freebiesglobal_scraper,
            self.tutorialbar_scraper,
            self.discudemy_scraper,
            self.coursevania_scraper,
        )

    async def run(self) -> list[str]:
        """
        Run any enabled scrapers and returns a list of links.

        :return: list of udemy course URLs
        """
        urls: list[str] = []
        enabled_scrapers = self._enabled_scrapers()
        if enabled_scrapers:
            urls = reduce(
                list.__add__,
                await asyncio.gather(*map(lambda sc: sc.run(), enabled_scrapers)),
            )
        return urls

    def _enabled_scrapers(self) -> list:
        """Return a list of scrapers that should run."""
        return list(filter(lambda sc: sc.should_run(), self._scrapers))
