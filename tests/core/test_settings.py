import os
from unittest import mock

import pytest
from ruamel.yaml import YAML

from core import Settings


@pytest.mark.parametrize(
    "email,password,zip_code,languages,categories,save,file_name",
    [
        (
            "test4@mail.com",
            "dskalksdl678",
            "12345",
            None,
            None,
            "Y",
            "test_settings1.yaml",
        ),
        (
            "test6@mail.com",
            "$6237556^^$",
            "12345",
            "English,French",
            None,
            "Y",
            "test_settings2.yaml",
        ),
        (
            "test9@mail.com",
            "$62371231236^^$",
            "12345",
            "English,French",
            "Development,Art",
            "Y",
            "test_settings5.yaml",
        ),
        (
            "cultest8lzie@mail.com",
            "43223*&6",
            "12345",
            None,
            None,
            "N",
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
def test_settings(email, password, zip_code, languages, categories, save, file_name):
    with mock.patch(
        "builtins.input", side_effect=[email, zip_code, languages, categories, save]
    ):
        with mock.patch("getpass.getpass", return_value=password):
            settings_path = f"test_tmp/{file_name}"
            settings = Settings(settings_path)
            assert settings.email == email
            assert settings.password == password
            assert settings.zip_code == zip_code
            assert settings.languages == [] if languages is None else languages
            assert settings.categories == [] if categories is None else categories

            if save.upper() == "Y":
                yaml = YAML()
                with open(settings_path) as f:
                    settings = yaml.load(f)
                    assert settings["udemy"]["email"] == email
                    assert settings["udemy"]["password"] == password
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
                Settings(settings_path)
            else:
                assert os.path.isdir(settings_path) is False


@pytest.mark.parametrize(
    "email,password,zip_code,languages,categories,save,file_name",
    [
        (
            "test9@mail.com",
            "uherwh834",
            "12345",
            None,
            None,
            "Y",
            "test_load_existing_settings1.yaml",
        ),
        (
            "test80@mail.com",
            "jkajsdsad",
            "None",
            "Italian",
            None,
            "Y",
            "test_load_existing_settings9.yaml",
        ),
        (
            "test10@mail.com",
            "234sdfs",
            "None",
            "English",
            "Development,Art",
            "Y",
            "test_load_existing_settings2.yaml",
        ),
        (
            "test11@mail.com",
            "frtuhrfty234",
            "788192",
            "French,German",
            None,
            "Y",
            "test_load_existing_settings3.yaml",
        ),
    ],
    ids=(
        "load existing settings no languages",
        "load existing settings no categories",
        "load existing settings no zipcode",
        "load existing settings full",
    ),
)
def test_load_existing_settings(
    email, password, zip_code, languages, categories, save, file_name
):
    with mock.patch(
        "builtins.input", side_effect=[email, zip_code, languages, categories, save]
    ):
        with mock.patch("getpass.getpass", return_value=password):
            settings_path = f"test_tmp/{file_name}"
            Settings(settings_path)

    # Load existing settings
    settings = Settings(settings_path)
    assert settings.email == email
    assert settings.password == password
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
    settings = Settings("")
    if is_ci_run:
        assert settings.email == email
        assert settings.password == password
