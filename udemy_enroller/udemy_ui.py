import time
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List

from price_parser import Price
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from udemy_enroller.exceptions import LoginException, RobotException
from udemy_enroller.logging import get_logger
from udemy_enroller.settings import Settings

logger = get_logger()


@dataclass(unsafe_hash=True)
class RunStatistics:
    prices: List[Decimal] = field(default_factory=list)

    expired: int = 0
    enrolled: int = 0
    already_enrolled: int = 0
    unwanted_language: int = 0
    unwanted_category: int = 0

    start_time = None

    currency_symbol = None

    def savings(self):
        return sum(self.prices) or 0

    def table(self):
        # Only show the table if we have something to show
        if self.prices:
            if self.currency_symbol is None:
                self.currency_symbol = "¤"
            run_time_seconds = int(
                (datetime.utcnow() - self.start_time).total_seconds()
            )

            logger.info("==================Run Statistics==================")
            logger.info(f"Enrolled:                   {self.enrolled}")
            logger.info(f"Unwanted Category:          {self.unwanted_category}")
            logger.info(f"Unwanted Language:          {self.unwanted_language}")
            logger.info(f"Already Claimed:            {self.already_enrolled}")
            logger.info(f"Expired:                    {self.expired}")
            logger.info(
                f"Savings:                    {self.currency_symbol}{self.savings():.2f}"
            )
            logger.info(f"Total run time (seconds):   {run_time_seconds}s")
            logger.info("==================Run Statistics==================")


class UdemyStatus(Enum):
    """
    Possible statuses of udemy course
    """

    ALREADY_ENROLLED = "ALREADY_ENROLLED"
    ENROLLED = "ENROLLED"
    EXPIRED = "EXPIRED"
    UNWANTED_LANGUAGE = "UNWANTED_LANGUAGE"
    UNWANTED_CATEGORY = "UNWANTED_CATEGORY"


class UdemyActionsUI:
    """
    Contains any logic related to interacting with udemy website
    """

    DOMAIN = "https://www.udemy.com"

    def __init__(self, driver: WebDriver, settings: Settings):
        self.driver = driver
        self.settings = settings
        self.logged_in = False
        self.stats = RunStatistics()
        self.stats.start_time = datetime.utcnow()

    def login(self, is_retry=False) -> None:
        """
        Login to your udemy account

        :param bool is_retry: Is this is a login retry and we still have captcha raise RobotException

        :return: None
        """
        if not self.logged_in:
            self.driver.get(f"{self.DOMAIN}/join/login-popup/")

            # Prompt for email/password if we don't have them saved in settings
            if self.settings.email is None:
                self.settings.prompt_email()
            if self.settings.password is None:
                self.settings.prompt_password()

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
                        "Before login. Please solve the captcha before proceeding. Hit enter once solved "
                    )
                    self.login(is_retry=True)
                    return
                if is_robot and is_retry:
                    raise RobotException("I am a bot!")
                raise e
            else:
                user_dropdown_xpath = "//a[@data-purpose='user-dropdown']"
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, user_dropdown_xpath))
                    )
                except TimeoutException:
                    is_robot = self._check_if_robot()
                    if is_robot and not is_retry:
                        input(
                            "After login. Please solve the captcha before proceeding. Hit enter once solved "
                        )
                        if self._check_if_robot():
                            raise RobotException("I am a bot!")
                        self.logged_in = True
                        return
                    raise LoginException("Udemy user failed to login")
                self.logged_in = True

    def enroll(self, url: str) -> str:
        """
        Redeems the course url passed in

        :param str url: URL of the course to redeem
        :return: A string detailing course status
        """
        self.driver.get(url)

        course_name = self.driver.title

        if not self._check_languages(course_name):
            return UdemyStatus.UNWANTED_LANGUAGE.value

        if not self._check_categories(course_name):
            return UdemyStatus.UNWANTED_CATEGORY.value

        # TODO: Make this depend on an element.
        time.sleep(2)

        # Enroll Now 1
        buy_course_button_xpath = "//button[@data-purpose='buy-this-course-button']"
        # We need to wait for this element to be clickable before checking if already purchased
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, buy_course_button_xpath))
        )

        # Check if already enrolled. If add to cart is available we have not yet enrolled
        if not self._check_enrolled(course_name):
            element_present = EC.presence_of_element_located(
                (By.XPATH, buy_course_button_xpath)
            )
            WebDriverWait(self.driver, 10).until(element_present).click()

            # Enroll Now 2
            enroll_button_xpath = (
                "//div[contains(@class, 'styles--checkout-pane-outer')]//button"
            )
            element_present = EC.presence_of_element_located(
                (
                    By.XPATH,
                    enroll_button_xpath,
                )
            )
            WebDriverWait(self.driver, 10).until(element_present)

            # Check if zipcode exists before doing this
            if self.settings.zip_code:
                # zipcode is only required in certain regions (e.g USA)
                try:
                    element_present = EC.presence_of_element_located(
                        (
                            By.ID,
                            "billingAddressSecondaryInput",
                        )
                    )
                    WebDriverWait(self.driver, 5).until(element_present).send_keys(
                        self.settings.zip_code
                    )

                    # After you put the zip code in, the page refreshes itself and disables the enroll button for a split
                    # second.
                    enroll_button_is_clickable = EC.element_to_be_clickable(
                        (By.XPATH, enroll_button_xpath)
                    )
                    WebDriverWait(self.driver, 5).until(enroll_button_is_clickable)
                except (TimeoutException, NoSuchElementException):
                    pass

            # Make sure the price has loaded
            price_class_loading = "udi-circle-loader"
            WebDriverWait(self.driver, 10).until_not(
                EC.presence_of_element_located((By.CLASS_NAME, price_class_loading))
            )

            # Make sure the course is Free
            if not self._check_price(course_name):
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
            success_element_class = (
                "//div[contains(@class, 'success-alert-banner-container')]"
            )
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, success_element_class))
            )

            logger.info(f"Successfully enrolled in: '{course_name}'")
            self.stats.enrolled += 1
            return UdemyStatus.ENROLLED.value
        else:
            return UdemyStatus.ALREADY_ENROLLED.value

    def _check_enrolled(self, course_name):
        add_to_cart_xpath = "//div[@data-purpose='add-to-cart']"
        add_to_cart_elements = self.driver.find_elements_by_xpath(add_to_cart_xpath)
        if not add_to_cart_elements or (
            add_to_cart_elements and not add_to_cart_elements[0].is_displayed()
        ):
            logger.debug(f"Already enrolled in '{course_name}'")
            self.stats.already_enrolled += 1
            return True
        return False

    def _check_languages(self, course_identifier):
        is_valid_language = True
        if self.settings.languages:
            locale_xpath = "//div[@data-purpose='lead-course-locale']"
            element_text = (
                WebDriverWait(self.driver, 10)
                .until(EC.presence_of_element_located((By.XPATH, locale_xpath)))
                .text
            )

            if element_text not in self.settings.languages:
                logger.debug(f"Course language not wanted: {element_text}")
                logger.debug(
                    f"Course '{course_identifier}' language not wanted: {element_text}"
                )
                self.stats.unwanted_language += 1
                is_valid_language = False
        return is_valid_language

    def _check_categories(self, course_identifier):
        is_valid_category = True
        if self.settings.categories:
            # If the wanted categories are specified, get all the categories of the course by
            # scraping the breadcrumbs on the top

            breadcrumbs_path = "udlite-breadcrumb"
            breadcrumbs_text_path = "udlite-heading-sm"
            breadcrumbs: WebElement = self.driver.find_element_by_class_name(
                breadcrumbs_path
            )
            breadcrumbs = breadcrumbs.find_elements_by_class_name(breadcrumbs_text_path)
            breadcrumb_text = [bc.text for bc in breadcrumbs]  # Get only the text

            for category in self.settings.categories:
                if category in breadcrumb_text:
                    is_valid_category = True
                    break
            else:
                logger.debug(
                    f"Skipping course '{course_identifier}' as it does not have a wanted category"
                )
                self.stats.unwanted_category += 1
                is_valid_category = False
        return is_valid_category

    def _check_price(self, course_name):
        course_is_free = True
        price_xpath = "//div[contains(@class, 'styles--checkout-pane-outer')]//span[@data-purpose='total-price']//span"
        price_element = self.driver.find_element_by_xpath(price_xpath)

        # We are only interested in the element which is displaying the price details
        if price_element.is_displayed():
            _price = price_element.text
            # This logic should work for different locales and currencies
            checkout_price = Price.fromstring(_price)

            # Set the currency for stats
            if (
                self.stats.currency_symbol is None
                and checkout_price.currency is not None
            ):
                self.stats.currency_symbol = checkout_price.currency

            if checkout_price.amount is None or checkout_price.amount > 0:
                logger.debug(
                    f"Skipping course '{course_name}' as it now costs {_price}"
                )
                self.stats.expired += 1
                course_is_free = False

        # Get the listed price of the course for stats
        if course_is_free:
            list_price_xpath = "//div[contains(@class, 'styles--checkout-pane-outer')]//td[@data-purpose='list-price']//span"
            list_price_element = self.driver.find_element_by_xpath(list_price_xpath)
            list_price = Price.fromstring(list_price_element.text)
            if list_price.amount is not None:
                self.stats.prices.append(list_price.amount)
        return course_is_free

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
