"""Tests for cli module."""

import logging
import sys
from importlib.metadata import PackageNotFoundError
from unittest import mock

import pytest

from udemy_enroller.cli import (
    determine_if_scraper_enabled,
    enable_debug_logging,
    log_os_version,
    log_package_details,
    log_python_version,
    main,
    parse_args,
    run,
)
from udemy_enroller.logger import get_logger


class TestEnableDebugLogging:
    def test_enable_debug_logging(self):
        logger = get_logger()
        original_level = logger.level
        try:
            enable_debug_logging()
            assert logger.level == logging.DEBUG
            for handler in logger.handlers:
                assert handler.level == logging.DEBUG
        finally:
            logger.setLevel(original_level)
            for handler in logger.handlers:
                handler.setLevel(original_level)


class TestLogPackageDetails:
    def test_log_package_details_installed(self, caplog):
        logger = get_logger()
        original_level = logger.level
        logger.setLevel(logging.DEBUG)
        try:
            log_package_details()
            msg_text = " ".join(r.message for r in caplog.records)
            assert "Name:" in msg_text or "Not installed" in msg_text
        finally:
            logger.setLevel(original_level)

    def test_log_package_details_not_installed(self, caplog):
        logger = get_logger()
        original_level = logger.level
        logger.setLevel(logging.DEBUG)
        try:
            with mock.patch(
                "udemy_enroller.cli.distribution",
                side_effect=PackageNotFoundError(),
            ):
                log_package_details()
                assert any(
                    "Not installed" in record.message for record in caplog.records
                )
        finally:
            logger.setLevel(original_level)


class TestLogPythonVersion:
    def test_log_python_version(self, caplog):
        logger = get_logger()
        original_level = logger.level
        logger.setLevel(logging.DEBUG)
        try:
            log_python_version()
            msg_text = " ".join(r.message for r in caplog.records)
            assert "Python:" in msg_text
        finally:
            logger.setLevel(original_level)


class TestLogOsVersion:
    def test_log_os_version(self, caplog):
        logger = get_logger()
        original_level = logger.level
        logger.setLevel(logging.DEBUG)
        try:
            log_os_version()
            msg_text = " ".join(r.message for r in caplog.records)
            assert "OS:" in msg_text
        finally:
            logger.setLevel(original_level)


class TestDetermineIfScraperEnabled:
    def test_all_false_sets_all_true(self):
        result = determine_if_scraper_enabled(False, False, False, False, False)
        assert result == (True, True, True, True, True)

    def test_one_true_keeps_others_false(self):
        result = determine_if_scraper_enabled(True, False, False, False, False)
        assert result == (True, False, False, False, False)

    def test_all_true(self):
        result = determine_if_scraper_enabled(True, True, True, True, True)
        assert result == (True, True, True, True, True)

    def test_mixed(self):
        result = determine_if_scraper_enabled(True, False, True, False, True)
        assert result == (True, False, True, False, True)


class TestRun:
    @mock.patch("udemy_enroller.cli.redeem_courses")
    @mock.patch("udemy_enroller.cli.Settings")
    def test_run_without_browser(self, mock_settings, mock_redeem_courses):
        mock_settings_instance = mock.MagicMock()
        mock_settings.return_value = mock_settings_instance

        run(
            browser=None,
            idownloadcoupon_enabled=True,
            freebiesglobal_enabled=False,
            tutorialbar_enabled=True,
            discudemy_enabled=False,
            coursevania_enabled=False,
            max_pages=5,
            delete_settings=False,
            delete_cookie=False,
        )
        mock_settings.assert_called_once_with(False, False)
        mock_redeem_courses.assert_called_once_with(
            mock_settings_instance, True, False, True, False, False, 5
        )

    @mock.patch("udemy_enroller.cli.redeem_courses_ui")
    @mock.patch("udemy_enroller.cli.DriverManager")
    @mock.patch("udemy_enroller.cli.Settings")
    def test_run_with_browser(
        self, mock_settings, mock_driver_manager, mock_redeem_courses_ui
    ):
        mock_settings_instance = mock.MagicMock()
        mock_settings_instance.is_ci_build = False
        mock_settings.return_value = mock_settings_instance

        mock_dm = mock.MagicMock()
        mock_dm.driver = mock.MagicMock()
        mock_driver_manager.return_value = mock_dm

        run(
            browser="chrome",
            idownloadcoupon_enabled=True,
            freebiesglobal_enabled=False,
            tutorialbar_enabled=False,
            discudemy_enabled=False,
            coursevania_enabled=False,
            max_pages=3,
            delete_settings=False,
            delete_cookie=False,
        )
        mock_redeem_courses_ui.assert_called_once_with(
            mock_dm.driver,
            mock_settings_instance,
            True, False, False, False, False, 3,
        )


class TestParseArgs:
    def test_parse_args_defaults(self):
        with mock.patch.object(sys, "argv", ["udemy_enroller"]):
            args = parse_args()
            assert args.browser is None
            assert args.idownloadcoupon is False
            assert args.freebiesglobal is False
            assert args.tutorialbar is False
            assert args.discudemy is False
            assert args.coursevania is False
            assert args.max_pages == 5
            assert args.delete_settings is False
            assert args.delete_cookie is False
            assert args.debug is False

    def test_parse_args_with_browser(self):
        with mock.patch.object(sys, "argv", ["udemy_enroller", "--browser", "chrome"]):
            args = parse_args()
            assert args.browser == "chrome"

    def test_parse_args_with_scrapers(self):
        with mock.patch.object(
            sys,
            "argv",
            [
                "udemy_enroller",
                "--idownloadcoupon",
                "--tutorialbar",
                "--max-pages",
                "10",
            ],
        ):
            args = parse_args()
            assert args.idownloadcoupon is True
            assert args.tutorialbar is True
            assert args.freebiesglobal is False
            assert args.max_pages == 10

    def test_parse_args_with_flags(self):
        with mock.patch.object(
            sys,
            "argv",
            [
                "udemy_enroller",
                "--delete-settings",
                "--delete-cookie",
                "--debug",
            ],
        ):
            args = parse_args()
            assert args.delete_settings is True
            assert args.delete_cookie is True
            assert args.debug is True

    def test_parse_args_all_scrapers(self):
        with mock.patch.object(
            sys,
            "argv",
            [
                "udemy_enroller",
                "--idownloadcoupon",
                "--freebiesglobal",
                "--tutorialbar",
                "--discudemy",
                "--coursevania",
            ],
        ):
            args = parse_args()
            assert args.idownloadcoupon is True
            assert args.freebiesglobal is True
            assert args.tutorialbar is True
            assert args.discudemy is True
            assert args.coursevania is True


class TestMain:
    @mock.patch("udemy_enroller.cli.run")
    def test_main_defaults(self, mock_run):
        with mock.patch.object(sys, "argv", ["udemy_enroller"]):
            main()
            mock_run.assert_called_once_with(
                None, True, True, True, True, True, 5, False, False
            )

    @mock.patch("udemy_enroller.cli.run")
    @mock.patch("udemy_enroller.cli.log_package_details")
    @mock.patch("udemy_enroller.cli.log_python_version")
    @mock.patch("udemy_enroller.cli.log_os_version")
    def test_main_with_debug(
        self, mock_os, mock_py, mock_pkg, mock_run
    ):
        with mock.patch.object(
            sys, "argv", ["udemy_enroller", "--debug"]
        ):
            main()
            mock_os.assert_called_once()
            mock_py.assert_called_once()
            mock_pkg.assert_called_once()
            mock_run.assert_called_once()

    @mock.patch("udemy_enroller.cli.run")
    def test_main_with_browser(self, mock_run):
        with mock.patch.object(
            sys, "argv", ["udemy_enroller", "--browser", "chrome", "--idownloadcoupon"]
        ):
            main()
            mock_run.assert_called_once_with(
                "chrome", True, False, False, False, False, 5, False, False
            )

    @mock.patch("udemy_enroller.cli.run")
    def test_main_single_scraper_keeps_others_disabled(self, mock_run):
        with mock.patch.object(
            sys, "argv", ["udemy_enroller", "--freebiesglobal"]
        ):
            main()
            mock_run.assert_called_once_with(
                None, False, True, False, False, False, 5, False, False
            )
