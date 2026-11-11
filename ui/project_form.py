import time
import streamlit as st


MARKET_CATEGORIES = [
    "Enterprise SaaS",
    "Healthcare & HealthTech",
    "FinTech & InsurTech",
    "Consumer AI & Apps",
    "Developer Tools & Infra",
    "ClimateTech & Clean Energy",
    "E-Commerce & Supply Chain",
    "EdTech & Future of Work",
    "Other",
]


def render_project_creation_form():
    """Render the guided multi-step project creation form with in-memory session persistence."""

    if "projects" not in st.session_state:
        st.session_state["projects"] = []

    if "create_step" not in st.session_state:
        st.session_state["create_step"] = 1

    step = st.session_state["create_step"]

    # Step progress header using clean CSS classes without hardcoded colors
    step_col1, step_col2, step_col3 = st.columns(3)
    with step_col1:
        active_cls = "vl-step-active" if step == 1 else ""
        st.markdown(
            f"""
            <div class="vl-step-box {active_cls}">
                <span class="vl-badge">Step 1</span>
                <div style="font-size: 0.82rem; font-weight: 700; margin-top: 4px;">Concept & ICP</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with step_col2:
        active_cls = "vl-step-active" if step == 2 else ""
        st.markdown(
            f"""
            <div class="vl-step-box {active_cls}">
                <span class="vl-badge">Step 2</span>
                <div style="font-size: 0.82rem; font-weight: 700; margin-top: 4px;">Problem & 10x Value</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with step_col3:
        active_cls = "vl-step-active" if step == 3 else ""
        st.markdown(
            f"""
            <div class="vl-step-box {active_cls}">
                <span class="vl-badge">Step 3</span>
                <div style="font-size: 0.82rem; font-weight: 700; margin-top: 4px;">Assumptions & Risks</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # Initialize draft form state if missing
    if "draft_name" not in st.session_state:
        st.session_state["draft_name"] = ""
    if "draft_category" not in st.session_state:
        st.session_state["draft_category"] = MARKET_CATEGORIES[0]
    if "draft_icp" not in st.session_state:
        st.session_state["draft_icp"] = ""
    if "draft_problem" not in st.session_state:
        st.session_state["draft_problem"] = ""
    if "draft_solution" not in st.session_state:
        st.session_state["draft_solution"] = ""
    if "draft_value_metric" not in st.session_state:
        st.session_state["draft_value_metric"] = ""
    if "draft_riskiest_assumption" not in st.session_state:
        st.session_state["draft_riskiest_assumption"] = ""
    if "draft_feasibility_risk" not in st.session_state:
        st.session_state["draft_feasibility_risk"] = ""

    if step == 1:
        st.subheader("Step 1: Idea Identity & Target Customer")
        st.caption("Anchor your venture concept and identify who suffers most acutely from this friction.")

        st.session_state["draft_name"] = st.text_input(
            "Project / Startup Name",
            value=st.session_state["draft_name"],
            placeholder="e.g. MedScribe AI, FleetPulse, CloudSaver",
            help="Working title for this validation workspace.",
        )

        cat_idx = (
            MARKET_CATEGORIES.index(st.session_state["draft_category"])
            if st.session_state["draft_category"] in MARKET_CATEGORIES
            else 0
        )
        st.session_state["draft_category"] = st.selectbox(
            "Market Category",
            MARKET_CATEGORIES,
            index=cat_idx,
            help="Primary industry sector for benchmark comparison.",
        )

        st.session_state["draft_icp"] = st.text_input(
            "Ideal Customer Profile (ICP)",
            value=st.session_state["draft_icp"],
            placeholder="e.g. Solo clinic doctors, Series A CTOs, Supply chain VP at mid-size retail",
            help="Be specific: who has budget, urgency, and decision-making power?",
        )

        st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns([1.8, 4.2])
        with c1:
            if st.button("Continue to Step 2 ➔", key="step1_next", type="primary", use_container_width=True):
                if not st.session_state["draft_name"].strip():
                    st.error("Please enter a project name to continue.")
                else:
                    st.session_state["create_step"] = 2
                    st.rerun()

    elif step == 2:
        st.subheader("Step 2: Core Problem & Proposed 10x Value Proposition")
        st.caption("Define the expensive, frequent, or urgent friction you are solving.")

        st.session_state["draft_problem"] = st.text_area(
            "Core Problem Statement",
            value=st.session_state["draft_problem"],
            placeholder="Describe the specific pain, current manual workarounds, and why existing tools fail...",
            height=120,
            help="Good problem statements focus on measurable friction, not lack of your feature.",
        )

        st.session_state["draft_solution"] = st.text_area(
            "Proposed 10x Solution Hypothesis",
            value=st.session_state["draft_solution"],
            placeholder="How does your solution eliminate this friction with an asymmetric advantage?...",
            height=120,
        )

        st.session_state["draft_value_metric"] = st.text_input(
            "Primary Value Metric",
            value=st.session_state["draft_value_metric"],
            placeholder="e.g. Reduce report generation time from 4 hours to 8 minutes",
            help="The concrete quantified outcome promised to the customer.",
        )

        st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
        c1, c2, _ = st.columns([1.6, 1.8, 2.6])
        with c1:
            if st.button("⬅ Back to Step 1", key="step2_back", use_container_width=True):
                st.session_state["create_step"] = 1
                st.rerun()
        with c2:
            if st.button("Continue to Step 3 ➔", key="step2_next", type="primary", use_container_width=True):
                st.session_state["create_step"] = 3
                st.rerun()

    elif step == 3:
        st.subheader("Step 3: Critical Assumptions & Riskiest Hypothesis (RAT)")
        st.caption("Decompose what must be true for this business to succeed.")

        st.session_state["draft_riskiest_assumption"] = st.text_area(
            "Riskiest Value Assumption (Must be validated first)",
            value=st.session_state["draft_riskiest_assumption"],
            placeholder="e.g. Doctors are willing to trust AI-generated SOAP notes without line-by-line manual verification...",
            height=100,
            help="What single assumption, if wrong, completely destroys the premise of the business?",
        )

        st.session_state["draft_feasibility_risk"] = st.text_area(
            "Primary Feasibility / Regulatory Risk",
            value=st.session_state["draft_feasibility_risk"],
            placeholder="e.g. HIPAA compliance and EHR integration latency across legacy health systems...",
            height=100,
        )

        st.markdown(
            """
            <div class="vl-card" style="margin: 20px 0; padding: 20px 22px;">
                <span class="vl-badge">VALIDATION READY</span>
                <p style="font-size: 0.88rem; margin-top: 8px; margin-bottom: 8px; opacity: 0.85;">
                    Initializing this project creates an in-memory validation workspace. You can review your hypotheses
                    in the Command Center, track assumptions, and explore competitor benchmarks.
                </p>
                <div style="font-size: 0.78rem; opacity: 0.7;">
                    🔒 Storage note: Database persistence connects in Milestone 3 (PostgreSQL & SQLAlchemy).
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2, _ = st.columns([1.6, 2.0, 2.4])
        with c1:
            if st.button("⬅ Back to Step 2", key="step3_back", use_container_width=True):
                st.session_state["create_step"] = 2
                st.rerun()
        with c2:
            if st.button("🚀 Initialize Project", key="step3_submit", type="primary", use_container_width=True):
                new_project = {
                    "id": f"proj-{int(time.time())}",
                    "name": st.session_state["draft_name"].strip() or "Untitled Idea",
                    "category": st.session_state["draft_category"],
                    "icp": st.session_state["draft_icp"],
                    "problem": st.session_state["draft_problem"],
                    "solution": st.session_state["draft_solution"],
                    "value_metric": st.session_state["draft_value_metric"],
                    "riskiest_assumption": st.session_state["draft_riskiest_assumption"],
                    "feasibility_risk": st.session_state["draft_feasibility_risk"],
                    "created_at": time.strftime("%Y-%m-%d %H:%M"),
                    "status": "In Validation",
                    "milestone_stage": 1,
                    "milestone_name": "Idea Ingestion",
                    "conviction_score": "Pending Evidence",
                }

                st.session_state["projects"].insert(0, new_project)

                # Reset form draft
                st.session_state["draft_name"] = ""
                st.session_state["draft_problem"] = ""
                st.session_state["draft_solution"] = ""
                st.session_state["draft_icp"] = ""
                st.session_state["draft_value_metric"] = ""
                st.session_state["draft_riskiest_assumption"] = ""
                st.session_state["draft_feasibility_risk"] = ""
                st.session_state["create_step"] = 1

                st.session_state["last_created_project"] = new_project["name"]
                st.session_state["nav_page"] = "My Projects"
                st.rerun()
