# Telegram File Transfer Bot

A Flask-based Telegram bot that enables seamless file transfers between Telegram, Google Drive, and basic torrent handling.

## Features

- 📁 **File Upload**: Upload files from Telegram directly to Google Drive
- 📥 **File Download**: Download files from Google Drive links to Telegram
- 🔗 **URL Downloads**: Download files from direct URLs and upload to Google Drive
- 🧲 **Torrent Support**: Basic torrent handling (MVP implementation)
- 📊 **Dashboard**: Web interface to monitor bot activity
- ⚙️ **Configuration**: Easy setup interface for API keys

## Quick Setup

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd telegram-file-transfer-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables
```bash
# Telegram Configuration
export TELEGRAM_BOT_TOKEN="your_bot_token_from_botfather"
export TELEGRAM_API_ID="your_api_id_from_my_telegram_org"
export TELEGRAM_API_HASH="your_api_hash_from_my_telegram_org"

# Google Drive Configuration
export GOOGLE_DRIVE_CREDENTIALS='{"type": "service_account", ...}'
export GOOGLE_DRIVE_FOLDER_ID="your_google_drive_folder_id"

# Optional Configuration
export WEBHOOK_URL="https://yourdomain.com/webhook"
export MAX_FILE_SIZE="52428800"  # 50MB in bytes
export TEMP_STORAGE_PATH="./temp_files"
export SESSION_SECRET="your-secret-key"
```

### 4. Run Application
```bash
# Development
python app.py

# Production
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## Getting API Credentials

### Telegram Bot Token
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow instructions
3. Copy the bot token (format: `1234567890:ABCDEFghijklmnop...`)

### Telegram API ID & Hash
1. Go to [my.telegram.org/apps](https://my.telegram.org/apps)
2. Create a new application
3. Copy API ID (number) and API Hash (32-character string)

### Google Drive Credentials
1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Create a new project or select existing
3. Enable Google Drive API
4. Create Service Account credentials
5. Download JSON key file
6. Copy entire JSON content to `GOOGLE_DRIVE_CREDENTIALS`

### Google Drive Folder ID (Optional)
1. Create a folder in Google Drive
2. Share it with your service account email
3. Copy folder ID from URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`

## Bot Commands

- `/start` - Show welcome message
- `/help` - Show detailed help
- `/upload [URL]` - Upload file from URL to Google Drive
- `/download [google_drive_link]` - Download from Google Drive
- `/torrent [magnet_link]` - Handle torrent downloads
- `/status` - Check bot and services status

## File Support

**Supported Formats:**
- Videos: `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm`
- Audio: `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.m4a`
- Documents: `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`
- Images: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`
- Archives: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`

**File Limits:**
- Maximum file size: 50MB (configurable)
- Automatic file validation
- Temporary file cleanup

## Deployment

### Replit Deployment
1. Import this repository to Replit
2. Set environment variables in Secrets
3. Run the application
4. Use the provided webhook URL

### Render Deployment (Recommended)
```bash
# Push to GitHub
git init && git add . && git commit -m "Initial commit"
git push origin main

# Deploy on Render
1. Connect GitHub repo at render.com
2. Set environment variables in dashboard
3. Deploy automatically using included render.yaml
```

### Heroku Deployment
```bash
# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set TELEGRAM_BOT_TOKEN="your_token"
heroku config:set GOOGLE_DRIVE_CREDENTIALS="your_json_credentials"
# ... set other variables

# Deploy
git push heroku main
```

### Docker Deployment
```bash
# Build image
docker build -t telegram-file-bot .

# Run container
docker run -p 5000:5000 \
  -e TELEGRAM_BOT_TOKEN="your_token" \
  -e GOOGLE_DRIVE_CREDENTIALS="your_credentials" \
  telegram-file-bot
```

## Project Structure

```
├── app.py                 # Main Flask application
├── main.py               # Application entry point
├── config.py             # Configuration management
├── bot_handlers.py       # Telegram bot message handling
├── google_drive_service.py # Google Drive API integration
├── torrent_service.py    # Torrent handling (MVP)
├── file_utils.py         # File operations utilities
├── templates/
│   ├── index.html        # Homepage
│   ├── config.html       # Configuration page
│   └── dashboard.html    # Monitoring dashboard
├── static/
│   ├── style.css         # Custom styles
│   └── app.js           # Frontend JavaScript
└── temp_files/          # Temporary file storage
```

## Security Features

- Environment-based secret management
- File size validation and restrictions
- Temporary file cleanup
- Secure API connections
- Error handling and logging

## Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check `TELEGRAM_BOT_TOKEN` is correct
   - Verify webhook is set properly
   - Check application logs

2. **Google Drive upload fails**
   - Verify service account JSON is valid
   - Check if service account has access to target folder
   - Ensure Google Drive API is enabled

3. **File size errors**
   - Check `MAX_FILE_SIZE` environment variable
   - Verify file is within Telegram's limits

### Logs and Monitoring

- Check application logs for detailed error information
- Use `/dashboard` to monitor bot statistics
- Use `/status` command to check service health

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests if applicable
5. Submit pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review application logs
3. Create an issue on GitHub
4. Contact support

---

**Note**: This is an MVP implementation. For production use, consider implementing additional security measures, rate limiting, and more robust error handling.