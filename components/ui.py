"""
Reusable UI Components for Point Jewels Dashboard
Modular components for consistent UI patterns.
"""

from utils.config import COLORS
from utils.helpers import html_escape

def render_progress_ring(percentage: float, size: int = 80, color: str = COLORS['gold'], label: str = "") -> str:
    """
    Render a circular progress ring with consistent styling.

    Args:
        percentage: Progress percentage (0-100)
        size: Ring diameter in pixels
        color: Ring color (hex or named color)
        label: Optional label below the ring

    Returns:
        HTML string for the progress ring
    """
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

def render_status_indicator(status: str, size: int = 12) -> str:
    """
    Render a status indicator dot with animation.

    Args:
        status: Status type ('completed', 'pending', 'overdue', 'active')
        size: Indicator size in pixels

    Returns:
        HTML string for the status indicator
    """
    colors = {
        'completed': COLORS['success'],
        'pending': COLORS['warning'],
        'overdue': COLORS['danger'],
        'active': COLORS['info'],
        'warning': COLORS['warning'],
        'success': COLORS['success'],
        'error': COLORS['danger']
    }

    color = colors.get(status, COLORS['text_muted'])

    return f"""
    <div style="
        width: {size}px;
        height: {size}px;
        border-radius: 50%;
        background: {color};
        display: inline-block;
        margin-right: 8px;
        box-shadow: 0 0 8px {color}40;
        animation: pulse 2s infinite;
    "></div>
    """

def render_badge(text: str, variant: str = "info", size: str = "sm") -> str:
    """
    Render a styled badge component.

    Args:
        text: Badge text content
        variant: Color variant ('success', 'warning', 'danger', 'info')
        size: Size variant ('sm', 'md', 'lg')

    Returns:
        HTML string for the badge
    """
    size_styles = {
        'sm': 'padding: 4px 12px; font-size: 11px;',
        'md': 'padding: 6px 16px; font-size: 12px;',
        'lg': 'padding: 8px 20px; font-size: 14px;'
    }

    return f"""
    <span class="badge badge-{variant}" style="{size_styles.get(size, size_styles['md'])}">
        {html_escape(text)}
    </span>
    """

def render_card(title: str = "", content: str = "", variant: str = "default", hover: bool = True) -> str:
    """
    Render a consistent card component.

    Args:
        title: Card title (optional)
        content: Card content HTML
        variant: Card style variant
        hover: Enable hover effects

    Returns:
        HTML string for the card
    """
    card_class = "stat-card"
    if variant == "task":
        card_class = "task-card"
    elif variant == "financial":
        card_class = "financial-card"

    hover_class = "hover" if hover else ""

    title_html = f'<div style="font-size: 18px; color: {COLORS["gold"]}; margin-bottom: 16px;">{html_escape(title)}</div>' if title else ""

    return f"""
    <div class="{card_class} {hover_class}">
        {title_html}
        {content}
    </div>
    """

def render_metric(label: str, value: str, sublabel: str = "", icon: str = "") -> str:
    """
    Render a metric display component.

    Args:
        label: Metric label
        value: Primary value
        sublabel: Secondary label
        icon: Optional icon

    Returns:
        HTML string for the metric
    """
    icon_html = f'<span style="margin-right: 8px;">{icon}</span>' if icon else ""

    return f"""
    <div style="text-align: center;">
        <div class="stat-value">{icon_html}{html_escape(value)}</div>
        <div class="stat-label">{html_escape(label)}</div>
        {f'<div style="font-size: 12px; color: {COLORS["text_muted"]}; margin-top: 4px;">{html_escape(sublabel)}</div>' if sublabel else ''}
    </div>
    """