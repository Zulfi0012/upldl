import os
import json

class Config:
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    TELEGRAM_API_ID = os.environ.get('TELEGRAM_API_ID')
    TELEGRAM_API_HASH = os.environ.get('TELEGRAM_API_HASH')
    WEBHOOK_URL = os.environ.get('WEBHOOK_URL', 'https://your-app-name.onrender.com/webhook')
    
    # Google Drive Configuration
    GOOGLE_DRIVE_CREDENTIALS = os.environ.get('GOOGLE_DRIVE_CREDENTIALS')
    GOOGLE_DRIVE_FOLDER_ID = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')
    
    # File Configuration
    MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', 50 * 1024 * 1024))  # 50MB default
    ALLOWED_EXTENSIONS = {
        'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
        'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
        'document': ['.pdf', '.doc', '.docx', '.txt', '.rtf'],
        'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
        'archive': ['.zip', '.rar', '.7z', '.tar', '.gz']
    }
    
    # Storage Configuration
    TEMP_STORAGE_PATH = os.environ.get('TEMP_STORAGE_PATH', './temp_files')
    
    # Bot Messages
    MESSAGES = {
        'welcome': """🤖 Welcome to File Transfer Bot!
        
Available commands:
/start - Show this help message
/upload [file/link] - Upload file to Google Drive
/download [google_drive_link] - Download from Google Drive to Telegram
/torrent [magnet_link] - Handle torrent downloads
/status - Check bot status
/help - Show detailed help

Simply send me a file and I'll upload it to Google Drive!""",
        
        'help': """📖 Detailed Help:

🔸 File Upload:
- Send any file directly to upload to Google Drive
- Use /upload command with file or link
- Supported: Videos, Audio, Documents, Images, Archives

🔸 Google Drive Download:
- Use /download with Google Drive share link
- Files will be sent back to Telegram

🔸 Torrent Handling:
- Use /torrent with magnet link (basic support)
- Files will be processed and uploaded to Google Drive

🔸 Limits:
- Maximum file size: 50MB
- Supported formats: Most common file types

🔸 Commands:
/status - Check bot and service status
/help - Show this help message""",
        
        'file_too_large': '❌ File is too large. Maximum size is 50MB.',
        'unsupported_format': '❌ Unsupported file format.',
        'upload_success': '✅ File uploaded to Google Drive successfully!',
        'download_success': '✅ File downloaded and sent successfully!',
        'error_occurred': '❌ An error occurred: {}',
        'processing': '⏳ Processing your request...',
        'invalid_link': '❌ Invalid or unsupported link format.',
        'google_drive_error': '❌ Google Drive service is not configured properly.'
    }
    
    @classmethod
    def get_credentials_dict(cls):
        """Parse Google Drive credentials from environment variable"""
        if cls.GOOGLE_DRIVE_CREDENTIALS:
            try:
                return json.loads(cls.GOOGLE_DRIVE_CREDENTIALS)
            except json.JSONDecodeError:
                return None
        return None
