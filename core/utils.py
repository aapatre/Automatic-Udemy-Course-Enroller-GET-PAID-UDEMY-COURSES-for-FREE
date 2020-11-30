import logging

from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.remote.webdriver import WebDriver

from core import CourseCache, Settings, TutorialBarScraper, UdemyActions, exceptions

logger = logging.getLogger("udemy_enroller")


def _redeem_courses(driver: WebDriver, settings: Settings):
    """
    Method to scrape courses from tutorialbar.com and enroll in them on udemy

    :return:
    """
    cache = CourseCache()
    tb_scraper = TutorialBarScraper()
    udemy_actions = UdemyActions(driver, settings)
    udemy_actions.login()  # login once outside while loop
    while True:
        udemy_course_links = tb_scraper.run()

        for course_link in udemy_course_links:
            try:
                if course_link not in cache:
                    status = udemy_actions.redeem(course_link)
                    cache.add(course_link, status)
                else:
                    logger.info(f"In cache: {course_link}")
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


def redeem_courses(driver, settings) -> None:
    """
    Wrapper of _redeem_courses so we always close browser on completion

    :param driver:
    :param settings:
    :return:
    """
    try:
        _redeem_courses(driver, settings)
    finally:
        logger.info("Closing browser")
        driver.quit()
