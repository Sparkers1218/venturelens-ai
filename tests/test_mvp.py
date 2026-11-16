from pathlib import Path

import pytest
from pydantic import ValidationError
from sqlalchemy.engine import URL
from sqlalchemy import inspect, text
from streamlit.testing.v1 import AppTest

from core.analysis import build_rule_based_report
from core.schemas import CompetitorInput, ProjectInput, ResearchSourceInput
from database.connection import (
    create_database_engine,
    database_session,
    initialize_database,
)
from database.repository import (
    add_competitor,
    add_source,
    create_project,
    create_report,
    delete_project,
    get_project,
    get_project_record,
    remove_competitor,
    remove_source,
    update_project,
)
from database.models import AnalysisReport, Competitor, ResearchSource


@pytest.fixture
def engine():
    test_engine = create_database_engine("sqlite://")
    initialize_database(test_engine)
    yield test_engine
    test_engine.dispose()


def test_inputs_validate_lengths_urls_and_source_details() -> None:
    with pytest.raises(ValidationError):
        ProjectInput(name=" ")
    with pytest.raises(ValidationError):
        CompetitorInput(name="Competitor", source_url="javascript:alert(1)")
    with pytest.raises(ValidationError):
        ResearchSourceInput(title="Empty source")

    source = ResearchSourceInput(
        title="Interview notes",
        summary="Founder-provided interview summary.",
        source_url="https://example.com/interview",
    )
    assert source.source_url.startswith("https://")


def test_projects_sources_competitors_and_reports_persist_and_scope_deletes(engine) -> None:
    project_data = ProjectInput(
        name="Idea Atlas",
        problem_statement="Teams struggle to compare local service providers.",
        proposed_solution="A transparent comparison workspace.",
        target_customers="Small business owners",
        industry="Software",
        geography="North America",
        business_model="Subscription paid by small business teams.",
    )
    with database_session(engine) as session:
        project = create_project(session, project_data)
        project_id = project.id
        competitor = add_competitor(
            session,
            project,
            CompetitorInput(
                name="Example alternative",
                description="Founder-provided note.",
                source_url="https://example.com/alternative",
                target_audience="Small business owners",
                pricing="Founder-entered estimate",
                differentiation_notes="Potentially easier onboarding; unverified.",
            ),
        )
        competitor_id = competitor.id
        source = add_source(
            session,
            project,
            ResearchSourceInput(
                title="Manual interview notes",
                summary="Two founders described the existing workaround.",
            ),
        )
        source_id = source.id
        report_payload = build_rule_based_report(
            {
                "name": project.name,
                "problem_statement": project.problem_statement,
                "proposed_solution": project.proposed_solution,
                "target_customers": project.target_customers,
                "industry": project.industry,
                "geography": project.geography,
                "business_model": project.business_model,
            },
            [
                {
                    "name": competitor.name,
                    "description": competitor.description,
                    "source_url": competitor.source_url,
                    "target_audience": competitor.target_audience,
                    "pricing": competitor.pricing,
                    "differentiation_notes": competitor.differentiation_notes,
                }
            ],
            [
                {
                    "title": source.title,
                    "summary": source.summary,
                    "source_url": source.source_url,
                    "publisher": source.publisher,
                    "provenance": source.provenance,
                }
            ],
        )
        report = create_report(
            session,
            project,
            "Rule-based demo analysis (not AI-generated)",
            report_payload,
        )
        report_id = report.id
        unrelated_project = create_project(
            session, ProjectInput(name="Unrelated project")
        )
        unrelated_project_id = unrelated_project.id

    with database_session(engine) as session:
        saved = get_project_record(session, project_id)
        assert saved is not None
        assert saved["name"] == "Idea Atlas"
        assert saved["business_model"] == (
            "Subscription paid by small business teams."
        )
        assert saved["competitors"][0]["id"] == competitor_id
        assert saved["competitors"][0]["target_audience"] == "Small business owners"
        assert saved["competitors"][0]["pricing"] == "Founder-entered estimate"
        assert saved["competitors"][0]["differentiation_notes"].startswith(
            "Potentially easier"
        )
        assert saved["sources"][0]["id"] == source_id
        assert saved["reports"][0]["id"] == report_id
        assert saved["analysis_status"] == "Report saved"
        assert "not AI-generated" in saved["reports"][0]["engine_label"]
        assert saved["reports"][0]["payload"]["manually_entered_sources"][0][
            "provenance"
        ].startswith("Manually entered")
        analysis = saved["reports"][0]["payload"]
        assert analysis["schema_version"] == 2
        assert len(analysis["assessment_scores"]) == 7
        assert all(
            0 <= score["score"] <= score["maximum"] == 3
            for score in analysis["assessment_scores"]
        )
        assert analysis["competitor_comparison"][0]["pricing"] == (
            "Founder-entered estimate"
        )
        assert analysis["evidence_and_research_references"][0]["provenance"].startswith(
            "Manually entered"
        )
        assert {"High", "Medium", "Low"} == set(analysis["risk_distribution"])
        assert analysis["validation_experiments"][0]["priority_score"] == 2

        assert remove_competitor(session, unrelated_project_id, competitor_id) is False
        assert remove_source(session, unrelated_project_id, source_id) is False
        assert remove_competitor(session, project_id, competitor_id) is True
        assert remove_source(session, project_id, source_id) is True

    with database_session(engine) as session:
        saved = get_project_record(session, project_id)
        assert saved is not None
        assert saved["competitors"] == []
        assert saved["sources"] == []
        assert saved["analysis_status"] == "Inputs changed since last report"
        project = get_project(session, project_id)
        assert project is not None
        update_project(
            session,
            project,
            ProjectInput(
                name="Idea Atlas Revised",
                business_model="Annual subscription.",
            ),
        )

    with database_session(engine) as session:
        saved = get_project_record(session, project_id)
        assert saved is not None
        assert saved["name"] == "Idea Atlas Revised"
        assert saved["business_model"] == "Annual subscription."
        project = get_project(session, project_id)
        assert project is not None
        delete_project(session, project)

    with database_session(engine) as session:
        assert get_project(session, project_id) is None


def test_rule_based_report_labels_unknowns_instead_of_claiming_research() -> None:
    report = build_rule_based_report(
        {"name": "Idea Atlas", "problem_statement": "A founder-described problem"},
        [],
        [],
    )

    assert report["report_type"] == "Rule-based demo analysis (not AI-generated)"
    assert report["founder_provided_information"][0]["provenance"].startswith(
        "User-provided"
    )
    assert report["ai_interpretations"].startswith("None.")
    assert report["manually_entered_sources"] == []
    assert any(
        "does not mean competitors are absent" in risk["detail"]
        for risk in report["risks_and_missing_information"]
    )
    assert report["input_completeness"]["meaning"].startswith("Input completeness only")
    assert report["validation_experiments"][0]["priority"] == "High"
    assert report["validation_experiments"][0]["priority_score"] == 3


def test_project_delete_cascades_to_related_records(engine) -> None:
    with database_session(engine) as session:
        project = create_project(session, ProjectInput(name="Cascade project"))
        project_id = project.id
        competitor = add_competitor(
            session, project, CompetitorInput(name="Manual competitor")
        )
        source = add_source(
            session,
            project,
            ResearchSourceInput(title="Source", summary="Manual note"),
        )
        report = create_report(session, project, "rule-based", {"notice": "demo"})
        related_ids = (competitor.id, source.id, report.id)
        delete_project(session, project)

    with database_session(engine) as session:
        assert get_project(session, project_id) is None
        assert session.get(Competitor, related_ids[0]) is None
        assert session.get(ResearchSource, related_ids[1]) is None
        assert session.get(AnalysisReport, related_ids[2]) is None


def test_project_and_report_survive_database_engine_restart(tmp_path: Path) -> None:
    database_url = str(URL.create("sqlite", database=str(tmp_path / "restart.db")))
    first_engine = create_database_engine(database_url)
    initialize_database(first_engine)
    with database_session(first_engine) as session:
        project = create_project(
            session,
            ProjectInput(name="Persistent idea", business_model="Service fee."),
        )
        project_id = project.id
        report_payload = build_rule_based_report(
            {
                "name": project.name,
                "business_model": project.business_model,
            },
            [],
            [],
        )
        create_report(
            session,
            project,
            "Rule-based demo analysis (not AI-generated)",
            report_payload,
        )
    first_engine.dispose()

    restarted_engine = create_database_engine(database_url)
    try:
        initialize_database(restarted_engine)
        with database_session(restarted_engine) as session:
            saved = get_project_record(session, project_id)
        assert saved is not None
        assert saved["business_model"] == "Service fee."
        assert len(saved["reports"]) == 1
        assert saved["reports"][0]["payload"]["schema_version"] == 2
    finally:
        restarted_engine.dispose()


def test_initialize_database_adds_new_fields_to_existing_demo_schema() -> None:
    engine = create_database_engine("sqlite://")
    try:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "CREATE TABLE projects (id VARCHAR(36) PRIMARY KEY, "
                    "name VARCHAR(120) NOT NULL, problem_statement TEXT NOT NULL "
                    "DEFAULT '', proposed_solution TEXT NOT NULL DEFAULT '', "
                    "target_customers TEXT NOT NULL DEFAULT '', "
                    "industry VARCHAR(120) NOT NULL DEFAULT '', "
                    "geography VARCHAR(160) NOT NULL DEFAULT '', "
                    "created_at DATETIME NOT NULL, updated_at DATETIME NOT NULL)"
                )
            )
            connection.execute(
                text(
                    "CREATE TABLE competitors (id VARCHAR(36) PRIMARY KEY, "
                    "project_id VARCHAR(36) NOT NULL, name VARCHAR(160) NOT NULL, "
                    "description TEXT NOT NULL DEFAULT '', "
                    "source_url VARCHAR(2048) NOT NULL DEFAULT '', "
                    "created_at DATETIME NOT NULL)"
                )
            )
            connection.execute(
                text(
                    "CREATE TABLE research_sources (id VARCHAR(36) PRIMARY KEY, "
                    "project_id VARCHAR(36) NOT NULL, title VARCHAR(200) NOT NULL, "
                    "publisher VARCHAR(200) NOT NULL DEFAULT '', "
                    "source_url VARCHAR(2048) NOT NULL DEFAULT '', "
                    "summary TEXT NOT NULL DEFAULT '', created_at DATETIME NOT NULL)"
                )
            )
            connection.execute(
                text(
                    "INSERT INTO projects "
                    "(id, name, problem_statement, proposed_solution, "
                    "target_customers, industry, geography, created_at, updated_at) "
                    "VALUES ('legacy-project', 'Legacy idea', '', '', '', '', '', "
                    "'2026-01-01 00:00:00', '2026-01-01 00:00:00')"
                )
            )
            connection.execute(
                text(
                    "INSERT INTO competitors "
                    "(id, project_id, name, description, source_url, created_at) "
                    "VALUES ('legacy-competitor', 'legacy-project', 'Old competitor', "
                    "'Old note', '', '2026-01-01 00:00:00')"
                )
            )
            connection.execute(
                text(
                    "INSERT INTO research_sources "
                    "(id, project_id, title, publisher, source_url, summary, created_at) "
                    "VALUES ('legacy-source', 'legacy-project', 'Old source', '', '', "
                    "'Old notes', '2026-01-01 00:00:00')"
                )
            )

        initialize_database(engine)
        initialize_database(engine)
        inspector = inspect(engine)
        assert "business_model" in {
            column["name"] for column in inspector.get_columns("projects")
        }
        assert {
            "target_audience",
            "pricing",
            "differentiation_notes",
        } <= {column["name"] for column in inspector.get_columns("competitors")}
        assert "provenance" in {
            column["name"]
            for column in inspector.get_columns("research_sources")
        }
        with database_session(engine) as session:
            legacy_project = get_project_record(session, "legacy-project")
        assert legacy_project is not None
        assert legacy_project["business_model"] == ""
        assert legacy_project["competitors"][0]["target_audience"] == ""
        assert legacy_project["competitors"][0]["pricing"] == ""
        assert legacy_project["sources"][0]["provenance"] == "manual_unverified"
    finally:
        engine.dispose()


def test_streamlit_demo_workflow_saves_a_reopenable_report(
    monkeypatch, tmp_path: Path
) -> None:
    from config.settings import get_settings
    from database.connection import database_session, get_engine
    from database.repository import get_project_record

    db_path = tmp_path / "streamlit-test.db"
    monkeypatch.setenv(
        "DATABASE_URL", str(URL.create("sqlite", database=str(db_path)))
    )
    get_settings.cache_clear()
    get_engine.cache_clear()
    app_path = Path(__file__).resolve().parents[1] / "app.py"

    app = AppTest.from_file(str(app_path), default_timeout=20).run()
    assert not app.exception
    assert app.radio(key="vl_theme").value == "Light"
    app.radio(key="vl_theme").set_value("Dark").run()
    assert not app.exception
    assert app.session_state["vl_theme"] == "Dark"
    metric_values = {item.label: item.value for item in app.metric}
    assert metric_values["Total projects"] == "0"
    assert metric_values["Completed analyses"] == "0"
    for page in (
        "My Projects",
        "Competitor Insights",
        "Research",
        "Analysis Report",
        "Notifications",
        "Profile",
        "Settings",
    ):
        app.radio(key="page_nav").set_value(page).run()
        assert not app.exception, f"Empty-state navigation to {page} failed"
    app.radio(key="page_nav").set_value("Create Project").run()
    next(item for item in app.text_input if item.label == "Project name *").set_value(
        "UI workflow project"
    )
    next(item for item in app.text_area if item.label == "Problem statement").set_value(
        "Teams need a clearer way to compare service options."
    )
    next(
        item for item in app.text_area if item.label == "Business model (optional)"
    ).set_value("Monthly subscription paid by local businesses.")
    app.button(key="FormSubmitter:create_project_form-Save project").click().run()
    assert not app.exception
    project_id = app.session_state["selected_project_id"]

    next(item for item in app.text_input if item.label == "Name *").set_value(
        "Founder-listed alternative"
    )
    next(
        item for item in app.text_area if item.label == "Target audience (optional)"
    ).set_value("Local businesses")
    next(item for item in app.text_input if item.label == "Pricing (optional)").set_value(
        "Manually noted; not verified"
    )
    next(
        item
        for item in app.text_area
        if item.label == "Differentiation notes (optional)"
    ).set_value("Founder thinks setup may be simpler.")
    app.button(
        key=f"FormSubmitter:competitor_form_{project_id}-Add competitor or alternative"
    ).click().run()
    assert not app.exception

    next(item for item in app.text_input if item.label == "Source title *").set_value(
        "Manual interview notes"
    )
    next(
        item
        for item in app.text_area
        if item.label == "Research note or relevant excerpt (optional)"
    ).set_value("Manually entered note; not retrieved by the app.")
    app.button(
        key=f"FormSubmitter:source_form_{project_id}-Save source note"
    ).click().run()
    assert not app.exception

    app.button(key=f"analyze_{project_id}").click().run()
    assert not app.exception
    assert any(
        item.label == "Download report (JSON)"
        for item in app.get("download_button")
    )
    app.radio(key="page_nav").set_value("My Projects").run()
    app.button(key=f"project_open_{project_id}").click().run()
    assert not app.exception
    assert app.radio(key="page_nav").value == "Project Workspace"
    assert any(
        item.label == "Download report (JSON)"
        for item in app.get("download_button")
    )
    for page in (
        "Dashboard",
        "My Projects",
        "Competitor Insights",
        "Research",
        "Analysis Report",
        "Notifications",
        "Profile",
        "Settings",
        "Project Workspace",
    ):
        app.radio(key="page_nav").set_value(page).run()
        assert not app.exception, f"Navigation to {page} raised a Streamlit exception"

    engine = get_engine()
    try:
        with database_session(engine) as session:
            project = get_project_record(session, project_id)
        assert project is not None
        assert len(project["competitors"]) == 1
        assert len(project["sources"]) == 1
        assert len(project["reports"]) == 1
        assert project["business_model"].startswith("Monthly subscription")
        assert project["competitors"][0]["target_audience"] == "Local businesses"
        assert project["competitors"][0]["pricing"] == "Manually noted; not verified"
        assert project["reports"][0]["payload"]["ai_interpretations"].startswith(
            "None."
        )
    finally:
        engine.dispose()
        get_engine.cache_clear()
        get_settings.cache_clear()

    restarted_app = AppTest.from_file(str(app_path), default_timeout=20).run()
    assert not restarted_app.exception
    assert restarted_app.radio(key="vl_theme").value == "Light"
    restarted_metrics = {
        item.label: item.value for item in restarted_app.metric
    }
    assert restarted_metrics["Total projects"] == "1"
    assert restarted_metrics["Completed analyses"] == "1"
    assert any(
        item.value == "UI workflow project" for item in restarted_app.subheader
    )
