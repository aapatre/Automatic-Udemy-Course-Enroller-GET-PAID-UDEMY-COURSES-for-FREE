import asyncio
import logging
from typing import List

import aiohttp
from bs4 import BeautifulSoup

from core.scrapers.base_scraper import BaseScraper

logger = logging.getLogger("udemy_enroller")


class TutorialBarScraper(BaseScraper):
    """
    Contains any logic related to scraping of data from tutorialbar.com
    """

    DOMAIN = "https://www.tutorialbar.com"
    AD_DOMAINS = ("https://amzn",)

    def __init__(self, enabled, max_pages=None):
        super().__init__()
        self.scraper_name = "tutorialbar"
        if not enabled:
            self.set_state_disabled()
        self.current_page = 0
        self.last_page = None
        self.links_per_page = 12
        self.max_pages = max_pages

    @BaseScraper.time_run
    async def run(self) -> List:
        """
        Runs the steps to scrape links from tutorialbar.com

        :return: list of udemy coupon links
        """
        links = await self.get_links()
        self.max_pages_reached()
        return links

    async def get_links(self):
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

    def max_pages_reached(self) -> bool:
        """
        Returns boolean of whether or not we should continue checking tutorialbar.com

        :return:
        """

        should_run = True

        if self.max_pages is not None:
            should_run = self.max_pages > self.current_page

            if not should_run:
                logger.info(
                    f"Stopping loop. We have reached max number of pages to scrape: {self.max_pages}"
                )
                self.set_state_complete()

        return should_run

    def _filter_ad_domains(self, udemy_links) -> List:
        """
        Filter out any known ad domains from the links scraped

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
        Gets the url of pages which contain the udemy link we want to get

        :param str url: The url to scrape data from
        :return: list of pages on tutorialbar.com that contain Udemy coupons
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.read()

        soup = BeautifulSoup(text.decode("utf-8"), "html.parser")

        links = soup.find_all("h3")
        course_links = [link.find("a").get("href") for link in links]

        self.last_page = (
            soup.find("li", class_="next_paginate_link").find_previous_sibling().text
        )

        return course_links

    @staticmethod
    async def get_udemy_course_link(url: str) -> str:
        """
        Gets the udemy course link

        :param str url: The url to scrape data from
        :return: Coupon link of the udemy course
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.read()
        soup = BeautifulSoup(text.decode("utf-8"), "html.parser")
        udemy_link = soup.find("span", class_="rh_button_wrapper").find("a").get("href")
        return udemy_link

    async def gather_udemy_course_links(self, courses: List[str]):
        """
        Threaded fetching of the udemy course links from tutorialbar.com

        :param list courses: A list of tutorialbar.com course links we want to fetch the udemy links for
        :return: list of udemy links
        """
        return await asyncio.gather(*map(self.get_udemy_course_link, courses))
