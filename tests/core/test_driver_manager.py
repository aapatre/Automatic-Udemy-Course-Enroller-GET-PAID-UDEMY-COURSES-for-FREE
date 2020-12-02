from unittest import mock

import pytest

from core import DriverManager
from core.driver_manager import (
    ALL_VALID_BROWSER_STRINGS,
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
@mock.patch("core.driver_manager.webdriver")
@mock.patch("core.driver_manager.ChromeDriverManager")
@mock.patch("core.driver_manager.GeckoDriverManager")
@mock.patch("core.driver_manager.EdgeChromiumDriverManager")
@mock.patch("core.driver_manager.IEDriverManager")
@mock.patch("core.driver_manager.OperaDriverManager")
@mock.patch("core.driver_manager.ChromeType")
def test_driver_manager_init(
    _,
    mock_opera_driver_manager,
    mock_internet_explorer_driver_manager,
    mock_edge_driver_manager,
    mock_firefox_driver_manager,
    mock_chrome_driver_manager,
    mock_selenium_web_driver,
    browser_name,
):
    try:
        dm = DriverManager(browser_name)
    except ValueError:
        assert browser_name not in ALL_VALID_BROWSER_STRINGS
    else:
        if browser_name in ("chrome",):
            mock_selenium_web_driver.Chrome.assert_called_once_with(
                mock_chrome_driver_manager().install(), options=None
            )
            assert dm.driver == mock_selenium_web_driver.Chrome()
        elif browser_name in ("chromium",):
            mock_selenium_web_driver.Chrome.assert_called_once_with(
                mock_chrome_driver_manager().install()
            )
            assert dm.driver == mock_selenium_web_driver.Chrome()
        elif browser_name in VALID_FIREFOX_STRINGS:
            mock_selenium_web_driver.Firefox.assert_called_once_with(
                executable_path=mock_firefox_driver_manager().install()
            )
            assert dm.driver == mock_selenium_web_driver.Firefox()
        elif browser_name in VALID_OPERA_STRINGS:
            mock_selenium_web_driver.Opera.assert_called_once_with(
                executable_path=mock_opera_driver_manager().install()
            )
            assert dm.driver == mock_selenium_web_driver.Opera()
        elif browser_name in VALID_EDGE_STRINGS:
            mock_selenium_web_driver.Edge.assert_called_once_with(
                mock_edge_driver_manager().install()
            )
            assert dm.driver == mock_selenium_web_driver.Edge()
        elif browser_name in VALID_INTERNET_EXPLORER_STRINGS:
            mock_selenium_web_driver.Ie.assert_called_once_with(
                mock_internet_explorer_driver_manager().install()
            )
            assert dm.driver == mock_selenium_web_driver.Ie()


@pytest.mark.parametrize(
    "browser_name,is_ci_build",
    [
        ("chrome", True),
        ("chrome", False),
    ],
    ids=("chrome is ci build", "chrome is not ci build"),
)
@mock.patch("core.driver_manager.webdriver")
@mock.patch("core.driver_manager.ChromeOptions")
@mock.patch("core.driver_manager.ChromeDriverManager")
@mock.patch("core.driver_manager.ChromeType")
def test_driver_manager_ci_build(
    _,
    mock_chrome_driver_manager,
    mock_chrome_options,
    mock_selenium_web_driver,
    browser_name,
    is_ci_build,
):

    dm = DriverManager(browser_name, is_ci_build=is_ci_build)

    if is_ci_build:
        options = mock_chrome_options()
    else:
        options = None
    mock_selenium_web_driver.Chrome.assert_called_once_with(
        mock_chrome_driver_manager().install(), options=options
    )
    assert dm.driver == mock_selenium_web_driver.Chrome()
