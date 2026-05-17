# region Docs
"""
[Module](app/settings.py)

Notes:

Tests:
    generate_settings_success
    settings_file_missing
    pydantic_sanity_check

"""
# endregion

from pydantic import ValidationError
import pytest


from app.settings import generate_settings, Settings


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
        "db_file": {str(tmp_path / "mock.db")}
    """

    d = tmp_path / "settings.yaml"
    d.write_text(mock_yaml, encoding="UTF-8")

    monkeypatch.chdir(tmp_path)

    settings = generate_settings()

    assert isinstance(settings, Settings)
    assert not settings.local
    assert settings.api_addr == "https://api.mock.com"
    assert settings.api_port == "123"
    assert settings.db_file == str(tmp_path / "mock.db")


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


def test_pydantic_sanity_check(tmp_path, monkeypatch):
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
