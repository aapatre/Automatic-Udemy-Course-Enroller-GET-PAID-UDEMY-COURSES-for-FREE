from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.remote.webdriver import WebDriver

from core import Settings, TutorialBarScraper, UdemyActions, exceptions
from core.cache import CourseCache


def redeem_courses(driver: WebDriver, settings: Settings):
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
                    print(f"In cache: {course_link}")
            except NoSuchElementException as e:
                print(e)
            except TimeoutException:
                print(f"Timeout on link: {course_link}")
            except WebDriverException as e:
                print(f"Webdriver exception on link: {course_link}")
                print(e)
            except KeyboardInterrupt:
                raise
            except exceptions.RobotException as e:
                print(e)
                raise e
            except Exception as e:
                print(f"Unexpected exception: {e}")
            finally:
                if settings.is_ci_build:
                    return

        print("Moving on to the next page of the course list on tutorialbar.com")
