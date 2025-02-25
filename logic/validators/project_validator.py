from typing import Tuple, Optional
from .base_validator import BaseValidator
from ..models.errors import LogicError

class ProjectValidator(BaseValidator):
    """Validates project operations"""
    
    def validate(self, project_id: str) -> Tuple[bool, Optional[LogicError]]:
        """
        Validate project ID
        Args:
            project_id: ID to validate
        Returns:
            Tuple of (is_valid, error_if_any)
        """
        if not project_id:
            return False, self.create_error(
                message="Project ID is required",
                code="MISSING_PROJECT_ID",
                details={"project_id": project_id}
            )
        
        if not isinstance(project_id, str):
            return False, self.create_error(
                message="Project ID must be a string",
                code="INVALID_PROJECT_ID_TYPE",
                details={"type": type(project_id).__name__}
            )
            
        if len(project_id.strip()) == 0:
            return False, self.create_error(
                message="Project ID cannot be empty",
                code="EMPTY_PROJECT_ID",
                details={"project_id": project_id}
            )
            
        return True, None 