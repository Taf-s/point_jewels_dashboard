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
        </style>
        """
        return css_template
    except Exception as e:
        st.warning(f"Error loading CSS: {e}. Using default styling.")
        return ""
