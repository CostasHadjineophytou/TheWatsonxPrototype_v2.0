from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from .base_service import BaseService
from ..utils.errors import AuthenticationError, ValidationError
import os
import stat
from pathlib import Path
import time
import glob
from ..utils.file_manager import FileManager

class TTSService(BaseService):
    """Handles Text-to-Speech API interactions"""
    
    def __init__(self, credentials_manager):
        super().__init__()
        self.credentials_manager = credentials_manager
        self._tts = None
        self._setup_audio_directory()

    def _setup_audio_directory(self):
        """Ensure audio directory exists with correct permissions"""
        try:
            audio_dir = Path("data/audio")
            audio_dir.mkdir(parents=True, exist_ok=True)
            audio_dir.chmod(0o777)
            
            # Clean up old audio files
            self._cleanup_old_files()
        except Exception as e:
            print(f"Warning: Could not set up audio directory: {e}")

    def _cleanup_old_files(self):
        """Clean up old audio files except the currently playing one"""
        try:
            # Get all wav files in the directory
            audio_files = glob.glob("data/audio/*.wav")
            
            # Keep only the 5 most recent files, delete the rest
            if len(audio_files) > 5:
                # Sort files by modification time
                audio_files.sort(key=lambda x: os.path.getmtime(x))
                
                # Delete older files
                for file in audio_files[:-5]:
                    try:
                        os.remove(file)
                    except:
                        pass  # Ignore errors if file is in use
        except Exception:
            pass  # Ignore cleanup errors

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
        """Raw TTS API call"""
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
            
            return self._save_audio_file(response)
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

    def _build_ssml(self, text: str, params: dict) -> str:
        """Build SSML text with prosody"""
        # Convert integers to strings and ensure they have % symbol
        pitch = f"{params.get('pitch', '0')}%"
        speed = f"{params.get('speed', '0')}%"
        
        # Remove % if already present to avoid double %
        pitch = pitch.replace('%%', '%')
        speed = speed.replace('%%', '%')
        
        return f"<prosody pitch='{pitch}' rate='{speed}'>{text}</prosody>"

    def _save_audio_file(self, audio_content: bytes) -> str:
        """Save audio content to file"""
        timestamp = int(time.time() * 1000)
        final_path = f"data/audio/output_{timestamp}.wav"
        
        try:
            with open(final_path, "wb") as audio_file:
                audio_file.write(audio_content)
            
            # Clean up old files after successful save
            FileManager.cleanup_audio_files()
            
            return final_path
        except Exception as e:
            raise self.handle_error(e, "Failed to save audio file") 