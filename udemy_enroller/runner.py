import asyncio
import random
import time
from typing import Union

from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)

from udemy_enroller import (
    ScraperManager,
    Settings,
    UdemyActions,
    UdemyActionsUI,
    UdemyStatus,
    exceptions,
)
from udemy_enroller.logging import get_logger

logger = get_logger()


def _redeem_courses(settings: Settings, scrapers: ScraperManager) -> None:
    """
    Method to scrape courses from the supported sites and enroll in them on udemy

    :param Settings settings: Core settings used for Udemy
    :param ScraperManager scrapers:
    :return:
    """
    udemy_actions = UdemyActions(settings)
    udemy_actions.login()
    loop = asyncio.get_event_loop()

    while True:
        udemy_course_links = loop.run_until_complete(scrapers.run())
        logger.info(f"Total courses this time: {len(udemy_course_links)}")
        if udemy_course_links:
            for course_link in udemy_course_links:
                try:
                    status = udemy_actions.enroll(course_link)

                    if status == UdemyStatus.ENROLLED.value:
                        # Try to avoid udemy throttling by sleeping for 1-5 seconds
                        sleep_time = random.choice(range(1, 5))
                        logger.debug(
                            f"Sleeping for {sleep_time} seconds between enrolments"
                        )
                        time.sleep(sleep_time)
                except KeyboardInterrupt:
                    logger.error("Exiting the script")
                    return
                except Exception as e:
                    logger.error(f"Unexpected exception: {e}")
                finally:
                    if settings.is_ci_build:
                        logger.info("We have attempted to subscribe to 1 udemy course")
                        logger.info("Ending test")
                        return
        else:
            udemy_actions.stats.table()
            logger.info("All scrapers complete")
            return


def redeem_courses(
    settings: Settings,
    freebiesglobal_enabled: bool,
    tutorialbar_enabled: bool,
    discudemy_enabled: bool,
    coursevania_enabled: bool,
    max_pages: Union[int, None],
) -> None:
    """
    Wrapper of _redeem_courses which catches unhandled exceptions

    :param Settings settings: Core settings used for Udemy
    :param bool freebiesglobal_enabled: Boolean signifying if freebiesglobal scraper should run
    :param bool tutorialbar_enabled: Boolean signifying if tutorialbar scraper should run
    :param bool discudemy_enabled: Boolean signifying if discudemy scraper should run
    :param bool coursevania_enabled: Boolean signifying if coursevania scraper should run
    :param int max_pages: Max pages to scrape from sites (if pagination exists)
    :return:
    """
    try:
        scrapers = ScraperManager(
            freebiesglobal_enabled,
            tutorialbar_enabled,
            discudemy_enabled,
            coursevania_enabled,
            max_pages,
        )
        _redeem_courses(settings, scrapers)
    except Exception as e:
        logger.error(f"Exception in redeem courses: {e}")


def _redeem_courses_ui(
    driver,
    settings: Settings,
    scrapers: ScraperManager,
) -> None:
    """
    Method to scrape courses from the supported sites and enroll in them on udemy.

    :param WebDriver driver: WebDriver to use to complete enrolment
    :param Settings settings: Core settings used for Udemy
    :param ScraperManager scrapers:
    :return:
    """
    udemy_actions = UdemyActionsUI(driver, settings)
    udemy_actions.login()
    loop = asyncio.get_event_loop()

    while True:
        udemy_course_links = loop.run_until_complete(scrapers.run())

        if udemy_course_links:
            for course_link in set(
                udemy_course_links
            ):  # Cast to set to remove duplicate links
                try:
                    status = udemy_actions.enroll(course_link)
                    if status == UdemyStatus.ENROLLED.value:
                        # Try to avoid udemy throttling by sleeping for 1-5 seconds
                        sleep_time = random.choice(range(1, 5))
                        logger.debug(
                            f"Sleeping for {sleep_time} seconds between enrolments"
                        )
                        time.sleep(sleep_time)
                except NoSuchElementException as e:
                    logger.error(f"No such element: {e}")
                except TimeoutException:
                    logger.error(f"Timeout on link: {course_link}")
                except WebDriverException:
                    logger.error(f"Webdriver exception on link: {course_link}")
                except KeyboardInterrupt:
                    udemy_actions.stats.table()
                    logger.warning("Exiting the script")
                    return
                except exceptions.RobotException as e:
                    logger.error(e)
                    return
                except Exception as e:
                    logger.error(f"Unexpected exception: {e}")
                finally:
                    if settings.is_ci_build:
                        logger.info("We have attempted to subscribe to 1 udemy course")
                        logger.info("Ending test")
                        return
        else:
            udemy_actions.stats.table()
            logger.info("All scrapers complete")
            return


def redeem_courses_ui(
    driver,
    settings: Settings,
    freebiesglobal_enabled: bool,
    tutorialbar_enabled: bool,
    discudemy_enabled: bool,
    coursevania_enabled: bool,
    max_pages: Union[int, None],
) -> None:
    """
    Wrapper of _redeem_courses so we always close browser on completion

    :param WebDriver driver: WebDriver to use to complete enrolment
    :param Settings settings: Core settings used for Udemy
    :param bool freebiesglobal_enabled: Boolean signifying if freebiesglobal scraper should run
    :param bool tutorialbar_enabled: Boolean signifying if tutorialbar scraper should run
    :param bool discudemy_enabled: Boolean signifying if discudemy scraper should run
    :param bool coursevania_enabled: Boolean signifying if coursevania scraper should run
    :param int max_pages: Max pages to scrape from sites (if pagination exists)
    :return:
    """

    try:
        scrapers = ScraperManager(
            freebiesglobal_enabled,
            tutorialbar_enabled,
            discudemy_enabled,
            coursevania_enabled,
            max_pages,
        )
        _redeem_courses_ui(driver, settings, scrapers)
    except Exception as e:
        logger.error(f"Exception in redeem courses: {e}")
    finally:
        logger.info("Closing browser")
        driver.quit()
