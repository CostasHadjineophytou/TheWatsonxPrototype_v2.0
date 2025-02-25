from typing import Dict, List
from backend.services.tts_service import TTSService
from ..validators.speech_validator import SpeechValidator
from .base_manager import BaseManager
from ..models.speech_request import TTSRequest
from ..models.responses import TTSResponse

class TTSManager(BaseManager):
    """Business logic for text-to-speech operations"""
    
    def __init__(self, tts_service: TTSService, validator: SpeechValidator):
        super().__init__()
        self.tts_service = tts_service
        self.validator = validator

    def synthesize_speech(self, request: TTSRequest) -> TTSResponse:
        """Process text-to-speech request"""
        try:
            # Validation
            is_valid, error = self.validator.validate(request)
            if not is_valid:
                raise self.handle_validation_error(
                    message=error.message,
                    details=error.details
                )

            # Process request
            try:
                audio_path = self.tts_service.synthesize_text(
                    text=request.text,
                    voice=request.voice,
                    params={
                        'pitch': request.pitch,
                        'speed': request.speed,
                        'accept': request.accept
                    }
                )
            except Exception as e:
                raise self.handle_business_error(
                    message="Speech synthesis failed",
                    code="SYNTHESIS_ERROR",
                    details={"error": str(e)}
                )

            return TTSResponse(
                audio_path=audio_path,
                text=request.text,
                voice=request.voice,
                parameters_used={
                    'pitch': request.pitch,
                    'speed': request.speed,
                    'accept': request.accept
                }
            )

        except Exception as e:
            error = self.handle_unknown_error(e, "Failed to synthesize speech")
            return TTSResponse(
                audio_path="",
                text=request.text,
                voice=request.voice,
                parameters_used={},
                error=error.message
            )

    def get_available_voices(self) -> List[Dict]:
        """Get list of available voices"""
        try:
            return self.tts_service.list_voices()
        except Exception as e:
            error = self.handle_unknown_error(e, "Failed to get voices")
            return [] 