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


def run(
    browser: str,
    max_pages: Union[int, None],
    cache_hit_limit: int,
):
    """
    Run the udemy enroller script

    :param str browser: Name of the browser we want to create a driver for
    :param int or None max_pages: Max number of pages to scrape from tutorialbar.com
    :param int cache_hit_limit: If we hit the cache this many times in a row we exit the script
    :return:
    """
    settings = Settings()
    dm = DriverManager(browser=browser, is_ci_build=settings.is_ci_build)
    redeem_courses(dm.driver, settings, max_pages, cache_hit_limit)


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
        "--max-pages",
        type=int,
        default=None,
        help="Max pages to scrape from tutorialbar.com",
    )
    parser.add_argument(
        "--cache-hits",
        type=int,
        default=12,
        help="If we hit the cache this number of times in a row we will exit the script",
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
        run(args.browser, args.max_pages, args.cache_hits)


if __name__ == "__main__":
    main()
