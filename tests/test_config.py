import streamlit as st

from config.settings import Settings


SETTING_ENV_VARS = (
    "APP_NAME",
    "APP_ENV",
    "DEBUG",
    "LOG_LEVEL",
    "DATABASE_URL",
    "DEMO_MODE",
    "DEMO_WRITABLE",
)


def test_settings_have_safe_defaults(monkeypatch) -> None:
    for name in SETTING_ENV_VARS:
        monkeypatch.delenv(name, raising=False)

    settings = Settings(_env_file=None)

    assert settings.app_name == "VentureLens AI"
    assert settings.app_env == "development"
    assert settings.debug is False
    assert settings.log_level == "INFO"
    assert settings.database_url == "sqlite:///./venturelens.db"
    assert settings.demo_mode is False
    assert settings.demo_writable is False


def test_settings_read_environment_variables(monkeypatch) -> None:
    monkeypatch.setenv("APP_NAME", "Test VentureLens")
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://user:password@localhost:5432/venturelens",
    )
    monkeypatch.setenv("DEMO_MODE", "true")
    monkeypatch.setattr(
        st,
        "secrets",
        {
            "APP_NAME": "Cloud VentureLens",
            "APP_ENV": "production",
            "DEMO_MODE": False,
        },
    )

    settings = Settings(_env_file=None)

    assert settings.app_name == "Test VentureLens"
    assert settings.app_env == "test"
    assert settings.debug is True
    assert settings.log_level == "DEBUG"
    assert settings.database_url == (
        "postgresql+psycopg://user:password@localhost:5432/venturelens"
    )
    assert settings.demo_mode is True


def test_settings_read_streamlit_cloud_secrets(monkeypatch) -> None:
    for name in SETTING_ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(
        st,
        "secrets",
        {"APP_ENV": "production", "DEMO_MODE": True},
    )

    settings = Settings(_env_file=None)

    assert settings.app_env == "production"
    assert settings.demo_mode is True


def test_production_secret_without_demo_secret_keeps_demo_disabled(
    monkeypatch,
) -> None:
    for name in SETTING_ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(st, "secrets", {"APP_ENV": "production"})

    settings = Settings(_env_file=None)

    assert settings.app_env == "production"
    assert settings.demo_mode is False
    assert settings.demo_writable is False


def test_settings_read_demo_writable_secret(monkeypatch) -> None:
    for name in SETTING_ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(
        st,
        "secrets",
        {"APP_ENV": "production", "DEMO_MODE": True, "DEMO_WRITABLE": True},
    )

    settings = Settings(_env_file=None)

    assert settings.app_env == "production"
    assert settings.demo_mode is True
    assert settings.demo_writable is True
