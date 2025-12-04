"""
Point Jewels Project Manager Dashboard
A pragmatic Streamlit dashboard using principles from:
- Never Split the Difference (clear value, strategic empathy)
- Pragmatic Programming (DRY, simple, solve at source)
"""

import streamlit as st
import json
from datetime import datetime
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
# CONFIGURATION & SETUP
# ============================================================================

st.set_page_config(
    page_title="Point Jewels | Project Manager",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Source+Sans+Pro:wght@300;400;600&display=swap');
        
        .stApp {{ background: linear-gradient(135deg, {COLORS['dark_bg']} 0%, {COLORS['dark_accent']} 50%, {COLORS['darker']} 100%); }}
        
        h1, h2, h3 {{ font-family: {FONTS['header']} !important; color: {COLORS['gold']} !important; }}
        p, li, span, div {{ font-family: {FONTS['body']}; }}
        
        [data-testid="metric-container"] {{
            background: linear-gradient(145deg, {COLORS['card_light']} 0%, {COLORS['dark_bg']} 100%);
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        
        [data-testid="stMetricValue"] {{ color: {COLORS['gold']} !important; font-family: {FONTS['header']} !important; }}
        [data-testid="stMetricLabel"] {{ color: {COLORS['text_muted']} !important; }}
        
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {COLORS['dark_bg']} 0%, {COLORS['darker']} 100%);
            border-right: 1px solid rgba(212, 175, 55, 0.2);
        }}
        
        .stButton > button {{
            background: linear-gradient(145deg, {COLORS['gold']} 0%, #b8962e 100%);
            color: {COLORS['dark_bg']};
            border: none;
            border-radius: 8px;
            font-weight: 600;
            font-family: {FONTS['body']};
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4); }}
        
        .stProgress > div > div {{ background: linear-gradient(90deg, {COLORS['gold']} 0%, #f4d03f 100%); }}
        
        .task-card {{
            background: linear-gradient(145deg, {COLORS['card_light']} 0%, {COLORS['dark_bg']} 100%);
            border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            transition: all 0.3s ease;
        }}
        
        .task-card:hover {{ border-color: rgba(212, 175, 55, 0.5); box-shadow: 0 8px 30px rgba(212, 175, 55, 0.1); }}
        .task-complete {{ border-left: 4px solid {COLORS['success']}; }}
        .task-pending {{ border-left: 4px solid {COLORS['warning']}; }}
        .task-overdue {{ border-left: 4px solid {COLORS['danger']}; }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .badge-success {{ background: rgba(74, 222, 128, 0.2); color: {COLORS['success']}; }}
        .badge-warning {{ background: rgba(251, 191, 36, 0.2); color: {COLORS['warning']}; }}
        .badge-danger {{ background: rgba(239, 68, 68, 0.2); color: {COLORS['danger']}; }}
        .badge-info {{ background: rgba(96, 165, 250, 0.2); color: {COLORS['info']}; }}
        
        .timeline-week {{
            background: linear-gradient(145deg, {COLORS['card_light']} 0%, {COLORS['dark_bg']} 100%);
            border-radius: 12px;
            padding: 16px;
            margin: 8px 0;
            border-left: 4px solid {COLORS['gold']};
        }}
        
        .timeline-week.current {{ border-left-color: {COLORS['success']}; box-shadow: 0 0 20px rgba(74, 222, 128, 0.2); }}
        .finance-positive {{ color: {COLORS['success']}; }}
        .finance-negative {{ color: {COLORS['danger']}; }}
        
        .streamlit-expanderHeader {{ background: rgba(212, 175, 55, 0.1); border-radius: 8px; }}
        
        hr {{ border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.3), transparent); margin: 24px 0; }}
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
    """Render a single task card (DRY - used everywhere)."""
    status_icon = "✅" if task["status"] == "completed" else "⏳"
    is_overdue = is_task_overdue(task)
    card_class = "task-complete" if task["status"] == "completed" else ("task-overdue" if is_overdue else "task-pending")
    priority_badge = get_priority_badge(task["priority"])
    
    st.markdown(f"""
    <div class="task-card {card_class}">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 16px; color: white;">{status_icon} {task['task']}</span>
            {priority_badge}
        </div>
        <div style="margin-top: 8px; color: {COLORS['text_dark']}; font-size: 13px;">
            📅 Due: {task['deadline']} | 👤 {task['assignee']}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_payment_card(payment: Dict[str, Any], direction: str = "in") -> None:
    """Render payment card (money in/out)."""
    status = payment["status"]
    is_pending = status == "pending"
    status_icon = "⏳" if is_pending else "✅"
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
        ["🏠 Dashboard", "✅ Tasks", "💰 Finances", "📅 Timeline", "👥 Contacts", "📝 Communications", "⚙️ Settings"],
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

if page == "🏠 Dashboard":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("# 🏠 Project Dashboard")
        st.markdown(f"**{data['project']['name']}** | Week {data['project']['current_week']} of 6")
    with col2:
        if st.button("🔄 Refresh"):
            data = load_data()
            st.rerun()
    
    st.markdown("---")
    
    # Key Metrics (Strategic empathy: show what matters to them)
    finances = get_financial_summary(data["finances"])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Project Progress", f"{progress:.0f}%", f"{stats['completed']} of {stats['total']}")
    with col2:
        st.metric("Money In", f"R{finances['received']:,}", f"of R{data['finances']['budget_total']:,}")
    with col3:
        st.metric("Money Out", f"R{finances['paid_out']:,}", "to team")
    with col4:
        st.metric("Your Balance", f"R{finances['balance']:,}", "available")
    
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
        weeks: List[WeekInfo] = [
            {"week": 1, "name": "Kickoff", "status": "current" if current_week == 1 else ("complete" if current_week > 1 else "upcoming")},
            {"week": 2, "name": "Shoot & Mockups", "status": "current" if current_week == 2 else ("complete" if current_week > 2 else "upcoming")},
            {"week": 3, "name": "Dev", "status": "current" if current_week == 3 else ("complete" if current_week > 3 else "upcoming")},
            {"week": 4, "name": "Prototype", "status": "current" if current_week == 4 else ("complete" if current_week > 4 else "upcoming")},
            {"week": 5, "name": "Polish", "status": "current" if current_week == 5 else ("complete" if current_week > 5 else "upcoming")},
            {"week": 6, "name": "LAUNCH 🚀", "status": "current" if current_week == 6 else ("complete" if current_week > 6 else "upcoming")},
        ]
        
        for w in weeks:
            icon = "🟢" if w["status"] == "complete" else ("🔵" if w["status"] == "current" else "⚪")
            highlight = "current" if w["status"] == "current" else ""
            st.markdown(f"""
            <div class="timeline-week {highlight}">
                {icon} <strong>W{w['week']}</strong>: {w['name']}
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
            st.success("✅ Saved!")
    
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
            if st.button("✅ Copy & Clear", key="copy_daughters"):
                st.session_state.action = None
                st.rerun()

elif page == "✅ Tasks":
    st.markdown("# ✅ Task Management")
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
    for task in filtered:
        col1, col2, col3 = st.columns([0.4, 4, 0.8])
        
        with col1:
            is_complete = task["status"] == "completed"
            if st.checkbox("", value=is_complete, key=f"task_{task['id']}"):
                task["status"] = "completed"
            else:
                task["status"] = "pending"
        
        with col2:
            style = "text-decoration: line-through; color: #666;" if task["status"] == "completed" else ""
            if is_task_overdue(task):
                style = f"color: {COLORS['danger']};"
            
            st.markdown(f"""
            <div style="{style}">
                <strong>{task['task']}</strong>
                <br><small style="color: {COLORS['text_dark']};">Week {task['week']} | Due: {task['deadline']} | {task['assignee']}</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            priority_icons = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
            st.markdown(priority_icons.get(task["priority"], "⚪"))
    
    st.markdown("---")
    
    # Add task (pragmatic: simple form)
    with st.expander("➕ Add New Task"):
        new_task = st.text_input("Task", placeholder="What needs to be done?")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            new_week = st.number_input("Week", 1, 6, 1)
        with col2:
            new_deadline = st.date_input("Due")
        with col3:
            new_priority = st.selectbox("Priority", ["critical", "high", "medium", "low"], index=1)
        with col4:
            new_assignee = st.selectbox("Assignee", ["You", "Jared", "Liza", "Everyone"])
        
        if st.button("Add Task"):
            if new_task.strip():
                new_id = max(t["id"] for t in data["tasks"]) + 1
                data["tasks"].append({
                    "id": new_id,
                    "task": new_task,
                    "week": new_week,
                    "deadline": str(new_deadline),
                    "status": "pending",
                    "assignee": new_assignee,
                    "priority": new_priority
                })
                save_data(data)
                st.success("✅ Task added!")
                st.rerun()
            else:
                st.error("Task description required")

elif page == "💰 Finances":
    st.markdown("# 💰 Financial Overview")
    st.markdown("---")
    
    finances = get_financial_summary(data["finances"])
    
    # Summary (Strategic: show the key numbers)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Budget", f"R{data['finances']['budget_total']:,}")
    with col2:
        st.metric("Received", f"R{finances['received']:,}", f"+R{finances['pending_in']:,} pending")
    with col3:
        st.metric("Paid Out", f"R{finances['paid_out']:,}", f"+R{finances['pending_out']:,} pending")
    with col4:
        st.metric("Your Profit", f"R{finances['profit']:,}")
    
    st.markdown("---")
    
    # Cash flow (Pragmatic: side-by-side comparison)
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
    st.markdown("### 📊 Budget Allocation")
    fig: Any = go.Figure(data=[go.Pie(
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
        legend=dict(orientation="h", yanchor="bottom", y=-0.2)
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "📅 Timeline":
    st.markdown("# 📅 6-Week Timeline")
    st.markdown("---")
    
    current_week = data["project"]["current_week"]
    
    weeks_timeline: List[TimelineWeek] = [
        {"week": 1, "title": "Kickoff & Activation", "dates": "Dec 2-8", "milestones": ["Designer activated", "Deposits paid", "Brand meeting", "Scope locked"]},
        {"week": 2, "title": "Photoshoot & Mockups", "dates": "Dec 9-15", "milestones": ["Photoshoot done", "Mockups ready", "Terry reviews", "Feedback in"]},
        {"week": 3, "title": "Development", "dates": "Dec 16-22", "milestones": ["Dev starts", "Product uploads", "Charts integrated", "Frontend built"]},
        {"week": 4, "title": "Prototype (Christmas)", "dates": "Dec 23-29", "milestones": ["Working site", "Terry shows approval", "Christmas week buffer"]},
        {"week": 5, "title": "Polish (New Year)", "dates": "Dec 30-Jan 5", "milestones": ["Mobile optimization", "Speed tuning", "Bug fixes", "Final tweaks"]},
        {"week": 6, "title": "LAUNCH 🚀", "dates": "Jan 6-12", "milestones": ["Final QA", "Train Liza", "Last payments", "GO LIVE"]}
    ]
    
    for w in weeks_timeline:
        is_current: bool = w["week"] == current_week
        is_complete: bool = w["week"] < current_week
        icon = "🟢" if is_complete else ("🔵" if is_current else "⚪")
        
        with st.expander(f"{icon} Week {w['week']}: {w['title']} ({w['dates']})", expanded=is_current):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("**Milestones:**")
                for m in w["milestones"]:
                    st.markdown(f"✓ {m}")
            
            with col2:
                week_tasks = [t for t in data["tasks"] if t["week"] == w["week"]]
                st.markdown("**Tasks:**")
                for t in week_tasks:
                    icon_task = "✅" if t["status"] == "completed" else "⏳"
                    st.markdown(f"{icon_task} {t['task'][:30]}...")

elif page == "👥 Contacts":
    st.markdown("# 👥 Key Contacts & Communication")
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

elif page == "📝 Communications":
    st.markdown("# 📝 Message Templates")
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

elif page == "⚙️ Settings":
    st.markdown("# ⚙️ Settings & Data")
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
            st.success("✅ Saved!")
        
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
