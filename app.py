import logging

import streamlit as st
from sqlalchemy.exc import SQLAlchemyError

from config.settings import get_settings
from database.init_db import initialize_database
from ui.components import PAGES, apply_requested_navigation
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

st.set_page_config(page_title=settings.app_name, layout="wide")

try:
    initialize_database()
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

with st.sidebar:
    st.title(settings.app_name)
    st.caption("Better Questions. Stronger Ideas.")
    page = st.selectbox("Navigate", PAGES, key="page_nav")
    st.divider()
    st.caption("Local demo mode · No login or live research")

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
else:
    render_project_workspace()
