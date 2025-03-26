from typing import Dict, Any, Tuple
from ..utils.errors import ValidationError
from ..config.text_config import TextConfig
from .base_validator import BaseValidator
import os

class TextValidator(BaseValidator):
    """Validates Text Generation service inputs before API calls"""

    @staticmethod
    def validate_text_params(params: Dict[str, Any]) -> None:
        """Validate text generation parameters."""
        required_params = TextConfig.DEFAULT_PARAMS.keys()
        missing = [param for param in required_params if param not in params]
        invalid = [param for param in params if param not in required_params]
        
        if missing or invalid:
            raise ValidationError(
                message="Invalid text generation parameters",
                code="INVALID_TEXT_PARAMS",
                details={
                    "missing_params": missing,
                    "invalid_params": invalid
                }
            )

    @staticmethod
    def validate_watson_text_params(params: Dict[str, Any]) -> None:
        """
        Validate text generation parameters for IBM Watson API.
        This method handles the IBM Watson-specific parameter names.
        """
        # Check that required parameters are present
        required_params = [
            'decoding_method',
            'max_new_tokens',
            'temperature',
            'top_p',
            'top_k',
            'repetition_penalty'
        ]
        
        missing = []
        for param in required_params:
            # Check for both snake_case and camelCase versions of the parameter
            snake_case = param
            camel_case = ''.join(word.capitalize() if i > 0 else word 
                               for i, word in enumerate(param.split('_')))
            
            if snake_case not in params and camel_case not in params:
                missing.append(param)
        
        if missing:
            raise ValidationError(
                message="Missing required Watson text parameters",
                code="MISSING_WATSON_PARAMS",
                details={"missing_params": missing}
            )
            
        # We don't check for invalid parameters because the Watson API
        # might accept parameters that we don't know about 

    @staticmethod
    def validate_prompt(prompt: str) -> None:
        """Validate text generation prompt"""
        if not isinstance(prompt, str):
            raise ValidationError(
                message="Prompt must be a string",
                code="INVALID_PROMPT_TYPE"
            )
            
        if not prompt or not prompt.strip():
            raise ValidationError(
                message="Prompt cannot be empty",
                code="EMPTY_PROMPT"
            )
            
        if len(prompt) > TextConfig.MAX_PROMPT_LENGTH:
            raise ValidationError(
                message="Prompt exceeds maximum length",
                code="PROMPT_TOO_LONG",
                details={"max_length": TextConfig.MAX_PROMPT_LENGTH}
            )
