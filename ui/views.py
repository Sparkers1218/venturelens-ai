from __future__ import annotations

import json
import logging
import re
from typing import Any

import streamlit as st
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from config.settings import get_settings
from core.analysis import build_rule_based_report
from core.schemas import CompetitorInput, ProjectInput, ResearchSourceInput
from database.connection import database_session
from database.repository import (
    add_competitor,
    add_source,
    create_project,
    create_report,
    delete_project,
    get_project,
    get_project_record,
    list_project_records,
    remove_competitor,
    remove_source,
    update_project,
)
from ui.components import request_navigation, show_validation_error


LOGGER = logging.getLogger(__name__)


def _serialize_report(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")


def _report_version_label(report: dict[str, Any]) -> str:
    return (
        f"{report['created_at']} · {report['engine_label']} · "
        f"{report['id'][:8]}"
    )


def _read_projects(search: str = "") -> list[dict[str, Any]] | None:
    try:
        with database_session() as session:
            return list_project_records(session, search)
    except SQLAlchemyError as error:
        LOGGER.error("Could not read projects (%s)", type(error).__name__)
        st.error("Projects could not be loaded. Check the database configuration and try again.")
        return None


def _recent_activities(
    projects: list[dict[str, Any]], limit: int = 8
) -> list[dict[str, str]]:
    activities: list[dict[str, str]] = []
    for project in projects:
        activities.append(
            {
                "timestamp": project["created_at"],
                "project": project["name"],
                "description": "Project created",
            }
        )
        if project["updated_at"] > project["created_at"]:
            activities.append(
                {
                    "timestamp": project["updated_at"],
                    "project": project["name"],
                    "description": "Project or related records updated",
                }
            )
        activities.extend(
            {
                "timestamp": item["created_at"],
                "project": project["name"],
                "description": f"Competitor added: {item['name']}",
            }
            for item in project["competitors"]
        )
        activities.extend(
            {
                "timestamp": item["created_at"],
                "project": project["name"],
                "description": f"Research note added: {item['title']}",
            }
            for item in project["sources"]
        )
        activities.extend(
            {
                "timestamp": item["created_at"],
                "project": project["name"],
                "description": "Analysis report generated",
            }
            for item in project["reports"]
        )
    return sorted(
        activities, key=lambda activity: activity["timestamp"], reverse=True
    )[:limit]


def _render_activity_feed(projects: list[dict[str, Any]], limit: int = 8) -> None:
    activities = _recent_activities(projects, limit)
    if not activities:
        st.info("Activity will appear here as you create and update projects.")
        return
    for activity in activities:
        st.caption(
            f"{activity['timestamp']} · {activity['project']} · "
            f"{activity['description']}"
        )


def render_dashboard() -> None:
    demo_mode = get_settings().demo_mode
    st.title("Dashboard")
    st.caption(
        "Fictional evaluator sample and deterministic analysis."
        if demo_mode
        else "Your saved startup projects and analysis."
    )
    if demo_mode:
        st.info(
            "Read-only evaluator demo using fictional synthetic data in temporary "
            "in-memory storage. No user data is accepted or persisted."
        )
    else:
        st.info(
            "Local demo mode. Projects and reports are saved to the configured database. "
            "Authentication, live research, and AI-provider integrations are not configured."
        )

    projects = _read_projects()
    if projects is None:
        return

    total_reports = sum(len(project["reports"]) for project in projects)
    followup_count = sum(
        project["analysis_status"] != "Report saved" for project in projects
    )
    metric_project, metric_reports, metric_needs_analysis = st.columns(3)
    metric_project.metric("Total projects", len(projects))
    metric_reports.metric("Completed analyses", total_reports)
    metric_needs_analysis.metric("Drafts or stale reports", followup_count)

    st.subheader("Idea brief completeness")
    st.caption(
        "Completeness of saved project inputs only; this is not a success or "
        "viability score."
    )
    if projects:
        latest = projects[0]
        values = {
            "Project name": latest["name"],
            "Problem": latest["problem_statement"],
            "Solution": latest["proposed_solution"],
            "Target customers": latest["target_customers"],
            "Industry": latest["industry"],
            "Geography": latest["geography"],
            "Business model": latest["business_model"],
        }
        st.bar_chart(
            {
                "field": list(values),
                "provided": [int(bool(value.strip())) for value in values.values()],
            },
            x="field",
            y="provided",
            horizontal=True,
        )
        st.caption("Showing the most recently updated project.")
    else:
        st.info("Create a project to see its input-completeness chart.")

    st.subheader("Recent projects")
    if not projects:
        st.write("No projects saved yet.")
    else:
        for project in projects[:5]:
            with st.container(border=True):
                st.subheader(project["name"])
                st.caption(
                    f"{project['industry'] or 'Industry not set'} · "
                    f"{project['geography'] or 'Geography not set'} · "
                    f"Updated {project['updated_at']}"
                )
                st.caption(project["analysis_status"])
                if st.button("Open project", key=f"dashboard_open_{project['id']}"):
                    request_navigation("Project Workspace", project["id"])

    st.subheader("Recent activity")
    _render_activity_feed(projects, limit=6)

    st.subheader("Next action")
    followup_project = next(
        (
            project
            for project in projects
            if project["analysis_status"] != "Report saved"
        ),
        None,
    )
    if followup_project:
        action_label = (
            "Continue draft"
            if not followup_project["reports"]
            else "Refresh analysis"
        )
        st.caption(followup_project["analysis_status"])
        if st.button(action_label, key="dashboard_continue_draft"):
            target_page = (
                "Project Workspace"
                if not followup_project["reports"]
                else "Analysis Report"
            )
            request_navigation(target_page, followup_project["id"])
    elif projects:
        st.caption("Every project has a saved report. Review the most recently updated one.")
        if st.button("Review latest report", key="dashboard_review_report"):
            request_navigation("Analysis Report", projects[0]["id"])
    else:
        st.caption("Create your first startup project to begin.")

    if not demo_mode and st.button(
        "Create a project", type="primary", key="dashboard_create"
    ):
        request_navigation("Create Project")


def render_new_project() -> None:
    st.title("Create Project")
    if get_settings().demo_mode:
        st.info(
            "Project creation is disabled in the read-only synthetic evaluator demo."
        )
        return
    st.caption("Save a draft now and refine it as you learn.")

    with st.form("create_project_form"):
        name = st.text_input("Project name *", max_chars=120)
        problem = st.text_area("Problem statement", max_chars=4000)
        solution = st.text_area("Proposed solution", max_chars=4000)
        customers = st.text_area("Target customers", max_chars=2000)
        industry = st.text_input("Industry", max_chars=120)
        geography = st.text_input("Geography", max_chars=160)
        business_model = st.text_area("Business model (optional)", max_chars=2000)
        submitted = st.form_submit_button("Save project", type="primary")

    if not submitted:
        return

    try:
        data = ProjectInput(
            name=name,
            problem_statement=problem,
            proposed_solution=solution,
            target_customers=customers,
            industry=industry,
            geography=geography,
            business_model=business_model,
        )
    except ValidationError as error:
        show_validation_error(error)
        return

    try:
        with database_session() as session:
            project = create_project(session, data)
            project_id = project.id
    except SQLAlchemyError as error:
        LOGGER.error("Could not save project (%s)", type(error).__name__)
        st.error("The project was not saved. Check the database and try again.")
        return

    st.session_state["selected_project_id"] = project_id
    st.success("Project saved.")
    request_navigation("Project Workspace", project_id)


def render_projects() -> None:
    demo_mode = get_settings().demo_mode
    st.title("My Projects")
    search = st.text_input(
        "Search by project name, problem, or target customers",
        key="projects_search",
    )
    projects = _read_projects(search)
    if projects is None:
        return
    if not projects:
        st.info("No matching projects. Create a project to start a validation workspace.")
        if not demo_mode and st.button("Create project", key="projects_empty_create"):
            request_navigation("Create Project")
        return

    delete_id = st.session_state.get("confirm_delete_project")
    for project in projects:
        with st.container(border=True):
            st.subheader(project["name"])
            st.caption(
                f"{project['industry'] or 'Industry not set'} · "
                f"{project['geography'] or 'Geography not set'} · "
                f"Updated {project['updated_at']}"
            )
            st.caption(project["analysis_status"])
            st.text(project["problem_statement"] or "No problem statement supplied.")
            if demo_mode:
                if st.button("Open workspace", key=f"project_open_{project['id']}"):
                    request_navigation("Project Workspace", project["id"])
            else:
                action_open, action_delete = st.columns([1, 1])
                with action_open:
                    if st.button("Open workspace", key=f"project_open_{project['id']}"):
                        request_navigation("Project Workspace", project["id"])
                with action_delete:
                    if st.button("Delete", key=f"project_delete_{project['id']}"):
                        st.session_state["confirm_delete_project"] = project["id"]
                        st.rerun()
            if project["reports"] and st.button(
                "View analysis report",
                key=f"project_report_{project['id']}",
            ):
                request_navigation("Analysis Report", project["id"])

            if not demo_mode and delete_id == project["id"]:
                st.warning("Delete this project and its competitors, sources, and saved reports?")
                confirm, cancel = st.columns(2)
                with confirm:
                    if st.button("Confirm delete", key=f"confirm_delete_{project['id']}"):
                        try:
                            with database_session() as session:
                                record = get_project(session, project["id"])
                                if record is not None:
                                    delete_project(session, record)
                        except SQLAlchemyError as error:
                            LOGGER.error(
                                "Could not delete project (%s)", type(error).__name__
                            )
                            st.error("The project was not deleted. Check the database and retry.")
                            return
                        st.session_state.pop("confirm_delete_project", None)
                        if st.session_state.get("selected_project_id") == project["id"]:
                            st.session_state.pop("selected_project_id", None)
                        if st.session_state.get("workspace_project_select") == project["id"]:
                            st.session_state.pop("workspace_project_select", None)
                        for key in (
                            "competitor_page_project",
                            "research_page_project",
                            "analysis_page_project",
                        ):
                            if st.session_state.get(key) == project["id"]:
                                st.session_state.pop(key, None)
                        st.success("Project and related records deleted.")
                        st.rerun()
                with cancel:
                    if st.button("Cancel", key=f"cancel_delete_{project['id']}"):
                        st.session_state.pop("confirm_delete_project", None)
                        st.rerun()


def _save_project_update(project_id: str, fields: dict[str, str]) -> bool:
    try:
        data = ProjectInput(**fields)
    except ValidationError as error:
        show_validation_error(error)
        return False

    try:
        with database_session() as session:
            project = get_project(session, project_id)
            if project is None:
                st.error("This project no longer exists.")
                return False
            update_project(session, project, data)
    except SQLAlchemyError as error:
        LOGGER.error("Could not update project (%s)", type(error).__name__)
        st.error("The project was not updated. Check the database and try again.")
        return False
    return True


def _render_project_editor(project: dict[str, Any]) -> None:
    demo_mode = get_settings().demo_mode
    st.subheader("Idea details")
    if demo_mode:
        st.caption("Fictional sample project details; editing is disabled.")
    with st.form(f"edit_project_{project['id']}"):
        name = st.text_input(
            "Project name *",
            value=project["name"],
            max_chars=120,
            key=f"edit_name_{project['id']}",
            disabled=demo_mode,
        )
        problem = st.text_area(
            "Problem statement",
            value=project["problem_statement"],
            max_chars=4000,
            key=f"edit_problem_{project['id']}",
            disabled=demo_mode,
        )
        solution = st.text_area(
            "Proposed solution",
            value=project["proposed_solution"],
            max_chars=4000,
            key=f"edit_solution_{project['id']}",
            disabled=demo_mode,
        )
        customers = st.text_area(
            "Target customers",
            value=project["target_customers"],
            max_chars=2000,
            key=f"edit_customers_{project['id']}",
            disabled=demo_mode,
        )
        industry = st.text_input(
            "Industry",
            value=project["industry"],
            max_chars=120,
            key=f"edit_industry_{project['id']}",
            disabled=demo_mode,
        )
        geography = st.text_input(
            "Geography",
            value=project["geography"],
            max_chars=160,
            key=f"edit_geography_{project['id']}",
            disabled=demo_mode,
        )
        business_model = st.text_area(
            "Business model (optional)",
            value=project["business_model"],
            max_chars=2000,
            key=f"edit_business_model_{project['id']}",
            disabled=demo_mode,
        )
        submitted = st.form_submit_button("Save changes", disabled=demo_mode)

    if submitted:
        if _save_project_update(
            project["id"],
            {
                "name": name,
                "problem_statement": problem,
                "proposed_solution": solution,
                "target_customers": customers,
                "industry": industry,
                "geography": geography,
                "business_model": business_model,
            },
        ):
            st.success("Project updated.")
            st.rerun()


def _render_competitors(project: dict[str, Any]) -> None:
    demo_mode = get_settings().demo_mode
    st.subheader("Competitors and alternatives")
    st.caption(
        "Fictional illustrative alternatives; not researched or verified."
        if demo_mode
        else "Entries are founder-provided and are not independently verified."
    )
    with st.form(f"competitor_form_{project['id']}"):
        name = st.text_input("Name *", max_chars=160, disabled=demo_mode)
        description = st.text_area(
            "Description or notes", max_chars=2000, disabled=demo_mode
        )
        source_url = st.text_input(
            "Website or reference URL (optional)", max_chars=2048, disabled=demo_mode
        )
        target_audience = st.text_area(
            "Target audience (optional)", max_chars=1000, disabled=demo_mode
        )
        pricing = st.text_input("Pricing (optional)", max_chars=1000, disabled=demo_mode)
        differentiation_notes = st.text_area(
            "Differentiation notes (optional)", max_chars=2000, disabled=demo_mode
        )
        submitted = st.form_submit_button(
            "Add competitor or alternative", disabled=demo_mode
        )

    if submitted:
        try:
            data = CompetitorInput(
                name=name,
                description=description,
                source_url=source_url,
                target_audience=target_audience,
                pricing=pricing,
                differentiation_notes=differentiation_notes,
            )
        except ValidationError as error:
            show_validation_error(error)
            return
        try:
            with database_session() as session:
                record = get_project(session, project["id"])
                if record is None:
                    st.error("This project no longer exists.")
                    return
                add_competitor(session, record, data)
        except SQLAlchemyError as error:
            LOGGER.error("Could not save competitor (%s)", type(error).__name__)
            st.error("The competitor entry was not saved. Check the database and retry.")
            return
        st.success("Competitor entry saved as founder-provided information.")
        st.rerun()

    if not project["competitors"]:
        st.info("No competitor or alternative entries yet. This does not imply none exist.")
    for competitor in project["competitors"]:
        with st.container(border=True):
            st.text(competitor["name"])
            st.text(competitor["description"] or "No notes supplied.")
            if competitor["target_audience"]:
                st.caption(f"Target audience: {competitor['target_audience']}")
            if competitor["pricing"]:
                pricing_label = (
                    "Pricing (not researched)"
                    if demo_mode
                    else "Pricing (founder-provided)"
                )
                st.caption(f"{pricing_label}: {competitor['pricing']}")
            if competitor["differentiation_notes"]:
                st.caption(
                    "Differentiation notes (unverified): "
                    f"{competitor['differentiation_notes']}"
                )
            if competitor["source_url"]:
                st.link_button("Open source", competitor["source_url"])
            if st.button(
                "Remove entry",
                key=f"remove_competitor_{competitor['id']}",
                disabled=demo_mode,
            ):
                try:
                    with database_session() as session:
                        remove_competitor(
                            session, project["id"], competitor["id"]
                        )
                except SQLAlchemyError as error:
                    LOGGER.error(
                        "Could not remove competitor (%s)", type(error).__name__
                    )
                    st.error("The competitor entry was not removed. Please retry.")
                    return
                st.rerun()


def _render_sources(project: dict[str, Any]) -> None:
    demo_mode = get_settings().demo_mode
    st.subheader("Research source notes")
    st.caption(
        "No external sources are included in this synthetic sample."
        if demo_mode
        else (
            "Manual source records only. They are user-provided references, not live "
            "research and not independently verified."
        )
    )
    with st.form(f"source_form_{project['id']}"):
        title = st.text_input("Source title *", max_chars=200, disabled=demo_mode)
        publisher = st.text_input(
            "Publisher (optional)", max_chars=200, disabled=demo_mode
        )
        source_url = st.text_input(
            "Source URL (optional)", max_chars=2048, disabled=demo_mode
        )
        summary = st.text_area(
            "Research note or relevant excerpt (optional)",
            max_chars=4000,
            disabled=demo_mode,
        )
        submitted = st.form_submit_button("Save source note", disabled=demo_mode)

    if submitted:
        try:
            data = ResearchSourceInput(
                title=title,
                publisher=publisher,
                source_url=source_url,
                summary=summary,
            )
        except ValidationError as error:
            show_validation_error(error)
            return
        try:
            with database_session() as session:
                record = get_project(session, project["id"])
                if record is None:
                    st.error("This project no longer exists.")
                    return
                add_source(session, record, data)
        except SQLAlchemyError as error:
            LOGGER.error("Could not save research source (%s)", type(error).__name__)
            st.error("The source note was not saved. Check the database and retry.")
            return
        st.success("Source note saved and labeled as user-provided.")
        st.rerun()

    if not project["sources"]:
        st.info("No source notes yet. No external research has been retrieved.")
    for source in project["sources"]:
        with st.container(border=True):
            st.text(source["title"])
            st.caption(
                f"{source['publisher'] or 'Publisher not supplied'} · "
                "User-provided; not independently verified"
            )
            st.text(source["summary"] or "No summary supplied.")
            if source["source_url"]:
                st.link_button("Open source", source["source_url"])
            if st.button(
                "Remove source",
                key=f"remove_source_{source['id']}",
                disabled=demo_mode,
            ):
                try:
                    with database_session() as session:
                        remove_source(
                            session, project["id"], source["id"]
                        )
                except SQLAlchemyError as error:
                    LOGGER.error(
                        "Could not remove research source (%s)", type(error).__name__
                    )
                    st.error("The source note was not removed. Please retry.")
                    return
                st.rerun()


def _render_report(project: dict[str, Any]) -> None:
    demo_mode = get_settings().demo_mode
    st.subheader("Analysis report")
    st.caption(
        (
            "Deterministic rule-based report of fictional synthetic data (not "
            "AI-generated or external research)."
            if demo_mode
            else "Rule-based demo analysis (not AI-generated). The completeness chart "
            "is not a success score."
        )
    )

    if st.button(
        "Generate and save report",
        type="primary",
        key=f"analyze_{project['id']}",
        disabled=demo_mode,
    ):
        payload = build_rule_based_report(
            {
                "name": project["name"],
                "problem_statement": project["problem_statement"],
                "proposed_solution": project["proposed_solution"],
                "target_customers": project["target_customers"],
                "industry": project["industry"],
                "geography": project["geography"],
                "business_model": project["business_model"],
            },
            project["competitors"],
            project["sources"],
        )
        try:
            with database_session() as session:
                record = get_project(session, project["id"])
                if record is None:
                    st.error("This project no longer exists.")
                    return
                saved_report = create_report(
                    session,
                    record,
                    "Rule-based demo analysis (not AI-generated)",
                    payload,
                )
                report_id = saved_report.id
        except SQLAlchemyError as error:
            LOGGER.error("Could not save analysis report (%s)", type(error).__name__)
            st.error("The report was not saved. Check the database and retry.")
            return
        st.session_state[f"selected_report_id_{project['id']}"] = report_id
        st.session_state[f"report_select_{project['id']}"] = report_id
        st.success("Report generated and saved.")
        st.rerun()

    if not project["reports"]:
        st.info("No saved reports yet. Generate a report to create one.")
        return

    reports = project["reports"]
    report_by_id = {report["id"]: report for report in reports}
    selection_key = f"report_select_{project['id']}"
    persistent_selection_key = f"selected_report_id_{project['id']}"
    preferred_id = st.session_state.get(persistent_selection_key)
    if preferred_id not in report_by_id:
        preferred_id = reports[0]["id"]
    selected_before_render = st.session_state.get(selection_key)
    if selected_before_render not in report_by_id:
        selected_before_render = preferred_id
        st.session_state[selection_key] = selected_before_render
    default_index = next(
        index
        for index, item in enumerate(reports)
        if item["id"] == selected_before_render
    )
    selected_id = st.selectbox(
        "Saved report",
        options=[report["id"] for report in reports],
        index=default_index,
        format_func=lambda report_id: _report_version_label(report_by_id[report_id]),
        key=selection_key,
    )
    st.session_state[persistent_selection_key] = selected_id
    report = report_by_id[selected_id]
    if selected_id != reports[0]["id"]:
        st.info("Viewing an earlier saved report version.")
    if project["analysis_status"] == "Inputs changed since last report":
        st.warning(
            "Project inputs changed after the latest report was saved. This report "
            "preserves the inputs used at that time; generate a new report to assess "
            "the current project information."
        )
    payload = report["payload"]
    if payload.get("schema_version") != 2:
        st.warning(
            "This saved report uses an earlier report format. Its original data "
            "is preserved; generate a new report to view the expanded assessment."
        )
        st.download_button(
            "Download legacy report (JSON)",
            data=_serialize_report(payload),
            file_name=f"venturelens-legacy-{report['id'][:8]}.json",
            mime="application/json",
            key=f"download_legacy_report_{report['id']}",
        )
        return
    coverage = payload["input_completeness"]
    st.warning(payload["notice"])
    st.markdown("### Executive summary")
    st.write(payload["executive_summary"])
    st.metric(
        "Brief fields documented",
        f"{coverage['completed_fields']} of {coverage['total_fields']}",
        help=coverage["meaning"],
    )

    st.markdown("### Dimension assessment")
    st.caption(payload["score_explanation"])
    score_rows = [
        {"Dimension": item["dimension"], "Score (0-3)": item["score"]}
        for item in payload["assessment_scores"]
    ]
    st.bar_chart(score_rows, x="Dimension", y="Score (0-3)", horizontal=True)
    with st.expander("Scoring rules and evidence"):
        for item in payload["assessment_scores"]:
            st.markdown(f"**{item['dimension']}: {item['score']}/{item['maximum']}**")
            st.write(item["basis"])
            st.caption(item["rubric"])

    st.markdown("### Problem and solution assessment")
    assessment = payload["problem_and_solution_assessment"]
    st.write(f"**Problem statement:** {assessment['problem_statement']}")
    st.write(f"**Proposed solution:** {assessment['proposed_solution']}")
    st.info(assessment["relevance_assessment"])

    st.markdown("### Customer analysis")
    customer = payload["customer_analysis"]
    st.write(f"**Target customers:** {customer['target_customers']}")
    st.write(f"**Industry:** {customer['industry']}")
    st.write(f"**Geographic market:** {customer['geographic_market']}")
    st.caption(customer["assessment"])

    st.markdown("### Competitor comparison")
    if payload["competitor_comparison"]:
        st.dataframe(
            [
                {
                    "Name": item["name"],
                    "Description": item["description"],
                    "Target audience": item["target_audience"],
                    "Pricing": item["pricing"],
                    "Differentiation notes": item["differentiation_notes"],
                    "Website/reference": item["website"],
                    "Provenance": item["provenance"],
                }
                for item in payload["competitor_comparison"]
            ],
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("No competitor or alternative records have been entered.")

    st.markdown("### Business model considerations")
    business_model = payload["business_model_considerations"]
    st.write(business_model["description"])
    st.caption(business_model["assessment"])

    st.markdown("### Strengths and weaknesses of this brief")
    st.markdown("**Documented inputs**")
    for item in payload["strengths_of_brief"]:
        st.markdown(f"- {item}")
    st.markdown("**Missing inputs**")
    if payload["weaknesses_of_brief"]:
        for item in payload["weaknesses_of_brief"]:
            st.markdown(f"- {item}")
    else:
        st.write("No tracked brief fields are missing.")

    st.markdown("### Risks and uncertainties")
    st.bar_chart(
        [
            {"Severity": severity, "Count": count}
            for severity, count in payload["risk_distribution"].items()
        ],
        x="Severity",
        y="Count",
    )
    for risk in payload["risks_and_uncertainties"]:
        st.markdown(f"**{risk['severity']}: {risk['title']}**")
        st.write(risk["detail"])
        st.caption(risk["provenance"])

    st.markdown("### Assumptions to validate")
    for assumption in payload["assumptions_to_validate"]:
        st.markdown(f"- **{assumption['status']}:** {assumption['statement']}")

    st.markdown("### Evidence and research references")
    st.caption(
        "No external research sources are included in this synthetic sample."
        if demo_mode
        else (
            "All listed sources are manual user-entered records. URLs are not fetched "
            "or verified by this application."
        )
    )
    if payload["evidence_and_research_references"]:
        st.dataframe(
            [
                {
                    "Title": item["title"],
                    "Publisher": item["publisher"],
                    "URL": item["url"],
                    "Notes": item["notes"],
                    "Provenance": item["provenance"],
                }
                for item in payload["evidence_and_research_references"]
            ],
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("No research sources have been entered.")

    st.markdown("### Recommended validation experiments")
    st.caption(payload["experiment_priority_explanation"])
    st.bar_chart(
        [
            {"Experiment": item["name"], "Priority (1-3)": item["priority_score"]}
            for item in payload["validation_experiments"]
        ],
        x="Experiment",
        y="Priority (1-3)",
    )
    for experiment in payload["validation_experiments"]:
        st.markdown(f"**{experiment['priority']} priority · {experiment['name']}**")
        st.write(experiment["question"])
        st.write(experiment["action"])
        st.caption(
            f"{experiment['cost_effort']} {experiment['success_threshold']}"
        )

    st.markdown("### Recommendations")
    for recommendation in payload["recommendations"]:
        st.markdown(f"**{recommendation['title']}**")
        st.write(recommendation["detail"])
        st.caption(recommendation["provenance"])

    st.markdown("### Recommended next steps")
    for step in payload["recommended_next_steps"]:
        st.markdown(f"- {step}")
    st.caption(payload["ai_interpretations"])

    filename_stem = re.sub(
        r"[^A-Za-z0-9_-]+", "-", project["name"]
    ).strip("-") or "venturelens-report"
    st.download_button(
        "Download report (JSON)",
        data=_serialize_report(payload),
        file_name=f"{filename_stem}-{report['id'][:8]}.json",
        mime="application/json",
        key=f"download_report_{report['id']}",
    )


def render_project_workspace() -> None:
    demo_mode = get_settings().demo_mode
    st.title("Project Workspace")
    projects = _read_projects()
    if projects is None:
        return
    if not projects:
        st.info("Create a project before opening a workspace.")
        if not demo_mode and st.button("Create project", key="workspace_empty_create"):
            request_navigation("Create Project")
        return

    project_by_id = {project["id"]: project for project in projects}
    current_id = st.session_state.get("selected_project_id")
    current_index = next(
        (index for index, item in enumerate(projects) if item["id"] == current_id),
        0,
    )
    selected_id = st.selectbox(
        "Choose a project",
        options=[project["id"] for project in projects],
        index=current_index,
        format_func=lambda project_id: project_by_id[project_id]["name"],
        key="workspace_project_select",
    )
    st.session_state["selected_project_id"] = selected_id

    try:
        with database_session() as session:
            project = get_project_record(session, selected_id)
    except SQLAlchemyError as error:
        LOGGER.error("Could not load project workspace (%s)", type(error).__name__)
        st.error("The project workspace could not be loaded. Check the database and retry.")
        return
    if project is None:
        st.warning("This project no longer exists.")
        return

    st.caption(
        f"Created {project['created_at']} · Last updated {project['updated_at']}"
    )
    tab_details, tab_competitors, tab_research, tab_analysis = st.tabs(
        ["Details", "Competitors", "Research", "Analysis"]
    )
    with tab_details:
        _render_project_editor(project)
    with tab_competitors:
        _render_competitors(project)
    with tab_research:
        _render_sources(project)
    with tab_analysis:
        _render_report(project)


def _choose_project(
    projects: list[dict[str, Any]], key: str
) -> dict[str, Any] | None:
    if not projects:
        return None
    by_id = {project["id"]: project for project in projects}
    if st.session_state.get(key) not in by_id:
        st.session_state.pop(key, None)
    current_id = st.session_state.get("selected_project_id")
    current_index = next(
        (index for index, project in enumerate(projects) if project["id"] == current_id),
        0,
    )
    selected_id = st.selectbox(
        "Project",
        options=[project["id"] for project in projects],
        index=current_index,
        format_func=lambda project_id: by_id[project_id]["name"],
        key=key,
    )
    st.session_state["selected_project_id"] = selected_id
    return by_id[selected_id]


def _render_project_required_empty_state() -> None:
    if get_settings().demo_mode:
        st.info("No synthetic sample project is available.")
        return
    st.info("Create a project first. Project-specific information will appear here.")
    if st.button("Create project", key="section_empty_create"):
        request_navigation("Create Project")


def render_competitor_insights() -> None:
    demo_mode = get_settings().demo_mode
    st.title("Competitor Insights")
    st.caption(
        (
            "Compare fictional illustrative alternatives. They are not researched "
            "or real competitor findings."
            if demo_mode
            else "Compare founder-entered competitors and alternatives. Entries are "
            "not independently verified."
        )
    )
    projects = _read_projects()
    if projects is None:
        return
    if not projects:
        _render_project_required_empty_state()
        return
    project = _choose_project(projects, "competitor_page_project")
    if project is not None:
        _render_competitors(project)


def render_research_page() -> None:
    demo_mode = get_settings().demo_mode
    st.title("Research")
    st.caption(
        (
            "The synthetic sample contains no external research sources."
            if demo_mode
            else "Add manual sources with attribution. VentureLens does not retrieve "
            "or verify these references."
        )
    )
    projects = _read_projects()
    if projects is None:
        return
    if not projects:
        _render_project_required_empty_state()
        return
    project = _choose_project(projects, "research_page_project")
    if project is not None:
        _render_sources(project)


def render_analysis_report_page() -> None:
    demo_mode = get_settings().demo_mode
    st.title("Analysis Report")
    st.caption(
        (
            "Review the saved deterministic report for the fictional sample."
            if demo_mode
            else "Generate and review a saved, rule-based report. Scores describe the "
            "information supplied, not business viability."
        )
    )
    projects = _read_projects()
    if projects is None:
        return
    if not projects:
        _render_project_required_empty_state()
        return
    project = _choose_project(projects, "analysis_page_project")
    if project is not None:
        _render_report(project)


def render_notifications() -> None:
    st.title("Notifications")
    st.caption(
        "Recent activity derived from saved project records; these are not "
        "external alerts or messages."
    )
    projects = _read_projects()
    if projects is None:
        return
    _render_activity_feed(projects, limit=30)


def render_profile() -> None:
    st.title("Profile")
    if get_settings().demo_mode:
        st.info("Public synthetic evaluator demo; user accounts are not enabled.")
        st.write("No user project data is accepted or stored in this read-only mode.")
    else:
        st.info("Demo mode: user accounts and authentication are not enabled.")
        st.write(
            "There is no signed-in profile. Projects belong to this local database "
            "and are not isolated by user."
        )


def render_settings() -> None:
    settings = get_settings()
    database_url = settings.database_url.lower()
    if settings.demo_mode:
        database_kind = "In-memory SQLite (read-only)"
    elif database_url.startswith("sqlite"):
        database_kind = "SQLite local database"
    elif database_url.startswith(("postgresql:", "postgresql+")):
        database_kind = "PostgreSQL database"
    else:
        database_kind = "Configured database"

    st.title("Settings")
    st.caption(
        "Public, synthetic, read-only evaluator demo."
        if settings.demo_mode
        else "Runtime configuration for this local demo."
    )
    app_column, database_column = st.columns(2)
    app_column.metric("Application mode", settings.app_env)
    database_column.metric("Database", database_kind)
    st.info(
        "No database URL, password, or other secret is displayed here. "
        "Database configuration is managed through environment settings."
    )
    st.subheader("Appearance")
    st.write(
        "Choose Light or Dark in the application header. Your choice remains "
        "active across Streamlit reruns in this session and resets for a new session."
    )
    st.subheader("Available integrations")
    st.write("Authentication, live research, and AI-provider integrations are disabled.")
