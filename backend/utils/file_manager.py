import os
import json
import logging
import stat
from pathlib import Path
from .errors import ConfigurationError

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
                # Set directory permissions
                path.chmod(0o777)
                
                # Set permissions for any existing files
                for file in path.glob('*'):
                    if file.is_file():
                        file.chmod(0o666)
            except Exception as e:
                print(f"Warning: Could not set permissions for {directory}: {e}")
    
    @staticmethod
    def save_json(filepath: str, data: dict):
        """Save data as JSON file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def load_json(filepath: str) -> dict:
        """Load data from JSON file"""
        if not os.path.exists(filepath):
            return {}
        with open(filepath, 'r') as f:
            return json.load(f)

    def save_json(self, filename: str, data: dict):
        """Save data to a JSON file"""
        try:
            # Ensure directory exists
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filename, "w") as f:
                json.dump(data, f)
        except Exception as e:
            self.logger.error(
                f"Failed to save file {filename}",
                extra={"error": str(e)}
            )
            raise ConfigurationError(
                message=f"Failed to save file {filename}",
                code="FILE_SAVE_ERROR",
                details={"error": str(e)}
            )

    def load_json(self, filename: str) -> dict:
        """Load data from a JSON file"""
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error(f"File {filename} not found")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(
                f"Invalid JSON in {filename}",
                extra={"error": str(e)}
            )
            return {}
        except Exception as e:
            self.logger.error(
                f"Error loading {filename}",
                extra={"error": str(e)}
            )
            return {} 