import json
import logging
from pathlib import Path
from .errors import ConfigurationError

class FileManager:
    """Handles file operations for the application"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
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