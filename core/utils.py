from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.remote.webdriver import WebDriver

from core import Settings, TutorialBarScraper, UdemyActions, exceptions


def _redeem_courses(driver: WebDriver, settings: Settings):
    """
    Method to scrape courses from tutorialbar.com and enroll in them on udemy

    :return:
    """
    tb_scraper = TutorialBarScraper()
    udemy_actions = UdemyActions(driver, settings)
    udemy_actions.login()  # login once outside while loop
    while True:
        udemy_course_links = tb_scraper.run()

        for course_link in udemy_course_links:
            try:
                udemy_actions.redeem(course_link)
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
        print("Closing browser")
        driver.quit()
