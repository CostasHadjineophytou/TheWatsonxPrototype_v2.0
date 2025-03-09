from typing import Dict, Any
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

    def transcribe_audio(self, file_path: str) -> Dict[str, Any]:
        """
        Process speech-to-text with simple parameters
        
        Args:
            file_path: Path to the audio file to transcribe
            
        Returns:
            Dictionary with transcription results
        """
        # Create STTRequest object from parameters
        request = STTRequest(audio_path=file_path)
        
        # Process the request using the existing method
        response = self.transcribe_speech(request)
        
        # Convert response to dictionary for UI layer
        return {
            "text": response.text,
            "audio_path": response.audio_path,
            "success": response.success,
            "error": response.error if hasattr(response, "error") else None,
            "duration": response.duration if hasattr(response, "duration") else None,
            "word_count": response.word_count if hasattr(response, "word_count") else None
        }

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