"""Freebiesglobal Scraper."""
import asyncio
from typing import List

from bs4 import BeautifulSoup

from udemy_enroller.http_utils import http_get
from udemy_enroller.logger import get_logger
from udemy_enroller.scrapers.base_scraper import BaseScraper

logger = get_logger()


class FreebiesglobalScraper(BaseScraper):
    """Contains any logic related to scraping of data from Freebiesglobal.com."""

    DOMAIN = "https://freebiesglobal.com"

    def __init__(self, enabled, max_pages=None):
        """Initialize."""
        super().__init__()
        self.scraper_name = "freebiesglobal"
        if not enabled:
            self.set_state_disabled()
        self.max_pages = max_pages

    @BaseScraper.time_run
    async def run(self) -> List:
        """
        Gathers the udemy links.

        :return: List of udemy course links
        """
        links = await self.get_links()
        logger.info(
            f"Page: {self.current_page} of {self.last_page} scraped from freebiesglobal.com"
        )
        self.max_pages_reached()
        return links

    async def get_links(self) -> List:
        """
        Scrape udemy links from freebiesglobal.com.

        :return: List of udemy course urls
        """
        freebiesglobal_links = []
        self.current_page += 1
        
        # Updated URL structure - using shop/udemy instead of dealstore/udemy
        url = f"{self.DOMAIN}/shop/udemy/"
        if self.current_page > 1:
            url = f"{self.DOMAIN}/shop/udemy/page/{self.current_page}/"
            
        coupons_data = await http_get(url)
        
        if coupons_data is None:
            logger.debug(f"Failed to fetch {url}")
            return []
            
        soup = BeautifulSoup(coupons_data.decode("utf-8"), "html.parser")

        # Find all article posts (some have class "post", others don't)
        articles = soup.find_all("article")
        
        for article in articles:
            # Find the title link which leads to the course detail page
            title_elem = article.find("h2") or article.find("h3")
            if title_elem:
                # Skip expired courses (FreebiesGlobal prefixes expired courses with "Expired")
                title_text = title_elem.get_text().strip()
                if title_text.startswith("Expired"):
                    logger.debug(f"Skipping expired course: {title_text[:50]}...")
                    continue
                    
                title_link = title_elem.find("a")
                if title_link and title_link.get("href"):
                    # Make sure it's a course link, not a navigation link
                    href = title_link.get("href")
                    if href and "/shop/udemy/" not in href and "freebiesglobal.com" in href:
                        freebiesglobal_links.append(href)

        links = await self.gather_udemy_course_links(freebiesglobal_links)

        for counter, course in enumerate(links):
            logger.debug(f"Received Link {counter + 1} : {course}")

        # Set last_page on first run only or when we find the actual last page
        if self.last_page is None:
            # FreebiesGlobal uses AJAX pagination - we can't determine exact count
            # Set a reasonable limit for scraping
            self.last_page = 10  # Will scrape up to 10 pages (310 courses)
        
        # Check if this is actually the last page (no "Show next" button)
        ajax_btn = soup.find("span", class_="re_ajax_pagination_btn")
        if not ajax_btn or "Show next" not in ajax_btn.text:
            # No more pages available
            self.last_page = self.current_page

        return links

    @classmethod
    async def get_udemy_course_link(cls, url: str) -> str:
        """
        Get the udemy course link.

        :param str url: The url to scrape data from
        :return: Coupon link of the udemy course
        """
        data = await http_get(url)
        if data is None:
            return None
            
        soup = BeautifulSoup(data.decode("utf-8"), "html.parser")
        
        # Find all links and check if they're valid Udemy coupon URLs
        # FreebiesGlobal uses various classes: re_track_btn, btn_offer_block, etc.
        for link in soup.find_all("a", href=True):
            href = link.get("href", "")
            # validate_coupon_url checks for udemy.com and couponCode= pattern
            validated_url = cls.validate_coupon_url(href)
            if validated_url:
                return validated_url
        
        return None

    async def gather_udemy_course_links(self, courses: List[str]):
        """
        Async fetching of the udemy course links from freebiesglobal.com.

        :param list courses: A list of freebiesglobal.com course links we want to fetch the udemy links for
        :return: list of udemy links
        """
        return [
            link
            for link in await asyncio.gather(*map(self.get_udemy_course_link, courses))
            if link is not None
        ]

