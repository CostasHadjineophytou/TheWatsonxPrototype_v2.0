import pytest
import os
from pathlib import Path
from unittest.mock import MagicMock

from logic.managers.tts_manager import TTSManager
from logic.models.speech_request import TTSRequest
from logic.validators.speech_validator import SpeechValidator
from logic.tests.fixtures.sample_responses import TEXT_PROCESSING_RESULT


class TestTTSSynthesis:
    """Integration tests for TTS synthesis flow in the logic layer"""

    @pytest.fixture
    def setup_tts_integration(self):
        """Setup TTS components for logic layer integration testing"""
        # Create mock service that simulates successful responses
        mock_service = MagicMock()
        
        # Setup default success response
        mock_service.synthesize_text.return_value = "data/audio/test_output/test.wav"
        
        # Setup error for invalid voice
        def service_side_effect(text, voice, params):
            if voice == "invalid_voice":
                raise ValueError("Invalid voice model specified")
            return "data/audio/test_output/test.wav"
            
        mock_service.synthesize_text.side_effect = service_side_effect
        
        # Create validator
        validator = SpeechValidator()
        
        # Create manager with real validator but mock service
        manager = TTSManager(tts_service=mock_service, validator=validator)
        
        # Setup test output directory
        output_dir = Path("data/audio/test_output")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a dummy output file to simulate service response
        test_file = output_dir / "test.wav"
        test_file.write_bytes(b"dummy audio data")
        
        yield manager
        
        # Cleanup test files after tests
        for file in output_dir.glob("*.wav"):
            try:
                file.unlink()
            except Exception:
                pass

    def test_tts_synthesis_flow(self, setup_tts_integration):
        """Test TTS synthesis flow through the logic layer"""
        # Get the TTS manager
        manager = setup_tts_integration
        
        # Create TTS request with test data
        request = TTSRequest(
            text=TEXT_PROCESSING_RESULT['original'],
            voice="en-US_AllisonV3Voice",
            accept="audio/wav",
            pitch=0,
            speed=0
        )
        
        # Execute synthesis
        response = manager.synthesize_speech(request)
        
        # Verify logic layer handling
        assert not response.error
        assert response.audio_path
        assert os.path.exists(response.audio_path)

    def test_tts_synthesis_with_different_voices(self, setup_tts_integration):
        """Test logic layer handling of different voice models"""
        manager = setup_tts_integration
        test_text = "This is a test of different voices."
        
        # Test multiple voices
        voices = ["en-US_AllisonV3Voice", "en-US_MichaelV3Voice"]
        
        for voice in voices:
            request = TTSRequest(
                text=test_text,
                voice=voice,
                accept="audio/wav"
            )
            
            response = manager.synthesize_speech(request)
            
            # Verify logic layer handling
            assert not response.error
            assert response.audio_path
            assert os.path.exists(response.audio_path)

    def test_tts_synthesis_with_speech_parameters(self, setup_tts_integration):
        """Test logic layer handling of speech parameters"""
        manager = setup_tts_integration
        test_text = "This is a test of speech parameters."
        
        # Test different parameter combinations
        params = [
            {"pitch": -10, "speed": 0.8},
            {"pitch": 10, "speed": 1.2}
        ]
        
        for param in params:
            request = TTSRequest(
                text=test_text,
                voice="en-US_AllisonV3Voice",
                accept="audio/wav",
                pitch=param["pitch"],
                speed=param["speed"]
            )
            
            response = manager.synthesize_speech(request)
            
            # Verify logic layer handling
            assert not response.error
            assert response.audio_path
            assert os.path.exists(response.audio_path)

    def test_tts_synthesis_error_handling(self, setup_tts_integration):
        """Test logic layer error handling"""
        manager = setup_tts_integration
        
        # Test with invalid text (validation error)
        empty_request = TTSRequest(
            text="",
            voice="en-US_AllisonV3Voice",
            accept="audio/wav"
        )
        empty_response = manager.synthesize_speech(empty_request)
        assert empty_response.error
        assert "text is required" in empty_response.error.lower()
        
        # Test with invalid voice (validation error)
        invalid_voice_request = TTSRequest(
            text="Test text",
            voice="invalid_voice",
            accept="audio/wav"
        )
        invalid_voice_response = manager.synthesize_speech(invalid_voice_request)
        assert invalid_voice_response.error
        assert "voice" in invalid_voice_response.error.lower() 