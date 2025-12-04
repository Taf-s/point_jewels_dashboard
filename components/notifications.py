"""
Notification components for Point Jewels Dashboard
Smart notification system for alerts and updates.
"""

from typing import Dict, Any, List
import streamlit as st
from utils.config import COLORS
from utils.helpers import html_escape, is_task_overdue, get_days_remaining

def render_toast() -> None:
    """Render toast notification if one exists."""
    if st.session_state.toast_message:
        toast_colors = {
            'success': COLORS['success'],
            'error': COLORS['danger'],
            'warning': COLORS['warning'],
            'info': COLORS['info']
        }

        # Enhanced toast with progress ring and better animations
        st.markdown(f"""
        <div style="
            position: fixed;
            top: 20px;
            right: 20px;
            background: {toast_colors.get(st.session_state.toast_type, COLORS['info'])};
            color: white;
            padding: 16px 24px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            z-index: 1000;
            animation: slideInBounce 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            display: flex;
            align-items: center;
            gap: 12px;
        ">
            <div style="
                width: 20px;
                height: 20px;
                border: 2px solid rgba(255,255,255,0.3);
                border-top: 2px solid white;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            "></div>
            <span style="font-weight: 500; font-size: 14px;">{html_escape(st.session_state.toast_message)}</span>
        </div>
        <style>
            @keyframes slideInBounce {{
                0% {{ transform: translateX(100%) scale(0.8); opacity: 0; }}
                50% {{ transform: translateX(-10px) scale(1.05); }}
                100% {{ transform: translateX(0) scale(1); opacity: 1; }}
            }}
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
        </style>
        """, unsafe_allow_html=True)

        # Auto-clear toast after 4 seconds with fade out
        st.session_state.toast_message = None

def show_toast(message: str, toast_type: str = 'success') -> None:
    """
    Show a toast notification with Apple-style animation.

    Args:
        message: Notification message
        toast_type: Type of notification ('success', 'error', 'warning', 'info')
    """
    st.session_state.toast_message = message
    st.session_state.toast_type = toast_type

def render_advanced_notifications() -> List[Dict[str, Any]]:
    """
    Generate smart notifications based on project state.

    Returns:
        List of notification dictionaries
    """
    # This would be called with actual data in the main app
    # For now, return empty list as placeholder
    return []

def generate_notifications(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate contextual notifications based on project data.

    Args:
        data: Project data dictionary

    Returns:
        List of notification dictionaries
    """
    notifications = []

    # Check for overdue tasks
    overdue_tasks = [t for t in data["tasks"] if is_task_overdue(t) and t["status"] != "completed"]
    if overdue_tasks:
        notifications.append({
            'type': 'urgent',
            'title': f"{len(overdue_tasks)} Overdue Task{'s' if len(overdue_tasks) > 1 else ''}",
            'message': f"You have {len(overdue_tasks)} task{'s' if len(overdue_tasks) > 1 else ''} past their deadline.",
            'action': 'View Tasks'
        })

    # Check budget warnings
    finances = data["finances"]
    budget_used = ((finances.get('received', []) + finances.get('paid_out', [])) / finances.get('budget_total', 1)) * 100
    if budget_used > 90:
        notifications.append({
            'type': 'budget',
            'title': 'Budget Alert',
            'message': f"You've used {budget_used:.1f}% of your budget. Consider reviewing expenses.",
            'action': 'View Finances'
        })

    # Check upcoming deadlines (next 3 days)
    upcoming_tasks = []
    for task in data["tasks"]:
        if task["status"] != "completed":
            try:
                deadline = datetime.strptime(task["deadline"], "%Y-%m-%d")
                days_until = (deadline - datetime.now()).days
                if 0 <= days_until <= 3:
                    upcoming_tasks.append(task)
            except ValueError:
                continue

    if upcoming_tasks:
        notifications.append({
            'type': 'warning',
            'title': f"{len(upcoming_tasks)} Task{'s' if len(upcoming_tasks) > 1 else ''} Due Soon",
            'message': f"You have {len(upcoming_tasks)} task{'s' if len(upcoming_tasks) > 1 else ''} due within 3 days.",
            'action': 'View Tasks'
        })

    # Check days remaining
    days_left = get_days_remaining(data["project"])
    if days_left <= 7 and days_left > 0:
        notifications.append({
            'type': 'milestone',
            'title': f"Launch in {days_left} Days",
            'message': f"Your project launches on {data['project']['launch_date']}. Time to finalize!",
            'action': 'View Timeline'
        })

    return notifications

def render_notification_center(notifications: List[Dict[str, Any]]) -> None:
    """
    Render the notification center with all active notifications.

    Args:
        notifications: List of notification dictionaries
    """
    if not notifications:
        st.info("🎉 All caught up! No notifications at this time.")
        return

    st.markdown(f"### 🔔 Smart Notifications ({len(notifications)})")

    for notification in notifications:
        col1, col2, col3 = st.columns([0.1, 4, 1])

        # Notification icon
        with col1:
            icon_map = {
                'urgent': '🚨',
                'warning': '⚠️',
                'overdue': '⏰',
                'budget': '💰',
                'milestone': '🎯'
            }
            st.markdown(icon_map.get(notification['type'], '📢'))

        # Notification content
        with col2:
            st.markdown(f"**{notification['title']}**")
            st.markdown(notification['message'])

        # Action button
        with col3:
            if st.button(notification.get('action', 'View'), key=f"action_{notification['type']}"):
                # This would trigger navigation in the main app
                pass