[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/it-works-why.svg)](https://forthebadge.com)


# Udemy Coupon Grabber & Course Enroller: Grab FREE Coupons!

Do you want to LEARN NEW STUFF for FREE? Don't worry, with the power of
web-scraping and automation, this script will find the necessary Udemy Coupons
&amp; enroll you to PAID UDEMY COURSES, ABSOLUTELY FREE!

**NOTE: THIS PROJECT IS NOT AFFILIATED WITH UDEMY.**

The code scrapes course links and coupons from
[tutorialbar.com](https://tutorialbar.com)

In case of any bugs or issues, please open an issue in github.

Also, don't forget to **Fork & Star the repository if you like it!**

**_Video Proof:_**

[![Udemy Auto-Course-Enroller](https://img.youtube.com/vi/IW8CCtv2k2A/0.jpg)](https://www.youtube.com/watch?v=IW8CCtv2k2A "GET PAID UDEMY Courses for FREE, Automatically with this Python Script!")

---

## **_Disclaimer & WARNINGS:_**


1. **Use** this ONLY for **Educational Purposes!** By using this code you agree
   that **I'm not responsible for any kind of trouble** caused by the code. **THIS PROJECT IS NOT AFFILIATED WITH UDEMY.** 
2. **Make sure web-scraping is legal in your region.**
3. This is **NOT a hacking script**, i.e., it can't enroll you for a specific
   course! Instead it finds courses that provide coupon links to make the
   transaction free and then LEGALLY enroll you to the course!

---

## Requirements:

### How to Install the Requirements?

**Required Python version:** [Python 3.8+](https://www.python.org/downloads/)

**You must have pip or poetry installed. Please look up how to install them in your OS.**

Download a release of this project or clone the repository then navigate to the
folder where you placed the files on. Type `pip install -r requirements.txt` to
get all the requirements installed in one go. Similar instructions applies for poetry.

- **Webdrivers are now automatically installed! But here are some links in case
  you are using the vanilla script or the Safari Browser:**

* Edge- https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
* Chrome- https://chromedriver.chromium.org/
* Firefox- https://github.com/mozilla/geckodriver/releases/
* Safari-
  https://developer.apple.com/documentation/webkit/about_webdriver_for_safari/
* Opera- https://github.com/operasoftware/operachromiumdriver/releases
* Internet Explorer-
  [Find it on your own accord](https://www.selenium.dev/downloads/)

**Note:** Make sure that the driver version matches your browser.

---

## Instructions

Props to Davidd Sargent for making a super simple video tutorial. If you prefer written instructions then continue reading further, else click on the image below for a quick video tutorial:

[![GET Udemy Courses for FREE with Python | 2 Minute Tuesday](https://i.ytimg.com/vi/tdLsVoraMxw/hq720.jpg)](https://www.youtube.com/watch?v=tdLsVoraMxw "GET Udemy Courses for FREE with Python | 2 Minute Tuesday")

1 . Make sure to install all the requirements above.

- Run the script and the cli will guide you through the settings required
- Otherwise you can rename the following file
  [sample_settings.yaml](sample_settings.yaml) to **settings.yaml** and edit it
  using a text editor and insert your **Udemy registered email in the email
  section**, your **Udemy password in the password section**, and the **ZIP Code
  in the zipcode section (if you reside in the United States or any other region
  where Udemy asks for ZIP Code as Billing Info, else enter a random number)**
  Additionally you can add your preferred languages and course categories.

2 . Choose the appropriate file for your browser (from the list below):

- **Tested and works perfectly:**

  - Chrome:
    [udemy_enroller_chrome.py](https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_chrome.py)
  - Chromium:
    [udemy_enroller_chromium.py](https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_chromium.py)
  - Edge:
    [udemy_enroller_edge.py](https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_edge.py)

- **Has issues when run on custom kernel but works fine on vanilla OS:**

  - Firefox:
    [udemy_enroller_firefox.py(might require manual driver installation)](https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_firefox.py)

- **Untested:**

  - Opera:
    [udemy_enroller_opera.py](https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_opera.py)

- **Experimentation or other Browsers (especially Safari):**

  - [aka the old bot- requires manual driver setup](https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_vanilla.py)

- **Use at your own risk:**
  - Vanilla
  - Internet Explorer:
    [udemy_enroller_internet_explorer.py](https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_internet_explorer.py)

3 . The script can be passed arguments:
- `--help`: View full list of arguments available
- `--max-pages=<NUMBER>`: Max number of pages to scrape from tutorialbar.com before exiting the script
- `--browser=<BROWSER_NAME>`: Run with a specific browser 
- `--cache-hits=<NUMBER>`: If we hit the cache this number of times in a row we will exit the script

4 . Run the chosen script in terminal like so:
- `python udemy_enroller_firefox.py`

   Or by using the generic script:
- `python udemy_enroller.py --browser=firefox`

5 . The bot starts scraping the course links from the first **All Courses** page
on [Tutorial Bar](https://www.tutorialbar.com/all-courses/page/1) and starts
enrolling you to Udemy courses. After it has enrolled you to courses from the
first page, it then moves to the next Tutorial Bar page and the cycle continues.

- Stop the script by pressing ctrl+c in terminal to stop the enrollment process.

---

## FAQs

### 1. Can I get a specific course for free with this script?

Unfortunately no, but let me assure you that you may be lucky enough to get a
particular course for free when the instructor posts its coupon code in order
to promote it. Also, over time you would build a library of courses by running
the script often and have all the required courses in your collection. In fact,
I made this course after completing a
[Python automation course](https://www.udemy.com/course/automate/) and selenium,
which of course I got for free! :)

### 2. How does the bot work?

The bot retrieves coupon links from Tutorial Bar's list to cut the prices and
then uses Selenium's Browser automation features to login and enroll to the
courses. Think of it this way: Epic Games & other clients like Steam provide you
a handful of games each week, for free; Only in this case, we need a coupon code
to make those courses free.

### 3. How frequently should you run the script?

Daily, at least once! I've painstakingly amassed over 4000
courses in the last four years! And out of those 4000, I've only paid for 4 of
these courses.

So, a mere **0.001%** of courses are **actually paid** in my collection!
Thankfully, you can get more than what I gathered in 4 years, in a matter of
weeks! 🙌🏻

### 4. Why did I create this?

It used to be my daily habit to redeem courses and it was an extremely tedious
task that took around 15 minutes, for 10 courses. And then I suddenly got the
idea to automate it, after I found the automation course mentioned above. I bet,
it will save your precious time too! :)

### 5. Udemy has detected that I'm using automation tools to browse the website! What should I do?

![](https://i.imgur.com/pwseilE.jpg) Relax! This happens when you run the script
several times in a short interval of time. Solve the captcha, hit enter in the terminal window you are running 
the script from and allow the script to continue as normal.
Easy peasy lemon squeezy! 🍋🙃 

### 6. The code compiles successfully but it's taking too long to work! IS there any way to fix that?

Since we are heavily dependent on a third-party site to retrieve coupons links,
there may be issues when the site is down. Needless to mention the connectivity
issues too. If everything is working fine, you can see the courses being
retrieved in the Python console/shell, which may take a while.

### 7. Which is the best way to run the script?

It is recommended to run the script using your terminal and system python.


### 8. Which branch to commit against?

Pull request should be made on "develop" branch.

### 9. What's the roadmap?

Take a look at our
[Roadmap here](https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/projects/1)
and help us on what you want or talk to us about your proposed changes.

---

## Supporters

### Jetbrains

[![JetBrains](https://i.imgur.com/h2R018M.jpg)](https://jetbrains.com/?from=udemy-free-course-enroller)

Thanks to [JetBrains](https://jetbrains.com/?from=udemy-free-course-enroller) for supporting us. They are the maker of world class IDE and developer tooling. If you think their product might help you, please support them. 

### GitBook

[![Gitbook](https://i.imgur.com/OkuB14I.jpg)](https://gitbook.com)

Thanks to [Gitbook](https://gitbook.com) for supporting us. Gitbook is the best place to track personal notes and ideas for teams. If you think their product might help you, please support them.
