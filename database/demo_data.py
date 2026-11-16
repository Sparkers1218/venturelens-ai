from threading import RLock

from sqlalchemy import Engine

from config.settings import get_settings
from core.analysis import build_rule_based_report
from core.schemas import CompetitorInput, ProjectInput
from database.connection import (
    enable_read_only_sqlite,
    get_engine,
    initialize_database,
    database_session,
)
from database.repository import (
    add_competitor,
    create_project,
    create_report,
    list_projects,
)


SYNTHETIC_PROJECT_NAME = "Synthetic sample: Harbor Harvest Planner"
_seed_lock = RLock()


def seed_evaluator_demo(engine: Engine | None = None) -> None:
    if not get_settings().demo_mode:
        raise RuntimeError("Synthetic evaluator data requires DEMO_MODE=true.")

    target_engine = engine or get_engine()
    initialize_database(target_engine)

    with _seed_lock:
        with database_session(target_engine) as session:
            project = next(
                (
                    item
                    for item in list_projects(session)
                    if item.name == SYNTHETIC_PROJECT_NAME
                ),
                None,
            )
            if project is None:
                project = create_project(
                    session,
                    ProjectInput(
                        name=SYNTHETIC_PROJECT_NAME,
                        problem_statement=(
                            "Fictional example: a volunteer-run neighborhood food "
                            "group wants to coordinate weekly pickup windows."
                        ),
                        proposed_solution=(
                            "Fictional concept: a lightweight planner for listing "
                            "produce and coordinating pickup times."
                        ),
                        target_customers=(
                            "Illustrative persona only: a volunteer-run neighborhood "
                            "food group; this is not customer research."
                        ),
                        industry="Synthetic community-software example",
                        geography="Not specified in this fictional example",
                        business_model="Hypothetical and untested; no pricing research.",
                    ),
                )
                competitor_inputs = (
                    CompetitorInput(
                        name="Illustrative spreadsheet workflow",
                        description=(
                            "Fictional alternative included only to demonstrate "
                            "the comparison view."
                        ),
                        target_audience="Synthetic example; not researched.",
                        pricing="Not researched.",
                        differentiation_notes="Illustrative placeholder only.",
                    ),
                    CompetitorInput(
                        name="Illustrative group-message workflow",
                        description=(
                            "Fictional alternative included only to demonstrate "
                            "the comparison view."
                        ),
                        target_audience="Synthetic example; not researched.",
                        pricing="Not researched.",
                        differentiation_notes="Illustrative placeholder only.",
                    ),
                )
                competitors = [
                    add_competitor(session, project, data)
                    for data in competitor_inputs
                ]
                payload = build_rule_based_report(
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
                            "name": item.name,
                            "description": item.description,
                            "source_url": item.source_url,
                            "target_audience": item.target_audience,
                            "pricing": item.pricing,
                            "differentiation_notes": item.differentiation_notes,
                        }
                        for item in competitors
                    ],
                    [],
                    synthetic_demo=True,
                )
                create_report(
                    session,
                    project,
                    "Rule-based synthetic sample (not AI-generated)",
                    payload,
                )

        enable_read_only_sqlite(target_engine)
