import streamlit as st


def render_my_projects_view():
    """Render the My Projects workspace view with project cards or honest empty state."""

    if "projects" not in st.session_state:
        st.session_state["projects"] = []

    projects = st.session_state["projects"]

    st.title("📁 My Projects")
    st.caption("Startup idea workspaces and validation records")
    st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)

    if not projects:
        st.markdown(
            """
            <div class="vl-card" style="text-align: center; padding: 40px 24px; margin-bottom: 20px;">
                <div style="font-size: 2.2rem; margin-bottom: 8px;">📁</div>
                <h3 style="font-weight: 700; margin-bottom: 8px;">No projects saved yet</h3>
                <p style="max-width: 520px; margin: 0 auto 16px auto; opacity: 0.8; font-size: 0.95rem;">
                    Your saved startup idea projects will appear here once created. Database persistence
                    (Milestone 3: PostgreSQL & SQLAlchemy) is pending; active projects are preserved during this session.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, _ = st.columns([1.8, 4.2])
        with col1:
            if st.button("＋ Create Your First Project", key="my_proj_empty_create_btn", type="primary", use_container_width=True):
                st.session_state["nav_page"] = "Create Project"
                st.rerun()
        return

    # Filter / Action bar
    f_col1, f_col2, f_col3 = st.columns([3, 1.6, 1.4])
    with f_col1:
        search_term = st.text_input("Search Projects", placeholder="Filter by project name, ICP, or problem...", label_visibility="collapsed")
    with f_col2:
        category_filter = st.selectbox(
            "Filter Category",
            ["All Categories"] + sorted(list(set(p.get("category", "Other") for p in projects))),
            label_visibility="collapsed",
        )
    with f_col3:
        if st.button("＋ New Project", key="my_proj_top_new_btn", type="primary", use_container_width=True):
            st.session_state["nav_page"] = "Create Project"
            st.rerun()

    # Filter projects
    filtered = projects
    if search_term.strip():
        term = search_term.lower()
        filtered = [
            p for p in filtered
            if term in p.get("name", "").lower()
            or term in p.get("icp", "").lower()
            or term in p.get("problem", "").lower()
        ]

    if category_filter != "All Categories":
        filtered = [p for p in filtered if p.get("category") == category_filter]

    st.markdown(f"<div style='font-size: 0.82rem; opacity: 0.7; margin-top: 10px; margin-bottom: 16px;'>Showing {len(filtered)} of {len(projects)} registered projects (In-memory session storage)</div>", unsafe_allow_html=True)

    # Render Project Cards
    for idx, proj in enumerate(filtered):
        with st.container():
            st.markdown(
                f"""
                <div class="vl-card" style="margin-bottom: 14px; padding: 22px 24px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                        <div>
                            <span class="vl-badge">{proj.get("category", "General")}</span>
                            <span class="vl-badge" style="margin-left: 6px;">STAGE {proj.get("milestone_stage", 1)}: {proj.get("milestone_name", "Idea Ingestion").upper()}</span>
                            <h3 style="margin-top: 8px; margin-bottom: 4px; font-weight: 700;">{proj.get("name", "Untitled Idea")}</h3>
                            <div style="font-size: 0.8rem; opacity: 0.7;">Created: {proj.get("created_at", "Recently")} · ICP: {proj.get("icp", "General Target")}</div>
                        </div>
                        <span class="vl-badge" style="background: rgba(59, 102, 222, 0.1); color: #3B66DE; border-color: rgba(59, 102, 222, 0.3);">
                            {proj.get("status", "In Validation")}
                        </span>
                    </div>
                    <div style="font-size: 0.92rem; line-height: 1.5; margin-bottom: 12px;">
                        <strong>Core Problem:</strong> {proj.get("problem") or "No problem description provided."}
                    </div>
                    <div style="font-size: 0.88rem; line-height: 1.4; opacity: 0.85;">
                        <strong>Riskiest Assumption:</strong> {proj.get("riskiest_assumption") or "Not yet articulated."}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            act_col1, act_col2, _ = st.columns([1.8, 1.2, 3.0])
            with act_col1:
                with st.expander("🔍 View Hypothesis Details"):
                    st.markdown(f"**Proposed 10x Solution:**\n{proj.get('solution') or 'N/A'}")
                    st.markdown(f"**Primary Value Metric:**\n{proj.get('value_metric') or 'N/A'}")
                    st.markdown(f"**Feasibility / Regulatory Risk:**\n{proj.get('feasibility_risk') or 'N/A'}")
                    st.caption("🔒 Analysis note: AI-driven assumption scoring and competitor extraction will connect in Milestones 5 & 6.")

            with act_col2:
                if st.button("🗑️ Delete", key=f"del_proj_{proj.get('id', idx)}", use_container_width=True):
                    st.session_state["projects"] = [p for p in st.session_state["projects"] if p.get("id") != proj.get("id")]
                    st.rerun()

            st.markdown("<hr style='opacity: 0.2; margin: 16px 0 24px 0;' />", unsafe_allow_html=True)
