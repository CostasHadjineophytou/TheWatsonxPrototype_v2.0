import pytest
from unittest.mock import patch, MagicMock

from logic.managers.tts_manager import TTSManager
from logic.models.errors import ValidationError, LogicError
from logic.models.speech_request import TTSRequest
from logic.validators.speech_validator import SpeechValidator
from logic.tests.fixtures.sample_responses import TEXT_PROCESSING_RESULT


class TestTTSSynthesis:
    """Integration tests for TTS synthesis flow"""

    @pytest.fixture
    def setup_tts_flow(self, mock_tts_service, mock_credentials):
        """Setup TTS manager and service with mocked dependencies"""
        validator = SpeechValidator()
        manager = TTSManager(tts_service=mock_tts_service, validator=validator)
        manager._credentials = mock_credentials
        return manager

    def test_tts_synthesis_flow(self, setup_tts_flow, mock_tts_service):
        """Test complete TTS synthesis flow from manager through service"""
        # Setup
        output_path = "data/audio/test_output.wav"
        mock_tts_service.synthesize_text.return_value = output_path
        
        # Get the TTS manager
        manager = setup_tts_flow
        
        # Create TTS request
        request = TTSRequest(
            text=TEXT_PROCESSING_RESULT['original'],
            voice="en-US_AllisonV3Voice",
            accept="audio/wav",
            pitch=0,
            speed=0
        )
        
        # Call the manager
        response = manager.synthesize_speech(request)
        
        # Assertions
        assert response.audio_path == output_path
        assert not response.error
        
        # Verify service was called correctly
        mock_tts_service.synthesize_text.assert_called_once_with(
            request.text,
            request.voice,
            {
                'accept': request.accept,
                'pitch': request.pitch,
                'speed': request.speed
            }
        )

    def test_tts_synthesis_validation_error(self, setup_tts_flow, mock_tts_service):
        """Test TTS synthesis with validation error"""
        manager = setup_tts_flow
        
        # Create invalid TTS request (empty text)
        request = TTSRequest(
            text="",
            voice="en-US_AllisonV3Voice",
            accept="audio/wav",
            pitch=0,
            speed=0
        )
        
        # Execute and Assert
        response = manager.synthesize_speech(request)
        assert response.error is not None
        assert "Text is required" in response.error
        assert not response.audio_path
        mock_tts_service.synthesize_text.assert_not_called()

    def test_tts_synthesis_service_error(self, setup_tts_flow, mock_tts_service):
        """Test TTS synthesis with service error"""
        # Setup service error
        mock_tts_service.synthesize_text.side_effect = LogicError(
            message="Service processing failed",
            code="SERVICE_ERROR"
        )
        
        manager = setup_tts_flow
        
        # Create TTS request
        request = TTSRequest(
            text=TEXT_PROCESSING_RESULT['original'],
            voice="en-US_AllisonV3Voice",
            accept="audio/wav",
            pitch=0,
            speed=0
        )
        
        # Execute and Assert
        response = manager.synthesize_speech(request)
        assert response.error is not None
        assert "Service processing failed" in response.error
        assert not response.audio_path
        
        # Verify service was called
        mock_tts_service.synthesize_text.assert_called_once_with(
            request.text,
            request.voice,
            {
                'accept': request.accept,
                'pitch': request.pitch,
                'speed': request.speed
            }
        ) 