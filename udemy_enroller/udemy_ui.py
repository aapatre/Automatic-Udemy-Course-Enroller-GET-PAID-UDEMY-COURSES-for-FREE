"""Udemy UI."""
import time
from dataclasses import dataclass, field
import os
import json
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List

from price_parser import Price
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from udemy_enroller.exceptions import LoginException, RobotException
from udemy_enroller.logger import get_logger
from udemy_enroller.settings import Settings
from udemy_enroller.utils import get_app_dir

logger = get_logger()


@dataclass(unsafe_hash=True)
class RunStatistics:
    """Gather statistics on courses enrolled in."""

    prices: List[Decimal] = field(default_factory=list)

    expired: int = 0
    enrolled: int = 0
    already_enrolled: int = 0
    unwanted_language: int = 0
    unwanted_category: int = 0

    start_time = None

    currency_symbol = None

    def savings(self) -> int:
        """Calculate the savings made from enrolling to these courses."""
        return sum(self.prices) or 0

    def table(self):
        """Log table of statistics to output."""
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
    """Possible statuses of udemy course."""

    ALREADY_ENROLLED = "ALREADY_ENROLLED"
    ENROLLED = "ENROLLED"
    EXPIRED = "EXPIRED"
    UNWANTED_LANGUAGE = "UNWANTED_LANGUAGE"
    UNWANTED_CATEGORY = "UNWANTED_CATEGORY"


class UdemyActionsUI:
    """Contains any logic related to interacting with udemy website."""

    DOMAIN = "https://www.udemy.com"

    def __init__(self, driver: WebDriver, settings: Settings):
        """Initialize."""
        self.driver = driver
        self.settings = settings
        self.logged_in = False
        self.stats = RunStatistics()
        self.stats.start_time = datetime.utcnow()

    def login(self, is_retry=False) -> None:
        """
        Login to your udemy account.

        :param bool is_retry: Is this is a login retry and we still have captcha raise RobotException

        :return: None
        """
        if not self.logged_in:
            # Try cookie-based login first
            try:
                self.driver.get(self.DOMAIN)
                cookie_path = os.path.join(get_app_dir(), ".cookie")
                if os.path.isfile(cookie_path):
                    with open(cookie_path) as f:
                        cookies = json.loads(f.read())
                    for k in ("access_token", "client_id", "csrftoken"):
                        if k in cookies:
                            self.driver.add_cookie({
                                "domain": "www.udemy.com",
                                "name": k,
                                "value": cookies[k],
                                "path": "/",
                            })
                    self.driver.get(self.DOMAIN)
                    user_dropdown_xpath = "//a[@data-purpose='user-dropdown']"
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, user_dropdown_xpath))
                        )
                        self.logged_in = True
                        return
                    except TimeoutException:
                        pass
            except Exception:
                pass

            # Fallback to interactive login
            try:
                self.driver.get(self.DOMAIN)
                login_link = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/join/login')]")
                ))
                login_link.click()
            except Exception:
                self.driver.get(f"{self.DOMAIN}/join/login/?locale=en_US&next=%2F")

            # Prompt for email/password if we don't have them saved in settings
            if self.settings.email is None:
                self.settings.prompt_email()
            if self.settings.password is None:
                self.settings.prompt_password()

            try:
                # Wait for fields; if inside iframe, try switching
                email_element = None
                email_selectors = [
                    (By.NAME, "email"),
                    (By.CSS_SELECTOR, "input[name='email']"),
                    (By.CSS_SELECTOR, "input[id*='email']"),
                    (By.XPATH, "//input[contains(@name,'email') or contains(@id,'email')]")
                ]
                # Try default content
                for by, sel in email_selectors:
                    try:
                        email_element = WebDriverWait(self.driver, 8).until(
                            EC.presence_of_element_located((by, sel))
                        )
                        break
                    except TimeoutException:
                        email_element = None
                # Try iframes
                if email_element is None:
                    frames = self.driver.find_elements(By.TAG_NAME, "iframe")
                    for fr in frames:
                        try:
                            self.driver.switch_to.frame(fr)
                            for by, sel in email_selectors:
                                try:
                                    email_element = WebDriverWait(self.driver, 5).until(
                                        EC.presence_of_element_located((by, sel))
                                    )
                                    break
                                except TimeoutException:
                                    email_element = None
                            if email_element is not None:
                                break
                        except Exception:
                            pass
                        finally:
                            if email_element is None:
                                self.driver.switch_to.default_content()
                if email_element is None:
                    raise NoSuchElementException("email field not found")

                email_element.send_keys(self.settings.email)

                password_element = None
                password_selectors = [
                    (By.NAME, "password"),
                    (By.CSS_SELECTOR, "input[name='password']"),
                    (By.CSS_SELECTOR, "input[type='password']"),
                    (By.CSS_SELECTOR, "input[id*='password']"),
                    (By.XPATH, "//input[contains(@name,'password') or contains(@id,'password')]")
                ]
                for by, sel in password_selectors:
                    try:
                        password_element = WebDriverWait(self.driver, 8).until(
                            EC.presence_of_element_located((by, sel))
                        )
                        break
                    except TimeoutException:
                        password_element = None
                if password_element is None:
                    frames = self.driver.find_elements(By.TAG_NAME, "iframe")
                    for fr in frames:
                        try:
                            self.driver.switch_to.frame(fr)
                            for by, sel in password_selectors:
                                try:
                                    password_element = WebDriverWait(self.driver, 5).until(
                                        EC.presence_of_element_located((by, sel))
                                    )
                                    break
                                except TimeoutException:
                                    password_element = None
                            if password_element is not None:
                                break
                        except Exception:
                            pass
                        finally:
                            if password_element is None:
                                self.driver.switch_to.default_content()
                if password_element is None:
                    raise NoSuchElementException("password field not found")
                password_element.send_keys(self.settings.password)

                try:
                    self.driver.find_element(
                        By.CSS_SELECTOR, "button[class*='auth-submit-button']"
                    ).click()
                except NoSuchElementException:
                    WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
                    ).click()
                # Return to default content before checking for user dropdown
                try:
                    self.driver.switch_to.default_content()
                except Exception:
                    pass
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
        Redeems the course url passed in.

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
            element = WebDriverWait(self.driver, 10).until(element_present)
            try:
                element.click()
            except StaleElementReferenceException:
                element = WebDriverWait(self.driver, 5).until(element_present)
                element.click()

            # Enroll Now 2
            enroll_button_xpath = "//div[starts-with(@class, 'checkout-button--checkout-button--container')]//button"
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

                    # After you put the zip code in, the page refreshes itself and disables
                    # the enroll button for a split second.
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
            billing_state_elements = self.driver.find_elements(
                By.ID, billing_state_element_id
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
            enroll_button_is_clickable = EC.element_to_be_clickable((By.XPATH, enroll_button_xpath))
            btn = WebDriverWait(self.driver, 10).until(enroll_button_is_clickable)
            try:
                btn.click()
            except StaleElementReferenceException:
                btn = WebDriverWait(self.driver, 5).until(enroll_button_is_clickable)
                btn.click()

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
        add_to_cart_xpath = (
            "//div[starts-with(@class, 'buy-box')]//div[@data-purpose='add-to-cart']"
        )
        add_to_cart_elements = self.driver.find_elements(By.XPATH, add_to_cart_xpath)
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
            breadcrumbs: WebElement = self.driver.find_element(
                By.CLASS_NAME, breadcrumbs_path
            )
            breadcrumb_elements = breadcrumbs.find_elements(
                By.CLASS_NAME, breadcrumbs_text_path
            )
            breadcrumb_text = [
                bc.text for bc in breadcrumb_elements
            ]  # Get only the text

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
        price_xpath = "//div[contains(@data-purpose, 'total-amount-summary')]//span[2]"
        price_element = self.driver.find_element(By.XPATH, price_xpath)

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
            list_price_xpath = (
                "//div[starts-with(@class, 'order-summary--original-price-text')]//span"
            )
            list_price_element = self.driver.find_element(By.XPATH, list_price_xpath)
            list_price = Price.fromstring(list_price_element.text)
            if list_price.amount is not None:
                self.stats.prices.append(list_price.amount)
        return course_is_free

    def _check_if_robot(self) -> bool:
        """
        Simply checks if the captcha element is present on login if email/password elements are not.

        :return: Bool
        """
        is_robot = True
        try:
            self.driver.find_element(By.ID, "px-captcha")
        except NoSuchElementException:
            is_robot = False
        return is_robot
