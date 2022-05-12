import json
import os
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from cloudscraper import create_scraper

from udemy_enroller.logging import get_logger
from udemy_enroller.settings import Settings
from udemy_enroller.utils import get_app_dir

logger = get_logger()


def format_requests(func):
    """
    Convenience method for handling requests response
    """

    def formatting(*args, **kwargs):
        result = func(*args, **kwargs)
        result.raise_for_status()
        return result.json()

    return formatting


@dataclass(unsafe_hash=True)
class RunStatistics:
    prices: List[float] = field(default_factory=list)

    expired: int = 0
    enrolled: int = 0
    already_enrolled: int = 0
    unwanted_language: int = 0
    unwanted_category: int = 0

    course_ids_start: int = 0
    course_ids_end: int = 0

    start_time = None
    end_time = None

    currency_symbol = "$"

    def savings(self):
        return sum(self.prices) or 0

    def table(self):
        logger.info("================== Run Statistics ==================")
        logger.info(f"Enrolled:                   {self.enrolled}")
        logger.info(f"Unwanted Category:          {self.unwanted_category}")
        logger.info(f"Unwanted Language:          {self.unwanted_language}")
        logger.info(f"Already Claimed:            {self.already_enrolled}")
        logger.info(f"Expired:                    {self.expired}")
        logger.info(f"Total Enrolments:           {self.course_ids_end}")
        logger.info(
            f"Savings:                    {self.currency_symbol}{self.savings():.2f}"
        )
        logger.info("================== Run Statistics ==================")


class UdemyStatus(Enum):
    """
    Possible statuses of udemy course
    """

    ALREADY_ENROLLED = "ALREADY_ENROLLED"
    ENROLLED = "ENROLLED"
    EXPIRED = "EXPIRED"
    UNWANTED_LANGUAGE = "UNWANTED_LANGUAGE"
    UNWANTED_CATEGORY = "UNWANTED_CATEGORY"


class UdemyActions:
    LOGIN_URL = "https://www.udemy.com/join/login-popup/?locale=en_US"
    MY_COURSES = (
        "https://www.udemy.com/api-2.0/users/me/subscribed-courses/?ordering=-last_accessed&fields["
        "course]=@min,enrollment_time,published_title,&fields[user]=@min"
    )
    CHECKOUT_URL = "https://www.udemy.com/payment/checkout-submit/"
    CHECK_PRICE = (
        "https://www.udemy.com/api-2.0/course-landing-components/{}/me/?couponCode={"
        "}&components=price_text,deal_badge,discount_expiration"
    )
    COURSE_DETAILS = (
        "https://www.udemy.com/api-2.0/courses/{}/?fields[course]=title,context_info,primary_category,"
        "primary_subcategory,avg_rating_recent,visible_instructors,locale,estimated_content_length,"
        "num_subscribers"
    )
    USER_DETAILS = "https://www.udemy.com/api-2.0/contexts/me/?me=True&Config=True"

    HEADERS = {
        "origin": "https://www.udemy.com",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "content-type": "application/json;charset=UTF-8",
        "x-requested-with": "XMLHttpRequest",
        "x-checkout-version": "2",
        "referer": "https://www.udemy.com/",
    }

    def __init__(self, settings: Settings, cookie_file_name: str = ".cookie"):
        self.settings = settings
        self.user_has_preferences = self.settings.categories or self.settings.languages
        self.session = requests.Session()
        self.udemy_scraper = create_scraper()
        self._cookie_file = os.path.join(get_app_dir(), cookie_file_name)
        self._enrolled_course_info = []
        self._all_course_ids = []
        self._currency_symbol = None
        self._currency = None

        self.stats = RunStatistics()

    def login(self, retry=False) -> None:
        """
        Login to Udemy using REST api
        Saves login cookies for future use

        :return: None
        """
        cookie_details = self._load_cookies()
        if cookie_details is None:
            response = self.udemy_scraper.get(self.LOGIN_URL)
            soup = BeautifulSoup(response.content, "html.parser")
            csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"}).get(
                "value"
            )
            if csrf_token is None:
                raise Exception(f"Unable to get csrf_token")

            # Prompt for email/password if we don't have them saved in settings
            if self.settings.email is None:
                self.settings.prompt_email()
            if self.settings.password is None:
                self.settings.prompt_password()

            _form_data = {
                "email": self.settings.email,
                "password": self.settings.password,
                "csrfmiddlewaretoken": csrf_token,
            }
            self.udemy_scraper.headers.update({"Referer": self.LOGIN_URL})
            auth_response = self.udemy_scraper.post(
                self.LOGIN_URL, data=_form_data, allow_redirects=False
            )
            if auth_response.status_code != 302:
                logger.debug(
                    f"Error while trying to login: {auth_response.status_code}"
                )
                logger.debug(f"Failed login response: {auth_response.text}")
                raise Exception(f"Could not login. Code: {auth_response.status_code}")
            else:
                cookie_details = {
                    "csrf_token": csrf_token,
                    "access_token": auth_response.cookies["access_token"],
                    "client_id": auth_response.cookies["client_id"],
                }
                self._cache_cookies(cookie_details)

        bearer_token = f"Bearer {cookie_details['access_token']}"
        self.session.headers = self.HEADERS
        self.session.headers.update(
            {
                "authorization": bearer_token,
                "x-udemy-authorization": bearer_token,
                "x-csrftoken": cookie_details["csrf_token"],
            }
        )
        self.session.cookies.update({"access_token": cookie_details["access_token"]})
        self.session.cookies.update({"client_id": cookie_details["client_id"]})

        try:
            self._enrolled_course_info = self.load_my_courses()

            user_details = self.load_user_details()
            # Extract the users currency info needed for checkout
            self._currency = user_details["Config"]["price_country"]["currency"]
            self._currency_symbol = user_details["Config"]["price_country"][
                "currency_symbol"
            ]
            self._all_course_ids = [
                course["id"] for course in self._enrolled_course_info
            ]
            self.stats.course_ids_start = len(self._all_course_ids)
            self.stats.currency_symbol = self._currency_symbol
        except Exception as e:
            # Log some info on the HTTPError we are getting
            if isinstance(e, requests.HTTPError):
                logger.error("HTTP error while trying to fetch Udemy information")
                logger.error(e)
                retry = True
            if not retry:
                logger.info("Retrying login")
                self._delete_cookies()
                return self.login(retry=True)
            else:
                logger.error(
                    "Unable to fetch existing courses. Login was not successful"
                )
                raise e

    def load_my_courses(self) -> List:
        """
        Loads users currently enrolled courses from Udemy

        :return: List of logged in users courses
        """
        logger.info("Loading existing course details")
        all_courses = list()
        page_size = 100

        my_courses = self.my_courses(1, page_size)
        all_courses.extend(my_courses["results"])
        total_pages = my_courses["count"] // page_size
        for page in range(2, total_pages + 2):
            my_courses = self.my_courses(page, page_size)
            if "results" in my_courses:
                all_courses.extend(my_courses["results"])
            time.sleep(1)
        logger.info(f"Currently enrolled in {len(all_courses)} courses")
        return all_courses

    @format_requests
    def load_user_details(self):
        """
        Load the current users details

        :return: Dict containing the users details
        """
        return self.session.get(self.USER_DETAILS)

    def is_enrolled(self, course_id: int) -> bool:
        """
        Check if the user is currently enrolled in the course based on course_id passed in

        :param int course_id: Check if the course_id is in the users current courses
        :return:
        """
        return course_id in self._all_course_ids

    def _add_enrolled_course(self, course_id):
        """
        Add enrolled course to the list of enrolled course ids

        :param int course_id: The course_id to add to the list
        :return:
        """
        self._all_course_ids.append(course_id)
        self.stats.course_ids_end = len(self._all_course_ids)

    def is_coupon_valid(
        self, course_id: int, coupon_code: str, course_identifier: str
    ) -> bool:
        """
        Check if the coupon is valid for a course

        :param int course_id: Id of the course to check the coupon against
        :param str coupon_code: Coupon to apply to the course
        :param str course_identifier: Name of the course used for logging
        :return:
        """
        coupon_valid = True
        coupon_details = self.coupon_details(course_id, coupon_code)
        current_price = coupon_details["price_text"]["data"]["pricing_result"]["price"][
            "amount"
        ]
        if bool(current_price):
            logger.debug(
                f"Skipping course '{course_identifier}' as it now costs {self._currency_symbol}{current_price}"
            )
            coupon_valid = False
        if not bool(
            coupon_details["price_text"]["data"]["pricing_result"]["list_price"][
                "amount"
            ]
        ):
            logger.debug(f"Skipping course '{course_identifier}' as it is always FREE")
            coupon_valid = False

        if coupon_valid:
            usual_price = coupon_details["price_text"]["data"]["pricing_result"][
                "saving_price"
            ]["amount"]
            self.stats.prices.append(usual_price)
        return coupon_valid

    def is_preferred_language(
        self, course_details: Dict, course_identifier: str
    ) -> bool:
        """
        Check if the course is in one of the languages preferred by the user

        :param dict course_details: Dictionary containing course details from Udemy
        :param str course_identifier: Name of the course used for logging
        :return: boolean
        """
        is_preferred_language = True
        course_language = course_details["locale"]["simple_english_title"]
        if course_language not in self.settings.languages:
            logger.debug(
                f"Course '{course_identifier}' language not wanted: {course_language}"
            )
            is_preferred_language = False

        return is_preferred_language

    def is_preferred_category(
        self, course_details: Dict, course_identifier: str
    ) -> bool:
        """
        Check if the course is in one of the categories preferred by the user

        :param dict course_details: Dictionary containing course details from Udemy
        :param str course_identifier: Name of the course used for logging
        :return: boolean
        """
        is_preferred_category = True

        if (
            course_details["primary_category"]["title"] not in self.settings.categories
            and course_details["primary_subcategory"]["title"]
            not in self.settings.categories
        ):
            logger.debug(
                f"Skipping course '{course_identifier}' as it does not have a wanted category"
            )
            is_preferred_category = False
        return is_preferred_category

    @format_requests
    def my_courses(self, page: int, page_size: int) -> Dict:
        """
        Load the current logged in users courses

        :param int page: page number to load
        :param int page_size: number of courses to load per page
        :return: dict containing the current users courses
        """
        return self.session.get(self.MY_COURSES + f"&page={page}&page_size={page_size}")

    @format_requests
    def coupon_details(self, course_id: int, coupon_code: str) -> Dict:
        """
        Check that the coupon is valid for the current course

        :param int course_id: Id of the course to check the coupon against
        :param str coupon_code: The coupon_code to check against the course
        :return: dictionary containing the course pricing details
        """
        return requests.get(self.CHECK_PRICE.format(course_id, coupon_code))

    @format_requests
    def course_details(self, course_id: int) -> Dict:
        """
        Retrieves details relating to the course passed in

        :param int course_id: Id of the course to get the details of
        :return: dictionary containing the course details
        """
        return requests.get(self.COURSE_DETAILS.format(course_id))

    def enroll(self, course_link: str) -> str:
        """
        Enroll the current user in the course provided

        :param str course_link: Link to the course with valid coupon attached
        :return: str representing the status of the enrolment
        """
        str_check = "?couponCode="
        if str_check in course_link:
            url, coupon_code = course_link.split(str_check)
            course_id = self._get_course_id(url)
            course_details = self.course_details(course_id)
            course_identifier = course_details.get("title", url)

            if self.is_enrolled(course_id):
                logger.info(f"Already enrolled in: '{course_identifier}'")
                self.stats.already_enrolled += 1
                return UdemyStatus.ALREADY_ENROLLED.value

            if self.user_has_preferences:
                if self.settings.languages:
                    if not self.is_preferred_language(
                        course_details, course_identifier
                    ):
                        self.stats.unwanted_language += 1
                        return UdemyStatus.UNWANTED_LANGUAGE.value
                if self.settings.categories:
                    if not self.is_preferred_category(
                        course_details, course_identifier
                    ):
                        self.stats.unwanted_category += 1
                        return UdemyStatus.UNWANTED_CATEGORY.value

            if not self.is_coupon_valid(course_id, coupon_code, course_identifier):
                self.stats.expired += 1
                return UdemyStatus.EXPIRED.value

            return self._checkout(course_id, coupon_code, course_identifier)
        else:
            logger.debug(f"Malformed url passed in: {course_link}")
            return UdemyStatus.EXPIRED.value

    def _get_course_id(self, url: str) -> int:
        """
        Get the course id from the url provided

        :param str url: Udemy url to fetch the course from
        :return: int representing the course id
        """
        response = self.session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        return int(soup.find("body")["data-clp-course-id"])

    def _checkout(
        self,
        course_id: int,
        coupon_code: str,
        course_identifier: str,
        retry: bool = False,
    ) -> str:
        """
        Checkout process for the course and coupon provided

        :param int course_id: The course id of the course to enroll in
        :param str coupon_code: The coupon code to apply on checkout
        :param str course_identifier: Name of the course being checked out
        :param str retry: If this is a retried checkout raise exception if not successful
        :return:
        """
        payload = self._build_checkout_payload(course_id, coupon_code)
        checkout_result = self.session.post(self.CHECKOUT_URL, json=payload)
        if not checkout_result.ok:
            if not retry:
                seconds = int(re.search("\\d+", checkout_result.text).group()) + 1
                logger.info(
                    f"Script has been rate limited. Sleeping for {seconds} seconds"
                )
                time.sleep(seconds)
                self._checkout(course_id, coupon_code, course_identifier, retry=True)
            else:
                raise Exception(
                    f"Checkout failed: Code: {checkout_result.status_code} Text: {checkout_result.text}"
                )
        else:
            result = checkout_result.json()
            if result["status"] == "succeeded":
                logger.info(f"Successfully enrolled: '{course_identifier}'")
                self._add_enrolled_course(course_id)
                self.stats.enrolled += 1
                return UdemyStatus.ENROLLED.value
            elif result["status"] == "failed":
                logger.warning(f"Checkout failed: '{course_identifier}'")
                logger.debug(f"Checkout payload: {payload}")
                # TODO: Shouldn't happen. Need to monitor if it does
                return UdemyStatus.EXPIRED.value

    def _build_checkout_payload(self, course_id: int, coupon_code: str) -> Dict:
        """
        Build the payload for checkout

        :param int course_id: The course id to checkout
        :param str coupon_code: The coupon code to use at checkout
        :return: dict representing the checkout payload
        """
        return {
            "checkout_event": "Submit",
            "checkout_environment": "Marketplace",
            "shopping_info": {
                "items": [
                    {
                        "discountInfo": {"code": coupon_code},
                        "buyable": {"type": "course", "id": course_id, "context": {}},
                        "price": {"amount": 0, "currency": self._currency},
                    }
                ],
                "is_cart": True,
            },
            "payment_info": {"payment_vendor": "Free", "payment_method": "free-method"},
        }

    def _cache_cookies(self, cookies: Dict) -> None:
        """
        Caches cookies for future logins

        :param cookies:
        :return:
        """
        logger.info("Caching cookie for future use")
        with open(self._cookie_file, "a+") as f:
            f.write(json.dumps(cookies))

    def _load_cookies(self) -> Dict:
        """
        Loads existing cookie file

        :return:
        """
        cookies = None

        if os.path.isfile(self._cookie_file):
            logger.info("Loading cookie from file")
            with open(self._cookie_file) as f:
                cookies = json.loads(f.read())
        else:
            logger.info("No cookie available")
        return cookies

    def _delete_cookies(self) -> None:
        """
        Remove existing cookie file

        :return:
        """
        logger.info("Deleting cookie")
        os.remove(self._cookie_file)
