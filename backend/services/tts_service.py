from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from .base_service import BaseService
from ..utils.errors import AuthenticationError, ValidationError

class TTSService(BaseService):
    """Handles Text-to-Speech API interactions"""
    
    def __init__(self, credentials_manager):
        super().__init__()
        self.credentials_manager = credentials_manager
        self._tts = None

    def initialize(self):
        """Initialize TTS client"""
        try:
            credentials = self.credentials_manager.get_service_credentials("Text to Speech")
            authenticator = IAMAuthenticator(credentials['apikey'])
            self._tts = TextToSpeechV1(
                authenticator=authenticator
            )
            self._tts.set_service_url(credentials['url'])
        except Exception as e:
            raise AuthenticationError(
                message="Failed to initialize TTS service",
                code="TTS_INIT_ERROR",
                details={"error": str(e)}
            )

    def synthesize_text(self, text: str, voice: str, params: dict) -> str:
        """Synthesize text to speech"""
        try:
            self.validator.validate_tts_request(text, voice, params)

            if not self._tts:
                self.initialize()

            ssml_text = self._build_ssml(text, params)
            response = self._tts.synthesize(
                text=ssml_text,
                voice=voice,
                accept=params.get('accept', 'audio/wav')
            ).get_result().content

            # Save to file
            audio_path = "data/audio/output.wav"
            with open(audio_path, "wb") as audio_file:
                audio_file.write(response)

            return audio_path

        except ValidationError:
            raise
        except Exception as e:
            raise self.handle_error(e, "Failed to synthesize speech")

    def list_voices(self) -> list:
        """Get available voices"""
        try:
            if not self._tts:
                self.initialize()
                
            return self._tts.list_voices().get_result()['voices']
        except Exception as e:
            raise self.handle_error(e, "Failed to list voices")

    def _build_ssml(self, text: str, params: dict) -> str:
        """Build SSML text with prosody"""
        pitch = params.get('pitch', '0')
        speed = params.get('speed', '0')
        return f"<prosody pitch='{pitch}%' rate='{speed}%'>{text}</prosody>" 