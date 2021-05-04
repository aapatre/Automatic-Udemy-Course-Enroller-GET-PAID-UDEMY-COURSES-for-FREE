# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1.0] - 2021-05-04

### Added

- Fixing issues with enrollment and scraping
- Updated to allow conditional saving of email/password in settings

## [3.0.0] - 2021-03-03

### Added

- Enrollment now relies on REST requests
- New coupon source from coursevania

### Removed
- No longer supporting browser enrolment (Bot captcha was unsolvable)

## [2.0.0] - 2021-01-19

### Added

- New coupon source from discudemy.com
- Refactored to have generic scrapers and manager
- Improved performance (asyncio)
- Packaged and published to PyPI
- Added cli args --debug, --tutorialbar, --discudemy
- Removed unpopular cli arg -> --cache-hits
- Write settings/cache to home folder so we can persist settings between versions (installed from PyPI)

## [1.0.0] - 2020-12-09

### Added

- Fix for state selection for India
- Added deprecation warning to individual browser endpoint to move to uniform endpoint in preparation for a release in PyPi
- Moved from print to logging for better debug
- Added arguments to script runtime to select max pages and max retry before timeout (default 12)
- Fixed Firefox webdriver autoinstall
- Stop trying to enroll in courses that has any price tag attached to them
- Added unittests
- General performance improvement

## [0.3] - 2020-11-26

### Added

- Add configuration to choose the categories you would like your free courses to be under
- Better handling of enrolled courses, invalid coupons, unwanted categories and unwanted languages
- Basic caching of courses which we have previously tried to enroll in. Improves speed of subsequent runs
- Give control back to user when we have a robot check on udemy login. Once solved the user can hit enter and the script 
can continue as normal

## [0.2] - 2020-11-05

### Added

- Generate settings.yaml on first execution of script through cli prompts
- Add configuration to choose the languages you would like your free courses to
  be in
- Started adding CI integrations

### Changed

- Close browser on script finish or user hitting ctrl-c
- Extracted core logic for tutorialbar and udemy to reduce duplication

## [0.1] - 2020-10-09

### Added

- This is our first pre release, marked as such because Firefox geckodriver
  auto-installation is not working properly yet. You can use the download the
  zip, extract, install the requirement and get a working version of this
  project running locally. Suitable for users who are not looking forward to
  contribute.
  
[3.1.0]:
  https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/releases/tag/v3.1.0
[3.0.0]:
  https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/releases/tag/v3.0.0
[2.0.0]:
  https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/releases/tag/v2.0.0
[1.0.0]:
  https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/releases/tag/v1.0.0
[0.3]:
  https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/releases/tag/v0.3
[0.2]:
  https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/releases/tag/v0.2
[0.1]:
  https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/releases/tag/v0.1
