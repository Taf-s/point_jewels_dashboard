"""
CSS styling utilities for the Point Jewels dashboard.
"""

import streamlit as st


def get_custom_css() -> str:
    """
    Load and return the custom CSS styles for the dashboard.

    Returns:
        str: The complete CSS stylesheet as a string
    """
    try:
        with open("styles/main.css", "r", encoding="utf-8") as f:
            css_content = f.read()
        return f"<style>{css_content}</style>"
    except FileNotFoundError:
        st.warning("Custom CSS file not found. Using default styling.")
        return ""
    except Exception as e:
        st.warning(f"Error loading CSS: {e}. Using default styling.")
        return ""