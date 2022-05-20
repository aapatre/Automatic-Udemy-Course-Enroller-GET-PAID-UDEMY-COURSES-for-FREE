from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.utils import ChromeType

from udemy_enroller.logging import get_logger

logger = get_logger()

VALID_FIREFOX_STRINGS = {"ff", "firefox"}
VALID_CHROME_STRINGS = {"chrome", "google-chrome"}
VALID_CHROMIUM_STRINGS = {"chromium"}
VALID_INTERNET_EXPLORER_STRINGS = {"internet_explorer", "ie"}
VALID_OPERA_STRINGS = {"opera"}
VALID_EDGE_STRINGS = {"edge"}

ALL_VALID_BROWSER_STRINGS = VALID_CHROME_STRINGS.union(VALID_CHROMIUM_STRINGS)


class DriverManager:
    def __init__(self, browser: str, is_ci_build: bool = False):
        self.driver = None
        self.options = None
        self.browser = browser
        self.is_ci_build = is_ci_build
        self._init_driver()

    def _init_driver(self):
        """
        Initialize the correct web driver based on the users requested browser

        :return: None
        """

        if self.browser.lower() in VALID_CHROME_STRINGS:
            if self.is_ci_build:
                self.options = self._build_ci_options_chrome()

            self.driver = webdriver.Chrome(
                ChromeDriverManager().install(), options=self.options
            )
        elif self.browser.lower() in VALID_CHROMIUM_STRINGS:
            self.driver = webdriver.Chrome(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            )
        elif self.browser.lower() in VALID_EDGE_STRINGS:
            self.driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        elif self.browser.lower() in VALID_FIREFOX_STRINGS:
            self.driver = webdriver.Firefox(
                executable_path=GeckoDriverManager().install()
            )
        elif self.browser.lower() in VALID_OPERA_STRINGS:
            self.driver = webdriver.Opera(
                executable_path=OperaDriverManager().install()
            )
        elif self.browser.lower() in VALID_INTERNET_EXPLORER_STRINGS:
            self.driver = webdriver.Ie(IEDriverManager().install())
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
        Build chrome options required to run in CI

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
