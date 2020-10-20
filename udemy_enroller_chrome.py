# Install all the requirements by running requirements.py in IDLE or follow the alternate instructions at
# https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/ Make sure you have
# cleared all saved payment details on your Udemy account & the browser!
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from core import Settings
from core.utils import redeem_courses

settings = Settings()

chrome_options = None
if settings.is_ci_build:
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

try:
    redeem_courses(driver, settings)
    if settings.is_ci_build:
        print("We have attempted to subscribe to 1 udemy course")
        print("Ending test")
except KeyboardInterrupt:
    print("Exiting the script")
except Exception as e:
    print("Error: {}".format(e))
finally:
    print("Closing browser")
    driver.quit()
