# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.3]:
  https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/releases/tag/v0.3
[0.2]:
  https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/releases/tag/v0.2
[0.1]:
  https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/releases/tag/v0.1
