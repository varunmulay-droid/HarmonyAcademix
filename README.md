# Project Harmony Hands - Student ERP System

A comprehensive Student ERP Management System built with Flask for managing 100-300 students with automated STU ID generation and integrated forms.

## Features

- **Student Management**: Automated STU ID generation (STU001-STU300)
- **Admin Dashboard**: Complete system oversight and management
- **5 Integrated Forms**:
  - Admission Form
  - Bonafide Certificate
  - Hostel Registration
  - Case Record Form
  - Pratinidhan Pramaan Patra
- **File Upload Support**: Secure document handling
- **Bilingual Support**: English and Marathi language support
- **Database Flexibility**: SQLite (default) or PostgreSQL/Supabase

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Git

### Local Development Setup (VS Code)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd harmony-hands-erp
   ```

2. **Set up Python virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   SESSION_SECRET=your-secret-key-here
   DATABASE_URL=sqlite:///harmony_hands.db
   ```

5. **Initialize the database**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

6. **Run the application**
   ```bash
   python main.py
   ```

7. **Access the application**
   Open your browser and go to `http://localhost:5000`

### Default Admin Access

- **Username**: admin
- **Password**: admin123

## Deployment Options

### Option 1: Render (Recommended - Free)

1. **Create a `requirements.txt` file** (already included)
2. **Create a `render.yaml` file** (already included)
3. **Push to GitHub**
4. **Connect to Render**:
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Create new Web Service
   - Connect your GitHub repository
   - Render will automatically deploy

### Option 2: Railway (Free Tier)

1. **Push to GitHub**
2. **Deploy to Railway**:
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect Flask and deploy

### Option 3: PythonAnywhere (Free Tier)

1. **Create account at [pythonanywhere.com](https://pythonanywhere.com)**
2. **Upload your code** via Files tab
3. **Create web app**:
   - Go to Web tab
   - Create new web app
   - Choose Flask
   - Set source code path
   - Set WSGI file to point to your `main.py`

### Option 4: Heroku (With Credit Card)

1. **Install Heroku CLI**
2. **Create `Procfile`** (already included)
3. **Deploy**:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

## Database Configuration

### Using SQLite (Default)
No additional setup required. Database file will be created automatically.

### Using Supabase (PostgreSQL)

1. **Create Supabase project**:
   - Go to [supabase.com](https://supabase.com)
   - Create new project
   - Get connection string from Settings → Database

2. **Set environment variable**:
   ```
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SESSION_SECRET` | Secret key for session security | Yes |
| `DATABASE_URL` | Database connection string | No (defaults to SQLite) |

## Project Structure

```
harmony-hands-erp/
├── app.py              # Flask application setup
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # Application routes
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment config
├── Procfile           # Heroku deployment config
├── static/            # CSS, JS, images
├── templates/         # HTML templates
└── uploads/           # User uploaded files
```

## VS Code Extensions (Recommended)

- Python
- Flask Snippets
- Jinja2
- SQLite Viewer
- GitLens

## Development Tips

1. **Hot Reload**: The app runs in debug mode for development
2. **Database Inspection**: Use SQLite Viewer extension to inspect the database
3. **Environment Management**: Use Python virtual environment
4. **Git Integration**: Use GitLens for better version control

## Troubleshooting

### Common Issues

1. **Module not found errors**:
   - Ensure virtual environment is activated
   - Install requirements: `pip install -r requirements.txt`

2. **Database connection errors**:
   - Check DATABASE_URL format
   - Ensure database permissions
   - Try SQLite fallback by removing DATABASE_URL

3. **Port already in use**:
   - Change port in main.py or kill existing process

### Getting Help

- Check application logs for detailed error messages
- Ensure all dependencies are installed
- Verify environment variables are set correctly

## License

This project is open source and available under the MIT License.