"""Tests for udemy_ui module."""

from decimal import Decimal
from unittest import mock

import pytest
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from udemy_enroller.exceptions import LoginException, RobotException
from udemy_enroller.udemy_ui import UdemyActionsUI, UdemyStatus, RunStatistics


@pytest.fixture
def mock_driver():
    return mock.MagicMock()


@pytest.fixture
def mock_settings():
    s = mock.MagicMock()
    s.email = "test@test.com"
    s.password = "password"
    s.categories = []
    s.languages = []
    s.authors = []
    s.years = []
    s.zip_code = None
    s.is_ci_build = False
    return s


class TestRunStatisticsUI:
    def test_savings_empty(self):
        stats = RunStatistics()
        assert stats.savings() == 0

    def test_savings_with_decimals(self):
        stats = RunStatistics()
        stats.prices = [Decimal("10.5"), Decimal("20.25")]
        assert stats.savings() == Decimal("30.75")

    def test_table_with_prices(self, caplog):
        import logging
        logger = logging.getLogger("udemy_enroller")
        original = logger.level
        logger.setLevel(logging.INFO)
        try:
            stats = RunStatistics()
            stats.prices = [Decimal("10.0")]
            stats.enrolled = 1
            stats.start_time = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
            stats.table()
            assert "Enrolled:" in caplog.text
        finally:
            logger.setLevel(original)

    def test_table_empty_prices(self, caplog):
        import logging
        logger = logging.getLogger("udemy_enroller")
        original = logger.level
        logger.setLevel(logging.INFO)
        try:
            stats = RunStatistics()
            stats.table()
            assert "Run Statistics" not in caplog.text
        finally:
            logger.setLevel(original)


class TestUdemyActionsUIInit:
    def test_init(self, mock_driver, mock_settings):
        actions = UdemyActionsUI(mock_driver, mock_settings)
        assert actions.driver == mock_driver
        assert actions.settings == mock_settings
        assert actions.logged_in is False
        assert actions.stats.start_time is not None


class TestLogin:
    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_login_success(self, mock_wait_class, mock_driver, mock_settings):
        mock_wait = mock.MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.return_value = mock.MagicMock()

        actions = UdemyActionsUI(mock_driver, mock_settings)
        actions.login()
        assert actions.logged_in is True
        mock_driver.get.assert_called_once()

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_login_already_logged_in(self, mock_wait_class, mock_driver, mock_settings):
        actions = UdemyActionsUI(mock_driver, mock_settings)
        actions.logged_in = True
        actions.login()
        mock_driver.get.assert_not_called()

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_login_prompts_email_password(self, mock_wait_class, mock_driver, mock_settings):
        mock_settings.email = None
        mock_settings.password = None
        mock_wait = mock.MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.return_value = mock.MagicMock()

        actions = UdemyActionsUI(mock_driver, mock_settings)
        actions.login()
        mock_settings.prompt_email.assert_called_once()
        mock_settings.prompt_password.assert_called_once()

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_login_no_such_element_robot_first_try(self, mock_wait_class, mock_driver, mock_settings):
        """Test that NoSuchElementException triggers robot check and retry."""
        email_fail_count = [0]

        def find_element_side_effect(*args, **kwargs):
            # Only fail the email lookup on the very first call
            if kwargs.get("value") == "email":
                email_fail_count[0] += 1
                if email_fail_count[0] == 1:
                    raise NoSuchElementException("not found")
            return mock.MagicMock()

        mock_driver.find_element.side_effect = find_element_side_effect
        mock_wait_class.return_value.until.return_value = mock.MagicMock()

        actions = UdemyActionsUI(mock_driver, mock_settings)
        with mock.patch("builtins.input", return_value=""):
            with mock.patch.object(actions, "_check_if_robot", side_effect=[True, False]):
                actions.login()
        assert actions.logged_in is True

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_login_no_such_element_robot_retry_raises(self, mock_wait_class, mock_driver, mock_settings):
        mock_driver.find_element.side_effect = NoSuchElementException("not found")

        actions = UdemyActionsUI(mock_driver, mock_settings)
        with mock.patch.object(actions, "_check_if_robot", return_value=True):
            with pytest.raises(RobotException):
                actions.login(is_retry=True)

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_login_no_such_element_not_robot_raises(self, mock_wait_class, mock_driver, mock_settings):
        mock_driver.find_element.side_effect = NoSuchElementException("not found")

        actions = UdemyActionsUI(mock_driver, mock_settings)
        with mock.patch.object(actions, "_check_if_robot", return_value=False):
            with pytest.raises(NoSuchElementException):
                actions.login()

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_login_timeout_robot_first_try(self, mock_wait_class, mock_driver, mock_settings):
        mock_wait = mock.MagicMock()
        mock_wait_class.return_value = mock_wait
        # WebDriverWait only called once for user dropdown in login()
        mock_wait.until.side_effect = TimeoutException()

        actions = UdemyActionsUI(mock_driver, mock_settings)
        with mock.patch.object(actions, "_check_if_robot", side_effect=[True, False]):
            with mock.patch("builtins.input", return_value=""):
                actions.login()
        assert actions.logged_in is True

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_login_timeout_robot_still_present(self, mock_wait_class, mock_driver, mock_settings):
        mock_wait = mock.MagicMock()
        mock_wait_class.return_value = mock_wait
        # WebDriverWait is only called once in login() for the user dropdown
        mock_wait.until.side_effect = TimeoutException()

        actions = UdemyActionsUI(mock_driver, mock_settings)
        with mock.patch.object(actions, "_check_if_robot", return_value=True):
            with mock.patch("builtins.input", return_value=""):
                with pytest.raises(RobotException):
                    actions.login()

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_login_timeout_not_robot_raises(self, mock_wait_class, mock_driver, mock_settings):
        mock_wait = mock.MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.side_effect = TimeoutException()

        actions = UdemyActionsUI(mock_driver, mock_settings)
        with mock.patch.object(actions, "_check_if_robot", return_value=False):
            with pytest.raises(LoginException):
                actions.login()


class TestEnroll:
    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_enroll_unwanted_language(self, mock_wait_class, mock_driver, mock_settings):
        mock_settings.languages = ["English"]
        mock_driver.title = "Test Course"

        mock_wait = mock.MagicMock()
        mock_wait_class.return_value = mock_wait
        locale_element = mock.MagicMock()
        locale_element.text = "German"
        mock_wait.until.return_value = locale_element

        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions.enroll("https://udemy.com/course/test")
        assert result == UdemyStatus.UNWANTED_LANGUAGE.value

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_enroll_unwanted_category(self, mock_wait_class, mock_driver, mock_settings):
        mock_settings.categories = ["Music"]
        mock_driver.title = "Test Course"

        mock_wait = mock.MagicMock()
        mock_wait_class.return_value = mock_wait
        # First call is for language check (no languages set, so skip)
        # Actually _check_languages checks settings.languages first
        # Since languages=[], it returns True without calling WebDriverWait
        # Then _check_categories is called

        breadcrumb = mock.MagicMock()
        bc1 = mock.MagicMock()
        bc1.text = "Development"
        breadcrumb.find_elements.return_value = [bc1]
        mock_driver.find_element.return_value = breadcrumb

        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions.enroll("https://udemy.com/course/test")
        assert result == UdemyStatus.UNWANTED_CATEGORY.value

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_enroll_unwanted_author(self, mock_wait_class, mock_driver, mock_settings):
        mock_settings.authors = ["Bad Author"]
        mock_driver.title = "Test Course"

        author_element = mock.MagicMock()
        author_element.text = "Bad Author"
        mock_driver.find_element.return_value = author_element

        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions.enroll("https://udemy.com/course/test")
        assert result == UdemyStatus.UNWANTED_AUTHOR.value

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_enroll_unwanted_year(self, mock_wait_class, mock_driver, mock_settings):
        mock_settings.years = ["2024"]
        mock_driver.title = "Test Course"

        year_element = mock.MagicMock()
        year_element.text = "2022"
        mock_driver.find_element.return_value = year_element

        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions.enroll("https://udemy.com/course/test")
        assert result == UdemyStatus.UNWANTED_YEAR.value

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_enroll_already_enrolled(self, mock_wait_class, mock_driver, mock_settings):
        mock_driver.title = "Test Course"

        mock_wait = mock.MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.return_value = mock.MagicMock()

        # _check_enrolled: no add_to_cart elements or not displayed
        mock_driver.find_elements.return_value = []

        actions = UdemyActionsUI(mock_driver, mock_settings)
        with mock.patch("udemy_enroller.udemy_ui.time.sleep"):
            result = actions.enroll("https://udemy.com/course/test")
        assert result == UdemyStatus.ALREADY_ENROLLED.value
        assert actions.stats.already_enrolled == 1

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_enroll_expired_course(self, mock_wait_class, mock_driver, mock_settings):
        mock_driver.title = "Test Course"

        mock_wait = mock.MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.return_value = mock.MagicMock()

        # _check_enrolled: add_to_cart is displayed (not enrolled)
        add_to_cart = mock.MagicMock()
        add_to_cart.is_displayed.return_value = True
        mock_driver.find_elements.return_value = [add_to_cart]

        # _check_price: price > 0
        price_element = mock.MagicMock()
        price_element.is_displayed.return_value = True
        price_element.text = "$10.00"
        mock_driver.find_element.return_value = price_element

        actions = UdemyActionsUI(mock_driver, mock_settings)
        with mock.patch("udemy_enroller.udemy_ui.time.sleep"):
            result = actions.enroll("https://udemy.com/course/test")
        assert result == UdemyStatus.EXPIRED.value
        assert actions.stats.expired == 1

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_enroll_success(self, mock_wait_class, mock_driver, mock_settings):
        mock_driver.title = "Test Course"

        mock_wait = mock.MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.return_value = mock.MagicMock()
        mock_wait.until_not.return_value = True

        # _check_enrolled: add_to_cart is displayed
        add_to_cart = mock.MagicMock()
        add_to_cart.is_displayed.return_value = True
        mock_driver.find_elements.return_value = [add_to_cart]

        # _check_price: free course
        price_element = mock.MagicMock()
        price_element.is_displayed.return_value = True
        price_element.text = "Free"
        list_price_element = mock.MagicMock()
        list_price_element.text = "$100.00"

        def find_element_side_effect(by, value):
            if "total-amount-summary" in value:
                return price_element
            if "order-summary--original-price-text" in value:
                return list_price_element
            return mock.MagicMock()

        mock_driver.find_element.side_effect = find_element_side_effect

        actions = UdemyActionsUI(mock_driver, mock_settings)
        with mock.patch("udemy_enroller.udemy_ui.time.sleep"):
            result = actions.enroll("https://udemy.com/course/test")
        assert result == UdemyStatus.ENROLLED.value
        assert actions.stats.enrolled == 1

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_enroll_with_zipcode(self, mock_wait_class, mock_driver, mock_settings):
        mock_settings.zip_code = "12345"
        mock_driver.title = "Test Course"

        mock_wait = mock.MagicMock()
        mock_wait_class.return_value = mock_wait
        # Track what until() was called with to verify zipcode element was waited for
        wait_calls = []
        original_until = mock_wait.until
        def until_side_effect(condition):
            wait_calls.append(condition)
            return mock.MagicMock()
        mock_wait.until.side_effect = until_side_effect
        mock_wait.until_not.return_value = True

        add_to_cart = mock.MagicMock()
        add_to_cart.is_displayed.return_value = True
        mock_driver.find_elements.return_value = [add_to_cart]

        price_element = mock.MagicMock()
        price_element.is_displayed.return_value = True
        price_element.text = "Free"
        list_price_element = mock.MagicMock()
        list_price_element.text = "$100.00"

        def find_element_side_effect(by, value):
            if "total-amount-summary" in value:
                return price_element
            if "order-summary--original-price-text" in value:
                return list_price_element
            return mock.MagicMock()

        mock_driver.find_element.side_effect = find_element_side_effect

        actions = UdemyActionsUI(mock_driver, mock_settings)
        with mock.patch("udemy_enroller.udemy_ui.time.sleep"):
            result = actions.enroll("https://udemy.com/course/test")
        assert result == UdemyStatus.ENROLLED.value

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_enroll_with_state_province(self, mock_wait_class, mock_driver, mock_settings):
        mock_driver.title = "Test Course"

        mock_wait = mock.MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.return_value = mock.MagicMock()
        mock_wait.until_not.return_value = True

        add_to_cart = mock.MagicMock()
        add_to_cart.is_displayed.return_value = True
        mock_driver.find_elements.return_value = [mock.MagicMock()]  # state element exists

        price_element = mock.MagicMock()
        price_element.is_displayed.return_value = True
        price_element.text = "Free"
        list_price_element = mock.MagicMock()
        list_price_element.text = "$100.00"

        def find_element_side_effect(by, value):
            if "total-amount-summary" in value:
                return price_element
            if "order-summary--original-price-text" in value:
                return list_price_element
            return mock.MagicMock()

        mock_driver.find_element.side_effect = find_element_side_effect

        actions = UdemyActionsUI(mock_driver, mock_settings)
        with mock.patch("udemy_enroller.udemy_ui.time.sleep"):
            result = actions.enroll("https://udemy.com/course/test")
        assert result == UdemyStatus.ENROLLED.value

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_enroll_zipcode_timeout(self, mock_wait_class, mock_driver, mock_settings):
        mock_settings.zip_code = "12345"
        mock_driver.title = "Test Course"

        mock_wait = mock.MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.return_value = mock.MagicMock()
        mock_wait.until_not.return_value = True

        # Make zipcode element lookup timeout
        call_count = [0]
        def until_side_effect(condition):
            call_count[0] += 1
            # The zipcode wait happens after buy button click and enroll button presence
            if call_count[0] == 4:
                raise TimeoutException()
            return mock.MagicMock()
        mock_wait.until.side_effect = until_side_effect

        add_to_cart = mock.MagicMock()
        add_to_cart.is_displayed.return_value = True
        mock_driver.find_elements.return_value = [add_to_cart]

        price_element = mock.MagicMock()
        price_element.is_displayed.return_value = True
        price_element.text = "Free"
        list_price_element = mock.MagicMock()
        list_price_element.text = "$100.00"

        def find_element_side_effect(by, value):
            if "total-amount-summary" in value:
                return price_element
            if "order-summary--original-price-text" in value:
                return list_price_element
            return mock.MagicMock()

        mock_driver.find_element.side_effect = find_element_side_effect

        actions = UdemyActionsUI(mock_driver, mock_settings)
        with mock.patch("udemy_enroller.udemy_ui.time.sleep"):
            result = actions.enroll("https://udemy.com/course/test")
        assert result == UdemyStatus.ENROLLED.value


class TestCheckEnrolled:
    def test_check_enrolled_no_elements(self, mock_driver, mock_settings):
        mock_driver.find_elements.return_value = []
        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_enrolled("Course")
        assert result is True
        assert actions.stats.already_enrolled == 1

    def test_check_enrolled_not_displayed(self, mock_driver, mock_settings):
        elem = mock.MagicMock()
        elem.is_displayed.return_value = False
        mock_driver.find_elements.return_value = [elem]
        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_enrolled("Course")
        assert result is True

    def test_check_enrolled_displayed(self, mock_driver, mock_settings):
        elem = mock.MagicMock()
        elem.is_displayed.return_value = True
        mock_driver.find_elements.return_value = [elem]
        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_enrolled("Course")
        assert result is False


class TestCheckLanguages:
    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_check_languages_match(self, mock_wait_class, mock_driver, mock_settings):
        mock_settings.languages = ["English"]
        elem = mock.MagicMock()
        elem.text = "English"
        mock_wait_class.return_value.until.return_value = elem

        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_languages("Course")
        assert result is True

    @mock.patch("udemy_enroller.udemy_ui.WebDriverWait")
    def test_check_languages_no_match(self, mock_wait_class, mock_driver, mock_settings):
        mock_settings.languages = ["English"]
        elem = mock.MagicMock()
        elem.text = "German"
        mock_wait_class.return_value.until.return_value = elem

        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_languages("Course")
        assert result is False
        assert actions.stats.unwanted_language == 1

    def test_check_languages_no_preference(self, mock_driver, mock_settings):
        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_languages("Course")
        assert result is True


class TestCheckCategories:
    def test_check_categories_match(self, mock_driver, mock_settings):
        mock_settings.categories = ["Development"]
        breadcrumb = mock.MagicMock()
        bc = mock.MagicMock()
        bc.text = "Development"
        breadcrumb.find_elements.return_value = [bc]
        mock_driver.find_element.return_value = breadcrumb

        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_categories("Course")
        assert result is True

    def test_check_categories_no_match(self, mock_driver, mock_settings):
        mock_settings.categories = ["Music"]
        breadcrumb = mock.MagicMock()
        bc = mock.MagicMock()
        bc.text = "Development"
        breadcrumb.find_elements.return_value = [bc]
        mock_driver.find_element.return_value = breadcrumb

        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_categories("Course")
        assert result is False
        assert actions.stats.unwanted_category == 1

    def test_check_categories_no_preference(self, mock_driver, mock_settings):
        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_categories("Course")
        assert result is True


class TestCheckAuthors:
    def test_check_author_match(self, mock_driver, mock_settings):
        mock_settings.authors = ["John Doe"]
        elem = mock.MagicMock()
        elem.text = "John Doe"
        mock_driver.find_element.return_value = elem

        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_authors("Course")
        assert result is False
        assert actions.stats.unwanted_author == 1

    def test_check_author_no_match(self, mock_driver, mock_settings):
        mock_settings.authors = ["John Doe"]
        elem = mock.MagicMock()
        elem.text = "Jane Doe"
        mock_driver.find_element.return_value = elem

        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_authors("Course")
        assert result is True

    def test_check_author_no_preference(self, mock_driver, mock_settings):
        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_authors("Course")
        assert result is True


class TestCheckYears:
    def test_check_year_match(self, mock_driver, mock_settings):
        mock_settings.years = ["2024"]
        elem = mock.MagicMock()
        elem.text = "2024"
        mock_driver.find_element.return_value = elem

        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_years("Course")
        assert result is True

    def test_check_year_no_match(self, mock_driver, mock_settings):
        mock_settings.years = ["2024"]
        elem = mock.MagicMock()
        elem.text = "2022"
        mock_driver.find_element.return_value = elem

        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_years("Course")
        assert result is False
        assert actions.stats.unwanted_year == 1

    def test_check_year_no_preference(self, mock_driver, mock_settings):
        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_years("Course")
        assert result is True


class TestCheckPrice:
    def test_check_price_free(self, mock_driver, mock_settings):
        price_elem = mock.MagicMock()
        price_elem.is_displayed.return_value = True
        price_elem.text = "Free"
        list_price_elem = mock.MagicMock()
        list_price_elem.text = "$100.00"

        def find_element_side_effect(by, value):
            if "total-amount-summary" in value:
                return price_elem
            if "order-summary--original-price-text" in value:
                return list_price_elem
            return mock.MagicMock()

        mock_driver.find_element.side_effect = find_element_side_effect

        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_price("Course")
        assert result is True
        assert len(actions.stats.prices) == 1

    def test_check_price_not_free(self, mock_driver, mock_settings):
        price_elem = mock.MagicMock()
        price_elem.is_displayed.return_value = True
        price_elem.text = "$10.00"

        def find_element_side_effect(by, value):
            if "total-amount-summary" in value:
                return price_elem
            return mock.MagicMock()

        mock_driver.find_element.side_effect = find_element_side_effect

        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_price("Course")
        assert result is False
        assert actions.stats.expired == 1

    def test_check_price_not_displayed(self, mock_driver, mock_settings):
        price_elem = mock.MagicMock()
        price_elem.is_displayed.return_value = False
        list_price_elem = mock.MagicMock()
        list_price_elem.text = "$100.00"

        def find_element_side_effect(by, value):
            if "total-amount-summary" in value:
                return price_elem
            if "order-summary--original-price-text" in value:
                return list_price_elem
            return mock.MagicMock()

        mock_driver.find_element.side_effect = find_element_side_effect

        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_price("Course")
        assert result is True
        assert len(actions.stats.prices) == 1

    def test_check_price_sets_currency(self, mock_driver, mock_settings):
        price_elem = mock.MagicMock()
        price_elem.is_displayed.return_value = True
        price_elem.text = "€0.00"
        list_price_elem = mock.MagicMock()
        list_price_elem.text = "€100.00"

        def find_element_side_effect(by, value):
            if "total-amount-summary" in value:
                return price_elem
            if "order-summary--original-price-text" in value:
                return list_price_elem
            return mock.MagicMock()

        mock_driver.find_element.side_effect = find_element_side_effect

        actions = UdemyActionsUI(mock_driver, mock_settings)
        actions._check_price("Course")
        assert actions.stats.currency_symbol == "€"


class TestCheckIfRobot:
    def test_check_if_robot_found(self, mock_driver, mock_settings):
        mock_driver.find_element.return_value = mock.MagicMock()
        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_if_robot()
        assert result is True

    def test_check_if_robot_not_found(self, mock_driver, mock_settings):
        mock_driver.find_element.side_effect = NoSuchElementException("not found")
        actions = UdemyActionsUI(mock_driver, mock_settings)
        result = actions._check_if_robot()
        assert result is False


class TestUdemyStatusUI:
    def test_status_values(self):
        assert UdemyStatus.ALREADY_ENROLLED.value == "ALREADY_ENROLLED"
        assert UdemyStatus.ENROLLED.value == "ENROLLED"
        assert UdemyStatus.EXPIRED.value == "EXPIRED"
        assert UdemyStatus.UNWANTED_LANGUAGE.value == "UNWANTED_LANGUAGE"
        assert UdemyStatus.UNWANTED_CATEGORY.value == "UNWANTED_CATEGORY"
        assert UdemyStatus.UNWANTED_AUTHOR.value == "UNWANTED_AUTHOR"
        assert UdemyStatus.UNWANTED_YEAR.value == "UNWANTED_YEAR"
