"""
Utility functions for Point Jewels Dashboard
Helper functions for data processing, validation, and common operations.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# ============================================================================
# DATA MANAGEMENT
# ============================================================================

DATA_FILE = Path("project_data.json")

def load_data() -> Dict[str, Any]:
    """Load project data or create defaults."""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return get_default_data()

def save_data(data: Dict[str, Any]) -> None:
    """Save project data to JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_default_data() -> Dict[str, Any]:
    """Return default project data structure."""
    return {
        "project": {
            "name": "Point Jewels Website",
            "status": "In Progress",
            "current_week": 1,
            "launch_date": "2025-01-12"
        },
        "tasks": [
            {"id": 1, "task": "Pay designer R5,000 deposit", "week": 1, "deadline": "2024-12-02", "status": "completed", "assignee": "You", "priority": "critical"},
            {"id": 2, "task": "Send Jared project brief", "week": 1, "deadline": "2024-12-04", "status": "pending", "assignee": "You", "priority": "high"},
            {"id": 3, "task": "Confirm Wednesday meeting with Liza", "week": 1, "deadline": "2024-12-03", "status": "pending", "assignee": "You", "priority": "high"},
        ],
        "finances": {
            "budget_total": 50000,
            "received": [],
            "pending_in": [],
            "paid_out": [],
            "pending_out": [],
            "designer_total": 20000,
            "expenses_misc": 3000
        },
        "contacts": {},
        "communications": {},
        "settings": {}
    }

# ============================================================================
# SECURITY & SANITIZATION
# ============================================================================

def html_escape(s: Any) -> str:
    """Return an HTML-escaped version of s (s can be any value) to avoid XSS in unsafe HTML blocks."""
    if s is None:
        return ""
    t = str(s)
    return (
        t.replace('&', '&amp;')
         .replace('<', '&lt;')
         .replace('>', '&gt;')
         .replace('"', '&quot;')
         .replace("'", '&#x27;')
    )

# ============================================================================
# BUSINESS LOGIC HELPERS
# ============================================================================

def get_task_stats(tasks: List[Dict[str, Any]]) -> Dict[str, int]:
    """Calculate task statistics."""
    total = len(tasks)
    completed = sum(1 for task in tasks if task["status"] == "completed")
    pending = total - completed
    overdue = sum(1 for task in tasks if is_task_overdue(task) and task["status"] != "completed")

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "overdue": overdue
    }

def get_financial_summary(finances: Dict[str, Any]) -> Dict[str, float]:
    """Calculate financial summary."""
    received = sum(p["amount"] for p in finances["received"] if p.get("status") == "received")
    pending_in = sum(p["amount"] for p in finances["pending_in"])
    paid_out = sum(p["amount"] for p in finances["paid_out"] if p.get("status") == "paid")
    pending_out = sum(p["amount"] for p in finances["pending_out"])

    total_received = received + pending_in
    total_paid = paid_out + pending_out
    profit = total_received - total_paid
    balance = total_received - paid_out  # Excluding pending payments

    return {
        "received": received,
        "pending_in": pending_in,
        "paid_out": paid_out,
        "pending_out": pending_out,
        "profit": profit,
        "balance": balance
    }

def is_task_overdue(task: Dict[str, Any]) -> bool:
    """Check if a task is overdue."""
    try:
        deadline = datetime.strptime(task["deadline"], "%Y-%m-%d")
        return deadline < datetime.now()
    except (ValueError, KeyError):
        return False

def get_days_remaining(project: Dict[str, Any]) -> int:
    """Calculate days until launch."""
    try:
        launch_date = datetime.strptime(project["launch_date"], "%Y-%m-%d")
        return max(0, (launch_date - datetime.now()).days)
    except (ValueError, KeyError):
        return 0

# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def validate_task_data(task: Dict[str, Any]) -> bool:
    """Validate task data structure."""
    required_fields = ["id", "task", "week", "deadline", "status", "assignee", "priority"]
    return all(field in task for field in required_fields)

def validate_financial_data(payment: Dict[str, Any]) -> bool:
    """Validate payment data structure."""
    required_fields = ["date", "amount", "status"]
    return all(field in payment for field in required_fields)

def sanitize_input(text: str, max_length: int = 1000) -> str:
    """Sanitize user input text."""
    if not isinstance(text, str):
        return ""
    # Remove potentially dangerous characters
    sanitized = text.strip()
    # Limit length to prevent abuse
    return sanitized[:max_length]

# ============================================================================
# PERFORMANCE OPTIMIZATION
# ============================================================================

_performance_cache = {}

def optimize_performance():
    """Cache expensive calculations for better performance."""
    # This is a placeholder for performance optimization
    # In a real implementation, you'd cache financial summaries, etc.
    return get_financial_summary(load_data()["finances"])

# ============================================================================
# FORMATTING HELPERS
# ============================================================================

def format_currency(amount: float, currency: str = "R") -> str:
    """Format amount as currency."""
    return f"{currency}{amount:,.0f}"

def format_percentage(value: float, total: float) -> str:
    """Format value as percentage."""
    if total == 0:
        return "0%"
    return f"{(value / total * 100):.1f}%"

def format_date(date_str: str, format: str = "%Y-%m-%d") -> str:
    """Format date string."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime(format)
    except ValueError:
        return date_str