from typing import Tuple, Optional
from ..models.requests import TextRequest
from ..models.errors import LogicError
from .base_validator import BaseValidator
from backend.config.text_config import TextConfig

class TextValidator(BaseValidator):
    """Validates text generation requests"""
    
    def validate(self, request: TextRequest) -> Tuple[bool, Optional[LogicError]]:
        """
        Validate text generation request parameters
        Args:
            request: Text generation request to validate
        Returns:
            Tuple of (is_valid, error_if_any)
        """
        try:
            # Required fields
            if not request.text.strip():
                return False, self.create_error(
                    message="Please enter some text to generate",
                    code="EMPTY_TEXT",
                    details={"text": request.text}
                )
                
            if not request.model_id:
                return False, self.create_error(
                    message="Please select a model",
                    code="NO_MODEL",
                    details={"model_id": request.model_id}
                )
                
            if not request.project_id:
                return False, self.create_error(
                    message="Please select a project",
                    code="NO_PROJECT",
                    details={"project_id": request.project_id}
                )
            
            # Validate temperature
            if request.temperature is not None:
                rule = TextConfig.get_param_rule('temperature')
                if not rule['min'] <= request.temperature <= rule['max']:
                    return False, self.create_error(
                        message=f"Temperature must be between {rule['min']} and {rule['max']}",
                        code="INVALID_TEMPERATURE",
                        details={"temperature": request.temperature, "limits": rule}
                    )
                    
            # Validate top_p
            if request.top_p is not None:
                rule = TextConfig.get_param_rule('top_p')
                if not rule['min'] <= request.top_p <= rule['max']:
                    return False, self.create_error(
                        message=f"Top P must be between {rule['min']} and {rule['max']}",
                        code="INVALID_TOP_P",
                        details={"top_p": request.top_p, "limits": rule}
                    )
                    
            # Validate top_k
            if request.top_k is not None:
                rule = TextConfig.get_param_rule('top_k')
                if not rule['min'] <= request.top_k <= rule['max']:
                    return False, self.create_error(
                        message=f"Top K must be between {rule['min']} and {rule['max']}",
                        code="INVALID_TOP_K",
                        details={"top_k": request.top_k, "limits": rule}
                    )

            # Validate max_tokens
            if request.max_tokens is not None:
                rule = TextConfig.get_param_rule('max_new_tokens')
                if not rule['min'] <= request.max_tokens <= rule['max']:
                    return False, self.create_error(
                        message=f"Max tokens must be between {rule['min']} and {rule['max']}",
                        code="INVALID_MAX_TOKENS",
                        details={"max_tokens": request.max_tokens, "limits": rule}
                    )

            # Validate min_tokens
            if request.min_tokens is not None:
                rule = TextConfig.get_param_rule('min_new_tokens')
                if not rule['min'] <= request.min_tokens <= rule['max']:
                    return False, self.create_error(
                        message=f"Min tokens must be between {rule['min']} and {rule['max']}",
                        code="INVALID_MIN_TOKENS",
                        details={"min_tokens": request.min_tokens, "limits": rule}
                    )

            # Validate repetition_penalty
            if request.repetition_penalty is not None:
                rule = TextConfig.get_param_rule('repetition_penalty')
                if not rule['min'] <= request.repetition_penalty <= rule['max']:
                    return False, self.create_error(
                        message=f"Repetition penalty must be between {rule['min']} and {rule['max']}",
                        code="INVALID_REPETITION_PENALTY",
                        details={"repetition_penalty": request.repetition_penalty, "limits": rule}
                    )

            # Validate token ranges
            if request.min_tokens is not None and request.max_tokens is not None:
                if request.min_tokens > request.max_tokens:
                    return False, self.create_error(
                        message="Min tokens cannot be greater than max tokens",
                        code="INVALID_TOKEN_RANGE",
                        details={"min": request.min_tokens, "max": request.max_tokens}
                    )
                    
            return True, None
            
        except Exception as e:
            return False, self.create_error(
                message="Validation failed",
                code="VALIDATION_ERROR",
                details={"error": str(e)}
            ) 