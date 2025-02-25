from typing import Tuple, Optional
from .base_validator import BaseValidator
from ..models.errors import LogicError

class ModelValidator(BaseValidator):
    """Validates model operations"""
    
    def validate(self, model_id: str) -> Tuple[bool, Optional[LogicError]]:
        """
        Validate model ID
        Args:
            model_id: ID to validate
        Returns:
            Tuple of (is_valid, error_if_any)
        """
        if not model_id:
            return False, self.create_error(
                message="Model ID is required",
                code="MISSING_MODEL_ID",
                details={"model_id": model_id}
            )
        
        if not isinstance(model_id, str):
            return False, self.create_error(
                message="Model ID must be a string",
                code="INVALID_MODEL_ID_TYPE",
                details={"type": type(model_id).__name__}
            )
            
        return True, None 