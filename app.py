import streamlit as st

from config.settings import get_settings
from ui import (
    apply_theme,
    render_dashboard_header,
    render_welcome_section,
    render_overview_cards,
    render_validation_progress_section,
    render_recent_projects_section,
    render_competitor_insights_section,
    render_pro_tip_section,
    render_project_creation_form,
    render_my_projects_view,
    render_auth_view,
    render_profile_view,
    render_settings_view,
    render_notifications_view,
)


settings = get_settings()

st.set_page_config(
    page_title=f"{settings.app_name} · Command Center",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Top Dashboard Header: Notifications bell, Theme controls, Founder profile
theme = render_dashboard_header()
apply_theme(theme)

NAV_LABELS = {
    "Dashboard": "📊 Dashboard",
    "My Projects": "📁 My Projects",
    "Create Project": "＋ Create Project",
    "Competitor Insights": "🎯 Competitor Insights",
    "Research": "🔬 Research",
    "Notifications": "🔔 Notifications",
    "Profile": "👤 Profile",
    "Account Settings": "⚙️ Account Settings",
    "Sign In / Sign Up": "🔐 Sign In / Sign Up",
    "Logout": "🚪 Logout",
}

NAV_OPTIONS = list(NAV_LABELS.keys())

# Ensure session state navigation key is initialized
if "nav_page" not in st.session_state:
    st.session_state["nav_page"] = "Dashboard"

# Sidebar Navigation
with st.sidebar:
    st.title("🔎 VentureLens AI")
    st.caption("Better Questions. Stronger Ideas.")
    st.caption("Sidebar can be collapsed via « at top left")

    st.divider()

    st.subheader("Intelligence Workspace")

    page = st.radio(
        "Navigation",
        NAV_OPTIONS,
        format_func=lambda x: NAV_LABELS.get(x, x),
        label_visibility="collapsed",
        key="nav_page",
    )

    st.divider()
    st.caption("🟢 Guest Founder (Offline)")
    st.caption("Milestone 1: Project Foundation")
    st.caption("Frontend preview · Backend integrations pending")


# Main Dashboard
if page == "Dashboard":
    # 1. Welcome section
    render_welcome_section()

    st.divider()

    # 2. Project overview cards
    render_overview_cards()

    st.divider()

    # 3. Startup Validation Progress pipeline
    render_validation_progress_section()

    st.divider()

    # 4 & 5. Recent Projects & Competitor Insights in a 2-column layout
    left_col, right_col = st.columns(2)

    with left_col:
        render_recent_projects_section()

    with right_col:
        render_competitor_insights_section()

    st.divider()

    # 6. Founder Pro Tip section
    render_pro_tip_section()

elif page == "My Projects":
    render_my_projects_view()

elif page == "Create Project":
    st.title("＋ Create a New Project")
    st.caption("Define your startup idea and initialize validation hypotheses")
    render_project_creation_form()

elif page == "Competitor Insights":
    st.title("🎯 Competitor Insights")
    st.caption("Market radar, competitor positioning, and whitespace discovery")
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
    render_competitor_insights_section(show_header=False)

elif page == "Research":
    st.title("🔬 Research Workspace")
    st.caption("Empirical market signals, search trends, and evidence attribution")
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
    st.info("ℹ️ External research provider integration is pending (Milestone 5). Research queries will be processed once provider API keys and source attribution contracts are configured.")

elif page == "Notifications":
    render_notifications_view()

elif page == "Profile":
    render_profile_view()

elif page == "Account Settings":
    render_settings_view()

elif page == "Sign In / Sign Up":
    render_auth_view()

elif page == "Logout":
    st.title("🚪 Session")
    st.caption("Authentication session status")

    st.warning("You are currently in guest preview mode. No persistent session credentials exist to terminate.")

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    b1, b2, _ = st.columns([1.6, 1.6, 2.8])
    with b1:
        if st.button("🔐 Go to Sign In", key="btn_logout_to_auth", type="primary", use_container_width=True):
            st.session_state["nav_page"] = "Sign In / Sign Up"
            st.session_state["auth_mode"] = "login"
            st.rerun()
    with b2:
        if st.button("Return to Dashboard", key="btn_logout_back", use_container_width=True):
            st.session_state["nav_page"] = "Dashboard"
            st.rerun()
