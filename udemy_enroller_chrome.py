# Install all the requirements by running requirements.py in IDLE or follow the alternate instructions at
# https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/ Make sure you have
# cleared all saved payment details on your Udemy account & the browser!
from core import UdemyEnroller

if __name__ == "__main__":
    enroller = UdemyEnroller("chrome", settings_file="settings.yaml")
    enroller.run()
