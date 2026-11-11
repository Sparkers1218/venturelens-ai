import pytest
from ui.theme import THEMES, get_theme_css, render_theme_selector
import streamlit as st


def test_themes_exist_with_required_keys():
    assert "Light" in THEMES
    assert "Dark" in THEMES

    required_keys = [
        "background",
        "surface",
        "sidebar",
        "text",
        "muted",
        "primary",
        "border",
        "shadow",
        "info_bg",
        "info_text",
        "button_gradient",
    ]

    for theme_name in ("Light", "Dark"):
        theme = THEMES[theme_name]
        for key in required_keys:
            assert key in theme, f"Missing key {key} in {theme_name} theme"


def test_theme_css_contains_pointer_events_header_fix():
    light_css = get_theme_css("Light")
    dark_css = get_theme_css("Dark")

    for css in (light_css, dark_css):
        # Header pointer events must be disabled to prevent click blocking
        assert '[data-testid="stHeader"]' in css
        assert "pointer-events: none !important" in css
        assert "pointer-events: auto !important" in css

        # Metric value and label contrast must be styled
        assert '[data-testid="stMetricValue"]' in css
        assert '[data-testid="stMetricLabel"]' in css

        # Alerts must have custom colors
        assert '[data-testid="stAlert"]' in css

        # Buttons must have background and text color
        assert ".stButton > button" in css

        # Theme selector segmented control styling
        assert ".st-key-vl_theme" in css


def test_theme_css_colors_match_theme_definition():
    dark_css = get_theme_css("Dark")
    assert THEMES["Dark"]["background"] in dark_css
    assert THEMES["Dark"]["text"] in dark_css
    assert THEMES["Dark"]["surface"] in dark_css

    light_css = get_theme_css("Light")
    assert THEMES["Light"]["background"] in light_css
    assert THEMES["Light"]["text"] in light_css
    assert THEMES["Light"]["surface"] in light_css
