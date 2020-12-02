import argparse
from unittest import mock

import pytest

from udemy_enroller import parse_args


@pytest.mark.parametrize(
    "browser_cli,max_pages_cli,expected_browser,expected_max_pages,print_help",
    [
        ("chrome", None, "chrome", None, False),
        ("firefox", None, "firefox", None, False),
        ("chromium", None, "chromium", None, False),
        ("internet_explorer", None, "internet_explorer", None, False),
        ("opera", None, "opera", None, False),
        ("edge", None, "edge", None, False),
        (None, None, None, None, True),
        ("firefox", 10, "firefox", 10, False),
    ],
    ids=(
        "Test chrome via cli",
        "Test firefox via cli",
        "Test chromium via cli",
        "Test internet_explorer via cli",
        "Test opera via cli",
        "Test edge via cli",
        "No browser selected print help",
        "Pass max pages via cli",
    ),
)
@mock.patch("argparse.ArgumentParser.print_help")
def test_argparse(
    mock_print_help,
    browser_cli,
    max_pages_cli,
    expected_browser,
    expected_max_pages,
    print_help,
):
    with mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(browser=browser_cli, max_pages=max_pages_cli),
    ):
        args = parse_args()
        if print_help:
            assert mock_print_help.call_count == 1
        else:
            assert args.browser == expected_browser
            assert args.max_pages is expected_max_pages
