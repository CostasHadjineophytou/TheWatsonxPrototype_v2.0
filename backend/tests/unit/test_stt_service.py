import pytest
from unittest.mock import patch, MagicMock, mock_open

from backend.services.stt_service import STTService
from backend.utils.errors import ValidationError, AuthenticationError, APIError, FileError


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

    @patch('backend.validators.service_validator.ServiceValidator.validate_audio_file')
    def test_transcribe_audio_success(self, mock_validate, mock_credentials_manager):
        """Test transcribing audio successfully"""
        service = STTService(mock_credentials_manager)
        
        # Mock STT client
        mock_stt = MagicMock()
        mock_response = {
            "results": [
                {
                    "alternatives": [
                        {
                            "transcript": "This is a test transcription.",
                            "confidence": 0.95
                        }
                    ],
                    "final": True
                }
            ],
            "result_index": 0
        }
        mock_stt.recognize.return_value.get_result.return_value = mock_response
        service._stt = mock_stt
        
        # Test file path
        audio_file = "test_audio.wav"
        
        # Mock file operations
        with patch('builtins.open', mock_open(read_data=b'mock audio data')):
            with patch('os.path.exists', return_value=True):
                result = service.transcribe_audio(audio_file)
        
        # Assertions
        assert result == "This is a test transcription."
        mock_validate.assert_called_once_with(audio_file)
        mock_stt.recognize.assert_called_once_with(
            audio=mock_response,
            content_type='audio/wav'
        )

    def test_transcribe_audio_file_not_found(self, mock_credentials_manager):
        """Test transcribing with non-existent audio file"""
        service = STTService(mock_credentials_manager)
        
        with patch('os.path.exists', return_value=False):
            with pytest.raises(FileError) as exc_info:
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

    def test_get_models_success(self, mock_credentials_manager):
        """Test getting available models successfully"""
        service = STTService(mock_credentials_manager)
        
        # Mock STT client
        mock_stt = MagicMock()
        mock_models = {
            "models": [
                {
                    "name": "en-US_BroadbandModel",
                    "language": "en-US",
                    "description": "US English broadband model"
                },
                {
                    "name": "en-US_NarrowbandModel",
                    "language": "en-US",
                    "description": "US English narrowband model"
                }
            ]
        }
        mock_stt.list_models.return_value.get_result.return_value = mock_models
        service._stt = mock_stt
        
        # Call the method
        result = service.get_models()
        
        # Assertions
        assert result == mock_models["models"]
        mock_stt.list_models.assert_called_once()

    def test_get_models_auth_error(self, mock_credentials_manager):
        """Test getting models with authentication error"""
        service = STTService(mock_credentials_manager)
        mock_credentials_manager.get_service_credentials.side_effect = AuthenticationError(
            "Authentication failed", "STT_INIT_ERROR"
        )
        
        with pytest.raises(AuthenticationError) as exc_info:
            service.get_models()
        
        assert exc_info.value.code == "STT_INIT_ERROR"

    def test_get_models_api_error(self, mock_credentials_manager):
        """Test getting models with API error"""
        service = STTService(mock_credentials_manager)
        
        # Mock STT client
        mock_stt = MagicMock()
        mock_stt.list_models.side_effect = Exception("API request failed")
        service._stt = mock_stt
        
        with pytest.raises(APIError) as exc_info:
            service.get_models()
        
        assert "API request failed" in str(exc_info.value)
        mock_stt.list_models.assert_called_once()

    @patch('backend.services.stt_service.STTService.get_models')
    def test_get_model_by_language_success(self, mock_get_models, mock_watson_client):
        """Test getting model by language successfully"""
        # Mock the get_models method
        mock_models = [
            {
                "name": "en-US_BroadbandModel",
                "language": "en-US",
                "description": "US English broadband model"
            },
            {
                "name": "en-US_NarrowbandModel",
                "language": "en-US",
                "description": "US English narrowband model"
            },
            {
                "name": "de-DE_BroadbandModel",
                "language": "de-DE",
                "description": "German broadband model"
            }
        ]
        mock_get_models.return_value = mock_models
        
        # Create the service
        service = STTService(mock_watson_client)
        
        # Call the method
        result = service.get_model_by_language("en-US")
        
        # Assertions
        assert len(result) == 2
        assert all(model["language"] == "en-US" for model in result)
        mock_get_models.assert_called_once()

    @patch('backend.services.stt_service.STTService.get_models')
    def test_get_model_by_language_no_match(self, mock_get_models, mock_watson_client):
        """Test getting model by language with no match"""
        # Mock the get_models method
        mock_models = [
            {
                "name": "en-US_BroadbandModel",
                "language": "en-US",
                "description": "US English broadband model"
            },
            {
                "name": "de-DE_BroadbandModel",
                "language": "de-DE",
                "description": "German broadband model"
            }
        ]
        mock_get_models.return_value = mock_models
        
        # Create the service
        service = STTService(mock_watson_client)
        
        # Call the method
        result = service.get_model_by_language("fr-FR")
        
        # Assertions
        assert len(result) == 0
        mock_get_models.assert_called_once()

    @patch('backend.validators.service_validator.ServiceValidator.validate_stt_params')
    @patch('builtins.open', new_callable=mock_open, read_data=b'mock audio data')
    def test_transcribe_audio_with_keywords(self, mock_file, mock_validate, mock_watson_client):
        """Test transcribing audio with keywords"""
        # Mock the client's post_request method
        mock_response = {
            "results": [
                {
                    "alternatives": [
                        {
                            "transcript": "This is a test transcription with keywords.",
                            "confidence": 0.95
                        }
                    ],
                    "final": True,
                    "keywords_result": {
                        "test": [
                            {
                                "normalized_text": "test",
                                "start_time": 1.2,
                                "end_time": 1.5,
                                "confidence": 0.98
                            }
                        ]
                    }
                }
            ],
            "result_index": 0
        }
        mock_watson_client.post_request.return_value = mock_response
        
        # Create the service
        service = STTService(mock_watson_client)
        
        # Parameters for transcription
        audio_file = "test_audio.wav"
        model = "en-US_BroadbandModel"
        params = {
            "content_type": "audio/wav",
            "keywords": ["test", "keywords"],
            "keywords_threshold": 0.5
        }
        
        # Mock os.path.exists to return True
        with patch('os.path.exists', return_value=True):
            # Call the method
            result = service.transcribe_audio(audio_file, model, params)
        
        # Assertions
        assert result == mock_response
        mock_validate.assert_called_once()
        mock_watson_client.post_request.assert_called_once()
        # Check that the keywords were included in the params
        _, kwargs = mock_watson_client.post_request.call_args
        assert 'keywords' in kwargs['params']
        assert kwargs['params']['keywords'] == ["test", "keywords"]
        assert kwargs['params']['keywords_threshold'] == 0.5 