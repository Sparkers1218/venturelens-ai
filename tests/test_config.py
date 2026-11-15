from config.settings import Settings


def test_settings_have_safe_defaults(monkeypatch) -> None:
    for name in ("APP_NAME", "APP_ENV", "DEBUG", "LOG_LEVEL", "DATABASE_URL"):
        monkeypatch.delenv(name, raising=False)

    settings = Settings(_env_file=None)

    assert settings.app_name == "VentureLens AI"
    assert settings.app_env == "development"
    assert settings.debug is False
    assert settings.log_level == "INFO"
    assert settings.database_url == "sqlite:///./venturelens.db"


def test_settings_read_environment_variables(monkeypatch) -> None:
    monkeypatch.setenv("APP_NAME", "Test VentureLens")
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://user:password@localhost:5432/venturelens",
    )

    settings = Settings(_env_file=None)

    assert settings.app_name == "Test VentureLens"
    assert settings.app_env == "test"
    assert settings.debug is True
    assert settings.log_level == "DEBUG"
    assert settings.database_url == (
        "postgresql+psycopg://user:password@localhost:5432/venturelens"
    )
