from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.remote.webdriver import WebDriver

from core import CourseCache, Settings, TutorialBarScraper, UdemyActions, exceptions


def _redeem_courses(driver: WebDriver, settings: Settings, max_pages):
    """
    Method to scrape courses from tutorialbar.com and enroll in them on udemy

    :return:
    """
    cache = CourseCache()
    tb_scraper = TutorialBarScraper(max_pages)
    udemy_actions = UdemyActions(driver, settings)
    udemy_actions.login()  # login once outside while loop
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
                else:
                    print(f"In cache: {course_link}")
            except NoSuchElementException as e:
                print(e)
            except TimeoutException:
                print(f"Timeout on link: {course_link}")
            except WebDriverException as e:
                print(f"Webdriver exception on link: {course_link}")
                print(e)
            except KeyboardInterrupt:
                print("Exiting the script")
                raise
            except exceptions.RobotException as e:
                print(e)
                raise e
            except Exception as e:
                print(f"Unexpected exception: {e}")
            finally:
                if settings.is_ci_build:
                    print("We have attempted to subscribe to 1 udemy course")
                    print("Ending test")
                    return

        print("Moving on to the next page of the course list on tutorialbar.com")


def redeem_courses(driver, settings, max_pages) -> None:
    """
    Wrapper of _redeem_courses so we always close browser on completion

    :param driver:
    :param settings:
    :param max_pages:
    :return:
    """
    try:
        _redeem_courses(driver, settings, max_pages)
    finally:
        print("Closing browser")
        driver.quit()
