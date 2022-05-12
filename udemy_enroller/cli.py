import argparse
import logging
from argparse import Namespace
from typing import Tuple, Union

from udemy_enroller import ALL_VALID_BROWSER_STRINGS, DriverManager, Settings
from udemy_enroller.logging import get_logger
from udemy_enroller.runner import redeem_courses, redeem_courses_ui

logger = get_logger()


def enable_debug_logging() -> None:
    """
    Enable debug logging for the scripts

    :return: None
    """
    logger.setLevel(logging.DEBUG)
    for handler in logger.handlers:
        handler.setLevel(logging.DEBUG)
    logger.info(f"Enabled debug logging")


def determine_if_scraper_enabled(
    freebiesglobal_enabled: bool,
    tutorialbar_enabled: bool,
    discudemy_enabled: bool,
    coursevania_enabled: bool,
) -> Tuple[bool, bool, bool, bool]:
    """
    Determine what scrapers should be enabled and disabled

    :return: tuple containing boolean of what scrapers should run
    """
    if (
        not freebiesglobal_enabled
        and not tutorialbar_enabled
        and not discudemy_enabled
        and not coursevania_enabled
    ):
        # Set all to True
        (
            freebiesglobal_enabled,
            tutorialbar_enabled,
            discudemy_enabled,
            coursevania_enabled,
        ) = (True, True, True, True)

    return (
        freebiesglobal_enabled,
        tutorialbar_enabled,
        discudemy_enabled,
        coursevania_enabled,
    )


def run(
    browser: str,
    freebiesglobal_enabled: bool,
    tutorialbar_enabled: bool,
    discudemy_enabled: bool,
    coursevania_enabled: bool,
    max_pages: Union[int, None],
    delete_settings: bool,
    delete_cookie: bool,
):
    """
    Run the udemy enroller script

    :param str browser: Name of the browser we want to create a driver for
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
    if browser:
        dm = DriverManager(browser=browser, is_ci_build=settings.is_ci_build)
        redeem_courses_ui(
            dm.driver,
            settings,
            freebiesglobal_enabled,
            tutorialbar_enabled,
            discudemy_enabled,
            coursevania_enabled,
            max_pages,
        )
    else:
        redeem_courses(
            settings,
            freebiesglobal_enabled,
            tutorialbar_enabled,
            discudemy_enabled,
            coursevania_enabled,
            max_pages,
        )


def parse_args() -> Namespace:
    """
    Parse args from the CLI or use the args passed in

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
        help=f"Max pages to scrape from sites (if pagination exists) (Default is 5)",
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

    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    if args:
        if args.debug:
            enable_debug_logging()
        (
            freebiesglobal_enabled,
            tutorialbar_enabled,
            discudemy_enabled,
            coursevania_enabled,
        ) = determine_if_scraper_enabled(
            args.freebiesglobal, args.tutorialbar, args.discudemy, args.coursevania
        )
        run(
            args.browser,
            freebiesglobal_enabled,
            tutorialbar_enabled,
            discudemy_enabled,
            coursevania_enabled,
            args.max_pages,
            args.delete_settings,
            args.delete_cookie,
        )
