import pytest
from ui.theme import THEMES, get_theme_css


def test_light_theme_tokens_contain_no_unwanted_black_backgrounds():
    light = THEMES["Light"]

    # Check background tokens used for interactive states
    for token_name in (
        "sidebar_hover",
        "sidebar_selected",
        "button_active_bg",
        "tab_hover",
        "tab_selected_bg",
        "dropdown_hover",
        "dropdown_selected",
    ):
        assert token_name in light, f"Missing token {token_name} in Light theme"
        val = light[token_name].lower()
        assert val not in ("#000", "#000000", "#0e1117", "#101827", "#131720", "#141f31", "#192438"), (
            f"Light theme token {token_name} has black/dark value: {val}"
        )


def test_light_theme_css_has_explicit_sidebar_interactive_states():
    css = get_theme_css("Light")

    # Selected sidebar navigation item
    assert '[data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked)' in css
    # Hover sidebar navigation item
    assert '[data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]:hover' in css
    # Focus sidebar navigation item
    assert '[data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]:focus' in css


def test_light_theme_css_has_explicit_button_interactive_states():
    css = get_theme_css("Light")

    # Secondary / standard button hover, active, focus
    assert ".stButton > button:hover" in css
    assert ".stButton > button:active" in css
    assert ".stButton > button:focus" in css

    # Primary button hover, active, focus
    assert 'button[kind="primary"]:hover' in css
    assert 'button[kind="primary"]:active' in css
    assert 'button[kind="primary"]:focus' in css


def test_light_theme_css_has_explicit_popover_and_tabs_states():
    css = get_theme_css("Light")

    # Popover trigger expanded state (replaces black background when opened)
    assert '[data-testid="stPopover"] > button[aria-expanded="true"]' in css
    assert '[data-testid="stPopover"] > button:hover' in css
    assert '[data-testid="stPopoverBody"]' in css

    # Streamlit Tabs hover and selected states
    assert '[data-testid="stTabs"] button[data-baseweb="tab"]:hover' in css
    assert '[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"]' in css
    assert '[data-baseweb="tab-highlight"]' in css


def test_light_theme_css_has_explicit_dropdown_item_states():
    css = get_theme_css("Light")

    # Dropdown select and option states (BaseWeb legacy + Streamlit 1.66 Virtual Dropdown)
    assert 'div[data-baseweb="select"]' in css
    assert 'li[role="option"]:hover' in css
    assert 'li[role="option"][aria-selected="true"]' in css

    # Streamlit 1.66 selectbox root, virtual dropdown, and emotion target selectors
    assert '[data-testid="stSelectbox"]' in css
    assert '[data-testid="stSelectboxVirtualDropdown"]' in css
    assert 'div[class*="e1oobldh4"]' in css
    assert 'div[class*="e1oobldh7"]' in css
    assert '[data-item-hl]' in css

    # Hover and selected option states with theme tokens
    assert '[data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover' in css
    assert '[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-hovered="true"]' in css
    assert '[data-testid="stSelectboxVirtualDropdown"] [role="option"][aria-selected="true"]' in css
    assert THEMES["Light"]["dropdown_hover"] in css
    assert THEMES["Light"]["dropdown_selected"] in css


def test_dark_theme_dropdown_retains_dark_surface():
    dark_css = get_theme_css("Dark")

    assert '[data-testid="stSelectboxVirtualDropdown"]' in dark_css
    assert THEMES["Dark"]["surface"] in dark_css
    assert THEMES["Dark"]["dropdown_hover"] in dark_css
    assert THEMES["Dark"]["dropdown_selected"] in dark_css


def test_dark_theme_css_retains_dark_interactive_styles():
    dark_css = get_theme_css("Dark")

    assert THEMES["Dark"]["background"] in dark_css
    assert THEMES["Dark"]["sidebar_selected"] in dark_css
    assert THEMES["Dark"]["primary"] in dark_css
    assert '[data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked)' in dark_css


def test_popover_buttons_targeted_with_st_popover_button():
    light_css = get_theme_css("Light")
    assert 'button[data-testid="stPopoverButton"]' in light_css
    assert '[data-testid="stPopover"] button' in light_css
    assert 'button[data-testid="stPopoverButton"]:hover' in light_css
    assert 'button[data-testid="stPopoverButton"][aria-expanded="true"]' in light_css


def test_sidebar_and_theme_radio_circles_are_removed():
    light_css = get_theme_css("Light")
    # Sidebar circle removal
    assert '[data-testid="stSidebar"] [data-testid="stRadioOption"] > div > div:first-child' in light_css
    assert '[data-testid="stSidebar"] [data-testid="stRadioOption"]' in light_css
    # Theme selector segmented switch circle removal
    assert '.st-key-vl_theme [data-testid="stRadioOption"] > div > div:first-child' in light_css
    assert '.st-key-vl_theme [data-testid="stRadioOption"]' in light_css


def test_primary_and_secondary_base_buttons_styled():
    light_css = get_theme_css("Light")
    assert 'button[data-testid="stBaseButton-primary"]' in light_css
    assert 'button[data-testid="stBaseButton-secondary"]' in light_css


def test_tooltip_styling_in_light_and_dark_themes():
    light_css = get_theme_css("Light")
    assert '[data-testid="stTooltipContent"]' in light_css
    assert THEMES["Light"]["surface"] in light_css
    assert THEMES["Light"]["text"] in light_css

    dark_css = get_theme_css("Dark")
    assert '[data-testid="stTooltipContent"]' in dark_css
    assert THEMES["Dark"]["surface"] in dark_css
    assert THEMES["Dark"]["text"] in dark_css


def test_checkbox_square_indicator_styling():
    light_css = get_theme_css("Light")
    assert '[data-testid="stCheckbox"] div[class*="e1ap2qgk"]' in light_css
    assert '[data-testid="stCheckbox"] label:has(input:checked)' in light_css
    assert THEMES["Light"]["primary"] in light_css


def test_password_visibility_button_styling():
    light_css = get_theme_css("Light")
    assert '[data-testid="stTextInput"] button' in light_css
    assert 'background: transparent !important' in light_css
    assert THEMES["Light"]["muted"] in light_css


def test_placeholder_contrast_styling():
    light_css = get_theme_css("Light")
    assert "input::placeholder" in light_css
    assert THEMES["Light"]["placeholder"] in light_css

    dark_css = get_theme_css("Dark")
    assert "input::placeholder" in dark_css
    assert THEMES["Dark"]["placeholder"] in dark_css
