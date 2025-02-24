from typing import Tuple, Optional
from logic.models.errors import LogicError
from .base_validator import BaseValidator

class ProjectValidator(BaseValidator):
    """Validates project operations"""
    
    @staticmethod
    def validate(project_id: str) -> Tuple[bool, Optional[LogicError]]:
        if not project_id:
            return False, LogicError(
                message="Invalid project ID",
                code="INVALID_PROJECT_ID"
            )
        return True, None 