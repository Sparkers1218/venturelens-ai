from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from functools import lru_cache
from threading import RLock

from sqlalchemy import Engine, create_engine, event, inspect, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from config.settings import get_settings
from database.models import Base


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


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    settings = get_settings()
    database_url = "sqlite://" if settings.demo_mode else settings.database_url
    return create_database_engine(database_url)


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
