import logging
from multiprocessing.dummy import Pool
from typing import List

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("udemy_enroller")


class TutorialBarScraper:
    """
    Contains any logic related to scraping of data from tutorialbar.com
    """

    DOMAIN = "https://www.tutorialbar.com"
    AD_DOMAINS = ("https://amzn",)

    def __init__(self, max_pages=None):
        self.current_page = 0
        self.last_page = None
        self.links_per_page = 12
        self.max_pages = max_pages

    def run(self) -> List:
        """
        Runs the steps to scrape links from tutorialbar.com

        :return: list of udemy coupon links
        """
        self.current_page += 1
        logger.info("Please Wait: Getting the course list from tutorialbar.com...")
        course_links = self.get_course_links(
            f"{self.DOMAIN}/all-courses/page/{self.current_page}/"
        )

        logger.info(f"Page: {self.current_page} of {self.last_page} scraped")
        udemy_links = self.gather_udemy_course_links(course_links)
        filtered_udemy_links = self._filter_ad_domains(udemy_links)

        for counter, course in enumerate(filtered_udemy_links):
            logger.info(f"Received Link {counter + 1} : {course}")

        return filtered_udemy_links

    def script_should_run(self) -> bool:
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
        return should_run

    def is_first_loop(self) -> bool:
        """
        Simple check to see if this is the first time we have executed

        :return: boolean showing if this is the first loop of the script
        """
        return self.current_page == 1

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

    def get_course_links(self, url: str) -> List:
        """
        Gets the url of pages which contain the udemy link we want to get

        :param str url: The url to scrape data from
        :return: list of pages on tutorialbar.com that contain Udemy coupons
        """
        response = requests.get(url=url)

        soup = BeautifulSoup(response.content, "html.parser")

        links = soup.find_all("h3")
        course_links = [link.find("a").get("href") for link in links]

        self.last_page = (
            soup.find("li", class_="next_paginate_link").find_previous_sibling().text
        )

        return course_links

    @staticmethod
    def get_udemy_course_link(url: str) -> str:
        """
        Gets the udemy course link

        :param str url: The url to scrape data from
        :return: Coupon link of the udemy course
        """
        response = requests.get(url=url)
        soup = BeautifulSoup(response.content, "html.parser")
        udemy_link = soup.find("span", class_="rh_button_wrapper").find("a").get("href")
        return udemy_link

    def gather_udemy_course_links(self, courses: List[str]) -> List:
        """
        Threaded fetching of the udemy course links from tutorialbar.com

        :param list courses: A list of tutorialbar.com course links we want to fetch the udemy links for
        :return: list of udemy links
        """
        thread_pool = Pool()
        results = thread_pool.map(self.get_udemy_course_link, courses)
        thread_pool.close()
        thread_pool.join()
        return results
