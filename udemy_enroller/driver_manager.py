"""Webdriver manager."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from udemy_enroller.logger import get_logger

logger = get_logger()

VALID_FIREFOX_STRINGS = {"ff", "firefox"}
VALID_CHROME_STRINGS = {"chrome", "google-chrome"}
VALID_CHROMIUM_STRINGS = {"chromium"}
VALID_INTERNET_EXPLORER_STRINGS = {"internet_explorer", "ie"}
VALID_OPERA_STRINGS = {"opera"}
VALID_EDGE_STRINGS = {"edge"}

ALL_VALID_BROWSER_STRINGS = (
    VALID_CHROME_STRINGS
    | VALID_CHROMIUM_STRINGS
    | VALID_FIREFOX_STRINGS
    | VALID_EDGE_STRINGS
    | VALID_OPERA_STRINGS
    | VALID_INTERNET_EXPLORER_STRINGS
)


class DriverManager:
    """Webdriver manager using Selenium 4.6+ built-in Selenium Manager."""

    def __init__(self, browser: str, is_ci_build: bool = False):
        """Initialize."""
        self.driver = None
        self.options = None
        self.browser = browser
        self.is_ci_build = is_ci_build
        self._init_driver()

    def _init_driver(self) -> None:
        """
        Initialize the correct web driver based on the users requested browser.

        Selenium 4.6+ includes Selenium Manager which automatically downloads
        and manages browser drivers for Chrome, Firefox, and Edge.

        :return: None
        """
        browser_lower = self.browser.lower()

        if browser_lower in VALID_CHROME_STRINGS:
            if self.is_ci_build:
                self.options = self._build_ci_options_chrome()
            self.driver = webdriver.Chrome(options=self.options)

        elif browser_lower in VALID_CHROMIUM_STRINGS:
            options = ChromeOptions()
            options.binary_location = "/usr/bin/chromium-browser"
            self.driver = webdriver.Chrome(options=options)

        elif browser_lower in VALID_EDGE_STRINGS:
            self.driver = webdriver.Edge()

        elif browser_lower in VALID_FIREFOX_STRINGS:
            self.driver = webdriver.Firefox()

        elif browser_lower in VALID_OPERA_STRINGS:
            self._init_opera()

        elif browser_lower in VALID_INTERNET_EXPLORER_STRINGS:
            self._init_ie()

        else:
            raise ValueError("No matching browser found")

        # Get around captcha
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": "const newProto = navigator.__proto__;"
                "delete newProto.webdriver;"
                "navigator.__proto__ = newProto;"
            },
        )
        # Maximize the browser
        self.driver.maximize_window()

    def _init_opera(self) -> None:
        """Initialize Opera driver (requires webdriver-manager)."""
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from webdriver_manager.opera import OperaDriverManager

            webdriver_service = ChromeService(OperaDriverManager().install())
            webdriver_service.start()
            options = webdriver.ChromeOptions()
            options.add_experimental_option("w3c", True)
            self.driver = webdriver.Remote(
                webdriver_service.service_url, options=options
            )
        except ImportError:
            raise ImportError(
                "Opera browser requires webdriver-manager. "
                "Install it with: pip install webdriver-manager"
            )

    def _init_ie(self) -> None:
        """Initialize Internet Explorer driver (requires webdriver-manager)."""
        try:
            from webdriver_manager.microsoft import IEDriverManager

            self.driver = webdriver.Ie(
                service=ChromeService(IEDriverManager().install())
            )
        except ImportError:
            raise ImportError(
                "Internet Explorer requires webdriver-manager. "
                "Install it with: pip install webdriver-manager"
            )

    @staticmethod
    def _build_ci_options_chrome() -> ChromeOptions:
        """
        Build chrome options required to run in CI.

        :return: ChromeOptions configured for CI
        """
        user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 "
            "Safari/537.36"
        )
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("accept-language=en-GB,en-US;q=0.9,en;q=0.8")
        options.add_argument("--window-size=1325x744")
        logger.info("This is a CI run")
        return options
