#!/bin/bash

# Point Jewels Dashboard Launcher
# This script starts the Streamlit dashboard with optimized settings

echo "💎 Starting Point Jewels Dashboard..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Set environment variables for better performance
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export STREAMLIT_SERVER_PORT=8501

# Run the dashboard
streamlit run app.py --server.headless true --server.port 8501 --browser.gatherUsageStats false

echo "✅ Dashboard stopped."