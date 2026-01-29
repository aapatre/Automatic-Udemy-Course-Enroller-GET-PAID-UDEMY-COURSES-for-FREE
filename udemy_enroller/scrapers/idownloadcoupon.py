"""IDownloadCoupon scraper."""
import asyncio
import re
import urllib.parse
from typing import List

import aiohttp
from bs4 import BeautifulSoup

from udemy_enroller.http_utils import http_get
from udemy_enroller.logger import get_logger
from udemy_enroller.scrapers.base_scraper import BaseScraper

logger = get_logger()


class IDownloadCouponScraper(BaseScraper):
    """Contains any logic related to scraping of site data."""

    DOMAIN = "https://www.idownloadcoupon.com"

    def __init__(self, enabled, max_pages=None):
        """Initialize."""
        super().__init__()
        self.scraper_name = "idownloadcoupon"
        if not enabled:
            self.set_state_disabled()
        self.last_page = None
        self.max_pages = max_pages

    @BaseScraper.time_run
    async def run(self) -> List:
        """
        Run the steps to scrape links.

        :return: list of udemy coupon links
        """
        links = await self.get_links()
        self.max_pages_reached()
        return links

    async def get_links(self):
        """
        Scrape udemy links.

        :return: List of udemy course urls
        """
        self.current_page += 1
        course_links = await self.get_course_links(
            f"{self.DOMAIN}/page/{self.current_page}/"
        )

        logger.info(
            f"Page: {self.current_page} of {self.last_page} scraped from {self.scraper_name}"
        )
        udemy_links = await self.gather_udemy_course_links(course_links)

        for counter, course in enumerate(udemy_links):
            logger.debug(f"Received Link {counter + 1} : {course}")

        return udemy_links

    async def get_course_links(self, url: str) -> List:
        """
        Get the url of pages which contain the udemy link we want to get.

        :param str url: The url to scrape data from
        :return: list of pages that contain Udemy coupons
        """
        text = await http_get(url)
        if text is not None:
            soup = BeautifulSoup(text.decode("utf-8"), "html.parser")

            links = soup.find_all("li", class_="product")
            course_links = []
            for link in links:
                anchors = link.find_all("a")
                if len(anchors) > 1 and anchors[1].get("href"):
                    course_links.append(anchors[1].get("href"))

            # Handle pagination with safety checks
            page_numbers = soup.find("ul", class_="page-numbers")
            if page_numbers:
                page_links = page_numbers.find_all("a", class_="page-numbers")
                if len(page_links) >= 2:
                    self.last_page = int(
                        page_links[-2].text.replace(",", "")
                    )

            return course_links

    @classmethod
    async def get_udemy_course_link(cls, url: str) -> str:
        """
        Get the udemy course link.

        :param str url: The url to scrape data from
        :return: Coupon link of the udemy course
        """
        # The product page does a 302 redirect with the Udemy URL in the murl parameter
        # We need to capture the redirect Location header without following it
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Don't follow redirects - we want to capture the Location header
                async with session.get(url, headers=headers, allow_redirects=False, timeout=10) as response:
                    if response.status in [301, 302, 303, 307, 308]:
                        location = response.headers.get('Location', '')
                        
                        # The Location header contains a linksynergy URL with murl parameter
                        if "murl=" in location:
                            # Extract the murl parameter
                            murl_match = re.search(r'[?&]murl=([^&]+)', location)
                            if murl_match:
                                # Decode the URL
                                decoded_url = urllib.parse.unquote(murl_match.group(1))
                                # Validate it's a proper Udemy coupon URL
                                validated = cls.validate_coupon_url(decoded_url)
                                if validated:
                                    return validated
                        
                        # Sometimes the Location might directly be a Udemy URL
                        validated = cls.validate_coupon_url(location)
                        if validated:
                            return validated
        except Exception as e:
            logger.debug(f"Error getting redirect for {url}: {e}")
        
        # Fallback to the old method if redirect capture fails
        text = await http_get(url)
        if text is not None:
            soup = BeautifulSoup(text.decode("utf-8"), "html.parser")
            
            # Check for any direct Udemy links on the page
            for link in soup.find_all("a", href=True):
                href = link.get("href", "")
                validated = cls.validate_coupon_url(href)
                if validated:
                    return validated
        
        return None

    async def gather_udemy_course_links(self, courses: List[str]):
        """
        Async fetching of the udemy course links.

        :param list courses: A list of course links we want to fetch the udemy links for
        :return: list of udemy links
        """
        return [
            link
            for link in await asyncio.gather(*map(self.get_udemy_course_link, courses))
            if link is not None
        ]
