from unittest import mock

import pytest
from bs4 import BeautifulSoup

from udemy_enroller.scrapers.freebiesglobal import FreebiesglobalScraper


@pytest.mark.parametrize(
    "enabled,expected_disabled",
    [(True, False), (False, True)],
    ids=("Test enabled", "Test disabled"),
)
def test_enable_status(enabled, expected_disabled):
    scraper = FreebiesglobalScraper(enabled=enabled)
    assert scraper.is_disabled() is expected_disabled


@pytest.mark.asyncio
@mock.patch.object(FreebiesglobalScraper, "get_links")
async def test_run(mock_get_links):
    mock_get_links.return_value = [
        "https://www.udemy.com/course/test/?couponCode=ABC",
    ]
    scraper = FreebiesglobalScraper(enabled=True)
    links = await scraper.run()
    assert links == ["https://www.udemy.com/course/test/?couponCode=ABC"]
    mock_get_links.assert_called_once()


@pytest.mark.asyncio
@mock.patch("udemy_enroller.scrapers.freebiesglobal.http_get")
@mock.patch.object(FreebiesglobalScraper, "gather_udemy_course_links")
async def test_get_links(mock_gather, mock_http_get):
    html = b"""<html>
    <a class="img-centered-flex rh-flex-center-align rh-flex-justify-center"
       href="https://freebiesglobal.com/dealstore/udemy/page/1/course-1">
       Course 1
    </a>
    <a class="img-centered-flex rh-flex-center-align rh-flex-justify-center"
       href="https://freebiesglobal.com/dealstore/udemy/page/1/course-2">
       Course 2
    </a>
    <ul class="page-numbers">
        <li>1</li>
        <li>2</li>
        <li>3</li>
    </ul>
    </html>"""
    mock_http_get.return_value = html
    mock_gather.return_value = [
        "https://www.udemy.com/course/test/?couponCode=ABC",
    ]
    scraper = FreebiesglobalScraper(enabled=True)
    links = await scraper.get_links()
    assert links == ["https://www.udemy.com/course/test/?couponCode=ABC"]
    assert scraper.last_page == 3
    assert scraper.current_page == 1
    mock_gather.assert_called_with(
        [
            "https://freebiesglobal.com/course-1",
            "https://freebiesglobal.com/course-2",
        ]
    )


@pytest.mark.asyncio
@mock.patch.object(FreebiesglobalScraper, "validate_coupon_url")
@mock.patch.object(FreebiesglobalScraper, "gather_udemy_course_links")
async def test_get_links_no_courses(mock_gather, mock_validate):
    html = b"""<html>
    <ul class="page-numbers">
        <li>1</li>
    </ul>
    </html>"""
    with mock.patch(
        "udemy_enroller.scrapers.freebiesglobal.http_get", return_value=html
    ):
        mock_gather.return_value = []
        scraper = FreebiesglobalScraper(enabled=True)
        links = await scraper.get_links()
        assert links == []
        assert scraper.last_page == 1


@pytest.mark.asyncio
@mock.patch("udemy_enroller.scrapers.freebiesglobal.http_get")
async def test_get_udemy_course_link(mock_http_get):
    html = b"""<html>
    <a class="re_track_btn"
       href="https://www.udemy.com/course/test-course/?couponCode=FREE2024">
       Enroll
    </a>
    </html>"""
    mock_http_get.return_value = html
    link = await FreebiesglobalScraper.get_udemy_course_link(
        "https://freebiesglobal.com/course-1"
    )
    assert link == "https://www.udemy.com/course/test-course/?couponCode=FREE2024"


@pytest.mark.asyncio
@mock.patch("udemy_enroller.scrapers.freebiesglobal.http_get")
async def test_get_udemy_course_link_no_valid(mock_http_get):
    html = b"""<html>
    <a class="re_track_btn"
       href="https://other-site.com/not-udemy">
       Not Udemy
    </a>
    </html>"""
    mock_http_get.return_value = html
    link = await FreebiesglobalScraper.get_udemy_course_link(
        "https://freebiesglobal.com/course-1"
    )
    assert link is None


def test_get_last_page():
    html = b"""<html>
    <ul class="page-numbers">
        <li>1</li>
        <li>2</li>
        <li>info</li>
        <li>5</li>
        <li>next</li>
    </ul>
    </html>"""
    soup = BeautifulSoup(html.decode("utf-8"), "html.parser")
    assert FreebiesglobalScraper._get_last_page(soup) == 5


@pytest.mark.asyncio
@mock.patch.object(FreebiesglobalScraper, "get_udemy_course_link")
async def test_gather_udemy_course_links(mock_get_udemy):
    async def fake_get(url):
        return f"https://www.udemy.com/course/{url}/?couponCode=ABC"

    mock_get_udemy.side_effect = fake_get
    scraper = FreebiesglobalScraper(enabled=True)
    courses = [
        "https://freebiesglobal.com/course_1",
        "https://freebiesglobal.com/course_2",
    ]
    links = await scraper.gather_udemy_course_links(courses)
    assert len(links) == 2
    assert all("udemy.com" in link for link in links)


@pytest.mark.asyncio
@mock.patch.object(FreebiesglobalScraper, "get_udemy_course_link")
async def test_gather_udemy_course_links_with_none(mock_get_udemy):
    async def fake_get(url):
        if "course_2" in url:
            return None
        return f"https://www.udemy.com/course/{url}/?couponCode=ABC"

    mock_get_udemy.side_effect = fake_get
    scraper = FreebiesglobalScraper(enabled=True)
    courses = [
        "https://freebiesglobal.com/course_1",
        "https://freebiesglobal.com/course_2",
    ]
    links = await scraper.gather_udemy_course_links(courses)
    assert len(links) == 1
