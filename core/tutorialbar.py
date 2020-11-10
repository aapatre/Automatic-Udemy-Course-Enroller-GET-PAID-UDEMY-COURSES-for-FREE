from multiprocessing.dummy import Pool
from typing import List

import requests
from bs4 import BeautifulSoup

from core import Settings


class TutorialBarScraper:
    """
    Contains any logic related to scraping of data from tutorialbar.com
    """

    DOMAIN = "https://www.tutorialbar.com"

    def __init__(self, settings: Settings):
        self.current_page = 0
        self.last_page = None
        self.all_courses_link = f"{self.DOMAIN}/all-courses/page/{self.current_page}/"
        self.links_per_page = 12
        self.settings = settings

    def run(self) -> List:
        """
        Runs the steps to scrape links from tutorialbar.com

        :return: list of udemy coupon links
        """
        self.current_page += 1
        print("Please Wait: Getting the course list from tutorialbar.com...")
        course_links = self.get_course_links(self.all_courses_link)

        print(f"Page: {self.current_page} of {self.last_page} scraped")
        udemy_links = self.gather_udemy_course_links(course_links)

        for counter, course in enumerate(udemy_links):
            print(f"Received Link {counter + 1} : {course}")

        return udemy_links

    def is_first_loop(self) -> bool:
        """
        Simple check to see if this is the first time we have executed

        :return: boolean showing if this is the first loop of the script
        """
        return self.current_page == 1

    def get_course_links(self, url: str) -> List:
        """
        Gets the url of pages which contain the udemy link we want to get

        :param str url: The url to scrape data from
        :return: list of pages on tutorialbar.com that contain Udemy coupons
        """
        response = requests.get(url=url)

        soup = BeautifulSoup(response.content, "html.parser")

        links = soup.find("div", class_="rh-post-wrapper").find_all("a")
        # print(links)

        courses = []

        x = 0
        for _ in range(12):
            if (
                    self.settings.categories
            ):  # If the categories are specified, then only add them if the category is in `categories`
                if links[x + 2].text in self.settings.categories:
                    courses.append(links[x].get("href"))
            else:  # If the categories aren't specified, just add them
                courses.append(links[x].get("href"))
            x += 3

        return courses

    @staticmethod
    def get_udemy_course_link(url: str) -> str:
        """
        Gets the udemy course link

        :param str url: The url to scrape data from
        :return: Coupon link of the udemy course
        """
        response = requests.get(url=url)
        soup = BeautifulSoup(response.content, "html.parser")
        udemy_link = soup.find(
            "span", class_="rh_button_wrapper").find("a").get("href")
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
