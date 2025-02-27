import pytest
from unittest.mock import MagicMock, patch
import os

from logic.managers.stt_manager import STTManager
from logic.models.errors import ValidationError, LogicError
from logic.validators.speech_validator import SpeechValidator
from logic.models.speech_request import STTRequest
from logic.models.responses import STTResponse
from backend.config.speech_config import SpeechConfig


class TestSTTManager:
    """Unit tests for STTManager class"""

    @pytest.fixture
    def setup_stt_manager(self, mock_stt_service):
        """Setup STTManager instance with mocked dependencies"""
        validator = SpeechValidator()
        manager = STTManager(stt_service=mock_stt_service, validator=validator)
        return manager

    @patch('os.path.exists')
    @patch('os.path.getsize')
    def test_transcribe_speech_success(self, mock_getsize, mock_exists, setup_stt_manager, mock_stt_service):
        """Test successful speech transcription"""
        # Setup mock response
        mock_exists.return_value = True  # Mock file exists
        mock_getsize.return_value = 1024  # Mock 1KB file size
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

    @patch('os.path.exists')
    @patch('os.path.getsize')
    def test_transcribe_speech_service_error(self, mock_getsize, mock_exists, setup_stt_manager, mock_stt_service):
        """Test handling of service error"""
        # Setup error
        mock_exists.return_value = True  # Mock file exists
        mock_getsize.return_value = 1024  # Mock 1KB file size
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

    @patch('os.path.exists')
    @patch('os.path.getsize')
    def test_transcribe_speech_empty_transcription(self, mock_getsize, mock_exists, setup_stt_manager, mock_stt_service):
        """Test handling of empty transcription"""
        # Setup empty response
        mock_exists.return_value = True  # Mock file exists
        mock_getsize.return_value = 1024  # Mock 1KB file size
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
        assert "Failed to transcribe speech" in result.error
        assert "Speech transcription failed" in result.error
        mock_stt_service.transcribe_audio.assert_called_once_with(
            file_path="test_audio.wav"
        ) 