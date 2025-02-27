import pytest
from unittest.mock import MagicMock

from logic.managers.stt_manager import STTManager
from logic.models.errors import ValidationError, LogicError
from logic.validators.speech_validator import SpeechValidator
from logic.models.speech_request import STTRequest
from logic.models.responses import STTResponse


class TestSTTManager:
    """Unit tests for STTManager class"""

    @pytest.fixture
    def setup_stt_manager(self, mock_stt_service):
        """Setup STTManager instance with mocked dependencies"""
        validator = SpeechValidator()
        manager = STTManager(stt_service=mock_stt_service, validator=validator)
        return manager

    def test_transcribe_speech_success(self, setup_stt_manager, mock_stt_service):
        """Test successful speech transcription"""
        # Setup mock response
        transcription = "This is a test transcription"
        mock_stt_service.transcribe_audio.return_value = transcription

        # Execute
        manager = setup_stt_manager
        request = STTRequest(audio_path="test_audio.wav")
        result = manager.transcribe_speech(request)

        # Assert
        assert result.text == transcription
        assert result.audio_path == "test_audio.wav"
        assert result.success is True
        assert not result.error
        mock_stt_service.transcribe_audio.assert_called_once_with(
            file_path="test_audio.wav"
        )

    def test_transcribe_speech_validation_error(self, setup_stt_manager, mock_stt_service):
        """Test transcription with invalid audio path"""
        # Execute
        manager = setup_stt_manager
        request = STTRequest(audio_path="")  # Invalid path
        result = manager.transcribe_speech(request)

        # Assert
        assert result.text == ""
        assert result.audio_path == ""
        assert result.success is False
        assert result.error is not None
        assert "Audio file path is required" in result.error
        mock_stt_service.transcribe_audio.assert_not_called()

    def test_transcribe_speech_service_error(self, setup_stt_manager, mock_stt_service):
        """Test handling of service error"""
        # Setup error
        mock_stt_service.transcribe_audio.side_effect = Exception("Service error")

        # Execute
        manager = setup_stt_manager
        request = STTRequest(audio_path="test_audio.wav")
        result = manager.transcribe_speech(request)

        # Assert
        assert result.text == ""
        assert result.audio_path == "test_audio.wav"
        assert result.success is False
        assert result.error is not None
        assert "Failed to transcribe speech" in result.error
        mock_stt_service.transcribe_audio.assert_called_once_with(
            file_path="test_audio.wav"
        )

    def test_transcribe_speech_empty_transcription(self, setup_stt_manager, mock_stt_service):
        """Test handling of empty transcription"""
        # Setup empty response
        mock_stt_service.transcribe_audio.return_value = ""

        # Execute
        manager = setup_stt_manager
        request = STTRequest(audio_path="test_audio.wav")
        result = manager.transcribe_speech(request)

        # Assert
        assert result.text == ""
        assert result.audio_path == "test_audio.wav"
        assert result.success is False
        assert result.error is not None
        assert "No transcription generated" in result.error
        mock_stt_service.transcribe_audio.assert_called_once_with(
            file_path="test_audio.wav"
        ) 