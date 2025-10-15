"""Tutorialbar scraper."""
import asyncio
from typing import List

from bs4 import BeautifulSoup

from udemy_enroller.http_utils import http_get
from udemy_enroller.logger import get_logger
from udemy_enroller.scrapers.base_scraper import BaseScraper

logger = get_logger()


class TutorialBarScraper(BaseScraper):
    """Contains any logic related to scraping of data from tutorialbar.com."""

    DOMAIN = "https://www.tutorialbar.com"
    AD_DOMAINS = ("https://amzn", "https://bit.ly")

    def __init__(self, enabled, max_pages=None):
        """Initialize."""
        super().__init__()
        self.scraper_name = "tutorialbar"
        if not enabled:
            self.set_state_disabled()
        self.last_page = None
        self.max_pages = max_pages

    @BaseScraper.time_run
    async def run(self) -> List:
        """
        Run the steps to scrape links from tutorialbar.com.

        :return: list of udemy coupon links
        """
        links = await self.get_links()
        self.max_pages_reached()
        return links

    async def get_links(self):
        """
        Scrape udemy links from tutorialbar.com.

        :return: List of udemy course urls
        """
        self.current_page += 1
        course_links = await self.get_course_links(
            f"{self.DOMAIN}/all-courses/page/{self.current_page}/"
        )

        logger.info(
            f"Page: {self.current_page} of {self.last_page} scraped from tutorialbar.com"
        )
        udemy_links = await self.gather_udemy_course_links(course_links)
        links = self._filter_ad_domains(udemy_links)

        for counter, course in enumerate(links):
            logger.debug(f"Received Link {counter + 1} : {course}")

        return links

    def _filter_ad_domains(self, udemy_links) -> List:
        """
        Filter out any known ad domains from the links scraped.

        :param list udemy_links: List of urls to filter ad domains from
        :return: A list of filtered urls
        """
        ad_links = set()
        for link in udemy_links:
            for ad_domain in self.AD_DOMAINS:
                if link.startswith(ad_domain):
                    ad_links.add(link)
        if ad_links:
            logger.info(f"Removing ad links from courses: {ad_links}")
        return list(set(udemy_links) - ad_links)

    async def get_course_links(self, url: str) -> List:
        """
        Get the url of pages which contain the udemy link we want to get.

        :param str url: The url to scrape data from
        :return: list of pages on tutorialbar.com that contain Udemy coupons
        """
        text = await http_get(url)
        if text is not None:
            soup = BeautifulSoup(text.decode("utf-8"), "html.parser")

            links = soup.find_all("h3")
            course_links = []
            for link in links:
                anchor = link.find("a")
                if anchor and anchor.get("href"):
                    course_links.append(anchor.get("href"))

            next_page_elem = soup.find("li", class_="next_paginate_link")
            if next_page_elem and next_page_elem.find_previous_sibling():
                self.last_page = next_page_elem.find_previous_sibling().text
            else:
                self.last_page = "1"

            return course_links

    @staticmethod
    async def get_udemy_course_link(url: str) -> str:
        """
        Get the udemy course link.

        :param str url: The url to scrape data from
        :return: Coupon link of the udemy course
        """
        text = await http_get(url)
        if text is not None:
            soup = BeautifulSoup(text.decode("utf-8"), "html.parser")
            button_wrapper = soup.find("span", class_="rh_button_wrapper")
            if button_wrapper:
                anchor = button_wrapper.find("a")
                if anchor and anchor.get("href"):
                    return anchor.get("href")
        return None

    async def gather_udemy_course_links(self, courses: List[str]):
        """
        Async fetching of the udemy course links from tutorialbar.com.

        :param list courses: A list of tutorialbar.com course links we want to fetch the udemy links for
        :return: list of udemy links
        """
        return [
            link
            for link in await asyncio.gather(*map(self.get_udemy_course_link, courses))
            if link is not None
        ]
