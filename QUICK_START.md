# Quick Start Guide

## 🎯 For VS Code Development

1. **Download project** from Replit (three dots → Download as zip)
2. **Extract** and open in VS Code
3. **Open terminal** in VS Code (Ctrl+`)
4. **Set up environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate    # Windows
   # OR
   source venv/bin/activate # Mac/Linux
   ```
5. **Install dependencies:**
   ```bash
   pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Flask-Login==0.6.3 Werkzeug==3.0.1 email-validator==2.1.0 psycopg2-binary==2.9.9 gunicorn==21.2.0
   ```
6. **Create .env file:**
   ```
   SESSION_SECRET=your-secret-key-here
   DATABASE_URL=sqlite:///harmony_hands.db
   FLASK_DEBUG=true
   ```
7. **Initialize database:**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```
8. **Run the app:**
   ```bash
   python main.py
   ```
9. **Open browser:** http://localhost:5000

**Default Admin Login:** 
- Username: `admin`
- Password: `admin123`

---

## 🚀 For Free Deployment

### Option 1: Render.com (Easiest)
1. **Push to GitHub:** Upload your code to a GitHub repository
2. **Sign up at render.com** with GitHub
3. **Create Web Service** → Connect GitHub repo
4. **Auto-deploy** (Render detects Flask automatically)
5. **Live in 5-10 minutes!**

### Option 2: Railway.app
1. **Push to GitHub**
2. **Sign up at railway.app**
3. **New Project** → Deploy from GitHub
4. **Done!** Railway handles everything

### Option 3: PythonAnywhere
1. **Sign up at pythonanywhere.com**
2. **Upload files** via Files tab
3. **Create web app** (Flask)
4. **Configure WSGI** to point to main.py

**Need detailed instructions?** See `DEPLOYMENT_GUIDE.md`

---

## 📱 Features Overview

- ✅ **Student Registration** with auto STU ID (STU001-STU300)
- ✅ **Admin Dashboard** for management
- ✅ **5 Integrated Forms:**
  - Admission Form
  - Bonafide Certificate  
  - Hostel Registration
  - Case Record Form
  - Pratinidhan Pramaan Patra
- ✅ **File Uploads** (photos, documents)
- ✅ **Bilingual Support** (English/Marathi)
- ✅ **Database Flexibility** (SQLite/PostgreSQL)

**Ready to go!** 🎉