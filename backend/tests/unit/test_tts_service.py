import pytest
from unittest.mock import patch, MagicMock, call, mock_open
import os

from backend.services.tts_service import TTSService
from backend.utils.errors import ValidationError, AuthenticationError, APIError, FileError
from backend.utils.ssml_builder import SSMLBuilder


class TestTTSService:
    """Tests for the TTSService class"""

    def test_init(self, mock_watson_client):
        """Test initializing the TTSService"""
        service = TTSService(mock_watson_client)
        assert service.client == mock_watson_client

    @patch('backend.validators.service_validator.ServiceValidator.validate_tts_params')
    @patch('backend.utils.file_manager.FileManager.save_audio_file')
    def test_synthesize_text_success(self, mock_save_audio, mock_validate, mock_watson_client):
        """Test synthesizing text successfully"""
        # Mock the client's post_request method
        mock_audio_content = b"mock audio data"
        mock_watson_client.post_request.return_value = mock_audio_content
        
        # Mock the save_audio_file method
        mock_save_audio.return_value = "data/audio/output_123456.wav"
        
        # Create the service
        service = TTSService(mock_watson_client)
        
        # Parameters for synthesis
        text = "This is a test sentence for speech synthesis."
        voice = "en-US_AllisonV3Voice"
        params = {
            "rate": 0,
            "pitch": 0
        }
        
        # Call the method
        result = service.synthesize_text(text, voice, params)
        
        # Assertions
        assert result == "data/audio/output_123456.wav"
        mock_validate.assert_called_once()
        mock_watson_client.post_request.assert_called_once()
        # Check that the first argument to post_request is the correct endpoint
        args, _ = mock_watson_client.post_request.call_args
        assert args[0] == '/v1/synthesize'
        # Check that the payload contains the expected data
        _, kwargs = mock_watson_client.post_request.call_args
        assert kwargs['json']['text'] == text
        assert kwargs['json']['voice'] == voice
        assert kwargs['json']['accept'] == 'audio/wav'
        # Check that the audio content was saved
        mock_save_audio.assert_called_once_with(mock_audio_content, 'audio/wav')

    def test_synthesize_text_empty_text(self, mock_watson_client):
        """Test synthesizing with empty text"""
        # Create the service
        service = TTSService(mock_watson_client)
        
        # Call the method with empty text and expect exception
        with pytest.raises(ValidationError) as exc_info:
            service.synthesize_text("", "en-US_AllisonV3Voice")
        
        assert exc_info.value.code == "INVALID_TEXT"
        mock_watson_client.post_request.assert_not_called()

    def test_synthesize_text_empty_voice(self, mock_watson_client):
        """Test synthesizing with empty voice"""
        # Create the service
        service = TTSService(mock_watson_client)
        
        # Call the method with empty voice and expect exception
        with pytest.raises(ValidationError) as exc_info:
            service.synthesize_text("Test text", "")
        
        assert exc_info.value.code == "INVALID_VOICE"
        mock_watson_client.post_request.assert_not_called()

    @patch('backend.validators.service_validator.ServiceValidator.validate_tts_params')
    def test_synthesize_text_validation_error(self, mock_validate, mock_watson_client):
        """Test synthesizing text with validation error"""
        # Mock the validator to raise a validation error
        mock_validate.side_effect = ValidationError(
            "Invalid parameters", "INVALID_PARAMS"
        )
        
        # Create the service
        service = TTSService(mock_watson_client)
        
        # Call the method and expect exception
        with pytest.raises(ValidationError) as exc_info:
            service.synthesize_text("Test text", "en-US_AllisonV3Voice", {"rate": 200})  # Invalid rate
        
        assert exc_info.value.code == "INVALID_PARAMS"
        mock_watson_client.post_request.assert_not_called()

    @patch('backend.validators.service_validator.ServiceValidator.validate_tts_params')
    def test_synthesize_text_auth_error(self, mock_validate, mock_watson_client):
        """Test synthesizing text with authentication error"""
        # Mock the client to raise an authentication error
        mock_watson_client.post_request.side_effect = AuthenticationError(
            "Authentication failed", "AUTHENTICATION_ERROR"
        )
        
        # Create the service
        service = TTSService(mock_watson_client)
        
        # Call the method and expect exception
        with pytest.raises(AuthenticationError) as exc_info:
            service.synthesize_text("Test text", "en-US_AllisonV3Voice")
        
        assert exc_info.value.code == "AUTHENTICATION_ERROR"
        mock_validate.assert_called_once()

    @patch('backend.validators.service_validator.ServiceValidator.validate_tts_params')
    def test_synthesize_text_api_error(self, mock_validate, mock_watson_client):
        """Test synthesizing text with API error"""
        # Mock the client to raise an API error
        mock_watson_client.post_request.side_effect = APIError(
            "API request failed", "API_ERROR"
        )
        
        # Create the service
        service = TTSService(mock_watson_client)
        
        # Call the method and expect exception
        with pytest.raises(APIError) as exc_info:
            service.synthesize_text("Test text", "en-US_AllisonV3Voice")
        
        assert exc_info.value.code == "API_ERROR"
        mock_validate.assert_called_once()

    @patch('backend.validators.service_validator.ServiceValidator.validate_tts_params')
    @patch('backend.utils.file_manager.FileManager.save_audio_file')
    def test_synthesize_text_file_error(self, mock_save_audio, mock_validate, mock_watson_client):
        """Test synthesizing text with file save error"""
        # Mock the client's post_request method
        mock_audio_content = b"mock audio data"
        mock_watson_client.post_request.return_value = mock_audio_content
        
        # Mock the save_audio_file method to raise an error
        mock_save_audio.side_effect = FileError(
            "Failed to save audio file", "AUDIO_SAVE_ERROR"
        )
        
        # Create the service
        service = TTSService(mock_watson_client)
        
        # Call the method and expect exception
        with pytest.raises(FileError) as exc_info:
            service.synthesize_text("Test text", "en-US_AllisonV3Voice")
        
        assert exc_info.value.code == "AUDIO_SAVE_ERROR"
        mock_validate.assert_called_once()
        mock_watson_client.post_request.assert_called_once()

    @patch('backend.validators.service_validator.ServiceValidator.validate_tts_params')
    @patch('backend.utils.file_manager.FileManager.save_audio_file')
    @patch('backend.utils.ssml_builder.SSMLBuilder.build_prosody')
    def test_synthesize_text_with_ssml(self, mock_build_prosody, mock_save_audio, mock_validate, mock_watson_client):
        """Test synthesizing text with SSML"""
        # Mock the SSML builder
        mock_ssml = "<prosody pitch='20%' rate='10%'>This is a test sentence for speech synthesis.</prosody>"
        mock_build_prosody.return_value = mock_ssml
        
        # Mock the client's post_request method
        mock_audio_content = b"mock audio data"
        mock_watson_client.post_request.return_value = mock_audio_content
        
        # Mock the save_audio_file method
        mock_save_audio.return_value = "data/audio/output_123456.wav"
        
        # Create the service
        service = TTSService(mock_watson_client)
        
        # Parameters for synthesis
        text = "This is a test sentence for speech synthesis."
        voice = "en-US_AllisonV3Voice"
        params = {
            "rate": 10,
            "pitch": 20
        }
        
        # Call the method
        result = service.synthesize_text(text, voice, params)
        
        # Assertions
        assert result == "data/audio/output_123456.wav"
        mock_build_prosody.assert_called_once_with(text, pitch=20, speed=10)
        mock_validate.assert_called_once()
        mock_watson_client.post_request.assert_called_once()
        # Check that the payload contains the SSML
        _, kwargs = mock_watson_client.post_request.call_args
        assert kwargs['json']['text'] == mock_ssml

    @patch('backend.validators.service_validator.ServiceValidator.validate_tts_params')
    @patch('backend.utils.file_manager.FileManager.save_audio_file')
    def test_synthesize_text_with_different_format(self, mock_save_audio, mock_validate, mock_watson_client):
        """Test synthesizing text with different audio format"""
        # Mock the client's post_request method
        mock_audio_content = b"mock audio data"
        mock_watson_client.post_request.return_value = mock_audio_content
        
        # Mock the save_audio_file method
        mock_save_audio.return_value = "data/audio/output_123456.mp3"
        
        # Create the service
        service = TTSService(mock_watson_client)
        
        # Parameters for synthesis
        text = "This is a test sentence for speech synthesis."
        voice = "en-US_AllisonV3Voice"
        params = {
            "format": "audio/mp3"
        }
        
        # Call the method
        result = service.synthesize_text(text, voice, params)
        
        # Assertions
        assert result == "data/audio/output_123456.mp3"
        mock_validate.assert_called_once()
        mock_watson_client.post_request.assert_called_once()
        # Check that the payload contains the correct format
        _, kwargs = mock_watson_client.post_request.call_args
        assert kwargs['json']['accept'] == 'audio/mp3'
        # Check that the audio content was saved with the correct format
        mock_save_audio.assert_called_once_with(mock_audio_content, 'audio/mp3')

    @patch('backend.services.tts_service.TTSService.get_voices')
    def test_get_voice_by_language_success(self, mock_get_voices, mock_watson_client):
        """Test getting voice by language successfully"""
        # Mock the get_voices method
        mock_voices = [
            {"name": "en-US_AllisonV3Voice", "language": "en-US", "gender": "female"},
            {"name": "en-US_MichaelV3Voice", "language": "en-US", "gender": "male"},
            {"name": "de-DE_BirgitV3Voice", "language": "de-DE", "gender": "female"}
        ]
        mock_get_voices.return_value = mock_voices
        
        # Create the service
        service = TTSService(mock_watson_client)
        
        # Call the method
        result = service.get_voice_by_language("en-US")
        
        # Assertions
        assert len(result) == 2
        assert all(voice["language"] == "en-US" for voice in result)
        mock_get_voices.assert_called_once()

    @patch('backend.services.tts_service.TTSService.get_voices')
    def test_get_voice_by_language_no_match(self, mock_get_voices, mock_watson_client):
        """Test getting voice by language with no match"""
        # Mock the get_voices method
        mock_voices = [
            {"name": "en-US_AllisonV3Voice", "language": "en-US", "gender": "female"},
            {"name": "en-US_MichaelV3Voice", "language": "en-US", "gender": "male"},
            {"name": "de-DE_BirgitV3Voice", "language": "de-DE", "gender": "female"}
        ]
        mock_get_voices.return_value = mock_voices
        
        # Create the service
        service = TTSService(mock_watson_client)
        
        # Call the method
        result = service.get_voice_by_language("fr-FR")
        
        # Assertions
        assert len(result) == 0
        mock_get_voices.assert_called_once()

    def test_get_voices_success(self, mock_watson_client):
        """Test getting available voices successfully"""
        # Mock the client's get_request method
        mock_response = {
            "voices": [
                {"name": "en-US_AllisonV3Voice", "language": "en-US", "gender": "female"},
                {"name": "en-US_MichaelV3Voice", "language": "en-US", "gender": "male"},
                {"name": "de-DE_BirgitV3Voice", "language": "de-DE", "gender": "female"}
            ]
        }
        mock_watson_client.get_request.return_value = mock_response
        
        # Create the service
        service = TTSService(mock_watson_client)
        
        # Call the method
        result = service.get_voices()
        
        # Assertions
        assert result == mock_response["voices"]
        mock_watson_client.get_request.assert_called_once_with('/v1/voices')

    def test_get_voices_auth_error(self, mock_watson_client):
        """Test getting voices with authentication error"""
        # Mock the client to raise an authentication error
        mock_watson_client.get_request.side_effect = AuthenticationError(
            "Authentication failed", "AUTHENTICATION_ERROR"
        )
        
        # Create the service
        service = TTSService(mock_watson_client)
        
        # Call the method and expect exception
        with pytest.raises(AuthenticationError) as exc_info:
            service.get_voices()
        
        assert exc_info.value.code == "AUTHENTICATION_ERROR"
        mock_watson_client.get_request.assert_called_once_with('/v1/voices')

    def test_get_voices_api_error(self, mock_watson_client):
        """Test getting voices with API error"""
        # Mock the client to raise an API error
        mock_watson_client.get_request.side_effect = APIError(
            "API request failed", "API_ERROR"
        )
        
        # Create the service
        service = TTSService(mock_watson_client)
        
        # Call the method and expect exception
        with pytest.raises(APIError) as exc_info:
            service.get_voices()
        
        assert exc_info.value.code == "API_ERROR"
        mock_watson_client.get_request.assert_called_once_with('/v1/voices') 