import os
import logging
import requests
import mimetypes
from urllib.parse import urlparse
from config import Config

logger = logging.getLogger(__name__)

class FileUtils:
    """Utility class for file operations"""
    
    def __init__(self):
        self.temp_path = Config.TEMP_STORAGE_PATH
        os.makedirs(self.temp_path, exist_ok=True)
    
    def download_from_url(self, url, filename=None):
        """Download file from URL"""
        try:
            # Validate URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                logger.error("Invalid URL format")
                return None
            
            # Make request with headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()
            
            # Check content length
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > Config.MAX_FILE_SIZE:
                logger.error("File too large")
                return None
            
            # Determine filename
            if not filename:
                filename = self.get_filename_from_url(url, response)
            
            # Create local file path
            local_file_path = os.path.join(self.temp_path, f"url_{filename}")
            
            # Download file
            total_size = 0
            with open(local_file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        total_size += len(chunk)
                        
                        # Check size limit during download
                        if total_size > Config.MAX_FILE_SIZE:
                            f.close()
                            os.remove(local_file_path)
                            logger.error("File size exceeded limit during download")
                            return None
            
            logger.info(f"Downloaded file: {filename} ({total_size} bytes)")
            return local_file_path
            
        except requests.RequestException as e:
            logger.error(f"Request error downloading file: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error downloading file from URL: {str(e)}")
            return None
    
    def get_filename_from_url(self, url, response=None):
        """Extract filename from URL or response headers"""
        try:
            # Try to get filename from Content-Disposition header
            if response and 'content-disposition' in response.headers:
                content_disposition = response.headers['content-disposition']
                if 'filename=' in content_disposition:
                    filename = content_disposition.split('filename=')[1].strip('"\'')
                    return filename
            
            # Extract from URL path
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            
            if filename and '.' in filename:
                return filename
            
            # Generate default filename based on content type
            content_type = response.headers.get('content-type', '') if response else ''
            extension = mimetypes.guess_extension(content_type.split(';')[0]) or '.bin'
            return f"downloaded_file{extension}"
            
        except Exception as e:
            logger.error(f"Error getting filename: {str(e)}")
            return "downloaded_file.bin"
    
    def get_file_type(self, filename):
        """Determine file type based on extension"""
        try:
            _, ext = os.path.splitext(filename.lower())
            
            for file_type, extensions in Config.ALLOWED_EXTENSIONS.items():
                if ext in extensions:
                    return file_type
            
            return 'unknown'
            
        except Exception as e:
            logger.error(f"Error determining file type: {str(e)}")
            return 'unknown'
    
    def is_supported_file(self, filename):
        """Check if file type is supported"""
        file_type = self.get_file_type(filename)
        return file_type != 'unknown'
    
    def get_file_size(self, file_path):
        """Get file size in bytes"""
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            logger.error(f"Error getting file size: {str(e)}")
            return 0
    
    def cleanup_file(self, file_path):
        """Delete temporary file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.debug(f"Cleaned up file: {file_path}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error cleaning up file: {str(e)}")
            return False
    
    def cleanup_old_files(self, max_age_hours=24):
        """Clean up old temporary files"""
        try:
            import time
            current_time = time.time()
            cleaned_count = 0
            
            for filename in os.listdir(self.temp_path):
                file_path = os.path.join(self.temp_path, filename)
                
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getmtime(file_path)
                    
                    if file_age > (max_age_hours * 3600):
                        self.cleanup_file(file_path)
                        cleaned_count += 1
            
            logger.info(f"Cleaned up {cleaned_count} old files")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Error cleaning up old files: {str(e)}")
            return 0
    
    def get_file_info(self, file_path):
        """Get comprehensive file information"""
        try:
            if not os.path.exists(file_path):
                return None
            
            stat = os.stat(file_path)
            filename = os.path.basename(file_path)
            
            return {
                'filename': filename,
                'size': stat.st_size,
                'created': stat.st_ctime,
                'modified': stat.st_mtime,
                'type': self.get_file_type(filename),
                'supported': self.is_supported_file(filename),
                'path': file_path
            }
            
        except Exception as e:
            logger.error(f"Error getting file info: {str(e)}")
            return None
    
    def validate_file(self, file_path):
        """Validate file before processing"""
        try:
            file_info = self.get_file_info(file_path)
            if not file_info:
                return False, "File not found"
            
            # Check file size
            if file_info['size'] > Config.MAX_FILE_SIZE:
                return False, f"File too large (max {Config.MAX_FILE_SIZE // (2*1024*1024*1024)}MB)"
            
            # Check if file type is supported
            if not file_info['supported']:
                return False, "Unsupported file type"
            
            return True, "File is valid"
            
        except Exception as e:
            logger.error(f"Error validating file: {str(e)}")
            return False, f"Validation error: {str(e)}"
