import pytest
from unittest.mock import patch, MagicMock

from backend.services.tts_service import TTSService
from backend.utils.errors import ValidationError, AuthenticationError, APIError, FileError
from backend.utils.ssml_builder import SSMLBuilder
from backend.tests.fixtures.sample_files import SAMPLE_AUDIO_BINARY


class TestTTSService:
    """Tests for the TTSService class"""

    def test_init(self, mock_credentials_manager):
        """Test initializing the TTSService"""
        service = TTSService(mock_credentials_manager)
        assert service.credentials_manager == mock_credentials_manager
        assert service._tts is None

    def test_initialize_success(self, mock_credentials_manager, mock_credentials):
        """Test successful TTS client initialization"""
        mock_credentials_manager.get_service_credentials.return_value = mock_credentials
        
        service = TTSService(mock_credentials_manager)
        service.initialize()
        
        mock_credentials_manager.get_service_credentials.assert_called_once_with("Text to Speech")
        assert service._tts is not None

    def test_initialize_error(self, mock_credentials_manager):
        """Test TTS client initialization failure"""
        mock_credentials_manager.get_service_credentials.side_effect = AuthenticationError(
            "Failed to get credentials", "TTS_INIT_ERROR"
        )
        
        service = TTSService(mock_credentials_manager)
        
        with pytest.raises(AuthenticationError) as exc_info:
            service.initialize()
        
        assert exc_info.value.code == "TTS_INIT_ERROR"
        assert service._tts is None

    @patch('backend.validators.service_validator.ServiceValidator.validate_tts_request')
    @patch('backend.utils.file_manager.FileManager.save_audio_file')
    @patch('backend.utils.ssml_builder.SSMLBuilder.build_prosody')
    def test_synthesize_text_success(self, mock_build_prosody, mock_save_audio, mock_validate, mock_credentials_manager):
        """Test synthesizing text successfully"""
        service = TTSService(mock_credentials_manager)
        
        # Mock TTS client
        mock_tts = MagicMock()
        mock_response = MagicMock()
        mock_response.get_result.return_value.content = SAMPLE_AUDIO_BINARY
        mock_tts.synthesize.return_value = mock_response
        service._tts = mock_tts
        
        # Mock the save_audio_file method
        mock_save_audio.return_value = "data/audio/output_123456.wav"
        
        # Mock SSML builder
        mock_ssml = "<prosody pitch='0%' speed='0%'>This is a test sentence.</prosody>"
        mock_build_prosody.return_value = mock_ssml
        
        # Parameters for synthesis
        text = "This is a test sentence."
        voice = "en-US_AllisonV3Voice"
        params = {
            "pitch": 0,
            "speed": 0
        }
        
        # Call the method
        result = service.synthesize_text(text, voice, params)
        
        # Assertions
        assert result == "data/audio/output_123456.wav"
        mock_validate.assert_called_once_with(text, voice, params)
        mock_build_prosody.assert_called_once_with(text=text, pitch=0, speed=0)
        mock_tts.synthesize.assert_called_once_with(
            text=mock_ssml,
            voice=voice,
            accept='audio/wav'
        )
        mock_save_audio.assert_called_once_with(SAMPLE_AUDIO_BINARY, 'audio/wav')

    def test_synthesize_text_empty_text(self, mock_credentials_manager):
        """Test synthesizing with empty text"""
        service = TTSService(mock_credentials_manager)
        
        with pytest.raises(ValidationError) as exc_info:
            service.synthesize_text("", "en-US_AllisonV3Voice", {})
        
        assert exc_info.value.code == "INVALID_TEXT"  # Changed from EMPTY_TEXT to INVALID_TEXT
        assert service._tts is None

    def test_synthesize_text_empty_voice(self, mock_credentials_manager):
        """Test synthesizing with empty voice"""
        service = TTSService(mock_credentials_manager)
        
        with pytest.raises(ValidationError) as exc_info:
            service.synthesize_text("Test text", "", {})
        
        assert exc_info.value.code == "INVALID_VOICE"
        assert service._tts is None

    @patch('backend.validators.service_validator.ServiceValidator.validate_tts_request')
    def test_synthesize_text_validation_error(self, mock_validate, mock_credentials_manager):
        """Test synthesizing text with validation error"""
        mock_validate.side_effect = ValidationError(
            "Invalid parameters", "INVALID_PARAMS"
        )
        
        service = TTSService(mock_credentials_manager)
        
        with pytest.raises(ValidationError) as exc_info:
            service.synthesize_text("Test text", "en-US_AllisonV3Voice", {"pitch": 200})
        
        assert exc_info.value.code == "INVALID_PARAMS"
        assert service._tts is None

    @patch('backend.validators.service_validator.ServiceValidator.validate_tts_request')
    def test_synthesize_text_auth_error(self, mock_validate, mock_credentials_manager):
        """Test synthesizing text with authentication error"""
        service = TTSService(mock_credentials_manager)
        mock_credentials_manager.get_service_credentials.side_effect = AuthenticationError(
            "Authentication failed", "TTS_INIT_ERROR"
        )
        
        with pytest.raises(AuthenticationError) as exc_info:
            service.synthesize_text("Test text", "en-US_AllisonV3Voice", {})
        
        assert exc_info.value.code == "TTS_INIT_ERROR"
        mock_validate.assert_called_once()

    @patch('backend.validators.service_validator.ServiceValidator.validate_tts_request')
    def test_synthesize_text_api_error(self, mock_validate, mock_credentials_manager):
        """Test synthesizing text with API error"""
        service = TTSService(mock_credentials_manager)
        
        # Mock TTS client
        mock_tts = MagicMock()
        mock_tts.synthesize.side_effect = Exception("API request failed")
        service._tts = mock_tts
        
        with pytest.raises(APIError) as exc_info:
            service.synthesize_text("Test text", "en-US_AllisonV3Voice", {})
        
        assert "API request failed" in str(exc_info.value)
        mock_validate.assert_called_once()

    @patch('backend.validators.service_validator.ServiceValidator.validate_tts_request')
    @patch('backend.utils.file_manager.FileManager.save_audio_file')
    @patch('backend.utils.ssml_builder.SSMLBuilder.build_prosody')
    def test_synthesize_text_file_error(self, mock_build_prosody, mock_save_audio, mock_validate, mock_credentials_manager):
        """Test synthesizing text with file save error"""
        service = TTSService(mock_credentials_manager)
        
        # Mock TTS client
        mock_tts = MagicMock()
        mock_response = MagicMock()
        mock_response.get_result.return_value.content = SAMPLE_AUDIO_BINARY
        mock_tts.synthesize.return_value = mock_response
        service._tts = mock_tts
        
        # Mock SSML builder
        mock_ssml = "<prosody pitch='0%' speed='0%'>Test text</prosody>"
        mock_build_prosody.return_value = mock_ssml
        
        # Mock save_audio_file to raise error
        mock_save_audio.side_effect = FileError(
            "Failed to save audio file", "AUDIO_SAVE_ERROR"
        )
        
        with pytest.raises(FileError) as exc_info:
            service.synthesize_text("Test text", "en-US_AllisonV3Voice", {})
        
        assert exc_info.value.code == "AUDIO_SAVE_ERROR"
        mock_validate.assert_called_once()
        mock_build_prosody.assert_called_once_with(text="Test text", pitch=0, speed=0)
        mock_tts.synthesize.assert_called_once_with(
            text=mock_ssml,
            voice="en-US_AllisonV3Voice",
            accept='audio/wav'
        )

    @patch('backend.validators.service_validator.ServiceValidator.validate_tts_request')
    @patch('backend.utils.file_manager.FileManager.save_audio_file')
    @patch('backend.utils.ssml_builder.SSMLBuilder.build_prosody')
    def test_synthesize_text_with_ssml(self, mock_build_prosody, mock_save_audio, mock_validate, mock_credentials_manager):
        """Test synthesizing text with SSML"""
        service = TTSService(mock_credentials_manager)
        
        # Mock SSML builder
        mock_ssml = "<prosody pitch='20%' rate='10%'>This is a test sentence.</prosody>"
        mock_build_prosody.return_value = mock_ssml
        
        # Mock TTS client
        mock_tts = MagicMock()
        mock_response = MagicMock()
        mock_response.get_result.return_value.content = SAMPLE_AUDIO_BINARY
        mock_tts.synthesize.return_value = mock_response
        service._tts = mock_tts
        
        # Mock save_audio_file
        mock_save_audio.return_value = "data/audio/output_123456.wav"
        
        # Call the method
        text = "This is a test sentence."
        result = service.synthesize_text(text, "en-US_AllisonV3Voice", {
            "pitch": 20,
            "speed": 10
        })
        
        # Assertions
        assert result == "data/audio/output_123456.wav"
        mock_build_prosody.assert_called_once_with(text=text, pitch=20, speed=10)
        mock_tts.synthesize.assert_called_once_with(
            text=mock_ssml,
            voice="en-US_AllisonV3Voice",
            accept='audio/wav'
        )

    def test_list_voices_success(self, mock_credentials_manager):
        """Test getting available voices successfully"""
        service = TTSService(mock_credentials_manager)
        
        # Mock TTS client
        mock_tts = MagicMock()
        mock_voices = {
            "voices": [
                {"name": "en-US_AllisonV3Voice", "language": "en-US", "gender": "female"},
                {"name": "en-US_MichaelV3Voice", "language": "en-US", "gender": "male"}
            ]
        }
        mock_tts.list_voices.return_value.get_result.return_value = mock_voices
        service._tts = mock_tts
        
        # Call the method
        result = service.list_voices()
        
        # Assertions
        assert result == mock_voices["voices"]
        mock_tts.list_voices.assert_called_once()

    def test_list_voices_auth_error(self, mock_credentials_manager):
        """Test getting voices with authentication error"""
        service = TTSService(mock_credentials_manager)
        mock_credentials_manager.get_service_credentials.side_effect = AuthenticationError(
            "Authentication failed", "TTS_INIT_ERROR"
        )
        
        with pytest.raises(AuthenticationError) as exc_info:
            service.list_voices()
        
        assert exc_info.value.code == "TTS_INIT_ERROR"

    def test_list_voices_api_error(self, mock_credentials_manager):
        """Test getting voices with API error"""
        service = TTSService(mock_credentials_manager)
        
        # Mock TTS client
        mock_tts = MagicMock()
        mock_tts.list_voices.side_effect = Exception("API request failed")
        service._tts = mock_tts
        
        with pytest.raises(APIError) as exc_info:
            service.list_voices()
        
        assert "API request failed" in str(exc_info.value)
        mock_tts.list_voices.assert_called_once() 