import os
import json
import logging
import glob
import time
from pathlib import Path
from .errors import FileError, ConfigurationError

class FileManager:
    """Handles file operations and directory management"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @staticmethod
    def ensure_directories():
        """Ensure all required directories exist with proper permissions"""
        directories = [
            "data/audio",
            "data/cloud",
            "data/temp",
            "data/datasets"
        ]
        
        for directory in directories:
            path = Path(directory)
            path.mkdir(parents=True, exist_ok=True)
            
            try:
                path.chmod(0o777)
                
                for file in path.glob('*'):
                    if file.is_file():
                        file.chmod(0o666)
            except Exception as e:
                print(f"Warning: Could not set permissions for {directory}: {e}")


    def save_json(self, filename: str, data: dict):
        """
        Save data to a JSON file with error handling
        
        Args:
            filename: Path to save the file
            data: Dictionary data to save as JSON
        
        Raises:
            FileError: If the file cannot be saved
        """
        try:
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filename, "w") as f:
                json.dump(data, f)
        except Exception as e:
            self.logger.error(
                f"Failed to save file {filename}",
                extra={"error": str(e)}
            )
            raise FileError(
                message=f"Failed to save data to {filename}",
                code="DATA_SAVE_ERROR",
                details={"error": str(e)}
            )

    def load_json(self, filename: str) -> dict:
        """
        Load data from a JSON file with error handling
        
        Args:
            filename: Path to the JSON file
            
        Returns:
            Dictionary containing the loaded data
            
        Raises:
            FileError: If the file cannot be loaded due to not found, invalid JSON, or other errors
        """
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error(f"File {filename} not found")
            raise FileError(
                message=f"File not found: {filename}",
                code="FILE_NOT_FOUND",
                details={"filename": filename}
            )
        except json.JSONDecodeError as e:
            self.logger.error(
                f"Invalid JSON in {filename}",
                extra={"error": str(e)}
            )
            raise FileError(
                message=f"Invalid JSON format in {filename}",
                code="INVALID_JSON",
                details={"error": str(e), "filename": filename}
            )
        except Exception as e:
            self.logger.error(
                f"Error loading {filename}",
                extra={"error": str(e)}
            )
            raise FileError(
                message=f"Failed to load file: {filename}",
                code="FILE_LOAD_ERROR",
                details={"error": str(e), "filename": filename}
            )

    @staticmethod
    def save_audio_file(audio_content: bytes, audio_format: str = "audio/wav") -> str:
        """
        Save audio content with timestamp and proper permissions
        
        Args:
            audio_content: Raw audio bytes
            audio_format: MIME type (e.g. 'audio/wav', 'audio/mp3', 'audio/ogg')
        """
        try:
            timestamp = int(time.time() * 1000)
            extension = audio_format.split('/')[-1]  # Extract 'wav' from 'audio/wav'
            final_path = f"data/audio/output_{timestamp}.{extension}"
            
            os.makedirs(os.path.dirname(final_path), exist_ok=True)
            
            with open(final_path, "wb") as audio_file:
                audio_file.write(audio_content)
            
            os.chmod(final_path, 0o666)
            
            FileManager.cleanup_audio_files()
            
            return final_path
            
        except Exception as e:
            raise FileError(
                message="Failed to save audio file",
                code="AUDIO_SAVE_ERROR",
                details={"error": str(e)}
            )

    @staticmethod
    def cleanup_audio_files(max_files: int = 5):
        """Clean up old audio files keeping only the most recent ones"""
        try:
            audio_dir = "data/audio"
            audio_files = []
            for ext in ['wav', 'mp3', 'ogg']:
                audio_files.extend(glob.glob(f"{audio_dir}/*.{ext}"))
            
            if len(audio_files) > max_files:
                audio_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                
                for file in audio_files[max_files:]:
                    try:
                        if os.path.exists(file):
                            os.remove(file)
                    except Exception as e:
                        logging.warning(f"Could not remove file {file}: {e}")
                        
        except Exception as e:
            logging.error(f"Audio cleanup failed: {e}")

    @staticmethod
    def ensure_audio_directory():
        """Ensure audio directory exists with correct permissions"""
        try:
            audio_dir = Path("data/audio")
            audio_dir.mkdir(parents=True, exist_ok=True)
            audio_dir.chmod(0o777)
            FileManager.cleanup_audio_files()
        except Exception as e:
            raise FileError(
                message="Failed to setup audio directory",
                code="DIRECTORY_SETUP_ERROR",
                details={"error": str(e)}
            ) 