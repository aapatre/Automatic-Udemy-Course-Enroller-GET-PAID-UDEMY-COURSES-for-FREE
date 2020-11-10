# Install all the requirements by running requirements.py in IDLE or follow the alternate instructions at
# https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/ Make sure you have
# cleared all saved payment details on your Udemy account & the browser!
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

from core import Settings
from core.utils import redeem_courses

settings = Settings()

driver = webdriver.Chrome(
    ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
)

# Maximizes the browser window since Udemy has a responsive design and the code only works
driver.maximize_window()
# in the maximized layout

try:
    redeem_courses(driver, settings)
except KeyboardInterrupt:
    print("Exiting the script")
except Exception as e:
    print("Error: {}".format(e))
finally:
    print("Closing browser")
    driver.quit()
