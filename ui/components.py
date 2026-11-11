import streamlit as st
from ui.notifications_view import get_unread_count, get_notifications, mark_all_read
from ui.profile_view import get_user_profile


PRO_TIPS = [
    {
        "quote": "Validate your riskiest assumption first. If your core hypothesis fails, auxiliary features don't matter.",
        "author": "Riskiest Assumption Test (RAT)",
        "tag": "De-Risking",
    },
    {
        "quote": "Customers rarely know what solution they want, but they always know what hurts. Listen for unsolved friction, not feature requests.",
        "author": "Problem Discovery Principle",
        "tag": "Customer Insight",
    },
    {
        "quote": "A competitor with 10x more capital is not 10x faster. Speed of customer learning is the ultimate asymmetric moat.",
        "author": "Competitive Dynamics",
        "tag": "Market Strategy",
    },
    {
        "quote": "Set falsifiable validation benchmarks before gathering evidence to protect yourself from confirmation bias.",
        "author": "Scientific Validation",
        "tag": "Hypothesis Testing",
    },
    {
        "quote": "Don't ask customers if they would buy it. Ask what they currently do, how much they currently pay, and when they last tried to solve it.",
        "author": "The Mom Test Philosophy",
        "tag": "Customer Discovery",
    },
]


def render_dashboard_header() -> str:
    """Render the dashboard top toolbar with notifications, theme selector, and founder profile."""

    if "vl_theme" not in st.session_state:
        st.session_state["vl_theme"] = "Light"

    current = st.session_state.get("vl_theme", "Light")
    options = ["Light", "Dark"]
    default_index = options.index(current) if current in options else 0

    col_brand, col_bell, col_theme, col_profile = st.columns([4.2, 0.7, 1.8, 1.3])

    with col_brand:
        st.caption("🔎 VentureLens AI · Intelligence Command Center")

    with col_bell:
        unread = get_unread_count()
        with st.popover(f"🔔 {unread}", help="Notifications & Alerts"):
            st.subheader(f"🔔 Notifications ({unread})")
            st.caption("Intelligence Alert Stream")

            all_notifs = get_notifications()
            recent_notifs = all_notifs[:3]

            if recent_notifs:
                for n in recent_notifs:
                    status_dot = "🔵" if not n.get("read", False) else "⚪"
                    st.markdown(
                        f"""
                        <div style="font-size: 0.85rem; padding: 6px 0; border-bottom: 1px solid rgba(128,128,128,0.2);">
                            <div><strong>{status_dot} {n.get('icon', '🔔')} {n.get('title', '')}</strong></div>
                            <div style="font-size: 0.78rem; opacity: 0.75; margin-left: 20px;">{n.get('timestamp', '')} · {n.get('category', '')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                if unread > 0:
                    if st.button("Mark all as read", key="pop_btn_mark_read", use_container_width=True):
                        mark_all_read()
                        st.rerun()
            else:
                st.info("No notifications in inbox.")

            st.markdown("<div style='margin-top: 6px;'></div>", unsafe_allow_html=True)
            if st.button("Open Notifications Center", key="pop_btn_open_notifs", use_container_width=True):
                st.session_state["nav_page"] = "Notifications"
                st.rerun()

    with col_theme:
        theme = st.radio(
            "Appearance",
            options=options,
            index=default_index,
            format_func=lambda opt: "☀️ Light" if opt == "Light" else "🌙 Dark",
            horizontal=True,
            label_visibility="collapsed",
            key="vl_theme",
        )

    with col_profile:
        profile = get_user_profile()
        prof_name = profile.get("name", "Guest Founder")
        prof_email = profile.get("email", "guest@venturelens.local")
        prof_role = profile.get("role", "Founder")
        with st.popover("👤 Founder", help="Account & Session"):
            st.subheader(prof_name)
            st.caption(prof_email)
            st.caption(f"🟢 Status: {prof_role} (Active Session)")
            st.divider()
            st.caption("Milestone 3: User Workspace UI")
            st.caption("Authentication & per-user tenancy will be integrated in Milestone 4 (OIDC).")
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            if st.button("🔐 Sign In / Register", key="pop_btn_auth", type="primary", use_container_width=True):
                st.session_state["nav_page"] = "Sign In / Sign Up"
                st.session_state["auth_mode"] = "login"
                st.rerun()
            st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
            if st.button("Open Profile", key="pop_btn_profile", use_container_width=True):
                st.session_state["nav_page"] = "Profile"
                st.rerun()
            st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
            if st.button("Account Settings", key="pop_btn_settings", use_container_width=True):
                st.session_state["nav_page"] = "Account Settings"
                st.rerun()

    return theme


def render_welcome_section():
    """Render the welcome hero banner with tagline, description, and primary CTA."""

    st.markdown(
        """
        <div class="vl-hero-card">
            <span class="vl-badge">COMMAND CENTER · PREVIEW</span>
            <h1 style="margin-top: 10px; margin-bottom: 4px; font-size: 2rem; font-weight: 800;">
                Welcome to VentureLens AI 👋
            </h1>
            <p style="font-size: 1.15rem; font-weight: 600; margin-bottom: 12px; color: inherit; opacity: 0.9;">
                Better Questions. Stronger Ideas.
            </p>
            <p style="max-width: 820px; line-height: 1.6; margin-bottom: 6px; font-size: 0.95rem; opacity: 0.85;">
                Your startup intelligence workspace. Explore ideas, examine evidence, stress-test critical assumptions,
                and plan validation cycles before writing production code.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    btn_col1, btn_col2, _ = st.columns([1.8, 2.0, 3.2])
    with btn_col1:
        if st.button("＋ Create New Project", key="hero_create_proj_btn", type="primary", use_container_width=True):
            st.session_state["nav_page"] = "Create Project"
            st.rerun()

    with btn_col2:
        with st.popover("📖 Validation Playbook", use_container_width=True):
            st.subheader("VentureLens AI Validation Framework")
            st.markdown(
                """
                1. **Idea Ingestion**: Articulate the core problem, user segment, and value hypothesis.
                2. **Assumption Mapping**: Dissect assumptions into Value, Growth, Feasibility, and Viability.
                3. **Evidence Gathering**: Synthesize web research, competitor benchmarks, and empirical signals.
                4. **Risk Stress-Testing**: Probe vulnerabilities, market head-winds, and operational risks.
                5. **Conviction Scoring**: Generate an evidence-backed score and actionable validation roadmap.
                """
            )

    st.markdown("<div style='margin-bottom: 4px;'></div>", unsafe_allow_html=True)


def render_overview_cards():
    """Render the 4 project overview metric cards with hybrid skeuomorphic styling."""

    st.subheader("Project Overview")
    st.caption("High-level metrics across registered venture ideas and validation cycles")
    st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

    projects = st.session_state.get("projects", [])
    total_projects = len(projects)
    active_projects = sum(1 for p in projects if p.get("status") == "In Validation")
    val_progress_label = f"Stage 1 / 5" if total_projects > 0 else "—"
    val_subtext = f"{active_projects} in progress" if total_projects > 0 else "0 of 5 milestones reached"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="vl-stat-box">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; opacity: 0.75;">Total Projects</span>
                    <span style="font-size: 1.2rem;">📁</span>
                </div>
                <div style="font-size: 2rem; font-weight: 800; line-height: 1.1; margin-bottom: 6px;">{total_projects}</div>
                <div style="font-size: 0.8rem; opacity: 0.7;">{total_projects} projects registered</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="vl-stat-box">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; opacity: 0.75;">Active Projects</span>
                    <span style="font-size: 1.2rem;">⚡</span>
                </div>
                <div style="font-size: 2rem; font-weight: 800; line-height: 1.1; margin-bottom: 6px;">{active_projects}</div>
                <div style="font-size: 0.8rem; opacity: 0.7;">{active_projects} in validation cycle</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="vl-stat-box">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; opacity: 0.75;">Validation Progress</span>
                    <span style="font-size: 1.2rem;">🎯</span>
                </div>
                <div style="font-size: 2rem; font-weight: 800; line-height: 1.1; margin-bottom: 6px;">{val_progress_label}</div>
                <div style="font-size: 0.8rem; opacity: 0.7;">{val_subtext}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
            <div class="vl-stat-box">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; opacity: 0.75;">Research Reports</span>
                    <span style="font-size: 1.2rem;">📊</span>
                </div>
                <div style="font-size: 2rem; font-weight: 800; line-height: 1.1; margin-bottom: 6px;">0</div>
                <div style="font-size: 0.8rem; opacity: 0.7;">Provider integration pending</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_validation_progress_section():
    """Render the startup validation progress pipeline and milestone presentation."""

    st.subheader("Startup Validation Progress")
    st.caption("VentureLens AI 5-stage conviction pipeline · Tracks hypotheses from concept to investor readiness.")

    projects = st.session_state.get("projects", [])
    if projects:
        active_proj = projects[0]
        progress_val = 20
        progress_text = f"Validation Pipeline: 20% complete · Active Idea: {active_proj.get('name', 'Untitled')}"
        stage1_status = "In Progress"
        stage1_desc = f"Concept: {active_proj.get('name')}"
    else:
        progress_val = 0
        progress_text = "Validation Pipeline: 0% complete · Awaiting project initiation"
        stage1_status = "Awaiting Project"
        stage1_desc = "Draft concept & problem scope"

    st.markdown("<div style='margin-top: 8px; margin-bottom: 12px;'></div>", unsafe_allow_html=True)
    st.progress(progress_val, text=progress_text)
    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    milestones = [
        ("1. Idea Ingestion", "💡", stage1_status, stage1_desc),
        ("2. Assumptions", "🧩", "Pending", "Map Value & Feasibility assumptions"),
        ("3. Market Evidence", "🔎", "Pending", "Synthesize competitor & search signals"),
        ("4. Risk Stress-Test", "⚠️", "Pending", "Flaw discovery & vulnerability score"),
        ("5. Conviction Report", "🏆", "Pending", "Evidence-backed validation scorecard"),
    ]

    for col, (title, icon, status, desc) in zip([col1, col2, col3, col4, col5], milestones):
        with col:
            st.markdown(
                f"""
                <div class="vl-step-box">
                    <div style="font-size: 1.3rem; margin-bottom: 4px;">{icon}</div>
                    <div style="font-size: 0.85rem; font-weight: 700; margin-bottom: 4px;">{title}</div>
                    <div style="font-size: 0.72rem; opacity: 0.7; margin-bottom: 6px;">{desc}</div>
                    <span class="vl-badge" style="font-size: 0.65rem; padding: 2px 6px;">{status}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    if not projects:
        st.info("ℹ️ Honest empty state: No active validation cycle in progress. Create your first startup project to begin hypothesis tracking and automated risk analysis.")
    else:
        st.caption(f"Currently tracking active idea: **{projects[0].get('name')}** (In-memory preview mode · Milestone 1).")


def render_recent_projects_section():
    """Render the recent projects section with professional layout and clear empty state."""

    st.subheader("Recent Projects")
    st.caption("Active validation workspaces and recent idea submissions")

    projects = st.session_state.get("projects", [])

    if not projects:
        st.markdown(
            """
            <div class="vl-card" style="text-align: center; padding: 36px 24px; margin-bottom: 16px;">
                <div style="font-size: 2.2rem; margin-bottom: 8px;">📂</div>
                <h3 style="margin-bottom: 6px; font-weight: 700;">No startup projects yet</h3>
                <p style="max-width: 540px; margin: 0 auto 18px auto; opacity: 0.8; font-size: 0.92rem; line-height: 1.5;">
                    Start by creating your first idea workspace. You will be able to log assumptions, track competitor movements,
                    and receive evidence-backed research reports.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        p_col1, p_col2 = st.columns([1.8, 3.2])
        with p_col1:
            if st.button("＋ Start First Project", key="recent_proj_create_btn", use_container_width=True):
                st.session_state["nav_page"] = "Create Project"
                st.rerun()

        with p_col2:
            st.caption("🔒 Storage note: Database persistence is in progress (Milestone 3: PostgreSQL & SQLAlchemy). Projects will be saved once persistence is wired.")
    else:
        for proj in projects[:3]:
            st.markdown(
                f"""
                <div class="vl-card" style="margin-bottom: 12px; padding: 18px 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span class="vl-badge">{proj.get("category", "General")}</span>
                        <span style="font-size: 0.75rem; opacity: 0.7;">{proj.get("created_at", "Recently")}</span>
                    </div>
                    <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 4px;">{proj.get("name", "Untitled")}</div>
                    <div style="font-size: 0.84rem; opacity: 0.8; margin-bottom: 8px; line-height: 1.4;">
                        {(proj.get("problem", "")[:140] + ('...' if len(proj.get("problem", "")) > 140 else '')) or 'No problem summary'}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem; opacity: 0.85;">
                        <span>Stage {proj.get("milestone_stage", 1)}: {proj.get("milestone_name", "Idea Ingestion")}</span>
                        <span style="color: #3B66DE; font-weight: 600;">{proj.get("status", "Active")}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns([1.5, 1.5])
        with c1:
            if st.button("📁 View in My Projects", key="btn_view_all_proj", use_container_width=True):
                st.session_state["nav_page"] = "My Projects"
                st.rerun()
        with c2:
            if st.button("＋ New Project", key="btn_recent_new_proj", use_container_width=True):
                st.session_state["nav_page"] = "Create Project"
                st.rerun()


def render_competitor_insights_section(show_header: bool = True):
    """Render the competitor insights panel with capability preview cards and honest status."""

    if show_header:
        st.subheader("Competitor Insights")
        st.caption("Market radar and competitor landscape intelligence")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="vl-stat-box">
                <div style="font-size: 1.3rem; margin-bottom: 6px;">🔍</div>
                <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 4px;">Automated Discovery</div>
                <div style="font-size: 0.82rem; opacity: 0.8; line-height: 1.4;">
                    Identify direct, indirect, and asymmetric competitors across real-time web signals.
                </div>
                <div style="margin-top: 12px;">
                    <span class="vl-badge">FEATURE PREVIEW</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="vl-stat-box">
                <div style="font-size: 1.3rem; margin-bottom: 6px;">📊</div>
                <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 4px;">Positioning & Gap Matrix</div>
                <div style="font-size: 0.82rem; opacity: 0.8; line-height: 1.4;">
                    Visualize competitor strengths, vulnerabilities, and underserved customer segments.
                </div>
                <div style="margin-top: 12px;">
                    <span class="vl-badge">FEATURE PREVIEW</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div class="vl-stat-box">
                <div style="font-size: 1.3rem; margin-bottom: 6px;">⚡</div>
                <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 4px;">Feature & Moat Radar</div>
                <div style="font-size: 0.82rem; opacity: 0.8; line-height: 1.4;">
                    Analyze competing feature velocity, pricing tiers, and defensible moats.
                </div>
                <div style="margin-top: 12px;">
                    <span class="vl-badge">FEATURE PREVIEW</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    st.info("ℹ️ Research status: Competitor discovery and market landscape feeds will connect during Milestone 5 (Research Integration). No external queries are performed in offline preview mode.")


def render_pro_tip_section():
    """Render the compact, visually appealing startup validation pro tip card."""

    if "pro_tip_idx" not in st.session_state:
        st.session_state["pro_tip_idx"] = 0

    tip_idx = st.session_state["pro_tip_idx"] % len(PRO_TIPS)
    tip = PRO_TIPS[tip_idx]

    st.subheader("💡 Founder Pro Tip")
    st.caption("Actionable principles for hypothesis testing and problem discovery")

    st.markdown(
        f"""
        <div class="vl-pro-tip">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span class="vl-badge">{tip["tag"]}</span>
                <span style="font-size: 0.78rem; opacity: 0.7;">Tip {tip_idx + 1} of {len(PRO_TIPS)}</span>
            </div>
            <p style="font-size: 1.05rem; font-style: italic; font-weight: 600; line-height: 1.55; margin-bottom: 10px;">
                "{tip["quote"]}"
            </p>
            <div style="font-size: 0.82rem; font-weight: 700; opacity: 0.85;">
                — {tip["author"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    t_col1, _ = st.columns([1.8, 4.2])
    with t_col1:
        if st.button("🎲 Next Insight", key="btn_next_tip", use_container_width=True):
            st.session_state["pro_tip_idx"] = (tip_idx + 1) % len(PRO_TIPS)
            st.rerun()
            st.rerun()
