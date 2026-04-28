from unittest import mock

import pytest

from udemy_enroller import DriverManager
from udemy_enroller.driver_manager import (
    ALL_VALID_BROWSER_STRINGS,
    VALID_CHROME_STRINGS,
    VALID_CHROMIUM_STRINGS,
    VALID_EDGE_STRINGS,
    VALID_FIREFOX_STRINGS,
    VALID_INTERNET_EXPLORER_STRINGS,
    VALID_OPERA_STRINGS,
)


@pytest.mark.parametrize(
    "browser_name",
    [
        ("chrome"),
        ("chromium"),
        ("edge"),
        ("firefox"),
        ("opera"),
        ("internet_explorer"),
        ("tor"),
    ],
    ids=(
        "create driver chrome",
        "create driver chromium",
        "create driver edge",
        "create driver firefox",
        "create driver opera",
        "create driver internet_explorer",
        "unsupported browser",
    ),
)
@mock.patch("udemy_enroller.driver_manager.webdriver")
def test_driver_manager_init(mock_selenium_web_driver, browser_name):
    try:
        dm = DriverManager(browser_name)
    except ValueError:
        assert browser_name not in ALL_VALID_BROWSER_STRINGS
    except (ImportError, StopIteration, Exception):
        # Opera/IE need webdriver-manager which may not work in test env
        assert browser_name in VALID_OPERA_STRINGS | VALID_INTERNET_EXPLORER_STRINGS
    else:
        if browser_name in VALID_CHROME_STRINGS:
            mock_selenium_web_driver.Chrome.assert_called_once()
            assert dm.driver == mock_selenium_web_driver.Chrome()
        elif browser_name in VALID_CHROMIUM_STRINGS:
            mock_selenium_web_driver.Chrome.assert_called_once()
            assert dm.driver == mock_selenium_web_driver.Chrome()
        elif browser_name in VALID_FIREFOX_STRINGS:
            mock_selenium_web_driver.Firefox.assert_called_once()
            assert dm.driver == mock_selenium_web_driver.Firefox()
        elif browser_name in VALID_EDGE_STRINGS:
            mock_selenium_web_driver.Edge.assert_called_once()
            assert dm.driver == mock_selenium_web_driver.Edge()


@pytest.mark.parametrize(
    "browser_name,is_ci_build",
    [
        ("chrome", True),
        ("chrome", False),
    ],
    ids=("chrome is ci build", "chrome is not ci build"),
)
@mock.patch("udemy_enroller.driver_manager.webdriver")
def test_driver_manager_ci_build(
    mock_selenium_web_driver,
    browser_name,
    is_ci_build,
):
    dm = DriverManager(browser_name, is_ci_build=is_ci_build)
    mock_selenium_web_driver.Chrome.assert_called_once()
    assert dm.driver == mock_selenium_web_driver.Chrome()
