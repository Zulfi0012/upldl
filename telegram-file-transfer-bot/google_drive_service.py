import os
import logging
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError
import io
from config import Config

logger = logging.getLogger(__name__)

class GoogleDriveService:
    def __init__(self):
        self.service = None
        self.folder_id = Config.GOOGLE_DRIVE_FOLDER_ID
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Google Drive service"""
        try:
            credentials_dict = Config.get_credentials_dict()
            if not credentials_dict:
                logger.warning("Google Drive credentials not configured")
                return
            
            # Create credentials from service account info
            credentials = Credentials.from_service_account_info(
                credentials_dict,
                scopes=['https://www.googleapis.com/auth/drive']
            )
            
            # Build the service
            self.service = build('drive', 'v3', credentials=credentials)
            logger.info("Google Drive service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Drive service: {str(e)}")
            self.service = None
    
    def is_configured(self):
        """Check if Google Drive service is properly configured"""
        return self.service is not None
    
    def upload_file(self, file_path, filename):
        """Upload file to Google Drive"""
        try:
            if not self.service:
                logger.error("Google Drive service not configured")
                return None
            
            # File metadata
            file_metadata = {
                'name': filename,
                'parents': [self.folder_id] if self.folder_id else []
            }
            
            # Create media upload
            media = MediaFileUpload(file_path, resumable=True)
            
            # Upload file
            file_result = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            # Make file shareable
            self.service.permissions().create(
                fileId=file_result['id'],
                body={'role': 'reader', 'type': 'anyone'}
            ).execute()
            
            logger.info(f"File uploaded successfully: {file_result['name']}")
            return file_result.get('webViewLink')
            
        except HttpError as e:
            logger.error(f"Google Drive API error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error uploading file to Google Drive: {str(e)}")
            return None
    
    def download_file(self, file_id):
        """Download file from Google Drive"""
        try:
            if not self.service:
                logger.error("Google Drive service not configured")
                return None
            
            # Get file metadata
            file_metadata = self.service.files().get(fileId=file_id).execute()
            filename = file_metadata.get('name', f'downloaded_{file_id}')
            
            # Download file content
            request = self.service.files().get_media(fileId=file_id)
            
            # Create local file path
            local_file_path = os.path.join(Config.TEMP_STORAGE_PATH, f"gd_{filename}")
            
            # Download in chunks
            with open(local_file_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    logger.debug(f"Download progress: {int(status.progress() * 100)}%")
            
            logger.info(f"File downloaded successfully: {filename}")
            return local_file_path
            
        except HttpError as e:
            logger.error(f"Google Drive API error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error downloading file from Google Drive: {str(e)}")
            return None
    
    def list_files(self, folder_id=None, limit=10):
        """List files in Google Drive folder"""
        try:
            if not self.service:
                return []
            
            query = f"'{folder_id or self.folder_id}' in parents" if (folder_id or self.folder_id) else ""
            
            results = self.service.files().list(
                q=query,
                pageSize=limit,
                fields="nextPageToken, files(id, name, size, createdTime, webViewLink)"
            ).execute()
            
            return results.get('files', [])
            
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            return []
    
    def delete_file(self, file_id):
        """Delete file from Google Drive"""
        try:
            if not self.service:
                return False
            
            self.service.files().delete(fileId=file_id).execute()
            logger.info(f"File deleted successfully: {file_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return False
    
    def get_file_info(self, file_id):
        """Get file information"""
        try:
            if not self.service:
                return None
            
            file_info = self.service.files().get(
                fileId=file_id,
                fields="id, name, size, createdTime, modifiedTime, webViewLink, mimeType"
            ).execute()
            
            return file_info
            
        except Exception as e:
            logger.error(f"Error getting file info: {str(e)}")
            return None
