import asyncio
import pytest

from udemy_enroller.scrapers.base_scraper import BaseScraper, ScraperStates


class FailingScraper(BaseScraper):
    DOMAIN = "http://example.com"

    async def run(self):
        return await self.get_links()

    async def get_links(self):
        raise RuntimeError("boom")


@pytest.mark.asyncio
async def test_time_run_marks_complete_on_exception():
    s = FailingScraper()
    s.scraper_name = "failing"

    @BaseScraper.time_run
    async def wrapped(self):
        return await self.get_links()

    res = await wrapped(s)
    assert res == []
    assert s.state == ScraperStates.COMPLETE.value
