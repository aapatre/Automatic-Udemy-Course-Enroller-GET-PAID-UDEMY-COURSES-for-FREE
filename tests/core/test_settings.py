import os
from unittest import mock

import pytest
from ruamel.yaml import YAML

from udemy_enroller import Settings
from udemy_enroller.utils import get_app_dir


@pytest.mark.parametrize(
    "email,should_save_email,password,should_save_password,zip_code,languages,categories,file_name",
    [
        (
            "test4@mail.com",
            "Y",
            "dskalksdl678",
            "Y",
            "12345",
            None,
            None,
            "test_settings1.yaml",
        ),
        (
            "test6@mail.com",
            "Y",
            "$6237556^^$",
            "Y",
            "12345",
            "English,French",
            None,
            "test_settings2.yaml",
        ),
        (
            "test9@mail.com",
            "Y",
            "$62371231236^^$",
            "Y",
            "12345",
            "English,French",
            "Development,Art",
            "test_settings5.yaml",
        ),
        (
            "cultest8lzie@mail.com",
            "Y",
            "43223*&6",
            "Y",
            "12345",
            None,
            None,
            "no_save_test_settings.yaml",
        ),
    ],
    ids=(
        "create settings all languages and save",
        "create settings select languages and save",
        "create settings select categories and save",
        "create settings all languages and don't save",
    ),
)
def test_settings(
    email,
    should_save_email,
    password,
    should_save_password,
    zip_code,
    languages,
    categories,
    file_name,
):
    with mock.patch(
        "builtins.input",
        side_effect=[
            email,
            should_save_email,
            should_save_password,
            zip_code,
            languages,
            categories,
        ],
    ):
        with mock.patch("getpass.getpass", return_value=password):
            settings_path = os.path.join(get_app_dir(), f"test_tmp/{file_name}")
            settings = Settings(False, settings_path)
            assert settings.email == email
            assert settings.password == password
            assert settings.zip_code == zip_code
            assert settings.languages == [] if languages is None else languages
            assert settings.categories == [] if categories is None else categories

            yaml = YAML()
            with open(settings_path) as f:
                settings = yaml.load(f)
                if should_save_email.upper() == "Y":
                    assert settings["udemy"]["email"] == email
                else:

                    assert settings["udemy"]["email"] is None
                if should_save_password.upper() == "Y":
                    assert settings["udemy"]["password"] == password
                else:
                    assert settings["udemy"]["password"] is None

                assert settings["udemy"]["zipcode"] == zip_code
                assert (
                    settings["udemy"]["languages"] == []
                    if languages is None
                    else ",".join(languages)
                )
                assert (
                    settings["udemy"]["categories"] == []
                    if categories is None
                    else categories
                )
            # Load settings just created
            Settings(False, settings_path)


@pytest.mark.parametrize(
    "email,should_save_email,password,should_save_password,zip_code,languages,categories,file_name",
    [
        (
            "test9@mail.com",
            "Y",
            "uherwh834",
            "Y",
            "12345",
            None,
            None,
            "test_load_existing_settings1.yaml",
        ),
        (
            "test80@mail.com",
            "Y",
            "jkajsdsad",
            "Y",
            "None",
            "Italian",
            None,
            "test_load_existing_settings9.yaml",
        ),
        (
            "test10@mail.com",
            "Y",
            "234sdfs",
            "Y",
            "None",
            "English",
            "Development,Art",
            "test_load_existing_settings2.yaml",
        ),
        (
            "test11@mail.com",
            "Y",
            "frtuhrfty234",
            "Y",
            "788192",
            "French,German",
            None,
            "test_load_existing_settings4.yaml",
        ),
        (
            "test54@mail.com",
            "N",
            "op123890",
            "Y",
            "788192",
            "French,German",
            None,
            "test_load_existing_settings3.yaml",
        ),
        (
            "test55@mail.com",
            "Y",
            "ajsdkljaklsdj",
            "N",
            "1231",
            "French,German",
            None,
            "test_load_existing_settings5.yaml",
        ),
        (
            "test70@mail.com",
            "N",
            "sda123efg",
            "N",
            "1231",
            "English,German",
            None,
            "test_load_existing_settings6.yaml",
        ),
    ],
    ids=(
        "load existing settings no languages",
        "load existing settings no categories",
        "load existing settings no zipcode",
        "load existing settings full",
        "load existing settings no email",
        "load existing settings no password",
        "load existing settings no email or pasword",
    ),
)
def test_load_existing_settings(
    email,
    should_save_email,
    password,
    should_save_password,
    zip_code,
    languages,
    categories,
    file_name,
):
    with mock.patch(
        "builtins.input",
        side_effect=[
            email,
            should_save_email,
            should_save_password,
            zip_code,
            languages,
            categories,
        ],
    ):
        with mock.patch("getpass.getpass", return_value=password):
            settings_path = f"test_tmp/{file_name}"
            Settings(False, settings_path)

    # Load existing settings
    settings = Settings(False, settings_path)
    if should_save_email.upper() == "Y":
        assert settings.email == email
    else:
        assert settings.email is None
    if should_save_password.upper() == "Y":
        assert settings.password == password
    else:
        assert settings.password is None
    assert settings.zip_code == zip_code
    assert settings.languages == [] if languages is None else languages
    assert settings.categories == [] if categories is None else categories


@pytest.mark.parametrize(
    "is_ci_run,email,password",
    [
        (
            True,
            "username1@mail.com",
            "password1",
        ),
        (
            False,
            "username2@mail.com",
            "password2",
        ),
    ],
    ids=(
        "is ci run",
        "is not a ci run",
    ),
)
@mock.patch.object(Settings, "_load_user_settings")
def test_load_ci_settings(_, monkeypatch, is_ci_run, email, password):
    monkeypatch.setenv("CI_TEST", str(is_ci_run))
    monkeypatch.setenv("UDEMY_EMAIL", email)
    monkeypatch.setenv("UDEMY_PASSWORD", password)
    settings = Settings(False, "")
    if is_ci_run:
        assert settings.email == email
        assert settings.password == password
