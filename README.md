# 💎 Point Jewels Project Manager Dashboard

A beautiful Streamlit-powered project management dashboard for your website development project.

## Features

- 🏠 **Dashboard** - Strategic overview with this week's priorities & one-click actions
- ✅ **Tasks** - Smart filtering by week/status/priority with inline editing
- 💰 **Finances** - Real-time cash flow tracking with budget allocation pie chart
- 📅 **Timeline** - 6-week roadmap with milestones & task tracking per week
- 👥 **Contacts** - Strategic communication notes for each stakeholder
- 📝 **Communications** - Ready-to-send message templates (daughters, Jared, Liza)
- ⚙️ **Settings** - Week control, data management, JSON export

## Principles Applied

### Never Split the Difference

- **Tactical Empathy**: Templates & one-click actions reduce friction for your stakeholders
- **Clear Value**: Each page shows what matters to different people (Terry sees money, Liza sees peace, Daughters see progress)
- **Anchoring**: Single source of truth (project_data.json) prevents miscommunication

### Pragmatic Programming

- **DRY (Don't Repeat Yourself)**: Reusable components (`render_task_card`, `render_payment_card`)
- **Simple & Direct**: Minimal UI, maximum clarity—no unnecessary clicks
- **Type hints**: Better code maintainability with Python typing
- **Single responsibility**: Each function does one thing well

## Quick Start

### Option 1: Local Installation

```bash
# 1. Navigate to the dashboard folder
cd point_jewels_dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Option 2: Using Replit

1. Go to [replit.com](https://replit.com)
2. Create new Python Repl
3. Upload `app.py` and `requirements.txt`
4. Click Run

### Option 3: Deploy to Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Deploy!

## Code Architecture

**Clean, maintainable structure:**

- **Configuration** - Colors, fonts, page setup in one place
- **Data Management** - Single `load_data()`/`save_data()` system
- **Utility Functions** - Reusable rendering & calculation functions
- **Page Logic** - Each page is self-contained and clear

## Stakeholder-Focused Design

| Who                       | Sees                          | Key Actions                            |
| ------------------------- | ----------------------------- | -------------------------------------- |
| **Terry** (Money)         | Budget progress, deliverables | Mockups in Week 2, Prototype in Week 4 |
| **Liza** (Operations)     | Unstressed updates            | Meeting invites, progress summaries    |
| **Daughters** (Champions) | Weekly wins + next steps      | Friday automation templates            |
| **Jared** (Designer)      | Structured check-ins          | Monday call scripts, payment tracking  |
| **You** (Manager)         | Everything                    | Dashboard control center               |

## File Structure

```
point_jewels_dashboard/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── project_data.json   # Auto-generated project data (created on first run)
└── README.md          # This file
```

## Customization

### Update Current Week

Go to ⚙️ Settings → Change "Current Week" number

### Add New Tasks

Go to ✅ Tasks → Expand "Add New Task" → Fill in details

### Export Data

Go to ⚙️ Settings → Click "Export Data (JSON)"

## Design

The dashboard uses a luxury jewelry aesthetic:

- Dark theme with gold (#d4af37) accents
- Playfair Display for headers
- Source Sans Pro for body text
- Gradient backgrounds and subtle animations

## Tips

- **Fridays**: Use the "Generate Daughters Update" button on Dashboard
- **Mondays**: Check the Designer Check-in template in Communications
- **Daily**: Mark tasks complete as you go - progress auto-saves

---

Built with ❤️ for the Point Jewels project
