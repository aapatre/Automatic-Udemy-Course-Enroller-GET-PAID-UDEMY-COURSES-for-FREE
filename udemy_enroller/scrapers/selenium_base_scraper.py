"""Base class for scrapers that require Selenium for JavaScript rendering."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from udemy_enroller.logger import get_logger
from udemy_enroller.scrapers.base_scraper import BaseScraper

logger = get_logger()


class SeleniumBaseScraper(BaseScraper):
    """Base class for scrapers that need Selenium for JavaScript-rendered content."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.driver = None

    def init_driver(self, headless=True, extra_options=None):
        """
        Initialize Chrome driver for JavaScript rendering.

        :param headless: Run browser in headless mode
        :param extra_options: List of additional Chrome options
        :return: None
        """
        if not self.driver:
            try:
                options = Options()
                if headless:
                    options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")

                # Add any extra options provided
                if extra_options:
                    for option in extra_options:
                        options.add_argument(option)

                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
                logger.debug(
                    f"Selenium driver initialized for {self.scraper_name} scraper"
                )
            except Exception as e:
                logger.error(
                    f"Failed to initialize Selenium driver for {self.scraper_name}: {e}"
                )
                self.driver = None

    def close_driver(self):
        """Close the Selenium driver."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            finally:
                self.driver = None
                logger.debug(f"Selenium driver closed for {self.scraper_name} scraper")

    def __del__(self):
        """Cleanup driver on deletion."""
        self.close_driver()
