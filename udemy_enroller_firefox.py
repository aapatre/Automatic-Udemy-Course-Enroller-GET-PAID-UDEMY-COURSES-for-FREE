# Install all the requirements by running requirements.py in IDLE or follow the alternate instructions at
# https://github.com/aapatre/Automatic-Udemy-Course-Enroller-GET-PAID-UDEMY-COURSES-for-FREE/ Make sure you have
# cleared all saved payment details on your Udemy account & the browser! For firefox you need to manually install the
# driver on Arch Linux (sudo pacman -S geckodriver). Untested on other platforms.
import warnings

from udemy_enroller import parse_args, run

if __name__ == "__main__":
    browser = "firefox"
    warnings.warn(
        f"Please use `udemy_enroller.py --browser={browser}` as this script will be removed soon",
        DeprecationWarning,
    )
    args = parse_args(browser)
    run(args.browser, args.max_pages, args.cache_hits)
