# Install all the requirements by running requirements.py in IDLE or follow the alternate instructions at
# https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/ Make sure you have
# cleared all saved payment details on your Udemy account & the browser!
import argparse

from core import Settings
from core.driver_manager import ALL_VALID_BROWSER_STRINGS, DriverManager
from core.utils import redeem_courses


def run(browser, max_pages, driver=None):
    settings = Settings()
    if driver is None:
        dm = DriverManager(browser=browser, is_ci_build=settings.is_ci_build)
        driver = dm.driver
    redeem_courses(driver, settings, max_pages)


def parse_args(browser=None, use_manual_driver=False):
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

    args = parser.parse_args()

    if args.browser is None and not use_manual_driver:
        parser.print_help()
    else:
        return args


if __name__ == "__main__":
    args = parse_args()
    if args:
        run(args.browser, args.max_pages)
