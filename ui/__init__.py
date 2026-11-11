from ui.theme import THEMES, apply_theme, get_theme_css, render_theme_selector
from ui.components import (
    render_dashboard_header,
    render_welcome_section,
    render_overview_cards,
    render_validation_progress_section,
    render_recent_projects_section,
    render_competitor_insights_section,
    render_pro_tip_section,
)
from ui.project_form import render_project_creation_form
from ui.projects_view import render_my_projects_view
from ui.auth import (
    render_auth_view,
    validate_login,
    validate_signup,
    validate_reset,
)
from ui.profile_view import (
    render_profile_view,
    get_user_profile,
    get_initials,
    DEFAULT_PROFILE,
)
from ui.settings_view import (
    render_settings_view,
    get_user_preferences,
    validate_password_change,
    DEFAULT_PREFERENCES,
)
from ui.notifications_view import (
    render_notifications_view,
    get_notifications,
    get_unread_count,
    mark_notification_read,
    mark_all_read,
    clear_all_notifications,
    reset_sample_notifications,
    INITIAL_NOTIFICATIONS,
)

__all__ = [
    "THEMES",
    "apply_theme",
    "get_theme_css",
    "render_theme_selector",
    "render_dashboard_header",
    "render_welcome_section",
    "render_overview_cards",
    "render_validation_progress_section",
    "render_recent_projects_section",
    "render_competitor_insights_section",
    "render_pro_tip_section",
    "render_project_creation_form",
    "render_my_projects_view",
    "render_auth_view",
    "validate_login",
    "validate_signup",
    "validate_reset",
    "render_profile_view",
    "get_user_profile",
    "get_initials",
    "DEFAULT_PROFILE",
    "render_settings_view",
    "get_user_preferences",
    "validate_password_change",
    "DEFAULT_PREFERENCES",
    "render_notifications_view",
    "get_notifications",
    "get_unread_count",
    "mark_notification_read",
    "mark_all_read",
    "clear_all_notifications",
    "reset_sample_notifications",
    "INITIAL_NOTIFICATIONS",
]
