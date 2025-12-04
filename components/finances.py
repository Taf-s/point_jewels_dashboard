"""
Financial components for Point Jewels Dashboard
Specialized components for financial data visualization and editing.
"""

from typing import Dict, Any, List
import streamlit as st
from utils.config import COLORS
from utils.helpers import html_escape, format_currency, get_financial_summary
from components.ui import render_progress_ring, render_card

def render_payment_card(payment: Dict[str, Any], direction: str = "in") -> None:
    """
    Render payment card (money in/out).

    Args:
        payment: Payment data dictionary
        direction: "in" for money received, "out" for money paid
    """
    status = payment["status"]
    is_pending = status == "pending"
    status_icon = "💎" if not is_pending else "⏳"  # Diamond for completed, hourglass for pending
    color = COLORS['success'] if not is_pending else COLORS['warning']
    label = payment.get("from") or payment.get("to", "Unknown")
    label_safe = html_escape(label)
    date_label = "Expected" if is_pending and direction == "in" else "Due" if is_pending else "Date"

    card_class = "task-complete" if not is_pending else "task-pending"

    st.markdown(f"""
    <div class="task-card {card_class}" style="border-left: 4px solid {color};">
        <strong style="color: {color}; font-size: 16px;">{status_icon} {format_currency(payment['amount'])}</strong>
        <br><small style="color: {COLORS['text_dark']}; font-size: 13px;">
            {label_safe} | {date_label}: {html_escape(payment['date'])}
        </small>
    </div>
    """, unsafe_allow_html=True)

def editable_metric(label: str, value: float, key: str, prefix: str = "R", suffix: str = "", help_text: str = "") -> float:
    """
    Create an editable metric with click-to-edit functionality.

    Args:
        label: Display label for the metric
        value: Current value
        key: Unique key for session state
        prefix: Prefix for display (e.g., "R")
        suffix: Suffix for display
        help_text: Help text for the metric

    Returns:
        New value if edited, None otherwise
    """
    edit_key = f"edit_{key}"

    # Initialize session state if needed
    if edit_key not in st.session_state:
        st.session_state[edit_key] = False

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

            with st.form(key=f"form_{key}"):
                col_a, col_b, col_c = st.columns([2, 1, 1])

                with col_a:
                    new_value = st.number_input(
                        f"New {label}",
                        value=float(value),
                        min_value=0.0,
                        max_value=10000000.0,  # Max 10M to prevent unreasonable values
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

def render_financial_overview(finances: Dict[str, Any]) -> None:
    """
    Render the financial overview section with cards.

    Args:
        finances: Financial data dictionary
    """
    summary = get_financial_summary(finances)

    # Financial Summary Cards
    st.markdown("## 💰 Financial Summary")

    # Editable budget metrics in organized cards
    st.markdown('<div class="financial-grid">', unsafe_allow_html=True)

    # Budget Total Card
    budget_total = finances.get('budget_total', 50000)
    new_budget = editable_metric("Total Budget", budget_total, "budget_total", "R")
    if new_budget is not None:
        finances['budget_total'] = new_budget

    st.markdown(f'''
    <div class="financial-card">
        <div style="font-size: 24px; color: {COLORS['gold']}; margin-bottom: 8px;">💼</div>
        <div style="font-size: 28px; font-weight: 700; color: {COLORS['gold']}; margin-bottom: 4px;">{format_currency(budget_total)}</div>
        <div style="font-size: 14px; color: {COLORS['text_muted']}; font-weight: 500;">TOTAL BUDGET</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 8px;">Click to edit</div>
    </div>
    ''', unsafe_allow_html=True)

    # Income Card
    st.markdown(f'''
    <div class="financial-card income">
        <div style="font-size: 24px; color: {COLORS['success']}; margin-bottom: 8px;">📈</div>
        <div style="font-size: 28px; font-weight: 700; color: {COLORS['success']}; margin-bottom: 4px;">{format_currency(summary['received'])}</div>
        <div style="font-size: 14px; color: {COLORS['text_muted']}; font-weight: 500;">TOTAL RECEIVED</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 8px;">+{format_currency(summary['pending_in'])} pending</div>
    </div>
    ''', unsafe_allow_html=True)

    # Expenses Card
    st.markdown(f'''
    <div class="financial-card expense">
        <div style="font-size: 24px; color: {COLORS['danger']}; margin-bottom: 8px;">📉</div>
        <div style="font-size: 28px; font-weight: 700; color: {COLORS['danger']}; margin-bottom: 4px;">{format_currency(summary['paid_out'])}</div>
        <div style="font-size: 14px; color: {COLORS['text_muted']}; font-weight: 500;">TOTAL PAID</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 8px;">+{format_currency(summary['pending_out'])} pending</div>
    </div>
    ''', unsafe_allow_html=True)

    # Profit Card
    profit_color = COLORS['success'] if summary['profit'] > 0 else COLORS['danger']
    st.markdown(f'''
    <div class="financial-card">
        <div style="font-size: 24px; color: {profit_color}; margin-bottom: 8px;">💰</div>
        <div style="font-size: 28px; font-weight: 700; color: {profit_color}; margin-bottom: 4px;">{format_currency(summary['profit'])}</div>
        <div style="font-size: 14px; color: {COLORS['text_muted']}; font-weight: 500;">PROJECT PROFIT</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 8px;">Balance: {format_currency(summary['balance'])}</div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Close financial-grid

def render_budget_breakdown(finances: Dict[str, Any]) -> None:
    """
    Render budget breakdown visualization.

    Args:
        finances: Financial data dictionary
    """
    import plotly.graph_objects as go

    summary = get_financial_summary(finances)

    # Budget breakdown chart
    st.markdown("### 📊 Budget Breakdown")
    fig = go.Figure(data=[go.Pie(
        labels=['Designer (Jared)', 'Misc Expenses', 'Your Profit'],
        values=[
            finances.get('designer_total', 20000),
            finances.get('expenses_misc', 3000),
            max(0, summary['profit'])  # Ensure non-negative for display
        ],
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