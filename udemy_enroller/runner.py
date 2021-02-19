import asyncio
import time
from typing import Union

from udemy_enroller import CourseCache, ScraperManager, Settings, UdemyActions
from udemy_enroller.logging import get_logger

logger = get_logger()


def _redeem_courses(
    settings: Settings,
    scrapers: ScraperManager,
) -> None:
    """
    Method to scrape courses from tutorialbar.com and enroll in them on udemy

    :param Settings settings: Core settings used for Udemy
    :param ScraperManager scrapers:
    :return:
    """
    cache = CourseCache()
    udemy_actions = UdemyActions(settings)
    udemy_actions.login()
    loop = asyncio.get_event_loop()

    while True:
        udemy_course_links = loop.run_until_complete(scrapers.run())

        if udemy_course_links:
            for course_link in udemy_course_links:
                try:
                    if course_link not in cache:
                        status = udemy_actions.enroll(course_link)
                        cache.add(course_link, status)
                        time.sleep(2)  # Try to avoid udemy throttling
                    else:
                        logger.debug(f"In cache: {course_link}")
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
            logger.info("All scrapers complete")
            return


def redeem_courses(
    settings: Settings,
    tutorialbar_enabled: bool,
    discudemy_enabled: bool,
    coursevania_enabled: bool,
    max_pages: Union[int, None],
) -> None:
    """
    Wrapper of _redeem_courses so we always close browser on completion

    :param Settings settings: Core settings used for Udemy
    :param bool tutorialbar_enabled: Boolean signifying if tutorialbar scraper should run
    :param bool discudemy_enabled: Boolean signifying if discudemy scraper should run
    :param bool coursevania_enabled: Boolean signifying if coursevania scraper should run
    :param int max_pages: Max pages to scrape from sites (if pagination exists)
    :return:
    """
    try:
        scrapers = ScraperManager(
            tutorialbar_enabled, discudemy_enabled, coursevania_enabled, max_pages
        )
        _redeem_courses(settings, scrapers)
    except Exception as e:
        logger.error(f"Exception in redeem courses: {e}")
