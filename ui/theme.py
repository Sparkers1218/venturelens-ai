import streamlit as st


THEMES: dict[str, dict[str, str]] = {
    "Light": {
        "background": "#F5F7FB",
        "surface": "#FFFFFF",
        "sidebar": "#FFFFFF",
        "sidebar_hover": "#EEF2F8",
        "text": "#172033",
        "muted": "#687386",
        "primary": "#3B66DE",
        "border": "#E2E8F0",
        "focus_ring": "#3B66DE",
        "shadow": "0 4px 18px rgba(25, 40, 75, 0.06)",
        "color_scheme": "light",
    },
    "Dark": {
        "background": "#101827",
        "surface": "#192438",
        "sidebar": "#141F31",
        "sidebar_hover": "#1E2D44",
        "text": "#F1F5FC",
        "muted": "#A1AEC2",
        "primary": "#7295FF",
        "border": "#2B3A50",
        "focus_ring": "#7295FF",
        "shadow": "0 4px 18px rgba(0, 0, 0, 0.28)",
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
}}

[data-testid="stAppViewContainer"],
[data-testid="stMain"] {{
    background-color: {theme["background"]};
    color: {theme["text"]};
}}

[data-testid="stHeader"] {{
    background-color: transparent;
}}

[data-testid="stMainBlockContainer"] {{
    max-width: 1440px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}}

[data-testid="stSidebar"] {{
    background-color: {theme["sidebar"]};
    border-right: 1px solid {theme["border"]};
}}

[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4,
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {{
    color: {theme["text"]};
}}

[data-testid="stCaptionContainer"] {{
    color: {theme["muted"]};
}}

[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stMetric"] {{
    background-color: {theme["surface"]};
    border: 1px solid {theme["border"]};
    border-radius: 14px;
    box-shadow: {theme["shadow"]};
}}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {{
    color: {theme["text"]};
}}

button[data-testid="stBaseButton-primary"] {{
    background-color: {theme["primary"]};
    border-color: {theme["primary"]};
    color: #FFFFFF;
}}

button[data-testid="stBaseButton-secondary"] {{
    background-color: {theme["surface"]};
    border-color: {theme["border"]};
    color: {theme["text"]};
}}

button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-secondary"]:hover {{
    border-color: {theme["primary"]};
}}

button:focus-visible,
input:focus-visible,
textarea:focus-visible,
[role="radio"]:focus-visible {{
    outline: 3px solid {theme["focus_ring"]};
    outline-offset: 2px;
}}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-baseweb="select"] > div {{
    background-color: {theme["surface"]};
    color: {theme["text"]};
    border-color: {theme["border"]};
}}

[data-testid="stSidebar"] [role="radiogroup"] label {{
    border-radius: 9px;
    padding: 0.45rem 0.6rem;
}}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {{
    background-color: {theme["sidebar_hover"]};
}}

[data-testid="stSidebar"] [role="radio"],
[data-testid="stRadio"] [role="radio"] {{
    accent-color: {theme["primary"]};
}}

[data-testid="stAlert"],
[data-testid="stDataFrame"] {{
    border-radius: 12px;
}}

a {{
    color: {theme["primary"]};
}}

@media (max-width: 768px) {{
    [data-testid="stMainBlockContainer"] {{
        padding: 1rem 1rem 2rem;
    }}
}}
</style>
"""


def apply_theme(theme_name: str) -> None:
    st.html(get_theme_css(theme_name))
