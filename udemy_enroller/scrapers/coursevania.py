"""Coursevania Scraper."""
import asyncio
import json
from typing import List
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from udemy_enroller.http_utils import http_get
from udemy_enroller.logger import get_logger
from udemy_enroller.scrapers.base_scraper import BaseScraper

logger = get_logger()


class CoursevaniaScraper(BaseScraper):
    """Contains any logic related to scraping of data from coursevania.com."""

    DOMAIN = "https://coursevania.com"

    def __init__(self, enabled, max_pages=None):
        """Initialize."""
        super().__init__()
        self.scraper_name = "coursevania"
        if not enabled:
            self.set_state_disabled()
        self.last_page = None
        self.max_pages = max_pages
        self._nonce = None

    @BaseScraper.time_run
    async def run(self) -> List:
        """
        Gather the udemy links.

        :return: List of udemy course links
        """
        links = await self.get_links()
        logger.info(
            f"Page: {self.current_page} of {self.last_page} scraped from coursevania.com"
        )
        self.max_pages_reached()
        return links

    async def get_links(self):
        """
        Scrape udemy links from coursevania.com.

        :return: List of udemy course urls
        """
        self.current_page += 1
        await self.load_nonce()
        course_links = await self.get_course_links()

        links = await self.gather_udemy_course_links(course_links)

        for counter, course in enumerate(links):
            logger.debug(f"Received Link {counter + 1} : {course}")

        return links

    async def load_nonce(self) -> None:
        """
        Load the nonce value needed to load the correct page data.

        :return: None
        """
        if self._nonce is None:
            response = await http_get(f"{self.DOMAIN}/courses")
            if response is not None:
                soup = BeautifulSoup(response, "html.parser")
                for script_element in soup.find_all("script"):
                    if "var stm_lms_nonces" in str(script_element):
                        data = json.loads(
                            script_element.string.split(" = ")[1].strip()[:-1]
                        )
                        self._nonce = data.get("load_content")

    async def get_course_links(self) -> List:
        """
        Get the url of pages which contain the udemy link we want to get.

        :return: list of pages on coursevania.com that contain Udemy coupons
        """
        query_params = {
            "offset": self.current_page - 1,
            "template": "courses/grid",
            "args": '{"image_d":"img-480-380","per_row":"4","posts_per_page":"12","class":"archive_grid"}',
            "action": "stm_lms_load_content",
            "sort": "date_high",
            "nonce": self._nonce,
        }
        headers = {
            "Host": "coursevania.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Referer": "https://coursevania.com/courses/",
            "TE": "Trailers",
        }
        query_string = urlencode(query_params)
        response = await http_get(
            f"{self.DOMAIN}/wp-admin/admin-ajax.php?{query_string}", headers=headers
        )
        if response is not None:
            json_data = json.loads(response)
            coupons_data = json_data.get("content")
            soup = BeautifulSoup(coupons_data, "html.parser")
            links = soup.find_all("a", class_="heading_font")
            course_links = list({link["href"] for link in links})

            self.last_page = json_data.get("pages")

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
            
            # Try multiple selectors and use validate_coupon_url to check
            # First try the old selector
            buy_buttons_div = soup.find("div", class_="stm-lms-buy-buttons")
            if buy_buttons_div:
                anchor = buy_buttons_div.find("a")
                if anchor and anchor.get("href"):
                    # validate_coupon_url will check if it's a proper Udemy URL with coupon
                    validated = CoursevaniaScraper.validate_coupon_url(anchor.get("href"))
                    if validated:
                        return validated
            
            # Try new selector - masterstudy-button-affiliate
            affiliate_button = soup.find("div", class_="masterstudy-button-affiliate")
            if affiliate_button:
                anchor = affiliate_button.find("a", href=True)
                if anchor and anchor.get("href"):
                    validated = CoursevaniaScraper.validate_coupon_url(anchor.get("href"))
                    if validated:
                        return validated
            
            # Try finding any link that passes validation
            for link in soup.find_all("a", href=True):
                href = link.get("href", "")
                validated = CoursevaniaScraper.validate_coupon_url(href)
                if validated:
                    return validated
        return None

    async def gather_udemy_course_links(self, courses: List[str]):
        """
        Async fetching of the udemy course links from coursevania.com.

        :param list courses: A list of coursevania.com course links we want to fetch the udemy links for
        :return: list of udemy links
        """
        return [
            link
            for link in await asyncio.gather(*map(self.get_udemy_course_link, courses))
            if link is not None
        ]
