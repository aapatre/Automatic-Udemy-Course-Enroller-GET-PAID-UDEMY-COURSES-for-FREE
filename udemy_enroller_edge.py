# Install all the requirements by running requirements.py in IDLE or follow the alternate instructions at
# https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/ Make sure you have
# cleared all saved payment details on your Udemy account & the browser!
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from core import Settings
from core import TutorialBarScraper

settings = Settings()

driver = webdriver.Edge(EdgeChromiumDriverManager().install())

# Maximizes the browser window since Udemy has a responsive design and the code only works
driver.maximize_window()
# in the maximized layout


def udemyLogin(email_text, password_text):
    driver.get("https://www.udemy.com/join/login-popup/")

    userEmail = driver.find_element_by_name("email")
    userPassword = driver.find_element_by_name("password")

    userEmail.send_keys(email_text)
    userPassword.send_keys(password_text)

    driver.find_element_by_name("submit").click()


def redeemUdemyCourse(url):
    driver.get(url)
    print("Trying to Enroll for: " + driver.title)

    # If the user has configured languages check it is a supported option
    if settings.languages:
        locale_xpath = "//div[@data-purpose='lead-course-locale']"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, locale_xpath)))

        locale_element = driver.find_element_by_xpath(locale_xpath)
        if locale_element.text not in settings.languages:
            print("Course language not wanted: {}".format(locale_element.text))
            return

    # Enroll Now 1
    element_present = EC.presence_of_element_located(
        (By.XPATH, "//button[@data-purpose='buy-this-course-button']"))
    WebDriverWait(driver, 10).until(element_present)

    udemyEnroll = driver.find_element_by_xpath(
        "//button[@data-purpose='buy-this-course-button']")  # Udemy
    udemyEnroll.click()

    # Enroll Now 2
    element_present = EC.presence_of_element_located((
        By.XPATH,
        '//*[@class="udemy pageloaded"]/div[1]/div[2]/div/div/div/div[2]/form/div[2]/div/div[4]/button',
    ))
    WebDriverWait(driver, 10).until(element_present)

    # Check if zipcode exists before doing this
    if settings.zip_code:
        # Assume sometimes zip is not required because script was originally pushed without this
        try:
            zipcode_element = driver.find_element_by_id(
                "billingAddressSecondaryInput")
            zipcode_element.send_keys(settings.zip_code)

            # After you put the zip code in, the page refreshes itself and disables the enroll button for a split second.
            time.sleep(1)
        except NoSuchElementException:
            pass

    udemyEnroll = driver.find_element_by_xpath(
        '//*[@class="udemy pageloaded"]/div[1]/div[2]/div/div/div/div[2]/form/div[2]/div/div[4]/button'
    )  # Udemy
    udemyEnroll.click()


def main_function():
    tb_scraper = TutorialBarScraper()
    while True:
        udemyLinks = tb_scraper.run()

        if tb_scraper.is_first_loop():
            udemyLogin(settings.email, settings.password)

        for link in udemyLinks:
            # noinspection PyBroadException
            try:
                redeemUdemyCourse(link)
            except KeyboardInterrupt:
                raise
            except Exception:
                print(
                    "Unable to enroll for this course either because you have already claimed it or the browser "
                    "window has been closed!")

        print(
            "Moving on to the next page of the course list on tutorialbar.com")


try:
    main_function()
except KeyboardInterrupt:
    print("Exiting the script")
except Exception as e:
    print("Error: {}".format(e))
finally:
    print("Closing browser")
    driver.quit()
