from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from .base_service import BaseService
from ..utils.errors import AuthenticationError, ValidationError
from ..utils.file_manager import FileManager
from ..utils.ssml_builder import SSMLBuilder
from ..validators.tts_validator import TTSValidator
import logging

class TTSService(BaseService):
    """Handles Text-to-Speech API interactions"""
    
    def __init__(self, credentials_manager, validator=None):
        super().__init__()
        self.credentials_manager = credentials_manager
        self._tts = None

        # Override the base validator with the TTS-specific validator
        # This gives us both common validation methods and TTS-specific ones
        self.validator = validator or TTSValidator()

        FileManager.ensure_audio_directory()

    def initialize(self):
        """Initialize TTS client"""
        try:
            credentials = self.credentials_manager.get_service_credentials("Text to Speech")
            
            # Validate that the required resource exists
            self.validator.validate_resource(
                required_resources=["text-to-speech"],
                api_key=credentials['apikey'],
                show_all_resources=False
            )
            
            # Only initialise if validation passes
            authenticator = IAMAuthenticator(credentials['apikey'])
            self._tts = TextToSpeechV1(authenticator=authenticator)
            self._tts.set_service_url(credentials['url'])
            logging.info("TTS service initialized successfully")
            
        except ValidationError as val_err:
            if hasattr(val_err, 'details') and 'missing_resources' in val_err.details:
                missing = val_err.details['missing_resources']
                raise ValidationError(
                    message=f"Text to Speech service not available. Missing resources: {', '.join(missing)}",
                    code="MISSING_TTS_RESOURCES",
                    details={"missing_resources": missing}
                )
            raise val_err
        except Exception as e:
            raise AuthenticationError(
                message="Failed to initialize TTS service",
                code="TTS_INIT_ERROR",
                details={"error": str(e)}
            )

    def synthesize_text(self, text: str, voice: str, params: dict) -> str:
        """Raw TTS API call"""
        try:
            self.validator.validate_tts_request(text, voice, params)
            
            if not self._tts:
                self.initialize()
            
            audio_format = params.get('accept', 'audio/wav')
            ssml_text = SSMLBuilder.build_prosody(
                text=text,
                pitch=params.get('pitch', 0),
                speed=params.get('speed', 0)
            )
            
            response = self._tts.synthesize(
                text=ssml_text,
                voice=voice,
                accept=audio_format
            ).get_result().content
            
            return FileManager.save_audio_file(response, audio_format)
            
        except ValidationError as e:
            raise e
        except Exception as e:
            raise self.handle_error(e, "TTS synthesis failed")

    def list_voices(self) -> list:
        """Get available voices"""
        try:
            if not self._tts:
                self.initialize()
            return self._tts.list_voices().get_result()['voices']
        except Exception as e:
            raise self.handle_error(e, "Failed to list voices")
 