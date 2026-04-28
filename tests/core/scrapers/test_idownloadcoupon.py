from unittest import mock

import pytest

from udemy_enroller.scrapers.idownloadcoupon import IDownloadCouponScraper


class MockResponse:
    def __init__(self, data, status=200, headers=None):
        self._data = data
        self.status = status
        self.headers = headers or {}

    async def read(self):
        return self._data

    async def json(self):
        return self._data

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


@pytest.mark.parametrize(
    "enabled,expected_disabled",
    [(True, False), (False, True)],
    ids=("Test enabled", "Test disabled"),
)
def test_enable_status(enabled, expected_disabled):
    scraper = IDownloadCouponScraper(enabled=enabled)
    assert scraper.is_disabled() is expected_disabled


@pytest.mark.asyncio
@mock.patch.object(IDownloadCouponScraper, "get_course_links")
@mock.patch.object(IDownloadCouponScraper, "gather_udemy_course_links")
async def test_run(mock_gather, mock_get_course):
    mock_get_course.return_value = [
        "https://www.idownloadcoupon.com/course_1",
    ]
    mock_gather.return_value = [
        "https://www.udemy.com/course/test/?couponCode=ABC",
    ]
    scraper = IDownloadCouponScraper(enabled=True)
    links = await scraper.run()
    assert links == ["https://www.udemy.com/course/test/?couponCode=ABC"]
    mock_get_course.assert_called_once()
    mock_gather.assert_called_once()


@pytest.mark.asyncio
@mock.patch.object(IDownloadCouponScraper, "get_course_links")
@mock.patch.object(IDownloadCouponScraper, "gather_udemy_course_links")
async def test_get_links(mock_gather, mock_get_course):
    mock_get_course.return_value = [
        "https://www.idownloadcoupon.com/course_1",
        "https://www.idownloadcoupon.com/course_2",
    ]
    mock_gather.return_value = [
        "https://www.udemy.com/course/test/?couponCode=ABC",
    ]
    scraper = IDownloadCouponScraper(enabled=True)
    links = await scraper.get_links()
    assert links == ["https://www.udemy.com/course/test/?couponCode=ABC"]
    assert scraper.current_page == 1
    mock_get_course.assert_called_with(
        "https://www.idownloadcoupon.com/page/1/"
    )
    mock_gather.assert_called_with(
        [
            "https://www.idownloadcoupon.com/course_1",
            "https://www.idownloadcoupon.com/course_2",
        ]
    )


@pytest.mark.asyncio
@mock.patch("udemy_enroller.scrapers.idownloadcoupon.http_get")
async def test_get_course_links(mock_http_get):
    html = b"""<html>
    <ul class="page-numbers">
        <li><a class="page-numbers">1,234</a></li>
        <li><a class="page-numbers">10</a></li>
    </ul>
    <li class="product">
        <a href="/ignore">Ignore</a>
        <a href="/course-1">Course 1</a>
    </li>
    <li class="product">
        <a href="/other">Other</a>
        <a href="/course-2">Course 2</a>
    </li>
    </html>"""
    mock_http_get.return_value = html
    scraper = IDownloadCouponScraper(enabled=True)
    links = await scraper.get_course_links(
        "https://www.idownloadcoupon.com/page/1/"
    )
    assert links == ["/course-1", "/course-2"]
    assert scraper.last_page == 1234


@pytest.mark.asyncio
@mock.patch("udemy_enroller.scrapers.idownloadcoupon.http_get")
async def test_get_course_links_none(mock_http_get):
    mock_http_get.return_value = None
    scraper = IDownloadCouponScraper(enabled=True)
    links = await scraper.get_course_links(
        "https://www.idownloadcoupon.com/page/1/"
    )
    assert links is None


@pytest.mark.asyncio
@mock.patch("udemy_enroller.scrapers.idownloadcoupon.http_get_no_redirect")
async def test_get_udemy_course_link(mock_http_get):
    mock_response = MockResponse(
        b"",
        headers={
            "location": "https://click.linksynergy.com/fs-bin/click?id=abc&murl=https%3A%2F%2Fwww.udemy.com%2Fcourse%2Ftest%2F%3FcouponCode%3DABC123",
        },
    )
    mock_http_get.return_value = mock_response
    link = await IDownloadCouponScraper.get_udemy_course_link(
        "https://www.idownloadcoupon.com/course_1"
    )
    assert link == "https://www.udemy.com/course/test/?couponCode=ABC123"


@pytest.mark.asyncio
@mock.patch("udemy_enroller.scrapers.idownloadcoupon.http_get_no_redirect")
async def test_get_udemy_course_link_no_linksynergy(mock_http_get):
    mock_response = MockResponse(
        b"",
        headers={
            "location": "https://other.com/redirect?murl=https%3A%2F%2Fwww.udemy.com%2Fcourse%2Ftest%2F%3FcouponCode%3DABC123",
        },
    )
    mock_http_get.return_value = mock_response
    link = await IDownloadCouponScraper.get_udemy_course_link(
        "https://www.idownloadcoupon.com/course_1"
    )
    assert link is None


@pytest.mark.asyncio
@mock.patch.object(IDownloadCouponScraper, "get_udemy_course_link")
async def test_gather_udemy_course_links(mock_get_udemy):
    async def fake_get(url):
        if "course_2" in url:
            return None
        return f"https://www.udemy.com/course/{url}/?couponCode=ABC"

    mock_get_udemy.side_effect = fake_get
    scraper = IDownloadCouponScraper(enabled=True)
    courses = [
        "https://www.idownloadcoupon.com/course_1",
        "https://www.idownloadcoupon.com/course_2",
        "https://www.idownloadcoupon.com/course_3",
    ]
    links = await scraper.gather_udemy_course_links(courses)
    assert len(links) == 2
    assert "course_2" not in str(links)
