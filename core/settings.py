import getpass
import os.path
from distutils.util import strtobool
from typing import Dict, List

from ruamel.yaml import YAML, dump


class Settings:
    """
    Contains all logic related to the scripts settings
    """

    def __init__(self):
        self.email = None
        self.password = None
        self.zip_code = None
        self.languages = []
        self.categories = []

        self._settings_path = "settings.yaml"
        self.is_ci_build = strtobool(os.environ.get("CI", "False"))
        self._init_settings()

    def _init_settings(self) -> None:
        """
        Initialize the settings to be used in the script

        :return:
        """
        if self.is_ci_build:
            self._load_ci_settings()
        else:
            settings = self._load_user_settings()
            if settings is None:
                self._generate_settings()
                self._save_settings()

    def _load_ci_settings(self):
        """
        Load environment variables for CI run

        :return:
        """
        print("Loading CI settings")
        self.email = os.environ["UDEMY_EMAIL"]
        self.password = os.environ["UDEMY_PASSWORD"]

    def _load_user_settings(self) -> Dict:
        """
        Loads the settings from the yaml file if it exists

        :return: dictionary containing the script settings
        """
        yaml = YAML()

        settings = None
        if os.path.isfile(self._settings_path):
            print("Loading existing settings")
            with open(self._settings_path) as f:
                settings = yaml.load(f)
            udemy_settings = settings["udemy"]
            self.email = udemy_settings["email"]
            self.password = udemy_settings["password"]
            self.zip_code = udemy_settings.get("zipcode")
            self.languages = udemy_settings.get("languages")
            self.categories = udemy_settings.get("categories", [])

        self.categories = []
        return settings

    def _generate_settings(self) -> None:
        """
        Generate the settings for the script

        :return:
        """
        self.email = self._get_email()
        self.password = self._get_password()
        self.zip_code = self._get_zip_code()
        self.languages = self._get_languages()
        self.categories = self._get_categories()

    def _get_email(self) -> str:
        """
        Get input from user on the email to use for udemy

        :return: The users udemy email
        """
        email = input("Please enter your udemy email address: ")
        if len(email) == 0:
            print("You must provide your email")
            return self._get_email()
        return email

    def _get_password(self) -> str:
        """
        Get input from user on the password to use for udemy

        :return: The users udemy password
        """
        password = getpass.getpass(prompt="Please enter your udemy password: ")
        if len(password) == 0:
            print("You must provide your password")
            return self._get_password()
        return password

    @staticmethod
    def _get_zip_code() -> str:
        """
        Get input from user on the zip code to use for udemy

        :return: The users udemy zip code
        """
        zip_code = input("Please enter your zipcode (Not necessary in some regions): ")
        return zip_code

    @staticmethod
    def _get_languages() -> List[str]:
        """
        Get input from user on the languages they want to get courses in

        :return: list of languages the user wants to redeem udemy courses in
        """
        languages = input(
            "Please enter your language preferences (comma separated list e.g. English,German): "
        )
        return [lang.strip() for lang in languages.split(",")] if languages else []

    @staticmethod
    def _get_categories() -> List[str]:
        categories = input(
            "Please enter in a list of comma separated values of"
            " the course categories you like, for example:\n"
            "Development, Design\n>"
        )
        return (
            [category.strip() for category in categories.split(",")]
            if categories
            else []
        )

    def _save_settings(self) -> None:
        """
        Confirm if the user wants to save settings to file

        :return:
        """
        yaml_structure = dict()
        save_settings = input("Do you want to save settings for future use (Y/N): ")
        if save_settings.lower() == "y":
            yaml_structure["udemy"] = {
                "email": str(self.email),
                "password": str(self.password),
                "zipcode": str(self.zip_code),
                "languages": self.languages,
                "categories": str(self.categories),
            }

            with open(self._settings_path, "w+") as f:
                dump(yaml_structure, stream=f)
            print(f"Saved your settings in {self._settings_path}")
        else:
            print("Not saving your settings as requested")


class Constants:
    udemy_categories = {
        "Development": [
            "Web Development",
            "Mobile Development",
            "Programming Languages",
            "Game Development",
            "Database Design & Development",
            "Software Testing",
        ],
        "Business": {},
        "Finance & Accounting": {},
        "IT & Software": {},
        "Office Productivity": {},
        "Personal Development": {},
        "Design": {},
        "Marketing": {},
        "Health & Fitness": {},
        "Music": {},
    }
