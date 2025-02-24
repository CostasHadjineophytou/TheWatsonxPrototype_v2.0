from typing import Tuple, Optional
from logic.models.errors import LogicError
from logic.models.text_request import TextRequest
from backend.config.text_config import TextConfig
from .base_validator import BaseValidator

class TextValidator(BaseValidator):
    """Validates text generation requests"""
    
    @staticmethod
    def validate(request: TextRequest) -> Tuple[bool, Optional[LogicError]]:
        # Basic validation
        if not request.text.strip():
            return False, LogicError(
                message="Please enter some text to generate",
                code="EMPTY_TEXT"
            )
        if not request.model_id:
            return False, LogicError(
                message="Please select a model",
                code="NO_MODEL"
            )
        if not request.project_id:
            return False, LogicError(
                message="Please select a project",
                code="NO_PROJECT"
            )

        # Parameter validation
        if request.temperature < 0 or request.temperature > 1:
            return False, LogicError(
                message="Temperature must be between 0 and 1",
                code="INVALID_TEMPERATURE",
                details={"value": request.temperature}
            )

        if request.max_tokens < TextConfig.DEFAULT_PARAMS["min_new_tokens"] or \
           request.max_tokens > TextConfig.DEFAULT_PARAMS["max_new_tokens"]:
            return False, LogicError(
                message=f"Max tokens must be between {TextConfig.DEFAULT_PARAMS['min_new_tokens']} and {TextConfig.DEFAULT_PARAMS['max_new_tokens']}",
                code="INVALID_MAX_TOKENS",
                details={"value": request.max_tokens}
            )

        if request.min_tokens < 0 or request.min_tokens > request.max_tokens:
            return False, LogicError(
                message="Min tokens must be between 0 and max tokens",
                code="INVALID_MIN_TOKENS",
                details={"value": request.min_tokens, "max": request.max_tokens}
            )

        if request.top_k < 0:
            return False, LogicError(
                message="Top K must be positive",
                code="INVALID_TOP_K",
                details={"value": request.top_k}
            )

        if request.top_p < 0 or request.top_p > 1:
            return False, LogicError(
                message="Top P must be between 0 and 1",
                code="INVALID_TOP_P",
                details={"value": request.top_p}
            )

        if request.repetition_penalty < 1:
            return False, LogicError(
                message="Repetition penalty must be greater than or equal to 1",
                code="INVALID_REPETITION_PENALTY",
                details={"value": request.repetition_penalty}
            )

        # Stop sequences validation
        if request.stop_sequences and not isinstance(request.stop_sequences, list):
            return False, LogicError(
                message="Stop sequences must be a list",
                code="INVALID_STOP_SEQUENCES",
                details={"type": type(request.stop_sequences).__name__}
            )

        return True, None 