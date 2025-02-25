from typing import Tuple
from ..models.text_request import TextRequest
from ..models.errors import ValidationError
from backend.config.text_config import TextConfig
from .base_validator import BaseValidator

class TextValidator(BaseValidator):
    """Validates text generation requests"""
    
    def validate(self, request: TextRequest) -> tuple[bool, ValidationError]:
        """
        Validate text generation request parameters
        Returns (is_valid, error_if_any)
        """
        try:
            # Required fields
            if not request.text.strip():
                return False, ValidationError(
                    message="Please enter some text to generate",
                    code="EMPTY_TEXT",
                    details={"text": request.text}
                )
                
            if not request.model_id:
                return False, ValidationError(
                    message="Please select a model",
                    code="NO_MODEL",
                    details={"model_id": request.model_id}
                )
                
            if not request.project_id:
                return False, ValidationError(
                    message="Please select a project",
                    code="NO_PROJECT",
                    details={"project_id": request.project_id}
                )
            
            # Parameter validations
            if request.temperature is not None:
                if not 0 <= request.temperature <= 2:
                    return False, ValidationError(
                        message="Temperature must be between 0 and 2",
                        code="INVALID_TEMPERATURE",
                        details={"temperature": request.temperature}
                    )
                    
            if request.max_tokens is not None:
                if request.max_tokens < 1:
                    return False, ValidationError(
                        message="Max tokens must be positive",
                        code="INVALID_MAX_TOKENS",
                        details={"max_tokens": request.max_tokens}
                    )
                    
            if request.min_tokens is not None:
                if request.min_tokens < 0:
                    return False, ValidationError(
                        message="Min tokens cannot be negative",
                        code="INVALID_MIN_TOKENS",
                        details={"min_tokens": request.min_tokens}
                    )
                if request.max_tokens and request.min_tokens > request.max_tokens:
                    return False, ValidationError(
                        message="Min tokens cannot be greater than max tokens",
                        code="INVALID_TOKEN_RANGE",
                        details={"min": request.min_tokens, "max": request.max_tokens}
                    )
                    
            return True, None
            
        except Exception as e:
            return False, ValidationError(
                message="Validation failed",
                code="VALIDATION_ERROR",
                details={"error": str(e)}
            ) 