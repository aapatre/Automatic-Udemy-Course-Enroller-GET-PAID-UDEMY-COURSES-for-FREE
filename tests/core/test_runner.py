"""Tests for runner module."""

import asyncio
from unittest import mock

import pytest
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)

from udemy_enroller import UdemyStatus, exceptions
from udemy_enroller.runner import (
    _redeem_courses,
    _redeem_courses_ui,
    redeem_courses,
    redeem_courses_ui,
)


@pytest.fixture
def mock_settings():
    s = mock.MagicMock()
    s.is_ci_build = False
    return s


@pytest.fixture
def mock_scrapers():
    sm = mock.MagicMock()
    sm.run = mock.AsyncMock()
    return sm


@pytest.fixture
def mock_udemy_actions():
    ua = mock.MagicMock()
    ua.login = mock.MagicMock()
    ua.enroll = mock.MagicMock()
    ua.stats = mock.MagicMock()
    return ua


class TestRedeemCourses:
    @mock.patch("udemy_enroller.runner.UdemyActions")
    def test_empty_links_exit(self, mock_ua_class, mock_settings, mock_scrapers):
        mock_ua_class.return_value = mock.MagicMock()
        mock_ua_class.return_value.login = mock.MagicMock()
        mock_ua_class.return_value.stats = mock.MagicMock()
        mock_scrapers.run.return_value = []

        _redeem_courses(mock_settings, mock_scrapers)

    @mock.patch("udemy_enroller.runner.UdemyActions")
    def test_enrolled_status_sleeps(self, mock_ua_class, mock_settings, mock_scrapers):
        ua = mock.MagicMock()
        ua.enroll.return_value = UdemyStatus.ENROLLED.value
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_scrapers.run.side_effect = [["http://example.com?couponCode=TEST"], []]

        with mock.patch("udemy_enroller.runner.time.sleep") as mock_sleep:
            _redeem_courses(mock_settings, mock_scrapers)
            mock_sleep.assert_called_once()

    @mock.patch("udemy_enroller.runner.UdemyActions")
    def test_not_enrolled_status_no_sleep(
        self, mock_ua_class, mock_settings, mock_scrapers
    ):
        ua = mock.MagicMock()
        ua.enroll.return_value = UdemyStatus.EXPIRED.value
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_scrapers.run.side_effect = [["http://example.com?couponCode=TEST"], []]

        with mock.patch("udemy_enroller.runner.time.sleep") as mock_sleep:
            _redeem_courses(mock_settings, mock_scrapers)
            mock_sleep.assert_not_called()

    @mock.patch("udemy_enroller.runner.UdemyActions")
    def test_keyboard_interrupt(self, mock_ua_class, mock_settings, mock_scrapers):
        ua = mock.MagicMock()
        ua.enroll.side_effect = KeyboardInterrupt()
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_scrapers.run.return_value = ["http://example.com?couponCode=TEST"]

        _redeem_courses(mock_settings, mock_scrapers)
        ua.stats.table.assert_called_once()

    @mock.patch("udemy_enroller.runner.UdemyActions")
    def test_unexpected_exception(self, mock_ua_class, mock_settings, mock_scrapers):
        ua = mock.MagicMock()
        ua.enroll.side_effect = [ValueError("bad data"), KeyboardInterrupt()]
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_scrapers.run.side_effect = [
            ["http://example.com?couponCode=TEST"],
            ["http://example.com?couponCode=TEST2"],
        ]

        _redeem_courses(mock_settings, mock_scrapers)
        assert ua.enroll.call_count == 2

    @mock.patch("udemy_enroller.runner.UdemyActions")
    def test_ci_build_path(self, mock_ua_class, mock_settings, mock_scrapers):
        mock_settings.is_ci_build = True
        ua = mock.MagicMock()
        ua.enroll.return_value = UdemyStatus.ENROLLED.value
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_scrapers.run.return_value = ["http://example.com?couponCode=TEST"]

        _redeem_courses(mock_settings, mock_scrapers)
        assert ua.enroll.call_count == 1

    @mock.patch("udemy_enroller.runner.UdemyActions")
    def test_ci_build_keyboard_interrupt_still_shows_table(
        self, mock_ua_class, mock_settings, mock_scrapers
    ):
        mock_settings.is_ci_build = True
        ua = mock.MagicMock()
        ua.enroll.side_effect = KeyboardInterrupt()
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_scrapers.run.return_value = ["http://example.com?couponCode=TEST"]

        _redeem_courses(mock_settings, mock_scrapers)
        ua.stats.table.assert_called_once()

    def test_redeem_courses_wrapper_success(self, mock_settings):
        with mock.patch(
            "udemy_enroller.runner._redeem_courses"
        ) as mock_redeem:
            redeem_courses(mock_settings, True, False, True, False, True, 5)
            mock_redeem.assert_called_once()

    def test_redeem_courses_wrapper_exception(self, mock_settings, caplog):
        with mock.patch(
            "udemy_enroller.runner._redeem_courses",
            side_effect=RuntimeError("test error"),
        ):
            redeem_courses(mock_settings, True, False, True, True, False, 3)
            assert "Exception in redeem courses" in caplog.text


class TestRedeemCoursesUI:
    @mock.patch("udemy_enroller.runner.UdemyActionsUI")
    def test_empty_links_exit(self, mock_ua_class, mock_settings, mock_scrapers):
        ua = mock.MagicMock()
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_scrapers.run.return_value = []

        driver = mock.MagicMock()
        _redeem_courses_ui(driver, mock_settings, mock_scrapers)

    @mock.patch("udemy_enroller.runner.UdemyActionsUI")
    def test_enrolled_sleeps(self, mock_ua_class, mock_settings, mock_scrapers):
        ua = mock.MagicMock()
        ua.enroll.return_value = UdemyStatus.ENROLLED.value
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_scrapers.run.side_effect = [["http://example.com?couponCode=TEST"], []]

        driver = mock.MagicMock()
        with mock.patch("udemy_enroller.runner.time.sleep") as mock_sleep:
            _redeem_courses_ui(driver, mock_settings, mock_scrapers)
            mock_sleep.assert_called_once()

    @mock.patch("udemy_enroller.runner.UdemyActionsUI")
    def test_not_enrolled_no_sleep(self, mock_ua_class, mock_settings, mock_scrapers):
        ua = mock.MagicMock()
        ua.enroll.return_value = UdemyStatus.EXPIRED.value
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_scrapers.run.side_effect = [["http://example.com?couponCode=TEST"], []]

        driver = mock.MagicMock()
        with mock.patch("udemy_enroller.runner.time.sleep") as mock_sleep:
            _redeem_courses_ui(driver, mock_settings, mock_scrapers)
            mock_sleep.assert_not_called()

    @mock.patch("udemy_enroller.runner.UdemyActionsUI")
    def test_no_such_element_exception(
        self, mock_ua_class, mock_settings, mock_scrapers, caplog
    ):
        ua = mock.MagicMock()
        ua.enroll.side_effect = [NoSuchElementException("missing"), KeyboardInterrupt()]
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_scrapers.run.side_effect = [
            ["http://example.com?couponCode=TEST"],
            ["http://example.com?couponCode=TEST2"],
        ]

        driver = mock.MagicMock()
        _redeem_courses_ui(driver, mock_settings, mock_scrapers)
        assert "No such element" in caplog.text

    @mock.patch("udemy_enroller.runner.UdemyActionsUI")
    def test_timeout_exception(
        self, mock_ua_class, mock_settings, mock_scrapers, caplog
    ):
        ua = mock.MagicMock()
        ua.enroll.side_effect = [TimeoutException(), KeyboardInterrupt()]
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_scrapers.run.side_effect = [
            ["http://example.com?couponCode=TEST"],
            ["http://example.com?couponCode=TEST2"],
        ]

        driver = mock.MagicMock()
        _redeem_courses_ui(driver, mock_settings, mock_scrapers)
        assert "Timeout on link" in caplog.text

    @mock.patch("udemy_enroller.runner.UdemyActionsUI")
    def test_webdriver_exception(
        self, mock_ua_class, mock_settings, mock_scrapers, caplog
    ):
        ua = mock.MagicMock()
        ua.enroll.side_effect = [WebDriverException("driver err"), KeyboardInterrupt()]
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_scrapers.run.side_effect = [
            ["http://example.com?couponCode=TEST"],
            ["http://example.com?couponCode=TEST2"],
        ]

        driver = mock.MagicMock()
        _redeem_courses_ui(driver, mock_settings, mock_scrapers)
        assert "Webdriver exception" in caplog.text

    @mock.patch("udemy_enroller.runner.UdemyActionsUI")
    def test_keyboard_interrupt(self, mock_ua_class, mock_settings, mock_scrapers):
        ua = mock.MagicMock()
        ua.enroll.side_effect = KeyboardInterrupt()
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_scrapers.run.return_value = ["http://example.com?couponCode=TEST"]

        driver = mock.MagicMock()
        _redeem_courses_ui(driver, mock_settings, mock_scrapers)
        ua.stats.table.assert_called_once()

    @mock.patch("udemy_enroller.runner.UdemyActionsUI")
    def test_robot_exception(self, mock_ua_class, mock_settings, mock_scrapers):
        ua = mock.MagicMock()
        ua.enroll.side_effect = exceptions.RobotException("I am a bot")
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_scrapers.run.return_value = ["http://example.com?couponCode=TEST"]

        driver = mock.MagicMock()
        _redeem_courses_ui(driver, mock_settings, mock_scrapers)

    @mock.patch("udemy_enroller.runner.UdemyActionsUI")
    def test_unexpected_exception(
        self, mock_ua_class, mock_settings, mock_scrapers, caplog
    ):
        ua = mock.MagicMock()
        ua.enroll.side_effect = [ValueError("bad"), KeyboardInterrupt()]
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_scrapers.run.side_effect = [
            ["http://example.com?couponCode=TEST"],
            ["http://example.com?couponCode=TEST2"],
        ]

        driver = mock.MagicMock()
        _redeem_courses_ui(driver, mock_settings, mock_scrapers)
        assert "Unexpected exception" in caplog.text

    @mock.patch("udemy_enroller.runner.UdemyActionsUI")
    def test_ci_build_path(self, mock_ua_class, mock_settings, mock_scrapers):
        mock_settings.is_ci_build = True
        ua = mock.MagicMock()
        ua.enroll.return_value = UdemyStatus.ENROLLED.value
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_scrapers.run.return_value = ["http://example.com?couponCode=TEST"]

        driver = mock.MagicMock()
        _redeem_courses_ui(driver, mock_settings, mock_scrapers)
        assert ua.enroll.call_count == 1

    @mock.patch("udemy_enroller.runner.UdemyActionsUI")
    def test_duplicate_links_removed(
        self, mock_ua_class, mock_settings, mock_scrapers
    ):
        ua = mock.MagicMock()
        ua.enroll.return_value = UdemyStatus.ENROLLED.value
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        # First call returns 2 duplicate links, second call returns empty to exit loop
        mock_scrapers.run.side_effect = [
            [
                "http://example.com?couponCode=TEST",
                "http://example.com?couponCode=TEST",
            ],
            [],
        ]

        driver = mock.MagicMock()
        with mock.patch("udemy_enroller.runner.time.sleep"):
            _redeem_courses_ui(driver, mock_settings, mock_scrapers)
        assert ua.enroll.call_count == 1  # duplicate removed by set()

    def test_redeem_courses_ui_wrapper_success(self, mock_settings):
        driver = mock.MagicMock()
        with mock.patch(
            "udemy_enroller.runner._redeem_courses_ui"
        ) as mock_redeem:
            redeem_courses_ui(driver, mock_settings, True, False, True, False, True, 5)
            mock_redeem.assert_called_once()
            driver.quit.assert_called_once()

    def test_redeem_courses_ui_wrapper_exception(self, mock_settings, caplog):
        driver = mock.MagicMock()
        with mock.patch(
            "udemy_enroller.runner._redeem_courses_ui",
            side_effect=RuntimeError("test error"),
        ):
            redeem_courses_ui(driver, mock_settings, True, False, True, True, False, 3)
            assert "Exception in redeem courses" in caplog.text
            driver.quit.assert_called_once()
