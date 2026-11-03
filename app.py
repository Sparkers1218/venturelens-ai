import streamlit as st

from config.settings import get_settings


settings = get_settings()

st.set_page_config(page_title=settings.app_name, layout="centered")
st.title(settings.app_name)
st.caption("Better Questions. Stronger Ideas.")

st.write(
    "VentureLens AI is being built to help aspiring entrepreneurs investigate "
    "startup ideas, examine evidence, identify assumptions, and plan practical "
    "validation experiments."
)
st.info(
    "Project foundation stage: authentication, database access, AI analysis, "
    "and external research are not implemented yet."
)
