from pathlib import Path

import pytest
import streamlit as st
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
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("DEMO_MODE", raising=False)
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{configured_database}")
    monkeypatch.setattr(
        st,
        "secrets",
        {"APP_ENV": "production", "DEMO_MODE": True},
    )
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
        assert any("Spark2Scale · PS49" in item.value for item in app.caption)
        assert not configured_database.exists()

        app.radio(key="vl_theme").set_value("Dark").run()
        assert not app.exception
        assert app.radio(key="vl_theme").value == "Dark"
        app.radio(key="page_nav").set_value("My Projects").run()
        assert app.radio(key="vl_theme").value == "Dark"
        app.radio(key="vl_theme").set_value("Light").run()
        assert app.radio(key="vl_theme").value == "Light"

        app.radio(key="page_nav").set_value("Create Project").run()
        assert not app.exception
        assert any("Project creation is disabled" in item.value for item in app.info)
        assert not any(item.label == "Project name *" for item in app.text_input)

        app.radio(key="page_nav").set_value("Project Workspace").run()
        assert not app.exception
        assert any(item.value == "Project Workspace" for item in app.title)
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
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("DEMO_MODE", raising=False)
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{configured_database}")
    monkeypatch.setattr(st, "secrets", {"APP_ENV": "production"})
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


def test_writable_evaluator_demo_mode_ui_journey(
    monkeypatch, tmp_path: Path
) -> None:
    configured_database = tmp_path / "writable-must-not-be-created.db"
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("DEMO_MODE", raising=False)
    monkeypatch.delenv("DEMO_WRITABLE", raising=False)
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{configured_database}")
    monkeypatch.setattr(
        st,
        "secrets",
        {"APP_ENV": "production", "DEMO_MODE": True, "DEMO_WRITABLE": True},
    )
    _clear_cached_runtime()
    app_path = Path(__file__).resolve().parents[1] / "app.py"

    try:
        app = AppTest.from_file(str(app_path), default_timeout=20).run()
        assert not app.exception
        assert any("PUBLIC EVALUATOR WORKSPACE" in item.value for item in app.warning)
        assert any("Isolated per-session evaluator demo" in item.value for item in app.caption)

        # Navigate to Create Project
        app.radio(key="page_nav").set_value("Create Project").run()
        assert not app.exception
        assert any(item.value == "Create Project" for item in app.title)

        # Form fields must be enabled
        name_input = next(item for item in app.text_input if item.label == "Project name *")
        assert not name_input.disabled
        name_input.set_value("Evaluator Innovation Project")

        problem_input = next(item for item in app.text_area if item.label == "Problem statement")
        assert not problem_input.disabled
        problem_input.set_value("Early stage startup founders struggle with manual validation.")

        solution_input = next(item for item in app.text_area if item.label == "Proposed solution")
        assert not solution_input.disabled
        solution_input.set_value("A structured intelligence tool for fast idea scoring.")

        customers_input = next(item for item in app.text_area if item.label == "Target customers")
        assert not customers_input.disabled
        customers_input.set_value("First-time founders and startup accelerator evaluators.")

        # Save project
        app.button(key="FormSubmitter:create_project_form-Save project").click().run()
        assert not app.exception
        assert "selected_project_id" in app.session_state
        project_id = app.session_state["selected_project_id"]

        # Project Workspace should now show the new project
        assert any(item.value == "Project Workspace" for item in app.title)
        assert any(item.value == "Evaluator Innovation Project" for item in app.text_input)

        # Form fields in workspace must NOT be disabled
        save_btn = next((item for item in app.button if item.label == "Save changes"), None)
        assert save_btn is not None
        assert not save_btn.disabled

        # Add competitor
        comp_name = next(item for item in app.text_input if item.label == "Name *")
        assert not comp_name.disabled
        comp_name.set_value("Traditional Venture Studio")
        app.button(
            key=f"FormSubmitter:competitor_form_{project_id}-Add competitor or alternative"
        ).click().run()
        assert not app.exception
        assert any("Traditional Venture Studio" in item.value for item in app.text)

        # Generate report
        gen_report_btn = next(item for item in app.button if item.label == "Generate and save report")
        assert not gen_report_btn.disabled
        gen_report_btn.click().run()
        assert not app.exception
        assert any(item.label == "Download report (JSON)" for item in app.get("download_button"))

        # Navigate to Analysis Report page and confirm it displays
        app.radio(key="page_nav").set_value("Analysis Report").run()
        assert not app.exception
        assert any(item.value == "Analysis Report" for item in app.title)
        assert any(item.label == "Download report (JSON)" for item in app.get("download_button"))

        # Configured database must NEVER be created on disk
        assert not configured_database.exists()
    finally:
        _clear_cached_runtime()


def test_writable_evaluator_demo_mode_session_isolation(
    monkeypatch, tmp_path: Path
) -> None:
    configured_database = tmp_path / "isolation-must-not-be-created.db"
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("DEMO_MODE", raising=False)
    monkeypatch.delenv("DEMO_WRITABLE", raising=False)
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{configured_database}")
    monkeypatch.setattr(
        st,
        "secrets",
        {"APP_ENV": "production", "DEMO_MODE": True, "DEMO_WRITABLE": True},
    )
    _clear_cached_runtime()
    app_path = Path(__file__).resolve().parents[1] / "app.py"

    try:
        # Evaluator Session A
        app_a = AppTest.from_file(str(app_path), default_timeout=20).run()
        app_a.radio(key="page_nav").set_value("Create Project").run()
        name_a = next(item for item in app_a.text_input if item.label == "Project name *")
        name_a.set_value("Founder A Private Project")
        app_a.button(key="FormSubmitter:create_project_form-Save project").click().run()
        assert not app_a.exception
        assert "selected_project_id" in app_a.session_state

        # Evaluator Session B
        app_b = AppTest.from_file(str(app_path), default_timeout=20).run()
        app_b.radio(key="page_nav").set_value("My Projects").run()

        # Session B must NOT see Session A's project
        subheaders_b = [item.value for item in app_b.subheader]
        assert "Founder A Private Project" not in subheaders_b
        assert SYNTHETIC_PROJECT_NAME in subheaders_b

        # Session B creates its own project
        app_b.radio(key="page_nav").set_value("Create Project").run()
        name_b = next(item for item in app_b.text_input if item.label == "Project name *")
        name_b.set_value("Founder B Private Project")
        app_b.button(key="FormSubmitter:create_project_form-Save project").click().run()
        assert not app_b.exception
        assert "selected_project_id" in app_b.session_state

        # Session A must NOT see Session B's project
        app_a.radio(key="page_nav").set_value("My Projects").run()
        subheaders_a = [item.value for item in app_a.subheader]
        assert "Founder B Private Project" not in subheaders_a
        assert "Founder A Private Project" in subheaders_a

        assert not configured_database.exists()
    finally:
        _clear_cached_runtime()
