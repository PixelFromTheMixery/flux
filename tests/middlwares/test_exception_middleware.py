import pytest
from fastapi import Request

from app.middlewares.exception_middleware import ExceptionMiddleware
from app.settings import generate_settings


@pytest.fixture(name="middleware_fixture")
def mock_settings(client, monkeypatch):
    monkeypatch.setattr(
        "app.middlewares.exception_middleware.generate_settings",
        lambda: generate_settings({"local": True}),
    )
    middleware = ExceptionMiddleware(client)

    return middleware


def test_exception_parser(middleware_fixture):

    with pytest.raises(Exception) as exc_info:
        middleware_fixture.request_lobby(
            Exception(type="FakeException", message="Fake Exception"), ()
        )
    assert exc_info.type == "FakeException"
