from typing import Tuple
from ..models.errors import ValidationError
from .base_validator import BaseValidator

class ModelValidator(BaseValidator):
    """Validates model operations"""
    
    def validate(self, model_id: str) -> tuple[bool, ValidationError]:
        """
        Validate model ID
        Returns (is_valid, error_if_any)
        """
        # Check for empty/None
        if not model_id:
            return False, ValidationError(
                message="Model ID is required",
                code="MISSING_MODEL_ID",
                details={"model_id": model_id}
            )
        
        # Check type
        if not isinstance(model_id, str):
            return False, ValidationError(
                message="Model ID must be a string",
                code="INVALID_MODEL_ID_TYPE",
                details={"type": type(model_id).__name__}
            )
        
        # Check format/length if needed
        if len(model_id.strip()) == 0:
            return False, ValidationError(
                message="Model ID cannot be empty string",
                code="EMPTY_MODEL_ID",
                details={"model_id": model_id}
            )
            
        # All validations passed
        return True, None 