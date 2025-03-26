from typing import Dict, Any, Tuple
from ..utils.errors import ValidationError, AuthenticationError
from ..config.speech_config import SpeechConfig
from .base_validator import BaseValidator
import os

class STTValidator(BaseValidator):
    """Validates Speech-to-Text service inputs before API calls"""

    @staticmethod
    def validate_audio_file(file_path: str) -> None:
        """Service-level validation"""
        # Technical validation
        if not os.path.exists(file_path):
            raise ValidationError(
                message="Audio file not found",
                code="FILE_NOT_FOUND"
            )

        # API-specific validation
        file_size = os.path.getsize(file_path)
        if file_size > SpeechConfig.MAX_AUDIO_SIZE:
            raise ValidationError(
                message="File too large for API",
                code="FILE_TOO_LARGE"
            )
