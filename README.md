# 💎 Point Jewels Dashboard

A comprehensive project management dashboard for the Point Jewels jewelry business, built with Streamlit and featuring Phase 3 enhancements including mobile optimization, smart suggestions, and advanced accessibility.

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Virtual environment

### Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Dashboard

```bash
# Using the provided script (recommended - no warnings)
./run_dashboard.sh

# Or manually
source .venv/bin/activate
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`

## ✨ Features

### Phase 3 Enhancements

- 📱 **Mobile Optimization**: Responsive design with touch-friendly controls
- 🧠 **Smart Suggestions**: AI-powered task suggestions based on project context
- ♿ **Accessibility**: Full ARIA support, keyboard navigation, screen reader compatibility
- ⚡ **Performance Caching**: Optimized data loading and rendering
- 🔔 **Advanced Notifications**: Intelligent alerts for deadlines and milestones

### Core Functionality

- 📊 **Project Dashboard**: Real-time progress tracking with visual indicators
- ✅ **Task Management**: Drag-and-drop task organization with priority levels
- 💰 **Financial Overview**: Click-to-edit budgets with automatic calculations
- 📈 **Timeline Tracking**: 6-week project timeline with milestone management
- 👥 **Contact Management**: Client and stakeholder communication tracking
- 💬 **Communications**: Message templates and update automation

## 🛠️ Development

### Never Split the Difference

- **Tactical Empathy**: Templates & one-click actions reduce friction for your stakeholders
- **Clear Value**: Each page shows what matters to different people (Terry sees money, Liza sees peace, Daughters see progress)
- **Anchoring**: Single source of truth (project_data.json) prevents miscommunication

### Pragmatic Programming

- **DRY (Don't Repeat Yourself)**: Reusable components (`render_task_card`, `render_payment_card`)
- **Simple & Direct**: Minimal UI, maximum clarity—no unnecessary clicks
- **Type hints**: Better code maintainability with Python typing
- **Single responsibility**: Each function does one thing well
- **Test-Driven**: Comprehensive unit tests ensure reliability

## 🛠️ Development

### Code Quality

- Linting with Ruff (auto-fixable issues resolved)
- Unit tests with pytest (14 test cases passing)
- HTML escaping for security
- Type hints throughout

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run linting
ruff check .
```

**Test Coverage:**

- ✅ Task statistics calculations
- ✅ Financial summary computations
- ✅ Task overdue detection
- ✅ Days remaining calculations
- ✅ Data persistence (JSON load/save)
- ✅ Data structure validation
- ✅ Integration tests

## 🔒 Security

- HTML injection prevention with `html_escape` on all user content
- Input validation on financial forms (0-10M range limits)
- Secure data persistence with JSON
- No external API dependencies
- XSS protection on task cards, payment cards, and notifications

## Quick Start

### Option 1: Local Development

```bash
# 1. Navigate to the dashboard folder
cd point_jewels_dashboard

# 2. Install production dependencies
pip install -r requirements.txt

# 3. (Optional) Install development dependencies for testing
pip install -r requirements-dev.txt

# 4. Run the dashboard
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Option 2: Streamlit Cloud Deployment

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy using `app.py` as the main file
5. The `requirements.txt` file contains only production dependencies

**Note:** `requirements-dev.txt` contains testing tools and is not needed for deployment.

### Option 3: Using Replit

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

## 📁 Project Structure

```
point_jewels_dashboard/
├── app.py                 # Main application with Phase 3 features
├── test_dashboard.py      # Unit tests (14 test cases)
├── project_data.json      # Data persistence
├── requirements.txt       # Python dependencies
├── requirements-dev.txt   # Development dependencies
├── run_dashboard.sh       # Launch script (no warnings)
├── pytest.ini            # Test configuration
└── README.md             # This documentation
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
