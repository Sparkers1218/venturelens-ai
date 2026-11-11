import pytest
from ui.components import PRO_TIPS
import ui


def test_pro_tips_structure():
    assert len(PRO_TIPS) >= 3
    for tip in PRO_TIPS:
        assert "quote" in tip and len(tip["quote"]) > 0
        assert "author" in tip and len(tip["author"]) > 0
        assert "tag" in tip and len(tip["tag"]) > 0


def test_ui_exports_all_required_components():
    required_exports = [
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
    ]
    for name in required_exports:
        assert hasattr(ui, name), f"ui module missing export {name}"


def test_theme_css_contains_skeuomorphic_classes():
    for theme_name in ("Light", "Dark"):
        css = ui.get_theme_css(theme_name)
        assert ".vl-hero-card" in css
        assert ".vl-stat-box" in css
        assert ".vl-badge" in css
        assert ".vl-step-box" in css
        assert ".vl-pro-tip" in css


def test_theme_css_contains_spacing_and_layout_rules():
    """Verify that cards, dividers, and alert components contain consistent spacing rules."""
    for theme_name in ("Light", "Dark"):
        css = ui.get_theme_css(theme_name)
        assert "margin-bottom: 18px" in css  # hero card separation
        assert "margin-bottom: 16px" in css  # pro tip and card separation
        assert '[data-testid="stDivider"]' in css
        assert "margin: 1.75rem 0 !important" in css  # divider section rhythm
        assert '[data-testid="stAlert"]' in css
        assert "margin: 1.15rem 0 !important" in css  # alert vertical spacing


def test_competitor_insights_section_accepts_show_header_kwarg():
    """Verify render_competitor_insights_section supports show_header toggle."""
    import inspect
    sig = inspect.signature(ui.render_competitor_insights_section)
    assert "show_header" in sig.parameters
    assert sig.parameters["show_header"].default is True


def test_render_pro_tip_section_is_unconditional():
    """Verify that render_pro_tip_section has no conditional preference gating."""
    import inspect
    source = inspect.getsource(ui.render_pro_tip_section)
    assert "show_pro_tips" not in source, "render_pro_tip_section must not conditionally check show_pro_tips"
    assert "user_preferences" not in source, "render_pro_tip_section must not conditionally read preferences"
