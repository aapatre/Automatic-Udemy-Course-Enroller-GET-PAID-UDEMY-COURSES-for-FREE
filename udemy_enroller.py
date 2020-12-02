# Install all the requirements by running requirements.py in IDLE or follow the alternate instructions at
# https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/ Make sure you have
# cleared all saved payment details on your Udemy account & the browser!
import argparse
from argparse import Namespace
from typing import Union

from selenium.webdriver.remote.webdriver import WebDriver

from core import ALL_VALID_BROWSER_STRINGS, DriverManager, Settings
from core.utils import redeem_courses


def run(
    browser: str,
    max_pages: Union[int, None],
    cache_hit_limit: int,
    driver: WebDriver = None,
):
    """
    Run the udemy enroller script

    :param str browser: Name of the browser we want to create a driver for
    :param int or None max_pages: Max number of pages to scrape from tutorialbar.com
    :param int cache_hit_limit: If we hit the cache this many times in a row we exit the script
    :param WebDriver driver:
    :return:
    """
    settings = Settings()
    if driver is None:
        dm = DriverManager(browser=browser, is_ci_build=settings.is_ci_build)
        driver = dm.driver
    redeem_courses(driver, settings, max_pages, cache_hit_limit)


def parse_args(browser=None, use_manual_driver=False) -> Namespace:
    """
    Parse args from the CLI or use the args passed in

    :param str browser: Name of the browser we want to create a driver for
    :param bool use_manual_driver: If True don't create a web driver using web driver manager
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

    args = parser.parse_args()

    if args.browser is None and not use_manual_driver:
        parser.print_help()
    else:
        return args


if __name__ == "__main__":
    args = parse_args()
    if args:
        run(args.browser, args.max_pages, args.cache_hits)
