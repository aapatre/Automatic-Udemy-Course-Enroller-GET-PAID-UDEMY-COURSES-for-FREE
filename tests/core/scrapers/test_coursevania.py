import json
from unittest import mock

import pytest

from udemy_enroller.scrapers.coursevania import CoursevaniaScraper


@pytest.mark.parametrize(
    "enabled,expected_disabled",
    [(True, False), (False, True)],
    ids=("Test enabled", "Test disabled"),
)
def test_enable_status(enabled, expected_disabled):
    scraper = CoursevaniaScraper(enabled=enabled)
    assert scraper.is_disabled() is expected_disabled


@pytest.mark.asyncio
@mock.patch.object(CoursevaniaScraper, "get_links")
async def test_run(mock_get_links):
    mock_get_links.return_value = [
        "https://www.udemy.com/course/test/?couponCode=ABC",
    ]
    scraper = CoursevaniaScraper(enabled=True)
    links = await scraper.run()
    assert links == ["https://www.udemy.com/course/test/?couponCode=ABC"]
    mock_get_links.assert_called_once()


@pytest.mark.asyncio
@mock.patch.object(CoursevaniaScraper, "load_nonce")
@mock.patch.object(CoursevaniaScraper, "get_course_links")
@mock.patch.object(CoursevaniaScraper, "gather_udemy_course_links")
async def test_get_links(mock_gather, mock_get_course, mock_load_nonce):
    mock_get_course.return_value = [
        "https://coursevania.com/course/test1/",
        "https://coursevania.com/course/test2/",
    ]
    mock_gather.return_value = [
        "https://www.udemy.com/course/test1/?couponCode=ABC",
        "https://www.udemy.com/course/test2/?couponCode=DEF",
    ]
    scraper = CoursevaniaScraper(enabled=True)
    links = await scraper.get_links()
    assert len(links) == 2
    assert scraper.current_page == 1
    mock_load_nonce.assert_called_once()
    mock_get_course.assert_called_once()
    mock_gather.assert_called_with(
        [
            "https://coursevania.com/course/test1/",
            "https://coursevania.com/course/test2/",
        ]
    )


@pytest.mark.asyncio
@mock.patch("udemy_enroller.scrapers.coursevania.http_get")
async def test_load_nonce(mock_http_get):
    html = b"""<html>
    <script>var stm_lms_nonces = {"load_content": "abc123nonce"};</script>
    <script>other stuff</script>
    </html>"""
    mock_http_get.return_value = html
    scraper = CoursevaniaScraper(enabled=True)
    assert scraper._nonce is None
    await scraper.load_nonce()
    assert scraper._nonce == "abc123nonce"


@pytest.mark.asyncio
@mock.patch("udemy_enroller.scrapers.coursevania.http_get")
async def test_load_nonce_cached(mock_http_get):
    scraper = CoursevaniaScraper(enabled=True)
    scraper._nonce = "cached_nonce"
    await scraper.load_nonce()
    mock_http_get.assert_not_called()


@pytest.mark.asyncio
@mock.patch("udemy_enroller.scrapers.coursevania.http_get")
async def test_load_nonce_none_response(mock_http_get):
    mock_http_get.return_value = None
    scraper = CoursevaniaScraper(enabled=True)
    await scraper.load_nonce()
    assert scraper._nonce is None


@pytest.mark.asyncio
@mock.patch("udemy_enroller.scrapers.coursevania.http_get")
async def test_get_course_links(mock_http_get):
    json_response = json.dumps(
        {
            "content": "<a class='heading_font' href='/course/test1/'>Test 1</a>"
            "<a class='heading_font' href='/course/test2/'>Test 2</a>",
            "pages": 5,
        }
    ).encode("utf-8")
    mock_http_get.return_value = json_response
    scraper = CoursevaniaScraper(enabled=True)
    scraper._nonce = "test_nonce"
    scraper.current_page = 1
    links = await scraper.get_course_links()
    assert sorted(links) == sorted(["/course/test1/", "/course/test2/"])
    assert scraper.last_page == 5


@pytest.mark.asyncio
@mock.patch("udemy_enroller.scrapers.coursevania.http_get")
async def test_get_course_links_none(mock_http_get):
    mock_http_get.return_value = None
    scraper = CoursevaniaScraper(enabled=True)
    scraper._nonce = "test_nonce"
    scraper.current_page = 1
    links = await scraper.get_course_links()
    assert links is None


@pytest.mark.asyncio
@mock.patch("udemy_enroller.scrapers.coursevania.http_get")
async def test_get_udemy_course_link(mock_http_get):
    html = b"""<html>
    <div class="stm-lms-buy-buttons">
        <a href="https://www.udemy.com/course/test-course/?couponCode=FREE2024">
            Enroll
        </a>
    </div>
    </html>"""
    mock_http_get.return_value = html
    link = await CoursevaniaScraper.get_udemy_course_link(
        "https://coursevania.com/course/test1/"
    )
    assert (
        link
        == "https://www.udemy.com/course/test-course/?couponCode=FREE2024"
    )


@pytest.mark.asyncio
@mock.patch("udemy_enroller.scrapers.coursevania.http_get")
async def test_get_udemy_course_link_none(mock_http_get):
    mock_http_get.return_value = None
    link = await CoursevaniaScraper.get_udemy_course_link(
        "https://coursevania.com/course/test1/"
    )
    assert link is None


@pytest.mark.asyncio
@mock.patch.object(CoursevaniaScraper, "get_udemy_course_link")
async def test_gather_udemy_course_links(mock_get_udemy):
    async def fake_get(url):
        return f"https://www.udemy.com/course/{url}/?couponCode=ABC"

    mock_get_udemy.side_effect = fake_get
    scraper = CoursevaniaScraper(enabled=True)
    courses = [
        "https://coursevania.com/course/test1/",
        "https://coursevania.com/course/test2/",
    ]
    links = await scraper.gather_udemy_course_links(courses)
    assert len(links) == 2
    assert all("udemy.com" in link for link in links)


@pytest.mark.asyncio
@mock.patch.object(CoursevaniaScraper, "get_udemy_course_link")
async def test_gather_udemy_course_links_with_none(mock_get_udemy):
    async def fake_get(url):
        if "test2" in url:
            return None
        return f"https://www.udemy.com/course/{url}/?couponCode=ABC"

    mock_get_udemy.side_effect = fake_get
    scraper = CoursevaniaScraper(enabled=True)
    courses = [
        "https://coursevania.com/course/test1/",
        "https://coursevania.com/course/test2/",
    ]
    links = await scraper.gather_udemy_course_links(courses)
    assert len(links) == 1
