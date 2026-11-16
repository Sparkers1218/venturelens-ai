import pytest

import streamlit as st

from ui.theme import THEMES, apply_theme, get_theme_css


def test_theme_css_applies_distinct_colors_and_accessible_responsive_controls() -> None:
    light_css = get_theme_css("Light")
    dark_css = get_theme_css("Dark")

    assert THEMES["Light"]["background"] in light_css
    assert THEMES["Dark"]["background"] in dark_css
    assert light_css != dark_css
    for css in (light_css, dark_css):
        assert "button:focus-visible" in css
        assert "@media (max-width: 768px)" in css
        assert '[data-testid="stSidebar"]' in css
        assert '[data-testid="stMetric"]' in css


def test_apply_theme_injects_selected_styles(monkeypatch: pytest.MonkeyPatch) -> None:
    injected: list[str] = []
    monkeypatch.setattr(st, "html", injected.append)

    apply_theme("Dark")

    assert len(injected) == 1
    assert THEMES["Dark"]["background"] in injected[0]
    assert "<style>" in injected[0]


def test_unknown_theme_is_reported() -> None:
    with pytest.raises(ValueError, match="Unknown theme"):
        get_theme_css("Sepia")
