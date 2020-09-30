# Automatic Udemy Course Enroller: GET PAID UDEMY COURSES for FREE
Do you want to LEARN NEW STUFF for FREE? Don't worry, with the power of web-scraping and automation, this script will find the necessary Udemy Coupons &amp; enroll you for PAID UDEMY COURSES, ABSOLUTELY FREE!

The code scrapes course links and coupons from [tutorialbar.com](https://tutorialbar.com)

In case of any bugs or issues, **feel free to ping me on [LinkedIn](https://www.linkedin.com/in/aapatre/) or [Twitter](https://twitter.com/Antariksh_Patre)**

Also, don't forget to **Fork & Star the repository if you like it! ❤**

***Video Proof:***

[![Udemy Auto-Course-Enroller](https://img.youtube.com/vi/IW8CCtv2k2A/0.jpg)](https://www.youtube.com/watch?v=IW8CCtv2k2A "GET PAID UDEMY Courses for FREE, Automatically with this Python Script!")

---

## ***Disclaimer & WARNINGS:***</br>
1. **IMPORTANT:** Make sure you **clear all saved Debit/Credit Card or any other saved payment info from your Browser & your Udemy account** before using the script!</br>
2. **Use** this ONLY for **Educational Purposes!** By using this code you agree that **I'm not responsible for any kind of trouble** caused by the code.</br>
3. **Make sure web-scraping is legal in your region.**</br>
4. This is **NOT a hacking script**, i.e., it can't enroll you for a specific course! Instead it finds courses that provide coupon links to make the transaction free and then LEGALLY enroll you to the course!</br>

---

## Requirements:

### How to Install the Requirements?
Simply run the <a href="">requirements.py</a> in Python's IDLE Editor. If all the requirements are installed, you are good to go but, in case of errors I've listed the individual requirements which can be installed by running the given commands in the terminal or the command prompt. You can even run <em>pip install requirements.txt</em> in the command prompt but if you are a beginner, I urge you to try either of the above mentioned methods. **Or click on the image below to watch a short tutorial:**

[![pip install tutorial](http://i3.ytimg.com/vi/bij66_Jtoqs/maxresdefault.jpg)](https://www.youtube.com/watch?v=bij66_Jtoqs "Tutorial to install Python Modules with pip")

<ul>
  <strong><li>Requests module for Python:</li></strong>
<pre><code>pip install requests</code></pre>

<strong><li>BeautifulSoup Web-Scraping Library for Python:</li></strong>
<pre><code>pip install beautifulsoup4</code></pre>

<strong><li>Selenium Browser Automation Tool for Python:</li></strong>
<pre><code>pip install selenium</code></pre>

<strong><li>Webdriver Manager for Python:</li></strong>
<pre><code>pip install webdriver_manager</code></pre>

<strong><li>Required Python version:</strong> [Python 3.8](https://www.python.org/downloads/release/python-380/)</li>

<strong><li>Webdrivers are now automatically installed! Hurray! But here are some links in case you are using the vanilla script or the Safari Browser:</strong> 
<ul>
  <li>Edge- https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/</li>
  <li>Chrome- https://chromedriver.chromium.org/</li>
  <li>Firefox- https://github.com/mozilla/geckodriver/releases</li>
  <li>Safari- https://webkit.org/blog/6900/webdriver-support-in-safari-10/ .etc</li>
  <li>Opera- https://github.com/operasoftware/operachromiumdriver/releases</li>
  <li>Internet Explorer- <a href='https://www.selenium.dev/downloads/'>Wait, who even uses this anymore!?</a></li>
</ul>

<strong>Note:</strong> Make sure that the driver version matches your browser. <br /> <br />
<strong>Note for Ubuntu/Linux Users:</strong> Run these commands in the terminal before installing the previous requirements: </br>
<pre><code>sudo apt-get update</code></pre>
<pre><code>sudo apt-get upgrade</code></pre>
<pre><code>sudo apt install python3-pip</code></pre></li>
</ul>

---

## Instructions
<ol>
  <li>Make sure to install all the requirements above.</li>
  </br>
  <li>Open <a href="https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/settings.txt">settings.txt</a> file and insert your <strong>Udemy registered email on the first line</strong>, your <strong>Udemy password on the second line</strong>, and the <strong>ZIP Code on the third (only if you stay in the United States or any other region where Udemy asks for ZIP Code as Billing Info, else clear the line and leave it blank)</strong>. Make sure there are no extra spaces or line breaks anywhere! <strong>Please use <a href="https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/settings_example.txt">settings_example.txt</a> as a reference.</strong></li>
  </br>
  <li>Choose the appropriate file for your browser (from the list below) in Python's IDLE Editor: </li>
  <ol>
    <li><strong>Tested and works perfectly: </strong></li>
    <ol>
      <li>Chrome: <a href="https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_chrome.py">udemy_enroller_chrome.py</a></li>
      <li>Chromium: <a href="https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_chromium.py">udemy_enroller_chromium.py</a></li>
      <li>Edge: <a href="https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_edge.py">udemy_enroller_edge.py</a></li>
    </ol>
    <li><strong>Has issues: </strong></li>
    <ol>
      <li>Firefox: <a href="https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_firefox.py">udemy_enroller_firefox.py</a></li>
    </ol>
    <li><strong>Untested: </strong></li>
    <ol>
      <li>Opera: <a href="https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_opera.py">udemy_enroller_opera.py</a></li>
    </ol>
    <li><strong>Experimentation or other Browsers (especially Safari):</strong></li>
    <ol><li>Vanilla (aka the old bot- requires manual driver setup): <a href="https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_vanilla.py">udemy_enroller_vanilla.py</a></li></ol>
    <li><strong>Should never be used by anyone with self-respect and dignity 🙃 (and of course has bugs):</strong></li>
    <ol><li>Internet Explorer: <a href="https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/blob/master/udemy_enroller_internet_explorer.py">udemy_enroller_internet_explorer.py</a></li></ol>
  </ol>
  </br>
  <li>Run the chosen script in Python's IDLE Editor.</li>
  </br>
  <li>The bot starts scraping the course links from the first <strong>All Courses</strong> page on <a href='https://www.tutorialbar.com/all-courses/page/1'>Tutorial Bar</a> and starts enrolling you to Udemy courses. After it has enrolled you to courses from the first page, it then moves to the next Tutorial Bar page and the cycle continues.</br><strong>Optional:</strong> However, you can change the starting page in the <strong><em>page</em></strong> variable inside the <em><strong>main_function()</em></strong>. (Not recommended, except when you are trying to redeem old coupons, which may or may not be valid at this point of time; But sometimes, by a stroke of luck, the coupons may still work!)</li>
  </br>
  <li>Close the browser window, the web-driver and the Python shell to stop the enrollment process.</li>
</ol>

---

## FAQs

### 1. Can I get a specific course for free with this script?
Unfortunately no, but let me assure you that you may be lucky enough to get a particular course for free when the instructor posts it's coupon code in order to promote it. Also, over time you would build a library of courses by running the script often and have all the required courses in your collection. In fact, I made this course after completing a [Python automation course](https://www.udemy.com/course/automate/) and selenium, which of course I got for free! :)

### 2. How the bot works?
The bot retrieves coupon links from Tutorial Bar's list to cut the prices and then uses Selenium's Browser automation features to login and enroll to the courses. Think of it this way: Epic Games & other clients like Steam provide you a handful of games each week, for free; Only in this case, we need a coupon code to make those courses free. 

### 3. How frequently should you run the script?
Daily, at least once! If you are using it for the first time, I recommend that you allow it to scrape through all pages on Tutorial Bar (might take a few hours since there are >500 pages on the site). I've painstakingly amassed over 4000 courses in the last four years! And out of those 4000, I've only paid for 4 of these courses:
<p align="center"><img src="https://i.imgur.com/p79IcDJ.png" width= 50%; height= 50%; /><p>

So, a mere **0.001%** of courses are **actually paid** in my collection! Thankfully, you can get more than what I gathered in 4 years, in a matter of weeks! 🙌🏻

### 4. Why did I create this?
It used to be my daily habit to redeem courses and it was an extremely tedious task that took around 15 minutes, for 10 courses. And then I suddenly got the idea to automate it, after I found the automation course mentioned above. I bet, it will save your precious time too! :)

### 5. "Udemy has detected that I'm using automation tools to browse the website! What should I do?"
<p align="center"><kbd><img src="https://i.imgur.com/pwseilE.jpg" /></kbd></p>
Relax! This happens when you run the script several times in a short interval of time. Solve the captcha, close the browser and the webdriver, and simply re-run the bot. Easy peasy lemon squeezy! 🍋🙃 <br /><br />
<p align="center"><kbd><img src="https://i.imgur.com/yMYtOUK.jpg" /></kbd></p>

### 6. The code compiles successfully but it's taking too long to work! IS there any way to fix that?
Since we are heavily dependent on a third-party site to retrieve coupons links, there may be issues when the site is down. Needless to mention the connectivity issues too. If everything is working fine, you can see the courses being retrieved in the Python console/shell, which may take a while.

### 7. Which is the best way to run the script?
It is highly recommended to run the script using Python's IDLE IDE. <br />
**Pro-tip:** Create a batch file, to launch the script instantly, using these instructions: https://datatofish.com/batch-python-script/

---

