from pathlib import Path

import pytest
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from streamlit.testing.v1 import AppTest

from config.settings import get_settings
from database.connection import database_session, get_engine
from database.demo_data import SYNTHETIC_PROJECT_NAME, seed_evaluator_demo
from database.repository import get_project_record, list_project_records


def _clear_cached_runtime() -> None:
    get_engine.cache_clear()
    get_settings.cache_clear()


def test_evaluator_demo_ignores_configured_database_and_blocks_writes(
    monkeypatch, tmp_path: Path
) -> None:
    configured_database = tmp_path / "must-not-be-created.db"
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("DEMO_MODE", "true")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{configured_database}")
    _clear_cached_runtime()

    engine = get_engine()
    try:
        seed_evaluator_demo(engine)
        assert engine.url.database is None
        assert not configured_database.exists()

        with engine.connect() as connection:
            assert connection.exec_driver_sql("PRAGMA query_only").scalar_one() == 1

        with database_session(engine) as session:
            projects = list_project_records(session)
            sample = get_project_record(session, projects[0]["id"])
        assert len(projects) == 1
        assert projects[0]["name"] == SYNTHETIC_PROJECT_NAME
        assert sample is not None
        report = sample["reports"][0]["payload"]
        assert report["notice"].startswith("Synthetic evaluator sample only")
        assert report["manually_entered_sources"] == []
        assert report["founder_provided_information"][0]["provenance"].startswith(
            "Synthetic demonstration data"
        )
        assert report["competitor_comparison"][0]["provenance"].startswith(
            "Synthetic fictional example"
        )

        with pytest.raises(OperationalError, match="readonly"):
            with database_session(engine) as session:
                session.execute(text("CREATE TABLE forbidden_write (id INTEGER)"))
    finally:
        engine.dispose()
        _clear_cached_runtime()


def test_public_evaluator_ui_is_read_only_and_discloses_synthetic_data(
    monkeypatch, tmp_path: Path
) -> None:
    configured_database = tmp_path / "ui-must-not-be-created.db"
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("DEMO_MODE", "true")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{configured_database}")
    _clear_cached_runtime()
    app_path = Path(__file__).resolve().parents[1] / "app.py"

    try:
        app = AppTest.from_file(str(app_path), default_timeout=20).run()
        assert not app.exception
        assert any(
            "fictional synthetic sample data only" in item.value
            for item in app.warning
        )
        assert any(
            item.value == SYNTHETIC_PROJECT_NAME for item in app.subheader
        )
        assert not configured_database.exists()

        app.radio(key="page_nav").set_value("Create Project").run()
        assert not app.exception
        assert any("Project creation is disabled" in item.value for item in app.info)
        assert not any(item.label == "Project name *" for item in app.text_input)

        app.radio(key="page_nav").set_value("Project Workspace").run()
        assert not app.exception
        assert all(item.disabled for item in app.text_input)
        assert all(item.disabled for item in app.text_area)
        mutation_labels = {
            "Save changes",
            "Add competitor or alternative",
            "Save source note",
            "Generate and save report",
            "Remove entry",
        }
        assert all(
            item.disabled for item in app.button if item.label in mutation_labels
        )
        assert app.get("download_button")
    finally:
        get_engine().dispose()
        get_engine.cache_clear()
        get_settings.cache_clear()


def test_production_without_demo_mode_stops_before_database_initialization(
    monkeypatch, tmp_path: Path
) -> None:
    configured_database = tmp_path / "production-must-not-start.db"
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("DEMO_MODE", "false")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{configured_database}")
    _clear_cached_runtime()
    app_path = Path(__file__).resolve().parents[1] / "app.py"

    try:
        app = AppTest.from_file(str(app_path), default_timeout=20).run()
        assert any(
            "Production startup is disabled" in item.value for item in app.error
        )
        assert not configured_database.exists()
    finally:
        get_engine.cache_clear()
        get_settings.cache_clear()
