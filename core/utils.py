import logging
from typing import Union

from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.remote.webdriver import WebDriver

from core import CourseCache, Settings, TutorialBarScraper, UdemyActions, exceptions

logger = logging.getLogger("udemy_enroller")


def _redeem_courses(
    driver: WebDriver,
    settings: Settings,
    max_pages: Union[int, None],
    cache_hit_limit: int,
) -> None:
    """
    Method to scrape courses from tutorialbar.com and enroll in them on udemy

    :param WebDriver driver: Webdriver used to enroll in Udemy courses
    :param Settings settings: Core settings used for Udemy
    :param int max_pages: Max pages to scrape from tutorialbar.com
    :param int cache_hit_limit: If we hit the cache this many times in a row we exit the script
    :return:
    """
    cache = CourseCache()
    tb_scraper = TutorialBarScraper(max_pages)
    udemy_actions = UdemyActions(driver, settings)
    udemy_actions.login()  # login once outside while loop

    current_cache_hits = 0

    while True:
        # Check if we should exit the loop
        if not tb_scraper.script_should_run():
            break
        udemy_course_links = tb_scraper.run()

        for course_link in udemy_course_links:
            try:
                if course_link not in cache:
                    status = udemy_actions.redeem(course_link)
                    cache.add(course_link, status)
                    # Reset cache hit count as we haven't scraped this page before
                    current_cache_hits = 0
                else:
                    logger.info(f"In cache: {course_link}")

                    # Increment the cache hit count since this link is in the cache
                    current_cache_hits += 1

                # Exit the loop if we have reached the cache hit limit
                if _reached_cache_hit_limit(cache_hit_limit, current_cache_hits):
                    return
            except NoSuchElementException as e:
                logger.error(e)
            except TimeoutException:
                logger.error(f"Timeout on link: {course_link}")
            except WebDriverException:
                logger.error(f"Webdriver exception on link: {course_link}")
            except KeyboardInterrupt:
                logger.error("Exiting the script")
                raise
            except exceptions.RobotException as e:
                logger.error(e)
                raise
            except Exception as e:
                logger.error(f"Unexpected exception: {e}")
            finally:
                if settings.is_ci_build:
                    logger.info("We have attempted to subscribe to 1 udemy course")
                    logger.info("Ending test")
                    return

        logger.info("Moving on to the next page of the course list on tutorialbar.com")


def _reached_cache_hit_limit(cache_hit_limit, cache_hits) -> bool:
    """
    Check if we have reached the cache hit limit

    :param int cache_hit_limit: Limit on the number of cache hits in a row to allow
    :param int cache_hits: Current number of cache hits in a row
    :return:
    """
    reached_hit_limit = cache_hit_limit <= cache_hits
    if reached_hit_limit:
        logger.info(f"Hit cache {cache_hits} times in a row. Exiting script")
    return reached_hit_limit


def redeem_courses(
    driver: WebDriver,
    settings: Settings,
    max_pages: Union[int, None],
    cache_hit_limit: int,
) -> None:
    """
    Wrapper of _redeem_courses so we always close browser on completion

    :param WebDriver driver: Webdriver used to enroll in Udemy courses
    :param Settings settings: Core settings used for Udemy
    :param int max_pages: Max pages to scrape from tutorialbar.com
    :param int cache_hit_limit: If we hit the cache this many times in a row we exit the script
    :return:
    """
    try:
        _redeem_courses(driver, settings, max_pages, cache_hit_limit)
    finally:
        logger.info("Closing browser")
        driver.quit()
