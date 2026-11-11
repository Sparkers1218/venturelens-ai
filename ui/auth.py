import re
import streamlit as st

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
MIN_PASSWORD_LENGTH = 8


def validate_email(email: str) -> tuple[bool, str | None]:
    """Validate email presence and RFC format."""
    clean_email = email.strip()
    if not clean_email:
        return False, "Email address is required."
    if not EMAIL_REGEX.match(clean_email):
        return False, "Please enter a valid email address (e.g. founder@venture.com)."
    return True, None


def validate_password(password: str) -> tuple[bool, str | None]:
    """Validate password presence and minimum length."""
    if not password:
        return False, "Password is required."
    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters long."
    return True, None


def validate_login(email: str, password: str) -> tuple[bool, dict[str, str]]:
    """Validate login form inputs."""
    errors = {}
    valid_email, email_err = validate_email(email)
    if not valid_email:
        errors["email"] = email_err

    if not password:
        errors["password"] = "Password is required."

    return len(errors) == 0, errors


def validate_signup(name: str, email: str, password: str, confirm_password: str) -> tuple[bool, dict[str, str]]:
    """Validate registration form inputs."""
    errors = {}
    clean_name = name.strip()
    if not clean_name:
        errors["name"] = "Full name is required."
    elif len(clean_name) < 2:
        errors["name"] = "Name must be at least 2 characters long."

    valid_email, email_err = validate_email(email)
    if not valid_email:
        errors["email"] = email_err

    valid_pwd, pwd_err = validate_password(password)
    if not valid_pwd:
        errors["password"] = pwd_err

    if not confirm_password:
        errors["confirm_password"] = "Please confirm your password."
    elif password != confirm_password:
        errors["confirm_password"] = "Passwords do not match."

    return len(errors) == 0, errors


def validate_reset(email: str) -> tuple[bool, dict[str, str]]:
    """Validate password reset form inputs."""
    errors = {}
    valid_email, email_err = validate_email(email)
    if not valid_email:
        errors["email"] = email_err
    return len(errors) == 0, errors


def render_auth_header():
    """Render consistent VentureLens AI branding and tagline."""
    st.markdown(
        """
        <div style="text-align: center; margin-top: 8px; margin-bottom: 22px;">
            <div style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 6px;">
                <span style="font-size: 1.6rem;">🔎</span>
                <span style="font-size: 1.5rem; font-weight: 800; letter-spacing: -0.02em;">VentureLens AI</span>
            </div>
            <div style="font-size: 0.92rem; font-weight: 600; opacity: 0.85; margin-bottom: 4px;">
                Better Questions. Stronger Ideas.
            </div>
            <div style="font-size: 0.8rem; opacity: 0.65;">
                Startup Intelligence & Hypothesis Validation Platform
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_login_screen():
    """Render the Login screen with email, password, show/hide, remember me, forgot password, and OAuth."""
    st.markdown(
        """
        <div style="margin-bottom: 18px;">
            <h2 style="font-size: 1.35rem; font-weight: 700; margin-bottom: 4px;">Welcome Back</h2>
            <p style="font-size: 0.88rem; opacity: 0.8; margin-bottom: 0;">
                Sign in to access your startup intelligence command center.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    email = st.text_input(
        "Work Email",
        placeholder="founder@venturelens.local",
        key="auth_login_email",
        help="The email address associated with your VentureLens workspace.",
    )

    show_pwd = st.checkbox("Show password", key="auth_login_show_pwd")
    password = st.text_input(
        "Password",
        type="default" if show_pwd else "password",
        placeholder="Enter your password",
        key="auth_login_pwd",
    )

    col_remember, col_forgot = st.columns([1.2, 1.2])
    with col_remember:
        st.checkbox("Remember me", value=True, key="auth_login_remember")
    with col_forgot:
        st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
        if st.button("Forgot Password?", key="auth_btn_to_forgot", help="Reset your account password"):
            st.session_state["auth_mode"] = "forgot_password"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

    if st.button("Sign In ➔", key="auth_btn_login_submit", type="primary", use_container_width=True):
        is_valid, errors = validate_login(email, password)
        if not is_valid:
            for field, err in errors.items():
                st.error(f"⚠️ {err}")
        else:
            st.success("✅ Form inputs validated successfully!")
            st.info(
                "ℹ️ Frontend Checkpoint: Credentials conform to the frontend validation schema. "
                "Persistent authentication and session tokens will connect in Milestone 4 "
                "(OpenID Connect / OIDC). You are currently exploring in guest preview mode."
            )

    st.markdown('<div class="vl-auth-divider">OR CONTINUE WITH</div>', unsafe_allow_html=True)

    if st.button("🌐 Continue with Google", key="auth_btn_google_login", use_container_width=True):
        st.info(
            "ℹ️ Google OAuth 2.0 / OIDC sign-in will be integrated in Milestone 4. "
            "Backend identity provider token exchange is pending."
        )

    st.markdown("<hr style='opacity: 0.2; margin: 24px 0 16px 0;' />", unsafe_allow_html=True)

    st.markdown(
        "<div style='text-align: center; font-size: 0.88rem; opacity: 0.85; margin-bottom: 8px;'>Don't have an account yet?</div>",
        unsafe_allow_html=True,
    )
    if st.button("Create an Account", key="auth_btn_switch_signup", use_container_width=True):
        st.session_state["auth_mode"] = "signup"
        st.rerun()

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    if st.button("← Return to Dashboard Preview", key="auth_btn_login_back_dash", use_container_width=True):
        st.session_state["nav_page"] = "Dashboard"
        st.rerun()


def render_signup_screen():
    """Render the Sign Up screen with full name, email, password confirmation, show/hide, and OAuth."""
    st.markdown(
        """
        <div style="margin-bottom: 18px;">
            <h2 style="font-size: 1.35rem; font-weight: 700; margin-bottom: 4px;">Create Your Account</h2>
            <p style="font-size: 0.88rem; opacity: 0.8; margin-bottom: 0;">
                Start stress-testing your startup ideas and uncovering market whitespace.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    name = st.text_input(
        "Full Name",
        placeholder="Alex Rivera",
        key="auth_signup_name",
        help="Your founder or teammate name.",
    )

    email = st.text_input(
        "Work Email",
        placeholder="founder@venturelens.local",
        key="auth_signup_email",
        help="We recommend using your work email address.",
    )

    show_pwd = st.checkbox("Show passwords", key="auth_signup_show_pwd")

    password = st.text_input(
        "Password",
        type="default" if show_pwd else "password",
        placeholder="Min. 8 characters",
        key="auth_signup_pwd",
        help="Must be at least 8 characters.",
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="default" if show_pwd else "password",
        placeholder="Re-enter your password",
        key="auth_signup_confirm",
    )

    st.caption("🔒 By registering, you agree to local preview terms. Per-user data tenancy connects in Milestone 4.")

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

    if st.button("Create Account ➔", key="auth_btn_signup_submit", type="primary", use_container_width=True):
        is_valid, errors = validate_signup(name, email, password, confirm_password)
        if not is_valid:
            for field, err in errors.items():
                st.error(f"⚠️ {err}")
        else:
            st.success(f"✅ Account details validated for {name.strip()}!")
            st.info(
                "ℹ️ Frontend Checkpoint: Registration fields validated successfully. "
                "Database account creation, password hashing (Argon2 / bcrypt), and tenant provisioning "
                "will connect in Milestones 3 & 4 (PostgreSQL & OIDC)."
            )

    st.markdown('<div class="vl-auth-divider">OR REGISTER WITH</div>', unsafe_allow_html=True)

    if st.button("🌐 Sign Up with Google", key="auth_btn_google_signup", use_container_width=True):
        st.info(
            "ℹ️ Google OAuth 2.0 / OIDC registration will connect in Milestone 4. "
            "Backend identity contracts are pending."
        )

    st.markdown("<hr style='opacity: 0.2; margin: 24px 0 16px 0;' />", unsafe_allow_html=True)

    st.markdown(
        "<div style='text-align: center; font-size: 0.88rem; opacity: 0.85; margin-bottom: 8px;'>Already have an account?</div>",
        unsafe_allow_html=True,
    )
    if st.button("Sign In to Existing Account", key="auth_btn_switch_login", use_container_width=True):
        st.session_state["auth_mode"] = "login"
        st.rerun()

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    if st.button("← Return to Dashboard Preview", key="auth_btn_signup_back_dash", use_container_width=True):
        st.session_state["nav_page"] = "Dashboard"
        st.rerun()


def render_forgot_password_screen():
    """Render the Forgot Password screen with explanation, email input, and recovery instructions."""
    st.markdown(
        """
        <div style="margin-bottom: 18px;">
            <h2 style="font-size: 1.35rem; font-weight: 700; margin-bottom: 4px;">Reset Your Password</h2>
            <p style="font-size: 0.88rem; opacity: 0.8; line-height: 1.5; margin-bottom: 0;">
                Enter your verified work email address below. We'll generate a secure, time-limited reset
                link to restore access to your startup workspaces.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    email = st.text_input(
        "Work Email Address",
        placeholder="founder@venturelens.local",
        key="auth_forgot_email",
        help="The email address registered with your VentureLens account.",
    )

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

    if st.button("Send Reset Link ➔", key="auth_btn_forgot_submit", type="primary", use_container_width=True):
        is_valid, errors = validate_reset(email)
        if not is_valid:
            for field, err in errors.items():
                st.error(f"⚠️ {err}")
        else:
            st.success(f"✅ Reset request validated for '{email.strip()}'!")
            st.info(
                "ℹ️ Frontend Checkpoint: Reset request schema verified. "
                "Transactional email delivery and cryptographic reset tokens will connect in Milestone 4. "
                "No external email was dispatched."
            )

    st.markdown("<hr style='opacity: 0.2; margin: 24px 0 16px 0;' />", unsafe_allow_html=True)

    if st.button("← Back to Sign In", key="auth_btn_forgot_back_login", use_container_width=True):
        st.session_state["auth_mode"] = "login"
        st.rerun()

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    if st.button("← Return to Dashboard Preview", key="auth_btn_forgot_back_dash", use_container_width=True):
        st.session_state["nav_page"] = "Dashboard"
        st.rerun()


def render_auth_view():
    """Render the centered, premium authentication view supporting Login, Sign Up, and Forgot Password."""
    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "login"

    mode = st.session_state["auth_mode"]

    # Centered responsive 3-column layout
    spacer_left, center_card, spacer_right = st.columns([1.1, 2.2, 1.1])

    with center_card:
        render_auth_header()

        # Mode quick switcher (Sign In vs Create Account) when not in forgot_password mode
        if mode in ("login", "signup"):
            tab_c1, tab_c2 = st.columns(2)
            with tab_c1:
                if st.button(
                    "Sign In",
                    key="tab_switch_login",
                    type="primary" if mode == "login" else "secondary",
                    use_container_width=True,
                ):
                    st.session_state["auth_mode"] = "login"
                    st.rerun()
            with tab_c2:
                if st.button(
                    "Create Account",
                    key="tab_switch_signup",
                    type="primary" if mode == "signup" else "secondary",
                    use_container_width=True,
                ):
                    st.session_state["auth_mode"] = "signup"
                    st.rerun()

            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

        if mode == "login":
            render_login_screen()
        elif mode == "signup":
            render_signup_screen()
        elif mode == "forgot_password":
            render_forgot_password_screen()
