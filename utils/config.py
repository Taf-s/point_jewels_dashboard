"""
Point Jewels Dashboard - Core Configuration
Centralized configuration for colors, icons, and constants.
"""

# ============================================================================
# COLOR PALETTE (Luxury Jewelry Theme)
# ============================================================================

COLORS = {
    # Primary Colors
    'gold': '#d4af37',           # Rich gold
    'gold_light': '#f4d03f',     # Light gold
    'gold_dark': '#b8962e',      # Dark gold

    # Background Colors
    'dark_bg': '#0f0f0f',        # Very dark background
    'dark_accent': '#1a1a1a',    # Slightly lighter dark
    'darker': '#0a0a0a',         # Even darker

    # Card Colors
    'card_light': '#1f1f1f',     # Light card background
    'card_dark': '#141414',      # Dark card background

    # Text Colors
    'text_primary': '#ffffff',   # Primary text
    'text_secondary': '#e0e0e0', # Secondary text
    'text_muted': '#a0a0a0',     # Muted text
    'text_dark': '#808080',      # Dark text

    # Status Colors
    'success': '#10b981',        # Green
    'warning': '#f59e0b',        # Orange
    'danger': '#ef4444',         # Red
    'info': '#3b82f6',           # Blue
}

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