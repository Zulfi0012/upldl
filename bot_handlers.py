import logging
import os
import requests
import json
from urllib.parse import urlparse
from config import Config
from google_drive_service import GoogleDriveService
from torrent_service import TorrentService
from file_utils import FileUtils

logger = logging.getLogger(__name__)

class BotHandler:
    def __init__(self):
        self.token = Config.TELEGRAM_BOT_TOKEN
        self.api_url = f"https://api.telegram.org/bot{self.token}"
        self.google_drive = GoogleDriveService()
        self.torrent_service = TorrentService()
        self.file_utils = FileUtils()
        self.stats = {
            'messages_processed': 0,
            'files_uploaded': 0,
            'files_downloaded': 0,
            'errors': 0
        }
        
        # Ensure temp directory exists
        os.makedirs(Config.TEMP_STORAGE_PATH, exist_ok=True)
    
    def process_update(self, update):
        """Process incoming Telegram update"""
        try:
            self.stats['messages_processed'] += 1
            
            if 'message' in update:
                message = update['message']
                chat_id = message['chat']['id']
                
                # Handle different message types
                if 'text' in message:
                    return self.handle_text_message(chat_id, message['text'])
                elif 'document' in message:
                    return self.handle_file_message(chat_id, message['document'], 'document')
                elif 'video' in message:
                    return self.handle_file_message(chat_id, message['video'], 'video')
                elif 'audio' in message:
                    return self.handle_file_message(chat_id, message['audio'], 'audio')
                elif 'photo' in message:
                    # Get the largest photo
                    photo = max(message['photo'], key=lambda p: p['file_size'])
                    return self.handle_file_message(chat_id, photo, 'photo')
                
        except Exception as e:
            logger.error(f"Error processing update: {str(e)}")
            self.stats['errors'] += 1
            return None
    
    def handle_text_message(self, chat_id, text):
        """Handle text messages and commands"""
        try:
            text = text.strip()
            
            if text.startswith('/start'):
                return self.send_message(chat_id, Config.MESSAGES['welcome'])
            
            elif text.startswith('/help'):
                return self.send_message(chat_id, Config.MESSAGES['help'])
            
            elif text.startswith('/status'):
                return self.handle_status_command(chat_id)
            
            elif text.startswith('/upload'):
                return self.handle_upload_command(chat_id, text)
            
            elif text.startswith('/download'):
                return self.handle_download_command(chat_id, text)
            
            elif text.startswith('/torrent'):
                return self.handle_torrent_command(chat_id, text)
            
            elif self.is_google_drive_link(text):
                return self.handle_google_drive_download(chat_id, text)
            
            elif self.is_magnet_link(text):
                return self.handle_torrent_download(chat_id, text)
            
            else:
                return self.send_message(chat_id, 
                    "I don't understand that command. Use /help for available commands.")
                
        except Exception as e:
            logger.error(f"Error handling text message: {str(e)}")
            return self.send_message(chat_id, Config.MESSAGES['error_occurred'].format(str(e)))
    
    def handle_file_message(self, chat_id, file_info, file_type):
        """Handle file uploads"""
        try:
            # Send processing message
            self.send_message(chat_id, Config.MESSAGES['processing'])
            
            # Get file information
            file_id = file_info['file_id']
            file_size = file_info.get('file_size', 0)
            
            # Check file size
            if file_size > Config.MAX_FILE_SIZE:
                return self.send_message(chat_id, Config.MESSAGES['file_too_large'])
            
            # Download file from Telegram
            file_path = self.download_telegram_file(file_id)
            if not file_path:
                return self.send_message(chat_id, "Failed to download file from Telegram.")
            
            # Upload to Google Drive
            result = self.google_drive.upload_file(file_path, file_info.get('file_name', f'telegram_file_{file_id}'))
            
            # Cleanup temp file
            self.file_utils.cleanup_file(file_path)
            
            if result:
                self.stats['files_uploaded'] += 1
                return self.send_message(chat_id, 
                    f"{Config.MESSAGES['upload_success']}\nGoogle Drive link: {result}")
            else:
                return self.send_message(chat_id, "Failed to upload file to Google Drive.")
                
        except Exception as e:
            logger.error(f"Error handling file message: {str(e)}")
            self.stats['errors'] += 1
            return self.send_message(chat_id, Config.MESSAGES['error_occurred'].format(str(e)))
    
    def handle_status_command(self, chat_id):
        """Handle status command"""
        try:
            google_drive_status = "✅ Connected" if self.google_drive.is_configured() else "❌ Not configured"
            
            status_message = f"""🤖 Bot Status:

📊 Statistics:
• Messages processed: {self.stats['messages_processed']}
• Files uploaded: {self.stats['files_uploaded']}
• Files downloaded: {self.stats['files_downloaded']}
• Errors: {self.stats['errors']}

🔧 Services:
• Google Drive: {google_drive_status}
• Torrent Service: ✅ Ready
• File Storage: ✅ Ready

💾 Configuration:
• Max file size: {Config.MAX_FILE_SIZE // (1024*1024)}MB
• Temp storage: {Config.TEMP_STORAGE_PATH}"""
            
            return self.send_message(chat_id, status_message)
            
        except Exception as e:
            logger.error(f"Error handling status command: {str(e)}")
            return self.send_message(chat_id, Config.MESSAGES['error_occurred'].format(str(e)))
    
    def handle_upload_command(self, chat_id, text):
        """Handle upload command with URL"""
        try:
            parts = text.split(' ', 1)
            if len(parts) < 2:
                return self.send_message(chat_id, 
                    "Please provide a URL after /upload command.\nExample: /upload https://example.com/file.pdf")
            
            url = parts[1].strip()
            
            # Send processing message
            self.send_message(chat_id, Config.MESSAGES['processing'])
            
            # Download file from URL
            file_path = self.file_utils.download_from_url(url)
            if not file_path:
                return self.send_message(chat_id, "Failed to download file from the provided URL.")
            
            # Upload to Google Drive
            filename = os.path.basename(urlparse(url).path) or 'downloaded_file'
            result = self.google_drive.upload_file(file_path, filename)
            
            # Cleanup temp file
            self.file_utils.cleanup_file(file_path)
            
            if result:
                self.stats['files_uploaded'] += 1
                return self.send_message(chat_id, 
                    f"{Config.MESSAGES['upload_success']}\nGoogle Drive link: {result}")
            else:
                return self.send_message(chat_id, "Failed to upload file to Google Drive.")
                
        except Exception as e:
            logger.error(f"Error handling upload command: {str(e)}")
            return self.send_message(chat_id, Config.MESSAGES['error_occurred'].format(str(e)))
    
    def handle_download_command(self, chat_id, text):
        """Handle download command"""
        try:
            parts = text.split(' ', 1)
            if len(parts) < 2:
                return self.send_message(chat_id, 
                    "Please provide a Google Drive link after /download command.\nExample: /download https://drive.google.com/file/d/...")
            
            url = parts[1].strip()
            return self.handle_google_drive_download(chat_id, url)
            
        except Exception as e:
            logger.error(f"Error handling download command: {str(e)}")
            return self.send_message(chat_id, Config.MESSAGES['error_occurred'].format(str(e)))
    
    def handle_torrent_command(self, chat_id, text):
        """Handle torrent command"""
        try:
            parts = text.split(' ', 1)
            if len(parts) < 2:
                return self.send_message(chat_id, 
                    "Please provide a magnet link after /torrent command.\nExample: /torrent magnet:?xt=...")
            
            magnet_link = parts[1].strip()
            return self.handle_torrent_download(chat_id, magnet_link)
            
        except Exception as e:
            logger.error(f"Error handling torrent command: {str(e)}")
            return self.send_message(chat_id, Config.MESSAGES['error_occurred'].format(str(e)))
    
    def handle_google_drive_download(self, chat_id, url):
        """Handle Google Drive file download"""
        try:
            # Send processing message
            self.send_message(chat_id, Config.MESSAGES['processing'])
            
            # Extract file ID from Google Drive URL
            file_id = self.extract_google_drive_file_id(url)
            if not file_id:
                return self.send_message(chat_id, Config.MESSAGES['invalid_link'])
            
            # Download from Google Drive
            file_path = self.google_drive.download_file(file_id)
            if not file_path:
                return self.send_message(chat_id, "Failed to download file from Google Drive.")
            
            # Send file to Telegram
            result = self.send_file_to_telegram(chat_id, file_path)
            
            # Cleanup temp file
            self.file_utils.cleanup_file(file_path)
            
            if result:
                self.stats['files_downloaded'] += 1
                return self.send_message(chat_id, Config.MESSAGES['download_success'])
            else:
                return self.send_message(chat_id, "Failed to send file to Telegram.")
                
        except Exception as e:
            logger.error(f"Error handling Google Drive download: {str(e)}")
            return self.send_message(chat_id, Config.MESSAGES['error_occurred'].format(str(e)))
    
    def handle_torrent_download(self, chat_id, magnet_link):
        """Handle torrent download (simplified implementation)"""
        try:
            # Send processing message
            self.send_message(chat_id, Config.MESSAGES['processing'])
            
            # Process torrent (mock implementation for MVP)
            result = self.torrent_service.process_magnet_link(magnet_link)
            
            if result:
                return self.send_message(chat_id, 
                    f"✅ Torrent processed successfully!\n"
                    f"Note: This is a simplified implementation. "
                    f"Full torrent support requires additional infrastructure.")
            else:
                return self.send_message(chat_id, "Failed to process torrent.")
                
        except Exception as e:
            logger.error(f"Error handling torrent download: {str(e)}")
            return self.send_message(chat_id, Config.MESSAGES['error_occurred'].format(str(e)))
    
    def download_telegram_file(self, file_id):
        """Download file from Telegram"""
        try:
            # Get file info
            response = requests.get(f"{self.api_url}/getFile?file_id={file_id}")
            if response.status_code != 200:
                return None
            
            file_info = response.json()
            if not file_info['ok']:
                return None
            
            file_path = file_info['result']['file_path']
            download_url = f"https://api.telegram.org/file/bot{self.token}/{file_path}"
            
            # Download file
            response = requests.get(download_url)
            if response.status_code != 200:
                return None
            
            # Save to temp file
            local_file_path = os.path.join(Config.TEMP_STORAGE_PATH, f"tg_{file_id}")
            with open(local_file_path, 'wb') as f:
                f.write(response.content)
            
            return local_file_path
            
        except Exception as e:
            logger.error(f"Error downloading Telegram file: {str(e)}")
            return None
    
    def send_file_to_telegram(self, chat_id, file_path):
        """Send file to Telegram"""
        try:
            with open(file_path, 'rb') as f:
                files = {'document': f}
                data = {'chat_id': chat_id}
                
                response = requests.post(f"{self.api_url}/sendDocument", 
                                       files=files, data=data)
                
                return response.status_code == 200
                
        except Exception as e:
            logger.error(f"Error sending file to Telegram: {str(e)}")
            return False
    
    def send_message(self, chat_id, text):
        """Send text message to Telegram"""
        try:
            data = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(f"{self.api_url}/sendMessage", json=data)
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return False
    
    def set_webhook(self):
        """Set up Telegram webhook"""
        try:
            data = {'url': Config.WEBHOOK_URL}
            response = requests.post(f"{self.api_url}/setWebhook", json=data)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('ok', False)
            return False
            
        except Exception as e:
            logger.error(f"Error setting webhook: {str(e)}")
            return False
    
    def is_google_drive_link(self, text):
        """Check if text is a Google Drive link"""
        return 'drive.google.com' in text and '/file/d/' in text
    
    def is_magnet_link(self, text):
        """Check if text is a magnet link"""
        return text.startswith('magnet:?')
    
    def extract_google_drive_file_id(self, url):
        """Extract file ID from Google Drive URL"""
        try:
            if '/file/d/' in url:
                return url.split('/file/d/')[1].split('/')[0]
            return None
        except:
            return None
    
    def get_stats(self):
        """Get bot statistics"""
        return self.stats.copy()
