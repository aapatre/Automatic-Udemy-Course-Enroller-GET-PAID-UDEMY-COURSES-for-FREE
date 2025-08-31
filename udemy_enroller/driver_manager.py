"""Webdriver manager."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService
from webdriver_manager.chrome import ChromeDriverManager

try:
    # For webdriver_manager 3.x
    from webdriver_manager.core.utils import ChromeType
except ImportError:
    try:
        # For webdriver_manager 4.x
        from webdriver_manager.core.os_manager import ChromeType
    except ImportError:
        # For newer webdriver_manager 4.x versions
        from webdriver_manager.core.driver import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager
from webdriver_manager.opera import OperaDriverManager

from udemy_enroller.logger import get_logger

logger = get_logger()

VALID_FIREFOX_STRINGS = {"ff", "firefox"}
VALID_CHROME_STRINGS = {"chrome", "google-chrome"}
VALID_CHROMIUM_STRINGS = {"chromium"}
VALID_INTERNET_EXPLORER_STRINGS = {"internet_explorer", "ie"}
VALID_OPERA_STRINGS = {"opera"}
VALID_EDGE_STRINGS = {"edge"}

ALL_VALID_BROWSER_STRINGS = VALID_CHROME_STRINGS.union(VALID_CHROMIUM_STRINGS)


class DriverManager:
    """Webdriver manager."""

    def __init__(self, browser: str, is_ci_build: bool = False):
        """Initialize."""
        self.driver = None
        self.options = None
        self.browser = browser
        self.is_ci_build = is_ci_build
        self._init_driver()

    def _init_driver(self):
        """
        Initialize the correct web driver based on the users requested browser.

        :return: None
        """
        if self.browser.lower() in VALID_CHROME_STRINGS:
            if self.is_ci_build:
                self.options = self._build_ci_options_chrome()

            try:
                # Try using webdriver_manager first
                self.driver = webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager().install()),
                    options=self.options,
                )
            except Exception as e:
                logger.warning(
                    f"Failed to initialize Chrome with webdriver_manager: {e}"
                )
                # Fallback: Try without explicit driver installation
                # This will work if chromedriver is in PATH
                try:
                    self.driver = webdriver.Chrome(options=self.options)
                except Exception as fallback_error:
                    logger.error(
                        f"Failed to initialize Chrome driver: {fallback_error}"
                    )
                    raise
        elif self.browser.lower() in VALID_CHROMIUM_STRINGS:
            self.driver = webdriver.Chrome(
                service=ChromeService(
                    ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
                )
            )
        elif self.browser.lower() in VALID_EDGE_STRINGS:
            self.driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install())
            )
        elif self.browser.lower() in VALID_FIREFOX_STRINGS:
            self.driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install())
            )
        elif self.browser.lower() in VALID_OPERA_STRINGS:
            webdriver_service = ChromeService(OperaDriverManager().install())
            webdriver_service.start()
            options = webdriver.ChromeOptions()
            options.add_experimental_option("w3c", True)
            self.driver = webdriver.Remote(
                webdriver_service.service_url, options=options
            )
        elif self.browser.lower() in VALID_INTERNET_EXPLORER_STRINGS:
            self.driver = webdriver.Ie(service=IEService(IEDriverManager().install()))
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

    @staticmethod
    def _build_ci_options_chrome():
        """
        Build chrome options required to run in CI.

        :return:
        """
        # Having the user-agent with Headless param was always leading to robot check
        user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 "
            "Safari/537.36"
        )
        options = ChromeOptions()
        # We need to run headless when using github CI
        options.add_argument("--headless")
        options.add_argument("user-agent={0}".format(user_agent))
        options.add_argument("accept-language=en-GB,en-US;q=0.9,en;q=0.8")
        options.add_argument("--window-size=1325x744")
        logger.info("This is a CI run")
        return options
