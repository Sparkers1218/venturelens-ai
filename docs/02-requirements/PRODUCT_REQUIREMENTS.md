# VentureLens AI — Product Requirements

## 1. Document information and status

| Field | Value |
|---|---|
| Document | Product Requirements Document |
| Project | VentureLens AI |
| Version | 1.0 |
| Status | Proposed; for review |
| Last updated | 2026-11-04 |
| Related charter | [Project Charter](../01-project-charter/PROJECT_CHARTER.md) |

This PRD defines proposed product behavior and MVP acceptance criteria. It is
not evidence that a requirement, architecture component, provider, or workflow
has been implemented or selected. Requirements remain subject to review and
the open decisions in Section 20.

## 2. Product overview

VentureLens AI is intended to help aspiring entrepreneurs investigate startup
ideas through structured analysis, competitor and alternative research,
evidence-backed insights, identification of assumptions and risks, missing
information, and practical, low-cost validation experiments.

The proposed product direction is a Streamlit UI and Python modular monolith.
PostgreSQL with SQLAlchemy and Alembic is the intended persistence direction.
Authentication, AI, research, database hosting, and deployment providers are
open. AI and research integrations must be replaceable through separate
provider-independent adapters.

At the PRD's initial drafting on 2026-11-04, the application was at foundation
stage with a Streamlit landing page, settings module, and initial configuration
tests. That is a historical snapshot, not the current implementation status.
The current local MVP status is summarized in Section 22. The requirements and
acceptance criteria below remain the intended product target; the status
summary does not imply that they have all been met.

## 3. Problem statement

Aspiring founders need help turning an initial idea into a structured
investigation: understanding the problem and target customer, considering
competitors and alternatives, tracking evidence separately from assumptions,
finding gaps and risks, and planning practical ways to learn more. VentureLens
AI should support that process without claiming that an idea is objectively
validated or that a business will succeed.

## 4. Product vision and objectives

**Vision:** Give founders an evidence-aware workspace for asking better
questions about an idea and planning useful next steps, with uncertainty and
the origin of each insight visible.

**Objectives:**

- Capture and organize startup idea projects and their structured context.
- Help users examine competitors, alternatives, relevant sources, risks, and
  missing information.
- Use AI as an assistive analysis tool, not as an authority or success
  predictor.
- Keep user input, external evidence, assumptions, AI interpretations, and
  recommendations distinguishable.
- Help users turn open questions into practical, low-cost experiments.
- Preserve access to project work when optional AI or external research
  services are unavailable.

## 5. Target users and user needs

| User | Needs |
|---|---|
| Aspiring entrepreneurs | Structure an early idea, research its context, and identify useful next steps. |
| Student founders | Organize idea research and make assumptions and evidence visible. |
| Early-stage startup teams | Keep project analysis, sources, competitors, and experiments together. |

The MVP is scoped to individual accounts. Shared workspaces and team
collaboration are not included unless separately approved.

## 6. Product scope

### Proposed MVP scope

- Individual user accounts and private project ownership.
- Dashboard and create, view, edit, and delete startup idea projects.
- Structured problem, solution, target customer, geography, and industry
  information; allow incomplete drafts.
- Manual competitor and alternative management.
- Manual research-source entry and provider-independent external research
  retrieval, subject to provider selection and verification.
- Source metadata, relevance, and provenance.
- AI-assisted structured analysis, subject to provider selection and
  verification.
- Identification of assumptions, risks, missing information, and competitor
  insights.
- Practical validation experiment recommendations with cost/effort caveats.
- Saved analysis versions and source-linked reports.
- Clear loading, empty, error, and unavailable-service states.
- Continued project work during AI or external research outages, as specified
  in Section 15.

### Implementation boundary

Streamlit, Python modular monolith, PostgreSQL, SQLAlchemy, Alembic, OIDC, AI,
and research adapters are design directions, not proof of implementation.
Provider and hosting choices remain open.

## 7. Out-of-scope features and non-goals

- Guaranteeing or objectively certifying startup success, investment returns,
  or business outcomes.
- Replacing legal, financial, investment, or other professional advice.
- Treating AI output as verified fact or external evidence.
- Fabricating citations, research results, market facts, statistics, or
  AI-generated results.
- Marketplace, fundraising, investor matching, or full business operations
  functionality.
- Shared team workspaces, public profiles, and social features.
- Paid-only capabilities or a mandatory paid provider.
- Advanced forecasting, market sizing claims, or automated business-plan
  generation unless separately scoped and evidenced.

## 8. User roles and permissions

| Role | Permissions |
|---|---|
| Individual user | Create and manage only their own idea projects, competitors, sources, analysis versions, and reports. |
| Application operator | Operate the service and its configuration. Access to user project contents is not implied by this role and requires a separately approved operational and privacy policy. |

Authentication provider and account lifecycle are open decisions. The
implemented product must deny access to another user's project data, including
through guessed or altered identifiers. No anonymous or shared-project access
is defined for the MVP.

## 9. Core user journeys and workflows

1. **Start a project:** Sign in, create an idea project, enter as much context
   as available, and save it as a draft even when optional providers are down.
2. **Build context:** Add or update competitors and alternatives manually;
   enter sources manually or request external research when available.
3. **Review provenance:** Inspect source metadata and see whether information
   came from the user, a retrieved source, an assumption, an AI interpretation,
   or a recommendation.
4. **Analyze:** Request AI-assisted analysis of available project information.
   Review identified assumptions, risks, gaps, competitor insights, and
   experiments without interpreting the result as proof of success.
5. **Save and revisit:** Save analysis versions and source-linked reports,
   return to the dashboard, and reopen saved work.
6. **Recover from an outage:** Continue editing and saving, use manual research
   and competitor entry, see which service is unavailable, retry or resume
   analysis later, and keep saved projects and reports accessible.

## 10. Functional requirements

Priorities: **Must** is required for MVP acceptance; **Should** is desirable
for the MVP where feasible; **Could** is optional. Every requirement has
observable acceptance criteria.

| ID | Priority | Requirement | Acceptance criteria |
|---|---|---|---|
| FR-001 | Must | The product shall provide individual user accounts and associate each user's projects with that account. | Given two authenticated test users, each can list and open their own projects; requests by either user for the other's project return an access-denied or not-found result and disclose no project contents. |
| FR-002 | Must | A user shall be able to create, view, edit, and delete their own idea projects. | A test user can perform each operation on an owned project; deletion requires an explicit confirmation and the deleted project is absent from subsequent lists and opens. |
| FR-003 | Must | A project shall capture a title and the idea's problem, solution, target customer, geography, and industry, and support saving incomplete drafts. | A user can save a draft with only a title, reopen it, fill or change each of the five context fields, save, and observe the saved values after reload. |
| FR-004 | Must | A user shall be able to add, view, edit, and remove competitors and alternatives for an owned project. | A manually entered competitor or alternative remains attached to its project after reload; edits persist; removal removes it from the project view. |
| FR-005 | Must | A user shall be able to manually add, view, edit, and remove research-source records without using an external research provider. | With the research adapter unavailable, a user can add a source, reopen it with its entered fields intact, edit it, and remove it. |
| FR-006 | Must | The product shall retrieve external research only through a replaceable research-provider adapter. | Automated adapter contract tests show the application calls the adapter boundary, can substitute a test provider without changing domain behavior, and reports provider failure without fabricating a result. |
| FR-007 | Must | Source records and retrieved findings shall preserve available source metadata and provenance. | For each source record, the interface shows its title or label, publisher when supplied, URL when supplied, retrieval date when applicable, relevance or user relevance note, and whether it was manually entered or externally retrieved; absent values are shown as unavailable, not invented. |
| FR-008 | Must | The product shall provide AI-assisted analysis through a replaceable AI-provider adapter. | Adapter contract tests substitute a test provider; analysis requests and responses are associated with the relevant project and analysis version; provider failure is surfaced as unavailable, not as a successful analysis. |
| FR-009 | Must | Analysis shall identify assumptions, risks, missing information, and competitor insights, and distinguish them from source evidence and user input. | A structured analysis view contains separately labeled sections for user-provided information, external evidence, assumptions, AI interpretations, risks, and recommendations; each generated item is identifiable as AI-generated and links to supporting source records when cited. |
| FR-010 | Must | The product shall support practical validation experiments derived from identified questions or risks. | Each experiment displays the question or risk it addresses, a proposed action, and an estimated cost/effort or an explicit “not estimated” value; the product does not imply that an experiment guarantees a positive outcome. |
| FR-011 | Must | A user shall be able to save and revisit analysis versions and reports for an owned project. | Saving creates a separately identifiable version; reopening an earlier version shows its saved content and source associations rather than silently replacing it with the latest analysis. |
| FR-012 | Must | Reports shall link claims or findings to available source records and clearly label unsourced analysis. | A generated report identifies cited source records and provides their available metadata; a finding without a source is explicitly labeled as an assumption, AI interpretation, recommendation, or unsourced user input, as applicable. |
| FR-013 | Must | The product shall provide a dashboard for listing and opening the user's projects. | The dashboard lists only the signed-in user's projects; each listed project opens its detail view; an account with no projects sees an empty state and a create-project action. |
| FR-014 | Must | The interface shall provide loading, empty, error, and unavailable-service states for applicable workflows. | Automated UI or component tests trigger each state and verify a visible, state-specific message; loading ends in a result, empty, error, or unavailable state rather than an indefinite spinner. |
| FR-015 | Must | When AI or external research is unavailable, the user shall still be able to create, edit, and save idea projects. | With each provider independently forced to fail, a user can create a draft, edit it, save it, reload it, and observe all saved values. |
| FR-016 | Must | When AI or external research is unavailable, the user shall still be able to manually add competitors and research sources. | With each provider independently forced to fail, manual competitor and source entry, edit, save, reload, and removal remain usable. |
| FR-017 | Must | The product shall clearly identify an unavailable AI or research service and shall not fabricate research, sources, market facts, statistics, or AI results. | Forced provider failures display which capability is unavailable and that no result was generated; no fabricated result, source, citation, market claim, or statistic appears in the response or report. |
| FR-018 | Must | Rule-based output shall never be presented as AI-generated output. | A test of every rule-based result confirms its label identifies it as rule-based; it is not shown in an AI-generated section or attributed to an AI provider. |
| FR-019 | Must | The user shall be able to retry or resume an interrupted analysis when its required provider is available. | After a simulated failure, retrying after provider recovery completes an analysis for the same project; existing project data remains unchanged, and the user can distinguish the completed version from the failed attempt. |
| FR-020 | Must | Saved projects and reports shall remain accessible when an AI or research provider is unavailable. | With either provider forced to fail, the user can list and open a previously saved project and report, including their saved contents and source associations. |
| FR-021 | Must | The product shall provide clear confirmation or failure feedback for project and report save operations. | For each tested save, the UI shows success only after persistence confirms completion; on persistence failure it reports failure and does not display a success state. |
| FR-022 | Should | Users should be able to filter or sort their dashboard projects by a small set of useful project attributes. | Applying each implemented filter or sort changes the displayed list predictably and does not expose another user's projects. |
| FR-023 | Should | Users should be able to mark competitors and sources as relevant to a specific analysis. | A saved relevance selection is visible after reopening the project and is reflected in the associated analysis or report. |
| FR-024 | Should | Reports should be exportable in a user-readable format without losing provenance labels. | An exported report retains evidence/user/assumption/AI/recommendation labels and source links present in the in-app report. |
| FR-025 | Could | Users could duplicate an idea project as a separate draft. | A duplicated draft receives a distinct project identifier, remains owned by the same user, and does not overwrite the original. |

## 11. User stories with measurable acceptance criteria

| Story | User story | Acceptance criteria |
|---|---|---|
| US-001 | As a founder, I want to save an incomplete idea so I can develop it over time. | Satisfies FR-002 and FR-003: create a title-only draft, reload it, add all five context fields, and verify persisted values. |
| US-002 | As a founder, I want to record competitors and sources myself so research can continue without integrations. | Satisfies FR-004, FR-005, and FR-016: with both providers unavailable, create, edit, reload, and remove one manual competitor and one manual source. |
| US-003 | As a founder, I want to know where a finding came from so I can judge its relevance. | Satisfies FR-007, FR-009, and FR-012: inspect a report containing each information category and verify source metadata or an explicit missing-source/category label for every item. |
| US-004 | As a founder, I want AI assistance to expose uncertainty rather than declare my idea successful. | Satisfies FR-008 through FR-010: the analysis separates assumptions, risks, missing information, competitor insights, and experiments, and contains no success guarantee. |
| US-005 | As a founder, I want to keep using my project during provider outages. | Satisfies FR-015 through FR-020: force AI and research failures independently and verify project CRUD, manual entries, saved report access, explicit outage messaging, no fabricated output, and a successful retry after recovery. |
| US-006 | As a founder, I want earlier analyses to remain reviewable. | Satisfies FR-011 and FR-012: save two versions, reopen the first, and verify its original content and source links remain unchanged. |
| US-007 | As a founder, I want my project information private to my account. | Satisfies FR-001 and SEC-001: attempt to access another test user's project by direct identifier and verify access is denied without exposing project data. |

## 12. Data and information requirements

The following are proposed logical records, not an implemented schema:

| Record | Minimum information |
|---|---|
| User | Authentication subject/reference and account status required to associate owned data. Avoid storing provider secrets or unnecessary identity data. |
| Idea project | Owner, title, problem, solution, target customer, geography, industry, and creation/update metadata. Context fields may be incomplete on a draft. |
| Competitor or alternative | Owning project, name, user-provided description, and optional source/relevance association. |
| Research source | Owning project, title/label, publisher when available, URL when available, retrieval date when applicable, relevance note/rating, entry method, and source reference/content permitted by provider terms. |
| Analysis version | Owning project, version identity, creation time, inputs considered, provider-independent analysis status, labeled structured output, and source associations. |
| Report | Owning project, saved version/content, generation time, and source links or explicit provenance labels. |
| Validation experiment | Owning project and analysis association, related question/risk, proposed action, and estimated cost/effort or an explicit unknown. |

Requirements:

- Record whether information was user-entered, externally retrieved,
  assumption, AI interpretation, or recommendation.
- Keep retrieval time distinct from user entry/update time.
- Preserve the source/analysis associations needed to reproduce and inspect a
  saved report; do not silently rewrite an earlier version.
- Do not store provider-returned material beyond its verified licensing and
  retention terms.
- Retention duration, deletion semantics, backup handling, and exact schema
  remain Open Decisions.

## 13. Evidence provenance and source attribution requirements

- Every externally retrieved finding must identify its source record and
  include available title, URL, publisher, and retrieval date.
- Manually entered sources must be labeled as user-provided, not represented
  as retrieved or independently verified.
- Missing metadata must be displayed as unavailable; the system must not infer
  or fabricate it.
- Reports must provide source links for cited external evidence and identify
  unlinked content by its correct category.
- Relevance is an assessment, not proof of factual accuracy. The user must be
  able to distinguish user-assessed relevance from provider metadata.
- Provider-specific source claims and limitations must be retained where
  allowed by the selected provider's terms.

## 14. AI output reliability and transparency requirements

- AI is assistive; generated analysis does not objectively validate an idea or
  predict or guarantee startup success.
- Clearly label AI interpretations and recommendations as AI-generated and
  distinguish them from evidence, user statements, and assumptions.
- Link AI claims to available evidence where applicable; identify unsupported
  interpretation as such rather than presenting it as sourced fact.
- Do not invent market facts, statistics, sources, citations, or results.
- Keep provider/model attribution and analysis time where available and
  permitted by provider terms. Unknown attribution must be shown as unknown.
- If an AI provider is unavailable or returns an unusable result, communicate
  that state and do not display a success-shaped empty, fabricated, or
  rule-based result as an AI response.
- Any rule-based assistance must be visibly labeled as rule-based.

## 15. Availability, error handling, and recovery requirements

The following behavior is mandatory when AI or external research services are
unavailable. The outage is scoped to those optional providers; it must not
disable local project workflows or access to persisted data.

| ID | Requirement | Acceptance check |
|---|---|---|
| AV-001 | Provider failure shall not block project create, edit, or save operations. | Force AI failure and research failure separately; create/edit/save/reload a project successfully in both cases. |
| AV-002 | Provider failure shall not block manual competitor or source entry. | Force each provider failure separately; manually create/edit/save/reload/remove a competitor and source. |
| AV-003 | The product shall identify the unavailable capability and communicate that no provider result was produced. | Simulated timeout, provider error, and unavailable configuration each show an explicit status; no result is shown as successful. |
| AV-004 | Provider failure shall not produce fabricated research, citations, market claims, statistics, or AI results. | Inspect response data and saved report after simulated failures; no generated finding or source exists unless returned successfully by a provider or explicitly entered by the user. |
| AV-005 | Rule-based output shall be labeled as rule-based and never as AI output. | Run rule-based path and verify its label and section; verify no AI attribution is emitted. |
| AV-006 | The user shall be able to retry or resume analysis after provider recovery. | Fail a request, restore the provider, retry for the same project, and verify a separately identifiable completed analysis is saved. |
| AV-007 | Saved projects and reports shall remain readable during AI and research outages. | With each provider disabled, list and open existing projects and reports and verify saved content and provenance remain available. |
| AV-008 | Loading and error states shall terminate in an actionable result or status. | Simulate success, timeout, and error; verify loading ends and the user can retry or return to project work in each case. |

The behavior when the persistence database itself is unavailable is separate
and remains an implementation and recovery decision; the product must not
claim a save succeeded without confirmation from persistence.

## 16. Security, privacy, and data ownership requirements

| ID | Requirement | Acceptance criteria |
|---|---|---|
| SEC-001 | The system shall enforce per-user ownership for every project, competitor, source, analysis, experiment, and report read or mutation. | Automated authorization tests attempt cross-user list, read, update, and delete operations for each record type; no operation exposes or changes another user's data. |
| SEC-002 | The system shall not expose credentials or secrets in source control, UI errors, reports, or application logs. | Secret scanning/configuration tests find no committed real credentials; simulated provider errors and logs contain no configured secret values. |
| SEC-003 | The product shall collect and retain only information needed for agreed product functionality and verified provider operation. | Data inventory maps every persisted field to a documented purpose; fields without an approved purpose are excluded before release. |
| SEC-004 | User-visible errors shall not reveal credentials, internal stack traces, or another user's data. | For simulated validation, provider, and authorization failures, the user receives a safe actionable message while sensitive detail is absent from the response. |
| SEC-005 | Project data shall not be sent to an external provider except as necessary for a user-requested operation and under verified provider terms. | Integration tests verify no provider call occurs without the corresponding user action; provider payload fields match the documented minimum for that operation. |

Transport encryption, account recovery, retention period, deletion propagation,
backups, and incident handling require decisions before production release;
they are not assumed to be solved by this PRD.

## 17. Non-functional requirements

| ID | Requirement | Acceptance criteria |
|---|---|---|
| NFR-001 | Development and core MVP workflows shall not require paid software, subscriptions, APIs, or services. | A documented no-payment path completes core project, manual competitor/source, and saved-work workflows using free or open-source options; when no provider meets the cost policy, provider-dependent features can remain unavailable without blocking those workflows. |
| NFR-002 | External providers and infrastructure shall not be adopted until cost, access, and terms are verified. | A provider decision record documents whether access is free, quotas/rate limits, payment-method requirements, overage charges, licensing/terms, and deployment/production restrictions before enabling the integration. |
| NFR-003 | AI and research integrations shall be replaceable without changing product-domain behavior. | Contract tests run the same domain use cases against a test adapter and an adapter implementation; domain tests do not import provider-specific SDKs. |
| NFR-004 | The interface shall make project and provider state understandable without requiring a successful integration. | Automated UI tests verify loading, empty, error, unavailable, and successful states and their user actions. |
| NFR-005 | Saved analysis versions and reports shall be reproducible as stored artifacts. | After a newer version is created, retrieving an older saved version returns the same stored content and source associations. |
| NFR-006 | Requirements and user-facing analysis shall avoid implying certainty not supported by the evidence. | Content review and automated phrase checks confirm no success guarantee; each report separates evidence, assumptions, AI interpretations, and recommendations. |
| NFR-007 | The product shall provide automated tests for ownership, provenance, provider failure, and report-version behavior. | The release test suite contains and passes at least one test for each listed behavior and the failure/recovery cases in Section 15. |

No latency, uptime, throughput, or capacity target has been supplied. Set such
targets only after product and deployment needs are known.

## 18. Success metrics

Track these measures during MVP evaluation; numeric targets are Open and must
not be inferred from this PRD.

| Metric | Measurement |
|---|---|
| Idea-project completion | Share of started projects that users save with the structured idea fields they choose to provide. |
| Analysis usefulness | User feedback on whether the analysis helped identify a next validation step. |
| Provenance completeness | Share of displayed external findings with available source metadata and an explicit provenance label. |
| Outage continuity | Pass rate of the Section 15 outage acceptance scenarios. |
| Recovery | Share of simulated provider failures for which a user can successfully retry/resume after recovery. |
| Data isolation | Pass rate of cross-user authorization tests. |

Set measurement targets, collection method, and privacy safeguards before
using metrics to make release decisions.

## 19. Assumptions, dependencies, and risks

| Type | Item |
|---|---|
| Assumption | The MVP is for aspiring entrepreneurs, student founders, and early-stage startup teams using individual accounts. |
| Assumption | Streamlit and a Python modular monolith remain suitable proposed directions, subject to implementation review. |
| Dependency | Authentication provider and account lifecycle must be selected and verified. |
| Dependency | AI and research providers must be separately selected and must pass the cost, licensing, limits, payment, and deployment review in NFR-002. |
| Dependency | Persistence requires a domain schema, PostgreSQL environment, migration approach, and ownership enforcement. |
| Risk | Provider outages, quota exhaustion, or access restrictions could disrupt analysis; required manual workflows and recovery behavior mitigate this risk. |
| Risk | Incomplete or stale sources and incorrect AI interpretations could mislead users; provenance and uncertainty labels are required. |
| Risk | User ideas may be sensitive; privacy, retention, access, and deletion decisions are required before production. |
| Risk | Free tiers, payment requirements, terms, or overage exposure may change; provider review must be current and rechecked before adoption. |

## 20. Open product and technical decisions

The following are **Open Decisions**, not selections:

- Authentication provider, OIDC configuration, account recovery, and account
  deletion.
- AI provider and model, including whether NVIDIA NIM is suitable after
  verification; no provider is selected.
- External research provider, source coverage, API contract, and attribution
  obligations.
- Hosting and deployment provider, including free-tier limits, payment
  requirements, overages, and production restrictions.
- PostgreSQL hosting/environment and local development setup.
- Domain schema, retention, deletion, backups, and privacy policy.
- How relevance is represented and whether it is user-assessed or supplied by
  a provider.
- Definitions and UX for low-cost experiments, including how estimates are
  derived.
- Numeric success targets and any response-time or availability objectives.
- MVP delivery schedule and acceptance owner.

No external provider is considered approved until its access, quotas/rate
limits, payment-method requirements, overage exposure, licensing and terms,
and deployment restrictions have been checked and recorded.

## 21. MVP release acceptance criteria

The MVP is ready for product review only when all of the following are true:

1. All **Must** requirements in Section 10 and all `AV-*` and `SEC-*`
   requirements pass their stated acceptance criteria.
2. A user can create, edit, save, reopen, and delete an owned project with the
   structured fields and incomplete-draft behavior defined above.
3. Manual competitor and source workflows work independently of external
   providers.
4. Analysis and reports visibly distinguish user input, external evidence,
   assumptions, AI interpretations, and recommendations; available source
   metadata and links are retained.
5. Analysis versions can be saved and reopened without silently overwriting
   earlier versions.
6. Every Section 15 outage and recovery scenario passes for AI and research
   failures independently, including no fabricated results and continued
   access to saved work.
7. Cross-user authorization tests pass for all project-owned record types.
8. Each selected external provider and hosting service has a completed
   verification record satisfying NFR-002 and does not make paid access
   mandatory.
9. Automated tests cover the release-critical domain, provenance, access
   control, report versioning, and provider-unavailability behavior.
10. No unresolved decision is represented in the product or its documentation
    as a finalized provider or implemented capability.

## 22. Current implementation status (2026-11-15)

This table describes the current local MVP, not completion of the full
requirements or acceptance criteria. “Implemented” applies only to the
capability as described in the row; it does not imply authentication,
ownership, provider integration, or production readiness.

| Capability | Status | Current implementation and limits |
|---|---|---|
| Local project storage and project create, edit, delete, and retrieval | Implemented | SQLAlchemy persistence with SQLite by default. Data is local and is not associated with an authenticated user. |
| Dashboard, navigation, project workspace, and project search | Implemented | Streamlit pages read actual saved project/report data. |
| Competitor records | Partially implemented | Users can manually add, list, and remove entries. Editing and independent verification are not implemented. |
| Research-source records | Partially implemented | Users can manually add, list, and remove source notes. No source is automatically retrieved or verified; editing is not implemented. |
| Rule-based analysis and report generation | Implemented | Deterministic output is labeled as rule-based, not AI-generated. Scores describe information coverage/detail, not market viability. |
| Risks, assumptions, customer analysis, competitor comparison, and validation experiments | Partially implemented | These are input-grounded rules, generic hypotheses, manual-record displays, and recommendations; they are not external research or independently validated findings. |
| Saved reports, JSON download, and charts | Implemented | Reports are saved and can be reopened/downloaded as JSON; charts use application data. |
| Evidence provenance | Partially implemented | User-provided and manually entered records are labeled unverified. External retrieved evidence and provider metadata are not available. |
| Authentication and per-user project ownership/isolation | Not implemented | There is no login, user identity, owner field, or per-user authorization. |
| AI-provider integration | Not implemented | No AI provider or adapter is configured. |
| Live research-provider integration | Not implemented | Research entry is manual only. |
| Provider outage/retry and recovery behavior | Not implemented | No AI or research provider exists to fail or recover. |
| PostgreSQL integration | Not verified | A PostgreSQL URL/driver is configurable, but no PostgreSQL integration run is verified. |
| Production, shared-user, mobile, and full accessibility behavior | Not verified | The MVP is restricted to a controlled local, single-user demonstration; these deployment and UI conditions have not been verified. |

The existing recorded test baseline is 9 passed and 0 failed. Tests were not
rerun for this documentation-only update. The current MVP does not satisfy all
Must requirements or the complete release acceptance criteria in Section 21.
