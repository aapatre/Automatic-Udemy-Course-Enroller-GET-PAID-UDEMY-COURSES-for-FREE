import asyncio
import pytest

from udemy_enroller.scrapers.fuzz_manager import FuzzManager, HARD_MAX_CONCURRENCY
from udemy_enroller.scrapers.base_scraper import BaseScraper


class DummyScraper(BaseScraper):
    DOMAIN = "http://example.com"

    def __init__(self, enabled=True):
        super().__init__()
        self.scraper_name = "dummy"
        if not enabled:
            self.set_state_disabled()

    async def run(self):
        return await self.get_links()

    async def get_links(self):
        return ["https://www.udemy.com/course/test/?couponCode=FREE"]


@pytest.mark.asyncio
async def test_fuzz_manager_clamp_and_run():
    fm = FuzzManager(True, False, False, False, False, max_pages=1, fuzz_enabled=False, max_concurrency=500)
    # monkey-patch enabled scrapers to only our dummy
    fm._scrapers = [DummyScraper(enabled=True)]
    res = await fm.run()
    assert isinstance(res, list) and len(res) == 1
    # semaphore should be clamped
    assert fm.semaphore._value <= HARD_MAX_CONCURRENCY
