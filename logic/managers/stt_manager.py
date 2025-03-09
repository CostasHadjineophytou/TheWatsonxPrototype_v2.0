from typing import Dict
from backend.services.stt_service import STTService
from ..validators.speech_validator import SpeechValidator
from .base_manager import BaseManager
from ..models.requests import STTRequest
from ..models.responses import STTResponse

class STTManager(BaseManager):
    """Business logic for speech-to-text operations"""
    
    def __init__(self, stt_service: STTService, validator: SpeechValidator):
        super().__init__()
        self.stt_service = stt_service
        self.validator = validator

    def transcribe_speech(self, request: STTRequest) -> STTResponse:
        """Process speech-to-text request"""
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
                transcription = self.stt_service.transcribe_audio(
                    file_path=request.audio_path
                )
                
                if not transcription:
                    raise self.handle_business_error(
                        message="No transcription generated",
                        code="EMPTY_TRANSCRIPTION"
                    )
                    
            except Exception as e:
                raise self.handle_business_error(
                    message="Speech transcription failed",
                    code="TRANSCRIPTION_ERROR",
                    details={"error": str(e)}
                )

            return STTResponse(
                text=transcription,
                audio_path=request.audio_path,
                success=True
            )

        except Exception as e:
            error = self.handle_unknown_error(e, "Failed to transcribe speech")
            return STTResponse(
                text="",
                audio_path=request.audio_path,
                error=error.message,
                success=False
            ) 