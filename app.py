import logging

import streamlit as st
from sqlalchemy.exc import SQLAlchemyError

from config.settings import get_settings
from database.demo_data import seed_evaluator_demo
from database.init_db import initialize_database
from ui.components import PAGES, apply_requested_navigation, render_app_header
from ui.views import (
    render_dashboard,
    render_analysis_report_page,
    render_competitor_insights,
    render_new_project,
    render_notifications,
    render_profile,
    render_project_workspace,
    render_projects,
    render_research_page,
    render_settings,
)


LOGGER = logging.getLogger(__name__)
settings = get_settings()

st.set_page_config(
    page_title=f"{settings.app_name} · Command Center",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="auto",
)

if settings.app_env == "production" and not settings.demo_mode:
    st.error(
        "Production startup is disabled unless DEMO_MODE=true. Authenticated "
        "multi-user access is not implemented."
    )
    st.stop()

try:
    initialize_database()
    if settings.demo_mode:
        seed_evaluator_demo()
except SQLAlchemyError as error:
    LOGGER.error(
        "Could not initialize the application database (%s)",
        type(error).__name__,
    )
    st.error(
        "VentureLens could not initialize its database. Check DATABASE_URL and "
        "database permissions, then restart the app."
    )
    st.stop()

apply_requested_navigation()
render_app_header(settings.app_name)
if settings.demo_mode:
    st.warning(
        "PUBLIC EVALUATOR DEMO — fictional synthetic sample data only; read-only; "
        "no authentication or user project data."
    )

PAGE_ICONS = {
    "Dashboard": "📊",
    "My Projects": "📁",
    "Create Project": "＋",
    "Competitor Insights": "🎯",
    "Research": "🔬",
    "Analysis Report": "📈",
    "Notifications": "🔔",
    "Profile": "👤",
    "Settings": "⚙️",
    "Project Workspace": "🗂️",
}

with st.sidebar:
    st.title(f"🔎 {settings.app_name}")
    st.caption("INTELLIGENCE WORKSPACE")
    st.divider()
    page = st.radio(
        "Navigation",
        PAGES,
        format_func=lambda item: f"{PAGE_ICONS[item]}  {item}",
        label_visibility="collapsed",
        key="page_nav",
    )
    st.divider()
    st.caption(
        "Read-only synthetic evaluator demo"
        if settings.demo_mode
        else "Local demo mode · No login or live research"
    )

if page == "Dashboard":
    render_dashboard()
elif page == "My Projects":
    render_projects()
elif page == "Create Project":
    render_new_project()
elif page == "Competitor Insights":
    render_competitor_insights()
elif page == "Research":
    render_research_page()
elif page == "Analysis Report":
    render_analysis_report_page()
elif page == "Notifications":
    render_notifications()
elif page == "Profile":
    render_profile()
elif page == "Settings":
    render_settings()
elif page == "Project Workspace":
    render_project_workspace()
