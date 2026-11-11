import streamlit as st
from ui.profile_view import get_user_profile

DEFAULT_PREFERENCES = {
    "default_landing": "Dashboard",
}


def get_user_preferences() -> dict:
    """Retrieve or initialize the session user preferences."""
    if "user_preferences" not in st.session_state:
        st.session_state["user_preferences"] = dict(DEFAULT_PREFERENCES)
    return st.session_state["user_preferences"]


def validate_password_change(current_pwd: str, new_pwd: str, confirm_pwd: str) -> tuple[bool, dict[str, str]]:
    """Validate password change inputs on the frontend."""
    errors = {}
    if not current_pwd:
        errors["current_pwd"] = "Current password is required."

    if not new_pwd:
        errors["new_pwd"] = "New password is required."
    elif len(new_pwd) < 8:
        errors["new_pwd"] = "New password must be at least 8 characters long."

    if not confirm_pwd:
        errors["confirm_pwd"] = "Please confirm your new password."
    elif new_pwd != confirm_pwd:
        errors["confirm_pwd"] = "New passwords do not match."

    if current_pwd and new_pwd and current_pwd == new_pwd:
        errors["new_pwd"] = "New password must be different from your current password."

    return len(errors) == 0, errors


def render_settings_view():
    """Render the Account Settings workspace view with Personal Preferences, Security, and Account Info."""
    profile = get_user_profile()
    prefs = get_user_preferences()

    st.title("⚙️ Account Settings")
    st.caption("Personal preferences, security controls, and workspace tenancy")
    st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)

    tab_pref, tab_sec, tab_info = st.tabs([
        "🎨 Personal Preferences",
        "🔐 Security & Password",
        "ℹ️ Account Information",
    ])

    # ----------------------------------------------------
    # TAB 1: PERSONAL PREFERENCES
    # ----------------------------------------------------
    with tab_pref:
        st.markdown(
            """
            <div class="vl-card" style="margin-bottom: 16px;">
                <h3 style="margin: 0 0 4px 0; font-size: 1.2rem; font-weight: 700;">Appearance & Workspace Preferences</h3>
                <p style="font-size: 0.86rem; opacity: 0.75; margin: 0;">
                    Configure your visual theme, landing route, and command center preferences.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        pref_col1, pref_col2 = st.columns(2)

        with pref_col1:
            current_theme = st.session_state.get("vl_theme", "Light")
            theme_choice = st.radio(
                "Theme Mode",
                options=["Light", "Dark"],
                index=0 if current_theme == "Light" else 1,
                format_func=lambda x: "☀️ Light Theme" if x == "Light" else "🌙 Dark Theme",
                key="settings_theme_radio",
                help="Applies instantly to the VentureLens AI hybrid skeuomorphic theme engine.",
            )

            if theme_choice != current_theme:
                st.session_state["vl_theme"] = theme_choice
                st.rerun()

        with pref_col2:
            pref_landing = st.selectbox(
                "Default Landing Workspace",
                options=["Dashboard", "My Projects", "Competitor Insights", "Research"],
                index=["Dashboard", "My Projects", "Competitor Insights", "Research"].index(
                    prefs.get("default_landing", "Dashboard")
                ) if prefs.get("default_landing", "Dashboard") in ["Dashboard", "My Projects", "Competitor Insights", "Research"] else 0,
                key="settings_pref_landing",
                help="Primary view opened when launching your session.",
            )

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

        if st.button("💾 Save Preferences", key="btn_save_prefs", type="primary"):
            st.session_state["user_preferences"] = {
                "default_landing": pref_landing,
            }
            st.success("✅ Preferences saved for this session!")

    # ----------------------------------------------------
    # TAB 2: SECURITY & PASSWORD
    # ----------------------------------------------------
    with tab_sec:
        st.markdown(
            """
            <div class="vl-card" style="margin-bottom: 16px;">
                <h3 style="margin: 0 0 4px 0; font-size: 1.2rem; font-weight: 700;">Password & Security Credentials</h3>
                <p style="font-size: 0.86rem; opacity: 0.75; margin: 0;">
                    Manage your workspace authentication credentials according to security policy.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        show_pwd = st.checkbox("Show passwords", key="settings_pwd_reveal")

        sec_col1, sec_col2 = st.columns(2)
        with sec_col1:
            curr_pwd = st.text_input(
                "Current Password",
                type="default" if show_pwd else "password",
                placeholder="Enter existing password",
                key="settings_curr_pwd",
            )
            new_pwd = st.text_input(
                "New Password",
                type="default" if show_pwd else "password",
                placeholder="Min. 8 characters",
                key="settings_new_pwd",
                help="Must contain at least 8 characters.",
            )

        with sec_col2:
            st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
            confirm_pwd = st.text_input(
                "Confirm New Password",
                type="default" if show_pwd else "password",
                placeholder="Re-enter new password",
                key="settings_confirm_pwd",
            )

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

        if st.button("Update Password ➔", key="btn_change_pwd", type="primary"):
            is_valid, errors = validate_password_change(curr_pwd, new_pwd, confirm_pwd)
            if not is_valid:
                for field, err in errors.items():
                    st.error(f"⚠️ {err}")
            else:
                st.success("✅ Password conforms to security requirements!")
                st.info(
                    "ℹ️ Backend Security Notice: Cryptographic password hashing (Argon2 / bcrypt) "
                    "and secure database updates will execute in Milestone 4. No credentials were sent or stored."
                )

        st.markdown("<hr style='opacity: 0.25; margin: 24px 0 16px 0;' />", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="font-size: 0.84rem; opacity: 0.8; line-height: 1.5;">
                🔒 <strong>Password Policy:</strong> Minimum 8 characters. Must differ from current password.
                Multi-Factor Authentication (MFA) and OIDC token revocation will be configurable in Milestone 4.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ----------------------------------------------------
    # TAB 3: ACCOUNT INFORMATION
    # ----------------------------------------------------
    with tab_info:
        st.markdown(
            f"""
            <div class="vl-card" style="margin-bottom: 16px;">
                <h3 style="margin: 0 0 10px 0; font-size: 1.2rem; font-weight: 700;">Workspace & Tenancy Profile</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 14px;">
                    <div>
                        <div style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; opacity: 0.65; margin-bottom: 2px;">Account Email</div>
                        <div style="font-size: 0.92rem; font-weight: 600;">{profile.get("email", "founder@venturelens.local")}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; opacity: 0.65; margin-bottom: 2px;">Login Provider</div>
                        <div style="font-size: 0.92rem; font-weight: 600;">Local Guest Session (OIDC Pending)</div>
                    </div>
                    <div>
                        <div style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; opacity: 0.65; margin-bottom: 2px;">Session Status</div>
                        <div style="font-size: 0.92rem; font-weight: 600; color: #3B66DE;">🟢 Active (Offline Preview)</div>
                    </div>
                    <div>
                        <div style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; opacity: 0.65; margin-bottom: 2px;">Tenancy Partition</div>
                        <div style="font-size: 0.92rem; font-weight: 600;">tenant-guest-001 (Isolated)</div>
                    </div>
                </div>
                <hr style="opacity: 0.2; margin: 16px 0;" />
                <h4 style="margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 700;">Integration Roadmap Status</h4>
                <div style="font-size: 0.86rem; line-height: 1.6; opacity: 0.85;">
                    • <strong>Milestone 1 & 2</strong>: Project Foundation & Premium UI/UX (Completed)<br />
                    • <strong>Milestone 3</strong>: User Workspace UI (Active) · PostgreSQL Backend (Dev 1)<br />
                    • <strong>Milestone 4</strong>: OpenID Connect (OIDC) Authentication & Multi-Tenancy (Pending)<br />
                    • <strong>Milestone 5</strong>: External Market Research APIs & Real-Time Tracking (Pending)<br />
                    • <strong>Milestone 6</strong>: Multi-Model AI Conviction Scoring & Export (Pending)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        b_dash, _ = st.columns([1.8, 4.2])
        with b_dash:
            if st.button("← Return to Dashboard", key="btn_settings_back", use_container_width=True):
                st.session_state["nav_page"] = "Dashboard"
                st.rerun()
