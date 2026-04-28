"""Tests for ScraperManager."""

import asyncio
from unittest import mock

import pytest

from udemy_enroller.scrapers.manager import ScraperManager


class TestScraperManager:
    def test_init_all_enabled(self):
        sm = ScraperManager(
            idownloadcoupon_enabled=True,
            freebiesglobal_enabled=True,
            tutorialbar_enabled=True,
            discudemy_enabled=True,
            coursevania_enabled=True,
            max_pages=10,
        )
        assert sm.idownloadcoupons_scraper is not None
        assert sm.freebiesglobal_scraper is not None
        assert sm.tutorialbar_scraper is not None
        assert sm.discudemy_scraper is not None
        assert sm.coursevania_scraper is not None
        assert len(sm._scrapers) == 5

        assert sm.idownloadcoupons_scraper.max_pages == 10
        assert sm.freebiesglobal_scraper.max_pages == 10
        assert sm.tutorialbar_scraper.max_pages == 10
        assert sm.discudemy_scraper.max_pages == 10
        assert sm.coursevania_scraper.max_pages == 10

        assert not sm.idownloadcoupons_scraper.is_disabled()
        assert not sm.freebiesglobal_scraper.is_disabled()
        assert not sm.tutorialbar_scraper.is_disabled()
        assert not sm.discudemy_scraper.is_disabled()
        assert not sm.coursevania_scraper.is_disabled()

    def test_init_all_disabled(self):
        sm = ScraperManager(
            idownloadcoupon_enabled=False,
            freebiesglobal_enabled=False,
            tutorialbar_enabled=False,
            discudemy_enabled=False,
            coursevania_enabled=False,
            max_pages=None,
        )
        assert sm.idownloadcoupons_scraper.is_disabled()
        assert sm.freebiesglobal_scraper.is_disabled()
        assert sm.tutorialbar_scraper.is_disabled()
        assert sm.discudemy_scraper.is_disabled()
        assert sm.coursevania_scraper.is_disabled()

    def test_init_mixed(self):
        sm = ScraperManager(
            idownloadcoupon_enabled=True,
            freebiesglobal_enabled=False,
            tutorialbar_enabled=True,
            discudemy_enabled=False,
            coursevania_enabled=True,
            max_pages=3,
        )
        assert not sm.idownloadcoupons_scraper.is_disabled()
        assert sm.freebiesglobal_scraper.is_disabled()
        assert not sm.tutorialbar_scraper.is_disabled()
        assert sm.discudemy_scraper.is_disabled()
        assert not sm.coursevania_scraper.is_disabled()

    def test_enabled_scrapers_all_disabled(self):
        sm = ScraperManager(
            idownloadcoupon_enabled=False,
            freebiesglobal_enabled=False,
            tutorialbar_enabled=False,
            discudemy_enabled=False,
            coursevania_enabled=False,
            max_pages=None,
        )
        enabled = sm._enabled_scrapers()
        assert enabled == []

    def test_enabled_scrapers_some_enabled(self):
        sm = ScraperManager(
            idownloadcoupon_enabled=True,
            freebiesglobal_enabled=False,
            tutorialbar_enabled=True,
            discudemy_enabled=False,
            coursevania_enabled=False,
            max_pages=None,
        )
        enabled = sm._enabled_scrapers()
        assert len(enabled) == 2

    @pytest.mark.asyncio
    async def test_run_with_no_enabled_scrapers(self):
        sm = ScraperManager(
            idownloadcoupon_enabled=False,
            freebiesglobal_enabled=False,
            tutorialbar_enabled=False,
            discudemy_enabled=False,
            coursevania_enabled=False,
            max_pages=None,
        )
        urls = await sm.run()
        assert urls == []

    @pytest.mark.asyncio
    async def test_run_with_enabled_scrapers(self):
        sm = ScraperManager(
            idownloadcoupon_enabled=True,
            freebiesglobal_enabled=False,
            tutorialbar_enabled=False,
            discudemy_enabled=False,
            coursevania_enabled=False,
            max_pages=None,
        )

        mock_links = ["https://www.udemy.com/course/test/?couponCode=TEST1"]
        with mock.patch.object(
            sm.idownloadcoupons_scraper, "run", return_value=mock_links
        ):
            urls = await sm.run()
            assert urls == mock_links

    @pytest.mark.asyncio
    async def test_run_multiple_enabled_scrapers(self):
        sm = ScraperManager(
            idownloadcoupon_enabled=True,
            freebiesglobal_enabled=True,
            tutorialbar_enabled=False,
            discudemy_enabled=False,
            coursevania_enabled=False,
            max_pages=None,
        )

        mock_links_1 = ["https://www.udemy.com/course/test1/?couponCode=A"]
        mock_links_2 = ["https://www.udemy.com/course/test2/?couponCode=B"]

        with mock.patch.object(
            sm.idownloadcoupons_scraper, "run", return_value=mock_links_1
        ):
            with mock.patch.object(
                sm.freebiesglobal_scraper, "run", return_value=mock_links_2
            ):
                urls = await sm.run()
                assert urls == mock_links_1 + mock_links_2
