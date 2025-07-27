# Render Deployment Guide for Telegram File Transfer Bot

## 🚀 Deploy to Render in 5 Minutes

Render is an excellent platform for hosting your Telegram bot with automatic SSL, custom domains, and easy environment variable management.

## 📋 Prerequisites

Before deploying, ensure you have:
- **Telegram Bot Token** (from @BotFather)
- **Google Drive Service Account JSON** (from Google Cloud Console)
- **Telegram API ID & Hash** (optional, from my.telegram.org/apps)
- **GitHub account** (to connect your repository)

## 🔧 Step-by-Step Deployment

### 1. Prepare Your Repository

```bash
# Upload your project to GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/telegram-file-bot.git
git push -u origin main
```

### 2. Deploy on Render

#### Option A: Using Render Dashboard (Recommended)
1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `telegram-file-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --reuse-port main:app`
   - **Instance Type**: `Free` (or higher for production)

#### Option B: Using render.yaml (Automatic)
1. The project includes `render.yaml` for automatic configuration
2. Simply connect your GitHub repo and Render will detect the configuration
3. Review and deploy

### 3. Set Environment Variables

In your Render service dashboard, go to **Environment** and add:

**Required Variables:**
```
TELEGRAM_BOT_TOKEN = 1234567890:ABCDEFghijklmnop_qrstuvwxyz
GOOGLE_DRIVE_CREDENTIALS = {"type": "service_account", "project_id": "..."}
```

**Optional Variables:**
```
TELEGRAM_API_ID = 1234567
TELEGRAM_API_HASH = abcdef1234567890abcdef1234567890
GOOGLE_DRIVE_FOLDER_ID = 1ABcDEfGhIjKlMnOpQrStUvWxYz
WEBHOOK_URL = https://your-app-name.onrender.com/webhook
MAX_FILE_SIZE = 52428800
TEMP_STORAGE_PATH = ./temp_files
```

### 4. Deploy and Set Webhook

1. Click **"Create Web Service"** - Render will automatically deploy
2. Once deployed, note your app URL: `https://your-app-name.onrender.com`
3. Set your Telegram webhook:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://your-app-name.onrender.com/webhook"}'
```

### 5. Test Your Bot

1. Visit your web interface: `https://your-app-name.onrender.com`
2. Check the dashboard: `https://your-app-name.onrender.com/dashboard`
3. Send a message to your Telegram bot to test

## 🔧 Render Configuration Details

### Build Settings
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --reuse-port main:app`
- **Python Version**: 3.11.0
- **Auto-Deploy**: Disabled (deploy manually for control)

### Health Check
- **Health Check Path**: `/health`
- Render will monitor this endpoint to ensure your service is running

### Persistent Storage
⚠️ **Important**: Render's free tier has ephemeral storage. Temporary files are automatically cleaned up, which is perfect for this bot.

## 🌐 Custom Domain (Optional)

1. In Render dashboard, go to **Settings** → **Custom Domains**
2. Add your domain (e.g., `mybot.yourdomain.com`)
3. Update your webhook URL to use the custom domain
4. Update `WEBHOOK_URL` environment variable

## 📊 Monitoring and Logs

### View Logs
- Go to your service dashboard
- Click **"Logs"** tab to see real-time application logs
- Monitor webhook requests and bot activity

### Health Monitoring
- Render automatically monitors `/health` endpoint
- Service will restart if health checks fail
- View uptime statistics in dashboard

## 🔒 Security Best Practices

### Environment Variables
- Never commit secrets to your repository
- Use Render's environment variable encryption
- Regenerate tokens if compromised

### Webhook Security
- Your webhook URL is public but secured by Telegram's validation
- Consider adding webhook secret validation for extra security

## 💰 Pricing Considerations

### Free Tier Limitations
- 750 hours/month (sufficient for most bots)
- Service sleeps after 15 minutes of inactivity
- 0.1 CPU, 512MB RAM

### Paid Plans
- **Starter ($7/month)**: Always-on, more resources
- **Standard ($25/month)**: Production-ready with scaling
- **Pro ($85/month)**: High-performance applications

## 🚨 Troubleshooting

### Common Issues

#### 1. Bot Not Responding
```bash
# Check if webhook is set correctly
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"

# Reset webhook if needed
curl -X POST "https://api.telegram.org/bot<TOKEN>/deleteWebhook"
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
     -d "url=https://your-app.onrender.com/webhook"
```

#### 2. Google Drive Errors
- Verify JSON credentials are valid
- Check if service account has Drive permissions
- Ensure Google Drive API is enabled

#### 3. Service Sleeping (Free Tier)
- Upgrade to paid plan for always-on service
- Use external monitoring services to ping your app
- Implement keep-alive mechanisms

#### 4. Build Failures
```bash
# Check requirements.txt is valid
pip install -r requirements.txt

# Verify Python version compatibility
python --version
```

### Debugging Steps
1. Check Render logs for error messages
2. Test endpoints manually: `/health`, `/webhook`
3. Verify environment variables are set correctly
4. Monitor bot activity in `/dashboard`

## 🔄 Updates and Maintenance

### Automatic Deployments
1. Enable auto-deploy in Render settings
2. Push changes to your main branch
3. Render automatically rebuilds and deploys

### Manual Deployments
1. Make changes to your code
2. Push to GitHub
3. Click "Manual Deploy" in Render dashboard

### Rolling Back
- Render keeps deployment history
- Click previous deployment to rollback instantly

## 📈 Scaling Considerations

### Performance Optimization
- Monitor CPU/memory usage in Render dashboard
- Upgrade instance type if needed
- Implement file size limits to prevent resource exhaustion

### High Availability
- Use paid plans for 99.9% uptime SLA
- Consider load balancing for high-traffic bots
- Implement database for persistent statistics

## 🆘 Support Resources

- **Render Documentation**: [render.com/docs](https://render.com/docs)
- **Render Community**: [community.render.com](https://community.render.com)
- **Telegram Bot API**: [core.telegram.org/bots/api](https://core.telegram.org/bots/api)
- **Google Drive API**: [developers.google.com/drive](https://developers.google.com/drive)

## ✅ Deployment Checklist

- [ ] GitHub repository created and pushed
- [ ] Render service configured
- [ ] Environment variables set
- [ ] Service deployed successfully
- [ ] Webhook URL set in Telegram
- [ ] Bot responds to test messages
- [ ] Web interface accessible
- [ ] Google Drive integration working
- [ ] Dashboard showing statistics

---

**🎉 Congratulations!** Your Telegram File Transfer Bot is now live on Render and ready to handle file transfers between Telegram and Google Drive!