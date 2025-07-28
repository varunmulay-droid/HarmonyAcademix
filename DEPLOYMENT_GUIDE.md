# Free Deployment Guide for Project Harmony Hands

## 🚀 Best Free Hosting Options (Ranked)

### 1. Render.com (Recommended) ⭐
**Pros:** Easy setup, automatic deploys, 750 hours/month free, PostgreSQL database included
**Cons:** Cold starts after inactivity

### 2. Railway.app 
**Pros:** Simple GitHub integration, generous free tier, great for beginners
**Cons:** Limited monthly usage

### 3. PythonAnywhere
**Pros:** Always-on free tier, no cold starts, beginner-friendly
**Cons:** Limited features on free tier

### 4. Fly.io
**Pros:** Modern platform, good performance
**Cons:** Requires credit card for verification

---

## 📋 Pre-Deployment Checklist

✅ Python code tested locally  
✅ Environment variables configured  
✅ Database working  
✅ Static files loading correctly  
✅ All forms functional  

---

## 🎯 Method 1: Render.com (Easiest)

### Step 1: Prepare Your Code
Your project already includes `render.yaml` configuration file.

### Step 2: Push to GitHub
1. Create new repository on [github.com](https://github.com)
2. Upload your project files:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git branch -M main
   git push -u origin main
   ```

### Step 3: Deploy on Render
1. Go to [render.com](https://render.com) and sign up with GitHub
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Render will auto-detect settings from `render.yaml`
5. Click "Deploy Web Service"
6. Wait 5-10 minutes for deployment

### Step 4: Set Environment Variables (if needed)
- Go to your service dashboard
- Click "Environment" tab
- Add any additional environment variables

**Your app will be live at:** `https://your-app-name.onrender.com`

---

## 🚂 Method 2: Railway.app

### Step 1: Push to GitHub (same as above)

### Step 2: Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Flask and deploys

**Your app will be live at:** `https://your-app-name.railway.app`

---

## 🐍 Method 3: PythonAnywhere

### Step 1: Create Account
1. Sign up at [pythonanywhere.com](https://pythonanywhere.com)
2. Choose the free "Beginner" account

### Step 2: Upload Code
1. Use the "Files" tab to upload your project
2. Or clone from GitHub using the console

### Step 3: Create Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Flask"
4. Set source code directory to your project folder
5. Edit the WSGI configuration file to point to your `main.py`

### Step 4: Install Dependencies
In the console:
```bash
pip3.10 install --user Flask Flask-SQLAlchemy Flask-Login Werkzeug email-validator psycopg2-binary gunicorn
```

**Your app will be live at:** `https://yourusername.pythonanywhere.com`

---

## ✈️ Method 4: Fly.io

### Step 1: Install Fly CLI
Download from [fly.io/docs/flyctl/installing/](https://fly.io/docs/flyctl/installing/)

### Step 2: Create Fly App
```bash
fly auth login
fly launch
```

### Step 3: Deploy
```bash
fly deploy
```

---

## 🗄️ Database Options

### SQLite (Default - Works Everywhere)
- Already configured
- No additional setup needed
- Data persists across deployments on most platforms

### PostgreSQL (For Production)
Most platforms offer free PostgreSQL:

**Render:**
- Automatically provides PostgreSQL
- Get connection string from dashboard

**Railway:**
- Add PostgreSQL plugin
- Copy connection string from variables

**Supabase (External):**
1. Create project at [supabase.com](https://supabase.com)
2. Get connection string from Settings → Database
3. Set as `DATABASE_URL` environment variable

---

## 🔧 Environment Variables Setup

For each platform, set these environment variables:

| Variable | Value | Required |
|----------|--------|----------|
| `SESSION_SECRET` | Random long string | Yes |
| `DATABASE_URL` | Database connection string | No (uses SQLite) |
| `FLASK_DEBUG` | `false` | Recommended |

**Generate a secure SESSION_SECRET:**
```python
import secrets
print(secrets.token_hex(32))
```

---

## 🐛 Troubleshooting Deployment

### Common Issues:

**1. "Application failed to start"**
- Check application logs
- Verify all dependencies in requirements
- Ensure `main.py` is the entry point

**2. "Static files not loading"**
- Verify static folder structure
- Check file paths in templates

**3. "Database connection failed"**
- Verify DATABASE_URL format
- Check database credentials
- Try SQLite fallback

**4. "Module not found"**
- Ensure all imports are correct
- Check requirements.txt is complete

### Getting Logs:

**Render:** Dashboard → Logs tab  
**Railway:** Project → Deployments → View logs  
**PythonAnywhere:** Web tab → Log files  
**Fly.io:** `fly logs`

---

## 📊 Free Tier Limitations

| Platform | Hours/Month | Sleep Time | Database |
|----------|-------------|------------|----------|
| Render | 750 | After 15min inactive | 1GB PostgreSQL |
| Railway | 500 hours | No sleep | 1GB PostgreSQL |
| PythonAnywhere | Always on | No sleep | MySQL |
| Fly.io | 2340 hours | After inactive | PostgreSQL |

---

## 🎉 Post-Deployment

### 1. Test Your App
- Register new student account
- Try all 5 forms
- Test admin dashboard
- Upload file attachments

### 2. Monitor Performance
- Check application logs regularly
- Monitor database usage
- Set up uptime monitoring

### 3. Custom Domain (Optional)
Most platforms allow custom domains on free tiers:
- Add CNAME record pointing to platform URL
- Configure in platform dashboard

---

## 🔒 Security Notes

1. **Change default admin password** immediately
2. **Use strong SESSION_SECRET** (64+ characters)
3. **Enable HTTPS** (most platforms do this automatically)
4. **Regular backups** of database
5. **Monitor logs** for suspicious activity

---

Your Student ERP System is now live and accessible worldwide! 🌍

**Need help?** Check platform documentation or deployment logs for specific error messages.