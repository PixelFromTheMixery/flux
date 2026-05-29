# region Docs
"""
[Module](app/settings.py)

Notes:

Tests:
    generate_settings_success
    generate_settings_from_supplied
    settings_file_missing
    pydantic_sanity_check_file
    pydantic_sanity_check_dict

"""
# endregion

from pydantic import ValidationError
import pytest


from app.settings import load_settings_from_file, generate_settings, Settings


def test_generate_settings_success(tmp_path, monkeypatch):
    # region Docs
    """
    Valid YAML content

    Notes: creates file in a fake dir

    Inputs:
        mock_yaml (str): acceptable yaml file

    Expected result: (Settings): Correct settings object
    """
    # endregion

    mock_yaml = f"""
        "local": false
        "api_addr": "https://api.mock.com"
        "api_port": "123"
        "db_file": {str(tmp_path / "mock.json")}
    """

    d = tmp_path / "settings.yaml"
    d.write_text(mock_yaml, encoding="UTF-8")

    monkeypatch.chdir(tmp_path)

    settings = generate_settings()

    load_settings_from_file.cache_clear()

    assert isinstance(settings, Settings)
    assert not settings.local
    assert settings.api_addr == "https://api.mock.com"
    assert settings.api_port == "123"
    assert settings.db_file == str(tmp_path / "mock.json")


def test_generate_settings_from_supplied(tmp_path, monkeypatch):
    # region Docs
    """
    Checks if supplied settings are used when provided

    Notes: Any nuances or references.

    Inputs:
        yaml_supplied (dict): mock settings from code

    Expected result: (Settings): as described by code
    """
    # endregion

    monkeypatch.chdir(tmp_path)

    yaml_supplied = {
        "local": False,
        "api_addr": "https://api.mock.com",
        "api_port": "123",
    }

    settings = generate_settings(yaml_supplied)

    assert isinstance(settings, Settings)
    assert not settings.local
    assert settings.api_addr == "https://api.mock.com"
    assert settings.api_port == "123"


def test_settings_file_missing(tmp_path, monkeypatch):
    # region Docs
    """
    Tests if settings file is missing

    Notes: tests in a fake directory.

    Expected result: (FileNotFoundError): with message about it being required
    """
    # endregion

    monkeypatch.chdir(tmp_path)

    with pytest.raises(FileNotFoundError) as exc_info:
        generate_settings()

    assert str(exc_info.value) == "settings.yaml required"


def test_pydantic_sanity_check_file(tmp_path, monkeypatch):
    # region Docs
    """
    Prompting Pydantic to error on a broken yaml.

    Notes: creates file in fake dir

    Inputs:
        mock_yaml (str): invalid yaml

    Expected result: (ValidationError): Pydantic panic
    """
    # endregion
    mock_yaml = """
    local: "STRING"
    """

    d = tmp_path / "settings.yaml"
    d.write_text(mock_yaml, encoding="UTF-8")

    monkeypatch.chdir(tmp_path)

    with pytest.raises(ValidationError) as exc_info:
        generate_settings()

    assert exc_info.type == ValidationError


def test_pydantic_sanity_check_dict():
    # region Docs
    """
    Prompting Pydantic to error on a broken yaml.

    Notes: creates file in fake dir

    Inputs:
        mock_yaml (str): invalid yaml

    Expected result: (ValidationError): Pydantic panic
    """
    # endregion

    yaml_supplied = {
        "local": "String",
    }

    with pytest.raises(ValidationError) as exc_info:
        generate_settings(yaml_supplied)

    assert exc_info.type == ValidationError
