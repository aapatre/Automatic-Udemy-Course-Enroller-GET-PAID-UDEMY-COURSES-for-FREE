"""Tests for udemy_rest module."""

import json
from pathlib import Path
from unittest import mock

import pytest
import requests

from udemy_enroller.models import RunStatistics, UdemyStatus
from udemy_enroller.udemy_rest import (
    UdemyActions,
    format_requests,
)


class MockResponse:
    def __init__(self, json_data=None, status_code=200, text="", cookies=None, content=b""):
        self.json_data = json_data or {}
        self.status_code = status_code
        self.text = text
        self.cookies = cookies or {}
        self.content = content or b""
        self.ok = status_code < 400

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code}")

    def json(self):
        return self.json_data


@pytest.fixture
def mock_settings():
    s = mock.MagicMock()
    s.email = "test@test.com"
    s.password = "password"
    s.categories = []
    s.languages = []
    s.authors = []
    s.years = []
    s.is_ci_build = False
    return s


class TestFormatRequests:
    def test_format_requests_raises_on_error(self):
        @format_requests
        def bad_request():
            resp = MockResponse(status_code=500)
            return resp

        with pytest.raises(requests.HTTPError):
            bad_request()

    def test_format_requests_returns_json(self):
        @format_requests
        def good_request():
            resp = MockResponse(json_data={"key": "value"}, status_code=200)
            return resp

        result = good_request()
        assert result == {"key": "value"}


class TestRunStatistics:
    def test_savings_empty(self):
        stats = RunStatistics()
        assert stats.savings() == 0

    def test_savings_with_prices(self):
        stats = RunStatistics()
        stats.prices = [10.0, 20.5, 5.0]
        assert stats.savings() == 35.5

    def test_table(self, caplog):
        import logging
        logger = logging.getLogger("udemy_enroller")
        original = logger.level
        logger.setLevel(logging.INFO)
        try:
            stats = RunStatistics()
            stats.enrolled = 5
            stats.expired = 2
            stats.already_enrolled = 3
            stats.unwanted_language = 1
            stats.unwanted_category = 1
            stats.unwanted_author = 1
            stats.unwanted_year = 1
            stats.course_ids_end = 10
            stats.prices = [10.0, 20.0]
            stats.table()
            assert "Enrolled:" in caplog.text
            assert "Savings:" in caplog.text
        finally:
            logger.setLevel(original)


class TestUdemyActionsInit:
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_init(self, mock_get_app_dir, mock_create_scraper, mock_settings):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        actions = UdemyActions(mock_settings)
        assert actions.settings == mock_settings
        assert actions.user_has_preferences == []
        mock_create_scraper.assert_called_once_with(ecdhCurve="secp384r1")

    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_init_with_preferences(self, mock_get_app_dir, mock_create_scraper, mock_settings):
        mock_settings.categories = ["Development"]
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        actions = UdemyActions(mock_settings)
        assert bool(actions.user_has_preferences) is True


class TestLogin:
    @mock.patch("pathlib.Path.is_file")
    @mock.patch("udemy_enroller.udemy_rest.open", mock.mock_open(read_data='{"access_token":"t","client_id":"c","csrftoken":"csrf"}'))
    @mock.patch("udemy_enroller.udemy_rest.json.loads")
    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_login_with_cached_cookies(
        self, mock_get_app_dir, mock_create_scraper, mock_requests_get, mock_json_loads, mock_isfile, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_isfile.return_value = True
        mock_json_loads.return_value = {
            "access_token": "tok",
            "client_id": "cid",
            "csrftoken": "csrf",
        }

        scraper = mock.MagicMock()
        mock_create_scraper.return_value = scraper

        # load_user_details mock
        mock_requests_get.return_value = MockResponse(
            json_data={
                "Config": {"price_country": {"currency": "USD", "currency_symbol": "$"}}
            }
        )

        actions = UdemyActions(mock_settings)
        actions.load_my_courses = mock.MagicMock(return_value=[])
        actions.login()

        assert actions._cookies["access_token"] == "tok"
        assert actions._currency == "USD"

    @mock.patch("pathlib.Path.is_file")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_login_fresh_no_csrf(
        self, mock_get_app_dir, mock_create_scraper, mock_isfile, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_isfile.return_value = False

        scraper = mock.MagicMock()
        scraper.get.return_value = mock.MagicMock(cookies={})
        mock_create_scraper.return_value = scraper

        actions = UdemyActions(mock_settings)
        with pytest.raises(Exception, match="Unable to get csrf_token"):
            actions.login()

    @mock.patch("pathlib.Path.is_file")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_login_fresh_success(
        self, mock_get_app_dir, mock_create_scraper, mock_isfile, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_isfile.return_value = False

        scraper = mock.MagicMock()
        scraper.get.return_value = mock.MagicMock(cookies={"csrftoken": "csrf123"})
        scraper.post.return_value = mock.MagicMock(
            status_code=200,
            cookies={"access_token": "tok", "client_id": "cid", "csrftoken": "csrf123"},
            json=lambda: {},
        )
        mock_create_scraper.return_value = scraper

        actions = UdemyActions(mock_settings)
        actions.load_my_courses = mock.MagicMock(return_value=[])
        with mock.patch("udemy_enroller.udemy_rest.requests.get") as mock_req_get:
            mock_req_get.return_value = MockResponse(
                json_data={
                    "Config": {"price_country": {"currency": "USD", "currency_symbol": "$"}}
                }
            )
            with mock.patch("builtins.open", mock.mock_open()):
                actions.login()

        assert actions._cookies is not None

    @mock.patch("pathlib.Path.is_file")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_login_fresh_with_error_in_response(
        self, mock_get_app_dir, mock_create_scraper, mock_isfile, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_isfile.return_value = False

        scraper = mock.MagicMock()
        scraper.get.return_value = mock.MagicMock(cookies={"csrftoken": "csrf123"})
        scraper.post.return_value = mock.MagicMock(
            status_code=200,
            json=lambda: {"error": {"data": {"formErrors": ["bad login"]}}},
        )
        mock_create_scraper.return_value = scraper

        actions = UdemyActions(mock_settings)
        with pytest.raises(Exception, match="Error detected on login"):
            actions.login()

    @mock.patch("pathlib.Path.is_file")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_login_non_200_auth(
        self, mock_get_app_dir, mock_create_scraper, mock_isfile, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_isfile.return_value = False

        scraper = mock.MagicMock()
        scraper.get.return_value = mock.MagicMock(cookies={"csrftoken": "csrf123"})
        scraper.post.return_value = mock.MagicMock(status_code=403)
        mock_create_scraper.return_value = scraper

        actions = UdemyActions(mock_settings)
        with pytest.raises(Exception, match="Could not login"):
            actions.login()

    @mock.patch("pathlib.Path.is_file")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_login_prompt_email_password(
        self, mock_get_app_dir, mock_create_scraper, mock_isfile, mock_settings
    ):
        mock_settings.email = None
        mock_settings.password = None
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_isfile.return_value = False

        scraper = mock.MagicMock()
        scraper.get.return_value = mock.MagicMock(cookies={"csrftoken": "csrf123"})
        scraper.post.return_value = mock.MagicMock(
            status_code=200,
            cookies={"access_token": "tok", "client_id": "cid", "csrftoken": "csrf123"},
            json=lambda: {},
        )
        mock_create_scraper.return_value = scraper

        actions = UdemyActions(mock_settings)
        actions.load_my_courses = mock.MagicMock(return_value=[])
        with mock.patch("udemy_enroller.udemy_rest.requests.get") as mock_req_get:
            mock_req_get.return_value = MockResponse(
                json_data={
                    "Config": {"price_country": {"currency": "USD", "currency_symbol": "$"}}
                }
            )
            with mock.patch("builtins.open", mock.mock_open()):
                actions.login()

        mock_settings.prompt_email.assert_called_once()
        mock_settings.prompt_password.assert_called_once()

    @mock.patch("pathlib.Path.is_file")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_login_httperror_retry_raises(
        self, mock_get_app_dir, mock_create_scraper, mock_isfile, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_isfile.return_value = True

        scraper = mock.MagicMock()
        mock_create_scraper.return_value = scraper

        actions = UdemyActions(mock_settings)
        actions._load_cookies = mock.MagicMock(
            return_value={"access_token": "t", "client_id": "c", "csrftoken": "csrf"}
        )
        actions.load_my_courses = mock.MagicMock(side_effect=requests.HTTPError("503"))

        with mock.patch("udemy_enroller.udemy_rest.requests.get") as mock_req_get:
            mock_req_get.return_value = MockResponse(
                json_data={
                    "Config": {"price_country": {"currency": "USD", "currency_symbol": "$"}}
                }
            )
            with pytest.raises(requests.HTTPError):
                actions.login()

    @mock.patch("pathlib.Path.is_file")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_login_httperror_retry_fails_again(
        self, mock_get_app_dir, mock_create_scraper, mock_isfile, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_isfile.return_value = True

        scraper = mock.MagicMock()
        mock_create_scraper.return_value = scraper

        actions = UdemyActions(mock_settings)
        actions._load_cookies = mock.MagicMock(
            return_value={"access_token": "t", "client_id": "c", "csrftoken": "csrf"}
        )
        actions.load_my_courses = mock.MagicMock(side_effect=requests.HTTPError("503"))

        with mock.patch("udemy_enroller.udemy_rest.requests.get") as mock_req_get:
            mock_req_get.return_value = MockResponse(
                json_data={
                    "Config": {"price_country": {"currency": "USD", "currency_symbol": "$"}}
                }
            )
            with pytest.raises(requests.HTTPError):
                actions.login()


class TestLoadMyCourses:
    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_load_my_courses_single_page(
        self, mock_get_app_dir, mock_create_scraper, mock_requests_get, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_get.return_value = MockResponse(
            json_data={"results": [{"id": 1}, {"id": 2}]}
        )

        actions = UdemyActions(mock_settings)
        actions._cookies = {"test": "cookie"}
        with mock.patch("udemy_enroller.udemy_rest.time.sleep"):
            courses = actions.load_my_courses()
        assert len(courses) == 2

    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_load_my_courses_pagination(
        self, mock_get_app_dir, mock_create_scraper, mock_requests_get, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        call_count = [0]

        def side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return MockResponse(
                    json_data={"results": [{"id": 1}], "next": "https://next.page"}
                )
            elif call_count[0] == 2:
                return MockResponse(json_data={"results": [{"id": 2}]})
            return MockResponse(json_data={"results": []})

        mock_requests_get.side_effect = side_effect

        actions = UdemyActions(mock_settings)
        actions._cookies = {"test": "cookie"}
        with mock.patch("udemy_enroller.udemy_rest.time.sleep"):
            courses = actions.load_my_courses()
        assert len(courses) == 2


class TestIsEnrolled:
    def test_is_enrolled_true(self, mock_settings):
        actions = UdemyActions(mock_settings)
        actions._all_course_ids = {1, 2, 3}
        assert actions.is_enrolled(2) is True

    def test_is_enrolled_false(self, mock_settings):
        actions = UdemyActions(mock_settings)
        actions._all_course_ids = {1, 2, 3}
        assert actions.is_enrolled(99) is False


class TestAddEnrolledCourse:
    def test_add_enrolled_course(self, mock_settings):
        actions = UdemyActions(mock_settings)
        actions._all_course_ids = {1}
        actions.stats.course_ids_end = 1
        actions._add_enrolled_course(2)
        assert 2 in actions._all_course_ids
        assert actions.stats.course_ids_end == 2


class TestIsCouponValid:
    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_coupon_valid(
        self, mock_get_app_dir, mock_create_scraper, mock_requests_get, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_get.return_value = MockResponse(
            json_data={
                "price_text": {
                    "data": {
                        "pricing_result": {
                            "price": {"amount": 0},
                            "list_price": {"amount": 100},
                            "saving_price": {"amount": 100},
                        }
                    }
                }
            }
        )

        actions = UdemyActions(mock_settings)
        result = actions.is_coupon_valid(1, "CODE", "Course Name")
        assert result is True
        assert 100.0 in actions.stats.prices

    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_coupon_not_free(
        self, mock_get_app_dir, mock_create_scraper, mock_requests_get, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_get.return_value = MockResponse(
            json_data={
                "price_text": {
                    "data": {
                        "pricing_result": {
                            "price": {"amount": 10},
                            "list_price": {"amount": 100},
                        }
                    }
                }
            }
        )

        actions = UdemyActions(mock_settings)
        actions._currency_symbol = "$"
        result = actions.is_coupon_valid(1, "CODE", "Course Name")
        assert result is False

    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_coupon_always_free(
        self, mock_get_app_dir, mock_create_scraper, mock_requests_get, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_get.return_value = MockResponse(
            json_data={
                "price_text": {
                    "data": {
                        "pricing_result": {
                            "price": {"amount": 0},
                            "list_price": {"amount": 0},
                        }
                    }
                }
            }
        )

        actions = UdemyActions(mock_settings)
        result = actions.is_coupon_valid(1, "CODE", "Course Name")
        assert result is False


class TestIsPreferredLanguage:
    def test_preferred_language_match(self, mock_settings):
        mock_settings.languages = ["English", "French"]
        actions = UdemyActions(mock_settings)
        result = actions.is_preferred_language(
            {"locale": {"simple_english_title": "English"}}, "Course"
        )
        assert result is True

    def test_preferred_language_no_match(self, mock_settings):
        mock_settings.languages = ["English"]
        actions = UdemyActions(mock_settings)
        result = actions.is_preferred_language(
            {"locale": {"simple_english_title": "German"}}, "Course"
        )
        assert result is False


class TestIsPreferredCategory:
    def test_preferred_category_match_primary(self, mock_settings):
        mock_settings.categories = ["Development"]
        actions = UdemyActions(mock_settings)
        result = actions.is_preferred_category(
            {
                "primary_category": {"title": "Development"},
                "primary_subcategory": {"title": "Web Dev"},
            },
            "Course",
        )
        assert result is True

    def test_preferred_category_match_sub(self, mock_settings):
        mock_settings.categories = ["Web Dev"]
        actions = UdemyActions(mock_settings)
        result = actions.is_preferred_category(
            {
                "primary_category": {"title": "Development"},
                "primary_subcategory": {"title": "Web Dev"},
            },
            "Course",
        )
        assert result is True

    def test_preferred_category_no_match(self, mock_settings):
        mock_settings.categories = ["Music"]
        actions = UdemyActions(mock_settings)
        result = actions.is_preferred_category(
            {
                "primary_category": {"title": "Development"},
                "primary_subcategory": {"title": "Web Dev"},
            },
            "Course",
        )
        assert result is False


class TestIsPreferredYear:
    def test_preferred_year_match(self, mock_settings):
        mock_settings.years = ["2024", "2023"]
        actions = UdemyActions(mock_settings)
        result = actions.is_preferred_year(
            {"units": [{"items": [{"last_update_date": "2024-01-15"}]}]}, "Course"
        )
        assert result is True

    def test_preferred_year_no_match(self, mock_settings):
        mock_settings.years = ["2024"]
        actions = UdemyActions(mock_settings)
        result = actions.is_preferred_year(
            {"units": [{"items": [{"last_update_date": "2022-01-15"}]}]}, "Course"
        )
        assert result is False


class TestIsExcludeAuthor:
    def test_exclude_author_match(self, mock_settings):
        mock_settings.authors = ["John Doe"]
        actions = UdemyActions(mock_settings)
        result = actions.is_exclude_author(
            {"visible_instructors": [{"title": "John Doe"}]}, "Course"
        )
        assert result is True

    def test_exclude_author_no_match(self, mock_settings):
        mock_settings.authors = ["John Doe"]
        actions = UdemyActions(mock_settings)
        result = actions.is_exclude_author(
            {"visible_instructors": [{"title": "Jane Doe"}]}, "Course"
        )
        assert result is False


class TestDecoratedMethods:
    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_my_courses(self, mock_get_app_dir, mock_create_scraper, mock_requests_get, mock_settings):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_get.return_value = MockResponse(json_data={"results": []})

        actions = UdemyActions(mock_settings)
        actions._cookies = {"test": "cookie"}
        result = actions.my_courses(1, 10)
        assert result == {"results": []}

    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_coupon_details(self, mock_get_app_dir, mock_create_scraper, mock_requests_get, mock_settings):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_get.return_value = MockResponse(json_data={"price": 0})

        actions = UdemyActions(mock_settings)
        result = actions.coupon_details(1, "CODE")
        assert result == {"price": 0}

    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_course_details(self, mock_get_app_dir, mock_create_scraper, mock_requests_get, mock_settings):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_get.return_value = MockResponse(json_data={"title": "Test Course"})

        actions = UdemyActions(mock_settings)
        result = actions.course_details(1)
        assert result == {"title": "Test Course"}

    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_course_units(self, mock_get_app_dir, mock_create_scraper, mock_requests_get, mock_settings):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_get.return_value = MockResponse(json_data={"units": []})

        actions = UdemyActions(mock_settings)
        result = actions.course_units(1)
        assert result == {"units": []}

    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_load_user_details(self, mock_get_app_dir, mock_create_scraper, mock_requests_get, mock_settings):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_get.return_value = MockResponse(
            json_data={"Config": {"price_country": {"currency": "USD", "currency_symbol": "$"}}}
        )

        actions = UdemyActions(mock_settings)
        actions._cookies = {"test": "cookie"}
        result = actions.load_user_details()
        assert result["Config"]["price_country"]["currency"] == "USD"


class TestEnroll:
    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.BeautifulSoup")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_enroll_already_enrolled(
        self, mock_get_app_dir, mock_create_scraper, mock_bs, mock_requests_get, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_get.return_value = MockResponse(
            json_data={"title": "Test Course"},
            content=b'<html><body data-clp-course-id="123"></body></html>',
        )
        mock_bs.return_value.find.return_value = {"data-clp-course-id": "123"}

        actions = UdemyActions(mock_settings)
        actions._all_course_ids = {123}

        result = actions.enroll("https://www.udemy.com/course/test/?couponCode=CODE")
        assert result == UdemyStatus.ALREADY_ENROLLED.value

    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.BeautifulSoup")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_enroll_unwanted_language(
        self, mock_get_app_dir, mock_create_scraper, mock_bs, mock_requests_get, mock_settings
    ):
        mock_settings.languages = ["English"]
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_get.return_value = MockResponse(
            json_data={
                "title": "Test Course",
                "locale": {"simple_english_title": "German"},
            },
            content=b'<html><body data-clp-course-id="123"></body></html>',
        )
        mock_bs.return_value.find.return_value = {"data-clp-course-id": "123"}

        actions = UdemyActions(mock_settings)
        result = actions.enroll("https://www.udemy.com/course/test/?couponCode=CODE")
        assert result == UdemyStatus.UNWANTED_LANGUAGE.value

    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.BeautifulSoup")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_enroll_unwanted_category(
        self, mock_get_app_dir, mock_create_scraper, mock_bs, mock_requests_get, mock_settings
    ):
        mock_settings.categories = ["Music"]
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_get.return_value = MockResponse(
            json_data={
                "title": "Test Course",
                "primary_category": {"title": "Development"},
                "primary_subcategory": {"title": "Web Dev"},
            },
            content=b'<html><body data-clp-course-id="123"></body></html>',
        )
        mock_bs.return_value.find.return_value = {"data-clp-course-id": "123"}

        actions = UdemyActions(mock_settings)
        result = actions.enroll("https://www.udemy.com/course/test/?couponCode=CODE")
        assert result == UdemyStatus.UNWANTED_CATEGORY.value

    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.BeautifulSoup")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_enroll_exclude_author(
        self, mock_get_app_dir, mock_create_scraper, mock_bs, mock_requests_get, mock_settings
    ):
        mock_settings.authors = ["Bad Author"]
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_get.return_value = MockResponse(
            json_data={
                "title": "Test Course",
                "visible_instructors": [{"title": "Bad Author"}],
            },
            content=b'<html><body data-clp-course-id="123"></body></html>',
        )
        mock_bs.return_value.find.return_value = {"data-clp-course-id": "123"}

        actions = UdemyActions(mock_settings)
        result = actions.enroll("https://www.udemy.com/course/test/?couponCode=CODE")
        assert result == UdemyStatus.UNWANTED_AUTHOR.value

    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.BeautifulSoup")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_enroll_unwanted_year(
        self, mock_get_app_dir, mock_create_scraper, mock_bs, mock_requests_get, mock_settings
    ):
        mock_settings.years = ["2024"]
        mock_get_app_dir.return_value = Path("/tmp/test_dir")

        def get_side_effect(*args, **kwargs):
            if "courses/" in args[0] and "discovery-units" not in args[0]:
                return MockResponse(json_data={"title": "Test Course"})
            return MockResponse(json_data={"units": [{"items": [{"last_update_date": "2022-01-01"}]}]})

        mock_requests_get.side_effect = get_side_effect
        mock_bs.return_value.find.return_value = {"data-clp-course-id": "123"}

        actions = UdemyActions(mock_settings)
        result = actions.enroll("https://www.udemy.com/course/test/?couponCode=CODE")
        assert result == UdemyStatus.UNWANTED_YEAR.value

    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.requests.post")
    @mock.patch("udemy_enroller.udemy_rest.BeautifulSoup")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_enroll_expired_coupon(
        self, mock_get_app_dir, mock_create_scraper, mock_bs, mock_requests_post, mock_requests_get, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_get.return_value = MockResponse(
            json_data={
                "title": "Test Course",
                "locale": {"simple_english_title": "English"},
                "primary_category": {"title": "Development"},
                "primary_subcategory": {"title": "Web Dev"},
                "visible_instructors": [{"title": "Good Author"}],
            },
            content=b'<html><body data-clp-course-id="123"></body></html>',
        )
        mock_bs.return_value.find.return_value = {"data-clp-course-id": "123"}

        # coupon_details: price is not 0
        def coupon_side_effect(*args, **kwargs):
            if "course-landing-components" in args[0]:
                return MockResponse(
                    json_data={
                        "price_text": {
                            "data": {
                                "pricing_result": {
                                    "price": {"amount": 10},
                                    "list_price": {"amount": 100},
                                }
                            }
                        }
                    }
                )
            return MockResponse(json_data={})

        mock_requests_get.side_effect = coupon_side_effect

        actions = UdemyActions(mock_settings)
        actions._currency_symbol = "$"
        result = actions.enroll("https://www.udemy.com/course/test/?couponCode=CODE")
        assert result == UdemyStatus.EXPIRED.value

    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.requests.post")
    @mock.patch("udemy_enroller.udemy_rest.BeautifulSoup")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_enroll_success(
        self, mock_get_app_dir, mock_create_scraper, mock_bs, mock_requests_post, mock_requests_get, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")

        def get_side_effect(*args, **kwargs):
            if "course-landing-components" in args[0]:
                return MockResponse(
                    json_data={
                        "price_text": {
                            "data": {
                                "pricing_result": {
                                    "price": {"amount": 0},
                                    "list_price": {"amount": 100},
                                    "saving_price": {"amount": 100},
                                }
                            }
                        }
                    }
                )
            elif "courses/" in args[0] and "discovery-units" not in args[0]:
                return MockResponse(
                    json_data={
                        "title": "Test Course",
                        "locale": {"simple_english_title": "English"},
                        "primary_category": {"title": "Development"},
                        "primary_subcategory": {"title": "Web Dev"},
                        "visible_instructors": [{"title": "Good Author"}],
                    }
                )
            return MockResponse(json_data={"units": [{"items": [{"last_update_date": "2024-01-01"}]}]})

        mock_requests_get.side_effect = get_side_effect
        mock_requests_post.return_value = MockResponse(
            json_data={"status": "succeeded"}, status_code=200
        )
        mock_bs.return_value.find.return_value = {"data-clp-course-id": "123"}

        actions = UdemyActions(mock_settings)
        actions._cookies = {"test": "cookie"}
        actions._currency = "USD"
        result = actions.enroll("https://www.udemy.com/course/test/?couponCode=CODE")
        assert result == UdemyStatus.ENROLLED.value
        assert actions.stats.enrolled == 1

    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.requests.post")
    @mock.patch("udemy_enroller.udemy_rest.BeautifulSoup")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_enroll_malformed_url(
        self, mock_get_app_dir, mock_create_scraper, mock_bs, mock_requests_post, mock_requests_get, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        actions = UdemyActions(mock_settings)
        result = actions.enroll("https://www.udemy.com/course/test/")
        assert result == UdemyStatus.EXPIRED.value


class TestGetCourseId:
    @mock.patch("udemy_enroller.udemy_rest.requests.get")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_get_course_id(
        self, mock_get_app_dir, mock_create_scraper, mock_requests_get, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_get.return_value = mock.MagicMock(
            status_code=200,
            content=b'<html><body data-clp-course-id="12345"></body></html>',
        )

        actions = UdemyActions(mock_settings)
        with mock.patch("udemy_enroller.udemy_rest.BeautifulSoup") as mock_bs:
            mock_soup = mock.MagicMock()
            mock_soup.find.return_value = {"data-clp-course-id": "12345"}
            mock_bs.return_value = mock_soup
            result = actions._get_course_id("https://www.udemy.com/course/test/")
        assert result == 12345


class TestCheckout:
    @mock.patch("udemy_enroller.udemy_rest.requests.post")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_checkout_success(
        self, mock_get_app_dir, mock_create_scraper, mock_requests_post, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_post.return_value = MockResponse(
            json_data={"status": "succeeded"}, status_code=200
        )

        actions = UdemyActions(mock_settings)
        actions._cookies = {"test": "cookie"}
        actions._currency = "USD"
        result = actions._checkout(1, "CODE", "Course")
        assert result == UdemyStatus.ENROLLED.value

    @mock.patch("udemy_enroller.udemy_rest.requests.post")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_checkout_failed(
        self, mock_get_app_dir, mock_create_scraper, mock_requests_post, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_post.return_value = MockResponse(
            json_data={"status": "failed"}, status_code=200
        )

        actions = UdemyActions(mock_settings)
        actions._cookies = {"test": "cookie"}
        actions._currency = "USD"
        result = actions._checkout(1, "CODE", "Course")
        assert result == UdemyStatus.EXPIRED.value

    @mock.patch("udemy_enroller.udemy_rest.requests.post")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_checkout_rate_limited_retry(
        self, mock_get_app_dir, mock_create_scraper, mock_requests_post, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        call_count = [0]

        def post_side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return mock.MagicMock(ok=False, status_code=429, text="Rate limited. Please wait 2 seconds")
            return MockResponse(json_data={"status": "succeeded"}, status_code=200)

        mock_requests_post.side_effect = post_side_effect

        actions = UdemyActions(mock_settings)
        actions._cookies = {"test": "cookie"}
        actions._currency = "USD"
        with mock.patch("udemy_enroller.udemy_rest.time.sleep") as mock_sleep:
            # Note: _checkout recursively calls itself but doesn't return the recursive result,
            # so the outer call returns None after sleeping and retrying
            actions._checkout(1, "CODE", "Course")
        mock_sleep.assert_called_once_with(3)
        assert call_count[0] == 2

    @mock.patch("udemy_enroller.udemy_rest.requests.post")
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_checkout_rate_limited_retry_fails(
        self, mock_get_app_dir, mock_create_scraper, mock_requests_post, mock_settings
    ):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_requests_post.return_value = mock.MagicMock(
            ok=False, status_code=429, text="Rate limited. Please wait 2 seconds"
        )

        actions = UdemyActions(mock_settings)
        actions._cookies = {"test": "cookie"}
        actions._currency = "USD"
        with mock.patch("udemy_enroller.udemy_rest.time.sleep"):
            with pytest.raises(Exception, match="Checkout failed"):
                actions._checkout(1, "CODE", "Course")


class TestBuildCheckoutPayload:
    def test_build_payload(self, mock_settings):
        actions = UdemyActions(mock_settings)
        actions._currency = "USD"
        payload = actions._build_checkout_payload(123, "CODE50")
        assert payload["shopping_info"]["items"][0]["buyable"]["id"] == 123
        assert payload["shopping_info"]["items"][0]["discountInfo"]["code"] == "CODE50"
        assert payload["shopping_info"]["items"][0]["price"]["currency"] == "USD"


class TestCacheCookies:
    @mock.patch("udemy_enroller.udemy_rest.create_scraper")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_cache_cookies(self, mock_get_app_dir, mock_create_scraper):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")

        actions = UdemyActions(mock.MagicMock())
        m = mock.mock_open()
        with mock.patch("builtins.open", m):
            with mock.patch("udemy_enroller.udemy_rest.json.dumps", return_value='{"a":"b"}'):
                actions._cache_cookies({"a": "b"})
        m.assert_called_once_with(actions._cookie_file, "w")


class TestLoadCookies:
    @mock.patch("pathlib.Path.is_file")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_load_cookies_exists(self, mock_get_app_dir, mock_isfile):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_isfile.return_value = True

        actions = UdemyActions(mock.MagicMock())
        m = mock.mock_open(read_data='{"token":"abc"}')
        with mock.patch("builtins.open", m):
            with mock.patch("udemy_enroller.udemy_rest.json.loads", return_value={"token": "abc"}):
                result = actions._load_cookies()
        assert result == {"token": "abc"}

    @mock.patch("pathlib.Path.is_file")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_load_cookies_not_exists(self, mock_get_app_dir, mock_isfile):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")
        mock_isfile.return_value = False

        actions = UdemyActions(mock.MagicMock())
        result = actions._load_cookies()
        assert result is None


class TestDeleteCookies:
    @mock.patch("pathlib.Path.unlink")
    @mock.patch("udemy_enroller.udemy_rest.get_app_dir")
    def test_delete_cookies(self, mock_get_app_dir, mock_remove):
        mock_get_app_dir.return_value = Path("/tmp/test_dir")

        actions = UdemyActions(mock.MagicMock())
        actions._delete_cookies()
        mock_remove.assert_called_once()


class TestUdemyStatus:
    def test_status_values(self):
        assert UdemyStatus.ALREADY_ENROLLED.value == "ALREADY_ENROLLED"
        assert UdemyStatus.ENROLLED.value == "ENROLLED"
        assert UdemyStatus.EXPIRED.value == "EXPIRED"
        assert UdemyStatus.UNWANTED_LANGUAGE.value == "UNWANTED_LANGUAGE"
        assert UdemyStatus.UNWANTED_CATEGORY.value == "UNWANTED_CATEGORY"
        assert UdemyStatus.UNWANTED_AUTHOR.value == "UNWANTED_AUTHOR"
        assert UdemyStatus.UNWANTED_YEAR.value == "UNWANTED_YEAR"
