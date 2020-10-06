import time
import requests
import threading, queue

from bs4 import BeautifulSoup

from ruamel.yaml import YAML
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class UdemyEnroller:
    def __init__(self, browser_name, settings_file):
        self.settings = self._load_settings(settings_file)
        self.email = self.settings["udemy"]["email"]
        self.password = self.settings["udemy"]["password"]
        self.zipcode = self.settings["udemy"]["zipcode"]
        self._init_web_driver(browser_name)
        self.udemy_logged_in = False

    @staticmethod
    def _load_settings(settings_file):
        yaml = YAML()
        with open(settings_file) as f:
            settings = yaml.load(f)
        return settings

    def _init_web_driver(self, browser_name):
        if browser_name.lower() == "chrome":
            from webdriver_manager.chrome import ChromeDriverManager

            self.driver = webdriver.Chrome(ChromeDriverManager().install())
        elif browser_name.lower() in ("firefox", "ff"):
            from webdriver_manager.firefox import GeckoDriverManager

            self.driver = webdriver.Firefox(GeckoDriverManager().install())
        elif browser_name.lower() == "chromium":
            from webdriver_manager.utils import ChromeType
            from webdriver_manager.chrome import ChromeDriverManager

            self.driver = webdriver.Chrome(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            )
        elif browser_name.lower() == "edge":
            from webdriver_manager.microsoft import EdgeChromiumDriverManager

            self.driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        elif browser_name.lower() in ("internet explorer", "ie"):
            from webdriver_manager.microsoft import IEDriverManager

            self.driver = webdriver.Ie(IEDriverManager().install())

        self.driver.maximize_window()

    def getUdemyLink(self, url, link_queue):
        response = requests.get(url=url)

        soup = BeautifulSoup(response.content, "html.parser")

        linkForUdemy = (
            soup.find("span", class_="rh_button_wrapper").find("a").get("href")
        )

        link_queue.put(linkForUdemy)

    def getTutorialBarLinks(self, url):
        response = requests.get(url=url)
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find("div", class_="rh-post-wrapper").find_all("a")
        courses = []

        x = 0
        for _ in range(12):
            courses.append(links[x].get("href"))
            x += 3

        return courses, int(links[-2].text)

    def udemyLogin(self, email_text, password_text):
        self.driver.get("https://www.udemy.com/join/login-popup/")

        email = self.driver.find_element_by_name("email")
        password = self.driver.find_element_by_name("password")

        email.send_keys(email_text)
        password.send_keys(password_text)

        self.driver.find_element_by_name("submit").click()
        self.udemy_logged_in = True

    def redeemUdemyCourse(self, url):
        self.driver.get(url)
        print("Trying to Enroll for: " + self.driver.title)

        # Enroll Now 1
        element_present = EC.presence_of_element_located(
            (By.XPATH, "//button[@data-purpose='buy-this-course-button']")
        )
        WebDriverWait(self.driver, 10).until(element_present)

        udemyEnroll = self.driver.find_element_by_xpath(
            "//button[@data-purpose='buy-this-course-button']"
        )  # Udemy
        udemyEnroll.click()

        # Enroll Now 2
        element_present = EC.presence_of_element_located(
            (
                By.XPATH,
                '//*[@class="udemy pageloaded"]/div[1]/div[2]/div/div/div/div[2]/form/div[2]/div/div[4]/button',
            )
        )
        WebDriverWait(self.driver, 10).until(element_present)

        # Assume sometimes zip is not required because script was originally pushed without this
        try:
            zipcode_element = self.driver.find_element_by_id(
                "billingAddressSecondaryInput"
            )
            zipcode_element.send_keys(self.zipcode)

            # After you put the zip code in, the page refreshes itself and disables the enroll button for a split second.
            time.sleep(1)
        except NoSuchElementException:
            pass

        udemyEnroll = self.driver.find_element_by_xpath(
            '//*[@class="udemy pageloaded"]/div[1]/div[2]/div/div/div/div[2]/form/div[2]/div/div[4]/button'
        )  # Udemy
        udemyEnroll.click()

    def gather_course_links(self, courses):
        thread_pool = []

        link_queue = queue.Queue()
        for course in courses:
            thread = threading.Thread(target=self.getUdemyLink, args=(course, link_queue))
            thread_pool.append(thread)
            thread.start()

        for thread in thread_pool:
            thread.join()

        return list(link_queue.queue)

    def run(self):
        page = 1  # Change the page number here only if necessary, else ignore
        last_page = None

        while True:
            print("Please Wait: Getting the course list from tutorialbar.com...")
            if last_page is not None:
                print("Page: {} of {}".format(page, last_page))
            else:
                print("Page: {} on the first run".format(page))

            url = "https://www.tutorialbar.com/all-courses/" + "page/" + str(page) + "/"

            courses, last_page = self.getTutorialBarLinks(url)

            udemyLinks = self.gather_course_links(courses)

            for counter, course in enumerate(udemyLinks):
                print(
                    "Received Link {} : {}".format((counter + 1), course)
                )

            if not self.udemy_logged_in:
                self.udemyLogin(self.email, self.password)

            for link in udemyLinks:
                # noinspection PyBroadException
                try:
                    self.redeemUdemyCourse(link)
                except BaseException as e:
                    print(
                        "Unable to enroll for this course either because you have already claimed it or the browser "
                        "window has been closed!"
                    )

            if page == last_page:
                print("This is the last page. Goodbye")
                break

            page += 1

            print("Moving on to page {} of the course list on tutorialbar.com".format(page))
