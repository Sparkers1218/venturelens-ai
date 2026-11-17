from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from functools import lru_cache
from threading import RLock

from sqlalchemy import Engine, create_engine, event, inspect, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
import streamlit as st

from config.settings import get_settings
from database.models import Base


SESSION_ENGINE_KEY = "_demo_session_engine"
_initialization_lock = RLock()
_initialized_engines: set[Engine] = set()


def create_database_engine(database_url: str) -> Engine:
    connect_args = (
        {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    )
    engine_options: dict[str, object] = {"connect_args": connect_args}
    if database_url in {"sqlite://", "sqlite:///:memory:"}:
        engine_options["poolclass"] = StaticPool
    engine = create_engine(database_url, **engine_options)

    if database_url.startswith("sqlite"):
        @event.listens_for(engine, "connect")
        def enable_sqlite_foreign_keys(connection, _record) -> None:
            del _record
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


def get_session_engine() -> Engine | None:
    """Return the active Streamlit session's in-memory SQLite engine if present."""
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is not None and SESSION_ENGINE_KEY in st.session_state:
            engine = st.session_state[SESSION_ENGINE_KEY]
            if isinstance(engine, Engine):
                return engine
    except Exception:
        pass
    return None


def get_or_create_session_engine() -> Engine:
    """Get or create an isolated in-memory SQLite engine for the current session."""
    session_engine = get_session_engine()
    if session_engine is not None:
        return session_engine

    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is not None:
            engine = create_database_engine("sqlite://")
            st.session_state[SESSION_ENGINE_KEY] = engine
            return engine
    except Exception:
        pass

    return _get_fallback_demo_engine()


@lru_cache(maxsize=1)
def _get_fallback_demo_engine() -> Engine:
    return create_database_engine("sqlite://")


@lru_cache(maxsize=1)
def _get_read_only_demo_engine() -> Engine:
    return create_database_engine("sqlite://")


@lru_cache(maxsize=1)
def _get_configured_engine(database_url: str) -> Engine:
    return create_database_engine(database_url)


def get_engine() -> Engine:
    settings = get_settings()
    if settings.demo_mode:
        if settings.demo_writable:
            return get_or_create_session_engine()
        return _get_read_only_demo_engine()
    return _get_configured_engine(settings.database_url)


def _clear_engine_cache() -> None:
    _get_configured_engine.cache_clear()
    _get_read_only_demo_engine.cache_clear()
    _get_fallback_demo_engine.cache_clear()
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is not None:
            st.session_state.pop(SESSION_ENGINE_KEY, None)
    except Exception:
        pass
    with _initialization_lock:
        _initialized_engines.clear()


get_engine.cache_clear = _clear_engine_cache  # type: ignore[attr-defined]


def enable_read_only_sqlite(engine: Engine) -> None:
    if engine.dialect.name != "sqlite" or engine.url.database not in {
        None,
        "",
        ":memory:",
    }:
        raise ValueError(
            "Read-only evaluator mode requires an in-memory SQLite database."
        )

    with engine.connect() as connection:
        connection.exec_driver_sql("PRAGMA query_only = ON")


def initialize_database(engine: Engine | None = None) -> None:
    target_engine = engine or get_engine()
    with _initialization_lock:
        if target_engine in _initialized_engines:
            return
        Base.metadata.create_all(target_engine)
        _upgrade_existing_schema(target_engine)
        _initialized_engines.add(target_engine)


def _upgrade_existing_schema(engine: Engine) -> None:
    additions = {
        "projects": {
            "business_model": "TEXT NOT NULL DEFAULT ''",
        },
        "competitors": {
            "target_audience": "TEXT NOT NULL DEFAULT ''",
            "pricing": "TEXT NOT NULL DEFAULT ''",
            "differentiation_notes": "TEXT NOT NULL DEFAULT ''",
        },
        "research_sources": {
            "provenance": "VARCHAR(40) NOT NULL DEFAULT 'manual_unverified'",
        },
    }
    with engine.begin() as connection:
        inspector = inspect(connection)
        for table_name, columns in additions.items():
            if not inspector.has_table(table_name):
                continue
            existing_columns = {
                column["name"] for column in inspector.get_columns(table_name)
            }
            for column_name, declaration in columns.items():
                if column_name not in existing_columns:
                    connection.execute(
                        text(
                            f"ALTER TABLE {table_name} ADD COLUMN "
                            f"{column_name} {declaration}"
                        )
                    )


@contextmanager
def database_session(engine: Engine | None = None) -> Generator[Session, None, None]:
    factory = sessionmaker(bind=engine or get_engine(), expire_on_commit=False)
    with factory.begin() as session:
        yield session
