"""Settings."""

import getpass
import os
from pathlib import Path

from ruamel.yaml import YAML

from udemy_enroller.logger import get_logger
from udemy_enroller.utils import get_app_dir

logger = get_logger()


class Settings:
    """Contains all logic related to the scripts settings."""

    def __init__(
        self, delete_settings: bool = False, delete_cookie: bool = False, settings_path: str = "settings.yaml"
    ):
        """Initialize."""
        self.email: str | None = None
        self.password: str | None = None
        self.zip_code: str | None = None
        self.languages: list[str] = []
        self.categories: list[str] = []
        self.authors: list[str] = []
        self.years: list[str] = []

        self._settings_path: Path = get_app_dir() / settings_path
        self._cookies_path: Path = get_app_dir() / ".cookie"
        self._should_store_email: bool = False
        self._should_store_password: bool = False
        self.is_ci_build: bool = os.environ.get("CI_TEST", "").lower() in ("true", "1", "yes")
        if delete_settings:
            self.delete_settings()
        if delete_cookie:
            self.delete_cookie()
        self._init_settings()

    def _init_settings(self) -> None:
        """Initialize the settings to be used in the script."""
        if self.is_ci_build:
            self._load_ci_settings()
        else:
            settings = self._load_user_settings()
            if settings is None:
                self._generate_settings()
                self._save_settings()

    def _load_ci_settings(self) -> None:
        """Load environment variables for CI run."""
        logger.info("Loading CI settings")
        self.email = os.environ["UDEMY_EMAIL"]
        self.password = os.environ["UDEMY_PASSWORD"]

    def _load_user_settings(self) -> dict | None:
        """Load the settings from the yaml file if it exists."""
        yaml = YAML()

        settings = None
        if self._settings_path.is_file():
            logger.info("Loading existing settings")
            with open(self._settings_path) as f:
                settings = yaml.load(f)
            udemy_settings = settings["udemy"]
            self.email = udemy_settings["email"]
            self.password = udemy_settings["password"]
            self.zip_code = udemy_settings.get("zipcode")
            self.languages = udemy_settings.get("languages")
            self.categories = udemy_settings.get("categories")
            self.authors = udemy_settings.get("authors")
            self.years = udemy_settings.get("years")

        return settings

    def _generate_settings(self) -> None:
        """Generate the settings for the script."""
        self.email, self._should_store_email = self._get_email()
        self.password, self._should_store_password = self._get_password()
        self.zip_code = self._get_zip_code()
        self.languages = self._get_languages()
        self.categories = self._get_categories()
        self.authors = self._get_authors()
        self.years = self._get_years()

    def _get_email(self, prompt_save: bool = True) -> tuple[str, bool]:
        """Get input from user on the email to use for udemy."""
        email = input("Please enter your udemy email address: ")
        if len(email) == 0:
            logger.warning("You must provide your email")
            return self._get_email(prompt_save=prompt_save)
        if prompt_save:
            save_email = input("Do you want to save your email for future use (Y/N): ")
            should_store = save_email.lower() == "y"
        else:
            should_store = False
        return email, should_store

    def _get_password(self, prompt_save: bool = True) -> tuple[str, bool]:
        """Get input from user on the password to use for udemy."""
        password = getpass.getpass(prompt="Please enter your udemy password: ")
        if len(password) == 0:
            logger.warning("You must provide your password")
            return self._get_password(prompt_save=prompt_save)
        if prompt_save:
            save_password = input(
                "Do you want to save your password for future use (Y/N): "
            )
            should_store = save_password.lower() == "y"
        else:
            should_store = False
        return password, should_store

    @staticmethod
    def _get_zip_code() -> str:
        """Get input from user on the zip code to use for udemy."""
        zip_code = input("Please enter your zipcode (Not necessary in some regions): ")
        return zip_code

    @staticmethod
    def _get_languages() -> list[str]:
        """Get input from user on the languages they want to get courses in."""
        languages = input(
            "Please enter your language preferences (comma separated list e.g. English,German): "
        )
        return [lang.strip() for lang in languages.split(",")] if languages else []

    @staticmethod
    def _get_categories() -> list[str]:
        """Get the categories the user wants."""
        categories = input(
            "Please enter in a list of comma separated values of"
            " the course categories you like, for example:\n"
            "Development, Design\n> "
        )
        return (
            [category.strip() for category in categories.split(",")]
            if categories
            else []
        )

    @staticmethod
    def _get_authors() -> list[str]:
        """Get the authors the user wants."""
        authors = input(
            "Please enter in a list of semicolon separated values of"
            " the authors you like, for example:\n"
            "John Doe; Jane Doe\n> "
        )
        return [author.strip() for author in authors.split(";")] if authors else []

    @staticmethod
    def _get_years() -> list[str]:
        """Get the years the user wants."""
        years = input(
            "Please enter in a list of comma separated values of"
            " the years you like, for example:\n"
            "2018, 2019\n> "
        )
        return [year.strip() for year in years.split(",")] if years else []

    def _save_settings(self) -> None:
        """Save settings to file."""
        yaml_structure = {
            "udemy": {
                "email": str(self.email) if self._should_store_email else None,
                "password": str(self.password) if self._should_store_password else None,
                "zipcode": str(self.zip_code),
                "languages": self.languages,
                "categories": self.categories,
                "authors": self.authors,
                "years": self.years,
            }
        }

        yaml = YAML()
        yaml.default_flow_style = False
        with open(self._settings_path, "w") as f:
            yaml.dump(yaml_structure, stream=f)
        logger.info(f"Saved your settings in {self._settings_path}")

        if not self._should_store_email:
            logger.info("Your email has not been saved to settings.")
        if not self._should_store_password:
            logger.info("Your password has not been saved to settings.")
        if not self._should_store_email or not self._should_store_password:
            logger.info(
                "You will be prompted to enter your email/password again when the cookie expires"
            )

    def delete_settings(self) -> None:
        """Delete the settings file."""
        if self._settings_path.is_file():
            delete_settings = input(
                "Please confirm that you want to delete your saved settings (Y/N): "
            )
            if delete_settings.lower() == "y":
                self._settings_path.unlink()
                logger.info(f"Settings file deleted: {self._settings_path}")
        else:
            logger.info("No settings to delete")

    def delete_cookie(self) -> None:
        """Delete the cookie file."""
        if self._cookies_path.is_file():
            self._cookies_path.unlink()
            logger.info(f"Cookie file deleted: {self._cookies_path}")
        else:
            logger.info("No cookie file to delete")

    def prompt_email(self) -> None:
        """Prompt for Udemy email only. Does not prompt for saving."""
        self.email, _ = self._get_email(prompt_save=False)

    def prompt_password(self) -> None:
        """Prompt for Udemy password only. Does not prompt for saving."""
        self.password, _ = self._get_password(prompt_save=False)
