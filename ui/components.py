import streamlit as st
from pydantic import ValidationError

from ui.theme import apply_theme, render_theme_selector


PAGES = (
    "Dashboard",
    "My Projects",
    "Create Project",
    "Competitor Insights",
    "Research",
    "Analysis Report",
    "Notifications",
    "Profile",
    "Settings",
    "Project Workspace",
)


def render_app_header(app_name: str) -> None:
    brand_column, theme_column = st.columns([4, 2], vertical_alignment="center")
    with brand_column:
        st.subheader(f"🔎 {app_name} · Intelligence Workspace")
        st.caption("Better Questions. Stronger Ideas.")
    with theme_column:
        theme = render_theme_selector()
    apply_theme(theme)


def request_navigation(page: str, project_id: str | None = None) -> None:
    if page not in PAGES:
        raise ValueError(f"Unknown page: {page}")
    if project_id is not None:
        st.session_state["selected_project_id"] = project_id
        for key in (
            "workspace_project_select",
            "competitor_page_project",
            "research_page_project",
            "analysis_page_project",
        ):
            st.session_state[key] = project_id
    st.session_state["navigate_to"] = page
    st.rerun()


def apply_requested_navigation() -> None:
    target = st.session_state.pop("navigate_to", None)
    if target in PAGES:
        st.session_state["page_nav"] = target
    if st.session_state.get("page_nav") not in PAGES:
        st.session_state["page_nav"] = "Dashboard"


def show_validation_error(error: ValidationError) -> None:
    messages = [
        f"{'.'.join(str(part) for part in item['loc'])}: {item['msg']}"
        for item in error.errors()
    ]
    st.error("Please correct the following fields:\n\n" + "\n\n".join(messages))
