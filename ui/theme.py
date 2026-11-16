import streamlit as st


THEMES: dict[str, dict[str, str]] = {
    "Light": {
        "background": "#F5F7FB",
        "surface": "#FFFFFF",
        "surface_alt": "#F8FAFD",
        "sidebar": "#FFFFFF",
        "sidebar_hover": "#F1F5FB",
        "sidebar_selected": "#EBF1FC",
        "sidebar_selected_border": "#C5D7F6",
        "text": "#172033",
        "muted": "#657186",
        "primary": "#3B66DE",
        "primary_button": "#3B66DE",
        "primary_button_hover": "#2E55C7",
        "border": "#E2E8F0",
        "focus_ring": "#3B66DE",
        "shadow": "0 6px 22px rgba(25, 40, 75, 0.07)",
        "color_scheme": "light",
    },
    "Dark": {
        "background": "#101827",
        "surface": "#192438",
        "surface_alt": "#1C2A40",
        "sidebar": "#141F31",
        "sidebar_hover": "#1E2D44",
        "sidebar_selected": "#1E2D44",
        "sidebar_selected_border": "#334664",
        "text": "#F1F5FC",
        "muted": "#A1AEC2",
        "primary": "#91A9FF",
        "primary_button": "#355DCB",
        "primary_button_hover": "#2E55C7",
        "border": "#2B3A50",
        "focus_ring": "#91A9FF",
        "shadow": "0 8px 26px rgba(0, 0, 0, 0.24)",
        "color_scheme": "dark",
    },
}


def render_theme_selector() -> str:
    if st.session_state.get("vl_theme") not in THEMES:
        st.session_state["vl_theme"] = "Light"

    return st.radio(
        "Appearance",
        options=tuple(THEMES),
        format_func=lambda theme: "☀️ Light" if theme == "Light" else "🌙 Dark",
        horizontal=True,
        label_visibility="collapsed",
        key="vl_theme",
    )


def get_theme_css(theme_name: str) -> str:
    try:
        theme = THEMES[theme_name]
    except KeyError as error:
        raise ValueError(f"Unknown theme: {theme_name}") from error

    return f"""
<style>
:root {{
    color-scheme: {theme["color_scheme"]};
    --vl-background: {theme["background"]};
    --vl-surface: {theme["surface"]};
    --vl-surface-alt: {theme["surface_alt"]};
    --vl-sidebar: {theme["sidebar"]};
    --vl-sidebar-hover: {theme["sidebar_hover"]};
    --vl-sidebar-selected: {theme["sidebar_selected"]};
    --vl-sidebar-selected-border: {theme["sidebar_selected_border"]};
    --vl-text: {theme["text"]};
    --vl-muted: {theme["muted"]};
    --vl-primary: {theme["primary"]};
    --vl-primary-button: {theme["primary_button"]};
    --vl-primary-button-hover: {theme["primary_button_hover"]};
    --vl-border: {theme["border"]};
    --vl-focus-ring: {theme["focus_ring"]};
    --vl-shadow: {theme["shadow"]};
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}

html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {{
    background: var(--vl-background) !important;
    color: var(--vl-text) !important;
    color-scheme: {theme["color_scheme"]};
    min-width: 0;
}}

.stApp,
[data-testid="stAppViewContainer"] {{
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}

[data-testid="stHeader"] {{
    background: transparent !important;
    pointer-events: none !important;
}}

[data-testid="stHeader"] [data-testid="stToolbar"] {{
    pointer-events: none !important;
}}

[data-testid="stHeader"] [data-testid="stToolbar"] button,
[data-testid="stHeader"] [data-testid="stToolbar"] a,
[data-testid="stHeader"] [role="button"] {{
    pointer-events: auto !important;
}}

[data-testid="stMainBlockContainer"] {{
    box-sizing: border-box;
    width: 100%;
    max-width: 1440px;
    padding: 4rem clamp(1rem, 3vw, 2.25rem) 3rem;
    margin-inline: auto;
}}

[data-testid="stSidebar"] {{
    background: var(--vl-sidebar) !important;
    border-right: 1px solid var(--vl-border) !important;
}}

[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4,
[data-testid="stMain"] p,
[data-testid="stMain"] label,
[data-testid="stMain"] li,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] li {{
    color: var(--vl-text) !important;
    overflow-wrap: anywhere;
}}

[data-testid="stMain"] h1 {{
    font-size: clamp(1.8rem, 4vw, 2.4rem);
    font-weight: 720;
    letter-spacing: -0.035em;
    line-height: 1.15;
}}

[data-testid="stMain"] h2,
[data-testid="stMain"] h3 {{
    font-weight: 650;
    letter-spacing: -0.02em;
}}

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
    color: var(--vl-muted) !important;
}}

[data-testid="stVerticalBlockBorderWrapper"] {{
    background: var(--vl-surface) !important;
    border: 1px solid var(--vl-border) !important;
    border-radius: 16px !important;
    box-shadow: var(--vl-shadow);
    transition: border-color 140ms ease, box-shadow 140ms ease;
}}

[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    border-color: var(--vl-sidebar_selected_border) !important;
}}

[data-testid="stMetric"] {{
    box-sizing: border-box;
    min-width: 0;
    padding: 1rem 1.1rem;
    background: var(--vl-surface) !important;
    border: 1px solid var(--vl-border);
    border-radius: 14px;
    box-shadow: var(--vl-shadow);
}}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {{
    color: var(--vl-muted) !important;
    overflow-wrap: anywhere;
}}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {{
    color: var(--vl-text) !important;
    overflow-wrap: anywhere;
}}

[data-testid="stMetricValue"] [data-testid="stMarkdownContainer"],
[data-testid="stMetricValue"] [data-testid="stMarkdownContainer"] p {{
    white-space: normal !important;
    overflow-wrap: anywhere;
}}

[data-testid="stForm"] {{
    padding: clamp(1rem, 2vw, 1.5rem);
    background: var(--vl-surface) !important;
    border: 1px solid var(--vl-border);
    border-radius: 16px;
}}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
[data-testid="stTimeInput"] input,
[data-baseweb="select"] > div {{
    box-sizing: border-box;
    max-width: 100%;
    background: var(--vl-surface) !important;
    border-color: var(--vl-border) !important;
    color: var(--vl-text) !important;
}}

input::placeholder,
textarea::placeholder {{
    color: var(--vl-muted) !important;
    opacity: 0.9;
}}

input[type="checkbox"],
input[type="radio"],
[data-testid="stSlider"] {{
    accent-color: var(--vl-primary);
}}

button[data-testid="stBaseButton-primary"],
[data-testid="stFormSubmitButton"] button[data-testid="stBaseButton-primary"] {{
    background: var(--vl-primary-button) !important;
    border-color: var(--vl-primary-button) !important;
    color: #FFFFFF !important;
}}

button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-primary"]:active {{
    background: var(--vl-primary-button-hover) !important;
    border-color: var(--vl-primary-button-hover) !important;
}}

button[data-testid="stBaseButton-secondary"],
[data-testid="stDownloadButton"] button,
[data-testid="stLinkButton"] a {{
    background: var(--vl-surface) !important;
    border-color: var(--vl-border) !important;
    color: var(--vl-text) !important;
}}

button[data-testid="stBaseButton-secondary"]:hover,
[data-testid="stDownloadButton"] button:hover,
[data-testid="stLinkButton"] a:hover {{
    border-color: var(--vl-primary) !important;
    color: var(--vl-primary) !important;
}}

.stButton > button,
.stDownloadButton > button,
.stLinkButton > a,
[data-testid="stFormSubmitButton"] button {{
    min-height: 42px;
    border-radius: 10px !important;
    font-weight: 600;
    white-space: normal;
    overflow-wrap: anywhere;
    transition: background-color 140ms ease, border-color 140ms ease, box-shadow 140ms ease;
}}

button:focus-visible,
a:focus-visible,
input:focus-visible,
textarea:focus-visible,
[role="radio"]:focus-visible,
[role="tab"]:focus-visible {{
    outline: 3px solid var(--vl-focus-ring) !important;
    outline-offset: 2px;
}}

[data-testid="stSidebar"] [data-testid="stRadioOption"] {{
    min-height: 44px;
    padding: 0.45rem 0.7rem !important;
    border: 1px solid transparent;
    border-radius: 10px !important;
    transition: background-color 140ms ease, border-color 140ms ease;
}}

[data-testid="stSidebar"] [data-testid="stRadioOption"]:hover {{
    background: var(--vl-sidebar-hover) !important;
}}

[data-testid="stSidebar"] [data-testid="stRadioOption"]:has(input:checked) {{
    background: var(--vl-sidebar-selected) !important;
    border-color: var(--vl-sidebar-selected-border) !important;
}}

[data-testid="stSidebar"] [data-testid="stRadioOption"]:has(input:checked) p,
[data-testid="stSidebar"] [data-testid="stRadioOption"]:has(input:checked) span {{
    color: var(--vl-primary) !important;
    font-weight: 650;
}}

.st-key-vl_theme [data-testid="stRadioOption"] {{
    min-height: 40px;
    padding: 0.35rem 0.8rem !important;
    border: 1px solid var(--vl-border);
    border-radius: 999px !important;
    background: var(--vl-surface) !important;
    color: var(--vl-text) !important;
    transition: background-color 140ms ease, border-color 140ms ease;
}}

.st-key-vl_theme [data-testid="stRadioOption"]:hover {{
    border-color: var(--vl-primary) !important;
}}

.st-key-vl_theme [data-testid="stRadioOption"]:has(input:checked) {{
    background: var(--vl-sidebar-selected) !important;
    border-color: var(--vl-primary) !important;
    color: var(--vl-primary) !important;
    font-weight: 650;
}}

[data-testid="stTabs"] [role="tab"] {{
    color: var(--vl-muted) !important;
    white-space: normal;
    overflow-wrap: anywhere;
}}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
    color: var(--vl-primary) !important;
    border-bottom-color: var(--vl-primary) !important;
}}

[data-testid="stDataFrame"] {{
    max-width: 100%;
    overflow-x: auto;
    border: 1px solid var(--vl-border);
    border-radius: 12px;
}}

[data-testid="stVegaLiteChart"],
[data-testid="stArrowVegaLiteChart"] {{
    max-width: 100%;
    background: var(--vl-surface) !important;
    border: 1px solid var(--vl-border);
    border-radius: 14px;
}}

[data-testid="stVegaLiteChart"] svg text,
[data-testid="stVegaLiteChart"] svg tspan,
[data-testid="stArrowVegaLiteChart"] svg text,
[data-testid="stArrowVegaLiteChart"] svg tspan {{
    fill: var(--vl-text) !important;
}}

[data-testid="stAlert"],
[data-testid="stStatus"],
[data-testid="stExpander"] {{
    color: var(--vl-text) !important;
    border-color: var(--vl-border) !important;
    border-radius: 12px;
}}

[data-testid="stAlert"] [data-testid="stMarkdownContainer"],
[data-testid="stStatus"] [data-testid="stMarkdownContainer"] {{
    color: var(--vl-text) !important;
}}

[data-testid="stDialog"],
[data-testid="stPopoverBody"],
[data-testid="stTooltipContent"],
[data-testid="stSelectboxVirtualDropdown"],
[role="listbox"] {{
    background: var(--vl-surface) !important;
    border-color: var(--vl-border) !important;
    color: var(--vl-text) !important;
}}

[data-testid="stSelectboxVirtualDropdown"] [role="option"],
[role="listbox"] [role="option"] {{
    color: var(--vl-text) !important;
    overflow-wrap: anywhere;
}}

[data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover,
[data-testid="stSelectboxVirtualDropdown"] [role="option"][aria-selected="true"],
[role="listbox"] [role="option"]:hover,
[role="listbox"] [role="option"][aria-selected="true"] {{
    background: var(--vl-sidebar-selected) !important;
}}

[data-testid="stMain"] p,
[data-testid="stMain"] li,
[data-testid="stMain"] a,
[data-testid="stMain"] code,
[data-testid="stMain"] button,
[data-testid="stMain"] label {{
    overflow-wrap: anywhere;
}}

[data-testid="stMain"] pre,
[data-testid="stDataFrame"] {{
    max-width: 100%;
    overflow-x: auto;
}}

a {{
    color: var(--vl-primary);
}}

@media (max-width: 900px) {{
    [data-testid="stMainBlockContainer"] {{
        padding: 3.75rem 1rem 2rem;
    }}

    [data-testid="stHorizontalBlock"] {{
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 0.75rem !important;
    }}

    [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
        box-sizing: border-box;
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        flex: 1 1 100% !important;
    }}

    [data-testid="stButton"] button,
    [data-testid="stDownloadButton"] button,
    [data-testid="stLinkButton"] a,
    [data-testid="stFormSubmitButton"] button {{
        width: 100%;
        min-height: 44px;
    }}

    [data-testid="stTabs"] [role="tablist"] {{
        max-width: 100%;
        overflow-x: auto;
        flex-wrap: nowrap;
    }}

    [data-testid="stTabs"] [role="tab"] {{
        flex: 0 0 auto;
        white-space: nowrap;
    }}
}}

@media (max-width: 380px) {{
    [data-testid="stMainBlockContainer"] {{
        padding-right: 0.75rem;
        padding-left: 0.75rem;
    }}

    [data-testid="stMain"] h1 {{
        font-size: clamp(1.6rem, 7vw, 1.8rem);
    }}
}}
</style>
"""


def apply_theme(theme_name: str) -> None:
    st.html(get_theme_css(theme_name))
