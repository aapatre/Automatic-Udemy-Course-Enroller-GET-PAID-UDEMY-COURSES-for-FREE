[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/it-works-why.svg)](https://forthebadge.com)

- Udemy Coupon Grabber & Course Enroller: Grab FREE Coupons!
  <br/>

Do you want to LEARN NEW STUFF for FREE? Don't worry, with the power of
web-scraping and automation, this script will find the necessary Udemy Coupons
&amp; enroll you to PAID UDEMY COURSES, ABSOLUTELY FREE!

**NOTE: THIS PROJECT IS NOT AFFILIATED WITH UDEMY.**

**NOTE: THIS PROJECT WILL NOT WORK WITH NON ENGLISH UDEMY.**

<br/>

The code scrapes course links and coupons from:

- [tutorialbar.com](https://tutorialbar.com)
- [discudemy.com](https://discudemy.com)
- [coursevania.com](https://coursevania.com)
- [freebiesglobal.com](https://freebiesglobal.com)
- [idownloadcoupon.com](https://idownloadcoupon.com) -> _New_

In case of any bugs or issues, please open an issue in github. Also, don't forget to **Fork & Star the repository if you like it!**

**We are also on _[GitLab](https://gitlab.com/the-automators/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE)_**
<br/><br/>

## Disclaimer & WARNINGS:

&emsp; 1. Use this ONLY for **Educational Purposes!** By using this code you agree that
**I'm not responsible for any kind of trouble** caused by the code. **THIS PROJECT IS NOT AFFILIATED WITH UDEMY.**
<br/>
&emsp; 2. **Make sure web-scraping is legal in your region.**
<br/>
&emsp; 3. This is **NOT a hacking script**, i.e., it can't enroll you for a specific
course! Instead it finds courses that provide coupon links to make the
transaction free and then LEGALLY enroll you to the course!

## Requirements:

### How to Install the Requirements?

&emsp; **Required Python version:** [Python 3.8+](https://www.python.org/downloads/)

&emsp; **(Windows users only) Required Microsoft Visual C++ 14.0+ version:** [Microsoft Visual C++ 14.0+](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

&emsp; **You must have pip or poetry installed. Please look up how to install them in your OS.**

Download a release of this project or clone the repository then navigate to the
folder where you placed the files on. Type `pip install -r requirements.txt` to
get all the requirements installed in one go. Similar instructions applies for poetry.

## Instructions

1 . Install from PyPI `pip install udemy-enroller`

- Run the script and the cli will guide you through the settings required.
- If you decide to save the settings they will be stored in your home directory: <br>
  **Windows**:
  C:/Users/CurrentUserName/.udemy_enroller<br>
  **Linux**:
  /home/username/.udemy_enroller
  **The values in settings.yaml should be in the same language as the site you are browsing on.**

<br/>

2 . The script can be passed arguments:

- `--help`: View full list of arguments available
- `--browser=<BROWSER_NAME>`: Run with a specific browser
- `--discudemy`: Run the discudemy scraper only
- `--coursevania`: Run the coursevania scraper only
- `--tutorialbar`: Run the tutorialbar scraper only
- `--freebiesglobal`: Run the freebiesglobal scraper only
- `--idownloadcoupon`: Run the idownloadcoupon scraper only
- `--max-pages=<NUMBER>`: Max number of pages to scrape from sites before exiting the script (default is 5)
- `--delete-settings`: Delete existing settings file
- `--delete-cookie`: Delete the cookie file if it exists
- `--debug`: Enable debug logging

<br/>

3 . Run the script in terminal with your target runner:

- `udemy_enroller`
- `udemy_enroller --browser=chrome`
- `udemy_enroller --browser=chromium`

<br/>

4 . The bot starts scraping the course links from the first **All Courses** page
on [Tutorial Bar](https://www.tutorialbar.com/all-courses/page/1), [DiscUdemy](https://www.discudemy.com/all), [Coursevania](https://coursevania.com) and [FreebiesGlobal](https://freebiesglobal.com) and starts
enrolling you to Udemy courses. After it has enrolled you to courses from the
first page, it then moves to the next site page and the cycle continues.

- Stop the script by pressing `ctrl+c` in terminal to stop the enrollment process.

<br/>

5 . _[New]_ At the end of process a detailed result is shown:

```
================== Run Statistics ==================

Enrolled:                   56
Unwanted Category:          0
Unwanted Language:          1
Already Claimed:            93
Expired:                    7
Total Enrolments:           1705
Savings:                    €2674.44
================== Run Statistics ==================
```

### Docker

Alternatively you can run the script in docker.

To build the image run:

```
docker build -t udemy_enroller .
```

After the build is finished you can run your container with one of the commands below (you can pass arguments as you would in the cli):

```
docker run -it udemy_enroller
```

After you entered your login credentials and settings detach from the interactive mode by pressing the `Ctrl-P` followed by `Ctrl-Q`.

You can also create a `settings.yaml` file from the `sample_settings.yaml` and mount to the container with the command:

```
docker run -v $(pwd)/settings.yaml:/home/enroller/.udemy_enroller/settings.yaml udemy_enroller
```

## FAQs

**1. Can I get a specific course for free with this script?**

&emsp; Unfortunately no, but let me assure you that you may be lucky enough to get a
particular course for free when the instructor posts its coupon code in order
to promote it. Also, over time you would build a library of courses by running
the script often and have all the required courses in your collection. In fact,
I made this course after completing a
[Python automation course](https://www.udemy.com/course/automate/) and [Selenium](https://www.selenium.dev/),
which of course I got for free! :)
<br/><br/>

**2. How does the bot work?**

&emsp; The bot retrieves coupon links from [Tutorial Bar](https://www.tutorialbar.com/all-courses/page/1), [DiscUdemy](https://www.discudemy.com/all) and [Coursevania](https://coursevania.com)'s lists to cut the prices and
then uses REST requests to authenticate and enroll to the
courses. Think of it this way: Epic Games & other clients like Steam provide you
a handful of games each week, for free; Only in this case, we need a coupon code
to make those courses free. <br/><br/>

**3. How frequently should you run the script?**

&emsp; Daily, at least once! I've painstakingly amassed over 4000
courses in the last four years! And out of those 4000, I've only paid for 4 of
these courses.

So, a mere **0.001%** of courses are **actually paid** in my collection!
Thankfully, you can get more than what I gathered in 4 years, in a matter of
weeks! 🙌🏻 <br/><br/>

**4. Why did I create this?**

&emsp; It used to be my daily habit to redeem courses and it was an extremely tedious
task that took around 15 minutes, for 10 courses. And then I suddenly got the
idea to automate it, after I found the automation course mentioned above. I bet,
it will save your precious time too! :) <br/><br/>

**5. The code compiles successfully, but it's taking too long to work! IS there any way to fix that?**

&emsp; Since we are heavily dependent on a third-party site to retrieve coupons links,
there may be issues when the site is down. Needless to mention the connectivity
issues too. If everything is working fine, you can see the courses being
retrieved in the Python console/shell, which may take a while. <br/></br>

**6. Which is the best way to run the script?**

&emsp; It is recommended to run the script using your terminal and system python. <br/><br/>

**7. Which branch to commit against?**

&emsp; Pull request should be made on "_develop_" branch. <br/><br/>

**8. What's the roadmap?**

&emsp; Take a look at our [Roadmap here](https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/projects/1) and help us on what you want or talk to us about your proposed changes. <br/><br/>

## Support & Maintenance Notice

By using this repo/script, you agree that the authors and contributors are under no obligation to provide support for the script and can discontinue it's development, as and when necessary, without prior notice.

## Supporters

### Jetbrains

[![JetBrains](https://i.imgur.com/h2R018M.jpg)](https://jetbrains.com/?from=udemy-free-course-enroller)

Thanks to [JetBrains](https://jetbrains.com/?from=udemy-free-course-enroller) for supporting us. They are the maker of world class IDE and developer tooling. If you think their product might help you, please support them.

### GitBook

[![GitBook](https://i.imgur.com/OkuB14I.jpg)](https://gitbook.com)

Thanks to [GitBook](https://gitbook.com) for supporting us. GitBook is the best place to track personal notes and ideas for teams. If you think their product might help you, please support them.

### GitLab

[![GitLab](https://i.imgur.com/aUWtSn4.png)](https://gitlab.com)

Thanks to [GitLab](https://gitlab.com) for supporting us. GitLab is one of the main code hosting and CI/CD providers out there. They support the open source community through their GitLab for [Open Source program](https://about.gitlab.com/solutions/open-source/). Please check them out.
