"""Tests for BaseScraper."""

import logging
from unittest import mock

import pytest

from udemy_enroller.scrapers.base_scraper import BaseScraper, ScraperStates


class ConcreteScraper(BaseScraper):
    """Concrete implementation of BaseScraper for testing."""

    DOMAIN = "https://example.com"

    def __init__(self, enabled=True, max_pages=None):
        super().__init__()
        self.scraper_name = "test_scraper"
        if not enabled:
            self.set_state_disabled()
        self.max_pages = max_pages

    async def run(self):
        return await self.get_links()

    async def get_links(self):
        return ["https://www.udemy.com/course/test/?couponCode=TEST123"]

    @staticmethod
    async def get_udemy_course_link(url):
        return url


class TestScraperStates:
    def test_scraper_states_enum(self):
        assert ScraperStates.DISABLED.value == "DISABLED"
        assert ScraperStates.RUNNING.value == "RUNNING"
        assert ScraperStates.COMPLETE.value == "COMPLETE"


class TestBaseScraper:
    def test_init_defaults(self):
        scraper = ConcreteScraper()
        assert scraper._state is None
        assert scraper.scraper_name == "test_scraper"
        assert scraper.max_pages is None
        assert scraper.last_page is None
        assert scraper.current_page == 0

    def test_state_property_getter(self):
        scraper = ConcreteScraper()
        assert scraper.state is None
        scraper._state = "DISABLED"
        assert scraper.state == "DISABLED"

    def test_state_setter_valid(self):
        scraper = ConcreteScraper()
        scraper.state = "DISABLED"
        assert scraper._state == "DISABLED"
        scraper.state = "RUNNING"
        assert scraper._state == "RUNNING"
        scraper.state = "COMPLETE"
        assert scraper._state == "COMPLETE"

    def test_state_setter_invalid(self):
        scraper = ConcreteScraper()
        scraper.state = "INVALID_STATE"
        assert scraper._state is None

    def test_set_state_disabled(self):
        scraper = ConcreteScraper()
        scraper.set_state_disabled()
        assert scraper.state == ScraperStates.DISABLED.value
        assert scraper.is_disabled()

    def test_set_state_running(self):
        scraper = ConcreteScraper()
        scraper.set_state_running()
        assert scraper.state == ScraperStates.RUNNING.value

    def test_set_state_complete(self):
        scraper = ConcreteScraper()
        scraper.set_state_complete()
        assert scraper.state == ScraperStates.COMPLETE.value
        assert scraper.is_complete()

    def test_is_disabled(self):
        scraper = ConcreteScraper()
        assert not scraper.is_disabled()
        scraper.set_state_disabled()
        assert scraper.is_disabled()

    def test_is_complete(self):
        scraper = ConcreteScraper()
        assert not scraper.is_complete()
        scraper.set_state_complete()
        assert scraper.is_complete()

    def test_should_run_when_enabled(self):
        scraper = ConcreteScraper(enabled=True)
        assert scraper.should_run()
        assert scraper.state == ScraperStates.RUNNING.value

    def test_should_run_when_disabled(self):
        scraper = ConcreteScraper(enabled=False)
        assert not scraper.should_run()

    def test_should_run_when_complete(self):
        scraper = ConcreteScraper()
        scraper.set_state_complete()
        assert not scraper.should_run()

    def test_validate_coupon_url_valid(self):
        url = "https://www.udemy.com/course/test/?couponCode=TEST123"
        result = BaseScraper.validate_coupon_url(url)
        assert result == url

    def test_validate_coupon_url_valid_no_match(self):
        result = BaseScraper.validate_coupon_url("https://example.com/not-a-coupon")
        assert result is None

    def test_validate_coupon_url_invalid(self):
        result = BaseScraper.validate_coupon_url("not-a-url")
        assert result is None

    @pytest.mark.asyncio
    async def test_time_run_success(self, caplog):
        caplog.set_level(logging.INFO, logger="udemy_enroller")

        class TimedScraper(ConcreteScraper):
            @BaseScraper.time_run
            async def run(self):
                return await self.get_links()

            @staticmethod
            async def get_udemy_course_link(url):
                return url

        scraper = TimedScraper()
        links = await scraper.run()
        assert links == ["https://www.udemy.com/course/test/?couponCode=TEST123"]

    @pytest.mark.asyncio
    async def test_time_run_exception(self, caplog):
        """Test that the time_run decorator catches exceptions and returns []."""
        caplog.set_level(logging.ERROR, logger="udemy_enroller")

        class FailingScraper(ConcreteScraper):
            @BaseScraper.time_run
            async def run(self):
                raise ValueError("scraper error")

            @staticmethod
            async def get_udemy_course_link(url):
                return url

        scraper = FailingScraper()
        links = await scraper.run()
        assert links == []

    def test_max_pages_reached_under_limit(self):
        scraper = ConcreteScraper(max_pages=5)
        scraper.current_page = 3
        assert scraper.max_pages_reached()
        assert scraper.state != ScraperStates.COMPLETE.value

    def test_max_pages_reached_at_limit(self):
        scraper = ConcreteScraper(max_pages=5)
        scraper.current_page = 5
        result = scraper.max_pages_reached()
        assert not result
        assert scraper.is_complete()

    def test_max_pages_reached_exceeded(self):
        scraper = ConcreteScraper(max_pages=5)
        scraper.current_page = 10
        result = scraper.max_pages_reached()
        assert not result
        assert scraper.is_complete()

    def test_max_pages_reached_last_page_equals_current(self):
        scraper = ConcreteScraper()
        scraper.last_page = 3
        scraper.current_page = 3
        result = scraper.max_pages_reached()
        assert result is True
        assert scraper.is_complete()

    def test_max_pages_reached_no_max_pages(self):
        scraper = ConcreteScraper()
        scraper.current_page = 1
        assert scraper.max_pages_reached()

    @pytest.mark.asyncio
    async def test_abstract_run_called_from_subclass(self):
        """Cover the abstract method body in base run() by calling it via a subclass."""

        class MinimalScraper(BaseScraper):
            DOMAIN = "test"

            async def run(self):
                return await BaseScraper.run(self)

            async def get_links(self):
                return []

            @staticmethod
            async def get_udemy_course_link(url):
                return url

        scraper = MinimalScraper()
        result = await scraper.run()
        assert result is None

    @pytest.mark.asyncio
    async def test_abstract_get_links_called_from_subclass(self):
        """Cover the abstract method body in base get_links() by calling it via a subclass."""

        class MinimalScraper(BaseScraper):
            DOMAIN = "test"

            async def run(self):
                return []

            async def get_links(self):
                return await BaseScraper.get_links(self)

            @staticmethod
            async def get_udemy_course_link(url):
                return url

        scraper = MinimalScraper()
        result = await scraper.get_links()
        assert result is None
