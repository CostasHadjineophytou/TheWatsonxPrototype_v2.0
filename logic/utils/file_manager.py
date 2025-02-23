import json
import logging
from pathlib import Path

class FileManager:
    """Handles file operations for the application"""
    
    def save_json(self, filename: str, data: dict):
        """Save data to a JSON file"""
        try:
            with open(filename, "w") as f:
                json.dump(data, f)
        except Exception as e:
            logging.error(f"Error saving to {filename}: {e}")
            raise RuntimeError(f"Failed to save file {filename}: {str(e)}")

    def load_json(self, filename: str) -> dict:
        """Load data from a JSON file"""
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading {filename}: {e}")
            return {} 