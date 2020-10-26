import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class UdemyActions:
    """
    Contains any logic related to interacting with udemy website
    """

    DOMAIN = "https://www.udemy.com"

    def __init__(self, driver, settings):
        self.driver = driver
        self.settings = settings
        self.logged_in = False

    def login(self) -> None:
        """
        Login to your udemy account

        :return: None
        """
        if not self.logged_in:
            self.driver.get(f"{self.DOMAIN}/join/login-popup/")

            email_element = self.driver.find_element_by_name("email")
            email_element.send_keys(self.settings.email)

            password_element = self.driver.find_element_by_name("password")
            password_element.send_keys(self.settings.password)

            self.driver.find_element_by_name("submit").click()
            self.logged_in = True

    def redeem(self, url: str) -> None:
        """
        Redeems the course url passed in

        :param str url: URL of the course to redeem
        :return: None
        """
        self.driver.get(url)
        print("Trying to Enroll for: " + self.driver.title)

        # If the user has configured languages check it is a supported option
        if self.settings.languages:
            locale_xpath = "//div[@data-purpose='lead-course-locale']"
            element_text = (WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, locale_xpath))).text)

            if element_text not in self.settings.languages:
                print("Course language not wanted: {}".format(element_text))
                return

        # Enroll Now 1
        buy_course_button_xpath = "//button[@data-purpose='buy-this-course-button']"
        element_present = EC.presence_of_element_located(
            (By.XPATH, buy_course_button_xpath))
        WebDriverWait(self.driver, 10).until(element_present).click()

        enroll_button_xpath = "//*[@class='udemy pageloaded']/div[1]/div[2]/div/div/div/div[2]/form/div[2]/div/div[4]/button"
        # Enroll Now 2
        element_present = EC.presence_of_element_located((
            By.XPATH,
            enroll_button_xpath,
        ))
        WebDriverWait(self.driver, 10).until(element_present)

        # Check if zipcode exists before doing this
        if self.settings.zip_code:
            # Assume sometimes zip is not required because script was originally pushed without this
            try:
                zipcode_element = self.driver.find_element_by_id(
                    "billingAddressSecondaryInput")
                zipcode_element.send_keys(self.settings.zip_code)

                # After you put the zip code in, the page refreshes itself and disables the enroll button for a split
                # second.
                time.sleep(1)
            except NoSuchElementException:
                pass

        udemy_enroll_element_2 = self.driver.find_element_by_xpath(
            enroll_button_xpath)  # Udemy
        udemy_enroll_element_2.click()
