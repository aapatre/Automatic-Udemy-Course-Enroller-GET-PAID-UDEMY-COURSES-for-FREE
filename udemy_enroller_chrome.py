# Install all the requirements by running requirements.py in IDLE or follow the alternate instructions at
# https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/ Make sure you have
# cleared all saved payment details on your Udemy account & the browser!
import os
import time
from distutils.util import strtobool
from multiprocessing.dummy import Pool

import requests
from bs4 import BeautifulSoup
from ruamel.yaml import YAML
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

yaml = YAML()
with open("settings.yaml") as f:
    settings = yaml.load(f)

email, password = (
    os.environ.get("UDEMY_EMAIL", settings["udemy"]["email"]),
    os.environ.get(
        "UDEMY_PASSWORD",
        settings["udemy"]["password"],
    ),
)

# Accounts for the edge case that someone removes the entire "zipcode" entry in settings.yaml instead of simply clearing the string or leaving it alone
# This shouldn't have to exist, but ?? here we are
if "zipcode" in settings["udemy"]:
    zipcode = settings["udemy"]["zipcode"]

is_ci_build = strtobool(os.environ.get("CI", "False"))
chrome_options = None
if is_ci_build:
    from selenium.webdriver.chrome.options import Options

    # Having the user-agent with Headless param was always leading to robot check
    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 "
        "Safari/537.36"
    )
    chrome_options = Options()
    # We need to run headless when using github CI
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent={0}".format(user_agent))
    chrome_options.add_argument("--window-size=1325x744")
    print("This is a CI run")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

# Maximizes the browser window since Udemy has a responsive design and the code only works
driver.maximize_window()
# in the maximized layout


def getUdemyLink(url):
    response = requests.get(url=url)

    soup = BeautifulSoup(response.content, "html.parser")

    linkForUdemy = soup.find("span", class_="rh_button_wrapper").find("a").get("href")

    return linkForUdemy


def gatherUdemyCourseLinks(courses):
    """
    Threaded fetching of the udemy course links from tutorialbar.com

    :param list courses: A list of tutorialbar.com course links we want to fetch the udemy links for
    :return: list of udemy links
    """
    thread_pool = Pool()
    results = thread_pool.map(getUdemyLink, courses)
    thread_pool.close()
    thread_pool.join()
    return results


def getTutorialBarLinks(url):
    response = requests.get(url=url)

    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.find("div", class_="rh-post-wrapper").find_all("a")
    # print(links)

    courses = []

    x = 0
    for i in range(12):
        courses.append(links[x].get("href"))
        x = x + 3

    return courses


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

    # Enroll Now 1
    element_present = EC.presence_of_element_located(
        (By.XPATH, "//button[@data-purpose='buy-this-course-button']")
    )
    WebDriverWait(driver, 10).until(element_present)

    udemyEnroll = driver.find_element_by_xpath(
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
    WebDriverWait(driver, 10).until(element_present)

    # Check if zipcode exists before doing this
    if zipcode:
        # Assume sometimes zip is not required because script was originally pushed without this
        try:
            zipcode_element = driver.find_element_by_id("billingAddressSecondaryInput")
            zipcode_element.send_keys(zipcode)

            # After you put the zip code in, the page refreshes itself and disables the enroll button for a split second.
            time.sleep(1)
        except NoSuchElementException:
            pass

    udemyEnroll = driver.find_element_by_xpath(
        '//*[@class="udemy pageloaded"]/div[1]/div[2]/div/div/div/div[2]/form/div[2]/div/div[4]/button'
    )  # Udemy
    udemyEnroll.click()


def main_function():
    page = 1  # Change the page number here only if necessary, else ignore

    loop_run_count = 0

    while True:

        print("Please Wait: Getting the course list from tutorialbar.com...")
        print("Page: " + str(page) + ", Loop run count: " + str(loop_run_count))

        url = "https://www.tutorialbar.com/all-courses/" + "page/" + str(page) + "/"
        courses = getTutorialBarLinks(url)

        udemyLinks = gatherUdemyCourseLinks(courses)

        for counter, course in enumerate(udemyLinks):
            print("Received Link {} : {}".format((counter + 1), course))

        if loop_run_count == 0:
            udemyLogin(email, password)

        for link in udemyLinks:
            # noinspection PyBroadException
            try:
                redeemUdemyCourse(link)
                if is_ci_build:
                    return
            except BaseException as e:
                if is_ci_build:
                    return
                print(
                    "Unable to enroll for this course either because you have already claimed it or the browser "
                    "window has been closed!"
                )

        page = page + 1
        loop_run_count = loop_run_count + 1

        print("Moving on to the next page of the course list on tutorialbar.com")


try:
    main_function()
except KeyboardInterrupt:
    print("Exiting the script")
except Exception as e:
    print("Error: {}".format(e))
finally:
    print("Closing browser")
    driver.quit()

main_function()
if is_ci_build:
    print("We have attempted to subscribe to 1 udemy course")
    print("Ending test")
