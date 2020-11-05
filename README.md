# Automatic Udemy Course Enroller: GET PAID COURSES for FREE! (Legally!)

Do you want to LEARN NEW STUFF for FREE? Don't worry, with the power of
web-scraping and automation, this script will find the necessary Udemy Coupons
&amp; enroll you for PAID UDEMY COURSES, ABSOLUTELY FREE!

The code scrapes course links and coupons from
[tutorialbar.com](https://tutorialbar.com)

In case of any bugs or issues, **feel free to ping me on
[LinkedIn](https://www.linkedin.com/in/aapatre/) or
[Twitter](https://twitter.com/Antariksh_Patre)**

Also, don't forget to **Fork & Star the repository if you like it!**

**_Video Proof:_**

[![Udemy Auto-Course-Enroller](https://img.youtube.com/vi/IW8CCtv2k2A/0.jpg)](https://www.youtube.com/watch?v=IW8CCtv2k2A "GET PAID UDEMY Courses for FREE, Automatically with this Python Script!")

---

## **_Disclaimer & WARNINGS:_**</br>

1. **IMPORTANT:** Make sure you **clear all saved Debit/Credit Card or any other
   saved payment info from your Browser & your Udemy account** before using the
   script!</br>
2. **Use** this ONLY for **Educational Purposes!** By using this code you agree
   that **I'm not responsible for any kind of trouble** caused by the code.</br>
3. **Make sure web-scraping is legal in your region.**</br>
4. This is **NOT a hacking script**, i.e., it can't enroll you for a specific
   course! Instead it finds courses that provide coupon links to make the
   transaction free and then LEGALLY enroll you to the course!</br>

---

## Requirements:

### How to Install the Requirements?

<strong>Required Python version:</strong>
[Python 3.8+](https://www.python.org/downloads/)

**You must have pip installed. Please look up how to install pip in your OS.**

Download a release of this project or clone the repository then navigate to the
folder where you placed the files on. Type `pip install -r requirements.txt` to
get all the requirements installed in one go. If you need to install individual
dependencies you can do so by inputting the commands below in your terminal.

<ul>
  <strong><li>Requests module for Python:</li></strong>
<pre><code>pip install requests</code></pre>

<strong><li>ruamel.yaml for Python:</li></strong>

<pre><code>pip install ruamel.yaml</code></pre>

<strong><li>BeautifulSoup Web-Scraping Library for Python:</li></strong>

<pre><code>pip install beautifulsoup4</code></pre>

<strong><li>Selenium Browser Automation Tool for Python:</li></strong>

<pre><code>pip install selenium</code></pre>

<strong><li>Webdriver Manager for Python:</li></strong>

<pre><code>pip install webdriver_manager</code></pre>

<strong><li>Webdrivers are now automatically installed! But here are some links
in case you are using the vanilla script or the Safari Browser:</strong>

<ul>
  <li>Edge- https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/</li>
  <li>Chrome- https://chromedriver.chromium.org/</li>
  <li>Firefox- https://github.com/mozilla/geckodriver/releases</li>
  <li>Safari- https://developer.apple.com/documentation/webkit/about_webdriver_for_safari/</li>
  <li>Opera- https://github.com/operasoftware/operachromiumdriver/releases</li>
  <li>Internet Explorer- <a href='https://www.selenium.dev/downloads/'>Find it on your own accord</a></li>
</ul>

<strong>Note:</strong> Make sure that the driver version matches your browser.

</ul>

---

## Instructions

<ol>
  <li>Make sure to install all the requirements above.</li>
  </br>
  <ol>
  <li>Run the script and the cli will guide you through the settings required</li>
  <li>Otherwise you can rename the following file <a href="sample_settings.yaml">sample_settings.yaml</a> to <strong>settings.py</strong> and edit it using a text editor and insert your <strong>Udemy registered email in the email section</strong>, your <strong>Udemy password in the password section</strong>, and the <strong>ZIP Code in the zipcode section (if you reside in the United States or any other region where Udemy asks for ZIP Code as Billing Info, else enter a random number)</strong>.</li>
  </ol>
  </br>
  <li>Choose the appropriate file for your browser (from the list below): </li>
  <ol>
    <li><strong>Tested and works perfectly: </strong></li>
    <ol>
      <li>Chrome: <a href="https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_chrome.py">udemy_enroller_chrome.py</a></li>
      <li>Chromium: <a href="https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_chromium.py">udemy_enroller_chromium.py</a></li>
      <li>Edge: <a href="https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_edge.py">udemy_enroller_edge.py</a></li>
    </ol>
    <li><strong>Has issues: </strong></li>
    <ol>
      <li>Firefox: <a href="https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_firefox.py">udemy_enroller_firefox.py</a></li> (requires manual driver installation)
    </ol>
    <li><strong>Untested: </strong></li>
    <ol>
      <li>Opera: <a href="https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_opera.py">udemy_enroller_opera.py</a></li>
    </ol>
    <li><strong>Experimentation or other Browsers (especially Safari):</strong></li>
    <ol><li>Vanilla (aka the old bot- requires manual driver setup): <a href="https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_vanilla.py">udemy_enroller_vanilla.py</a></li></ol>
    <li><strong>User at your own risk:</strong></li>
    <ol><li>Internet Explorer: <a href="https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_internet_explorer.py">udemy_enroller_internet_explorer.py</a></li></ol>
  </ol>
  </br>
  <li>Run the chosen script in terminal like so:  <code>python udemy_enroller_firefox.py</code>
</li>
  </br>
  <li>The bot starts scraping the course links from the first <strong>All Courses</strong> page on <a href='https://www.tutorialbar.com/all-courses/page/1'>Tutorial Bar</a> and starts enrolling you to Udemy courses. After it has enrolled you to courses from the first page, it then moves to the next Tutorial Bar page and the cycle continues.
  </br>
  <li>Stop the script by pressing ctrl+c in terminal to stop the enrollment process.</li>
</ol>

---

## FAQs

### 1. Can I get a specific course for free with this script?

Unfortunately no, but let me assure you that you may be lucky enough to get a
particular course for free when the instructor posts it's coupon code in order
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

Daily, at least once! If you are using it for the first time, I recommend that
you allow it to scrape through all pages on Tutorial Bar (might take a few hours
since there are >500 pages on the site). I've painstakingly amassed over 4000
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

### 5. "Udemy has detected that I'm using automation tools to browse the website! What should I do?"

<p align="center"><kbd><img src="https://i.imgur.com/pwseilE.jpg" /></kbd></p>
Relax! This happens when you run the script several times in a short interval of time. Solve the captcha, close the browser, and simply re-run the script. Easy peasy lemon squeezy! 🍋🙃 <br /><br />

### 6. The code compiles successfully but it's taking too long to work! IS there any way to fix that?

Since we are heavily dependent on a third-party site to retrieve coupons links,
there may be issues when the site is down. Needless to mention the connectivity
issues too. If everything is working fine, you can see the courses being
retrieved in the Python console/shell, which may take a while.

### 7. Which is the best way to run the script?

It is recommended to run the script using Python's IDLE IDE. <br /> **Pro-tip:**
Create a batch file, to launch the script instantly, using these instructions:
https://datatofish.com/batch-python-script/

### 8. Which branch to commit against?

Pull request should be made on "develop" branch.

### 9. What's the roadmap?

Take a look at our
[Roadmap here](https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/projects/1)
and help us on what you want or talk to us about your proposed changes.

---
