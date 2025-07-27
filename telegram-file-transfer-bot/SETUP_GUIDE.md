# Quick Setup Guide for Telegram File Transfer Bot

## 📁 Project Structure
```
telegram-file-transfer-bot/
├── app.py                    # Main Flask application
├── main.py                   # Application entry point
├── config.py                 # Configuration management
├── bot_handlers.py           # Telegram bot logic
├── google_drive_service.py   # Google Drive integration
├── torrent_service.py        # Torrent handling
├── file_utils.py            # File utilities
├── templates/               # HTML templates
│   ├── index.html          # Homepage
│   ├── config.html         # Configuration page
│   └── dashboard.html      # Dashboard
├── static/                 # Static files
│   ├── style.css          # Custom styles
│   └── app.js             # Frontend JavaScript
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker deployment
├── deploy.sh              # Deployment script
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
└── README.md              # Full documentation
```

## 🚀 Quick Start (5 Minutes)

### 1. Get Your Credentials

**Telegram Bot:**
- Go to [@BotFather](https://t.me/BotFather) on Telegram
- Send `/newbot` and follow instructions
- Copy your bot token

**Telegram API (Optional but Recommended):**
- Visit [my.telegram.org/apps](https://my.telegram.org/apps)
- Create new application
- Copy API ID and API Hash

**Google Drive:**
- Go to [Google Cloud Console](https://console.developers.google.com/)
- Create project → Enable Drive API → Create Service Account
- Download JSON credentials

### 2. Deploy Options

#### Option A: Local Development
```bash
# Extract ZIP file
unzip telegram-file-transfer-bot.zip
cd telegram-file-transfer-bot

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TELEGRAM_BOT_TOKEN="your_token_here"
export GOOGLE_DRIVE_CREDENTIALS='{"your": "json_here"}'

# Run application
python app.py
```

#### Option B: Render Deployment (Recommended)
1. Push code to GitHub
2. Connect repo at render.com
3. Set environment variables in dashboard
4. Deploy using included render.yaml config
5. Set webhook URL to your Render app

#### Option C: Replit Deployment
1. Upload ZIP to Replit
2. Extract files
3. Set Secrets in Replit:
   - `TELEGRAM_BOT_TOKEN`
   - `GOOGLE_DRIVE_CREDENTIALS`
   - `TELEGRAM_API_ID` (optional)
   - `TELEGRAM_API_HASH` (optional)
4. Run the application

#### Option D: Heroku Deployment
```bash
# Create Heroku app
heroku create your-bot-name

# Set environment variables
heroku config:set TELEGRAM_BOT_TOKEN="your_token"
heroku config:set GOOGLE_DRIVE_CREDENTIALS="your_json"

# Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

#### Option E: Docker Deployment
```bash
# Build and run
docker build -t telegram-file-bot .
docker run -p 5000:5000 \
  -e TELEGRAM_BOT_TOKEN="your_token" \
  -e GOOGLE_DRIVE_CREDENTIALS="your_json" \
  telegram-file-bot
```

### 3. Set Webhook
After deployment, set your bot's webhook:
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://your-app-url.com/webhook"}'
```

## 🔧 Environment Variables

**Required:**
- `TELEGRAM_BOT_TOKEN` - Your bot token from BotFather
- `GOOGLE_DRIVE_CREDENTIALS` - Complete JSON from service account

**Optional:**
- `TELEGRAM_API_ID` - For advanced features
- `TELEGRAM_API_HASH` - For advanced features
- `GOOGLE_DRIVE_FOLDER_ID` - Specific folder for uploads
- `WEBHOOK_URL` - Your webhook endpoint
- `MAX_FILE_SIZE` - File size limit (default: 50MB)

## 📱 Bot Commands
Once running, your bot supports:
- `/start` - Welcome message
- `/help` - Detailed help
- `/upload [URL]` - Upload from URL
- `/download [drive_link]` - Download from Google Drive
- `/torrent [magnet]` - Handle torrents
- `/status` - Check bot status
- Send files directly to upload to Google Drive

## 🌐 Web Interface
- Homepage: `http://your-app/`
- Configuration: `http://your-app/config`
- Dashboard: `http://your-app/dashboard`

## 🆘 Troubleshooting
- Check application logs for errors
- Verify all environment variables are set
- Ensure Google Drive service account has permissions
- Test webhook endpoint is accessible

## 📞 Support
- Check README.md for detailed documentation
- Review logs for specific error messages
- Verify API credentials are correct