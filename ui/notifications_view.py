import streamlit as st

INITIAL_NOTIFICATIONS = [
    {
        "id": "notif-001",
        "title": "Validation Stage 1 Initialized",
        "description": "Your project workspace has completed Idea Ingestion and is ready for assumption mapping.",
        "timestamp": "12 minutes ago",
        "category": "Milestone",
        "icon": "💡",
        "read": False,
    },
    {
        "id": "notif-002",
        "title": "Competitor Signal Detected",
        "description": "A new AI documentation tool launched on Product Hunt targeting your primary ICP segment.",
        "timestamp": "2 hours ago",
        "category": "Competitor",
        "icon": "⚡",
        "read": False,
    },
    {
        "id": "notif-003",
        "title": "Search Trend Signal: EHR Voice AI",
        "description": "Keyword search volume for ambient medical scribe workflows rose 34% over the last 30 days.",
        "timestamp": "Yesterday",
        "category": "Research",
        "icon": "🔬",
        "read": True,
    },
    {
        "id": "notif-004",
        "title": "Local Preview Session Active",
        "description": "VentureLens AI is operating in Milestone 3 local preview mode. Offline guest session is active.",
        "timestamp": "3 days ago",
        "category": "System",
        "icon": "🔔",
        "read": True,
    },
]


def get_notifications() -> list[dict]:
    """Retrieve or initialize the session notifications list."""
    if "notifications" not in st.session_state:
        st.session_state["notifications"] = [dict(n) for n in INITIAL_NOTIFICATIONS]
    return st.session_state["notifications"]


def get_unread_count() -> int:
    """Calculate the number of unread notifications in session state."""
    notifs = get_notifications()
    return sum(1 for n in notifs if not n.get("read", False))


def mark_notification_read(notif_id: str, read_state: bool = True) -> None:
    """Update read status of a specific notification."""
    notifs = get_notifications()
    for n in notifs:
        if n.get("id") == notif_id:
            n["read"] = read_state
            break


def mark_all_read() -> None:
    """Mark all notifications as read."""
    notifs = get_notifications()
    for n in notifs:
        n["read"] = True


def clear_all_notifications() -> None:
    """Remove all notifications from current session."""
    st.session_state["notifications"] = []


def reset_sample_notifications() -> None:
    """Restore the default illustrative notifications."""
    st.session_state["notifications"] = [dict(n) for n in INITIAL_NOTIFICATIONS]


def render_notifications_view():
    """Render the Notification Center workspace view with filtering, read/unread states, and bulk actions."""
    notifs = get_notifications()
    unread_count = get_unread_count()

    st.title("🔔 Notifications")
    st.caption("Intelligence alerts, competitor shifts, and validation milestones")
    st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)

    # Top Toolbar: Filter pills and Bulk Actions
    col_filter, col_bulk = st.columns([3.2, 2.8])

    with col_filter:
        filter_mode = st.radio(
            "Filter Notifications",
            options=["All", "Unread"],
            format_func=lambda x: f"All ({len(notifs)})" if x == "All" else f"Unread ({unread_count})",
            horizontal=True,
            label_visibility="collapsed",
            key="notif_filter_radio",
        )

    with col_bulk:
        st.markdown("<div style='display: flex; gap: 8px; justify-content: flex-end;'>", unsafe_allow_html=True)
        b_c1, b_c2 = st.columns(2)
        with b_c1:
            if st.button("Mark All as Read", key="btn_notif_mark_all", disabled=unread_count == 0, use_container_width=True):
                mark_all_read()
                st.rerun()
        with b_c2:
            if st.button("Clear All", key="btn_notif_clear_trigger", disabled=len(notifs) == 0, use_container_width=True):
                st.session_state["confirm_clear_notifs"] = True
                st.rerun()

    # Clear confirmation modal/dialog block
    if st.session_state.get("confirm_clear_notifs", False):
        st.markdown(
            """
            <div class="vl-card" style="margin: 16px 0; border-color: rgba(239, 68, 68, 0.4);">
                <div style="font-weight: 700; margin-bottom: 4px;">⚠️ Confirm Clear Notifications</div>
                <div style="font-size: 0.88rem; opacity: 0.85; margin-bottom: 12px;">
                    Are you sure you want to clear all notifications from this session? This action cannot be undone.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        conf_col1, conf_col2, _ = st.columns([1.6, 1.4, 4.0])
        with conf_col1:
            if st.button("Yes, Clear All", key="btn_confirm_clear_yes", type="primary", use_container_width=True):
                clear_all_notifications()
                st.session_state["confirm_clear_notifs"] = False
                st.rerun()
        with conf_col2:
            if st.button("Cancel", key="btn_confirm_clear_no", use_container_width=True):
                st.session_state["confirm_clear_notifs"] = False
                st.rerun()

    st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

    # Filtered list
    if filter_mode == "Unread":
        displayed = [n for n in notifs if not n.get("read", False)]
    else:
        displayed = notifs

    if not displayed:
        # Empty state
        if filter_mode == "Unread" and len(notifs) > 0:
            st.markdown(
                """
                <div class="vl-card" style="text-align: center; padding: 36px 20px; margin-bottom: 16px;">
                    <div style="font-size: 2rem; margin-bottom: 8px;">✨</div>
                    <h3 style="margin: 0 0 6px 0; font-weight: 700;">All caught up!</h3>
                    <p style="font-size: 0.9rem; opacity: 0.75; margin: 0;">
                        You have no unread notifications. Check the 'All' tab to view past activity.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="vl-card" style="text-align: center; padding: 40px 24px; margin-bottom: 16px;">
                    <div style="font-size: 2.2rem; margin-bottom: 8px;">🔕</div>
                    <h3 style="margin: 0 0 6px 0; font-weight: 700;">No notifications found</h3>
                    <p style="max-width: 500px; margin: 0 auto 16px auto; font-size: 0.9rem; opacity: 0.75; line-height: 1.5;">
                        Your notification inbox is currently empty. Intelligence alerts will trigger as your startup validation cycles progress.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            col_restore, _ = st.columns([2.0, 4.0])
            with col_restore:
                if st.button("🔄 Load Sample Notifications", key="btn_restore_notifs", use_container_width=True):
                    reset_sample_notifications()
                    st.rerun()
        return

    # Render Notification Cards
    for idx, notif in enumerate(displayed):
        is_read = notif.get("read", False)
        card_cls = "vl-notification-card" if is_read else "vl-notification-card vl-notification-unread"
        status_label = "READ" if is_read else "NEW"

        st.markdown(
            f"""
            <div class="{card_cls}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; margin-bottom: 6px;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 1.25rem;">{notif.get("icon", "🔔")}</span>
                        <div>
                            <span style="font-size: 0.98rem; font-weight: 700;">{notif.get("title", "Untitled Alert")}</span>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; flex-shrink: 0;">
                        <span class="vl-badge" style="font-size: 0.68rem; padding: 2px 7px;">{notif.get("category", "General")}</span>
                        <span style="font-size: 0.76rem; opacity: 0.65;">{notif.get("timestamp", "Recently")}</span>
                    </div>
                </div>
                <div style="font-size: 0.88rem; opacity: 0.85; line-height: 1.5; margin-left: 32px; margin-bottom: 8px;">
                    {notif.get("description", "")}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Action column below each notification card
        act_col, _ = st.columns([1.8, 5.2])
        with act_col:
            btn_label = "Mark as Unread" if is_read else "✓ Mark as Read"
            if st.button(btn_label, key=f"btn_notif_toggle_{notif.get('id', idx)}", use_container_width=True):
                mark_notification_read(notif.get("id"), read_state=not is_read)
                st.rerun()

        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
