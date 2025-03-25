from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from .base_service import BaseService
from ..utils.errors import AuthenticationError, ValidationError
from ..utils.file_manager import FileManager
from ..validators.stt_validator import STTValidator
import logging

class STTService(BaseService):
    """Handles Speech-to-Text API interactions"""
    
    def __init__(self, credentials_manager, validator=None):
        # Initialize BaseService (which sets self.validator = BaseValidator())
        super().__init__()
        self.credentials_manager = credentials_manager
        self._stt = None
        
        # Override the base validator with the STT-specific validator
        # This gives us both common validation methods and STT-specific ones
        self.validator = validator or STTValidator()

    def initialize(self):
        """Initialize STT client"""
        try:
            credentials = self.credentials_manager.get_service_credentials("Speech to Text")
            
            # Validate that the required resource exists
            self.validator.validate_resource(
                required_resources=["speech-to-text"],
                api_key=credentials['apikey'],
                show_all_resources=False
            )
            
            # Only initialise if validation passes
            authenticator = IAMAuthenticator(credentials['apikey'])
            self._stt = SpeechToTextV1(
                authenticator=authenticator
            )
            self._stt.set_service_url(credentials['url'])
            logging.info("STT service initialized successfully")
            
        except ValidationError as val_err:
            if hasattr(val_err, 'details') and 'missing_resources' in val_err.details:
                missing = val_err.details['missing_resources']
                raise ValidationError(
                    message=f"Speech to Text service not available. Missing resources: {', '.join(missing)}",
                    code="MISSING_STT_RESOURCES",
                    details={"missing_resources": missing}
                )
            raise val_err
        except Exception as e:
            raise AuthenticationError(
                message="Failed to initialize STT service",
                code="STT_INIT_ERROR",
                details={"error": str(e)}
            )

    def get_available_models(self):
        """Get list of available STT models"""
        if not self._stt:
            self.initialize()
        
        try:
            response = self._stt.list_models().get_result()
            return [model['name'] for model in response['models']]
        except Exception as e:
            raise ValidationError(
                message="Failed to retrieve STT models",
                code="MODEL_LIST_ERROR",
                details={"error": str(e)}
            )

    def transcribe_audio(self, file_path: str, model: str = None) -> str:
        """
        Transcribe audio to text
        
        Args:
            file_path: Path to audio file
            model: STT model to use (optional)
        
        Returns:
            Transcription text
        """
        try:
            # Use the STT-specific validator
            self.validator.validate_audio_file(file_path)

            if not self._stt:
                self.initialize()
            
            # Set up parameters for recognition
            params = {
                'audio': None,
                'content_type': 'audio/wav'
            }
            
            # Add model if specified
            if model:
                params['model'] = model
            
            with open(file_path, 'rb') as audio_file:
                params['audio'] = audio_file
                response = self._stt.recognize(**params).get_result()

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