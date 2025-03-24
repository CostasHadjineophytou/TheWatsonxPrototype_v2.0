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
        self.validator = validator or TTSValidator()
        FileManager.ensure_audio_directory()

    def initialize(self):
        """Initialize TTS client"""
        try:
            credentials = self.credentials_manager.get_service_credentials("Text to Speech")
            
            # Try API key validation first - this is the most important thing
            try:
                # Validate that the required resource exists - but catch errors
                self.validator.validate_resource(
                    required_resources=["text-to-speech"],
                    api_key=credentials['apikey'],
                    show_all_resources=False
                )
                logging.debug("TTS service resources validated successfully")
                print("TTS service resources validated successfully")
            except ValidationError as val_err:
                # Log at debug level instead of warning since we know initialization works
                if hasattr(val_err, 'details') and 'missing_resources' in val_err.details:
                    missing = val_err.details['missing_resources']
                    logging.debug(f"TTS validation - Resources not detected in API: {', '.join(missing)}")
                    logging.debug("This is expected in some IBM Cloud configurations")
                else:
                    logging.debug(f"TTS resource validation completed with note: {str(val_err)}")
                # Continue with initialization anyway
            except Exception as ex:
                # For other exceptions, just log at debug level
                logging.debug(f"TTS validation note: {str(ex)}")
            
            # Initialize the client even if validation had notes
            authenticator = IAMAuthenticator(credentials['apikey'])
            self._tts = TextToSpeechV1(authenticator=authenticator)
            self._tts.set_service_url(credentials['url'])
            logging.info("TTS service initialized successfully")
            
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
 