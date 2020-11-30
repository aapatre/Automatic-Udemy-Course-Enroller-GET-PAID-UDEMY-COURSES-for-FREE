# Install all the requirements by running requirements.py in IDLE or follow the alternate instructions at
# https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/ Make sure you have
# cleared all saved payment details on your Udemy account & the browser!
from selenium import webdriver

from core import Settings
from core.utils import redeem_courses

settings = Settings()
"""### **Enter the path/location of your webdriver**
By default, the webdriver for Microsoft Edge browser has been chosen in the code below.

Also, enter the location of your webdriver.
"""

# On windows you need the r (raw string) in front of the string to deal with backslashes.
# Replace this string with the path for your webdriver
path = r"..location\msedgedriver.exe"
driver = webdriver.Edge(
    path
)
# driver = webdriver.Chrome(path)  # Uncomment for Google Chrome driver
# driver = webdriver.Firefox(path)  # Uncomment for Mozilla Firefox driver
# driver = webdriver.Edge(path)  # Uncomment for Microsoft Edge driver
# driver = webdriver.Safari(path)  # Uncomment for Apple Safari driver

# Maximizes the browser window since Udemy has a responsive design and the code only works
# in the maximized layout
driver.maximize_window()

redeem_courses(driver, settings, max_pages=None)
