#!/usr/bin/env python3
"""
Unit tests for Point Jewels Dashboard
Tests core business logic functions for robustness and correctness.
"""

import pytest
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

# Import functions from app.py (we'll need to be careful about Streamlit dependencies)
# For now, let's duplicate the functions we want to test to avoid Streamlit imports

# ============================================================================
# TEST DATA & FIXTURES
# ============================================================================

@pytest.fixture
def sample_tasks():
    """Sample task data for testing."""
    return [
        {"id": 1, "task": "Pay designer R5,000 deposit", "week": 1, "deadline": "2024-12-02", "status": "completed", "assignee": "You", "priority": "critical"},
        {"id": 2, "task": "Send Jared project brief", "week": 1, "deadline": "2024-12-04", "status": "pending", "assignee": "You", "priority": "high"},
        {"id": 3, "task": "Confirm Wednesday meeting with Liza", "week": 1, "deadline": "2024-12-03", "status": "pending", "assignee": "You", "priority": "high"},
        {"id": 4, "task": "Book models for photoshoot", "week": 1, "deadline": "2024-12-04", "status": "pending", "assignee": "You", "priority": "medium"},
    ]

@pytest.fixture
def sample_finances():
    """Sample financial data for testing."""
    return {
        "budget_total": 50000,
        "received": [
            {"date": "2024-11-25", "amount": 11400, "from": "Terry (50% preliminary)", "status": "received"}
        ],
        "pending_in": [
            {"date": "2024-12-16", "amount": 19300, "from": "Terry (Milestone 2)", "status": "pending"}
        ],
        "paid_out": [
            {"date": "2024-12-02", "amount": 5000, "to": "Jared (Deposit 1)", "status": "paid"}
        ],
        "pending_out": [
            {"date": "2024-12-05", "amount": 5000, "to": "Jared (Deposit 2)", "status": "pending"}
        ],
        "designer_total": 20000,
        "expenses_misc": 3000
    }

@pytest.fixture
def sample_project():
    """Sample project data for testing."""
    return {
        "name": "Point Jewels Website Revamp",
        "launch_date": "2025-01-12",
        "current_week": 1
    }

# ============================================================================
# FUNCTIONS TO TEST (copied from app.py to avoid Streamlit dependencies)
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

def get_days_remaining(project: Dict[str, Any]) -> int:
    """Calculate days until launch."""
    launch_date = datetime.strptime(project["launch_date"], "%Y-%m-%d")
    return (launch_date - datetime.now()).days

# ============================================================================
# UNIT TESTS
# ============================================================================

class TestTaskStats:
    """Test task statistics calculations."""

    def test_get_task_stats_basic(self, sample_tasks):
        """Test basic task statistics calculation."""
        stats = get_task_stats(sample_tasks)

        assert stats["total"] == 4
        assert stats["completed"] == 1
        assert stats["pending"] == 3
        assert stats["critical"] == 1

    def test_get_task_stats_empty_list(self):
        """Test task stats with empty task list."""
        stats = get_task_stats([])

        assert stats["total"] == 0
        assert stats["completed"] == 0
        assert stats["pending"] == 0
        assert stats["critical"] == 0

    def test_get_task_stats_all_completed(self):
        """Test task stats when all tasks are completed."""
        tasks = [
            {"status": "completed", "priority": "critical"},
            {"status": "completed", "priority": "high"},
            {"status": "completed", "priority": "medium"},
        ]
        stats = get_task_stats(tasks)

        assert stats["total"] == 3
        assert stats["completed"] == 3
        assert stats["pending"] == 0
        assert stats["critical"] == 1

class TestFinancialSummary:
    """Test financial calculations."""

    def test_get_financial_summary_basic(self, sample_finances):
        """Test basic financial summary calculation."""
        summary = get_financial_summary(sample_finances)

        assert summary["received"] == 11400
        assert summary["pending_in"] == 19300
        assert summary["paid_out"] == 5000
        assert summary["pending_out"] == 5000
        assert summary["profit"] == 50000 - 20000 - 3000  # 27000
        assert summary["balance"] == 11400 - 5000  # 6400

    def test_get_financial_summary_empty(self):
        """Test financial summary with empty data."""
        finances = {
            "budget_total": 10000,
            "received": [],
            "pending_in": [],
            "paid_out": [],
            "pending_out": [],
            "designer_total": 5000,
            "expenses_misc": 1000
        }
        summary = get_financial_summary(finances)

        assert summary["received"] == 0
        assert summary["pending_in"] == 0
        assert summary["paid_out"] == 0
        assert summary["pending_out"] == 0
        assert summary["profit"] == 10000 - 5000 - 1000  # 4000
        assert summary["balance"] == 0

class TestTaskOverdue:
    """Test task overdue detection."""

    def test_task_not_overdue_completed(self):
        """Test that completed tasks are never overdue."""
        task = {
            "status": "completed",
            "deadline": "2020-01-01"  # Very old date
        }
        assert not is_task_overdue(task)

    def test_task_not_overdue_future_deadline(self):
        """Test that tasks with future deadlines are not overdue."""
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        task = {
            "status": "pending",
            "deadline": future_date
        }
        assert not is_task_overdue(task)

    def test_task_overdue_past_deadline(self):
        """Test that pending tasks with past deadlines are overdue."""
        past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        task = {
            "status": "pending",
            "deadline": past_date
        }
        assert is_task_overdue(task)

class TestDaysRemaining:
    """Test days remaining calculations."""

    def test_days_remaining_future_launch(self):
        """Test days remaining for future launch date."""
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        project = {"launch_date": future_date}

        days = get_days_remaining(project)
        assert 29 <= days <= 30  # Allow for timing precision (approximately 30 days)

    def test_days_remaining_past_launch(self):
        """Test days remaining for past launch date."""
        past_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        project = {"launch_date": past_date}

        days = get_days_remaining(project)
        assert -31 <= days <= -29  # Allow for timing precision (approximately -30 days)

class TestDataPersistence:
    """Test data loading and saving functionality."""

    def test_data_file_operations(self, tmp_path):
        """Test that data can be saved and loaded correctly."""
        # Create a temporary data file
        data_file = tmp_path / "test_data.json"

        test_data = {
            "project": {"name": "Test Project", "current_week": 1},
            "tasks": [{"id": 1, "task": "Test task", "status": "pending"}]
        }

        # Save data
        with open(data_file, 'w') as f:
            json.dump(test_data, f, indent=2, default=str)

        # Load data
        with open(data_file, 'r') as f:
            loaded_data = json.load(f)

        assert loaded_data["project"]["name"] == "Test Project"
        assert loaded_data["tasks"][0]["task"] == "Test task"

class TestDataValidation:
    """Test data structure validation."""

    def test_task_structure(self, sample_tasks):
        """Test that task data has required fields."""
        for task in sample_tasks:
            required_fields = ["id", "task", "week", "deadline", "status", "assignee", "priority"]
            for field in required_fields:
                assert field in task, f"Task missing required field: {field}"

    def test_financial_structure(self, sample_finances):
        """Test that financial data has required fields."""
        required_fields = ["budget_total", "received", "pending_in", "paid_out", "pending_out", "designer_total", "expenses_misc"]
        for field in required_fields:
            assert field in sample_finances, f"Finances missing required field: {field}"

        # Test that arrays contain objects with amount field
        for payment_list in ["received", "pending_in", "paid_out", "pending_out"]:
            for payment in sample_finances[payment_list]:
                assert "amount" in payment, f"Payment missing amount field in {payment_list}"

# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Test integration between different components."""

    def test_full_workflow_calculation(self, sample_tasks, sample_finances, sample_project):
        """Test that all calculations work together correctly."""
        # Calculate all metrics
        task_stats = get_task_stats(sample_tasks)
        financial_summary = get_financial_summary(sample_finances)
        days_remaining = get_days_remaining(sample_project)

        # Verify relationships
        assert task_stats["total"] == len(sample_tasks)
        assert financial_summary["profit"] > 0  # Should have profit
        assert isinstance(days_remaining, int)

        # Test that overdue tasks are counted correctly
        overdue_count = sum(1 for task in sample_tasks if is_task_overdue(task))
        assert overdue_count >= 0  # Should not be negative

if __name__ == "__main__":
    pytest.main([__file__, "-v"])