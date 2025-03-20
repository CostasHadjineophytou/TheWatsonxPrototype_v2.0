from typing import Dict, Any, Tuple
from ..utils.errors import ValidationError
from ..config.speech_config import SpeechConfig
from .base_validator import BaseValidator
import os

class TTSValidator(BaseValidator):
    """Validates raw service inputs before API calls"""

    def validate_tts_request(self, text: str, voice: str, params: dict) -> None:
        """Validate TTS request parameters"""
        if not text or len(text) > SpeechConfig.MAX_TEXT_LENGTH:
            raise ValidationError(
                message="Invalid text length",
                code="INVALID_TEXT",
                details={"max_length": SpeechConfig.MAX_TEXT_LENGTH}
            )
            
        if not voice:
            raise ValidationError(
                message="Voice must be specified",
                code="INVALID_VOICE"
            )
            
        # Validate pitch
        pitch = params.get('pitch', 0)
        if not isinstance(pitch, (int, float)) or not (
            SpeechConfig.PITCH_RANGE[0] <= pitch <= SpeechConfig.PITCH_RANGE[1]
        ):
            raise ValidationError(
                message="Invalid pitch value",
                code="INVALID_PITCH",
                details={"range": SpeechConfig.PITCH_RANGE}
            )
            
        # Validate speed
        speed = params.get('speed', 0)
        if not isinstance(speed, (int, float)) or not (
            SpeechConfig.SPEED_RANGE[0] <= speed <= SpeechConfig.SPEED_RANGE[1]
        ):
            raise ValidationError(
                message="Invalid speed value",
                code="INVALID_SPEED",
                details={"range": SpeechConfig.SPEED_RANGE}
            )

