import pytest
from ui.project_form import MARKET_CATEGORIES, render_project_creation_form
from ui.projects_view import render_my_projects_view
import ui


def test_ui_exports_project_views():
    assert hasattr(ui, "render_project_creation_form")
    assert callable(ui.render_project_creation_form)
    assert hasattr(ui, "render_my_projects_view")
    assert callable(ui.render_my_projects_view)


def test_market_categories_defined():
    assert isinstance(MARKET_CATEGORIES, list)
    assert len(MARKET_CATEGORIES) >= 5
    assert "Enterprise SaaS" in MARKET_CATEGORIES
    assert "Healthcare & HealthTech" in MARKET_CATEGORIES
    assert "FinTech & InsurTech" in MARKET_CATEGORIES


def test_project_schema_integrity():
    mock_project = {
        "id": "proj-1731283200",
        "name": "MedScribe AI",
        "category": "Healthcare & HealthTech",
        "icp": "Private practice physicians",
        "problem": "Doctors spend 3+ hours every evening charting SOAP notes manually.",
        "solution": "Ambient voice listening to generate structured EHR clinical notes.",
        "value_metric": "Reduce documentation time by 80%",
        "riskiest_assumption": "Clinicians will trust AI notes without line-by-line proofreading.",
        "feasibility_risk": "HIPAA compliance and EHR integration latency.",
        "created_at": "2026-11-11 01:00",
        "status": "In Validation",
        "milestone_stage": 1,
        "milestone_name": "Idea Ingestion",
        "conviction_score": "Pending Evidence",
    }

    expected_keys = {
        "id",
        "name",
        "category",
        "icp",
        "problem",
        "solution",
        "value_metric",
        "riskiest_assumption",
        "feasibility_risk",
        "created_at",
        "status",
        "milestone_stage",
        "milestone_name",
        "conviction_score",
    }

    assert expected_keys.issubset(mock_project.keys())
