"""
CSS styling utilities for the Point Jewels dashboard.
"""

import streamlit as st
from utils.config import COLORS


def get_custom_css() -> str:
    """
    Load and return the custom CSS styles for the dashboard.

    Returns:
        str: The complete CSS stylesheet as a string
    """
    try:
        # Simple test CSS
        css_template = """
        <style>
            body {
                background-color: #0f0f0f;
                color: #d4af37;
            }
            .stat-card {
                background-color: #1f1f1f;
                border: 1px solid #d4af37;
                border-radius: 16px;
                padding: 20px;
                margin: 8px 0;
            }
            .stat-value {
                font-size: 24px;
                font-weight: 700;
                color: #d4af37;
                margin-bottom: 4px;
            }
            .stat-label {
                font-size: 12px;
                color: #a0a0a0;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .fade-in {
                animation: fadeIn 0.6s ease-in-out;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
        """
        return css_template
    except Exception as e:
        st.warning(f"Error loading CSS: {e}. Using default styling.")
        return ""
