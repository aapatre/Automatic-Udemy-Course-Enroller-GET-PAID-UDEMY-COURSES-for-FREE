from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver

from core import Settings, TutorialBarScraper, UdemyActions, exceptions


def redeem_courses(driver: WebDriver, settings: Settings):
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
            except KeyboardInterrupt:
                raise
            except (exceptions.RobotException, Exception) as e:
                print(e)
                raise e
            finally:
                if settings.is_ci_build:
                    return

        print("Moving on to the next page of the course list on tutorialbar.com")
