from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from .base_service import BaseService
from ..utils.errors import AuthenticationError
from ..utils.file_manager import FileManager
from ..utils.ssml_builder import SSMLBuilder

class TTSService(BaseService):
    """Handles Text-to-Speech API interactions"""
    
    def __init__(self, credentials_manager):
        super().__init__()
        self.credentials_manager = credentials_manager
        self._tts = None
        FileManager.ensure_audio_directory()

    def initialize(self):
        """Initialize TTS client"""
        try:
            credentials = self.credentials_manager.get_service_credentials("Text to Speech")
            authenticator = IAMAuthenticator(credentials['apikey'])
            self._tts = TextToSpeechV1(authenticator=authenticator)
            self._tts.set_service_url(credentials['url'])
        except Exception as e:
            raise AuthenticationError(
                message="Failed to initialize TTS service",
                code="TTS_INIT_ERROR",
                details={"error": str(e)}
            )

    def synthesize_text(self, text: str, voice: str, params: dict) -> str:
        """Raw TTS API call"""
        try:
            if not self._tts:
                self.initialize()
            
            ssml_text = SSMLBuilder.build_prosody(
                text=text,
                pitch=params.get('pitch', 0),
                speed=params.get('speed', 0)
            )
            
            response = self._tts.synthesize(
                text=ssml_text,
                voice=voice,
                accept=params.get('accept', 'audio/wav')
            ).get_result().content
            
            return FileManager.save_audio_file(response)
            
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
 