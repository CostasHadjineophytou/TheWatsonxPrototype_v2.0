import pytest
from unittest.mock import patch, MagicMock

from logic.managers.tts_manager import TTSManager
from logic.models.errors import ValidationError, LogicError
from logic.models.speech_request import TTSRequest
from logic.validators.speech_validator import SpeechValidator


class TestTTSManager:
    """Unit tests for TTSManager class"""

    @pytest.fixture
    def setup_tts_manager(self, mock_tts_service, mock_credentials):
        """Setup TTSManager instance with mocked dependencies"""
        validator = SpeechValidator()
        manager = TTSManager(tts_service=mock_tts_service, validator=validator)
        manager._credentials = mock_credentials
        return manager

    def test_synthesize_text_success(self, setup_tts_manager, mock_tts_service):
        """Test successful text synthesis"""
        # Setup
        output_file = "output.wav"
        mock_tts_service.synthesize_text.return_value = output_file
        
        manager = setup_tts_manager
        
        # Test data
        request = TTSRequest(
            text="Test text to synthesize",
            voice="en-US_AllisonV3Voice",
            accept="audio/wav",
            pitch=0,
            speed=0
        )
        
        # Execute
        result = manager.synthesize_speech(request)
        
        # Assert
        assert result.audio_path == output_file
        mock_tts_service.synthesize_text.assert_called_once_with(
            request.text,
            request.voice,
            {
                'accept': request.accept,
                'pitch': request.pitch,
                'speed': request.speed
            }
        )

    def test_synthesize_text_validation_error(self, setup_tts_manager, mock_tts_service):
        """Test synthesis with validation error"""
        manager = setup_tts_manager
        
        # Test data - empty text should fail validation
        request = TTSRequest(
            text="",  # Invalid text
            voice="en-US_AllisonV3Voice",
            accept="audio/wav",
            pitch=0,
            speed=0
        )
        
        # Execute and Assert
        result = manager.synthesize_speech(request)
        assert result.error is not None
        assert "Text is required" in result.error
        mock_tts_service.synthesize_text.assert_not_called()

    def test_synthesize_text_service_error(self, setup_tts_manager, mock_tts_service):
        """Test synthesis with service error"""
        # Setup
        mock_tts_service.synthesize_text.side_effect = LogicError(
            message="Service processing failed",
            code="SERVICE_ERROR"
        )
        
        manager = setup_tts_manager
        
        # Test data
        request = TTSRequest(
            text="Test text",
            voice="en-US_AllisonV3Voice",
            accept="audio/wav",
            pitch=0,
            speed=0
        )
        
        # Execute and Assert
        result = manager.synthesize_speech(request)
        assert result.error is not None
        assert "Service processing failed" in result.error 