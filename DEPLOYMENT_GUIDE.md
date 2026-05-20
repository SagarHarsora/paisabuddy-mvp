# PaisaBuddy — Railway Deployment Guide

## For Non-Technical Users

This guide will walk you through deploying PaisaBuddy to Railway in **3 simple steps**.

---

## Prerequisites

- ✅ GitHub account (free, takes 2 minutes to create)
- ✅ Railway account (free tier available)
- ✅ This project ZIP file

---

## Step 1: Push Code to GitHub (5 minutes)

### 1.1 Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `paisabuddy-mvp`
3. Description: "PaisaBuddy MVP — Financial clarity for Indians"
4. Select "Public"
5. Click **Create repository**

### 1.2 Upload Code to GitHub

**Option A: Using GitHub Web Interface (Easiest)**

1. In your new repository, click **Add file → Upload files**
2. Drag and drop your `paisabuddy-mvp` folder
3. Scroll down and click **Commit changes**

**Option B: Using Git Command Line**

```bash
cd paisabuddy-mvp
git init
git add .
git commit -m "Initial commit: PaisaBuddy MVP"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/paisabuddy-mvp.git
git push -u origin main
```

---

## Step 2: Create Railway Project (3 minutes)

### 2.1 Sign Up for Railway

1. Go to [railway.app](https://railway.app)
2. Click **Sign Up** (or login if you have an account)
3. Connect with GitHub (recommended)

### 2.2 Create New Project

1. Click **+ New Project**
2. Select **Deploy from GitHub repo**
3. Authorize Railway to access GitHub
4. Select your `paisabuddy-mvp` repository
5. Click **Deploy**

Railway will automatically detect the `railway.toml` and start building.

---

## Step 3: Configure Environment Variables (5 minutes)

### 3.1 Set Database Password

1. In Railway dashboard, go to **Variables** tab
2. Click **+ Add Variable**
3. Add these variables:

```
ENVIRONMENT = production
DEBUG = false
JWT_SECRET = <generate a random string>
DATABASE_URL = postgresql://postgres:PASSWORD@localhost:5432/paisabuddy
REDIS_URL = redis://localhost:6379/0
SENTRY_DSN = <optional, get from sentry.io>
AWS_ACCESS_KEY_ID = <optional>
AWS_SECRET_ACCESS_KEY = <optional>
AWS_BUCKET_NAME = paisabuddy-statements-prod
AWS_REGION = ap-south-1
LOG_LEVEL = INFO
```

### 3.2 Generate JWT Secret

Go to this website to generate a random string: https://www.random.org/strings/

Use that as your `JWT_SECRET` value.

### 3.3 Add PostgreSQL

1. In Railway dashboard, click **+ Add Service**
2. Select **PostgreSQL**
3. It auto-generates a `DATABASE_URL` — copy this to your variables

### 3.4 Add Redis

1. Click **+ Add Service** again
2. Select **Redis**
3. It auto-generates a `REDIS_URL` — copy this to your variables

---

## Step 4: Deploy (Automatic)

Railway automatically deploys when you push to GitHub.

Once deployed:

1. Go to **Deployments** tab
2. Wait for "Build success" ✓
3. Copy the **Public URL** (it will be `https://your-app.railway.app`)
4. Visit the URL in your browser

**Your app is live!** 🎉

---

## Troubleshooting

### Build Failed

**Check logs:**
1. Go to **Deployments** tab
2. Click on the failed deployment
3. Scroll down to see error messages
4. Most common: Missing environment variables

**Solution:** Go back to Step 3 and ensure all variables are set.

### PostgreSQL Connection Error

**Solution:**
1. Make sure `DATABASE_URL` is set correctly
2. Check that PostgreSQL service is running (green checkmark in services)
3. Restart the deployment

### App Not Loading

**Solution:**
1. Wait 2-3 minutes after deployment (apps take time to boot)
2. Refresh the browser
3. Check the logs for errors

---

## Next Steps

### Test the API

1. Go to `https://your-app.railway.app/docs` (if DEBUG=true)
2. Or use `https://your-app.railway.app/api/v1/health` to check health

### Monitor in Production

1. Set up **Sentry.io** account (free tier)
2. Get Sentry DSN
3. Add `SENTRY_DSN` to Railway variables
4. Errors will now be tracked automatically

### View Logs

1. Go to Railway dashboard
2. Click **Logs** tab
3. See real-time application logs

---

## Common Questions

### How much will it cost?

- Free tier: up to 5 projects, limited computing
- Paid tier: ~$5-10/month for a small fintech app
- Database: included in Railway pricing

### How do I update the code?

1. Make changes locally
2. Commit: `git add . && git commit -m "message"`
3. Push: `git push origin main`
4. Railway automatically redeploys

### How do I see error messages?

Railway → Logs tab → Shows all errors in real-time

### How do I backup the database?

Railway provides automatic daily backups (paid plans).

For free tier, use `pg_dump` to manually backup:
```bash
pg_dump $DATABASE_URL > backup.sql
```

---

## Success!

Your PaisaBuddy MVP is now live on the internet. 🚀

**Next:** Share the public URL with testers and collect feedback.

---

*For more help, see Railway docs: [docs.railway.app](https://docs.railway.app)*
