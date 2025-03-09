import pytest
from unittest.mock import patch, MagicMock, mock_open

from backend.services.stt_service import STTService
from backend.utils.errors import ValidationError, AuthenticationError, APIError
from backend.tests.fixtures.sample_responses import STT_RESPONSE


class TestSTTTranscription:
    """Integration tests for STT transcription flow"""

    @pytest.fixture
    def setup_stt_service(self, mock_credentials_manager):
        """Setup STT service with mocked dependencies"""
        return STTService(mock_credentials_manager)

    @patch('backend.services.stt_service.SpeechToTextV1')
    def test_stt_transcription_flow(self, mock_stt_v1, setup_stt_service, sample_stt_response):
        """Test the complete STT transcription flow from request to response"""
        # Mock the STT client response
        mock_stt_instance = MagicMock()
        mock_stt_v1.return_value = mock_stt_instance
        mock_stt_instance.recognize.return_value.get_result.return_value = STT_RESPONSE
        
        # Get the STT service from fixture
        stt_service = setup_stt_service
        
        # Test file path
        audio_file = "test_audio.wav"
        
        # Mock file operations
        mock_file = mock_open(read_data=b'mock audio data')
        with patch('builtins.open', mock_file), \
             patch('os.path.exists', return_value=True), \
             patch('os.path.getsize', return_value=1024):  # Mock 1KB file size
            # Call the service
            result = stt_service.transcribe_audio(audio_file)
        
        # Assertions
        assert result == "This is a sample transcription of speech to text."
        
        # Verify STT client was called correctly
        mock_stt_instance.recognize.assert_called_once_with(
            audio=mock_file(),
            content_type='audio/wav'
        )

    @patch('backend.services.stt_service.SpeechToTextV1')
    def test_stt_transcription_validation_error(self, mock_stt_v1, setup_stt_service):
        """Test STT transcription with validation error"""
        stt_service = setup_stt_service
        
        # Patch the validator to raise an exception
        with patch.object(stt_service.validator, 'validate_audio_file', side_effect=ValidationError(
            "Invalid audio file", "INVALID_AUDIO_FILE"
        )):
            audio_file = "invalid.wav"
            
            # Call the service and expect exception
            with pytest.raises(ValidationError) as exc_info:
                stt_service.transcribe_audio(audio_file)
            
            assert exc_info.value.code == "INVALID_AUDIO_FILE"
            
            # Verify STT client was not called
            mock_stt_v1.assert_not_called()

    @patch('backend.services.stt_service.SpeechToTextV1')
    def test_stt_transcription_api_error(self, mock_stt_v1, setup_stt_service):
        """Test STT transcription with API error"""
        # Mock the STT client to raise an API error
        mock_stt_instance = MagicMock()
        mock_stt_v1.return_value = mock_stt_instance
        mock_stt_instance.recognize.side_effect = Exception("API request failed")
        
        stt_service = setup_stt_service
        
        # Test file path
        audio_file = "test_audio.wav"
        
        # Create mock file object
        mock_file = mock_open(read_data=b'mock audio data')
        
        # Mock file operations
        with patch('builtins.open', mock_file), \
             patch('os.path.exists', return_value=True), \
             patch('os.path.getsize', return_value=1024):  # Mock 1KB file size
            # Call the service and expect exception
            with pytest.raises(APIError) as exc_info:
                stt_service.transcribe_audio(audio_file)
        
        assert "API request failed" in str(exc_info.value)
        
        # Verify STT client was called with the same mock file object
        mock_stt_instance.recognize.assert_called_once_with(
            audio=mock_file(),
            content_type='audio/wav'
        ) 