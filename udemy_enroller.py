import argparse
import logging
from argparse import Namespace
from typing import Union

from core import ALL_VALID_BROWSER_STRINGS, DriverManager, Settings
from core.utils import redeem_courses

logger = logging.getLogger("udemy_enroller")


def enable_debug_logging() -> None:
    """
    Enable debug logging for the scripts

    :return: None
    """
    logger.setLevel(logging.DEBUG)
    for handlers in logger.handlers:
        handlers.setLevel(logging.DEBUG)
    logger.info(f"Enabled debug logging")


def determine_if_scraper_enabled(
    tutorialbar_enabled: bool,
    comidoc_enabled: bool,
):
    """


    :return: None
    """
    if not tutorialbar_enabled and not comidoc_enabled:
        # Set both to True since user has not enabled a specific scraper i.e Run all scrapers
        tutorialbar_enabled, comidoc_enabled = True, True
    return tutorialbar_enabled, comidoc_enabled


def run(
    browser: str,
    tutorialbar_enabled: bool,
    comidoc_enabled: bool,
    max_pages: Union[int, None],
):
    """
    Run the udemy enroller script

    :param str browser: Name of the browser we want to create a driver for
    :param bool tutorialbar_enabled:
    :param bool comidoc_enabled:
    :param int or None max_pages: Max number of pages to scrape from tutorialbar.com
    :return:
    """
    settings = Settings()
    dm = DriverManager(browser=browser, is_ci_build=settings.is_ci_build)
    redeem_courses(dm.driver, settings, tutorialbar_enabled, comidoc_enabled, max_pages)


def parse_args(browser=None) -> Namespace:
    """
    Parse args from the CLI or use the args passed in

    :param str browser: Name of the browser we want to create a driver for
    :return: Args to be used in the script
    """
    parser = argparse.ArgumentParser(description="Udemy Enroller")

    parser.add_argument(
        "--browser",
        type=str,
        default=browser,
        choices=ALL_VALID_BROWSER_STRINGS,
        help="Browser to use for Udemy Enroller",
    )
    parser.add_argument(
        "--tutorialbar",
        action="store_true",
        default=False,
        help="Run tutorialbar scraper",
    )
    parser.add_argument(
        "--comidoc",
        action="store_true",
        default=False,
        help="Run comidoc scraper",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=5,
        help=f"Max pages to scrape from tutorialbar (Default is 5)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    if args.browser is None:
        parser.print_help()
    else:
        return args


def main():
    args = parse_args()
    if args:
        if args.debug:
            enable_debug_logging()
        tutorialbar_enabled, comidoc_enabled = determine_if_scraper_enabled(
            args.tutorialbar, args.comidoc
        )
        run(args.browser, tutorialbar_enabled, comidoc_enabled, args.max_pages)


if __name__ == "__main__":
    main()
