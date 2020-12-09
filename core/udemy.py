import logging
import time
from enum import Enum

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.exceptions import RobotException
from core.settings import Settings

logger = logging.getLogger("udemy_enroller")


class UdemyStatus(Enum):
    """
    Possible statuses of udemy course
    """

    ENROLLED = "ENROLLED"
    EXPIRED = "EXPIRED"
    UNWANTED_LANGUAGE = "UNWANTED_LANGUAGE"
    UNWANTED_CATEGORY = "UNWANTED_CATEGORY"


class UdemyActions:
    """
    Contains any logic related to interacting with udemy website
    """

    DOMAIN = "https://www.udemy.com"

    def __init__(self, driver: WebDriver, settings: Settings):
        self.driver = driver
        self.settings = settings
        self.logged_in = False

    def login(self, is_retry=False) -> None:
        """
        Login to your udemy account

        :param bool is_retry: Is this is a login retry and we still have captcha raise RobotException

        :return: None
        """
        if not self.logged_in:
            self.driver.get(f"{self.DOMAIN}/join/login-popup/")
            try:
                email_element = self.driver.find_element_by_name("email")
                email_element.send_keys(self.settings.email)

                password_element = self.driver.find_element_by_name("password")
                password_element.send_keys(self.settings.password)

                self.driver.find_element_by_name("submit").click()
            except NoSuchElementException as e:
                is_robot = self._check_if_robot()
                if is_robot and not is_retry:
                    input(
                        "Please solve the captcha before proceeding. Hit enter once solved "
                    )
                    self.login(is_retry=True)
                    return
                if is_robot and is_retry:
                    raise RobotException("I am a bot!")
                raise e
            else:
                # TODO: Verify successful login
                self.logged_in = True

    def redeem(self, url: str) -> str:
        """
        Redeems the course url passed in

        :param str url: URL of the course to redeem
        :return: A string detailing course status
        """
        self.driver.get(url)

        course_name = self.driver.title

        # If the user has configured languages check it is a supported option
        if self.settings.languages:
            locale_xpath = "//div[@data-purpose='lead-course-locale']"
            element_text = (
                WebDriverWait(self.driver, 10)
                .until(EC.presence_of_element_located((By.XPATH, locale_xpath)))
                .text
            )

            if element_text not in self.settings.languages:
                logger.info(f"Course language not wanted: {element_text}")
                return UdemyStatus.UNWANTED_LANGUAGE.value

        if self.settings.categories:
            # If the wanted categories are specified, get all the categories of the course by
            # scraping the breadcrumbs on the top

            breadcrumbs_path = "udlite-breadcrumb"
            breadcrumbs_text_path = "udlite-heading-sm"
            breadcrumbs: WebElement = self.driver.find_element_by_class_name(
                breadcrumbs_path
            )
            breadcrumbs = breadcrumbs.find_elements_by_class_name(breadcrumbs_text_path)
            breadcrumbs = [bc.text for bc in breadcrumbs]  # Get only the text

            for category in self.settings.categories:
                if category in breadcrumbs:
                    break
            else:
                logger.info("Skipping course as it does not have a wanted category")
                return UdemyStatus.UNWANTED_CATEGORY.value

        # Enroll Now 1
        buy_course_button_xpath = "//button[@data-purpose='buy-this-course-button']"
        # We need to wait for this element to be clickable before checking if already purchased
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, buy_course_button_xpath))
        )

        # Check if already enrolled
        already_purchased_xpath = (
            "//div[starts-with(@class, 'buy-box--purchased-text-banner')]"
        )
        if self.driver.find_elements_by_xpath(already_purchased_xpath):
            logger.info(f"Already enrolled in {course_name}")
            return UdemyStatus.ENROLLED.value

        # Click to enroll in the course
        element_present = EC.presence_of_element_located(
            (By.XPATH, buy_course_button_xpath)
        )
        WebDriverWait(self.driver, 10).until(element_present).click()

        enroll_button_xpath = "//*[@class='udemy pageloaded']/div[1]/div[2]/div/div/div/div[2]/form/div[2]/div/div[4]/button"
        # Enroll Now 2
        element_present = EC.presence_of_element_located(
            (
                By.XPATH,
                enroll_button_xpath,
            )
        )
        WebDriverWait(self.driver, 10).until(element_present)

        # Check if zipcode exists before doing this
        if self.settings.zip_code:
            # Assume sometimes zip is not required because script was originally pushed without this
            try:
                zipcode_element = self.driver.find_element_by_id(
                    "billingAddressSecondaryInput"
                )
                zipcode_element.send_keys(self.settings.zip_code)

                # After you put the zip code in, the page refreshes itself and disables the enroll button for a split
                # second.
                time.sleep(1)
            except NoSuchElementException:
                pass

        # Make sure the price has loaded
        price_class_loading = "udi-circle-loader"
        WebDriverWait(self.driver, 10).until_not(
            EC.presence_of_element_located((By.CLASS_NAME, price_class_loading))
        )

        # Make sure the course is Free
        price_xpath = "//span[@data-purpose='total-price']//span"
        price_elements = self.driver.find_elements_by_xpath(price_xpath)
        # We get elements here as one of there are 2 matches for this xpath

        for price_element in price_elements:
            # We are only interested in the element which is displaying the price details
            if price_element.is_displayed():
                _price = price_element.text
                # Extract the numbers from the price text
                # This logic should work for different locales and currencies
                _numbers = "".join(filter(lambda x: x if x.isdigit() else None, _price))
                if _numbers.isdigit() and int(_numbers) > 0:
                    logger.info(
                        f"Skipping course as it now costs {_price}: {course_name}"
                    )
                    return UdemyStatus.EXPIRED.value

        # Check if state/province element exists
        billing_state_element_id = "billingAddressSecondarySelect"
        billing_state_elements = self.driver.find_elements_by_id(
            billing_state_element_id
        )
        if billing_state_elements:
            # If we are here it means a state/province element exists and needs to be filled
            # Open the dropdown menu
            billing_state_elements[0].click()

            # Pick the first element in the state/province dropdown
            first_state_xpath = (
                "//select[@id='billingAddressSecondarySelect']//option[2]"
            )
            element_present = EC.presence_of_element_located(
                (By.XPATH, first_state_xpath)
            )
            WebDriverWait(self.driver, 10).until(element_present).click()

        # Hit the final Enroll now button
        enroll_button_is_clickable = EC.element_to_be_clickable(
            (By.XPATH, enroll_button_xpath)
        )
        WebDriverWait(self.driver, 10).until(enroll_button_is_clickable).click()

        # Wait for success page to load
        success_element_class = "alert-success"
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, success_element_class))
        )

        logger.info(f"Successfully enrolled in: {course_name}")
        return UdemyStatus.ENROLLED.value

    def _check_if_robot(self) -> bool:
        """
        Simply checks if the captcha element is present on login if email/password elements are not

        :return: Bool
        """
        is_robot = True
        try:
            self.driver.find_element_by_id("px-captcha")
        except NoSuchElementException:
            is_robot = False
        return is_robot
