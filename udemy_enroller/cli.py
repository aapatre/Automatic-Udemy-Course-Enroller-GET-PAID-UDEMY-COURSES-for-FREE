"""CLI entrypoint for this script."""
import argparse
import logging
import platform
import sys
from argparse import Namespace
from typing import Tuple, Union

import importlib.metadata as im

from udemy_enroller import ALL_VALID_BROWSER_STRINGS, DriverManager, Settings
from udemy_enroller.logger import get_logger
from udemy_enroller.runner import redeem_courses, redeem_courses_ui, redeem_courses_config, redeem_courses_ui_config
from udemy_enroller.run_config import RunConfig

logger = get_logger()


def enable_debug_logging() -> None:
    """
    Enable debug logging for the scripts.

    :return: None
    """
    logger.setLevel(logging.DEBUG)
    for handler in logger.handlers:
        handler.setLevel(logging.DEBUG)
    logger.info("Enabled debug logging")


def log_package_details() -> None:
    """
    Log details of the package.

    :return: None
    """
    try:
        name = "udemy_enroller"
        version = im.version(name)
        logger.debug(f"Name: {name}")
        logger.debug(f"Version: {version}")
    except im.PackageNotFoundError:
        logger.debug("Not installed on python env.")


def log_python_version():
    """
    Log version of python in use.

    :return: None
    """
    logger.debug(f"Python: {sys.version}")


def log_os_version():
    """
    Log version of the OS.

    :return: None
    """
    logger.debug(f"OS: {platform.platform()}")


def determine_if_scraper_enabled(
    idownloadcoupon_enabled: bool,
    freebiesglobal_enabled: bool,
    tutorialbar_enabled: bool,
    discudemy_enabled: bool,
    coursevania_enabled: bool,
) -> Tuple[bool, bool, bool, bool, bool]:
    """
    Determine what scrapers should be enabled and disabled.

    :return: tuple containing boolean of what scrapers should run
    """
    if (
        not idownloadcoupon_enabled
        and not freebiesglobal_enabled
        and not tutorialbar_enabled
        and not discudemy_enabled
        and not coursevania_enabled
    ):
        # Set all to True
        (
            idownloadcoupon_enabled,
            freebiesglobal_enabled,
            tutorialbar_enabled,
            discudemy_enabled,
            coursevania_enabled,
        ) = (True, True, True, True, True)

    return (
        idownloadcoupon_enabled,
        freebiesglobal_enabled,
        tutorialbar_enabled,
        discudemy_enabled,
        coursevania_enabled,
    )


def run(
    browser: str,
    idownloadcoupon_enabled: bool,
    freebiesglobal_enabled: bool,
    tutorialbar_enabled: bool,
    discudemy_enabled: bool,
    coursevania_enabled: bool,
    max_pages: Union[int, None],
    experimental_fuzz: bool,
    fuzz_seed: Union[int, None],
    max_concurrency: int,
    delete_settings: bool,
    delete_cookie: bool,
):
    """
    Run the udemy enroller script.

    :param str browser: Name of the browser we want to create a driver for
    :param bool idownloadcoupon_enabled:
    :param bool freebiesglobal_enabled:
    :param bool tutorialbar_enabled:
    :param bool discudemy_enabled:
    :param bool coursevania_enabled:
    :param int max_pages: Max pages to scrape from sites (if pagination exists)
    :param bool delete_settings: Determines if we should delete old settings file
    :param bool delete_cookie: Determines if we should delete the cookie file
    :return:
    """
    settings = Settings(delete_settings, delete_cookie)
    config = RunConfig(
        browser,
        idownloadcoupon_enabled,
        freebiesglobal_enabled,
        tutorialbar_enabled,
        discudemy_enabled,
        coursevania_enabled,
        max_pages,
        delete_settings,
        delete_cookie,
        experimental_fuzz,
        fuzz_seed,
        max_concurrency,
    )
    if browser:
        dm = DriverManager(browser=browser, is_ci_build=settings.is_ci_build)
        redeem_courses_ui_config(dm.driver, settings, config)
    else:
        redeem_courses_config(settings, config)


def parse_args() -> Namespace:
    """
    Parse args from the CLI or use the args passed in.

    :return: Args to be used in the script
    """
    parser = argparse.ArgumentParser(description="Udemy Enroller")

    parser.add_argument(
        "--browser",
        required=False,
        type=str,
        choices=ALL_VALID_BROWSER_STRINGS,
        help="Browser to use for Udemy Enroller",
    )
    parser.add_argument(
        "--idownloadcoupon",
        action="store_true",
        default=False,
        help="Run idownloadcoupon scraper",
    )
    parser.add_argument(
        "--freebiesglobal",
        action="store_true",
        default=False,
        help="Run freebiesglobal scraper",
    )
    parser.add_argument(
        "--tutorialbar",
        action="store_true",
        default=False,
        help="Run tutorialbar scraper",
    )
    parser.add_argument(
        "--discudemy",
        action="store_true",
        default=False,
        help="Run discudemy scraper",
    )
    parser.add_argument(
        "--coursevania",
        action="store_true",
        default=False,
        help="Run coursevania scraper",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=5,
        help="Max pages to scrape from sites (if pagination exists) (Default is 5)",
    )
    parser.add_argument(
        "--experimental-fuzz",
        action="store_true",
        default=False,
        help="Enable experimental fuzz mode for scrapers",
    )
    parser.add_argument(
        "--fuzz-seed",
        type=int,
        required=False,
        help="Seed for experimental fuzz mode",
    )
    parser.add_argument(
        "--max-concurrency",
        type=int,
        default=10,
        help="Max concurrent scraper tasks (Default is 10)",
    )
    parser.add_argument(
        "--delete-settings",
        action="store_true",
        default=False,
        help="Delete any existing settings file",
    )

    parser.add_argument(
        "--delete-cookie",
        action="store_true",
        default=False,
        help="Delete existing cookie file",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    parser.add_argument(
        "--email",
        type=str,
        required=False,
        help="Udemy email (overrides settings/env if provided)",
    )
    parser.add_argument(
        "--password",
        type=str,
        required=False,
        help="Udemy password (overrides settings/env if provided)",
    )

    return parser.parse_args()


def main():
    """Entrypoint for scripts."""
    args = parse_args()
    if args:
        if args.debug:
            enable_debug_logging()
            log_package_details()
            log_python_version()
            log_os_version()
        (
            idownloadcoupon_enabled,
            freebiesglobal_enabled,
            tutorialbar_enabled,
            discudemy_enabled,
            coursevania_enabled,
        ) = determine_if_scraper_enabled(
            args.idownloadcoupon,
            args.freebiesglobal,
            args.tutorialbar,
            args.discudemy,
            args.coursevania,
        )
        # Allow passing credentials via CLI flags without changing Settings API
        if args.email:
            import os
            os.environ["UDEMY_EMAIL"] = args.email
        if args.password:
            import os
            os.environ["UDEMY_PASSWORD"] = args.password
        run(
            args.browser,
            idownloadcoupon_enabled,
            freebiesglobal_enabled,
            tutorialbar_enabled,
            discudemy_enabled,
            coursevania_enabled,
            args.max_pages,
            args.experimental_fuzz,
            args.fuzz_seed,
            args.max_concurrency,
            args.delete_settings,
            args.delete_cookie,
        )
