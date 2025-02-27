import pytest
from unittest.mock import patch, MagicMock, mock_open

from backend.services.tts_service import TTSService
from backend.utils.errors import ValidationError, AuthenticationError, APIError
from backend.tests.fixtures.sample_responses import TTS_RESPONSE, SAMPLE_AUDIO_BINARY


class TestTTSGeneration:
    """Integration tests for TTS generation flow"""

    @pytest.fixture
    def setup_tts_service(self, mock_credentials_manager):
        """Setup TTS service with mocked dependencies"""
        return TTSService(mock_credentials_manager)

    @patch('backend.services.tts_service.TextToSpeechV1')
    def test_tts_generation_flow(self, mock_tts_v1, setup_tts_service, sample_tts_response):
        """Test the complete TTS generation flow from request to response"""
        # Mock the TTS client response
        mock_tts_instance = MagicMock()
        mock_tts_v1.return_value = mock_tts_instance
        
        # Create a mock result object with content attribute
        mock_result = MagicMock()
        mock_result.content = SAMPLE_AUDIO_BINARY
        mock_tts_instance.synthesize.return_value.get_result.return_value = mock_result
        mock_tts_instance.synthesize.return_value.get_headers.return_value = {'content-type': 'audio/wav'}
        
        # Get the TTS service from fixture
        tts_service = setup_tts_service
        
        # Process text
        text = "Convert this text to speech"
        voice = "en-US_AllisonV3Voice"
        params = {
            'accept': 'audio/wav',
            'pitch': 0,
            'speed': 0
        }
        output_file = "test_output.wav"
        
        # Mock FileManager.save_audio_file to return TTS_RESPONSE
        with patch('backend.services.tts_service.FileManager.save_audio_file', return_value=TTS_RESPONSE):
            # Call the service
            response = tts_service.synthesize_text(text, voice, params)
        
        # Assertions
        assert response == TTS_RESPONSE
        
        # Verify TTS client was called correctly with SSML wrapped text
        expected_ssml = f"<prosody pitch='0%' rate='0%'>{text}</prosody>"
        mock_tts_instance.synthesize.assert_called_once_with(
            text=expected_ssml,
            voice=voice,
            accept='audio/wav'
        )

    @patch('backend.services.tts_service.TextToSpeechV1')
    def test_tts_generation_validation_error(self, mock_tts_v1, setup_tts_service):
        """Test TTS generation with validation error"""
        tts_service = setup_tts_service
        
        # Patch the validator to raise an exception
        with patch.object(tts_service.validator, 'validate_tts_request', side_effect=ValidationError(
            "Invalid text input", "INVALID_TEXT"
        )):
            text = ""  # Invalid text
            voice = "en-US_AllisonV3Voice"
            params = {
                'accept': 'audio/wav',
                'pitch': 0,
                'speed': 0
            }
            
            # Call the service and expect exception
            with pytest.raises(ValidationError) as exc_info:
                tts_service.synthesize_text(text, voice, params)
            
            assert exc_info.value.code == "INVALID_TEXT"
            
            # Verify TTS client was not called
            mock_tts_v1.assert_not_called()

    @patch('backend.services.tts_service.TextToSpeechV1')
    def test_tts_generation_api_error(self, mock_tts_v1, setup_tts_service):
        """Test TTS generation with API error"""
        # Mock the TTS client to raise an API error
        mock_tts_instance = MagicMock()
        mock_tts_v1.return_value = mock_tts_instance
        mock_tts_instance.synthesize.side_effect = Exception("API request failed")
        
        tts_service = setup_tts_service
        
        # Process text
        text = "Test text for API error"
        voice = "en-US_AllisonV3Voice"
        params = {
            'accept': 'audio/wav',
            'pitch': 0,
            'speed': 0
        }
        
        # Call the service and expect exception
        with pytest.raises(APIError) as exc_info:
            tts_service.synthesize_text(text, voice, params)
        
        assert "API request failed" in str(exc_info.value)
        
        # Verify TTS client was called with SSML wrapped text
        expected_ssml = f"<prosody pitch='0%' rate='0%'>{text}</prosody>"
        mock_tts_instance.synthesize.assert_called_once_with(
            text=expected_ssml,
            voice=voice,
            accept='audio/wav'
        ) 