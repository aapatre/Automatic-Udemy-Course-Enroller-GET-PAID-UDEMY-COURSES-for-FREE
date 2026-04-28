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
from udemy_enroller.runner import redeem_courses, redeem_courses_ui


@pytest.fixture
def mock_settings():
    s = mock.MagicMock()
    s.is_ci_build = False
    return s


@pytest.fixture(autouse=True)
def mock_asyncio_run():
    """Mock asyncio.run to prevent it from actually running coroutines."""
    def _noop(coro):
        # Close the coroutine to prevent RuntimeWarning
        if hasattr(coro, 'close'):
            coro.close()
    with mock.patch("udemy_enroller.runner.asyncio.run", side_effect=_noop) as m:
        yield m


class TestRedeemCourses:
    @mock.patch("udemy_enroller.runner.UdemyActions")
    def test_creates_and_logs_in(self, mock_ua_class, mock_settings, mock_asyncio_run):
        ua = mock.MagicMock()
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua

        redeem_courses(mock_settings, True, False, True, False, True, 5)
        mock_ua_class.assert_called_once_with(mock_settings)
        ua.login.assert_called_once()

    @mock.patch("udemy_enroller.runner.UdemyActions")
    def test_exception_caught(self, mock_ua_class, mock_settings, mock_asyncio_run, caplog):
        ua = mock.MagicMock()
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_asyncio_run.side_effect = RuntimeError("test error")

        redeem_courses(mock_settings, True, False, True, False, True, 5)
        assert "Exception in redeem courses" in caplog.text

    @mock.patch("udemy_enroller.runner.UdemyActions")
    def test_keyboard_interrupt_caught(self, mock_ua_class, mock_settings, mock_asyncio_run):
        ua = mock.MagicMock()
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_asyncio_run.side_effect = KeyboardInterrupt()

        # Should not raise
        redeem_courses(mock_settings, True, False, True, False, True, 5)


class TestRedeemCoursesUI:
    @mock.patch("udemy_enroller.runner.UdemyActionsUI")
    def test_creates_and_logs_in(self, mock_ua_class, mock_settings, mock_asyncio_run):
        ua = mock.MagicMock()
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua

        driver = mock.MagicMock()
        redeem_courses_ui(driver, mock_settings, True, False, True, False, True, 5)
        mock_ua_class.assert_called_once_with(driver, mock_settings)
        ua.login.assert_called_once()

    @mock.patch("udemy_enroller.runner.UdemyActionsUI")
    def test_driver_quit_on_success(self, mock_ua_class, mock_settings, mock_asyncio_run):
        ua = mock.MagicMock()
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua

        driver = mock.MagicMock()
        redeem_courses_ui(driver, mock_settings, True, False, True, False, True, 5)
        driver.quit.assert_called_once()

    @mock.patch("udemy_enroller.runner.UdemyActionsUI")
    def test_exception_caught(self, mock_ua_class, mock_settings, mock_asyncio_run, caplog):
        ua = mock.MagicMock()
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_asyncio_run.side_effect = RuntimeError("test error")

        driver = mock.MagicMock()
        redeem_courses_ui(driver, mock_settings, True, False, True, False, True, 5)
        assert "Exception in redeem courses" in caplog.text
        driver.quit.assert_called_once()

    @mock.patch("udemy_enroller.runner.UdemyActionsUI")
    def test_keyboard_interrupt_driver_quit(self, mock_ua_class, mock_settings, mock_asyncio_run):
        ua = mock.MagicMock()
        ua.stats = mock.MagicMock()
        mock_ua_class.return_value = ua
        mock_asyncio_run.side_effect = KeyboardInterrupt()

        driver = mock.MagicMock()
        redeem_courses_ui(driver, mock_settings, True, False, True, False, True, 5)
        driver.quit.assert_called_once()
