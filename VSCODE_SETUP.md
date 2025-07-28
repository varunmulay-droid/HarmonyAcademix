# VS Code Setup Guide for Project Harmony Hands

## Prerequisites

1. **Install Python 3.8+** from [python.org](https://python.org)
2. **Install Git** from [git-scm.com](https://git-scm.com)
3. **Install VS Code** from [code.visualstudio.com](https://code.visualstudio.com)

## Step-by-Step Setup

### 1. Download Project Files

**Option A: Download from Replit**
1. In Replit, click the three dots menu → "Download as zip"
2. Extract the zip file to your desired folder
3. Open VS Code and select "File → Open Folder" → choose the extracted folder

**Option B: Clone from GitHub (if you have it there)**
```bash
git clone <your-github-repo-url>
cd harmony-hands-erp
code .
```

### 2. Install VS Code Extensions

Open VS Code and install these extensions:
- **Python** (Microsoft) - Essential for Python development
- **Flask Snippets** - Helpful Flask code snippets
- **Jinja2** - Template syntax highlighting
- **SQLite Viewer** - View database contents
- **GitLens** - Git integration (optional)

### 3. Set Up Python Environment

1. **Open Terminal in VS Code** (View → Terminal or Ctrl+`)

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Flask-Login==0.6.3 Werkzeug==3.0.1 email-validator==2.1.0 psycopg2-binary==2.9.9 gunicorn==21.2.0
   ```

### 4. Configure Environment Variables

1. **Create `.env` file** in the root folder:
   ```
   SESSION_SECRET=your-super-secret-key-here-make-it-long-and-random
   DATABASE_URL=sqlite:///harmony_hands.db
   FLASK_DEBUG=true
   ```

2. **Install python-dotenv** (to load .env files):
   ```bash
   pip install python-dotenv
   ```

### 5. Initialize Database

Run this command in terminal:
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"
```

### 6. Run the Application

```bash
python main.py
```

The application will start at `http://localhost:5000`

### 7. VS Code Configuration

Create `.vscode/settings.json` for better development:
```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python",
    "python.terminal.activateEnvironment": true,
    "files.associations": {
        "*.html": "jinja-html"
    },
    "emmet.includeLanguages": {
        "jinja-html": "html"
    }
}
```

## Default Login Credentials

- **Admin Username:** admin
- **Admin Password:** admin123

## Debugging in VS Code

1. **Create Debug Configuration**
   - Go to Run and Debug (Ctrl+Shift+D)
   - Click "create a launch.json file"
   - Choose "Flask"

2. **Sample launch.json:**
   ```json
   {
       "version": "0.2.0",
       "configurations": [
           {
               "name": "Flask",
               "type": "python",
               "request": "launch",
               "program": "main.py",
               "env": {
                   "FLASK_DEBUG": "true"
               },
               "console": "integratedTerminal"
           }
       ]
   }
   ```

## Common Issues & Solutions

### Issue: "Python not found"
**Solution:** 
1. Ensure Python is installed and in PATH
2. Restart VS Code after Python installation
3. Select correct Python interpreter (Ctrl+Shift+P → "Python: Select Interpreter")

### Issue: "Module not found"
**Solution:**
1. Ensure virtual environment is activated (you should see `(venv)` in terminal)
2. Reinstall packages: `pip install -r requirements.txt`

### Issue: "Permission denied" (Windows)
**Solution:**
1. Run VS Code as Administrator, or
2. Use `python -m pip install` instead of just `pip install`

### Issue: Database errors
**Solution:**
1. Delete `harmony_hands.db` file if it exists
2. Run database initialization command again
3. Check file permissions in project folder

## Next Steps

1. **Test the application** - Register a new student and try submitting forms
2. **Customize** - Modify templates, styles, or add new features
3. **Deploy** - Follow the deployment guide for your chosen platform

## File Structure Overview

```
harmony-hands-erp/
├── app.py              # Flask app configuration
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # URL routes and logic
├── .env                # Environment variables (create this)
├── .env.example        # Environment template
├── static/             # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── uploads/
├── templates/          # HTML templates
│   ├── forms/
│   └── admin/
└── venv/              # Python virtual environment
```

You're now ready to develop with VS Code!