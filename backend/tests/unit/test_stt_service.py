import pytest
from unittest.mock import patch, MagicMock, mock_open

from backend.services.stt_service import STTService
from backend.utils.errors import ValidationError, AuthenticationError, APIError, FileError
from backend.tests.fixtures.sample_responses import STT_RESPONSE


class TestSTTService:
    """Tests for the STTService class"""

    def test_init(self, mock_credentials_manager):
        """Test initializing the STTService"""
        service = STTService(mock_credentials_manager)
        assert service.credentials_manager == mock_credentials_manager
        assert service._stt is None

    def test_initialize_success(self, mock_credentials_manager, mock_credentials):
        """Test successful STT client initialization"""
        mock_credentials_manager.get_service_credentials.return_value = mock_credentials
        
        service = STTService(mock_credentials_manager)
        service.initialize()
        
        mock_credentials_manager.get_service_credentials.assert_called_once_with("Speech to Text")
        assert service._stt is not None

    def test_initialize_error(self, mock_credentials_manager):
        """Test STT client initialization failure"""
        mock_credentials_manager.get_service_credentials.side_effect = AuthenticationError(
            "Failed to get credentials", "STT_INIT_ERROR"
        )
        
        service = STTService(mock_credentials_manager)
        
        with pytest.raises(AuthenticationError) as exc_info:
            service.initialize()
        
        assert exc_info.value.code == "STT_INIT_ERROR"
        assert service._stt is None

    @patch('backend.validators.service_validator.ServiceValidator.validate_audio_file')
    def test_transcribe_audio_success(self, mock_validate, mock_credentials_manager):
        """Test transcribing audio successfully"""
        service = STTService(mock_credentials_manager)
        
        # Mock STT client
        mock_stt = MagicMock()
        mock_stt.recognize.return_value.get_result.return_value = STT_RESPONSE
        service._stt = mock_stt
        
        # Test file path
        audio_file = "test_audio.wav"
        
        # Mock file operations
        mock_file = mock_open(read_data=b'mock audio data')
        with patch('builtins.open', mock_file):
            with patch('os.path.exists', return_value=True):
                result = service.transcribe_audio(audio_file)
        
        # Assertions
        assert result == "This is a sample transcription of speech to text."
        mock_validate.assert_called_once_with(audio_file)
        mock_stt.recognize.assert_called_once_with(
            audio=mock_file(),
            content_type='audio/wav'
        )

    def test_transcribe_audio_file_not_found(self, mock_credentials_manager):
        """Test transcribing with non-existent audio file"""
        service = STTService(mock_credentials_manager)
        
        with patch('os.path.exists', return_value=False):
            with pytest.raises(ValidationError) as exc_info:
                service.transcribe_audio("nonexistent.wav")
        
        assert exc_info.value.code == "FILE_NOT_FOUND"
        assert service._stt is None

    def test_transcribe_audio_validation_error(self, mock_credentials_manager):
        """Test transcribing with validation error"""
        service = STTService(mock_credentials_manager)
        
        with patch.object(service.validator, 'validate_audio_file') as mock_validate:
            mock_validate.side_effect = ValidationError(
                "Invalid audio file", "INVALID_AUDIO_FILE"
            )
            
            with pytest.raises(ValidationError) as exc_info:
                service.transcribe_audio("test.wav")
            
            assert exc_info.value.code == "INVALID_AUDIO_FILE"
            assert service._stt is None

    @patch('backend.validators.service_validator.ServiceValidator.validate_audio_file')
    def test_transcribe_audio_auth_error(self, mock_validate, mock_credentials_manager):
        """Test transcribing with authentication error"""
        service = STTService(mock_credentials_manager)
        mock_credentials_manager.get_service_credentials.side_effect = AuthenticationError(
            "Authentication failed", "STT_INIT_ERROR"
        )
        
        with patch('os.path.exists', return_value=True):
            with pytest.raises(AuthenticationError) as exc_info:
                service.transcribe_audio("test.wav")
            
            assert exc_info.value.code == "STT_INIT_ERROR"
            mock_validate.assert_called_once()

    @patch('backend.validators.service_validator.ServiceValidator.validate_audio_file')
    def test_transcribe_audio_api_error(self, mock_validate, mock_credentials_manager):
        """Test transcribing with API error"""
        service = STTService(mock_credentials_manager)
        
        # Mock STT client
        mock_stt = MagicMock()
        mock_stt.recognize.side_effect = Exception("API request failed")
        service._stt = mock_stt
        
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=b'mock audio data')):
                with pytest.raises(APIError) as exc_info:
                    service.transcribe_audio("test.wav")
        
        assert "API request failed" in str(exc_info.value)
        mock_validate.assert_called_once()