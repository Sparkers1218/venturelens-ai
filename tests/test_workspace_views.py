import pytest
import streamlit as st
import ui
from ui.profile_view import get_initials, DEFAULT_PROFILE, get_user_profile
from ui.settings_view import (
    validate_password_change,
    DEFAULT_PREFERENCES,
    get_user_preferences,
)
from ui.notifications_view import (
    INITIAL_NOTIFICATIONS,
    get_notifications,
    get_unread_count,
    mark_notification_read,
    mark_all_read,
    clear_all_notifications,
    reset_sample_notifications,
)
from ui.theme import get_theme_css


def test_ui_exports_workspace_views():
    """Verify that ui package exports all workspace components and helpers."""
    expected_exports = [
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
    for export_name in expected_exports:
        assert hasattr(ui, export_name), f"ui module must export {export_name}"


def test_get_initials_utility():
    """Verify initials generation logic for varied user name formats."""
    assert get_initials("Alex Rivera") == "AR"
    assert get_initials("Dhruv") == "DH"
    assert get_initials("Mary Jane Watson") == "MW"
    assert get_initials("   Elena   Rostova   ") == "ER"
    assert get_initials("") == "VL"
    assert get_initials("   ") == "VL"


def test_default_profile_schema():
    """Verify DEFAULT_PROFILE includes all expected attributes for workspace rendering."""
    required_keys = [
        "name",
        "email",
        "role",
        "organization",
        "bio",
        "industry",
        "tier",
        "status",
        "member_since",
    ]
    for k in required_keys:
        assert k in DEFAULT_PROFILE, f"DEFAULT_PROFILE must have '{k}' key"
        assert isinstance(DEFAULT_PROFILE[k], str), f"'{k}' should be a string"


def test_validate_password_change():
    """Verify frontend validation logic for user password change."""
    # Empty current password
    valid, errors = validate_password_change("", "NewSecret123!", "NewSecret123!")
    assert not valid
    assert "current_pwd" in errors

    # Empty new password
    valid, errors = validate_password_change("OldSecret123!", "", "")
    assert not valid
    assert "new_pwd" in errors

    # Too short new password (< 8 chars)
    valid, errors = validate_password_change("OldSecret123!", "short", "short")
    assert not valid
    assert "new_pwd" in errors
    assert "at least 8" in errors["new_pwd"].lower()

    # Passwords do not match
    valid, errors = validate_password_change("OldSecret123!", "NewSecret123!", "DifferentSecret123!")
    assert not valid
    assert "confirm_pwd" in errors

    # New password same as current password
    valid, errors = validate_password_change("SamePassword123!", "SamePassword123!", "SamePassword123!")
    assert not valid
    assert "new_pwd" in errors
    assert "different from your current" in errors["new_pwd"].lower()

    # Valid change
    valid, errors = validate_password_change("OldSecret123!", "BrandNewPassword999!", "BrandNewPassword999!")
    assert valid
    assert len(errors) == 0


def test_default_preferences_schema():
    """Verify DEFAULT_PREFERENCES schema and defaults."""
    assert DEFAULT_PREFERENCES["default_landing"] == "Dashboard"
    assert "show_pro_tips" not in DEFAULT_PREFERENCES, "show_pro_tips preference must be removed (permanently enabled)"
    assert "density" not in DEFAULT_PREFERENCES, "Layout density must not be in DEFAULT_PREFERENCES (spacious layout is permanent)"


def test_settings_view_has_no_density_controls():
    """Verify that Account Settings contains no obsolete layout density controls or compact options."""
    import inspect
    from ui import settings_view
    source = inspect.getsource(settings_view)
    assert "Layout Density" not in source, "Layout Density radio control must be removed"
    assert "settings_pref_density" not in source, "settings_pref_density key must be removed"
    assert '"Compact"' not in source and "'Compact'" not in source, "Compact option must be removed"


def test_settings_view_has_no_pro_tip_toggle():
    """Verify that Account Settings contains no checkbox or toggle to disable Founder Pro Tip."""
    import inspect
    from ui import settings_view
    source = inspect.getsource(settings_view)
    assert "show_pro_tips" not in source, "show_pro_tips key must be removed"
    assert "settings_pref_tips" not in source, "settings_pref_tips key must be removed"
    assert "Founder Pro Tip of the Day" not in source, "Pro Tip toggle label must be removed"




def test_notification_state_operations():
    """Verify notification filtering, read toggling, and bulk operations using session_state."""
    # Reset session notifications
    st.session_state["notifications"] = [dict(n) for n in INITIAL_NOTIFICATIONS]

    # Check count
    notifs = get_notifications()
    assert len(notifs) == len(INITIAL_NOTIFICATIONS)
    unread = get_unread_count()
    expected_unread = sum(1 for n in INITIAL_NOTIFICATIONS if not n.get("read", False))
    assert unread == expected_unread

    # Mark specific notification read
    first_id = notifs[0]["id"]
    mark_notification_read(first_id, True)
    assert get_unread_count() == expected_unread - 1

    # Mark all read
    mark_all_read()
    assert get_unread_count() == 0

    # Clear all notifications
    clear_all_notifications()
    assert len(get_notifications()) == 0
    assert get_unread_count() == 0

    # Reset notifications back to default
    reset_sample_notifications()
    assert len(get_notifications()) == len(INITIAL_NOTIFICATIONS)
    assert get_unread_count() == expected_unread


def test_theme_css_contains_workspace_classes():
    """Verify that both Light and Dark theme CSS contain workspace-specific styling."""
    for theme_name in ["Light", "Dark"]:
        css = get_theme_css(theme_name)
        assert ".vl-avatar" in css, f".vl-avatar missing from {theme_name} theme CSS"
        assert ".vl-notification-card" in css, f".vl-notification-card missing from {theme_name} theme CSS"
        assert ".vl-notification-unread" in css, f".vl-notification-unread missing from {theme_name} theme CSS"
