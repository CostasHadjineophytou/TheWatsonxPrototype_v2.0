import os
from typing import Tuple, Optional
from .base_validator import BaseValidator
from ..models.errors import LogicError
from ..models.speech_request import TTSRequest, STTRequest
from backend.config.speech_config import SpeechConfig

class SpeechValidator(BaseValidator):
    """Validates speech service requests"""
    
    def validate(self, request) -> Tuple[bool, Optional[LogicError]]:
        """Validate request based on type"""
        if isinstance(request, TTSRequest):
            return self.validate_tts_request(request)
        elif isinstance(request, STTRequest):
            return self.validate_stt_request(request)
        else:
            return False, self.create_error(
                message="Invalid request type",
                code="INVALID_REQUEST_TYPE",
                details={"type": type(request).__name__}
            )

    def validate_tts_request(self, request: TTSRequest) -> Tuple[bool, Optional[LogicError]]:
        """Validate TTS request parameters"""
        # Check text
        if not request.text or not request.text.strip():
            return False, self.create_error(
                message="Text is required",
                code="EMPTY_TEXT"
            )
            
        if len(request.text) > SpeechConfig.MAX_TEXT_LENGTH:
            return False, self.create_error(
                message=f"Text exceeds maximum length of {SpeechConfig.MAX_TEXT_LENGTH} characters",
                code="TEXT_TOO_LONG",
                details={"length": len(request.text)}
            )

        # Check pitch
        if not SpeechConfig.TTS_PARAMS["pitch"]["min"] <= request.pitch <= SpeechConfig.TTS_PARAMS["pitch"]["max"]:
            return False, self.create_error(
                message="Invalid pitch value",
                code="INVALID_PITCH",
                details={
                    "value": request.pitch,
                    "allowed_range": f"{SpeechConfig.TTS_PARAMS['pitch']['min']} to {SpeechConfig.TTS_PARAMS['pitch']['max']}"
                }
            )

        # Check speed
        if not SpeechConfig.TTS_PARAMS["speed"]["min"] <= request.speed <= SpeechConfig.TTS_PARAMS["speed"]["max"]:
            return False, self.create_error(
                message="Invalid speed value",
                code="INVALID_SPEED",
                details={
                    "value": request.speed,
                    "allowed_range": f"{SpeechConfig.TTS_PARAMS['speed']['min']} to {SpeechConfig.TTS_PARAMS['speed']['max']}"
                }
            )

        # Check accept format
        if request.accept not in SpeechConfig.TTS_PARAMS["accept"]["options"]:
            return False, self.create_error(
                message="Invalid audio format",
                code="INVALID_FORMAT",
                details={
                    "format": request.accept,
                    "allowed_formats": SpeechConfig.TTS_PARAMS["accept"]["options"]
                }
            )

        return True, None

    def validate_stt_request(self, request: STTRequest) -> Tuple[bool, Optional[LogicError]]:
        """Validate STT request parameters"""
        if not request.audio_path:
            return False, self.create_error(
                message="Audio file path is required",
                code="NO_AUDIO_PATH"
            )

        if not os.path.exists(request.audio_path):
            return False, self.create_error(
                message="Audio file not found",
                code="FILE_NOT_FOUND",
                details={"path": request.audio_path}
            )

        file_extension = os.path.splitext(request.audio_path)[1].lower()
        if file_extension not in SpeechConfig.SUPPORTED_AUDIO_FORMATS:
            return False, self.create_error(
                message="Unsupported audio format",
                code="UNSUPPORTED_FORMAT",
                details={
                    "format": file_extension,
                    "supported_formats": SpeechConfig.SUPPORTED_AUDIO_FORMATS
                }
            )

        try:
            file_size = os.path.getsize(request.audio_path)
            if file_size > SpeechConfig.MAX_AUDIO_SIZE:
                return False, self.create_error(
                    message=f"Audio file exceeds maximum size of {SpeechConfig.MAX_AUDIO_SIZE/1024/1024:.1f}MB",
                    code="FILE_TOO_LARGE",
                    details={
                        "size": file_size,
                        "max_size": SpeechConfig.MAX_AUDIO_SIZE
                    }
                )
        except OSError:
            return False, self.create_error(
                message="Cannot access audio file",
                code="FILE_ACCESS_ERROR",
                details={"path": request.audio_path}
            )

        return True, None 