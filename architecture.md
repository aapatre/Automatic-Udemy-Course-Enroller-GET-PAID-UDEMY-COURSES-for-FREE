# Architecture

This document describes the high-level architecture of Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE. Here is all the info you need to make yourself familiar with the codebase.

## Bird's Eye View

![High-Level-Diagram](public/images/High-Level%20Diagram.png)

Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE is a cli tool which takes the user udemy account and use it with scraping tools to find udemy coupons which then get used to enroll the user to paid udemy courses.

## Code Map

This sections talks about directories and data structures.

### udemy_enroller/cli.py

This parse the user flags, logging info and to run the udemy actions as it is or with the browser.

### udemy_enroller/runner.py

This is a Central loop that logs into udemy, runs scrapers and trys enrollment for each of the coupon URL.

### udemy_enroller/setting.py

This collect user info, lang/cate filters and zip code which is saved in a ymal file and cache udemy cookies.

### udemy_enroller/scrapers/\*

This scrapes coupon links from sites like Tutorial Bar, DiscUdemy, Coursevania and FreebiesGlobal.

### udemy_enroller/udemy_rest.py

This use cloudscraper and requests to authenticate, use cached cookies, inspect course, runs statistics and saving estimates.

### udemy_enroller/udemy_ui.py

This runs a browser to solves REST calls fail or when the user uses the cli flags.

### udemy_enroller/driver_manager.py

This downloads and installs web drivers like chrome, edge etc.

## Testing

Pytest with asyncio supports and coverage is under tests/ with fixtures in tests/conftest.py.
