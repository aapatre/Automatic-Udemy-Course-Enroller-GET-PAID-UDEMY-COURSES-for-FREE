from selenium.webdriver.remote.webdriver import WebDriver

from core import Settings
from core import TutorialBarScraper
from core import UdemyActions


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
                if settings.is_ci_build:
                    return
            except KeyboardInterrupt:
                raise
            except Exception:
                if settings.is_ci_build:
                    return
                print(
                    "Unable to enroll for this course either because you have already claimed it or the browser "
                    "window has been closed!"
                )

        print("Moving on to the next page of the course list on tutorialbar.com")
