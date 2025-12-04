"""
Task-related components for Point Jewels Dashboard
Specialized components for task management UI.
"""

from typing import Dict, Any, List
from utils.config import COLORS, ICONS
from utils.helpers import html_escape, is_task_overdue
from components.ui import render_status_indicator, render_badge

def get_priority_badge(priority: str) -> str:
    """Get HTML for priority badge."""
    priority_colors = {
        "critical": "#dc2626",
        "high": "#ea580c",
        "medium": "#ca8a04",
        "low": "#16a34a"
    }

    priority_icons = {
        "critical": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢"
    }

    color = priority_colors.get(priority, "#6b7280")
    icon = priority_icons.get(priority, "⚪")

    return f"""
    <span style="
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(255,255,255,0.1);
        color: {color};
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    ">
        {icon} {html_escape(priority)}
    </span>
    """

def render_task_card(task: Dict[str, Any]) -> None:
    """
    Render a single task card with enhanced visual feedback and accessibility.

    Args:
        task: Task data dictionary
    """
    import streamlit as st

    status_icon = ICONS["completed"] if task["status"] == "completed" else ICONS["pending"]
    is_overdue_flag = is_task_overdue(task)
    card_class = "task-complete" if task["status"] == "completed" else ("task-overdue" if is_overdue_flag else "task-pending")
    priority_badge = get_priority_badge(task["priority"])

    # Status indicator for the card
    status_indicator = render_status_indicator(
        "completed" if task["status"] == "completed" else "overdue" if is_overdue_flag else "pending"
    )

    # Priority color coding
    priority_colors = {
        "critical": "#dc2626",
        "high": "#ea580c",
        "medium": "#ca8a04",
        "low": "#16a34a"
    }
    priority_color = priority_colors.get(task["priority"], "#6b7280")

    # Accessibility attributes
    aria_label = f"Task: {html_escape(task['task'])}. Status: {html_escape(task['status'])}. Priority: {html_escape(task['priority'])}. Due: {html_escape(task['deadline'])}. Assigned to: {html_escape(task['assignee'])}"
    if is_overdue_flag:
        aria_label += ". This task is overdue."

    st.markdown(f"""
    <div class="task-card {card_class}" style="
        border-left: 4px solid {priority_color};
        position: relative;
        overflow: hidden;
    "
    role="article"
    aria-label="{aria_label}"
    tabindex="0">
        <div style="
            position: absolute;
            top: 8px;
            right: 8px;
            opacity: 0.7;
        ">
            {status_indicator}
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding-right: 30px;">
            <span style="font-size: 16px; color: white; font-weight: 500;">{status_icon} {html_escape(task['task'])}</span>
            {priority_badge}
        </div>
        <div style="margin-top: 8px; color: {COLORS['text_dark']}; font-size: 13px;">
            📅 Due: {html_escape(task['deadline'])} | 👤 {html_escape(task['assignee'])} | Week {task['week']}
        </div>
        <div style="
            position: absolute;
            bottom: 0;
            left: 0;
            height: 3px;
            background: linear-gradient(90deg, {priority_color} 0%, transparent 100%);
            width: {80 if task['status'] == 'completed' else 40}%;
            transition: width 0.3s ease;
        "></div>
    </div>
    """, unsafe_allow_html=True)

def render_task_filters(current_filter: str) -> str:
    """
    Render task filter buttons.

    Args:
        current_filter: Currently active filter

    Returns:
        Selected filter value
    """
    import streamlit as st

    col1, col2, col3, col4, col5 = st.columns(5)

    filters = {
        "all": ("All Tasks", col1),
        "pending": ("Pending", col2),
        "completed": ("Completed", col3),
        "overdue": ("Overdue", col4),
        "critical": ("Critical", col5)
    }

    selected_filter = current_filter

    for filter_key, (label, col) in filters.items():
        with col:
            if st.button(
                label,
                key=f"filter_{filter_key}",
                use_container_width=True,
                type="primary" if current_filter == filter_key else "secondary"
            ):
                selected_filter = filter_key

    return selected_filter

def filter_tasks(tasks: List[Dict[str, Any]], filter_type: str) -> List[Dict[str, Any]]:
    """
    Filter tasks based on filter type.

    Args:
        tasks: List of task dictionaries
        filter_type: Filter type

    Returns:
        Filtered list of tasks
    """
    if filter_type == "all":
        return tasks
    elif filter_type == "pending":
        return [t for t in tasks if t["status"] == "pending"]
    elif filter_type == "completed":
        return [t for t in tasks if t["status"] == "completed"]
    elif filter_type == "overdue":
        return [t for t in tasks if is_task_overdue(t) and t["status"] != "completed"]
    elif filter_type == "critical":
        return [t for t in tasks if t["priority"] == "critical"]
    else:
        return tasks

def render_smart_suggestions(task_input: str, existing_tasks: List[Dict[str, Any]]) -> List[str]:
    """
    Generate smart task suggestions based on input and existing tasks.

    Args:
        task_input: Current task input text
        existing_tasks: List of existing tasks

    Returns:
        List of suggested task completions
    """
    if not task_input or len(task_input) < 3:
        return []

    suggestions = []
    input_lower = task_input.lower()

    # Common task patterns for jewelry website
    common_patterns = [
        "Review and approve",
        "Schedule meeting with",
        "Update project timeline for",
        "Send payment reminder to",
        "Check progress on",
        "Create content for",
        "Test functionality of",
        "Document requirements for",
        "Coordinate with",
        "Finalize design for"
    ]

    # Generate suggestions based on input
    for pattern in common_patterns:
        if any(word in pattern.lower() for word in input_lower.split()):
            suggestion = f"{pattern} {task_input}"
            if suggestion not in [t["task"] for t in existing_tasks]:
                suggestions.append(suggestion)

    # Limit to 3 suggestions
    return suggestions[:3]