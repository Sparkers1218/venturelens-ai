from __future__ import annotations

from uuid import uuid4

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from core.schemas import CompetitorInput, ProjectInput, ResearchSourceInput
from database.models import AnalysisReport, Competitor, Project, ResearchSource, utc_now


def _isoformat(value) -> str:
    return value.isoformat(timespec="seconds")


def project_to_dict(project: Project) -> dict:
    reports = sorted(
        project.reports, key=lambda report: report.created_at, reverse=True
    )
    latest_report = reports[0] if reports else None
    analysis_status = (
        "Draft · No analysis saved"
        if latest_report is None
        else "Inputs changed since last report"
        if project.updated_at > latest_report.created_at
        else "Report saved"
    )
    return {
        "id": project.id,
        "name": project.name,
        "problem_statement": project.problem_statement,
        "proposed_solution": project.proposed_solution,
        "target_customers": project.target_customers,
        "industry": project.industry,
        "geography": project.geography,
        "business_model": project.business_model,
        "created_at": _isoformat(project.created_at),
        "updated_at": _isoformat(project.updated_at),
        "analysis_status": analysis_status,
        "competitors": [
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "source_url": item.source_url,
                "target_audience": item.target_audience,
                "pricing": item.pricing,
                "differentiation_notes": item.differentiation_notes,
                "provenance": "User-provided; not independently verified.",
                "created_at": _isoformat(item.created_at),
            }
            for item in project.competitors
        ],
        "sources": [
            {
                "id": item.id,
                "title": item.title,
                "publisher": item.publisher,
                "source_url": item.source_url,
                "summary": item.summary,
                "provenance": item.provenance,
                "created_at": _isoformat(item.created_at),
            }
            for item in project.sources
        ],
        "reports": [
            {
                "id": item.id,
                "engine_label": item.engine_label,
                "created_at": _isoformat(item.created_at),
                "payload": item.payload,
            }
            for item in reports
        ],
    }


def create_project(session: Session, data: ProjectInput) -> Project:
    project = Project(id=str(uuid4()), **data.model_dump())
    session.add(project)
    session.flush()
    return project


def list_projects(session: Session, search: str = "") -> list[Project]:
    statement = (
        select(Project)
        .options(
            selectinload(Project.competitors),
            selectinload(Project.sources),
            selectinload(Project.reports),
        )
        .order_by(Project.updated_at.desc())
    )
    if search.strip():
        term = f"%{search.strip()}%"
        statement = statement.where(
            or_(
                Project.name.ilike(term),
                Project.problem_statement.ilike(term),
                Project.target_customers.ilike(term),
            )
        )
    return list(session.scalars(statement))


def get_project(session: Session, project_id: str) -> Project | None:
    statement = (
        select(Project)
        .where(Project.id == project_id)
        .options(
            selectinload(Project.competitors),
            selectinload(Project.sources),
            selectinload(Project.reports),
        )
    )
    return session.scalar(statement)


def get_project_record(session: Session, project_id: str) -> dict | None:
    project = get_project(session, project_id)
    return project_to_dict(project) if project is not None else None


def list_project_records(session: Session, search: str = "") -> list[dict]:
    return [
        project_to_dict(project)
        for project in list_projects(session, search=search)
    ]


def update_project(
    session: Session, project: Project, data: ProjectInput
) -> Project:
    for field, value in data.model_dump().items():
        setattr(project, field, value)
    session.flush()
    return project


def delete_project(session: Session, project: Project) -> None:
    session.delete(project)


def add_competitor(
    session: Session, project: Project, data: CompetitorInput
) -> Competitor:
    project.updated_at = utc_now()
    competitor = Competitor(
        id=str(uuid4()),
        project=project,
        name=data.name,
        description=data.description,
        source_url=data.source_url,
        target_audience=data.target_audience,
        pricing=data.pricing,
        differentiation_notes=data.differentiation_notes,
    )
    session.add(competitor)
    session.flush()
    return competitor


def remove_competitor(
    session: Session, project_id: str, competitor_id: str
) -> bool:
    competitor = session.scalar(
        select(Competitor).where(
            Competitor.id == competitor_id,
            Competitor.project_id == project_id,
        )
    )
    if competitor is None:
        return False
    competitor.project.updated_at = utc_now()
    session.delete(competitor)
    return True


def add_source(
    session: Session, project: Project, data: ResearchSourceInput
) -> ResearchSource:
    project.updated_at = utc_now()
    source = ResearchSource(
        id=str(uuid4()),
        project=project,
        title=data.title,
        publisher=data.publisher,
        source_url=data.source_url,
        summary=data.summary,
        provenance="manual_unverified",
    )
    session.add(source)
    session.flush()
    return source


def remove_source(session: Session, project_id: str, source_id: str) -> bool:
    source = session.scalar(
        select(ResearchSource).where(
            ResearchSource.id == source_id,
            ResearchSource.project_id == project_id,
        )
    )
    if source is None:
        return False
    source.project.updated_at = utc_now()
    session.delete(source)
    return True


def create_report(
    session: Session,
    project: Project,
    engine_label: str,
    payload: dict,
) -> AnalysisReport:
    project.updated_at = utc_now()
    report = AnalysisReport(
        id=str(uuid4()),
        project=project,
        engine_label=engine_label,
        payload=payload,
    )
    session.add(report)
    session.flush()
    return report


def get_report(
    session: Session, project_id: str, report_id: str
) -> AnalysisReport | None:
    return session.scalar(
        select(AnalysisReport).where(
            AnalysisReport.project_id == project_id,
            AnalysisReport.id == report_id,
        )
    )


def list_reports(session: Session, project_id: str) -> list[AnalysisReport]:
    statement = (
        select(AnalysisReport)
        .where(AnalysisReport.project_id == project_id)
        .order_by(AnalysisReport.created_at.desc())
    )
    return list(session.scalars(statement))
