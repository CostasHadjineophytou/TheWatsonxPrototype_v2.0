import pytest
import os
from pathlib import Path

from backend.services.tts_service import TTSService
from backend.services.credentials_manager import CredentialsManager
from logic.managers.tts_manager import TTSManager
from logic.models.speech_request import TTSRequest
from logic.validators.speech_validator import SpeechValidator


class TestTTSEndToEnd:
    """End-to-end tests for Text-to-Speech functionality"""

    @pytest.fixture
    def setup_tts_system(self):
        """Setup complete TTS system with real components"""
        # Initialize real credentials manager
        credentials_manager = CredentialsManager()

        # Create real TTS service
        service = TTSService(credentials_manager=credentials_manager)

        # Create real validator
        validator = SpeechValidator()

        # Create real manager
        manager = TTSManager(tts_service=service, validator=validator)

        # Setup output directory for generated audio
        output_dir = Path("data/audio/e2e_test_output")
        output_dir.mkdir(parents=True, exist_ok=True)

        yield manager

        # Cleanup generated files after tests
        for file in output_dir.glob("*.wav"):
            try:
                file.unlink()
            except Exception:
                pass

    def test_basic_speech_synthesis(self, setup_tts_system):
        """Test basic text-to-speech synthesis end-to-end"""
        manager = setup_tts_system

        # Create a simple request
        request = TTSRequest(
            text="Hello, this is an end-to-end test of the text to speech system.",
            voice="en-US_AllisonV3Voice",
            accept="audio/wav"
        )

        # Execute the full synthesis pipeline
        response = manager.synthesize_speech(request)

        # Verify complete flow
        assert not response.error, f"Synthesis failed with error: {response.error}"
        assert response.audio_path
        assert os.path.exists(response.audio_path)
        assert os.path.getsize(response.audio_path) > 1000  # Real audio file should have significant size

    def test_long_text_synthesis(self, setup_tts_system):
        """Test synthesis of longer text content"""
        manager = setup_tts_system

        # Create a request with longer text
        long_text = """
        This is a longer piece of text that will test the system's ability to handle
        multiple sentences and paragraphs. It includes various punctuation marks,
        and should result in a longer audio file. The system should process this
        correctly and generate appropriate speech output.
        """

        request = TTSRequest(
            text=long_text,
            voice="en-US_AllisonV3Voice",
            accept="audio/wav"
        )

        # Execute synthesis
        response = manager.synthesize_speech(request)

        # Verify
        assert not response.error, f"Long text synthesis failed with error: {response.error}"
        assert os.path.exists(response.audio_path)
        assert os.path.getsize(response.audio_path) > 5000  # Longer text should produce larger file

    def test_voice_variations(self, setup_tts_system):
        """Test synthesis with different voices"""
        manager = setup_tts_system
        test_text = "This is a test of different voice models."

        # Test multiple voice models
        voices = [
            "en-US_AllisonV3Voice",
            "en-US_MichaelV3Voice",
            "en-US_LisaV3Voice"
        ]

        previous_sizes = []
        for voice in voices:
            request = TTSRequest(
                text=test_text,
                voice=voice,
                accept="audio/wav"
            )

            response = manager.synthesize_speech(request)

            # Verify each voice produces unique output
            assert not response.error, f"Voice {voice} failed with error: {response.error}"
            assert os.path.exists(response.audio_path)
            
            current_size = os.path.getsize(response.audio_path)
            assert current_size > 1000  # Ensure real audio is generated
            
            # Different voices should produce different file sizes
            assert current_size not in previous_sizes
            previous_sizes.append(current_size)

    def test_speech_parameters(self, setup_tts_system):
        """Test synthesis with various speech parameters"""
        manager = setup_tts_system
        test_text = "This is a test of speech parameter variations."

        # Test different parameter combinations
        test_cases = [
            {"pitch": -10, "speed": 0.8},  # Slower, lower pitch
            {"pitch": 10, "speed": 1.2},   # Faster, higher pitch
            {"pitch": 0, "speed": 1.0}     # Default settings
        ]

        for params in test_cases:
            request = TTSRequest(
                text=test_text,
                voice="en-US_AllisonV3Voice",
                accept="audio/wav",
                pitch=params["pitch"],
                speed=params["speed"]
            )

            response = manager.synthesize_speech(request)

            # Verify basic success criteria
            assert not response.error, f"Parameters {params} failed with error: {response.error}"
            assert os.path.exists(response.audio_path), f"Audio file not created for parameters {params}"
            
            # Verify file is not empty and has reasonable size
            file_size = os.path.getsize(response.audio_path)
            assert file_size > 1000, f"Audio file too small for parameters {params}"
            assert file_size < 1000000, f"Audio file unexpectedly large for parameters {params}"

    def test_error_conditions(self, setup_tts_system):
        """Test system handling of error conditions"""
        manager = setup_tts_system

        # Test empty text
        empty_request = TTSRequest(
            text="",
            voice="en-US_AllisonV3Voice",
            accept="audio/wav"
        )
        empty_response = manager.synthesize_speech(empty_request)
        assert empty_response.error
        assert "text is required" in empty_response.error.lower()

        # Test invalid voice
        invalid_voice_request = TTSRequest(
            text="Test text",
            voice="invalid_voice",
            accept="audio/wav"
        )
        invalid_voice_response = manager.synthesize_speech(invalid_voice_request)
        assert invalid_voice_response.error
        assert "voice" in invalid_voice_response.error.lower()

        # Test invalid audio format
        invalid_format_request = TTSRequest(
            text="Test text",
            voice="en-US_AllisonV3Voice",
            accept="invalid/format"
        )
        invalid_format_response = manager.synthesize_speech(invalid_format_request)
        assert invalid_format_response.error
