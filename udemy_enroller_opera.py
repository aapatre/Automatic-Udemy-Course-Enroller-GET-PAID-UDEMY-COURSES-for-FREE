"""
# **Get Paid Udemy Courses for Free with this Python Script!**
## **Install the necessary dependencies before running the code**
---
Requests module for Python:
> pip install requests
BeautifulSoup Web-Scraping Library for Python:
> pip install beautifulsoup4
Selenium Browser Automation Tool  for Python:
> pip install selenium
Required Python version:
> Python 3.8
"""

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.opera import OperaDriverManager
import time


f = open("settings.txt", "r")

email, password, zipcode = f.readline().rstrip('\n'), f.readline().rstrip('\n'), f.readline().rstrip('\n')

driver = webdriver.Opera(executable_path=OperaDriverManager().install())

driver.maximize_window()  #Maximizes the browser window since Udemy has a responsive design and the code only works in the maximized layout

def getUdemyLink(url):
    response = requests.get(
    url = url
    )

    soup = BeautifulSoup(response.content,'html.parser')

    linkForUdemy = soup.find('span', class_="rh_button_wrapper").find('a').get('href')

    return linkForUdemy

def getTutorialBarLinks(url):
    response = requests.get(
    url = url
    )

    soup = BeautifulSoup(response.content,'html.parser')


    links = soup.find('div', class_="rh-post-wrapper").find_all('a')
    #print(links)

    courses=[]

    x=0
    for i in range(12):
        courses.append(links[x].get('href'))
        x=x+3

    return courses

def udemyLogin(email_text,password_text):
    
    driver.get("https://www.udemy.com/join/login-popup/")

    email = driver.find_element_by_name("email")
    password = driver.find_element_by_name("password")

    email.send_keys(email_text)
    password.send_keys(password_text)

    driver.find_element_by_name("submit").click()

def redeemUdemyCourse(url):

    driver.get(url)
    print("Trying to Enroll for: " + driver.title)
    
    #Enroll Now 1
    element_present = EC.presence_of_element_located((By.XPATH, "//button[@data-purpose='buy-this-course-button']"))
    WebDriverWait(driver, 10).until(element_present)

    udemyEnroll = driver.find_element_by_xpath("//button[@data-purpose='buy-this-course-button']") #Udemy
    udemyEnroll.click()

    #Enroll Now 2
    element_present = EC.presence_of_element_located((By.XPATH, "//*[@id=\"udemy\"]/div[1]/div[2]/div/div/div/div[2]/form/div[2]/div/div[4]/button"))
    WebDriverWait(driver, 10).until(element_present)

    #Assume sometimes zip is not required because script was originally pushed without this
    try:
        zipcode_element = driver.find_element_by_id("billingAddressSecondaryInput")
        zipcode_element.send_keys(zipcode)

        #After you put the zip code in, the page refreshes itself and disables the enroll button for a split second.
        time.sleep(1)
    except NoSuchElementException: pass

    udemyEnroll = driver.find_element_by_xpath("//*[@id=\"udemy\"]/div[1]/div[2]/div/div/div/div[2]/form/div[2]/div/div[4]/button") #Udemy
    udemyEnroll.click()

def main_function():

    page = 1  #Change the page number here only if necessary, else ignore

    loop_run_count = 0

    while True:

        print("Please Wait: Getting the course list from tutorialbar.com...")
        print("Page: "+str(page)+", Loop run count: "+str(loop_run_count))

        url="https://www.tutorialbar.com/all-courses/"+"page/"+str(page)+"/"
        courses=getTutorialBarLinks(url)
        
        udemyLinks=[]
        linkCounter=0
        
        for course in courses:
            
            udemyLinks.append(getUdemyLink(course))
            print("Received Link " + str(linkCounter+1) + ": "+udemyLinks[linkCounter])
            linkCounter=linkCounter+1

        if loop_run_count == 0:
            
            udemyLogin(email,password)

        for link in udemyLinks:
            try:
                redeemUdemyCourse(link)
            except BaseException as e:
                print("Unable to enroll for this course either because you have already claimed it or the browser window has been closed!")

        page = page + 1
        loop_run_count = loop_run_count + 1
        
        print("Moving on to the next page of the course list on tutorialbar.com")

main_function()
