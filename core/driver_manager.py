from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.utils import ChromeType


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

        if self.browser.lower() in ("chrome", "google-chrome"):
            if self.is_ci_build:
                self.options = self._build_ci_options_chrome()
            self.driver = webdriver.Chrome(
                ChromeDriverManager().install(), options=self.options
            )
        elif self.browser.lower() in ("chromium",):
            self.driver = webdriver.Chrome(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            )
        elif self.browser.lower() in ("edge",):
            self.driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        elif self.browser.lower() in ("firefox", "ff"):
            self.driver = webdriver.Firefox(
                executable_path=GeckoDriverManager().install()
            )
        elif self.browser.lower() in ("opera",):
            self.driver = webdriver.Opera(
                executable_path=OperaDriverManager().install()
            )
        elif self.browser.lower() in ("internet_explorer", "ie"):
            self.driver = webdriver.Ie(IEDriverManager().install())
        else:
            raise ValueError("No matching browser found")

        # Maximize the browser
        self.driver.maximize_window()

    @staticmethod
    def _build_ci_options_chrome():
        """
        Build chrome options required to run in CI

        :return:
        """
        from selenium.webdriver.chrome.options import Options

        # Having the user-agent with Headless param was always leading to robot check
        user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 "
            "Safari/537.36"
        )
        options = Options()
        # We need to run headless when using github CI
        options.add_argument("--headless")
        options.add_argument("user-agent={0}".format(user_agent))
        options.add_argument("--window-size=1325x744")
        print("This is a CI run")
        return options
