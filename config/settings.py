from functools import lru_cache
from typing import Any, Literal

import streamlit as st
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from streamlit.errors import StreamlitSecretNotFoundError


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "VentureLens AI"
    app_env: Literal["development", "test", "production"] = "development"
    debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    database_url: str = "sqlite:///./venturelens.db"
    demo_mode: bool = False

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[Any, ...]:
        def streamlit_secrets_settings() -> dict[str, Any]:
            return _streamlit_secrets_settings(settings_cls)

        return (
            init_settings,
            env_settings,
            dotenv_settings,
            streamlit_secrets_settings,
            file_secret_settings,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


def _streamlit_secrets_settings(
    settings_cls: type[BaseSettings],
) -> dict[str, Any]:
    try:
        secrets = st.secrets
        values: dict[str, Any] = {}
        for field_name in settings_cls.model_fields:
            for key in (field_name.upper(), field_name):
                if key in secrets:
                    values[field_name] = secrets[key]
                    break
    except StreamlitSecretNotFoundError as error:
        if error.error_id != "no-secrets-found":
            raise
        return {}
    return values
