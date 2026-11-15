from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping, Sequence


CONTEXT_FIELDS = (
    ("Project name", "name"),
    ("Problem statement", "problem_statement"),
    ("Proposed solution", "proposed_solution"),
    ("Target customers", "target_customers"),
    ("Industry", "industry"),
    ("Geographic market", "geography"),
    ("Business model", "business_model"),
)

_TEXT_SCORE_RUBRIC = (
    "0 = not supplied; 1 = supplied in 1-7 words; "
    "2 = supplied in 8-20 words; 3 = supplied in more than 20 words. "
    "This measures description detail only, not quality or likelihood of success."
)


def _text_detail_score(value: str) -> int:
    word_count = len(value.split())
    if word_count == 0:
        return 0
    if word_count < 8:
        return 1
    if word_count <= 20:
        return 2
    return 3


def _dimension(
    name: str, score: int, basis: str, rubric: str = _TEXT_SCORE_RUBRIC
) -> dict[str, Any]:
    return {
        "dimension": name,
        "score": score,
        "maximum": 3,
        "basis": basis,
        "rubric": rubric,
    }


def build_rule_based_report(
    project: Mapping[str, str],
    competitors: Sequence[Mapping[str, str]],
    sources: Sequence[Mapping[str, str]],
) -> dict[str, Any]:
    """Build an input-grounded report; scores measure brief coverage only."""
    completed = [
        label for label, key in CONTEXT_FIELDS if project.get(key, "").strip()
    ]
    missing = [
        label for label, key in CONTEXT_FIELDS if not project.get(key, "").strip()
    ]
    coverage = round(len(completed) / len(CONTEXT_FIELDS) * 100)

    founder_inputs = [
        {
            "field": label,
            "content": project[key],
            "provenance": "User-provided; not independently verified.",
        }
        for label, key in CONTEXT_FIELDS
        if project.get(key, "").strip()
    ]
    competitor_records = [
        {
            "name": item["name"],
            "description": item.get("description", ""),
            "website": item.get("source_url", ""),
            "target_audience": item.get("target_audience", ""),
            "pricing": item.get("pricing", ""),
            "differentiation_notes": item.get("differentiation_notes", ""),
            "provenance": "User-provided; not independently verified.",
        }
        for item in competitors
    ]
    source_records = [
        {
            "title": item["title"],
            "url": item.get("source_url", ""),
            "publisher": item.get("publisher", ""),
            "notes": item.get("summary", ""),
            "provenance": (
                "Manually entered source information; not retrieved or "
                "independently verified by VentureLens AI."
            ),
        }
        for item in sources
    ]

    problem = project.get("problem_statement", "").strip()
    solution = project.get("proposed_solution", "").strip()
    customers = project.get("target_customers", "").strip()
    business_model = project.get("business_model", "").strip()
    differentiation_count = sum(
        bool(item.get("differentiation_notes", "").strip()) for item in competitors
    )
    if competitors:
        competitor_score = 1 if len(competitors) == 1 else (
            2 if len(competitors) <= 3 else 3
        )
        differentiation_score = (
            1
            if differentiation_count == 0
            else 3
            if differentiation_count == len(competitors)
            else 2
        )
    else:
        competitor_score = 0
        differentiation_score = 0

    value_prop_parts = sum(bool(value) for value in (problem, solution, customers))
    scores = [
        _dimension(
            "Problem clarity",
            _text_detail_score(problem),
            f"Problem statement contains {len(problem.split())} words.",
        ),
        _dimension(
            "Customer definition",
            _text_detail_score(customers),
            f"Target-customer description contains {len(customers.split())} words.",
        ),
        _dimension(
            "Solution detail",
            _text_detail_score(solution),
            f"Solution description contains {len(solution.split())} words. "
            "Whether it is relevant requires customer evidence.",
        ),
        _dimension(
            "Value proposition inputs",
            value_prop_parts,
            f"{value_prop_parts} of 3 input elements are present: problem, solution, and customer.",
            "One point for each supplied input element (problem, solution, target customer). "
            "This does not assess value or product-market fit.",
        ),
        _dimension(
            "Competitor landscape records",
            competitor_score,
            f"{len(competitors)} user-provided competitor or alternative record(s).",
            "0 = none; 1 = one record; 2 = two or three records; "
            "3 = four or more records. Count only; not a market coverage assessment.",
        ),
        _dimension(
            "Differentiation notes coverage",
            differentiation_score,
            f"{differentiation_count} of {len(competitors)} competitor record(s) "
            "include founder-entered differentiation notes.",
            "0 = no competitor records; 1 = records exist but none have notes; "
            "2 = some have notes; 3 = all have notes. Notes are not verified.",
        ),
        _dimension(
            "Business model detail",
            _text_detail_score(business_model),
            f"Business model description contains {len(business_model.split())} words.",
        ),
    ]

    assumptions = [
        {
            "statement": (
                "The stated target customers experience this problem often "
                "and urgently enough to seek a solution."
            ),
            "status": "Untested hypothesis",
            "label": "Hypothesis to validate; not a finding.",
        },
        {
            "statement": (
                "The proposed solution fits the target customers' workflow "
                "better than their current alternatives."
            ),
            "status": "Untested hypothesis",
            "label": "Hypothesis to validate; not a finding.",
        },
    ]

    risks: list[dict[str, str]] = []
    if not problem:
        risks.append(
            {
                "title": "Problem statement missing",
                "detail": "The project has no problem statement to assess.",
                "severity": "High",
                "provenance": "Derived from missing user input.",
            }
        )
    if not customers:
        risks.append(
            {
                "title": "Target customer not defined",
                "detail": "The project does not identify a target customer group.",
                "severity": "High",
                "provenance": "Derived from missing user input.",
            }
        )
    if not solution:
        risks.append(
            {
                "title": "Proposed solution missing",
                "detail": "The project has no proposed solution to discuss.",
                "severity": "Medium",
                "provenance": "Derived from missing user input.",
            }
        )
    if not business_model:
        risks.append(
            {
                "title": "Business model not supplied",
                "detail": "Pricing, revenue, and delivery approach remain unspecified.",
                "severity": "Low",
                "provenance": "Derived from missing user input.",
            }
        )
    if not competitor_records:
        risks.append(
            {
                "title": "Competitor landscape not supplied",
                "detail": (
                    "No competitor or alternative records were entered. "
                    "This does not mean competitors are absent."
                ),
                "severity": "Medium",
                "provenance": "Derived from project records.",
            }
        )
    if not source_records:
        risks.append(
            {
                "title": "No research sources supplied",
                "detail": (
                    "This report contains no external research. Add attributable "
                    "source records and review their relevance and recency."
                ),
                "severity": "Medium",
                "provenance": "Derived from project records.",
            }
        )
    else:
        risks.append(
            {
                "title": "Source records are unverified",
                "detail": (
                    "Source details were entered manually and were not retrieved "
                    "or fact-checked by this application."
                ),
                "severity": "Low",
                "provenance": "Derived from source-entry workflow.",
            }
        )

    customer_phrase = customers or "a clearly defined customer segment"
    recommendations = [
        {
            "title": "Test the problem before building",
            "detail": (
                f"Interview people in {customer_phrase} about a recent instance "
                "of the problem and their current workaround. Record what they "
                "actually did, not just whether they like the idea."
            ),
            "provenance": "Rule-based recommendation; not AI-generated.",
        },
        {
            "title": "Map alternatives using attributable sources",
            "detail": (
                "Record direct products, indirect substitutes, and manual or "
                "do-nothing alternatives. Attach a source URL or label each "
                "entry as founder-provided."
            ),
            "provenance": "Rule-based recommendation; not AI-generated.",
        },
        {
            "title": "Clarify the business model",
            "detail": (
                "Write down who pays, what they pay for, and how the product "
                "would be delivered. Treat each as a hypothesis until tested."
            ),
            "provenance": "Rule-based recommendation; not AI-generated.",
        },
    ]
    experiments = [
        {
            "name": "Problem-discovery interviews",
            "priority": "High" if not problem or not customers else "Medium",
            "priority_score": 3 if not problem or not customers else 2,
            "question": "Do target customers experience the stated problem?",
            "action": (
                "Ask about recent examples, existing workarounds, and the "
                "consequences of the problem. Avoid pitching the solution."
            ),
            "cost_effort": "Low-cost exploratory activity; no cost estimate supplied.",
            "success_threshold": (
                "Set a decision threshold before starting; none is inferred "
                "by this application."
            ),
        },
        {
            "name": "Alternative-workflow mapping",
            "priority": "High" if not competitor_records else "Medium",
            "priority_score": 3 if not competitor_records else 2,
            "question": "What do customers use or do instead today?",
            "action": (
                "Document direct products, indirect substitutes, manual "
                "workarounds, and doing nothing; attach attributable sources."
            ),
            "cost_effort": "Desk research and founder interviews; no cost estimate supplied.",
            "success_threshold": (
                "Review whether each alternative is supported by a source "
                "or clearly marked as founder-provided."
            ),
        },
        {
            "name": "Business-model conversations",
            "priority": "Medium" if business_model else "High",
            "priority_score": 2 if business_model else 3,
            "question": "Who would pay, for what outcome, and under which conditions?",
            "action": (
                "Discuss current spending and purchasing decisions with target "
                "customers; avoid treating stated willingness as a purchase."
            ),
            "cost_effort": "Customer conversations; no cost estimate supplied.",
            "success_threshold": (
                "Define the evidence needed to continue before conducting interviews."
            ),
        },
    ]

    strengths = [
        f"{label} is documented."
        for label, key in CONTEXT_FIELDS
        if project.get(key, "").strip()
    ]
    weaknesses = [
        f"{label} is missing from the brief." for label in missing
    ]
    if competitor_records:
        strengths.append(
            f"{len(competitor_records)} founder-provided competitor/alternative "
            "record(s) are available for comparison."
        )
    if source_records:
        strengths.append(f"{len(source_records)} manual source note(s) are attached.")
    if not strengths:
        strengths.append("No substantive idea details have been supplied yet.")

    risk_distribution = {
        severity: sum(risk["severity"] == severity for risk in risks)
        for severity in ("High", "Medium", "Low")
    }
    dimensions_filled = sum(score["score"] > 0 for score in scores)

    return {
        "schema_version": 2,
        "report_type": "Rule-based demo analysis (not AI-generated)",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "notice": (
            "This report is a structured review of user-provided inputs. It is not "
            "market research, independent validation, or a prediction of business "
            "success. All scores measure information coverage or description detail."
        ),
        "project_name": project.get("name", ""),
        "executive_summary": (
            f"The brief includes {len(completed)} of {len(CONTEXT_FIELDS)} tracked "
            f"information fields ({coverage}% coverage). This percentage measures "
            "documentation only, not idea quality or viability."
        ),
        "score_explanation": (
            "Each 0-3 score follows the dimension-specific rule shown beside it. "
            "Scores indicate only whether information was supplied and its amount "
            "of detail; they are not scientific, validated, predictive, or a measure "
            "of commercial potential."
        ),
        "experiment_priority_explanation": (
            "Priority order is a rule-based planning aid: High = 3, Medium = 2, "
            "Low = 1. Missing problem/customer/competitor/business-model inputs "
            "raise the related experiment's priority. It is not a measured "
            "probability or predicted outcome."
        ),
        "assessment_scores": scores,
        "input_completeness": {
            "completed_fields": len(completed),
            "total_fields": len(CONTEXT_FIELDS),
            "percentage": coverage,
            "completed": completed,
            "missing": missing,
            "meaning": "Input completeness only; not a success or viability score.",
        },
        "dimension_coverage": {
            "dimensions_with_any_input": dimensions_filled,
            "total_dimensions": len(scores),
            "meaning": "Count of report dimensions with supplied data, not a quality score.",
        },
        "problem_and_solution_assessment": {
            "problem_statement": problem or "Not supplied.",
            "problem_detail_score": scores[0]["score"],
            "proposed_solution": solution or "Not supplied.",
            "solution_detail_score": scores[2]["score"],
            "relevance_assessment": (
                "Solution-to-problem fit cannot be established from the brief alone; "
                "test it with target customers."
            ),
        },
        "customer_analysis": {
            "target_customers": customers or "Not supplied.",
            "industry": project.get("industry", "").strip() or "Not supplied.",
            "geographic_market": project.get("geography", "").strip() or "Not supplied.",
            "assessment": (
                "Customer details reflect founder input only; segment size, need, "
                "and purchasing behavior have not been independently established."
            ),
        },
        "competitor_comparison": competitor_records,
        "business_model_considerations": {
            "description": business_model or "Not supplied.",
            "assessment": (
                "Revenue model, pricing, costs, and delivery assumptions require "
                "customer and operational validation."
            ),
        },
        "strengths_of_brief": strengths,
        "weaknesses_of_brief": weaknesses,
        "risk_distribution": risk_distribution,
        "founder_provided_information": founder_inputs,
        "competitors_and_alternatives": competitor_records,
        "manually_entered_sources": source_records,
        "assumptions_to_validate": assumptions,
        "risks_and_uncertainties": risks,
        "risks_and_missing_information": risks,
        "missing_information": missing,
        "evidence_and_research_references": source_records,
        "ai_interpretations": (
            "None. No AI provider is configured; this report is rule-based."
        ),
        "recommendations": recommendations,
        "recommended_next_steps": [
            "Review the missing brief fields and add only information you can support.",
            "Run problem-discovery interviews before building or making market claims.",
            "Record alternatives and research references with clear provenance.",
            "Set experiment decision criteria before collecting results.",
        ],
        "validation_experiments": experiments,
    }
