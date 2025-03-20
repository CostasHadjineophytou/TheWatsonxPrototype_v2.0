from typing import Dict, Any
from .base_validator import BaseValidator
from ..utils.errors import ValidationError

class ProjectValidator(BaseValidator):
    """Validator for project-related operations"""
    
    @staticmethod
    def validate_project_id(project_id: str) -> None:
        """Validate project ID format"""
        if not project_id or not isinstance(project_id, str):
            raise ValidationError(
                message="Invalid project ID format",
                code="INVALID_PROJECT_ID",
                details={"project_id": project_id}
            )