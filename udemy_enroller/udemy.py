import json
import os
import time
from enum import Enum
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from cloudscraper import create_scraper

from udemy_enroller.logging import get_logger
from udemy_enroller.settings import Settings
from udemy_enroller.utils import get_app_dir

logger = get_logger()


class UdemyStatus(Enum):
    """
    Possible statuses of udemy course
    """

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
    CHECK_PRICE = "https://www.udemy.com/api-2.0/course-landing-components/{}/me/?couponCode={}&components=price_text,deal_badge,discount_expiration"
    COURSE_DETAILS = "https://www.udemy.com/api-2.0/courses/{}/?fields[course]=context_info,primary_category,primary_subcategory,avg_rating_recent,visible_instructors,locale,estimated_content_length,num_subscribers"

    HEADERS = {
        "origin": "https://www.udemy.com",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 "
        "Safari/537.36",
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

    def login(self) -> None:
        cookie_details = self._load_cookies()
        if cookie_details is None:
            response = self.udemy_scraper.get(self.LOGIN_URL)
            soup = BeautifulSoup(response.content, "html.parser")
            csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]
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
                raise Exception("Could not login")
            else:
                cookie_details = {
                    "csrf_token": csrf_token,
                    "access_token": auth_response.cookies["access_token"],
                    "client_id": auth_response.cookies["client_id"],
                }
                self._cache_cookies(cookie_details)
        else:
            cookie_details = self._load_cookies()
            logger.info("Loaded cookies from file")

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
        except Exception as e:
            logger.error("Unable to fetch existing courses. Login was not successful")
            raise e

    def load_my_courses(self) -> List:
        logger.info("Loading existing course details")
        all_courses = list()
        page_size = 100

        my_courses = self.my_courses(1, page_size)
        all_courses.extend(my_courses["results"])
        total_pages = my_courses["count"] // page_size
        for page in range(2, total_pages + 2):
            my_courses = self.my_courses(page, page_size)
            all_courses.extend(my_courses["results"])
            time.sleep(1)

        return all_courses

    def is_enrolled(self, course_id) -> bool:
        enrolled = False
        all_course_ids = [course["id"] for course in self._enrolled_course_info]
        if course_id in all_course_ids:
            enrolled = True

        return enrolled

    def is_coupon_valid(self, course_id: int, coupon_code: str) -> bool:
        coupon_valid = True
        coupon_details = self.coupon_details(course_id, coupon_code)
        current_price = coupon_details["price_text"]["data"]["pricing_result"]["price"][
            "amount"
        ]
        if bool(current_price):
            logger.debug(f"Skipping course as it now costs {current_price}")
            coupon_valid = False

        return coupon_valid

    def is_preferred_language(self, course_details: Dict) -> bool:
        is_preferred_language = True
        course_language = course_details["locale"]["simple_english_title"]
        if course_language not in self.settings.languages:
            logger.debug(f"Course language not wanted: {course_language}")
            is_preferred_language = False

        return is_preferred_language

    def is_preferred_category(self, course_details: Dict) -> bool:
        is_preferred_category = True

        if (
            course_details["primary_category"]["title"] not in self.settings.categories
            and course_details["primary_subcategory"]["title"]
            not in self.settings.categories
        ):
            logger.debug("Skipping course as it does not have a wanted category")
            is_preferred_category = False
        return is_preferred_category

    def my_courses(self, page, page_size) -> Dict:
        response = self.session.get(
            self.MY_COURSES + f"&page={page}&page_size={page_size}"
        )
        return response.json()

    def coupon_details(self, course_id: int, coupon_code: str) -> Dict:
        response = requests.get(self.CHECK_PRICE.format(course_id, coupon_code))
        return response.json()

    def course_details(self, course_id: int) -> Dict:
        response = requests.get(self.COURSE_DETAILS.format(course_id))
        return response.json()

    def enroll(self, course_link: str) -> str:
        url, coupon_code = course_link.split("?couponCode=")
        course_id = self._get_course_id(url)

        if self.is_enrolled(course_id):
            logger.info(f"Already enrolled in {url}")
            return UdemyStatus.ENROLLED.value

        if self.user_has_preferences:
            course_details = self.course_details(course_id)
            if self.settings.languages:
                if not self.is_preferred_language(course_details):
                    return UdemyStatus.UNWANTED_LANGUAGE.value
            if self.settings.categories:
                if not self.is_preferred_category(course_details):
                    return UdemyStatus.UNWANTED_CATEGORY.value

        if not self.is_coupon_valid(course_id, coupon_code):
            return UdemyStatus.EXPIRED.value

        self._checkout(course_id, coupon_code, url)

    def _get_course_id(self, url: str) -> int:
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        return int(soup.find("body")["data-clp-course-id"])

    def _checkout(self, course_id: int, coupon_code: str, url: str) -> str:
        payload = self._build_checkout_payload(course_id, coupon_code)
        checkout_result = self.session.post(self.CHECKOUT_URL, json=payload)
        if not checkout_result.ok:
            logger.error(
                f"Checkout failed: Code: {checkout_result.status_code} Text: {checkout_result.text}"
            )
            # TODO: Handle non 200 responses
            #  e.g. Status code: 429 {"detail":"Request was throttled. Expected available in 9 seconds."}
        else:
            result = checkout_result.json()
            if result["status"] == "failed":
                logger.warning("Checkout failed")
                # TODO: Shouldn't happen. Need to monitor if it does
                return UdemyStatus.EXPIRED.value
            elif result["status"] == "succeeded":
                logger.info(f"Successfully enrolled: {url}")
                return UdemyStatus.ENROLLED.value

    @staticmethod
    def _build_checkout_payload(course_id: int, discount_code: str) -> Dict:
        """

        :param course_id:
        :param discount_code:
        :return:
        """
        return {
            "checkout_event": "Submit",
            "shopping_cart": {
                "items": [
                    {
                        "discountInfo": {"code": discount_code},
                        "purchasePrice": {
                            "amount": 0,
                            "currency": "EUR",
                            "price_string": "Free",
                            "currency_symbol": "€",
                        },
                        "buyableType": "course",
                        "buyableId": course_id,
                        "buyableContext": {},
                    }
                ],
                "is_cart": True,
            },
            "payment_info": {"payment_vendor": "Free", "payment_method": "free-method"},
        }

    def _cache_cookies(self, cookies: Dict) -> None:
        with open(self._cookie_file, "a+") as f:
            f.write(json.dumps(cookies))

    def _load_cookies(self) -> Dict:
        cookies = None
        if os.path.isfile(self._cookie_file):
            with open(self._cookie_file) as f:
                cookies = json.loads(f.read())
        return cookies
