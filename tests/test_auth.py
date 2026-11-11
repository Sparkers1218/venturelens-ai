import pytest
import ui
from ui.auth import (
    validate_email,
    validate_password,
    validate_login,
    validate_signup,
    validate_reset,
    render_auth_view,
    render_login_screen,
    render_signup_screen,
    render_forgot_password_screen,
)


def test_ui_exports_auth_components():
    assert hasattr(ui, "render_auth_view")
    assert callable(ui.render_auth_view)
    assert hasattr(ui, "validate_login")
    assert callable(ui.validate_login)
    assert hasattr(ui, "validate_signup")
    assert callable(ui.validate_signup)
    assert hasattr(ui, "validate_reset")
    assert callable(ui.validate_reset)


def test_validate_email_success():
    valid_cases = [
        "founder@venturelens.local",
        "alex.rivera@startup.co",
        "cto+earlyaccess@venture-capital.io",
        "user123@sub.domain.com",
    ]
    for email in valid_cases:
        is_valid, err = validate_email(email)
        assert is_valid is True
        assert err is None


def test_validate_email_failures():
    invalid_cases = [
        ("", "Email address is required."),
        ("   ", "Email address is required."),
        ("notanemail", "valid email"),
        ("founder@", "valid email"),
        ("@domain.com", "valid email"),
        ("founder@domain", "valid email"),
    ]
    for email, expected_fragment in invalid_cases:
        is_valid, err = validate_email(email)
        assert is_valid is False
        assert expected_fragment.lower() in err.lower()


def test_validate_password_length():
    valid, err = validate_password("Pass1234")
    assert valid is True
    assert err is None

    empty, err = validate_password("")
    assert empty is False
    assert "required" in err.lower()

    short, err = validate_password("short1")
    assert short is False
    assert "at least 8" in err.lower()


def test_validate_login_valid_and_invalid():
    # Valid login
    valid, errors = validate_login("founder@venturelens.local", "secretpass123")
    assert valid is True
    assert errors == {}

    # Empty inputs
    invalid, errors = validate_login("", "")
    assert invalid is False
    assert "email" in errors
    assert "password" in errors

    # Invalid email format
    invalid_email, errors = validate_login("invalid-email", "validpassword")
    assert invalid_email is False
    assert "email" in errors


def test_validate_signup_full():
    # Valid sign-up
    valid, errors = validate_signup(
        name="Alex Rivera",
        email="alex@venturelens.local",
        password="ValidPassword123",
        confirm_password="ValidPassword123",
    )
    assert valid is True
    assert errors == {}

    # Password mismatch
    mismatch, errors = validate_signup(
        name="Alex Rivera",
        email="alex@venturelens.local",
        password="ValidPassword123",
        confirm_password="DifferentPassword456",
    )
    assert mismatch is False
    assert "confirm_password" in errors
    assert "do not match" in errors["confirm_password"].lower()

    # Short password
    short_pwd, errors = validate_signup(
        name="Alex Rivera",
        email="alex@venturelens.local",
        password="short",
        confirm_password="short",
    )
    assert short_pwd is False
    assert "password" in errors
    assert "at least 8" in errors["password"].lower()

    # Empty name
    no_name, errors = validate_signup(
        name="",
        email="alex@venturelens.local",
        password="ValidPassword123",
        confirm_password="ValidPassword123",
    )
    assert no_name is False
    assert "name" in errors


def test_validate_reset_email():
    valid, errors = validate_reset("founder@venturelens.local")
    assert valid is True
    assert errors == {}

    invalid, errors = validate_reset("not-an-email")
    assert invalid is False
    assert "email" in errors


def test_auth_card_and_divider_css_in_themes():
    for theme_name in ("Light", "Dark"):
        css = ui.get_theme_css(theme_name)
        assert ".vl-auth-card" in css
        assert ".vl-auth-divider" in css
        assert '[data-testid="stCheckbox"]' in css


def test_auth_view_source_has_no_empty_wrapper_box():
    """Ensure render_auth_view does not render an empty markdown card above branding."""
    import inspect
    from ui import auth
    source = inspect.getsource(auth.render_auth_view)
    assert '<div class="vl-auth-card">' not in source
    assert 'st.markdown("</div>"' not in source
