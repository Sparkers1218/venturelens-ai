import streamlit as st


THEMES = {
    "Light": {
        "background": "#F5F7FB",
        "surface": "#FFFFFF",
        "sidebar": "#FFFFFF",
        "sidebar_hover": "#EEF2F8",
        "sidebar_selected": "#EBF1FC",
        "sidebar_selected_border": "#C5D7F6",
        "text": "#172033",
        "muted": "#687386",
        "primary": "#3B66DE",
        "primary_glow": "rgba(59, 102, 222, 0.22)",
        "primary_gradient": "linear-gradient(180deg, #3B66DE 0%, #2E55C7 100%)",
        "primary_hover_gradient": "linear-gradient(180deg, #4873EC 0%, #355DD4 100%)",
        "border": "#E2E8F0",
        "shadow": "0 4px 18px rgba(25, 40, 75, 0.06)",
        "hover_shadow": "0 8px 24px rgba(25, 40, 75, 0.10)",
        "elevated_shadow": "0 2px 6px rgba(25, 40, 75, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.9)",
        "inset_shadow": "inset 0 1px 2px rgba(25, 40, 75, 0.06)",
        "button_gradient": "linear-gradient(180deg, #FFFFFF 0%, #F1F4F9 100%)",
        "button_hover_gradient": "linear-gradient(180deg, #FFFFFF 0%, #EBF1FB 100%)",
        "button_active_bg": "#E4EDFA",
        "selector_track": "#EDF2F9",
        "selector_hover": "rgba(25, 40, 75, 0.06)",
        "active_pill_bg": "#FFFFFF",
        "active_pill_border": "#D0D9E5",
        "active_pill_shadow": "0 2px 6px rgba(25, 40, 75, 0.12), 0 1px 1px rgba(0, 0, 0, 0.05)",
        "tab_hover": "#F0F4FA",
        "tab_selected_bg": "#EEF3FC",
        "dropdown_hover": "#F0F4FA",
        "dropdown_selected": "#E8F0FC",
        "focus_ring": "rgba(59, 102, 222, 0.25)",
        "info_bg": "#EEF4FF",
        "info_border": "#C8DCFE",
        "info_text": "#17346A",
        "sidebar_hover_legacy": "rgba(25, 40, 75, 0.04)",
        "card_gradient": "linear-gradient(180deg, #FFFFFF 0%, #F9FAFC 100%)",
        "badge_bg": "#EEF2F8",
        "badge_text": "#35558A",
        "progress_track": "#E5EBF4",
        "placeholder": "#768396",
    },
    "Dark": {
        "background": "#101827",
        "surface": "#192438",
        "sidebar": "#141F31",
        "sidebar_hover": "rgba(255, 255, 255, 0.05)",
        "sidebar_selected": "#1E2D44",
        "sidebar_selected_border": "#334664",
        "text": "#F1F5FC",
        "muted": "#A1AEC2",
        "primary": "#7295FF",
        "primary_glow": "rgba(114, 149, 255, 0.25)",
        "primary_gradient": "linear-gradient(180deg, #5B84F7 0%, #446EE8 100%)",
        "primary_hover_gradient": "linear-gradient(180deg, #6B92FF 0%, #517BEE 100%)",
        "border": "#2B3A50",
        "shadow": "0 4px 18px rgba(0, 0, 0, 0.28)",
        "hover_shadow": "0 8px 24px rgba(0, 0, 0, 0.4)",
        "elevated_shadow": "0 2px 6px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.08)",
        "inset_shadow": "inset 0 1px 3px rgba(0, 0, 0, 0.45)",
        "button_gradient": "linear-gradient(180deg, #24334C 0%, #1A263B 100%)",
        "button_hover_gradient": "linear-gradient(180deg, #2A3B57 0%, #1F2D44 100%)",
        "button_active_bg": "#172234",
        "selector_track": "#121A29",
        "selector_hover": "rgba(255, 255, 255, 0.05)",
        "active_pill_bg": "#1E2D44",
        "active_pill_border": "#3B4D68",
        "active_pill_shadow": "0 2px 8px rgba(0, 0, 0, 0.4)",
        "tab_hover": "#1E2B40",
        "tab_selected_bg": "#1E2D44",
        "dropdown_hover": "#223048",
        "dropdown_selected": "#1E2D44",
        "focus_ring": "rgba(114, 149, 255, 0.3)",
        "info_bg": "#142138",
        "info_border": "#283D63",
        "info_text": "#D9E6FF",
        "sidebar_hover_legacy": "rgba(255, 255, 255, 0.04)",
        "card_gradient": "linear-gradient(180deg, #1C273C 0%, #162032 100%)",
        "badge_bg": "#1E2B42",
        "badge_text": "#9AB7E8",
        "progress_track": "#182235",
        "placeholder": "#7E8EAA",
    },
}


def render_theme_selector() -> str:
    """Display the theme selector in the top toolbar and return the selected theme."""

    if "vl_theme" not in st.session_state:
        st.session_state["vl_theme"] = "Light"

    current = st.session_state.get("vl_theme", "Light")
    options = ["Light", "Dark"]
    default_index = options.index(current) if current in options else 0

    theme = st.radio(
        "Appearance",
        options=options,
        index=default_index,
        format_func=lambda opt: "☀️ Light" if opt == "Light" else "🌙 Dark",
        horizontal=True,
        label_visibility="collapsed",
        key="vl_theme",
    )

    return theme


def get_theme_css(theme_name: str) -> str:
    """Generate custom CSS for the selected visual theme."""

    theme = THEMES.get(theme_name, THEMES["Light"])

    return f"""
    <style>
        /* Base app styling */
        .stApp {{
            background-color: {theme["background"]} !important;
            color: {theme["text"]} !important;
        }}

        /* Fix header click interception */
        [data-testid="stHeader"] {{
            background-color: transparent !important;
            pointer-events: none !important;
        }}

        [data-testid="stHeader"] > * {{
            pointer-events: auto !important;
        }}

        [data-testid="stToolbar"] {{
            pointer-events: auto !important;
        }}

        /* Content container spacing */
        .block-container {{
            padding-top: 2.75rem !important;
            padding-bottom: 3rem !important;
            max-width: 1440px !important;
        }}

        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {theme["sidebar"]} !important;
            border-right: 1px solid {theme["border"]} !important;
        }}

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {{
            color: {theme["text"]} !important;
        }}

        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
        [data-testid="stSidebar"] .stCaption {{
            color: {theme["muted"]} !important;
        }}

        /* Sidebar navigation radio items (tabs) */
        [data-testid="stSidebar"] [data-testid="stRadioOption"],
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"],
        [data-testid="stSidebar"] div[role="radiogroup"] label {{
            padding: 9px 14px !important;
            border-radius: 9px !important;
            margin-bottom: 3px !important;
            background: transparent !important;
            border: 1px solid transparent !important;
            transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease !important;
            cursor: pointer !important;
            display: flex !important;
            align-items: center !important;
            width: 100% !important;
        }}

        [data-testid="stSidebar"] [data-testid="stRadioOption"]:hover,
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]:hover,
        [data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
            background: {theme["sidebar_hover"]} !important;
            border-color: transparent !important;
        }}

        [data-testid="stSidebar"] [data-testid="stRadioOption"]:focus,
        [data-testid="stSidebar"] [data-testid="stRadioOption"]:focus-within,
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]:focus,
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]:focus-within,
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]:focus-visible,
        [data-testid="stSidebar"] div[role="radiogroup"] label:focus-within {{
            background: {theme["sidebar_hover"]} !important;
            outline: 2px solid {theme["focus_ring"]} !important;
            outline-offset: -1px !important;
        }}

        [data-testid="stSidebar"] [data-testid="stRadioOption"]:active,
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]:active,
        [data-testid="stSidebar"] div[role="radiogroup"] label:active {{
            background: {theme["sidebar_selected"]} !important;
        }}

        /* Selected sidebar item - ensures NO black background in Light Theme */
        [data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"],
        [data-testid="stSidebar"] [data-testid="stRadioOption"]:has(input:checked),
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked),
        [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
            background: {theme["sidebar_selected"]} !important;
            border: 1px solid {theme["sidebar_selected_border"]} !important;
            box-shadow: {theme["inset_shadow"]} !important;
        }}

        [data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"] p,
        [data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"] span,
        [data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"] div,
        [data-testid="stSidebar"] [data-testid="stRadioOption"]:has(input:checked) p,
        [data-testid="stSidebar"] [data-testid="stRadioOption"]:has(input:checked) span,
        [data-testid="stSidebar"] [data-testid="stRadioOption"]:has(input:checked) div,
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) p,
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) span,
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) div,
        [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p,
        [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) span {{
            color: {theme["primary"]} !important;
            font-weight: 700 !important;
        }}

        /* Remove unwanted solid black radio circle indicators in the sidebar */
        [data-testid="stSidebar"] [data-testid="stRadioOption"] > div > div:first-child,
        [data-testid="stSidebar"] [data-testid="stRadioOption"] [class*="e1dm8mpf4"],
        [data-testid="stSidebar"] div[data-baseweb="radio"] > div:first-child,
        [data-testid="stSidebar"] div[role="radiogroup"] label > div > div:first-child {{
            display: none !important;
        }}

        [data-testid="stSidebar"] [data-testid="stRadioOption"] > div,
        [data-testid="stSidebar"] div[role="radiogroup"] label > div {{
            width: 100% !important;
        }}

        /* General radio circle styling fallback across the app */
        [data-testid="stRadioOption"] [class*="e1dm8mpf4"],
        [data-testid="stRadioOption"] > div > div:first-child,
        div[data-baseweb="radio"] > div:first-child {{
            border-color: {theme["border"]} !important;
            background-color: {theme["surface"]} !important;
        }}

        [data-testid="stRadioOption"][data-selected="true"] [class*="e1dm8mpf4"],
        [data-testid="stRadioOption"]:has(input:checked) [class*="e1dm8mpf4"],
        [data-testid="stRadioOption"][data-selected="true"] > div > div:first-child,
        [data-testid="stRadioOption"]:has(input:checked) > div > div:first-child,
        div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) div[data-baseweb="radio"] > div:first-child {{
            border-color: {theme["primary"]} !important;
            background-color: {theme["primary"]} !important;
        }}

        /* Typography & readability */
        h1, h2, h3, h4, p, label, .stMarkdown {{
            color: {theme["text"]} !important;
        }}

        [data-testid="stCaptionContainer"] p,
        .stCaption,
        .vl-muted {{
            color: {theme["muted"]} !important;
        }}

        /* Dividers - balanced vertical rhythm between sections */
        hr, [data-testid="stDivider"] {{
            border-color: {theme["border"]} !important;
            opacity: 0.8 !important;
            margin: 1.75rem 0 !important;
        }}

        /* Metrics cards */
        [data-testid="stMetric"] {{
            background-color: {theme["surface"]} !important;
            border: 1px solid {theme["border"]} !important;
            border-radius: 14px !important;
            padding: 18px !important;
            box-shadow: {theme["shadow"]} !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }}

        [data-testid="stMetric"]:hover {{
            transform: translateY(-2px) !important;
            box-shadow: {theme["hover_shadow"]} !important;
        }}

        [data-testid="stMetricLabel"] p,
        [data-testid="stMetricLabel"] label,
        [data-testid="stMetricLabel"] {{
            color: {theme["muted"]} !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
        }}

        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] > div,
        [data-testid="stMetricValue"] * {{
            color: {theme["text"]} !important;
            font-weight: 700 !important;
        }}

        /* Standard / Secondary Buttons */
        .stButton > button,
        button[data-testid="stBaseButton-secondary"],
        button[data-testid="baseButton-secondary"] {{
            background: {theme["button_gradient"]} !important;
            background-color: {theme["surface"]} !important;
            color: {theme["text"]} !important;
            border: 1px solid {theme["border"]} !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            padding: 0.55rem 1.3rem !important;
            box-shadow: {theme["elevated_shadow"]} !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}

        .stButton > button *,
        button[data-testid="stBaseButton-secondary"] *,
        button[data-testid="baseButton-secondary"] * {{
            color: {theme["text"]} !important;
        }}

        .stButton > button:hover,
        button[data-testid="stBaseButton-secondary"]:hover,
        button[data-testid="baseButton-secondary"]:hover {{
            background: {theme["button_hover_gradient"]} !important;
            background-color: {theme["sidebar_hover"]} !important;
            border-color: {theme["primary"]} !important;
            color: {theme["primary"]} !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 14px {theme["primary_glow"]} !important;
        }}

        .stButton > button:hover *,
        button[data-testid="stBaseButton-secondary"]:hover *,
        button[data-testid="baseButton-secondary"]:hover * {{
            color: {theme["primary"]} !important;
        }}

        .stButton > button:active,
        button[data-testid="stBaseButton-secondary"]:active,
        button[data-testid="baseButton-secondary"]:active {{
            background: {theme["button_active_bg"]} !important;
            background-color: {theme["button_active_bg"]} !important;
            color: {theme["primary"]} !important;
            transform: translateY(0) !important;
            box-shadow: {theme["inset_shadow"]} !important;
        }}

        .stButton > button:active *,
        button[data-testid="stBaseButton-secondary"]:active *,
        button[data-testid="baseButton-secondary"]:active * {{
            color: {theme["primary"]} !important;
        }}

        .stButton > button:focus,
        .stButton > button:focus-visible,
        button[data-testid="stBaseButton-secondary"]:focus,
        button[data-testid="stBaseButton-secondary"]:focus-visible,
        button[data-testid="baseButton-secondary"]:focus,
        button[data-testid="baseButton-secondary"]:focus-visible {{
            background: {theme["button_hover_gradient"]} !important;
            color: {theme["primary"]} !important;
            border-color: {theme["primary"]} !important;
            outline: 2px solid {theme["focus_ring"]} !important;
            outline-offset: 1px !important;
        }}

        .stButton > button:focus *,
        button[data-testid="stBaseButton-secondary"]:focus *,
        button[data-testid="baseButton-secondary"]:focus * {{
            color: {theme["primary"]} !important;
        }}

        /* Primary Buttons */
        .stButton > button[kind="primary"],
        button[data-testid="stBaseButton-primary"],
        button[data-testid="baseButton-primary"] {{
            background: {theme["primary_gradient"]} !important;
            background-color: {theme["primary"]} !important;
            color: #FFFFFF !important;
            border: 1px solid {theme["primary"]} !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            padding: 0.55rem 1.3rem !important;
            box-shadow: 0 2px 8px {theme["primary_glow"]}, inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}

        .stButton > button[kind="primary"] *,
        button[data-testid="stBaseButton-primary"] *,
        button[data-testid="baseButton-primary"] * {{
            color: #FFFFFF !important;
        }}

        .stButton > button[kind="primary"]:hover,
        button[data-testid="stBaseButton-primary"]:hover,
        button[data-testid="baseButton-primary"]:hover {{
            background: {theme["primary_hover_gradient"]} !important;
            color: #FFFFFF !important;
            border-color: {theme["primary"]} !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 16px {theme["primary_glow"]} !important;
        }}

        .stButton > button[kind="primary"]:hover *,
        button[data-testid="stBaseButton-primary"]:hover *,
        button[data-testid="baseButton-primary"]:hover * {{
            color: #FFFFFF !important;
        }}

        .stButton > button[kind="primary"]:active,
        button[data-testid="stBaseButton-primary"]:active,
        button[data-testid="baseButton-primary"]:active {{
            background: {theme["primary"]} !important;
            color: #FFFFFF !important;
            transform: translateY(0) !important;
            box-shadow: {theme["inset_shadow"]} !important;
        }}

        .stButton > button[kind="primary"]:focus,
        .stButton > button[kind="primary"]:focus-visible,
        button[data-testid="stBaseButton-primary"]:focus,
        button[data-testid="baseButton-primary"]:focus {{
            background: {theme["primary_gradient"]} !important;
            color: #FFFFFF !important;
            outline: 2px solid {theme["focus_ring"]} !important;
            outline-offset: 2px !important;
        }}

        /* Popover Trigger Buttons - fixes notification bell, Founder profile, Validation Playbook */
        [data-testid="stPopover"] button,
        button[data-testid="stPopoverButton"],
        [data-testid="stPopover"] > button,
        .stPopover button {{
            background: {theme["button_gradient"]} !important;
            background-color: {theme["surface"]} !important;
            color: {theme["text"]} !important;
            border: 1px solid {theme["border"]} !important;
            border-radius: 10px !important;
            font-weight: 500 !important;
            box-shadow: {theme["elevated_shadow"]} !important;
            transition: all 0.2s ease !important;
        }}

        [data-testid="stPopover"] button *,
        button[data-testid="stPopoverButton"] *,
        [data-testid="stPopover"] > button *,
        .stPopover button * {{
            color: {theme["text"]} !important;
            fill: {theme["text"]} !important;
        }}

        [data-testid="stPopover"] button:hover,
        button[data-testid="stPopoverButton"]:hover,
        [data-testid="stPopover"] > button:hover,
        .stPopover button:hover {{
            background: {theme["button_hover_gradient"]} !important;
            background-color: {theme["sidebar_hover"]} !important;
            border-color: {theme["primary"]} !important;
            color: {theme["primary"]} !important;
            box-shadow: 0 4px 14px {theme["primary_glow"]} !important;
        }}

        [data-testid="stPopover"] button:hover *,
        button[data-testid="stPopoverButton"]:hover *,
        [data-testid="stPopover"] > button:hover *,
        .stPopover button:hover * {{
            color: {theme["primary"]} !important;
            fill: {theme["primary"]} !important;
        }}

        [data-testid="stPopover"] button:focus,
        [data-testid="stPopover"] button:focus-visible,
        button[data-testid="stPopoverButton"]:focus,
        button[data-testid="stPopoverButton"]:focus-visible,
        [data-testid="stPopover"] > button:focus,
        [data-testid="stPopover"] > button:focus-visible,
        .stPopover button:focus,
        .stPopover button:focus-visible {{
            background: {theme["button_hover_gradient"]} !important;
            color: {theme["primary"]} !important;
            border-color: {theme["primary"]} !important;
            outline: 2px solid {theme["focus_ring"]} !important;
            outline-offset: 1px !important;
        }}

        [data-testid="stPopover"] button:focus *,
        button[data-testid="stPopoverButton"]:focus *,
        [data-testid="stPopover"] > button:focus *,
        .stPopover button:focus * {{
            color: {theme["primary"]} !important;
            fill: {theme["primary"]} !important;
        }}

        /* Open/expanded popover trigger - replaces black background with light active state */
        [data-testid="stPopover"] button[aria-expanded="true"],
        button[data-testid="stPopoverButton"][aria-expanded="true"],
        [data-testid="stPopover"] > button[aria-expanded="true"],
        [data-testid="stPopover"] button:active,
        button[data-testid="stPopoverButton"]:active,
        [data-testid="stPopover"] > button:active,
        .stPopover button[aria-expanded="true"],
        .stPopover button:active {{
            background: {theme["sidebar_selected"]} !important;
            background-color: {theme["sidebar_selected"]} !important;
            border-color: {theme["primary"]} !important;
            color: {theme["primary"]} !important;
            box-shadow: {theme["inset_shadow"]} !important;
        }}

        [data-testid="stPopover"] button[aria-expanded="true"] *,
        button[data-testid="stPopoverButton"][aria-expanded="true"] *,
        [data-testid="stPopover"] > button[aria-expanded="true"] *,
        button[data-testid="stPopoverButton"]:active *,
        .stPopover button[aria-expanded="true"] *,
        .stPopover button:active * {{
            color: {theme["primary"]} !important;
            fill: {theme["primary"]} !important;
        }}

        [data-testid="stPopoverBody"] {{
            background-color: {theme["surface"]} !important;
            border: 1px solid {theme["border"]} !important;
            border-radius: 14px !important;
            box-shadow: {theme["hover_shadow"]} !important;
            color: {theme["text"]} !important;
            padding: 20px 22px !important;
        }}

        [data-testid="stPopoverBody"] h1,
        [data-testid="stPopoverBody"] h2,
        [data-testid="stPopoverBody"] h3,
        [data-testid="stPopoverBody"] h4,
        [data-testid="stPopoverBody"] p,
        [data-testid="stPopoverBody"] span,
        [data-testid="stPopoverBody"] label,
        [data-testid="stPopoverBody"] div {{
            color: {theme["text"]} !important;
        }}

        [data-testid="stPopoverBody"] [data-testid="stCaptionContainer"] p,
        [data-testid="stPopoverBody"] .stCaption {{
            color: {theme["muted"]} !important;
        }}

        /* Streamlit Tabs Component */
        [data-testid="stTabs"] {{
            background: transparent !important;
        }}

        [data-testid="stTabs"] [role="tablist"] {{
            border-bottom: 1px solid {theme["border"]} !important;
            gap: 4px !important;
            background: transparent !important;
        }}

        [data-testid="stTabs"] button[data-baseweb="tab"] {{
            background: transparent !important;
            color: {theme["muted"]} !important;
            border: none !important;
            border-radius: 8px 8px 0 0 !important;
            padding: 10px 18px !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            transition: all 0.2s ease !important;
        }}

        /* Tab Hover - must NOT turn black */
        [data-testid="stTabs"] button[data-baseweb="tab"]:hover {{
            background: {theme["tab_hover"]} !important;
            color: {theme["text"]} !important;
        }}

        /* Selected Tab - replaces black background with clean theme-selected background */
        [data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {{
            background: {theme["tab_selected_bg"]} !important;
            color: {theme["primary"]} !important;
            border-bottom: 2px solid {theme["primary"]} !important;
            font-weight: 700 !important;
        }}

        /* Tab Focus */
        [data-testid="stTabs"] button[data-baseweb="tab"]:focus,
        [data-testid="stTabs"] button[data-baseweb="tab"]:focus-visible {{
            background: {theme["tab_hover"]} !important;
            color: {theme["primary"]} !important;
            outline: 2px solid {theme["focus_ring"]} !important;
            outline-offset: -2px !important;
        }}

        [data-baseweb="tab-highlight"] {{
            background-color: {theme["primary"]} !important;
        }}

        [data-baseweb="tab-border"] {{
            background-color: {theme["border"]} !important;
        }}

        /* Dropdown Selectboxes & Menus (Streamlit 1.66 Virtual Dropdown & BaseWeb) */
        [data-testid="stSelectbox"] div[data-testid="stSelectboxRootElement"],
        [data-testid="stSelectbox"] div[class*="e1oobldh0"],
        [data-testid="stSelectbox"] > div > div[data-baseweb="select"] > div,
        div[data-baseweb="select"] > div {{
            background-color: {theme["surface"]} !important;
            color: {theme["text"]} !important;
            border: 1px solid {theme["border"]} !important;
            border-radius: 10px !important;
            box-shadow: {theme["inset_shadow"]} !important;
            transition: all 0.15s ease !important;
        }}

        [data-testid="stSelectbox"] div[class*="e1oobldh0"]:hover,
        [data-testid="stSelectbox"] > div > div[data-baseweb="select"] > div:hover,
        div[data-baseweb="select"] > div:hover {{
            border-color: {theme["primary"]} !important;
        }}

        [data-testid="stSelectbox"] div[class*="e1oobldh0"][data-focus-within],
        [data-testid="stSelectbox"] div[class*="e1oobldh0"]:focus-within,
        div[data-baseweb="select"] > div:focus,
        div[data-baseweb="select"] > div:focus-within {{
            border-color: {theme["primary"]} !important;
            box-shadow: 0 0 0 3px {theme["focus_ring"]} !important;
        }}

        [data-testid="stSelectbox"] div[data-baseweb="select"] *,
        div[data-baseweb="select"] * {{
            color: {theme["text"]} !important;
        }}

        /* Selectbox input field */
        [data-testid="stSelectbox"] input,
        [data-testid="stSelectbox"] input[class*="e1oobldh1"],
        div[data-baseweb="select"] input {{
            background-color: transparent !important;
            color: {theme["text"]} !important;
            border: none !important;
            font-size: 0.9rem !important;
            caret-color: {theme["text"]} !important;
        }}

        [data-testid="stSelectbox"] input::placeholder,
        div[data-baseweb="select"] input::placeholder {{
            color: {theme["placeholder"]} !important;
            -webkit-text-fill-color: {theme["placeholder"]} !important;
        }}

        /* Dropdown open chevron/icon */
        [data-testid="stSelectbox"] div[class*="e1oobldh2"],
        [data-testid="stSelectbox"] div[class*="e1oobldh2"] svg,
        [data-testid="stSelectbox"] svg {{
            color: {theme["muted"]} !important;
            fill: {theme["muted"]} !important;
        }}

        /* Dropdown Popover & Menu Container */
        [data-testid="stSelectboxVirtualDropdown"],
        [data-testid="stMultiSelectDropdown"],
        div[class*="e1oobldh4"],
        div[class*="ew56mvo4"],
        div[data-baseweb="popover"]:has(ul[role="listbox"]),
        div[data-baseweb="popover"]:has([role="option"]),
        div[data-baseweb="popover"],
        ul[role="listbox"],
        div[data-baseweb="menu"] {{
            background-color: {theme["surface"]} !important;
            border: 1px solid {theme["border"]} !important;
            border-radius: 10px !important;
            box-shadow: {theme["hover_shadow"]} !important;
            color: {theme["text"]} !important;
        }}

        /* Listbox element */
        [data-testid="stSelectboxVirtualDropdown"] ul[role="listbox"],
        [data-testid="stMultiSelectDropdown"] ul[role="listbox"],
        [data-testid="stSelectboxVirtualDropdown"] ul[class*="e1oobldh5"],
        ul[role="listbox"] {{
            background-color: {theme["surface"]} !important;
            color: {theme["text"]} !important;
            padding: 4px !important;
            border: none !important;
            box-shadow: none !important;
        }}

        /* Option items - Normal state */
        [data-testid="stSelectboxVirtualDropdown"] [role="option"],
        [data-testid="stMultiSelectDropdown"] [role="option"],
        div[class*="e1oobldh7"],
        li[role="option"],
        div[data-baseweb="menu-item"] {{
            background-color: transparent !important;
            color: {theme["text"]} !important;
            padding: 8px 14px !important;
            border-radius: 6px !important;
            cursor: pointer !important;
            transition: background 0.12s ease !important;
        }}

        [data-testid="stSelectboxVirtualDropdown"] [role="option"] [data-item-hl],
        [data-testid="stSelectboxVirtualDropdown"] [role="option"] div[class*="e1oobldh8"],
        [data-testid="stMultiSelectDropdown"] [role="option"] [data-item-hl],
        [data-testid="stSelectboxVirtualDropdown"] [role="option"] *,
        [data-testid="stMultiSelectDropdown"] [role="option"] *,
        div[class*="e1oobldh7"] *,
        li[role="option"] *,
        div[data-baseweb="menu-item"] * {{
            color: {theme["text"]} !important;
            background-color: transparent !important;
        }}

        /* Option items - Hover state */
        [data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover,
        [data-testid="stSelectboxVirtualDropdown"] [role="option"][data-hovered="true"],
        [data-testid="stMultiSelectDropdown"] [role="option"]:hover,
        [data-testid="stMultiSelectDropdown"] [role="option"][data-hovered="true"],
        div[class*="e1oobldh7"]:hover,
        div[class*="e1oobldh7"][data-hovered="true"],
        li[role="option"]:hover,
        div[data-baseweb="menu-item"]:hover {{
            background-color: {theme["dropdown_hover"]} !important;
            color: {theme["text"]} !important;
        }}

        [data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover [data-item-hl],
        [data-testid="stSelectboxVirtualDropdown"] [role="option"][data-hovered="true"] [data-item-hl],
        [data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover div[class*="e1oobldh8"],
        [data-testid="stSelectboxVirtualDropdown"] [role="option"][data-hovered="true"] div[class*="e1oobldh8"],
        [data-testid="stMultiSelectDropdown"] [role="option"]:hover [data-item-hl],
        [data-testid="stMultiSelectDropdown"] [role="option"][data-hovered="true"] [data-item-hl],
        div[class*="e1oobldh7"]:hover [data-item-hl],
        div[class*="e1oobldh7"][data-hovered="true"] [data-item-hl] {{
            background-color: {theme["dropdown_hover"]} !important;
            color: {theme["text"]} !important;
        }}

        /* Option items - Focus state */
        [data-testid="stSelectboxVirtualDropdown"] [role="option"]:focus,
        [data-testid="stSelectboxVirtualDropdown"] [role="option"]:focus-visible,
        [data-testid="stSelectboxVirtualDropdown"] [role="option"][data-focused="true"],
        [data-testid="stMultiSelectDropdown"] [role="option"]:focus,
        [data-testid="stMultiSelectDropdown"] [role="option"]:focus-visible,
        [data-testid="stMultiSelectDropdown"] [role="option"][data-focused="true"],
        div[class*="e1oobldh7"]:focus,
        div[class*="e1oobldh7"][data-focused="true"],
        li[role="option"]:focus,
        li[role="option"]:focus-visible {{
            background-color: {theme["dropdown_hover"]} !important;
            color: {theme["text"]} !important;
            outline: none !important;
        }}

        [data-testid="stSelectboxVirtualDropdown"] [role="option"]:focus [data-item-hl],
        [data-testid="stSelectboxVirtualDropdown"] [role="option"][data-focused="true"] [data-item-hl],
        [data-testid="stSelectboxVirtualDropdown"] [role="option"]:focus div[class*="e1oobldh8"],
        [data-testid="stSelectboxVirtualDropdown"] [role="option"][data-focused="true"] div[class*="e1oobldh8"],
        [data-testid="stMultiSelectDropdown"] [role="option"]:focus [data-item-hl],
        [data-testid="stMultiSelectDropdown"] [role="option"][data-focused="true"] [data-item-hl] {{
            background-color: {theme["dropdown_hover"]} !important;
            color: {theme["text"]} !important;
        }}

        /* Option items - Selected state */
        [data-testid="stSelectboxVirtualDropdown"] [role="option"][aria-selected="true"],
        [data-testid="stSelectboxVirtualDropdown"] [role="option"][data-selected="true"],
        [data-testid="stMultiSelectDropdown"] [role="option"][aria-selected="true"],
        [data-testid="stMultiSelectDropdown"] [role="option"][data-selected="true"],
        div[class*="e1oobldh7"][aria-selected="true"],
        div[class*="e1oobldh7"][data-selected="true"],
        li[role="option"][aria-selected="true"],
        div[data-baseweb="menu-item"][aria-selected="true"] {{
            background-color: {theme["dropdown_selected"]} !important;
            color: {theme["primary"]} !important;
            font-weight: 600 !important;
        }}

        [data-testid="stSelectboxVirtualDropdown"] [role="option"][aria-selected="true"] [data-item-hl],
        [data-testid="stSelectboxVirtualDropdown"] [role="option"][data-selected="true"] [data-item-hl],
        [data-testid="stSelectboxVirtualDropdown"] [role="option"][aria-selected="true"] div[class*="e1oobldh8"],
        [data-testid="stSelectboxVirtualDropdown"] [role="option"][data-selected="true"] div[class*="e1oobldh8"],
        [data-testid="stMultiSelectDropdown"] [role="option"][aria-selected="true"] [data-item-hl],
        [data-testid="stMultiSelectDropdown"] [role="option"][data-selected="true"] [data-item-hl],
        div[class*="e1oobldh7"][aria-selected="true"] [data-item-hl],
        div[class*="e1oobldh7"][data-selected="true"] [data-item-hl],
        [data-testid="stSelectboxVirtualDropdown"] [role="option"][aria-selected="true"] *,
        [data-testid="stSelectboxVirtualDropdown"] [role="option"][data-selected="true"] *,
        [data-testid="stMultiSelectDropdown"] [role="option"][aria-selected="true"] *,
        [data-testid="stMultiSelectDropdown"] [role="option"][data-selected="true"] *,
        div[class*="e1oobldh7"][aria-selected="true"] *,
        div[class*="e1oobldh7"][data-selected="true"] *,
        li[role="option"][aria-selected="true"] *,
        div[data-baseweb="menu-item"][aria-selected="true"] * {{
            background-color: {theme["dropdown_selected"]} !important;
            color: {theme["primary"]} !important;
            font-weight: 600 !important;
        }}

        /* Info & Alert blocks */
        [data-testid="stAlert"] {{
            background-color: {theme["info_bg"]} !important;
            border: 1px solid {theme["info_border"]} !important;
            border-radius: 12px !important;
            box-shadow: {theme["shadow"]} !important;
            margin: 1.15rem 0 !important;
        }}

        [data-testid="stAlert"] p,
        [data-testid="stAlert"] div,
        [data-testid="stAlert"] span {{
            color: {theme["info_text"]} !important;
        }}

        [data-testid="stAlert"] svg {{
            fill: {theme["primary"]} !important;
            color: {theme["primary"]} !important;
        }}

        /* Tooltip styling - prevents black tooltip backgrounds and unreadable text */
        [data-testid="stTooltipContent"],
        .stTooltipContent,
        div[class*="e1wa7l463"],
        div[data-baseweb="tooltip"],
        div[role="tooltip"] {{
            background-color: {theme["surface"]} !important;
            color: {theme["text"]} !important;
            border: 1px solid {theme["border"]} !important;
            border-radius: 8px !important;
            box-shadow: {theme["hover_shadow"]} !important;
            padding: 6px 12px !important;
            font-size: 0.82rem !important;
        }}

        [data-testid="stTooltipContent"] *,
        .stTooltipContent *,
        div[class*="e1wa7l463"] *,
        div[data-baseweb="tooltip"] *,
        div[role="tooltip"] * {{
            color: {theme["text"]} !important;
        }}

        /* Inputs & textareas */
        [data-testid="stTextInput"] div[data-testid="stTextInputRootElement"],
        [data-testid="stTextInput"] div[class*="e1bh1cux2"],
        [data-testid="stTextArea"] textarea {{
            background-color: {theme["surface"]} !important;
            color: {theme["text"]} !important;
            border: 1px solid {theme["border"]} !important;
            border-radius: 10px !important;
            box-shadow: {theme["inset_shadow"]} !important;
        }}

        [data-testid="stTextInput"] div[data-testid="stTextInputRootElement"]:hover,
        [data-testid="stTextInput"] div[class*="e1bh1cux2"]:hover,
        [data-testid="stTextArea"] textarea:hover {{
            border-color: {theme["primary"]} !important;
        }}

        [data-testid="stTextInput"] div[data-testid="stTextInputRootElement"]:focus-within,
        [data-testid="stTextInput"] div[class*="e1bh1cux2"]:focus-within,
        [data-testid="stTextArea"] textarea:focus,
        [data-testid="stTextArea"] textarea:focus-visible {{
            background-color: {theme["surface"]} !important;
            color: {theme["text"]} !important;
            border-color: {theme["primary"]} !important;
            box-shadow: 0 0 0 3px {theme["focus_ring"]} !important;
            outline: none !important;
        }}

        /* Input field element */
        [data-testid="stTextInput"] input,
        [data-testid="stTextInputField"] {{
            background-color: transparent !important;
            color: {theme["text"]} !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0.6rem 0.9rem !important;
        }}

        /* Password Visibility Toggle Button */
        [data-testid="stTextInput"] button,
        [data-testid="stTextInput"] button[class*="e1bh1cux9"],
        [data-testid="stTextInput"] button[aria-label*="password" i],
        [data-testid="stTextInput"] button[aria-label*="entry" i] {{
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: {theme["muted"]} !important;
            cursor: pointer !important;
            padding: 0 10px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: color 0.15s ease !important;
        }}

        [data-testid="stTextInput"] button *,
        [data-testid="stTextInput"] button svg,
        [data-testid="stTextInput"] button span {{
            color: {theme["muted"]} !important;
            fill: {theme["muted"]} !important;
        }}

        [data-testid="stTextInput"] button:hover,
        [data-testid="stTextInput"] button:hover *,
        [data-testid="stTextInput"] button:hover svg {{
            color: {theme["primary"]} !important;
            fill: {theme["primary"]} !important;
            background: transparent !important;
            background-color: transparent !important;
        }}

        [data-testid="stTextInput"] button:active,
        [data-testid="stTextInput"] button:active * {{
            color: {theme["primary"]} !important;
            fill: {theme["primary"]} !important;
            background: transparent !important;
            background-color: transparent !important;
        }}

        [data-testid="stTextInput"] button:focus,
        [data-testid="stTextInput"] button:focus-visible {{
            outline: none !important;
            color: {theme["primary"]} !important;
        }}

        /* Input & Textarea Placeholders */
        input::placeholder,
        textarea::placeholder,
        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder,
        [data-testid="stTextInputField"]::placeholder {{
            color: {theme["placeholder"]} !important;
            opacity: 1 !important;
            -webkit-text-fill-color: {theme["placeholder"]} !important;
        }}

        input::-webkit-input-placeholder,
        textarea::-webkit-input-placeholder {{
            color: {theme["placeholder"]} !important;
            opacity: 1 !important;
            -webkit-text-fill-color: {theme["placeholder"]} !important;
        }}

        input::-moz-placeholder,
        textarea::-moz-placeholder {{
            color: {theme["placeholder"]} !important;
            opacity: 1 !important;
        }}

        /* Expander styling */
        [data-testid="stExpander"] {{
            background-color: {theme["surface"]} !important;
            border: 1px solid {theme["border"]} !important;
            border-radius: 12px !important;
            box-shadow: {theme["shadow"]} !important;
        }}

        [data-testid="stExpander"] summary {{
            color: {theme["text"]} !important;
        }}

        [data-testid="stExpander"] summary:hover {{
            color: {theme["primary"]} !important;
        }}

        /* Custom Skeuomorphic UI Classes */
        .vl-card {{
            background: {theme["card_gradient"]} !important;
            border: 1px solid {theme["border"]} !important;
            border-radius: 16px !important;
            padding: 24px 26px !important;
            box-shadow: {theme["shadow"]} !important;
            margin-bottom: 16px;
        }}

        .vl-hero-card {{
            background: {theme["card_gradient"]} !important;
            border: 1px solid {theme["border"]} !important;
            border-radius: 18px !important;
            padding: 28px 32px !important;
            box-shadow: {theme["shadow"]} !important;
            position: relative;
            overflow: hidden;
            margin-bottom: 18px;
        }}

        .vl-stat-box {{
            background: {theme["card_gradient"]} !important;
            border: 1px solid {theme["border"]} !important;
            border-radius: 14px !important;
            padding: 20px 22px !important;
            box-shadow: {theme["shadow"]} !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
            height: 100%;
            margin-bottom: 10px;
        }}

        .vl-stat-box:hover {{
            transform: translateY(-2px) !important;
            box-shadow: {theme["hover_shadow"]} !important;
            border-color: {theme["primary"]} !important;
        }}

        .vl-badge {{
            display: inline-block;
            background: {theme["badge_bg"]};
            color: {theme["badge_text"]};
            font-size: 0.76rem;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 12px;
            letter-spacing: 0.03em;
            text-transform: uppercase;
            border: 1px solid {theme["border"]};
        }}

        .vl-progress-pipeline {{
            background: {theme["surface"]};
            border: 1px solid {theme["border"]};
            border-radius: 14px;
            padding: 22px 24px;
            box-shadow: {theme["shadow"]};
            margin-bottom: 16px;
        }}

        .vl-step-box {{
            background: {theme["badge_bg"]};
            border: 1px solid {theme["border"]};
            border-radius: 10px;
            padding: 14px 14px;
            text-align: center;
            height: 100%;
            margin-bottom: 8px;
        }}

        .vl-pro-tip {{
            background: {theme["card_gradient"]};
            border: 1px solid {theme["border"]};
            border-left: 4px solid {theme["primary"]} !important;
            border-radius: 14px;
            padding: 20px 24px;
            box-shadow: {theme["shadow"]};
            margin-bottom: 16px;
        }}

        /* Profile Avatar */
        .vl-avatar {{
            width: 68px;
            height: 68px;
            border-radius: 50%;
            background: {theme["primary_gradient"]};
            color: #FFFFFF;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            box-shadow: 0 4px 14px {theme["primary_glow"]}, {theme["elevated_shadow"]};
            border: 2px solid {theme["surface"]};
            flex-shrink: 0;
        }}

        /* Notification Card Styles */
        .vl-notification-card {{
            background: {theme["card_gradient"]} !important;
            border: 1px solid {theme["border"]} !important;
            border-radius: 14px !important;
            padding: 16px 20px !important;
            margin-bottom: 12px;
            box-shadow: {theme["shadow"]} !important;
            transition: all 0.15s ease !important;
        }}

        .vl-notification-card:hover {{
            box-shadow: {theme["hover_shadow"]} !important;
            border-color: {theme["primary"]} !important;
        }}

        .vl-notification-unread {{
            border-left: 4px solid {theme["primary"]} !important;
            background: {theme["sidebar_selected"]} !important;
        }}

        /* Authentication Card & Divider */
        .vl-auth-card {{
            background: {theme["card_gradient"]} !important;
            border: 1px solid {theme["border"]} !important;
            border-radius: 20px !important;
            padding: 34px 38px !important;
            box-shadow: {theme["hover_shadow"]} !important;
            margin-top: 10px;
            margin-bottom: 24px;
        }}

        .vl-auth-divider {{
            display: flex;
            align-items: center;
            text-align: center;
            margin: 22px 0 16px 0;
            color: {theme["muted"]};
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}

        .vl-auth-divider::before,
        .vl-auth-divider::after {{
            content: '';
            flex: 1;
            border-bottom: 1px solid {theme["border"]};
        }}

        .vl-auth-divider:not(:empty)::before {{
            margin-right: 1em;
        }}

        .vl-auth-divider:not(:empty)::after {{
            margin-left: 1em;
        }}

        /* Checkbox styling */
        [data-testid="stCheckbox"] label span,
        [data-testid="stCheckbox"] label p,
        [data-testid="stCheckbox"] label div {{
            color: {theme["text"]} !important;
            font-size: 0.88rem !important;
        }}

        /* Checkbox square indicator - unchecked */
        [data-testid="stCheckbox"] div[class*="e1ap2qgk"],
        [data-testid="stCheckbox"] label > div > div:first-child,
        div[data-baseweb="checkbox"] > div:first-child {{
            background-color: {theme["surface"]} !important;
            border: 1px solid {theme["border"]} !important;
            border-radius: 4px !important;
            transition: all 0.15s ease !important;
        }}

        /* Checkbox square indicator - hover */
        [data-testid="stCheckbox"]:hover div[class*="e1ap2qgk"],
        [data-testid="stCheckbox"] label:hover > div > div:first-child,
        div[data-baseweb="checkbox"]:hover > div:first-child {{
            border-color: {theme["primary"]} !important;
        }}

        /* Checkbox square indicator - checked */
        [data-testid="stCheckbox"] label:has(input:checked) div[class*="e1ap2qgk"],
        [data-testid="stCheckbox"] label:has(input:checked) > div > div:first-child,
        div[data-baseweb="checkbox"]:has(input:checked) > div:first-child {{
            background-color: {theme["primary"]} !important;
            border-color: {theme["primary"]} !important;
        }}

        [data-testid="stCheckbox"] label:has(input:checked) svg,
        div[data-baseweb="checkbox"]:has(input:checked) svg {{
            stroke: #FFFFFF !important;
            fill: none !important;
        }}

        [data-testid="stCheckbox"] input[type="checkbox"] {{
            accent-color: {theme["primary"]} !important;
        }}

        /* Theme Selector Pill (Skeuomorphic segmented switch) */
        .st-key-vl_theme {{
            display: flex !important;
            justify-content: flex-end !important;
            margin-bottom: 0 !important;
        }}

        .st-key-vl_theme [data-testid="stRadioGroup"],
        .st-key-vl_theme div[role="radiogroup"] {{
            background: {theme["selector_track"]} !important;
            border: 1px solid {theme["border"]} !important;
            border-radius: 20px !important;
            padding: 3px !important;
            box-shadow: {theme["inset_shadow"]} !important;
            display: inline-flex !important;
            gap: 4px !important;
            align-items: center !important;
        }}

        .st-key-vl_theme [data-testid="stRadioOption"],
        .st-key-vl_theme div[role="radiogroup"] label[data-baseweb="radio"],
        .st-key-vl_theme div[role="radiogroup"] label {{
            margin: 0 !important;
            padding: 5px 14px !important;
            border-radius: 16px !important;
            cursor: pointer !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border: 1px solid transparent !important;
            background: transparent !important;
            display: inline-flex !important;
            align-items: center !important;
        }}

        .st-key-vl_theme [data-testid="stRadioOption"]:hover,
        .st-key-vl_theme div[role="radiogroup"] label[data-baseweb="radio"]:hover,
        .st-key-vl_theme div[role="radiogroup"] label:hover {{
            background: {theme["selector_hover"]} !important;
        }}

        .st-key-vl_theme [data-testid="stRadioOption"]:focus,
        .st-key-vl_theme [data-testid="stRadioOption"]:focus-within,
        .st-key-vl_theme div[role="radiogroup"] label[data-baseweb="radio"]:focus,
        .st-key-vl_theme div[role="radiogroup"] label[data-baseweb="radio"]:focus-visible,
        .st-key-vl_theme div[role="radiogroup"] label:focus-within {{
            background: {theme["selector_hover"]} !important;
            outline: 2px solid {theme["focus_ring"]} !important;
            outline-offset: -1px !important;
        }}

        .st-key-vl_theme [data-testid="stRadioOption"]:active,
        .st-key-vl_theme div[role="radiogroup"] label[data-baseweb="radio"]:active,
        .st-key-vl_theme div[role="radiogroup"] label:active {{
            background: {theme["active_pill_bg"]} !important;
        }}

        /* Hide the native radio circle so it behaves as a segmented control without ugly black dots */
        .st-key-vl_theme [data-testid="stRadioOption"] > div > div:first-child,
        .st-key-vl_theme [data-testid="stRadioOption"] [class*="e1dm8mpf4"],
        .st-key-vl_theme div[role="radiogroup"] label > div > div:first-child,
        .st-key-vl_theme div[role="radiogroup"] label[data-baseweb="radio"] > div:first-of-type {{
            display: none !important;
        }}

        .st-key-vl_theme [data-testid="stRadioOption"] div,
        .st-key-vl_theme [data-testid="stRadioOption"] p,
        .st-key-vl_theme div[role="radiogroup"] label[data-baseweb="radio"] div,
        .st-key-vl_theme div[role="radiogroup"] label[data-baseweb="radio"] p,
        .st-key-vl_theme div[role="radiogroup"] label div,
        .st-key-vl_theme div[role="radiogroup"] label p {{
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            color: {theme["muted"]} !important;
            letter-spacing: 0.01em !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1.2 !important;
        }}

        /* Active pill state */
        .st-key-vl_theme [data-testid="stRadioOption"][data-selected="true"],
        .st-key-vl_theme [data-testid="stRadioOption"]:has(input:checked),
        .st-key-vl_theme div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked),
        .st-key-vl_theme div[role="radiogroup"] label:has(input:checked) {{
            background: {theme["active_pill_bg"]} !important;
            border-color: {theme["active_pill_border"]} !important;
            box-shadow: {theme["active_pill_shadow"]} !important;
        }}

        .st-key-vl_theme [data-testid="stRadioOption"][data-selected="true"] div,
        .st-key-vl_theme [data-testid="stRadioOption"][data-selected="true"] p,
        .st-key-vl_theme [data-testid="stRadioOption"]:has(input:checked) div,
        .st-key-vl_theme [data-testid="stRadioOption"]:has(input:checked) p,
        .st-key-vl_theme div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) div,
        .st-key-vl_theme div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) p,
        .st-key-vl_theme div[role="radiogroup"] label:has(input:checked) div,
        .st-key-vl_theme div[role="radiogroup"] label:has(input:checked) p {{
            color: {theme["primary"]} !important;
            font-weight: 700 !important;
        }}
    </style>
    """


def apply_theme(theme_name: str) -> None:
    """Apply the selected visual theme using custom CSS."""
    css = get_theme_css(theme_name)
    st.markdown(css, unsafe_allow_html=True)
