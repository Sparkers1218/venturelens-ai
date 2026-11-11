import streamlit as st
from ui.auth import validate_email

DEFAULT_PROFILE = {
    "name": "Alex Rivera",
    "email": "alex.rivera@venturelens.local",
    "role": "Founder & Chief Strategist",
    "organization": "Rivera Ventures · Stealth Lab",
    "bio": "Building empirical AI validation models to stress-test venture hypotheses and uncover defensible market whitespace.",
    "industry": "Enterprise SaaS & HealthTech",
    "tier": "Early Founder Sandbox",
    "status": "Active (Local Session)",
    "member_since": "November 2026",
}


def get_initials(name: str) -> str:
    """Generate 1-2 character uppercase initials from full name."""
    parts = [p.strip() for p in name.strip().split() if p.strip()]
    if not parts:
        return "VL"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def get_user_profile() -> dict:
    """Retrieve or initialize the session user profile."""
    if "user_profile" not in st.session_state:
        st.session_state["user_profile"] = dict(DEFAULT_PROFILE)
    return st.session_state["user_profile"]


def render_profile_view():
    """Render the Founder Profile page with view, edit, and validation modes."""
    profile = get_user_profile()

    st.title("👤 Founder Profile")
    st.caption("Personal identity, workspace designation, and founder bio")
    st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)

    if "profile_editing" not in st.session_state:
        st.session_state["profile_editing"] = False

    is_editing = st.session_state["profile_editing"]

    if not is_editing:
        # --- VIEW MODE ---
        initials = get_initials(profile.get("name", "Alex Rivera"))

        st.markdown(
            f"""
            <div class="vl-card">
                <div style="display: flex; align-items: center; gap: 20px; flex-wrap: wrap;">
                    <div class="vl-avatar">{initials}</div>
                    <div style="flex: 1; min-width: 220px;">
                        <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 4px;">
                            <h2 style="margin: 0; font-size: 1.45rem; font-weight: 800;">{profile.get("name", "Alex Rivera")}</h2>
                            <span class="vl-badge">{profile.get("tier", "Founder Sandbox")}</span>
                        </div>
                        <div style="font-size: 0.95rem; font-weight: 600; opacity: 0.85; margin-bottom: 2px;">
                            {profile.get("role", "Founder")}
                        </div>
                        <div style="font-size: 0.84rem; opacity: 0.7;">
                            {profile.get("email", "founder@venturelens.local")} · Member since {profile.get("member_since", "November 2026")}
                        </div>
                    </div>
                </div>
                <hr style="opacity: 0.25; margin: 20px 0 16px 0;" />
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 16px;">
                    <div>
                        <div style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; opacity: 0.65; margin-bottom: 2px;">Organization</div>
                        <div style="font-size: 0.92rem; font-weight: 600;">{profile.get("organization", "N/A")}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; opacity: 0.65; margin-bottom: 2px;">Target Industry</div>
                        <div style="font-size: 0.92rem; font-weight: 600;">{profile.get("industry", "N/A")}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; opacity: 0.65; margin-bottom: 2px;">Session Status</div>
                        <div style="font-size: 0.92rem; font-weight: 600; color: #3B66DE;">{profile.get("status", "Active Preview")}</div>
                    </div>
                </div>
                <div>
                    <div style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; opacity: 0.65; margin-bottom: 4px;">Founder Bio</div>
                    <p style="font-size: 0.92rem; line-height: 1.55; opacity: 0.85; margin: 0;">
                        {profile.get("bio", "No bio provided.")}
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

        col_act1, col_act2, col_act3, _ = st.columns([1.5, 1.8, 2.2, 2.5])
        with col_act1:
            if st.button("✏️ Edit Profile", key="btn_prof_edit_open", type="primary", use_container_width=True):
                st.session_state["profile_editing"] = True
                st.rerun()

        with col_act2:
            if st.button("🔄 Reset Profile", key="btn_prof_reset", use_container_width=True):
                st.session_state["user_profile"] = dict(DEFAULT_PROFILE)
                st.success("Profile restored to default template.")
                st.rerun()

        with col_act3:
            if st.button("🔐 Switch Account", key="btn_prof_switch_auth", use_container_width=True):
                st.session_state["nav_page"] = "Sign In / Sign Up"
                st.session_state["auth_mode"] = "login"
                st.rerun()

    else:
        # --- EDIT MODE ---
        st.markdown(
            """
            <div class="vl-card" style="margin-bottom: 16px;">
                <h3 style="margin: 0 0 4px 0; font-size: 1.25rem; font-weight: 700;">Edit Profile Information</h3>
                <p style="font-size: 0.86rem; opacity: 0.75; margin: 0;">
                    Update your founder designation, contact info, and workspace bio for this session.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        with c1:
            edit_name = st.text_input(
                "Full Name",
                value=profile.get("name", ""),
                key="input_prof_name",
                help="Your display name visible across project reports.",
            )
            edit_role = st.text_input(
                "Role / Designation",
                value=profile.get("role", ""),
                key="input_prof_role",
                placeholder="e.g. Founder & CEO, Technical Co-founder",
            )
            edit_org = st.text_input(
                "Organization / Studio",
                value=profile.get("organization", ""),
                key="input_prof_org",
                placeholder="e.g. Rivera Ventures, Stealth AI Lab",
            )

        with c2:
            edit_email = st.text_input(
                "Work Email Address",
                value=profile.get("email", ""),
                key="input_prof_email",
                help="Email address used for workspace reports and notifications.",
            )
            edit_industry = st.selectbox(
                "Primary Industry Focus",
                options=[
                    "Enterprise SaaS & HealthTech",
                    "FinTech & InsurTech",
                    "Consumer AI & Apps",
                    "Developer Tools & Infra",
                    "ClimateTech & Clean Energy",
                    "E-Commerce & Supply Chain",
                    "EdTech & Future of Work",
                    "Other",
                ],
                index=0,
                key="input_prof_industry",
            )
            edit_tier = st.text_input(
                "Workspace Tier",
                value=profile.get("tier", "Early Founder Sandbox"),
                disabled=True,
                help="Tenancy tier managed by backend provisioning (Milestone 4).",
            )

        edit_bio = st.text_area(
            "Founder Bio & Focus Areas",
            value=profile.get("bio", ""),
            height=110,
            key="input_prof_bio",
            help="Short summary of your venture goals and focus areas.",
        )

        st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)

        b_save, b_cancel, _ = st.columns([1.6, 1.4, 4.0])
        with b_save:
            if st.button("💾 Save Changes", key="btn_prof_save", type="primary", use_container_width=True):
                # Validate inputs
                clean_name = edit_name.strip()
                if not clean_name:
                    st.error("⚠️ Full name is required.")
                elif len(clean_name) < 2:
                    st.error("⚠️ Name must be at least 2 characters long.")
                else:
                    valid_email, email_err = validate_email(edit_email)
                    if not valid_email:
                        st.error(f"⚠️ {email_err}")
                    else:
                        st.session_state["user_profile"] = {
                            "name": clean_name,
                            "email": edit_email.strip(),
                            "role": edit_role.strip() or "Founder",
                            "organization": edit_org.strip() or "Independent Venture",
                            "industry": edit_industry,
                            "bio": edit_bio.strip() or "No bio provided.",
                            "tier": profile.get("tier", "Early Founder Sandbox"),
                            "status": profile.get("status", "Active (Local Session)"),
                            "member_since": profile.get("member_since", "November 2026"),
                        }
                        st.session_state["profile_editing"] = False
                        st.success("✅ Profile updated successfully for this session!")
                        st.rerun()

        with b_cancel:
            if st.button("✖️ Cancel", key="btn_prof_cancel", use_container_width=True):
                st.session_state["profile_editing"] = False
                st.rerun()

    # Honest architecture callout
    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    st.info(
        "ℹ️ Session Storage Checkpoint: Profile modifications are preserved within your active Streamlit session "
        "(`st.session_state`). Per-user persistent storage (PostgreSQL/SQLAlchemy) and authenticated user claims (OIDC) "
        "will connect in Milestones 3 & 4."
    )
