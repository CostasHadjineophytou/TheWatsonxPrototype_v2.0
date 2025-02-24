import json
from pathlib import Path
from ..models.errors import LogicError
from ..managers.base_manager import BaseManager

class FileManager(BaseManager):
    """Handles file operations for the application"""
    
    def save_json(self, filename: str, data: dict):
        """Save data to a JSON file"""
        try:
            with open(filename, "w") as f:
                json.dump(data, f)
        except Exception as e:
            self.log_error(LogicError(
                message=f"Failed to save file {filename}",
                code="FILE_SAVE_ERROR",
                details={"error": str(e)}
            ))

    def load_json(self, filename: str) -> dict:
        """Load data from a JSON file"""
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            self.log_error(LogicError(
                message=f"File {filename} not found",
                code="FILE_NOT_FOUND",
                details={"filename": filename}
            ))
            return {}
        except json.JSONDecodeError as e:
            self.log_error(LogicError(
                message=f"Invalid JSON in {filename}",
                code="INVALID_JSON",
                details={"error": str(e)}
            ))
            return {}
        except Exception as e:
            self.log_error(LogicError(
                message=f"Error loading {filename}",
                code="FILE_LOAD_ERROR",
                details={"error": str(e)}
            ))
            return {} 