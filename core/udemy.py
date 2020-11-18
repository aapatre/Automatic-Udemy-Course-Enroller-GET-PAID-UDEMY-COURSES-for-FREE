import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.exceptions import RobotException
from core.settings import Settings


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
                elif is_robot and is_retry:
                    raise RobotException("I am a bot!")
                else:
                    raise e
            else:
                # TODO: Verify successful login
                self.logged_in = True

    def redeem(self, url: str) -> None:
        """
        Redeems the course url passed in

        :param str url: URL of the course to redeem
        :return: None
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
                print(f"Course language not wanted: {element_text}")
                return
        if self.settings.categories:
            # If the wanted categories are specified, get all the categories of the course by
            # scraping the breadcrumbs on the top

            breadcrumbs_path = "udlite-breadcrumb"
            breadcrumbs_text_path = "udlite-breadcrumb"
            breadcrumbs: WebElement = self.driver.find_element_by_class_name(breadcrumbs_path)
            breadcrumbs = breadcrumbs.find_elements_by_class_name(breadcrumbs_text_path)
            breadcrumbs = [bc.text for bc in breadcrumbs]  # Get only the text

            for category in self.settings.categories:
                if category in breadcrumbs:
                    break
            else:
                return print("Skipping course as it does not have a wanted category")

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
            print(f"Already enrolled in {course_name}")
            return

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
                    print(f"Skipping course as it now costs {_price}: {course_name}")
                    return

        # Hit the final Enroll now button
        udemy_enroll_element_2 = self.driver.find_element_by_xpath(enroll_button_xpath)
        udemy_enroll_element_2.click()

        print(f"Successfully enrolled in: {course_name}")

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
