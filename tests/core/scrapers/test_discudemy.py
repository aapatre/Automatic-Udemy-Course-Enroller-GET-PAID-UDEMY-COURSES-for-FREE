from unittest import mock

import pytest
from bs4 import BeautifulSoup

from udemy_enroller.scrapers.discudemy import DiscUdemyScraper


@pytest.mark.parametrize(
    "enabled,expected_disabled",
    [(True, False), (False, True)],
    ids=("Test enabled", "Test disabled"),
)
def test_enable_status(enabled, expected_disabled):
    scraper = DiscUdemyScraper(enabled=enabled)
    assert scraper.is_disabled() is expected_disabled


@pytest.mark.asyncio
@mock.patch.object(DiscUdemyScraper, "get_links")
async def test_run(mock_get_links):
    mock_get_links.return_value = [
        "https://www.udemy.com/course/test/?couponCode=ABC",
    ]
    scraper = DiscUdemyScraper(enabled=True)
    links = await scraper.run()
    assert links == ["https://www.udemy.com/course/test/?couponCode=ABC"]
    mock_get_links.assert_called_once()


@pytest.mark.asyncio
@mock.patch("udemy_enroller.scrapers.discudemy.http_get")
@mock.patch.object(DiscUdemyScraper, "gather_udemy_course_links")
async def test_get_links(mock_gather, mock_http_get):
    html = b"""<html>
    <a class="card-header" href="/course/some-course">
       Course 1
    </a>
    <a class="card-header" href="/course/another-course">
       Course 2
    </a>
    <ul class="pagination3">
        <li>1</li>
        <li>2</li>
        <li>abc</li>
        <li>4</li>
    </ul>
    </html>"""
    mock_http_get.return_value = html
    mock_gather.return_value = [
        "https://www.udemy.com/course/test1/?couponCode=ABC",
        "https://www.udemy.com/course/test2/?couponCode=DEF",
    ]
    scraper = DiscUdemyScraper(enabled=True)
    links = await scraper.get_links()
    assert len(links) == 2
    assert scraper.last_page == 4
    assert scraper.current_page == 1
    mock_gather.assert_called_with(
        [
            "https://discudemy.com/go/some-course",
            "https://discudemy.com/go/another-course",
        ]
    )


@pytest.mark.asyncio
@mock.patch.object(DiscUdemyScraper, "gather_udemy_course_links")
async def test_get_links_no_courses(mock_gather):
    html = b"""<html>
    <ul class="pagination3">
        <li>1</li>
    </ul>
    </html>"""
    with mock.patch(
        "udemy_enroller.scrapers.discudemy.http_get", return_value=html
    ):
        mock_gather.return_value = []
        scraper = DiscUdemyScraper(enabled=True)
        links = await scraper.get_links()
        assert links == []
        assert scraper.last_page == 1


@pytest.mark.asyncio
@mock.patch("udemy_enroller.scrapers.discudemy.http_get")
async def test_get_udemy_course_link(mock_http_get):
    html = b"""<html>
    <a href="https://www.udemy.com/course/test-course/?couponCode=FREE2024">
       Udemy Course
    </a>
    </html>"""
    mock_http_get.return_value = html
    link = await DiscUdemyScraper.get_udemy_course_link(
        "https://discudemy.com/go/some-course"
    )
    assert link == "https://www.udemy.com/course/test-course/?couponCode=FREE2024"


@pytest.mark.asyncio
@mock.patch("udemy_enroller.scrapers.discudemy.http_get")
async def test_get_udemy_course_link_no_valid(mock_http_get):
    html = b"""<html>
    <a href="https://other-site.com/not-udemy">
       Not Udemy
    </a>
    </html>"""
    mock_http_get.return_value = html
    link = await DiscUdemyScraper.get_udemy_course_link(
        "https://discudemy.com/go/some-course"
    )
    assert link is None


def test_get_last_page():
    html = b"""<html>
    <ul class="pagination3">
        <li>1</li>
        <li>text</li>
        <li>7</li>
        <li>next</li>
    </ul>
    </html>"""
    soup = BeautifulSoup(html.decode("utf-8"), "html.parser")
    assert DiscUdemyScraper._get_last_page(soup) == 7


@pytest.mark.asyncio
@mock.patch.object(DiscUdemyScraper, "get_udemy_course_link")
async def test_gather_udemy_course_links(mock_get_udemy):
    async def fake_get(url):
        return f"https://www.udemy.com/course/{url}/?couponCode=ABC"

    mock_get_udemy.side_effect = fake_get
    scraper = DiscUdemyScraper(enabled=True)
    courses = [
        "https://discudemy.com/go/course_1",
        "https://discudemy.com/go/course_2",
    ]
    links = await scraper.gather_udemy_course_links(courses)
    assert len(links) == 2
    assert all("udemy.com" in link for link in links)


@pytest.mark.asyncio
@mock.patch.object(DiscUdemyScraper, "get_udemy_course_link")
async def test_gather_udemy_course_links_with_none(mock_get_udemy):
    async def fake_get(url):
        if "course_2" in url:
            return None
        return f"https://www.udemy.com/course/{url}/?couponCode=ABC"

    mock_get_udemy.side_effect = fake_get
    scraper = DiscUdemyScraper(enabled=True)
    courses = [
        "https://discudemy.com/go/course_1",
        "https://discudemy.com/go/course_2",
    ]
    links = await scraper.gather_udemy_course_links(courses)
    assert len(links) == 1
