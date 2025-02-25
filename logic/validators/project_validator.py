from typing import Tuple, Optional
from logic.models.errors import LogicError
from .base_validator import BaseValidator
from ..models.errors import ValidationError

class ProjectValidator(BaseValidator):
    """Validates project operations"""
    
    def validate(self, project_id: str) -> tuple[bool, ValidationError]:
        """Validate project ID"""
        if not project_id:
            return False, ValidationError(
                message="Project ID is required",
                code="MISSING_PROJECT_ID",
                details={"project_id": project_id}
            )
            
        if not isinstance(project_id, str):
            return False, ValidationError(
                message="Project ID must be a string",
                code="INVALID_PROJECT_ID_TYPE",
                details={"type": type(project_id).__name__}
            )
            
        return True, None 