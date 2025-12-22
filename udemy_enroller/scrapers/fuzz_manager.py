import asyncio
import random
from typing import List, Optional

from udemy_enroller.logger import get_logger
from udemy_enroller.scrapers.manager import ScraperManager


logger = get_logger()


HARD_MAX_CONCURRENCY = 20


class FuzzManager(ScraperManager):
    def __init__(
        self,
        idownloadcoupon_enabled: bool,
        freebiesglobal_enabled: bool,
        tutorialbar_enabled: bool,
        discudemy_enabled: bool,
        coursevania_enabled: bool,
        max_pages: Optional[int],
        fuzz_enabled: bool = False,
        fuzz_seed: Optional[int] = None,
        max_concurrency: int = 10,
        task_timeout: int = 30,
    ):
        super().__init__(
            idownloadcoupon_enabled,
            freebiesglobal_enabled,
            tutorialbar_enabled,
            discudemy_enabled,
            coursevania_enabled,
            max_pages,
        )
        self.fuzz_enabled = fuzz_enabled
        self.fuzz_seed = fuzz_seed
        if max_concurrency > HARD_MAX_CONCURRENCY:
            logger.warning(f"max_concurrency clamped from {max_concurrency} to {HARD_MAX_CONCURRENCY}")
        self.semaphore = asyncio.Semaphore(max(1, min(max_concurrency, HARD_MAX_CONCURRENCY)))
        self.task_timeout = task_timeout
        self._rand = random.Random(fuzz_seed) if fuzz_seed is not None else random

    async def run(self) -> List[str]:
        urls: List[str] = []
        total = 0
        success = 0
        errors = 0
        timeouts = 0
        import time
        start = time.monotonic()
        enabled_scrapers = self._enabled_scrapers()
        tasks = [self._scrape(scraper) for scraper in enabled_scrapers]
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for res in results:
                total += 1
                if isinstance(res, Exception):
                    if isinstance(res, asyncio.TimeoutError):
                        timeouts += 1
                    else:
                        errors += 1
                    logger.error(res)
                else:
                    success += 1
                    urls.extend(res)
        if self.fuzz_enabled and urls:
            self._rand.shuffle(urls)
        duration = time.monotonic() - start
        logger.info(
            f"fuzz_summary total={total} success={success} error={errors} timeout={timeouts} duration={duration:.2f}s urls={len(urls)}"
        )
        return urls

    async def _scrape(self, scraper) -> List[str]:
        async with self.semaphore:
            if self.fuzz_enabled:
                jitter = self._rand.uniform(0, 0.25)
                await asyncio.sleep(jitter)
                if self.max_pages is not None:
                    scraper.max_pages = max(1, min(self.max_pages, scraper.max_pages or self.max_pages))
            return await asyncio.wait_for(scraper.run(), timeout=self.task_timeout)
