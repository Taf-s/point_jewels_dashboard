"""
Point Jewels Project Manager Dashboard
A pragmatic Streamlit dashboard using principles from:
- Never Split the Difference (clear value, strategic empathy)
- Pragmatic Programming (DRY, simple, solve at source)
"""

import streamlit as st
import json
from datetime import datetime, timedelta
from pathlib import Path
import plotly.graph_objects as go
from typing import Dict, List, Any, TypedDict

# ============================================================================
# TYPE DEFINITIONS
# ============================================================================

class WeekInfo(TypedDict):
    week: int
    name: str
    status: str

class TimelineWeek(TypedDict):
    week: int
    title: str
    dates: str
    milestones: List[str]

# ============================================================================
# ICON SYSTEM (Luxury Jewelry Theme)
# ============================================================================

ICONS = {
    # Status Icons
    "completed": "💎",      # Diamond for completed tasks
    "pending": "⏳",        # Hourglass for pending
    "overdue": "💔",        # Broken heart for overdue
    "critical": "🔴",       # Red diamond for critical

    # Timeline Icons
    "week_complete": "💚",  # Green heart for completed weeks
    "week_current": "💙",   # Blue heart for current week
    "week_upcoming": "🤍",  # White heart for upcoming weeks

    # Navigation Icons
    "dashboard": "🏠",      # Keep house for dashboard
    "tasks": "📋",          # Clipboard for tasks
    "finances": "💰",       # Money bag for finances
    "timeline": "📊",       # Chart for timeline
    "contacts": "👨‍👩‍👧‍👦", # Family for contacts
    "communications": "💌", # Letter for communications
    "settings": "⚙️",       # Keep settings gear

    # Priority Icons
    "high": "🟡",           # Yellow diamond for high priority
    "medium": "🔵",         # Blue circle for medium
    "low": "⚪",             # White circle for low

    # Action Icons
    "save": "💾",           # Floppy disk for save
    "refresh": "🔄",        # Refresh symbol
    "add": "➕",             # Plus for add
    "copy": "📋",           # Clipboard for copy
    "launch": "🚀",         # Rocket for launch
}

# ============================================================================
# INTERACTIVE FEATURES (Apple-Inspired UX)
# ============================================================================

# Initialize session state for interactive features
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = None
if 'toast_message' not in st.session_state:
    st.session_state.toast_message = None
if 'toast_type' not in st.session_state:
    st.session_state.toast_type = 'info'

def show_toast(message: str, toast_type: str = 'success'):
    """Show a toast notification with Apple-style animation."""
    st.session_state.toast_message = message
    st.session_state.toast_type = toast_type

def render_toast():
    """Render toast notification if one exists."""
    if st.session_state.toast_message:
        toast_colors = {
            'success': '#10b981',
            'error': '#ef4444',
            'warning': '#f59e0b',
            'info': '#3b82f6'
        }

        # Enhanced toast with progress ring and better animations
        st.markdown(f"""
        <div style="
            position: fixed;
            top: 20px;
            right: 20px;
            background: {toast_colors.get(st.session_state.toast_type, '#3b82f6')};
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
            <span style="font-weight: 500; font-size: 14px;">{st.session_state.toast_message}</span>
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

def render_progress_ring(percentage: float, size: int = 60, color: str = "#10b981", label: str = ""):
    """Render a circular progress ring with Apple-style design."""
    # Ensure percentage is between 0 and 100
    percentage = max(0, min(100, percentage))

    # Calculate the stroke-dasharray values
    circumference = 2 * 3.14159 * (size / 2 - 4)  # radius = size/2 - stroke_width/2
    stroke_dasharray = f"{circumference * percentage / 100} {circumference}"

    return f"""
    <div style="position: relative; width: {size}px; height: {size}px; display: inline-block;">
        <svg width="{size}" height="{size}" style="transform: rotate(-90deg);">
            <!-- Background circle -->
            <circle cx="{size/2}" cy="{size/2}" r="{size/2 - 4}"
                    stroke="rgba(255,255,255,0.2)" stroke-width="4" fill="none"/>
            <!-- Progress circle -->
            <circle cx="{size/2}" cy="{size/2}" r="{size/2 - 4}"
                    stroke="{color}" stroke-width="4" fill="none"
                    stroke-dasharray="{stroke_dasharray}" stroke-linecap="round"/>
        </svg>
        <div style="
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 12px;
            font-weight: bold;
            color: white;
        ">
            {int(percentage)}%
        </div>
        {f'<div style="position: absolute; top: {size + 5}px; left: 50%; transform: translateX(-50%); font-size: 10px; color: rgba(255,255,255,0.7); white-space: nowrap;">{label}</div>' if label else ''}
    </div>
    """

def render_status_indicator(status: str, size: int = 12):
    """Render a status indicator dot with animation."""
    colors = {
        'completed': '#10b981',
        'pending': '#f59e0b',
        'overdue': '#ef4444',
        'critical': '#dc2626',
        'active': '#3b82f6'
    }

    color = colors.get(status, '#6b7280')

    if status == 'active':
        animation = 'pulse 2s infinite'
    else:
        animation = 'none'

    return f"""
    <div style="
        width: {size}px;
        height: {size}px;
        border-radius: 50%;
        background: {color};
        display: inline-block;
        margin-right: 8px;
        animation: {animation};
        box-shadow: 0 0 8px {color}40;
    "></div>
    <style>
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.7; transform: scale(1.1); }}
        }}
    </style>
    """

def render_micro_animation(element_id: str, animation_type: str = "bounce"):
    """Add micro-animations to elements."""
    animations = {
        'bounce': """
            @keyframes bounce {
                0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
                40% { transform: translateY(-10px); }
                60% { transform: translateY(-5px); }
            }
            animation: bounce 0.6s ease-in-out;
        """,
        'fadeIn': """
            @keyframes fadeIn {
                from { opacity: 0; transform: scale(0.9); }
                to { opacity: 1; transform: scale(1); }
            }
            animation: fadeIn 0.3s ease-out;
        """,
        'slideUp': """
            @keyframes slideUp {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            animation: slideUp 0.4s ease-out;
        """
    }

    return f"""
    <style>
        #{element_id} {{
            {animations.get(animation_type, animations['fadeIn'])}
        }}
    </style>
    """

# ============================================================================
# PHASE 3: MOBILE OPTIMIZATION & ADVANCED FEATURES
# ============================================================================

def detect_mobile_device():
    """Detect if user is on mobile device using JavaScript."""
    return """
    <script>
        function isMobile() {
            return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
                   window.innerWidth <= 768;
        }
        window.isMobileDevice = isMobile();
    </script>
    """

def get_mobile_optimized_css():
    """Mobile-responsive CSS with touch-friendly interactions."""
    return """
    /* Mobile Optimization */
    @media (max-width: 768px) {
        /* Sidebar adjustments */
        .css-1d391kg { /* Sidebar container */
            width: 100% !important;
            position: relative !important;
        }

        .css-1lcbmhc { /* Sidebar content */
            padding: 1rem !important;
        }

        /* Main content adjustments */
        .css-18e3th9 { /* Main container */
            padding: 1rem !important;
            margin-left: 0 !important;
        }

        /* Touch-friendly buttons */
        .stButton > button {
            min-height: 44px !important;
            padding: 12px 16px !important;
            font-size: 16px !important;
            border-radius: 8px !important;
        }

        /* Larger touch targets for mobile */
        .task-card {
            padding: 16px !important;
            margin: 8px 0 !important;
            border-radius: 12px !important;
        }

        /* Progress rings - smaller on mobile */
        .progress-ring {
            width: 50px !important;
            height: 50px !important;
        }

        /* Stack columns vertically on mobile */
        .css-1r6slb0 { /* Columns container */
            flex-direction: column !important;
        }

        .css-1cpxqw2 { /* Column */
            width: 100% !important;
            margin-bottom: 1rem !important;
        }

        /* Toast notifications - full width on mobile */
        .toast-notification {
            left: 10px !important;
            right: 10px !important;
            width: auto !important;
        }

        /* Navigation tabs - horizontal scroll on mobile */
        .css-1avcm0n { /* Tab container */
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
        }

        /* Form inputs - larger on mobile */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {
            font-size: 16px !important;
            padding: 12px !important;
        }

        /* Metrics - stack vertically */
        .css-1xarl3l { /* Metric container */
            flex-direction: column !important;
            text-align: center !important;
        }
    }

    /* Touch-friendly interactions */
    @media (hover: none) and (pointer: coarse) {
        /* Remove hover effects on touch devices */
        .task-card:hover {
            transform: none !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        }

        /* Larger tap targets */
        button, .clickable {
            min-height: 44px !important;
            min-width: 44px !important;
        }

        /* Prevent zoom on input focus */
        input[type="text"],
        input[type="number"],
        select,
        textarea {
            font-size: 16px !important;
        }
    }

    /* Accessibility improvements */
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }

    /* High contrast mode support */
    @media (prefers-contrast: high) {
        .task-card {
            border: 2px solid currentColor !important;
        }

        .progress-ring circle {
            stroke-width: 6px !important;
        }
    }

    /* Dark mode optimizations */
    @media (prefers-color-scheme: dark) {
        .task-card {
            background: rgba(30, 30, 30, 0.8) !important;
            backdrop-filter: blur(10px) !important;
        }
    }
    """

def render_smart_suggestions(task_input: str, existing_tasks: List[Dict[str, Any]]):
    """Provide smart suggestions based on task input and existing tasks."""
    suggestions = []

    if not task_input.strip():
        return suggestions

    input_lower = task_input.lower()

    # Task type suggestions
    task_types = {
        "design": ["Create mockups", "Review designs", "Update branding", "Design review"],
        "development": ["Code review", "Implement feature", "Fix bug", "Deploy to staging"],
        "payment": ["Send invoice", "Receive payment", "Process refund", "Update budget"],
        "meeting": ["Client call", "Team standup", "Design review", "Project update"],
        "content": ["Write copy", "Create assets", "Update website", "Social media"]
    }

    for category, tasks in task_types.items():
        if category in input_lower:
            suggestions.extend(tasks)

    # Existing task patterns
    for task in existing_tasks[-5:]:  # Last 5 tasks
        if input_lower in task["task"].lower() or any(word in task["task"].lower() for word in input_lower.split()):
            similar_tasks = [t["task"] for t in existing_tasks if t != task and task["task"].lower() in t["task"].lower()]
            suggestions.extend(similar_tasks[:2])  # Max 2 similar tasks

    # Remove duplicates and limit to 5 suggestions
    seen = set()
    unique_suggestions = []
    for suggestion in suggestions:
        if suggestion.lower() not in seen and len(unique_suggestions) < 5:
            seen.add(suggestion.lower())
            unique_suggestions.append(suggestion)

    return unique_suggestions

def render_advanced_notifications():
    """Advanced notification system with scheduling and smart alerts."""
    # Initialize notification preferences in session state
    if 'notification_settings' not in st.session_state:
        st.session_state.notification_settings = {
            'task_deadlines': True,
            'budget_alerts': True,
            'weekly_updates': True,
            'milestone_reminders': True,
            'quiet_hours': {'start': '22:00', 'end': '08:00'}
        }

    notifications = []

    # Smart deadline notifications
    current_week = data["project"]["current_week"]
    week_tasks = [t for t in data["tasks"] if t["week"] == current_week]

    for task in week_tasks:
        if task["status"] != "completed":
            days_until_deadline = (datetime.strptime(task["deadline"], "%Y-%m-%d") - datetime.now()).days

            if days_until_deadline == 0:
                notifications.append({
                    'type': 'urgent',
                    'title': 'Task Due Today',
                    'message': f"'{task['task']}' is due today",
                    'action': 'complete_task',
                    'task_id': task['id']
                })
            elif days_until_deadline == 1:
                notifications.append({
                    'type': 'warning',
                    'title': 'Task Due Tomorrow',
                    'message': f"'{task['task']}' is due tomorrow",
                    'action': 'view_task',
                    'task_id': task['id']
                })
            elif days_until_deadline < 0:
                notifications.append({
                    'type': 'overdue',
                    'title': 'Overdue Task',
                    'message': f"'{task['task']}' is {abs(days_until_deadline)} days overdue",
                    'action': 'view_task',
                    'task_id': task['id']
                })

    # Budget alerts
    finances = get_financial_summary(data["finances"])
    budget_used = ((finances['received'] + finances['paid_out']) / data['finances']['budget_total']) * 100

    if budget_used > 85:
        notifications.append({
            'type': 'budget',
            'title': 'Budget Alert',
            'message': f"Budget utilization at {budget_used:.1f}%",
            'action': 'view_finances'
        })

    # Weekly milestone reminders
    if current_week < 6:
        week_progress = len([t for t in week_tasks if t["status"] == "completed"]) / len(week_tasks) if week_tasks else 0

        if week_progress < 0.5:
            notifications.append({
                'type': 'milestone',
                'title': 'Weekly Progress',
                'message': f"Week {current_week} is {week_progress*100:.0f}% complete",
                'action': 'view_tasks'
            })

    return notifications

def render_touch_friendly_button(label: str, key: str, icon: str = "", help_text: str = "", use_container_width: bool = False):
    """Render a touch-friendly button optimized for mobile."""
    button_style = f"""
    <style>
        .touch-button-{key} {{
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 8px !important;
            min-height: 44px !important;
            padding: 12px 16px !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            border-radius: 8px !important;
            border: none !important;
            background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['secondary']}) !important;
            color: white !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
            text-decoration: none !important;
        }}
        .touch-button-{key}:hover {{
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        }}
        .touch-button-{key}:active {{
            transform: translateY(0) !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        }}
        @media (max-width: 768px) {{
            .touch-button-{key} {{
                width: 100% !important;
                margin: 4px 0 !important;
            }}
        }}
    </style>
    """

    button_html = f"""
    {button_style}
    <button class="touch-button-{key}" title="{help_text}">
        {icon} {label}
    </button>
    """

    return button_html

def optimize_performance():
    """Performance optimizations for better mobile experience."""
    # Lazy loading for heavy components
    # Caching expensive calculations
    # Debounced input handling

    # Cache expensive calculations
    if 'cached_financial_summary' not in st.session_state:
        st.session_state.cached_financial_summary = None
        st.session_state.last_financial_update = None

    current_time = datetime.now()
    if (st.session_state.last_financial_update is None or
        (current_time - st.session_state.last_financial_update).seconds > 30):  # Cache for 30 seconds
        st.session_state.cached_financial_summary = get_financial_summary(data["finances"])
        st.session_state.last_financial_update = current_time

    return st.session_state.cached_financial_summary

def editable_metric(label: str, value: float, key: str, prefix: str = "R", suffix: str = "", help_text: str = ""):
    """Create an editable metric with click-to-edit functionality."""
    edit_key = f"edit_{key}"
    form_key = f"form_{key}"

    # Initialize session state if needed
    if edit_key not in st.session_state:
        st.session_state[edit_key] = False

    col1, col2 = st.columns([4, 1])

    with col1:
        # Display current value as a button to enable editing
        if st.button(f"{prefix}{value:,.0f}{suffix}",
                    key=f"display_{key}",
                    help=help_text or f"Click to edit {label.lower()}",
                    use_container_width=True):
            st.session_state[edit_key] = True
            st.rerun()

        # Show current value as metric when not editing
        if not st.session_state[edit_key]:
            st.metric(label, f"{prefix}{value:,.0f}{suffix}")

    # Show edit form when in edit mode
    if st.session_state[edit_key]:
        with st.container():
            st.markdown(f"### ✏️ Edit {label}")

            with st.form(key=form_key):
                col_a, col_b, col_c = st.columns([2, 1, 1])

                with col_a:
                    new_value = st.number_input(
                        f"New {label}",
                        value=float(value),
                        min_value=0.0,
                        step=1000.0,
                        format="%.0f",
                        help=f"Enter new value for {label.lower()}"
                    )

                with col_b:
                    save_clicked = st.form_submit_button("💾 Save", use_container_width=True)

                with col_c:
                    cancel_clicked = st.form_submit_button("❌ Cancel", use_container_width=True)

            if save_clicked:
                st.session_state[edit_key] = False
                st.success(f"✅ {label} updated successfully!")
                return new_value

            if cancel_clicked:
                st.session_state[edit_key] = False
                st.info("Changes cancelled")
                st.rerun()

    return None

def trigger_financial_chain_reaction(data: Dict[str, Any], change_type: str, amount: float):
    """Trigger all chain reactions when financial amounts change."""
    finances = data["finances"]

    # Recalculate all financial summaries
    new_summary = get_financial_summary(finances)

    # Check for budget alerts
    budget_used = (new_summary['received'] + new_summary['paid_out']) / finances['budget_total'] * 100
    if budget_used > 90:
        show_toast("⚠️ Budget utilization over 90%!", "warning")
    elif budget_used > 100:
        show_toast("🚨 Budget exceeded!", "error")

    # Check profit margins
    if new_summary['profit'] < 0:
        show_toast("📉 Negative profit margin detected", "error")
    elif new_summary['profit'] > finances['budget_total'] * 0.3:  # 30% profit margin
        show_toast("💰 Excellent profit margin!", "success")

    # Update task dependencies based on payments
    update_task_dependencies_from_finances(data)

    return new_summary

def update_task_dependencies_from_finances(data: Dict[str, Any]):
    """Update task statuses based on financial changes."""
    finances = data["finances"]

    # Mark payment tasks as complete when payments are received/made
    for task in data["tasks"]:
        if "payment" in task["task"].lower() or "pay" in task["task"].lower():
            task_complete = False

            if "deposit" in task["task"].lower():
                total_deposits = sum(p["amount"] for p in finances["paid_out"] if "deposit" in p.get("to", "").lower())
                if total_deposits >= 10000:  # Assuming R10k total deposits
                    task_complete = True

            if "milestone" in task["task"].lower():
                total_milestones = sum(p["amount"] for p in finances["paid_out"] if "milestone" in p.get("to", "").lower())
                if total_milestones >= 15000:  # Assuming R15k milestone payments
                    task_complete = True

            if task_complete and task["status"] != "completed":
                task["status"] = "completed"
                show_toast(f"✅ Task completed: {task['task'][:30]}...", "success")

st.set_page_config(
    page_title="Point Jewels | Project Manager",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Mobile device detection
st.markdown(detect_mobile_device(), unsafe_allow_html=True)

DATA_FILE = Path(__file__).parent / "project_data.json"

# ============================================================================
# STYLING SYSTEM (DRY - One source of truth)
# ============================================================================

COLORS = {
    "gold": "#d4af37",
    "dark_bg": "#1a1a2e",
    "dark_accent": "#16213e",
    "darker": "#0f0f23",
    "card_light": "#232342",
    "success": "#4ade80",
    "warning": "#fbbf24",
    "danger": "#ef4444",
    "info": "#60a5fa",
    "text_muted": "#a0a0a0",
    "text_dark": "#888",
}

FONTS = {
    "header": "'Playfair Display', serif",
    "body": "'Source Sans Pro', sans-serif",
}

# CSS compiled once, used everywhere
def get_custom_css():
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap');

        /* Base styling */
        .stApp {{
            background: linear-gradient(135deg, {COLORS['dark_bg']} 0%, {COLORS['dark_accent']} 50%, {COLORS['darker']} 100%);
            font-family: 'Inter', sans-serif;
        }}

        /* Typography */
        h1, h2, h3 {{
            font-family: 'Playfair Display', serif !important;
            color: {COLORS['gold']} !important;
            font-weight: 600 !important;
        }}

        p, li, span, div {{
            font-family: 'Inter', sans-serif;
        }}

        /* Metrics styling */
        [data-testid="metric-container"] {{
            background: linear-gradient(145deg, {COLORS['card_light']} 0%, {COLORS['dark_bg']} 100%);
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }}

        [data-testid="metric-container"]:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(212, 175, 55, 0.2);
        }}

        [data-testid="stMetricValue"] {{
            color: {COLORS['gold']} !important;
            font-family: 'Playfair Display', serif !important;
            font-size: 28px !important;
            font-weight: 700 !important;
        }}

        [data-testid="stMetricLabel"] {{
            color: {COLORS['text_muted']} !important;
            font-size: 14px !important;
            font-weight: 500 !important;
        }}

        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {COLORS['dark_bg']} 0%, {COLORS['darker']} 100%);
            border-right: 2px solid rgba(212, 175, 55, 0.2);
            box-shadow: 2px 0 20px rgba(0,0,0,0.3);
        }}

        /* Button styling */
        .stButton > button {{
            background: linear-gradient(145deg, {COLORS['gold']} 0%, #b8962e 100%);
            color: {COLORS['dark_bg']};
            border: none;
            border-radius: 12px;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            padding: 12px 24px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 16px rgba(212, 175, 55, 0.3);
        }}

        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(212, 175, 55, 0.4);
        }}

        .stButton > button:active {{
            transform: translateY(0);
        }}

        /* Progress bars */
        .stProgress > div > div {{
            background: linear-gradient(90deg, {COLORS['gold']} 0%, #f4d03f 100%);
            border-radius: 8px;
            height: 8px !important;
        }}

        .stProgress > div {{
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
            height: 8px !important;
        }}

        /* Card styling */
        .task-card {{
            background: linear-gradient(145deg, {COLORS['card_light']} 0%, {COLORS['dark_bg']} 100%);
            border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: 16px;
            padding: 24px;
            margin: 12px 0;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }}

        .task-card:hover {{
            border-color: rgba(212, 175, 55, 0.5);
            box-shadow: 0 12px 32px rgba(212, 175, 55, 0.15);
            transform: translateY(-2px);
        }}

        .task-complete {{ border-left: 4px solid {COLORS['success']}; }}
        .task-pending {{ border-left: 4px solid {COLORS['warning']}; }}
        .task-overdue {{ border-left: 4px solid {COLORS['danger']}; }}

        /* Badge styling */
        .badge {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .badge-success {{
            background: rgba(74, 222, 128, 0.2);
            color: {COLORS['success']};
            border: 1px solid rgba(74, 222, 128, 0.3);
        }}

        .badge-warning {{
            background: rgba(251, 191, 36, 0.2);
            color: {COLORS['warning']};
            border: 1px solid rgba(251, 191, 36, 0.3);
        }}

        .badge-danger {{
            background: rgba(239, 68, 68, 0.2);
            color: {COLORS['danger']};
            border: 1px solid rgba(239, 68, 68, 0.3);
        }}

        .badge-info {{
            background: rgba(96, 165, 250, 0.2);
            color: {COLORS['info']};
            border: 1px solid rgba(96, 165, 250, 0.3);
        }}

        /* Progress ring styling */
        .progress-ring {{
            display: inline-block;
            margin: 10px;
        }}

        .progress-ring circle {{
            transition: stroke-dasharray 0.3s ease;
        }}

        /* Stats grid styling */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}

        .stat-card {{
            background: linear-gradient(145deg, {COLORS['card_light']} 0%, {COLORS['dark_bg']} 100%);
            border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 32px rgba(212, 175, 55, 0.15);
        }}

        .stat-value {{
            font-size: 36px;
            font-weight: 700;
            color: {COLORS['gold']};
            font-family: 'Playfair Display', serif;
            margin-bottom: 8px;
        }}

        .stat-label {{
            font-size: 14px;
            color: {COLORS['text_muted']};
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        /* Financial overview styling */
        .financial-overview {{
            background: linear-gradient(145deg, {COLORS['card_light']} 0%, {COLORS['dark_bg']} 100%);
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 20px;
            padding: 32px;
            margin: 24px 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }}

        .financial-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 24px;
            margin-top: 24px;
        }}

        .financial-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(212, 175, 55, 0.1);
        }}

        .financial-card.income {{
            border-left: 4px solid {COLORS['success']};
        }}

        .financial-card.expense {{
            border-left: 4px solid {COLORS['danger']};
        }}

        /* Timeline styling */
        .timeline-container {{
            position: relative;
            padding-left: 40px;
        }}

        .timeline-item {{
            position: relative;
            margin-bottom: 32px;
            padding-left: 24px;
        }}

        .timeline-item::before {{
            content: '';
            position: absolute;
            left: -20px;
            top: 8px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: {COLORS['gold']};
            border: 3px solid {COLORS['dark_bg']};
        }}

        .timeline-item.completed::before {{
            background: {COLORS['success']};
        }}

        .timeline-item.pending::before {{
            background: {COLORS['warning']};
        }}

        .timeline-line {{
            position: absolute;
            left: -17px;
            top: 20px;
            bottom: -20px;
            width: 2px;
            background: linear-gradient(to bottom, {COLORS['gold']}, rgba(212, 175, 55, 0.3));
        }}

        /* Mobile responsiveness */
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}

            .financial-grid {{
                grid-template-columns: 1fr;
            }}

            .stat-card, .financial-card {{
                padding: 16px;
            }}

            .progress-ring {{
                margin: 5px;
            }}
        }}

        /* Animation keyframes */
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .fade-in {{
            animation: fadeIn 0.5s ease-out;
        }}
    </style>
    """
        
        .timeline-week {{
            background: linear-gradient(145deg, {COLORS['card_light']} 0%, {COLORS['dark_bg']} 100%);
            border-radius: 12px;
            padding: 16px;
            margin: 8px 0;
            border-left: 4px solid {COLORS['gold']};
            animation: slideInFade 0.6s ease-out forwards;
            opacity: 0;
            transform: translateX(-20px);
        }}
        
        .timeline-week.current {{
            border-left-color: {COLORS['success']};
            box-shadow: 0 0 20px rgba(74, 222, 128, 0.2);
            animation: slideInFade 0.6s ease-out forwards, pulseGlow 3s infinite;
        }}
        
        @keyframes slideInFade {{
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}
        
        @keyframes pulseGlow {{
            0%, 100% {{ box-shadow: 0 0 20px rgba(74, 222, 128, 0.2); }}
            50% {{ box-shadow: 0 0 30px rgba(74, 222, 128, 0.4); }}
        }}
        .finance-positive {{ color: {COLORS['success']}; }}
        .finance-negative {{ color: {COLORS['danger']}; }}
        
        .streamlit-expanderHeader {{ background: rgba(212, 175, 55, 0.1); border-radius: 8px; }}
        
        hr {{ border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.3), transparent); margin: 24px 0; }}

        {get_mobile_optimized_css()}
    </style>
    """

st.markdown(get_custom_css(), unsafe_allow_html=True)

# ============================================================================
# DATA MANAGEMENT (Single source of truth)
# ============================================================================

def load_data() -> Dict[str, Any]:
    """Load project data or create defaults."""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return get_default_data()

def save_data(data: Dict[str, Any]) -> None:
    """Persist data to disk."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def get_default_data() -> Dict[str, Any]:
    """Return fresh project template."""
    return {
        "project": {
            "name": "Point Jewels Website Revamp",
            "client": "Terry & Liza",
            "start_date": "2024-12-02",
            "launch_date": "2025-01-12",
            "current_week": 1,
            "status": "In Progress"
        },
        "tasks": [
            {"id": 1, "task": "Pay designer R5,000 deposit", "week": 1, "deadline": "2024-12-02", "status": "completed", "assignee": "You", "priority": "critical"},
            {"id": 2, "task": "Send Jared project brief", "week": 1, "deadline": "2024-12-04", "status": "pending", "assignee": "You", "priority": "high"},
            {"id": 3, "task": "Confirm Wednesday meeting with Liza", "week": 1, "deadline": "2024-12-03", "status": "pending", "assignee": "You", "priority": "high"},
            {"id": 4, "task": "Book models for photoshoot", "week": 1, "deadline": "2024-12-04", "status": "pending", "assignee": "You", "priority": "medium"},
            {"id": 5, "task": "Pay Jared second R5,000", "week": 1, "deadline": "2024-12-05", "status": "pending", "assignee": "You", "priority": "critical"},
            {"id": 6, "task": "Wednesday brand meeting with Liza & Jared", "week": 1, "deadline": "2024-12-04", "status": "pending", "assignee": "You", "priority": "critical"},
            {"id": 7, "task": "Scout photoshoot location", "week": 1, "deadline": "2024-12-06", "status": "pending", "assignee": "You", "priority": "medium"},
            {"id": 8, "task": "Send Friday update to daughters", "week": 1, "deadline": "2024-12-06", "status": "pending", "assignee": "You", "priority": "high"},
            {"id": 9, "task": "Conduct photoshoot", "week": 2, "deadline": "2024-12-11", "status": "pending", "assignee": "You", "priority": "critical"},
            {"id": 10, "task": "Jared delivers mockups", "week": 2, "deadline": "2024-12-13", "status": "pending", "assignee": "Jared", "priority": "critical"},
            {"id": 11, "task": "Show Terry mockups", "week": 2, "deadline": "2024-12-13", "status": "pending", "assignee": "You", "priority": "high"},
            {"id": 12, "task": "Pay Jared R7,500 (mockup milestone)", "week": 3, "deadline": "2024-12-16", "status": "pending", "assignee": "You", "priority": "critical"},
            {"id": 13, "task": "Begin website development", "week": 3, "deadline": "2024-12-16", "status": "pending", "assignee": "Jared", "priority": "high"},
            {"id": 14, "task": "Upload product photos", "week": 3, "deadline": "2024-12-20", "status": "pending", "assignee": "You", "priority": "medium"},
            {"id": 15, "task": "Integrate gold price chart", "week": 3, "deadline": "2024-12-20", "status": "pending", "assignee": "Jared", "priority": "medium"},
            {"id": 16, "task": "Working prototype ready", "week": 4, "deadline": "2024-12-27", "status": "pending", "assignee": "Jared", "priority": "critical"},
            {"id": 17, "task": "Show Terry working site", "week": 4, "deadline": "2024-12-27", "status": "pending", "assignee": "You", "priority": "high"},
            {"id": 18, "task": "Mobile optimization", "week": 5, "deadline": "2025-01-03", "status": "pending", "assignee": "Jared", "priority": "high"},
            {"id": 19, "task": "Final testing & QA", "week": 6, "deadline": "2025-01-10", "status": "pending", "assignee": "You", "priority": "critical"},
            {"id": 20, "task": "Train Liza on admin panel", "week": 6, "deadline": "2025-01-10", "status": "pending", "assignee": "You", "priority": "high"},
            {"id": 21, "task": "Pay Jared final R7,500", "week": 6, "deadline": "2025-01-12", "status": "pending", "assignee": "You", "priority": "critical"},
            {"id": 22, "task": "LAUNCH WEBSITE 🚀", "week": 6, "deadline": "2025-01-12", "status": "pending", "assignee": "Everyone", "priority": "critical"},
        ],
        "finances": {
            "budget_total": 50000,
            "received": [
                {"date": "2024-11-25", "amount": 11400, "from": "Terry (50% preliminary)", "status": "received"}
            ],
            "pending_in": [
                {"date": "2024-12-16", "amount": 19300, "from": "Terry (Milestone 2)", "status": "pending"},
                {"date": "2025-01-12", "amount": 19300, "from": "Terry (Final)", "status": "pending"}
            ],
            "paid_out": [
                {"date": "2024-12-02", "amount": 5000, "to": "Jared (Deposit 1)", "status": "paid"}
            ],
            "pending_out": [
                {"date": "2024-12-05", "amount": 5000, "to": "Jared (Deposit 2)", "status": "pending"},
                {"date": "2024-12-16", "amount": 7500, "to": "Jared (Mockup milestone)", "status": "pending"},
                {"date": "2025-01-12", "amount": 7500, "to": "Jared (Final)", "status": "pending"}
            ],
            "designer_total": 20000,
            "expenses_misc": 3000
        },
        "contacts": {
            "terry": {"name": "Terry", "role": "Client (Money)", "notes": "Bulldog negotiator. Wants results, not process. Direct."},
            "liza": {"name": "Liza", "role": "Client (Operations)", "notes": "Kind, timid, your buffer. Keep her unstressed."},
            "daughters": {"name": "Daughters", "role": "Champions", "notes": "Your advocates. Update every Friday."},
            "jared": {"name": "Jared", "role": "Designer", "notes": "R20k total. Has day job. Monday check-ins."}
        },
        "communications": [],
        "risks": []
    }

# ============================================================================
# UTILITY FUNCTIONS (Reusable components)
# ============================================================================

def get_task_stats(tasks: List[Dict[str, Any]]) -> Dict[str, int]:
    """Calculate task statistics."""
    return {
        "total": len(tasks),
        "completed": len([t for t in tasks if t["status"] == "completed"]),
        "pending": len([t for t in tasks if t["status"] == "pending"]),
        "critical": len([t for t in tasks if t["priority"] == "critical"]),
    }

def get_financial_summary(finances: Dict[str, Any]) -> Dict[str, int]:
    """Calculate financial overview."""
    return {
        "received": sum(r["amount"] for r in finances["received"]),
        "pending_in": sum(p["amount"] for p in finances["pending_in"]),
        "paid_out": sum(p["amount"] for p in finances["paid_out"]),
        "pending_out": sum(p["amount"] for p in finances["pending_out"]),
        "profit": finances["budget_total"] - finances["designer_total"] - finances["expenses_misc"],
        "balance": sum(r["amount"] for r in finances["received"]) - sum(p["amount"] for p in finances["paid_out"]),
    }

def is_task_overdue(task: Dict[str, Any]) -> bool:
    """Check if task is past deadline and not complete."""
    if task["status"] == "completed":
        return False
    deadline = datetime.strptime(task["deadline"], "%Y-%m-%d")
    return deadline < datetime.now()

def get_priority_badge(priority: str) -> str:
    """Return HTML badge for priority."""
    badges = {
        "critical": '<span class="badge badge-danger">CRITICAL</span>',
        "high": '<span class="badge badge-warning">HIGH</span>',
        "medium": '<span class="badge badge-info">MEDIUM</span>',
        "low": '<span class="badge badge-info">LOW</span>',
    }
    return badges.get(priority, "")

def render_task_card(task: Dict[str, Any]) -> None:
    """Render a single task card with enhanced visual feedback and accessibility (DRY - used everywhere)."""
    status_icon = ICONS["completed"] if task["status"] == "completed" else ICONS["pending"]
    is_overdue = is_task_overdue(task)
    card_class = "task-complete" if task["status"] == "completed" else ("task-overdue" if is_overdue else "task-pending")
    priority_badge = get_priority_badge(task["priority"])

    # Status indicator for the card
    status_indicator = render_status_indicator(
        "completed" if task["status"] == "completed" else "overdue" if is_overdue else "pending"
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
    aria_label = f"Task: {task['task']}. Status: {task['status']}. Priority: {task['priority']}. Due: {task['deadline']}. Assigned to: {task['assignee']}"
    if is_overdue:
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
            <span style="font-size: 16px; color: white; font-weight: 500;">{status_icon} {task['task']}</span>
            {priority_badge}
        </div>
        <div style="margin-top: 8px; color: {COLORS['text_dark']}; font-size: 13px;">
            📅 Due: {task['deadline']} | 👤 {task['assignee']} | Week {task['week']}
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

def render_payment_card(payment: Dict[str, Any], direction: str = "in") -> None:
    """Render payment card (money in/out)."""
    status = payment["status"]
    is_pending = status == "pending"
    status_icon = ICONS["pending"] if is_pending else ICONS["completed"]
    color = COLORS['warning'] if is_pending else COLORS['success']
    label = payment.get("from") or payment.get("to")
    date_label = "Expected" if is_pending and direction == "in" else "Due" if is_pending else "Date"
    
    st.markdown(f"""
    <div class="task-card {'task-pending' if is_pending else 'task-complete'}">
        <strong style="color: {color};">{status_icon} R{payment['amount']:,}</strong>
        <br><small style="color: {COLORS['text_dark']};"> {label} | {date_label}: {payment['date']}</small>
    </div>
    """, unsafe_allow_html=True)

def get_days_remaining(project: Dict[str, Any]) -> int:
    """Calculate days until launch."""
    launch_date = datetime.strptime(project["launch_date"], "%Y-%m-%d")
    return (launch_date - datetime.now()).days

# ============================================================================
# NAVIGATION & STATE
# ============================================================================

data = load_data()

    # Sidebar navigation
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
# PAGES
# ============================================================================

if page == f"{ICONS['dashboard']} Dashboard":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"# {ICONS['dashboard']} Project Dashboard")
        st.markdown(f"**{data['project']['name']}** | Week {data['project']['current_week']} of 6")
    with col2:
        if st.button(f"{ICONS['refresh']} Refresh"):
            data = load_data()
            st.rerun()
    
    st.markdown("---")

    # Enhanced Key Metrics with Progress Rings (Apple-inspired visual design)
    finances = optimize_performance()  # Use cached financial summary for better performance

    # Progress Overview with Rings in organized cards
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)

    # Project Progress Card
    st.markdown(f'''
    <div class="stat-card fade-in">
        <div style="margin-bottom: 16px;">
            <div style="font-size: 18px; color: {COLORS['gold']}; margin-bottom: 8px;">📊 Project Progress</div>
        </div>
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 12px;">
            {render_progress_ring(progress, 100, "#10b981", "")}
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
                {render_progress_ring(budget_used, 70, "#f59e0b", "")}
                <div style="font-size: 12px; color: {COLORS['text_muted']}; margin-top: 4px;">Budget</div>
            </div>
            <div style="text-align: center;">
                {render_progress_ring(abs(profit_margin), 70, "#10b981" if profit_margin > 20 else "#ef4444" if profit_margin < 0 else "#f59e0b", "")}
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

    # Financial Summary Cards (enhanced)
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
    
    # This week priorities (Strategic: show what matters NOW)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🔥 This Week - Critical & Pending")
        current_week = data["project"]["current_week"]
        week_tasks = [t for t in data["tasks"] if t["week"] == current_week]
        
        # Sort: critical first, then overdue, then pending
        critical = [t for t in week_tasks if t["priority"] == "critical"]
        overdue = [t for t in week_tasks if is_task_overdue(t) and t not in critical]
        others = [t for t in week_tasks if t not in critical and t not in overdue]
        
        for task in critical + overdue + others:
            render_task_card(task)
    
    with col2:
        st.markdown("### 📈 Timeline Progress")

        # Overall project progress ring
        weeks: List[WeekInfo] = [
            {"week": 1, "name": "Kickoff", "status": "current" if current_week == 1 else ("complete" if current_week > 1 else "upcoming")},
            {"week": 2, "name": "Shoot & Mockups", "status": "current" if current_week == 2 else ("complete" if current_week > 2 else "upcoming")},
            {"week": 3, "name": "Dev", "status": "current" if current_week == 3 else ("complete" if current_week > 3 else "upcoming")},
            {"week": 4, "name": "Prototype", "status": "current" if current_week == 4 else ("complete" if current_week > 4 else "upcoming")},
            {"week": 5, "name": "Polish", "status": "current" if current_week == 5 else ("complete" if current_week > 5 else "upcoming")},
            {"week": 6, "name": "LAUNCH 🚀", "status": "current" if current_week == 6 else ("complete" if current_week > 6 else "upcoming")},
        ]

        # Timeline progress visualization
        completed_weeks = sum(1 for w in weeks if w["status"] == "complete")
        timeline_progress = (completed_weeks / len(weeks)) * 100

        col_a, col_b = st.columns([1, 2])
        with col_a:
            timeline_ring = render_progress_ring(timeline_progress, 70, "#8b5cf6", "Timeline")
            st.markdown(timeline_ring, unsafe_allow_html=True)

        with col_b:
            st.markdown(f"**Week {current_week} of 6**")
            current_week_name = next((w["name"] for w in weeks if w["status"] == "current"), "Planning")
            st.markdown(f"*{current_week_name}*")

        st.markdown("---")

        # Enhanced timeline with status indicators
        for i, w in enumerate(weeks):
            icon = ICONS["week_complete"] if w["status"] == "complete" else (ICONS["week_current"] if w["status"] == "current" else ICONS["week_upcoming"])
            highlight = "current" if w["status"] == "current" else ""

            # Status indicator for each week
            week_status = "completed" if w["status"] == "complete" else "active" if w["status"] == "current" else "pending"
            status_dot = render_status_indicator(week_status, 8)

            # Animation delay for cascade effect
            animation_delay = f"animation-delay: {i * 0.1}s;"

            st.markdown(f"""
            <div class="timeline-week {highlight}" style="
                {animation_delay}
                border-left: 3px solid {'#10b981' if w['status'] == 'complete' else '#8b5cf6' if w['status'] == 'current' else '#6b7280'};
                transition: all 0.3s ease;
            ">
                <div style="display: flex; align-items: center; gap: 8px;">
                    {status_dot}
                    <span>{icon}</span>
                    <strong>W{w['week']}</strong>: {w['name']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Strategic Actions (Pragmatic: One button for each key job)
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
            st.success(f"{ICONS['save']} Saved!")
    
    # Generated message display (Strategic empathy: pre-written to reduce friction)
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

elif page == f"{ICONS['tasks']} Tasks":
    st.markdown(f"# {ICONS['tasks']} Task Management")
    st.markdown("---")
    
    # Pragmatic filters (show what matters: status, priority, week)
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_week = st.selectbox("Week", ["All"] + [f"W{i}" for i in range(1, 7)])
    with col2:
        filter_status = st.selectbox("Status", ["All", "Pending", "Completed"])
    with col3:
        filter_priority = st.selectbox("Priority", ["All", "Critical", "High", "Medium"])
    
    st.markdown("---")
    
    # Filter tasks
    filtered = data["tasks"]
    if filter_week != "All":
        week_num = int(filter_week[1:])
        filtered = [t for t in filtered if t["week"] == week_num]
    if filter_status != "All":
        filtered = [t for t in filtered if t["status"] == filter_status.lower()]
    if filter_priority != "All":
        filtered = [t for t in filtered if t["priority"] == filter_priority.lower()]
    
    # Display tasks with checkbox (pragmatic: inline editing)
    for i, task in enumerate(filtered):
        col1, col2, col3, col4 = st.columns([0.3, 0.3, 4, 0.8])

        with col1:
            # Drag up button
            if i > 0 and st.button("⬆️", key=f"up_{task['id']}", help="Move task up"):
                # Find task in original list and swap with previous
                task_idx = data["tasks"].index(task)
                if task_idx > 0:
                    data["tasks"][task_idx], data["tasks"][task_idx - 1] = data["tasks"][task_idx - 1], data["tasks"][task_idx]
                    save_data(data)
                    show_toast("✅ Task moved up", "success")
                    st.rerun()

        with col2:
            # Drag down button
            if i < len(filtered) - 1 and st.button("⬇️", key=f"down_{task['id']}", help="Move task down"):
                # Find task in original list and swap with next
                task_idx = data["tasks"].index(task)
                if task_idx < len(data["tasks"]) - 1:
                    data["tasks"][task_idx], data["tasks"][task_idx + 1] = data["tasks"][task_idx + 1], data["tasks"][task_idx]
                    save_data(data)
                    show_toast("✅ Task moved down", "success")
                    st.rerun()

        with col3:
            is_complete = task["status"] == "completed"
            if st.checkbox("", value=is_complete, key=f"task_{task['id']}"):
                if task["status"] != "completed":
                    task["status"] = "completed"
                    show_toast(f"✅ Task completed: {task['task'][:30]}...", "success")
            else:
                if task["status"] != "pending":
                    task["status"] = "pending"
                    show_toast(f"🔄 Task reopened: {task['task'][:30]}...", "info")

        with col4:
            style = "text-decoration: line-through; color: #666;" if task["status"] == "completed" else ""
            if is_task_overdue(task):
                style = f"color: {COLORS['danger']};"

            st.markdown(f"""
            <div style="{style}">
                <strong>{task['task']}</strong>
                <br><small style="color: {COLORS['text_dark']};">Week {task['week']} | Due: {task['deadline']} | {task['assignee']}</small>
            </div>
            """, unsafe_allow_html=True)

        # Priority indicator (moved to end)
        priority_icons = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
        st.markdown(f"**Priority:** {priority_icons.get(task['priority'], '⚪')} {task['priority'].title()}")

        st.markdown("---")
    
    st.markdown("---")

    # Advanced Notifications
    notifications = render_advanced_notifications()
    if notifications:
        with st.expander(f"🔔 Smart Notifications ({len(notifications)})", expanded=True):
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
                    if notification['type'] in ['urgent', 'warning', 'overdue']:
                        if st.button("View", key=f"view_{notification.get('task_id', notification['type'])}"):
                            # Scroll to task or change page
                            if 'task_id' in notification:
                                st.session_state.scroll_to_task = notification['task_id']
                            st.rerun()

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
            # Smart deadline suggestion based on week
            default_deadline = datetime.now() + timedelta(days=(new_week - data["project"]["current_week"]) * 7)
            new_deadline = st.date_input("Due Date", default_deadline.date())
        with col3:
            new_priority = st.selectbox("Priority", ["critical", "high", "medium", "low"], index=1)
        with col4:
            new_assignee = st.selectbox("Assignee", ["You", "Jared", "Liza", "Everyone"])

        # Touch-friendly add button
        add_button_html = render_touch_friendly_button(
            "Add Task",
            "add_task",
            "➕",
            "Add the new task to your project"
        )

        if st.button("Add Task", key="add_task_btn"):
            task_text = st.session_state.get('task_input', task_input)
            if task_text.strip():
                new_id = max(t["id"] for t in data["tasks"]) + 1
                data["tasks"].append({
                    "id": new_id,
                    "task": task_text,
                    "week": new_week,
                    "deadline": str(new_deadline),
                    "status": "pending",
                    "assignee": new_assignee,
                    "priority": new_priority
                })
                save_data(data)
                show_toast(f"✅ Task added: {task_text[:30]}...", "success")
                # Clear input
                st.session_state.task_input = ""
                st.rerun()
            else:
                st.error("Task description required")

elif page == f"{ICONS['finances']} Finances":
    st.markdown(f"# {ICONS['finances']} Financial Overview")
    st.markdown("---")

    finances = get_financial_summary(data["finances"])

    # Enhanced Financial Summary with better organization
    st.markdown('<div class="financial-overview">', unsafe_allow_html=True)
    st.markdown("## 💰 Financial Summary")

    # Editable budget metrics in organized cards
    st.markdown('<div class="financial-grid">', unsafe_allow_html=True)

    # Budget Total Card
    new_budget = editable_metric("Total Budget", data['finances']['budget_total'], "budget_total", "R")
    if new_budget is not None:
        data['finances']['budget_total'] = new_budget
        save_data(data)
        trigger_financial_chain_reaction(data, "budget_change", new_budget)
        st.rerun()

    st.markdown(f'''
    <div class="financial-card">
        <div style="font-size: 24px; color: {COLORS['gold']}; margin-bottom: 8px;">💼</div>
        <div style="font-size: 28px; font-weight: 700; color: {COLORS['gold']}; margin-bottom: 4px;">R{data['finances']['budget_total']:,}</div>
        <div style="font-size: 14px; color: {COLORS['text_muted']}; font-weight: 500;">TOTAL BUDGET</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 8px;">Click to edit</div>
    </div>
    ''', unsafe_allow_html=True)

    # Income Card
    st.markdown(f'''
    <div class="financial-card income">
        <div style="font-size: 24px; color: {COLORS['success']}; margin-bottom: 8px;">📈</div>
        <div style="font-size: 28px; font-weight: 700; color: {COLORS['success']}; margin-bottom: 4px;">R{finances['received']:,}</div>
        <div style="font-size: 14px; color: {COLORS['text_muted']}; font-weight: 500;">TOTAL RECEIVED</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 8px;">+R{finances['pending_in']:,} pending</div>
    </div>
    ''', unsafe_allow_html=True)

    # Expenses Card
    st.markdown(f'''
    <div class="financial-card expense">
        <div style="font-size: 24px; color: {COLORS['danger']}; margin-bottom: 8px;">📉</div>
        <div style="font-size: 28px; font-weight: 700; color: {COLORS['danger']}; margin-bottom: 4px;">R{finances['paid_out']:,}</div>
        <div style="font-size: 14px; color: {COLORS['text_muted']}; font-weight: 500;">TOTAL PAID</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 8px;">+R{finances['pending_out']:,} pending</div>
    </div>
    ''', unsafe_allow_html=True)

    # Profit Card
    profit_color = COLORS['success'] if finances['profit'] > 0 else COLORS['danger']
    st.markdown(f'''
    <div class="financial-card">
        <div style="font-size: 24px; color: {profit_color}; margin-bottom: 8px;">💰</div>
        <div style="font-size: 28px; font-weight: 700; color: {profit_color}; margin-bottom: 4px;">R{finances['profit']:,}</div>
        <div style="font-size: 14px; color: {COLORS['text_muted']}; font-weight: 500;">PROJECT PROFIT</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 8px;">Balance: R{finances['balance']:,}</div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Close financial-grid

    # Editable budget components
    st.markdown("## 📊 Budget Allocation")
    col1, col2 = st.columns(2)

    with col1:
        new_designer = editable_metric("Designer Total", data['finances']['designer_total'], "designer_total", "R")
        if new_designer is not None:
            data['finances']['designer_total'] = new_designer
            save_data(data)
            trigger_financial_chain_reaction(data, "designer_change", new_designer)
            st.rerun()

    with col2:
        new_expenses = editable_metric("Misc Expenses", data['finances']['expenses_misc'], "expenses_misc", "R")
        if new_expenses is not None:
            data['finances']['expenses_misc'] = new_expenses
            save_data(data)
            trigger_financial_chain_reaction(data, "expenses_change", new_expenses)
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)  # Close financial-overview

    # Render toast notifications
    render_toast()

    st.markdown("---")

    # Cash flow visualization
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

    # Budget breakdown chart
    st.markdown("### 📊 Budget Breakdown")
    fig = go.Figure(data=[go.Pie(
        labels=['Designer (Jared)', 'Misc Expenses', 'Your Profit'],
        values=[data['finances']['designer_total'], data['finances']['expenses_misc'], finances['profit']],
        hole=.6,
        marker_colors=[COLORS['info'], COLORS['warning'], COLORS['success']]
    )])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    st.plotly_chart(fig, use_container_width=True)
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2)
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == f"{ICONS['timeline']} Timeline":
    st.markdown(f"# {ICONS['timeline']} 6-Week Project Timeline")
    st.markdown("---")

    current_week = data["project"]["current_week"]

    # Timeline progress overview
    weeks_timeline: List[TimelineWeek] = [
        {"week": 1, "title": "Kickoff & Activation", "dates": "Dec 2-8", "milestones": ["Designer activated", "Deposits paid", "Brand meeting", "Scope locked"]},
        {"week": 2, "title": "Photoshoot & Mockups", "dates": "Dec 9-15", "milestones": ["Photoshoot done", "Mockups ready", "Terry reviews", "Feedback in"]},
        {"week": 3, "title": "Development", "dates": "Dec 16-22", "milestones": ["Dev starts", "Product uploads", "Charts integrated", "Frontend built"]},
        {"week": 4, "title": "Prototype (Christmas)", "dates": "Dec 23-29", "milestones": ["Working site", "Terry shows approval", "Christmas week buffer"]},
        {"week": 5, "title": "Polish (New Year)", "dates": "Dec 30-Jan 5", "milestones": ["Mobile optimization", "Speed tuning", "Bug fixes", "Final tweaks"]},
        {"week": 6, "title": "LAUNCH 🚀", "dates": "Jan 6-12", "milestones": ["Final QA", "Train Liza", "Last payments", "GO LIVE"]}
    ]

    # Timeline progress calculation
    completed_weeks = sum(1 for w in weeks_timeline if w["week"] < current_week)
    timeline_progress = (completed_weeks / len(weeks_timeline)) * 100

    # Progress overview card
    st.markdown(f'''
    <div class="stat-card" style="margin-bottom: 32px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <div>
                <div style="font-size: 20px; color: {COLORS['gold']}; margin-bottom: 4px;">📈 Timeline Progress</div>
                <div style="font-size: 14px; color: {COLORS['text_muted']};">Week {current_week} of {len(weeks_timeline)}</div>
            </div>
            <div style="text-align: center;">
                {render_progress_ring(timeline_progress, 80, "#8b5cf6", "")}
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div class="stat-value">{completed_weeks}/{len(weeks_timeline)}</div>
                <div class="stat-label">Weeks Completed</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 18px; color: {COLORS['gold']}; font-weight: 600;">{timeline_progress:.0f}%</div>
                <div style="font-size: 12px; color: {COLORS['text_muted']};">Overall Progress</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Visual timeline with proper styling
    st.markdown('<div class="timeline-container">', unsafe_allow_html=True)

    for i, w in enumerate(weeks_timeline):
        is_current: bool = w["week"] == current_week
        is_complete: bool = w["week"] < current_week
        is_upcoming: bool = w["week"] > current_week

        # Determine status and styling
        if is_complete:
            status_class = "completed"
            bg_color = f"background: linear-gradient(145deg, {COLORS['success']}20, {COLORS['card_light']} 100%); border-left: 4px solid {COLORS['success']};"
            icon = ICONS["week_complete"]
        elif is_current:
            status_class = "current"
            bg_color = f"background: linear-gradient(145deg, {COLORS['gold']}20, {COLORS['card_light']} 100%); border-left: 4px solid {COLORS['gold']};"
            icon = ICONS["week_current"]
        else:
            status_class = "upcoming"
            bg_color = f"background: linear-gradient(145deg, {COLORS['card_light']} 0%, {COLORS['dark_bg']} 100%); border-left: 4px solid {COLORS['text_muted']};"
            icon = ICONS["week_upcoming"]

        # Week tasks progress
        week_tasks = [t for t in data["tasks"] if t["week"] == w["week"]]
        completed_tasks = len([t for t in week_tasks if t["status"] == "completed"])
        total_tasks = len(week_tasks)
        task_progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        # Timeline item HTML
        timeline_html = f'''
        <div class="timeline-item {status_class}" style="{bg_color}">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <div>
                    <div style="font-size: 18px; font-weight: 600; color: {COLORS['gold']}; margin-bottom: 4px;">
                        {icon} Week {w['week']}: {w['title']}
                    </div>
                    <div style="font-size: 14px; color: {COLORS['text_muted']}; margin-bottom: 8px;">
                        📅 {w['dates']}
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 14px; color: {COLORS['text_muted']}; margin-bottom: 4px;">Tasks</div>
                    <div style="font-size: 18px; font-weight: 600; color: {COLORS['gold']};">{completed_tasks}/{total_tasks}</div>
                </div>
            </div>

            <div style="margin-bottom: 16px;">
                <div style="font-size: 14px; font-weight: 500; color: white; margin-bottom: 8px;">🎯 Milestones:</div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 8px;">
        '''

        for milestone in w["milestones"]:
            timeline_html += f'<div style="font-size: 13px; color: {COLORS["text_dark"]};">• {milestone}</div>'

        timeline_html += '</div></div>'

        # Add task progress bar if there are tasks
        if total_tasks > 0:
            timeline_html += f'''
            <div style="margin-top: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="font-size: 14px; font-weight: 500; color: white;">📋 Task Progress</div>
                    <div style="font-size: 12px; color: {COLORS['text_muted']};">{task_progress:.0f}%</div>
                </div>
                <div style="width: 100%; height: 6px; background: rgba(255,255,255,0.2); border-radius: 3px; overflow: hidden;">
                    <div style="width: {task_progress}%; height: 100%; background: linear-gradient(90deg, {COLORS['gold']}, #f4d03f); border-radius: 3px; transition: width 0.3s ease;"></div>
                </div>
            </div>
            '''

        timeline_html += '</div>'

        # Add timeline line (except for last item)
        if i < len(weeks_timeline) - 1:
            timeline_html += '<div class="timeline-line"></div>'

        st.markdown(timeline_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Close timeline-container

elif page == f"{ICONS['contacts']} Contacts":
    st.markdown(f"# {ICONS['contacts']} Key Contacts & Communication")
    st.markdown("---")
    
    contacts_info = [
        ("🦁 Terry", "Client (Money)", "terry", [
            "Bulldog negotiator—gets what he wants",
            "Cares about RESULTS, not process",
            "Will test you—stay respectful & firm",
            "Show mockups Week 2, prototype Week 4",
            "Direct but rarely communicates—daughters are buffer"
        ]),
        ("💝 Liza", "Client (Operations)", "liza", [
            "Kind, timid, your stress buffer",
            "KEEP HER UNSTRESSED",
            "Prefers short messages with ❤️",
            "Make her feel valued & included",
            "Her confidence = Terry's confidence"
        ]),
        ("👩‍👧‍👧 Daughters", "Your Champions", "daughters", [
            "Convinced Terry to hire you",
            "Managing his expectations",
            "Update every Friday (critical!)",
            "They defend you to Terry",
            "Most important stakeholders"
        ]),
        ("🎨 Jared", "Designer", "jared", [
            "R20k total (deposits + milestone + final)",
            "Has day job—respect his capacity",
            "Monday check-in calls (non-negotiable)",
            "Same bank = instant transfers",
            "Talented but timid—manage scope creep"
        ]),
    ]
    
    for i, (name, role, key, notes) in enumerate(contacts_info):
        col = st.columns(2)[i % 2]
        with col:
            st.markdown(f"""
            <div class="task-card">
                <h3 style="color: {COLORS['gold']}; margin-top: 0;">{name}</h3>
                <p><strong>Role:</strong> {role}</p>
                <hr>
                <p style="margin: 0;"><strong>Key Points:</strong></p>
                <ul style="margin-top: 8px; padding-left: 20px;">
                    {"".join([f"<li>{n}</li>" for n in notes])}
                </ul>
            </div>
            """, unsafe_allow_html=True)

elif page == f"{ICONS['communications']} Communications":
    st.markdown(f"# {ICONS['communications']} Message Templates")
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📱 Daughters", "🎨 Jared", "💝 Liza"])
    
    with tab1:
        st.markdown("### Friday Update Template")
        week = data["project"]["current_week"]
        daughters_msg = f"""Week {week} update ✓

✅ Completed this week:
- [List 2-3 key wins]

🎯 Coming next:
- [List 2-3 next steps]

Everything locked in for your timeline 👍"""
        st.text_area("Copy & customize:", daughters_msg, height=180, disabled=True)
    
    with tab2:
        st.markdown("### Monday Check-in (5 min call)")
        jared_msg = """Hey Jared, quick sync:

1️⃣ What did you complete last week?
2️⃣ What are you working on this week?
3️⃣ Any blockers I need to clear?

Also confirming [specific deliverable] is on track for [date]?"""
        st.text_area("Use this script:", jared_msg, height=200, disabled=True)
    
    with tab3:
        st.markdown("### Liza Templates")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Meeting Request:**")
            liza_msg = """Hi Liza!

Designer is activated 🎉

Can you do 45min video call Wednesday 4:30pm? Jared wants to hear your brand vision before designing. Super informal, no prep needed ❤️

Link coming tomorrow. Does 4:30 work?"""
            st.text_area("Copy this:", liza_msg, height=150, disabled=True, key="liza1")
        
        with col2:
            st.markdown("**Progress Update:**")
            liza_msg2 = """Hi Liza!

Quick update: Everything on track this week. Designer working on [X], you'll see [Y] by [date].

Focus on the business—I've got the website. Big milestone coming [date] ❤️"""
            st.text_area("Copy this:", liza_msg2, height=150, disabled=True, key="liza2")

elif page == f"{ICONS['settings']} Settings":
    st.markdown(f"# {ICONS['settings']} Settings & Data")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Project")
        new_week = st.number_input("Current Week", 1, 6, data["project"]["current_week"])
        if new_week != data["project"]["current_week"]:
            data["project"]["current_week"] = new_week
            save_data(data)
            st.success("✅ Week updated")
        
        new_status = st.selectbox("Status", ["In Progress", "On Hold", "Completed"], 
                                   index=["In Progress", "On Hold", "Completed"].index(data["project"]["status"]))
        if new_status != data["project"]["status"]:
            data["project"]["status"] = new_status
            save_data(data)
            st.success("✅ Status updated")
    
    with col2:
        st.markdown("### Data Management")
        if st.button("💾 Save All Data"):
            save_data(data)
            st.success(f"{ICONS['save']} Saved!")
        
        if st.button("🔄 Reset to Fresh Data"):
            if st.checkbox("Confirm reset"):
                data = get_default_data()
                save_data(data)
                st.success("✅ Reset complete")
                st.rerun()
    
    st.markdown("---")
    st.download_button(
        "📥 Export Data (JSON)",
        json.dumps(data, indent=2),
        "point_jewels_project_data.json",
        "application/json"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px; font-size: 12px;">
    💎 Point Jewels Project Manager | Built with Streamlit | Pragmatic & Simple
</div>
""", unsafe_allow_html=True)

# Always save on exit
save_data(data)
