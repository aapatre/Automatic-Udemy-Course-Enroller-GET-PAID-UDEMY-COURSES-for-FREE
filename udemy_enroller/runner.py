"""Runner."""

import asyncio
import random
import time

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
from udemy_enroller.logger import get_logger

logger = get_logger()


def redeem_courses(
    settings: Settings,
    idownloadcoupon_enabled: bool,
    freebiesglobal_enabled: bool,
    tutorialbar_enabled: bool,
    discudemy_enabled: bool,
    coursevania_enabled: bool,
    max_pages: int | None,
) -> None:
    """
    Scrape courses and enroll via REST API.

    :param settings: Core settings used for Udemy
    :param idownloadcoupon_enabled: Enable idownloadcoupon scraper
    :param freebiesglobal_enabled: Enable freebiesglobal scraper
    :param tutorialbar_enabled: Enable tutorialbar scraper
    :param discudemy_enabled: Enable discudemy scraper
    :param coursevania_enabled: Enable coursevania scraper
    :param max_pages: Max pages to scrape (None for unlimited)
    """
    try:
        scrapers = ScraperManager(
            idownloadcoupon_enabled,
            freebiesglobal_enabled,
            tutorialbar_enabled,
            discudemy_enabled,
            coursevania_enabled,
            max_pages,
        )
        udemy_actions = UdemyActions(settings)
        udemy_actions.login()

        async def _run() -> None:
            while True:
                udemy_course_links = await scrapers.run()
                logger.info(f"Total courses this time: {len(udemy_course_links)}")
                if udemy_course_links:
                    for course_link in udemy_course_links:
                        should_exit = False
                        try:
                            status = udemy_actions.enroll(course_link)
                            if status == UdemyStatus.ENROLLED.value:
                                sleep_time = random.choice(range(1, 6))
                                logger.debug(
                                    f"Sleeping for {sleep_time}s between enrolments"
                                )
                                time.sleep(sleep_time)
                        except KeyboardInterrupt:
                            udemy_actions.stats.table()
                            logger.error("Exiting the script")
                            should_exit = True
                        except Exception as e:
                            logger.error(f"Unexpected exception: {e}")
                        finally:
                            if settings.is_ci_build:
                                logger.info("We have attempted to subscribe to 1 udemy course")
                                logger.info("Ending test")
                                should_exit = True
                        if should_exit:
                            return
                else:
                    udemy_actions.stats.table()
                    logger.info("All scrapers complete")
                    return

        asyncio.run(_run())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Exception in redeem courses: {e}")


def redeem_courses_ui(
    driver,
    settings: Settings,
    idownloadcoupon_enabled: bool,
    freebiesglobal_enabled: bool,
    tutorialbar_enabled: bool,
    discudemy_enabled: bool,
    coursevania_enabled: bool,
    max_pages: int | None,
) -> None:
    """
    Scrape courses and enroll via Selenium UI.

    :param driver: WebDriver to use to complete enrolment
    :param settings: Core settings used for Udemy
    :param idownloadcoupon_enabled: Enable idownloadcoupon scraper
    :param freebiesglobal_enabled: Enable freebiesglobal scraper
    :param tutorialbar_enabled: Enable tutorialbar scraper
    :param discudemy_enabled: Enable discudemy scraper
    :param coursevania_enabled: Enable coursevania scraper
    :param max_pages: Max pages to scrape (None for unlimited)
    """
    try:
        scrapers = ScraperManager(
            idownloadcoupon_enabled,
            freebiesglobal_enabled,
            tutorialbar_enabled,
            discudemy_enabled,
            coursevania_enabled,
            max_pages,
        )
        udemy_actions = UdemyActionsUI(driver, settings)
        udemy_actions.login()

        async def _run() -> None:
            while True:
                udemy_course_links = list(set(await scrapers.run()))

                if udemy_course_links:
                    for course_link in udemy_course_links:
                        should_exit = False
                        try:
                            status = udemy_actions.enroll(course_link)
                            if status == UdemyStatus.ENROLLED.value:
                                sleep_time = random.choice(range(1, 6))
                                logger.debug(
                                    f"Sleeping for {sleep_time}s between enrolments"
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
                            should_exit = True
                        except exceptions.RobotException as e:
                            logger.error(e)
                            should_exit = True
                        except Exception as e:
                            logger.error(f"Unexpected exception: {e}")
                        finally:
                            if settings.is_ci_build:
                                logger.info("We have attempted to subscribe to 1 udemy course")
                                logger.info("Ending test")
                                should_exit = True
                        if should_exit:
                            return
                else:
                    udemy_actions.stats.table()
                    logger.info("All scrapers complete")
                    return

        asyncio.run(_run())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Exception in redeem courses: {e}")
    finally:
        logger.info("Closing browser")
        driver.quit()
