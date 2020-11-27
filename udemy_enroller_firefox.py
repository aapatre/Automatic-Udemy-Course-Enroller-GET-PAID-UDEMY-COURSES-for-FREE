# Install all the requirements by running requirements.py in IDLE or follow the alternate instructions at
# https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/ Make sure you have
# cleared all saved payment details on your Udemy account & the browser! For firefox you need to manually install the
# driver on Arch Linux (sudo pacman -S geckodriver). Untested on other platforms.
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

from core import Settings
from core.utils import redeem_courses

settings = Settings()

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

# Maximizes the browser window since Udemy has a responsive design and the
# code only works in the maximized layout
driver.maximize_window()

redeem_courses(driver, settings)
