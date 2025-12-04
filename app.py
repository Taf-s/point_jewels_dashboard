"""
Point Jewels Project Manager Dashboard
A modern, modular Streamlit dashboard using component-based architecture.
"""

import sys
import os

# Add the current directory to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now try your import
from styles.main import get_custom_css

import streamlit as st
from datetime import datetime

# Import our modular components
from utils.config import COLORS, ICONS

from utils.helpers import (
    load_data, save_data, get_task_stats, get_financial_summary,
    is_task_overdue, get_days_remaining, optimize_performance
)
from components.ui import render_progress_ring, render_status_indicator, render_card, render_metric
from components.tasks import render_task_card, render_task_filters, filter_tasks, render_smart_suggestions
from components.finances import (
    render_payment_card, editable_metric, render_financial_overview, render_budget_breakdown
)
from components.notifications import show_toast, render_toast, generate_notifications, render_notification_center

# ============================================================================
# APP CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="💎 Point Jewels Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = None
if 'toast_message' not in st.session_state:
    st.session_state.toast_message = None
if 'toast_type' not in st.session_state:
    st.session_state.toast_type = 'info'
if 'task_filter' not in st.session_state:
    st.session_state.task_filter = 'all'

# Load CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Load data
data = load_data()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    st.markdown("# 💎 Point Jewels")
    st.markdown("### Project Manager")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        [f"{ICONS['dashboard']} Dashboard", f"{ICONS['tasks']} Tasks", f"{ICONS['finances']} Finances", f"{ICONS['timeline']} Timeline", f"{ICONS['contacts']} Contacts", f"{ICONS['communications']} Communications", f"{ICONS['settings']} Settings"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 📊 Quick Stats")

    stats = get_task_stats(data["tasks"])
    progress = (stats["completed"] / stats["total"] * 100) if stats["total"] > 0 else 0

    st.progress(progress / 100)
    st.caption(f"{stats['completed']}/{stats['total']} tasks complete")

    days_left = get_days_remaining(data["project"])
    if days_left > 0:
        st.metric("Days to Launch", days_left)
    else:
        st.success("🚀 Launched!")

# ============================================================================
# PAGE RENDERERS
# ============================================================================

def render_dashboard_page():
    """Render the main dashboard page."""
    # Load data at the start of the function
    data = load_data()
    stats = get_task_stats(data['tasks'])
    progress = int((stats['completed'] / stats['total']) * 100) if stats['total'] > 0 else 0

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"# {ICONS['dashboard']} Project Dashboard")
        st.markdown(f"**{data['project']['name']}** | Week {data['project']['current_week']} of 6")
    with col2:
        if st.button(f"{ICONS['refresh']} Refresh"):
            data = load_data()
            stats = get_task_stats(data['tasks'])
            progress = int((stats['completed'] / stats['total']) * 100) if stats['total'] > 0 else 0
            st.rerun()

    st.markdown("---")

    # Enhanced Key Metrics with Progress Rings
    finances = optimize_performance()

    # Progress Overview with Rings in organized cards
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)

    # Project Progress Card
    st.markdown(f'''
    <div class="stat-card fade-in">
        <div style="margin-bottom: 16px;">
            <div style="font-size: 18px; color: {COLORS['gold']}; margin-bottom: 8px;">📊 Project Progress</div>
        </div>
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 12px;">
            {render_progress_ring(progress, 100, COLORS['success'], "")}
        </div>
        <div class="stat-value">{stats['completed']}/{stats['total']}</div>
        <div class="stat-label">Tasks Completed</div>
    </div>
    ''', unsafe_allow_html=True)

    # Financial Health Card
    budget_used = ((finances['received'] + finances['paid_out']) / data['finances']['budget_total']) * 100
    profit_margin = (finances['profit'] / data['finances']['budget_total']) * 100 if data['finances']['budget_total'] > 0 else 0

    st.markdown(f'''
    <div class="stat-card fade-in">
        <div style="font-size: 18px; color: {COLORS['gold']}; margin-bottom: 8px;">💰 Financial Health</div>
        <div style="display: flex; justify-content: space-around; align-items: center; margin-bottom: 12px;">
            <div style="text-align: center;">
                {render_progress_ring(budget_used, 80, COLORS['warning'], "")}
                <div style="font-size: 12px; color: {COLORS['text_muted']}; margin-top: 4px;">Budget</div>
            </div>
            <div style="text-align: center;">
                {render_progress_ring(abs(profit_margin), 80, COLORS['success'] if profit_margin > 20 else COLORS['danger'] if profit_margin < 0 else COLORS['warning'], "")}
                <div style="font-size: 12px; color: {COLORS['text_muted']}; margin-top: 4px;">Profit</div>
            </div>
        </div>
        <div class="stat-value">R{finances['profit']:,}</div>
        <div class="stat-label">Total Profit</div>
    </div>
    ''', unsafe_allow_html=True)

    # Status Overview Card
    status_items = [
        ("Project", "active" if data["project"]["status"] == "In Progress" else "completed"),
        ("Week", "active" if data["project"]["current_week"] <= 3 else "completed"),
        ("Budget", "completed" if budget_used < 90 else "warning" if budget_used < 100 else "overdue"),
        ("Tasks", "completed" if progress > 80 else "pending")
    ]

    status_html = ""
    for label, status in status_items:
        indicator = render_status_indicator(status, 8)
        status_color = {
            'completed': COLORS['success'],
            'pending': COLORS['warning'],
            'overdue': COLORS['danger'],
            'active': COLORS['info']
        }.get(status, COLORS['text_muted'])
        status_html += f'<div style="display: flex; align-items: center; margin: 6px 0;">{indicator}<span style="color: {status_color}; font-size: 14px;">{label}</span></div>'

    st.markdown(f'''
    <div class="stat-card fade-in">
        <div style="font-size: 18px; color: {COLORS['gold']}; margin-bottom: 16px;">🎯 Project Status</div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
            {status_html}
        </div>
        <div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid rgba(212, 175, 55, 0.2);">
            <div class="stat-value">{data["project"]["current_week"]}</div>
            <div class="stat-label">Current Week</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Close stats-grid

    st.markdown("---")

    # Financial Summary Cards
    st.markdown("### 💎 Financial Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💰 Total Budget", f"R{data['finances']['budget_total']:,}")
    with col2:
        received_pct = (finances['received'] / data['finances']['budget_total']) * 100
        st.metric("📥 Money In", f"R{finances['received']:,}", f"{received_pct:.1f}% of budget")
    with col3:
        paid_pct = (finances['paid_out'] / data['finances']['budget_total']) * 100
        st.metric("📤 Money Out", f"R{finances['paid_out']:,}", f"{paid_pct:.1f}% spent")
    with col4:
        profit_color = "🟢" if finances['profit'] > 0 else "🔴"
        st.metric(f"{profit_color} Your Profit", f"R{finances['profit']:,}", "net earnings")

    st.markdown("---")

    # This week priorities
    st.markdown("### 🎯 This Week's Priorities")
    current_week = data["project"]["current_week"]
    week_tasks = [t for t in data["tasks"] if t["week"] == current_week]

    if week_tasks:
        critical = [t for t in week_tasks if t["priority"] == "critical"]
        overdue = [t for t in week_tasks if is_task_overdue(t) and t not in critical]
        others = [t for t in week_tasks if t not in critical and t not in overdue]

        for task in critical + overdue + others:
            render_task_card(task)
    else:
        st.info("No tasks scheduled for this week yet.")

    # Strategic Actions
    st.markdown("---")
    st.markdown("### ⚡ One-Click Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📱 Friday Update for Daughters", use_container_width=True):
            st.session_state.action = "daughters_update"

    with col2:
        if st.button("🎨 Monday Check-in for Jared", use_container_width=True):
            st.session_state.action = "jared_checkin"

    with col3:
        if st.button("💾 Save All Data", use_container_width=True):
            save_data(data)
            show_toast("✅ Data saved successfully!", "success")

    # Generated message display
    if st.session_state.get("action") == "daughters_update":
        with st.expander("📱 Copy & Send to Daughters", expanded=True):
            completed = [t["task"] for t in week_tasks if t["status"] == "completed"]
            pending_critical = [t["task"] for t in week_tasks if t["status"] != "completed" and t["priority"] == "critical"]

            message = f"""Week {current_week} update ✓

✅ Completed:
{chr(10).join(['- ' + t for t in completed[:3]]) if completed else '- Building momentum on key tasks'}

🎯 Next Steps:
{chr(10).join(['- ' + t for t in pending_critical[:3]]) if pending_critical else '- All on track!'}

Timeline is locked in. Your dad's going to love this 👍"""

            st.text_area("Ready to send:", message, height=200, disabled=True)
            if st.button(f"{ICONS['copy']} Copy & Clear", key="copy_daughters"):
                st.session_state.action = None
                st.rerun()

def render_tasks_page():
    """Render the tasks management page."""
    st.markdown(f"# {ICONS['tasks']} Task Management")
    st.markdown("---")

    # Task filters
    st.session_state.task_filter = render_task_filters(st.session_state.task_filter)

    # Filter tasks
    filtered_tasks = filter_tasks(data["tasks"], st.session_state.task_filter)

    # Task statistics
    total_tasks = len(filtered_tasks)
    completed_tasks = sum(1 for t in filtered_tasks if t["status"] == "completed")
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Tasks", total_tasks)
    with col2:
        st.metric("Completed", completed_tasks)
    with col3:
        st.metric("Completion Rate", f"{completion_rate:.1f}%")

    st.markdown("---")

    # Render filtered tasks
    if filtered_tasks:
        for task in filtered_tasks:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

            with col1:
                render_task_card(task)

            with col2:
                is_complete = task["status"] == "completed"
                if st.checkbox("", value=is_complete, key=f"task_{task['id']}"):
                    if task["status"] != "completed":
                        task["status"] = "completed"
                        show_toast(f"✅ Task completed: {task['task'][:30]}...", "success")
                else:
                    if task["status"] != "pending":
                        task["status"] = "pending"
                        show_toast(f"🔄 Task reopened: {task['task'][:30]}...", "info")

            with col3:
                # Move up/down buttons would go here
                pass

            with col4:
                # Delete button would go here
                pass
    else:
        st.info("No tasks match the current filter.")

    # Advanced Notifications
    notifications = generate_notifications(data)
    if notifications:
        with st.expander(f"🔔 Smart Notifications ({len(notifications)})", expanded=True):
            render_notification_center(notifications)

    st.markdown("---")

    # Enhanced Add Task with Smart Suggestions
    with st.expander("➕ Add New Task", expanded=False):
        # Task input with smart suggestions
        task_input = st.text_input(
            "Task Description",
            placeholder="Start typing to see smart suggestions...",
            key="task_input"
        )

        # Show smart suggestions
        if task_input.strip():
            suggestions = render_smart_suggestions(task_input, data["tasks"])
            if suggestions:
                st.markdown("**💡 Smart Suggestions:**")
                suggestion_cols = st.columns(min(len(suggestions), 3))

                for i, suggestion in enumerate(suggestions):
                    with suggestion_cols[i % 3]:
                        if st.button(
                            suggestion,
                            key=f"suggestion_{i}",
                            help="Click to use this suggestion",
                            use_container_width=True
                        ):
                            st.session_state.task_input = suggestion
                            st.rerun()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            new_week = st.number_input("Week", 1, 6, data["project"]["current_week"])
        with col2:
            new_priority = st.selectbox("Priority", ["low", "medium", "high", "critical"])
        with col3:
            new_assignee = st.text_input("Assignee", value="You")
        with col4:
            new_deadline = st.date_input("Deadline", value=datetime.now().date())

        if st.button("Add Task", type="primary"):
            if task_input.strip():
                new_task = {
                    "id": max([t["id"] for t in data["tasks"]] + [0]) + 1,
                    "task": task_input.strip(),
                    "week": new_week,
                    "deadline": new_deadline.strftime("%Y-%m-%d"),
                    "status": "pending",
                    "assignee": new_assignee,
                    "priority": new_priority
                }
                data["tasks"].append(new_task)
                save_data(data)
                show_toast("✅ Task added successfully!", "success")
                st.rerun()
            else:
                show_toast("❌ Please enter a task description", "error")

def render_finances_page():
    """Render the financial overview page."""
    st.markdown(f"# {ICONS['finances']} Financial Overview")
    st.markdown("---")

    finances = get_financial_summary(data["finances"])

    # Financial overview
    render_financial_overview(data["finances"])

    # Editable budget components
    st.markdown("## 📊 Budget Allocation")
    col1, col2 = st.columns(2)

    with col1:
        new_designer = editable_metric("Designer Total", data['finances']['designer_total'], "designer_total", "R")
        if new_designer is not None:
            data['finances']['designer_total'] = new_designer
            save_data(data)
            show_toast("✅ Designer budget updated!", "success")
            st.rerun()

    with col2:
        new_expenses = editable_metric("Misc Expenses", data['finances']['expenses_misc'], "expenses_misc", "R")
        if new_expenses is not None:
            data['finances']['expenses_misc'] = new_expenses
            save_data(data)
            show_toast("✅ Expenses updated!", "success")
            st.rerun()

    # Cash flow visualization
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📥 Money In")
        for payment in data["finances"]["received"]:
            render_payment_card(payment, "in")
        st.markdown("**Pending Income:**")
        for payment in data["finances"]["pending_in"]:
            render_payment_card(payment, "in")

    with col2:
        st.markdown("### 📤 Money Out")
        for payment in data["finances"]["paid_out"]:
            render_payment_card(payment, "out")
        st.markdown("**Pending Payments:**")
        for payment in data["finances"]["pending_out"]:
            render_payment_card(payment, "out")

    st.markdown("---")

    # Budget breakdown
    render_budget_breakdown(data["finances"])

# ============================================================================
# MAIN APP LOGIC
# ============================================================================

# Page routing
if page == f"{ICONS['dashboard']} Dashboard":
    render_dashboard_page()
elif page == f"{ICONS['tasks']} Tasks":
    render_tasks_page()
elif page == f"{ICONS['finances']} Finances":
    render_finances_page()
elif page == f"{ICONS['timeline']} Timeline":
    st.markdown(f"# {ICONS['timeline']} 6-Week Project Timeline")
    st.markdown("Timeline page - Coming soon!")
elif page == f"{ICONS['contacts']} Contacts":
    st.markdown(f"# {ICONS['contacts']} Contact Management")
    st.markdown("Contacts page - Coming soon!")
elif page == f"{ICONS['communications']} Communications":
    st.markdown(f"# {ICONS['communications']} Communication Templates")
    st.markdown("Communications page - Coming soon!")
elif page == f"{ICONS['settings']} Settings":
    st.markdown(f"# {ICONS['settings']} Settings")
    st.markdown("Settings page - Coming soon!")

# Render toast notifications
render_toast()
