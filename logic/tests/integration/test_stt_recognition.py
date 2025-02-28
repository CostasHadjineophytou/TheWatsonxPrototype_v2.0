import pytest
import os
from pathlib import Path
from unittest.mock import MagicMock

from logic.managers.stt_manager import STTManager
from logic.models.speech_request import STTRequest
from logic.validators.speech_validator import SpeechValidator
from backend.config.speech_config import SpeechConfig


class TestSTTRecognition:
    """Integration tests for STT recognition flow in the logic layer"""

    @pytest.fixture
    def setup_stt_integration(self):
        """Setup STT components for logic layer integration testing"""
        # Create mock service that simulates successful responses
        mock_service = MagicMock()
        
        # Setup default success response
        mock_service.transcribe_audio.return_value = "This is a test transcription"
        
        # Setup error for invalid files
        def service_side_effect(file_path, **kwargs):
            if not os.path.exists(file_path):
                raise ValueError("File not found")
            if not file_path.endswith('.wav'):
                raise ValueError("Unsupported audio format")
            return "This is a test transcription"
            
        mock_service.transcribe_audio.side_effect = service_side_effect
        
        # Create validator
        validator = SpeechValidator()
        
        # Create manager with real validator but mock service
        manager = STTManager(stt_service=mock_service, validator=validator)
        
        # Setup test audio directory
        audio_dir = Path("data/audio/test_samples")
        audio_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a dummy test file
        test_file = audio_dir / "test_speech.wav"
        test_file.write_bytes(b"dummy audio data")
        
        yield manager, audio_dir
        
        # Cleanup test files after tests
        for file in audio_dir.glob("*.wav"):
            try:
                file.unlink()
            except Exception:
                pass

    def test_stt_recognition_flow(self, setup_stt_integration):
        """Test STT recognition flow through the logic layer"""
        # Get the STT manager and test directory
        manager, audio_dir = setup_stt_integration
        
        # Create STT request with test data
        request = STTRequest(
            audio_path=str(audio_dir / "test_speech.wav")
        )
        
        # Execute recognition
        response = manager.transcribe_speech(request)
        
        # Verify logic layer handling
        assert not response.error
        assert response.text == "This is a test transcription"
        assert response.success
        assert response.audio_path == str(audio_dir / "test_speech.wav")

    def test_stt_validation(self, setup_stt_integration):
        """Test STT request validation"""
        manager, audio_dir = setup_stt_integration
        
        # Test empty path
        empty_request = STTRequest(audio_path="")
        empty_response = manager.transcribe_speech(empty_request)
        assert empty_response.error
        assert "path" in empty_response.error.lower()
        assert not empty_response.success
        
        # Test non-existent file
        nonexistent_request = STTRequest(audio_path="nonexistent.wav")
        nonexistent_response = manager.transcribe_speech(nonexistent_request)
        assert nonexistent_response.error
        assert "file" in nonexistent_response.error.lower()
        assert not nonexistent_response.success
        
        # Test unsupported format
        unsupported_path = audio_dir / "test.mp3"
        unsupported_path.write_bytes(b"dummy audio data")
        unsupported_request = STTRequest(audio_path=str(unsupported_path))
        unsupported_response = manager.transcribe_speech(unsupported_request)
        assert unsupported_response.error
        assert "format" in unsupported_response.error.lower()
        assert not unsupported_response.success
        
        # Cleanup test file
        unsupported_path.unlink()

    def test_stt_error_handling(self, setup_stt_integration):
        """Test STT error handling in logic layer"""
        manager, audio_dir = setup_stt_integration
        
        # Create a test file that will trigger service error
        test_file = audio_dir / "test_speech.wav"
        
        # Mock service to raise an error
        manager.stt_service.transcribe_audio.side_effect = Exception("Service error")
        
        # Test service error handling
        request = STTRequest(audio_path=str(test_file))
        response = manager.transcribe_speech(request)
        
        # Verify error handling
        assert response.error
        assert "failed" in response.error.lower()
        assert not response.success
        assert response.text == ""  # Empty text on error
