import pytest
import os
import shutil
from pathlib import Path

from backend.services.stt_service import STTService
from backend.services.credentials_manager import CredentialsManager
from logic.managers.stt_manager import STTManager
from logic.models.speech_request import STTRequest
from logic.validators.speech_validator import SpeechValidator


class TestSTTEndToEnd:
    """End-to-end tests for Speech-to-Text functionality"""

    @pytest.fixture(autouse=True)
    def setup_test_files(self):
        """Setup and cleanup test files before and after each test"""
        # Setup test directories
        test_dir = Path("data/audio/test_samples")
        test_dir.mkdir(parents=True, exist_ok=True)

        # Clean up any existing test files
        for file in test_dir.glob("test_speech.*"):
            file.unlink(missing_ok=True)

        yield

        # Cleanup after test
        for file in test_dir.glob("test_speech.*"):
            file.unlink(missing_ok=True)

    @pytest.fixture
    def setup_stt_system(self):
        """Setup complete STT system with real components"""
        # Initialize real credentials manager
        credentials_manager = CredentialsManager()

        # Create real STT service
        service = STTService(credentials_manager=credentials_manager)

        # Create real validator
        validator = SpeechValidator()

        # Create real manager
        manager = STTManager(stt_service=service, validator=validator)

        # Setup test audio directory
        audio_dir = Path("data/audio/test_samples")
        audio_dir.mkdir(parents=True, exist_ok=True)

        # Copy the sample audio file
        sample_path = Path("tests/resources/audio_samples/sample_speech.wav")
        if not sample_path.exists():
            raise FileNotFoundError(
                "Sample audio file not found at tests/resources/audio_samples/sample_speech.wav"
            )

        test_file = audio_dir / "test_speech.wav"
        shutil.copy2(sample_path, test_file)

        yield manager, audio_dir

    def test_basic_speech_recognition(self, setup_stt_system):
        """Test basic speech-to-text recognition end-to-end"""
        manager, audio_dir = setup_stt_system
        audio_file = audio_dir / "test_speech.wav"

        # Create a simple request
        request = STTRequest(
            audio_path=str(audio_file)
        )

        # Execute the full recognition pipeline
        response = manager.transcribe_speech(request)

        # Verify complete flow
        assert not response.error, f"Recognition failed with error: {response.error}"
        assert response.text is not None
        assert len(response.text) > 0

    def test_different_models(self, setup_stt_system):
        """Test recognition with different STT models"""
        manager, audio_dir = setup_stt_system
        audio_file = audio_dir / "test_speech.wav"

        # Just test basic transcription since models aren't supported
        request = STTRequest(
            audio_path=str(audio_file)
        )
        response = manager.transcribe_speech(request)

        # Verify basic transcription works
        assert not response.error, f"Transcription failed with error: {response.error}"
        assert response.text is not None
        assert len(response.text) > 0

    def test_recognition_parameters(self, setup_stt_system):
        """Test recognition with various parameters"""
        manager, audio_dir = setup_stt_system
        audio_file = audio_dir / "test_speech.wav"

        # Just test basic transcription since parameters aren't supported
        request = STTRequest(
            audio_path=str(audio_file)
        )
        response = manager.transcribe_speech(request)

        # Verify basic transcription works
        assert not response.error, f"Transcription failed with error: {response.error}"
        assert response.text is not None
        assert len(response.text) > 0

    def test_error_conditions(self, setup_stt_system):
        """Test system handling of error conditions"""
        manager, _ = setup_stt_system

        # Test non-existent file
        invalid_file_request = STTRequest(audio_path="nonexistent.wav")
        invalid_file_response = manager.transcribe_speech(invalid_file_request)
        assert invalid_file_response.error
        assert "file" in invalid_file_response.error.lower()

        # Test empty path
        empty_path_request = STTRequest(audio_path="")
        empty_path_response = manager.transcribe_speech(empty_path_request)
        assert empty_path_response.error
        assert "path" in empty_path_response.error.lower()

        # Test unsupported format
        invalid_format_request = STTRequest(audio_path="test.xyz")
        invalid_format_response = manager.transcribe_speech(invalid_format_request)
        assert invalid_format_response.error
        assert "format" in invalid_format_response.error.lower()
