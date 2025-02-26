from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from .base_service import BaseService
from ..utils.errors import AuthenticationError, ValidationError
from ..utils.file_manager import FileManager
from ..validators.service_validator import ServiceValidator

class STTService(BaseService):
    """Handles Speech-to-Text API interactions"""
    
    def __init__(self, credentials_manager):
        super().__init__()
        self.credentials_manager = credentials_manager
        self._stt = None
        self.validator = ServiceValidator()

    def initialize(self):
        """Initialize STT client"""
        try:
            credentials = self.credentials_manager.get_service_credentials("Speech to Text")
            authenticator = IAMAuthenticator(credentials['apikey'])
            self._stt = SpeechToTextV1(
                authenticator=authenticator
            )
            self._stt.set_service_url(credentials['url'])
        except Exception as e:
            raise AuthenticationError(
                message="Failed to initialize STT service",
                code="STT_INIT_ERROR",
                details={"error": str(e)}
            )

    def transcribe_audio(self, file_path: str) -> str:
        """Transcribe audio to text"""
        try:
            self.validator.validate_audio_file(file_path)

            if not self._stt:
                self.initialize()
            
            with open(file_path, 'rb') as audio_file:
                response = self._stt.recognize(
                    audio=audio_file,
                    content_type='audio/wav'
                ).get_result()

            return self._extract_transcription(response)

        except ValidationError:
            raise
        except Exception as e:
            raise self.handle_error(e, "Failed to transcribe audio")

    def _extract_transcription(self, response: dict) -> str:
        """Extract transcription text from response"""
        try:
            transcriptions = response['results']
            return " ".join([
                result['alternatives'][0]['transcript'] 
                for result in transcriptions
            ])
        except Exception as e:
            raise self.handle_error(e, "Failed to extract transcription") 