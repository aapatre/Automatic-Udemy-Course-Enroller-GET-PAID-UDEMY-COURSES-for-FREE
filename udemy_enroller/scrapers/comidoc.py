import asyncio
import logging
from typing import List

from bs4 import BeautifulSoup

from udemy_enroller.http import get
from udemy_enroller.scrapers.base_scraper import BaseScraper

logger = logging.getLogger("udemy_enroller")


class ComidocScraper(BaseScraper):
    """
    Contains any logic related to scraping of data from comidoc.net
    """

    DOMAIN = "https://comidoc.net"

    def __init__(self, enabled, max_pages=None):
        super().__init__()
        self.scraper_name = "comidoc"
        if not enabled:
            self.set_state_disabled()
        self.max_pages = max_pages

    @BaseScraper.time_run
    async def run(self) -> List:
        """
        Called to gather the udemy links

        :return: List of udemy course links
        """
        links = await self.get_links()
        logger.info(
            f"Page: {self.current_page} of {self.last_page} scraped from comidoc.net"
        )
        self.max_pages_reached()
        return links

    async def get_links(self) -> List:
        """
        Scrape udemy links from comidoc.net

        :return: List of udemy course urls
        """
        comidoc_links = []
        self.current_page += 1
        coupons_data = await get(f"{self.DOMAIN}/coupons?page={self.current_page}")
        soup = BeautifulSoup(coupons_data.decode("utf-8"), "html.parser")
        for course_card in soup.find_all("div", class_="MuiPaper-root"):
            all_links = course_card.find_all("a")
            if len(all_links) == 2:
                comidoc_links.append(f"{self.DOMAIN}{all_links[1].get('href')}")

        links = await self.gather_udemy_course_links(comidoc_links)
        self.last_page = self._get_last_page(soup)

        return links

    @classmethod
    async def get_udemy_course_link(cls, url: str) -> str:
        """
        Gets the udemy course link

        :param str url: The url to scrape data from
        :return: Coupon link of the udemy course
        """

        data = await get(url)
        soup = BeautifulSoup(data.decode("utf-8"), "html.parser")
        for link in soup.find_all("a", href=True):
            udemy_link = cls.validate_coupon_url(link["href"])
            if udemy_link is not None:
                return udemy_link

    async def gather_udemy_course_links(self, courses: List[str]):
        """
        Async fetching of the udemy course links from comidoc.net

        :param list courses: A list of comidoc.net course links we want to fetch the udemy links for
        :return: list of udemy links
        """
        return [
            link
            for link in await asyncio.gather(*map(self.get_udemy_course_link, courses))
            if link is not None
        ]

    @staticmethod
    def _get_last_page(soup: BeautifulSoup) -> int:
        """
        Extract the last page number to scrape

        :param soup:
        :return: The last page number to scrape
        """
        all_pages = []
        for page_link in soup.find("ul", class_="MuiPagination-ul").find_all("li"):
            pagination = page_link.find("a")

            if pagination:
                page_number = pagination["aria-label"].split()[-1]
                if page_number.isdigit():
                    all_pages.append(int(page_number))

        return max(all_pages)
