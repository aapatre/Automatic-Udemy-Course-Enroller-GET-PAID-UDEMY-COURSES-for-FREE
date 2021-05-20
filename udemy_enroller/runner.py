import asyncio
import random
import time
from typing import Union

from udemy_enroller import ScraperManager, Settings, UdemyActions, UdemyStatus
from udemy_enroller.logging import get_logger

logger = get_logger()


def _redeem_courses(
        settings: Settings,
        scrapers: ScraperManager,
        counter_enroled: int = 0,
        counter_already_enroled: int = 0,
        counter_expired: int = 0,
        counter_other_languages: int = 0,
        counter_other_categories: int = 0,
        counter_total: int = 0
) -> None:
    """
    Method to scrape courses from tutorialbar.com and enroll in them on udemy

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
                counter_total += 1
                try:
                    status = udemy_actions.enroll(course_link)

                    if status == UdemyStatus.ENROLLED.value:
                        counter_enroled += 1
                        # Try to avoid udemy throttling by sleeping for 1-5 seconds
                        sleep_time = random.choice(range(1, 5))
                        logger.debug(
                            f"Sleeping for {sleep_time} seconds between enrolments"
                        )
                        time.sleep(sleep_time)
                    elif status == UdemyStatus.ALREADY_ENROLLED.value:
                        counter_already_enroled += 1
                    elif status == UdemyStatus.EXPIRED.value:
                        counter_expired += 1
                    elif status == UdemyStatus.UNWANTED_LANGUAGE.value:
                        counter_other_languages += 1
                    elif status == UdemyStatus.UNWANTED_CATEGORY.value:
                        counter_other_categories += 1

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
            logger.info("All scrapers complete\n\n")
            logger.info("\t####################################")
            logger.info("\t#             RESULTS              #")
            logger.info("\t####################################")
            logger.info(f"\t#  New Enrolled Courses:     {counter_enroled:04}  #")
            logger.info(f"\t#  Already Enrolled Courses: {counter_already_enroled:04}  #")
            logger.info(f"\t#  Expired:                  {counter_expired:04}  #")
            logger.info(f"\t#  Other Languages:          {counter_other_languages:04}  #")
            logger.info(f"\t#  Other Categories:         {counter_other_categories:04}  #")
            logger.info("\t####################################")
            logger.info(f"\t#  Total Courses Scraped:    {counter_total:04}  #")
            logger.info("\t####################################")
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
    Wrapper of _redeem_courses so we always close browser on completion

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
            max_pages
        )
        _redeem_courses(settings, scrapers)
    except Exception as e:
        logger.error(f"Exception in redeem courses: {e}")
