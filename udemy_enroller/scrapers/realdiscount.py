"""RealDiscount scraper - requires Selenium for JavaScript content."""

import re
import time
from typing import List, Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from udemy_enroller.logger import get_logger
from udemy_enroller.scrapers.selenium_base_scraper import SeleniumBaseScraper

logger = get_logger()


class RealDiscountScraper(SeleniumBaseScraper):
    """Contains any logic related to scraping of data from real.discount."""

    DOMAIN = "https://real.discount"

    def __init__(self, enabled, max_pages=None):
        """Initialize."""
        super().__init__()
        self.scraper_name = "realdiscount"
        if not enabled:
            self.set_state_disabled()
        self.max_pages = max_pages

    @SeleniumBaseScraper.time_run
    async def run(self) -> List:
        """
        Gathers the udemy links.

        :return: List of udemy course links
        """
        try:
            links = await self.get_links()
            logger.info(f"Page: {self.current_page} scraped from real.discount")
            self.max_pages_reached()
            return links
        finally:
            # Clean up driver after scraping is complete
            if self.is_complete() or self.is_disabled():
                self.close_driver()

    async def get_links(self) -> List:
        """
        Scrape udemy links from real.discount using Selenium.

        :return: List of udemy course urls
        """
        self.current_page += 1

        # Initialize driver if needed
        self.init_driver()

        if not self.driver:
            logger.error("Cannot scrape real.discount without Selenium driver")
            return []

        # Get the list page with course offers
        list_url = f"{self.DOMAIN}/stores/udemy?page={self.current_page}"

        try:
            self.driver.get(list_url)

            # Wait for offer links to load
            wait = WebDriverWait(self.driver, 10)
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="/offer/"]'))
            )
            time.sleep(2)  # Additional wait for dynamic content

            # Extract offer links from the page
            offer_links = []
            links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="/offer/"]')

            for link in links:
                href = link.get_attribute("href")
                if href and not href.startswith("https://www.udemy.com"):
                    if href not in offer_links:
                        offer_links.append(href)

            logger.debug(
                f"Found {len(offer_links)} offer links on page {self.current_page}"
            )

            # Fetch the actual Udemy links from each offer page
            udemy_links = self.gather_udemy_course_links(offer_links)

            for counter, course in enumerate(udemy_links):
                logger.debug(f"Received Link {counter + 1} : {course}")

            return udemy_links

        except Exception as e:
            logger.error(f"Error scraping page {self.current_page}: {e}")
            return []

    def get_udemy_course_link(self, url: str) -> Optional[str]:
        """
        Get the udemy course link from an offer page using Selenium.

        :param str url: The offer page URL to scrape
        :return: Coupon link of the udemy course
        """
        if not self.driver:
            return None

        try:
            self.driver.get(url)
            time.sleep(2)  # Wait for page to load

            # Find the Get Course link
            links = self.driver.find_elements(By.LINK_TEXT, "Get Course")
            if not links:
                # Try partial text match
                links = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "Get Course")

            for link in links:
                href = link.get_attribute("href")
                if href and "www.udemy.com/course/" in href:
                    # Convert RealDiscount's format (?c=CODE) to standard format if needed
                    if "couponCode=" in href:
                        return self.validate_coupon_url(href)
                    elif "?c=" in href:
                        match = re.search(r"\?c=([A-Z0-9]+)", href)
                        if match:
                            coupon = match.group(1)
                            base_url = href.split("?")[0]
                            return f"{base_url}?couponCode={coupon}"
                    return href

        except Exception as e:
            logger.debug(f"Error getting link from {url}: {e}")

        return None

    def gather_udemy_course_links(self, courses: List[str]):
        """
        Fetch the udemy course links from real.discount offer pages.

        :param list courses: A list of real.discount offer page links
        :return: list of udemy links
        """
        udemy_links = []

        for url in courses:
            link = self.get_udemy_course_link(url)
            if link:
                udemy_links.append(link)

        return udemy_links
