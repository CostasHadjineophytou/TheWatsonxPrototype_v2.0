from typing import Dict, Any, Tuple
from ..utils.errors import ValidationError
from .base_validator import BaseValidator
import os

class ModelValidator(BaseValidator):
    """Validates Model service inputs before API calls"""

    @staticmethod
    def validate_model_id(model_id: str) -> None:
        """Validate model ID format"""
        if not model_id or not isinstance(model_id, str):
            raise ValidationError(
                message="Invalid model ID format",
                code="INVALID_MODEL_ID",
                details={"model_id": model_id}
            )