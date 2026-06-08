# region Docs
"""
[Module](app/settings.py)

Notes: Order is important since this is a global operation
- Missing File
- Incorrect File
- ...

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


from app.settings import get_settings, init_test_settings, Settings


@pytest.fixture(name="_fake_env_vars")
def monkeypatch_envs(monkeypatch):
    # region Docs
    """
    Sets up fake env variables for use by tests

    Args:
        monkeypatch: method for faking attributes and actions
    """
    # endregion

    monkeypatch.setenv("API_ADDR", "https://api.mock.com")
    monkeypatch.setenv("API_PORT", "123")
    monkeypatch.setenv("FIELD_ENCRYPTION_KEY", "fake_key")
    monkeypatch.setenv("MONGODB_URI", "mongobd://mock.uri")


def test_settings_file_missing(tmp_path, monkeypatch, _fake_env_vars):
    # region Docs
    """
    Tests if settings file is missing

    Notes: tests in a fake directory.

    Expected result: (FileNotFoundError): with message about it being required
    """
    # endregion

    monkeypatch.chdir(tmp_path)

    with pytest.raises(FileNotFoundError) as exc_info:
        get_settings()

    assert str(exc_info.value) == "settings.yaml required"


def test_pydantic_sanity_check_file(tmp_path, monkeypatch, _fake_env_vars):
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
        get_settings()

    assert exc_info.type == ValidationError


def test_generate_settings_success(tmp_path, monkeypatch, _fake_env_vars):
    # region Docs
    """
    Valid YAML content

    Notes: creates file in a fake dir

    Inputs:
        mock_yaml (str): acceptable yaml file

    Expected result: (Settings): Correct settings object
    """
    # endregion

    mock_yaml = """
local: false
    """

    d = tmp_path / "settings.yaml"
    d.write_text(mock_yaml, encoding="UTF-8")

    monkeypatch.chdir(tmp_path)

    settings = get_settings()

    assert isinstance(settings, Settings)

    assert not settings.config.local
    assert settings.secrets.api_addr == "https://api.mock.com"
    assert settings.secrets.api_port == "123"
    assert settings.secrets.field_encryption_key == "fake_key"
    assert settings.secrets.mongodb_uri == "mongobd://mock.uri"


def test_generate_settings_from_supplied(_fake_env_vars):
    # region Docs
    """
    Checks if supplied settings are used when provided

    Notes: Any nuances or references.

    Inputs:
        yaml_supplied (dict): mock settings from code

    Expected result: (Settings): as described by code
    """
    # endregion

    yaml_supplied = {
        "local": False,
    }

    settings = init_test_settings(yaml_supplied)

    assert isinstance(settings, Settings)
    assert not settings.config.local
    assert settings.secrets.api_addr == "https://api.mock.com"


def test_pydantic_sanity_check_dict(_fake_env_vars):
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
        init_test_settings(yaml_supplied)

    assert exc_info.type == ValidationError
