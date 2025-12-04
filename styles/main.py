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
        # Execute the CSS template with COLORS variables
        css_template = f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap');

            /* ===== BASE STYLING ===== */
            .stApp {{
                background: linear-gradient(135deg, {COLORS['dark_bg']} 0%, {COLORS['dark_accent']} 50%, {COLORS['darker']} 100%);
                font-family: 'Inter', sans-serif;
                min-height: 100vh;
            }}

            /* ===== TYPOGRAPHY ===== */
            h1, h2, h3 {{
                font-family: 'Playfair Display', serif !important;
                color: {COLORS['gold']} !important;
                font-weight: 600 !important;
                margin-bottom: 1rem !important;
            }}

            p, li, span, div {{
                font-family: 'Inter', sans-serif;
            }}

            /* ===== METRICS STYLING ===== */
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

            /* ===== SIDEBAR STYLING ===== */
            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, {COLORS['dark_bg']} 0%, {COLORS['darker']} 100%);
                border-right: 2px solid rgba(212, 175, 55, 0.2);
                box-shadow: 2px 0 20px rgba(0,0,0,0.3);
            }}

            /* ===== BUTTON STYLING ===== */
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

            /* ===== PROGRESS BARS ===== */
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

            /* ===== CARDS AND COMPONENTS ===== */
            .stat-card {{
                background: linear-gradient(145deg, {COLORS['card_light']} 0%, {COLORS['dark_bg']} 100%);
                border: 1px solid rgba(212, 175, 55, 0.2);
                border-radius: 16px;
                padding: 20px;
                margin: 8px 0;
                box-shadow: 0 4px 16px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }}

            .stat-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 24px rgba(212, 175, 55, 0.15);
            }}

            .stat-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: linear-gradient(90deg, {COLORS['gold']} 0%, transparent 100%);
            }}

            .stat-value {{
                font-size: 24px;
                font-weight: 700;
                color: {COLORS['gold']};
                font-family: 'Playfair Display', serif;
                margin-bottom: 4px;
            }}

            .stat-label {{
                font-size: 12px;
                color: {COLORS['text_muted']};
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}

            /* ===== GRID LAYOUTS ===== */
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 16px;
                margin: 20px 0;
            }}

            .task-grid {{
                display: grid;
                grid-template-columns: 1fr;
                gap: 12px;
                margin: 16px 0;
            }}

            /* ===== ANIMATIONS ===== */
            .fade-in {{
                animation: fadeIn 0.6s ease-in-out;
            }}

            @keyframes fadeIn {{
                from {{
                    opacity: 0;
                    transform: translateY(20px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}

            /* ===== RESPONSIVE DESIGN ===== */
            @media (max-width: 768px) {{
                .stats-grid {{
                    grid-template-columns: 1fr;
                }}

                .stat-card {{
                    padding: 16px;
                }}

                [data-testid="metric-container"] {{
                    padding: 16px;
                }}
            }}

            /* ===== UTILITY CLASSES ===== */
            .text-center {{
                text-align: center;
            }}

            .mb-4 {{
                margin-bottom: 16px;
            }}

            .mt-4 {{
                margin-top: 16px;
            }}
        </style>
        """
        return css_template
    except Exception as e:
        st.warning(f"Error loading CSS: {e}. Using default styling.")
        return ""