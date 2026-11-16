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
        assert "@media (max-width: 900px)" in css
        assert "@media (max-width: 380px)" in css
        assert '[data-testid="stSidebar"]' in css
        assert '[data-testid="stMetric"]' in css
        assert (
            '[data-testid="stMetricValue"] [data-testid="stMarkdownContainer"] p'
            in css
        )
        assert "white-space: normal !important" in css
        assert '[data-testid="stHorizontalBlock"] > [data-testid="column"]' in css
        assert '[data-testid="stDataFrame"]' in css
        assert '[data-testid="stVegaLiteChart"] svg text' in css


def _relative_luminance(color: str) -> float:
    channels = [int(color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        channel / 12.92
        if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return sum(
        channel * weight
        for channel, weight in zip(linear, (0.2126, 0.7152, 0.0722))
    )


def _contrast_ratio(foreground: str, background: str) -> float:
    lighter, darker = sorted(
        (_relative_luminance(foreground), _relative_luminance(background)),
        reverse=True,
    )
    return (lighter + 0.05) / (darker + 0.05)


@pytest.mark.parametrize("theme_name", tuple(THEMES))
def test_theme_text_and_primary_buttons_meet_contrast_target(theme_name: str) -> None:
    theme = THEMES[theme_name]

    assert _contrast_ratio(theme["text"], theme["background"]) >= 4.5
    assert _contrast_ratio(theme["muted"], theme["background"]) >= 4.5
    assert _contrast_ratio(theme["primary"], theme["background"]) >= 4.5
    assert _contrast_ratio("#FFFFFF", theme["primary_button"]) >= 4.5
    assert _contrast_ratio("#FFFFFF", theme["primary_button_hover"]) >= 4.5


def test_theme_css_supports_header_controls_and_mobile_columns() -> None:
    css = get_theme_css("Light")

    assert '[data-testid="stHeader"] [data-testid="stToolbar"]' in css
    assert "pointer-events: none !important" in css
    assert "flex-direction: column !important" in css


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
