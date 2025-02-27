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
        self.service = tts_service
        self.validator = validator

    def synthesize_speech(self, request: TTSRequest) -> TTSResponse:
        """Handle TTS request and response"""
        try:
            # Validation
            is_valid, error = self.validator.validate_tts_request(request)
            if not is_valid:
                return TTSResponse(audio_path="", error=error.message)

            # Process request
            audio_path = self.service.synthesize_text(
                request.text,
                request.voice,
                {
                    'pitch': request.pitch,
                    'speed': request.speed,
                    'accept': request.accept
                }
            )
            return TTSResponse(audio_path=audio_path)
        except Exception as e:
            return TTSResponse(audio_path="", error=str(e))

    def get_available_voices(self) -> List[Dict]:
        """Get list of available voices"""
        try:
            return self.service.list_voices()
        except Exception as e:
            error = self.handle_unknown_error(e, "Failed to get voices")
            return [] 