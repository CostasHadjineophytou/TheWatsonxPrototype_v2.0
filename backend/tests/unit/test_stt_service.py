import pytest
from unittest.mock import patch, MagicMock, call, mock_open
import os
import json

from backend.services.stt_service import STTService
from backend.utils.errors import ValidationError, AuthenticationError, APIError, FileError


class TestSTTService:
    """Tests for the STTService class"""

    def test_init(self, mock_watson_client):
        """Test initializing the STTService"""
        service = STTService(mock_watson_client)
        assert service.client == mock_watson_client

    @patch('backend.validators.service_validator.ServiceValidator.validate_stt_params')
    @patch('builtins.open', new_callable=mock_open, read_data=b'mock audio data')
    def test_transcribe_audio_success(self, mock_file, mock_validate, mock_watson_client):
        """Test transcribing audio successfully"""
        # Mock the client's post_request method
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
        mock_watson_client.post_request.return_value = mock_response
        
        # Create the service
        service = STTService(mock_watson_client)
        
        # Parameters for transcription
        audio_file = "test_audio.wav"
        model = "en-US_BroadbandModel"
        params = {
            "content_type": "audio/wav",
            "word_confidence": True
        }
        
        # Mock os.path.exists to return True
        with patch('os.path.exists', return_value=True):
            # Call the method
            result = service.transcribe_audio(audio_file, model, params)
        
        # Assertions
        assert result == mock_response
        mock_validate.assert_called_once()
        mock_watson_client.post_request.assert_called_once()
        # Check that the first argument to post_request is the correct endpoint
        args, _ = mock_watson_client.post_request.call_args
        assert args[0] == '/v1/recognize'
        # Check that the file was opened
        mock_file.assert_called_once_with(audio_file, 'rb')
        # Check that the payload contains the expected data
        _, kwargs = mock_watson_client.post_request.call_args
        assert 'files' in kwargs
        assert 'model' in kwargs['params']
        assert kwargs['params']['model'] == model
        assert 'word_confidence' in kwargs['params']
        assert kwargs['params']['word_confidence'] == True

    def test_transcribe_audio_file_not_found(self, mock_watson_client):
        """Test transcribing with non-existent audio file"""
        # Create the service
        service = STTService(mock_watson_client)
        
        # Mock os.path.exists to return False
        with patch('os.path.exists', return_value=False):
            # Call the method with non-existent file and expect exception
            with pytest.raises(FileError) as exc_info:
                service.transcribe_audio("nonexistent.wav", "en-US_BroadbandModel")
        
        assert exc_info.value.code == "FILE_NOT_FOUND"
        mock_watson_client.post_request.assert_not_called()

    def test_transcribe_audio_empty_file(self, mock_watson_client):
        """Test transcribing with empty audio file path"""
        # Create the service
        service = STTService(mock_watson_client)
        
        # Call the method with empty file path and expect exception
        with pytest.raises(ValidationError) as exc_info:
            service.transcribe_audio("", "en-US_BroadbandModel")
        
        assert exc_info.value.code == "INVALID_AUDIO_FILE"
        mock_watson_client.post_request.assert_not_called()

    def test_transcribe_audio_empty_model(self, mock_watson_client):
        """Test transcribing with empty model"""
        # Create the service
        service = STTService(mock_watson_client)
        
        # Mock os.path.exists to return True
        with patch('os.path.exists', return_value=True):
            # Call the method with empty model and expect exception
            with pytest.raises(ValidationError) as exc_info:
                service.transcribe_audio("test_audio.wav", "")
        
        assert exc_info.value.code == "INVALID_MODEL"
        mock_watson_client.post_request.assert_not_called()

    @patch('backend.validators.service_validator.ServiceValidator.validate_stt_params')
    def test_transcribe_audio_validation_error(self, mock_validate, mock_watson_client):
        """Test transcribing audio with validation error"""
        # Mock the validator to raise a validation error
        mock_validate.side_effect = ValidationError(
            "Invalid parameters", "INVALID_PARAMS"
        )
        
        # Create the service
        service = STTService(mock_watson_client)
        
        # Mock os.path.exists to return True
        with patch('os.path.exists', return_value=True):
            # Call the method and expect exception
            with pytest.raises(ValidationError) as exc_info:
                service.transcribe_audio("test_audio.wav", "en-US_BroadbandModel", {"invalid_param": True})
        
        assert exc_info.value.code == "INVALID_PARAMS"
        mock_watson_client.post_request.assert_not_called()

    @patch('backend.validators.service_validator.ServiceValidator.validate_stt_params')
    @patch('builtins.open', new_callable=mock_open, read_data=b'mock audio data')
    def test_transcribe_audio_auth_error(self, mock_file, mock_validate, mock_watson_client):
        """Test transcribing audio with authentication error"""
        # Mock the client to raise an authentication error
        mock_watson_client.post_request.side_effect = AuthenticationError(
            "Authentication failed", "AUTHENTICATION_ERROR"
        )
        
        # Create the service
        service = STTService(mock_watson_client)
        
        # Mock os.path.exists to return True
        with patch('os.path.exists', return_value=True):
            # Call the method and expect exception
            with pytest.raises(AuthenticationError) as exc_info:
                service.transcribe_audio("test_audio.wav", "en-US_BroadbandModel")
        
        assert exc_info.value.code == "AUTHENTICATION_ERROR"
        mock_validate.assert_called_once()
        mock_file.assert_called_once()

    @patch('backend.validators.service_validator.ServiceValidator.validate_stt_params')
    @patch('builtins.open', new_callable=mock_open, read_data=b'mock audio data')
    def test_transcribe_audio_api_error(self, mock_file, mock_validate, mock_watson_client):
        """Test transcribing audio with API error"""
        # Mock the client to raise an API error
        mock_watson_client.post_request.side_effect = APIError(
            "API request failed", "API_ERROR"
        )
        
        # Create the service
        service = STTService(mock_watson_client)
        
        # Mock os.path.exists to return True
        with patch('os.path.exists', return_value=True):
            # Call the method and expect exception
            with pytest.raises(APIError) as exc_info:
                service.transcribe_audio("test_audio.wav", "en-US_BroadbandModel")
        
        assert exc_info.value.code == "API_ERROR"
        mock_validate.assert_called_once()
        mock_file.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_transcribe_audio_file_error(self, mock_file, mock_watson_client):
        """Test transcribing audio with file error"""
        # Mock open to raise an exception
        mock_file.side_effect = Exception("File error")
        
        # Create the service
        service = STTService(mock_watson_client)
        
        # Mock os.path.exists to return True
        with patch('os.path.exists', return_value=True):
            # Call the method and expect exception
            with pytest.raises(FileError) as exc_info:
                service.transcribe_audio("test_audio.wav", "en-US_BroadbandModel")
        
        assert exc_info.value.code == "FILE_READ_ERROR"
        mock_watson_client.post_request.assert_not_called()

    def test_get_models_success(self, mock_watson_client):
        """Test getting available models successfully"""
        # Mock the client's get_request method
        mock_response = {
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
                },
                {
                    "name": "de-DE_BroadbandModel",
                    "language": "de-DE",
                    "description": "German broadband model"
                }
            ]
        }
        mock_watson_client.get_request.return_value = mock_response
        
        # Create the service
        service = STTService(mock_watson_client)
        
        # Call the method
        result = service.get_models()
        
        # Assertions
        assert result == mock_response["models"]
        mock_watson_client.get_request.assert_called_once_with('/v1/models')

    def test_get_models_auth_error(self, mock_watson_client):
        """Test getting models with authentication error"""
        # Mock the client to raise an authentication error
        mock_watson_client.get_request.side_effect = AuthenticationError(
            "Authentication failed", "AUTHENTICATION_ERROR"
        )
        
        # Create the service
        service = STTService(mock_watson_client)
        
        # Call the method and expect exception
        with pytest.raises(AuthenticationError) as exc_info:
            service.get_models()
        
        assert exc_info.value.code == "AUTHENTICATION_ERROR"
        mock_watson_client.get_request.assert_called_once_with('/v1/models')

    def test_get_models_api_error(self, mock_watson_client):
        """Test getting models with API error"""
        # Mock the client to raise an API error
        mock_watson_client.get_request.side_effect = APIError(
            "API request failed", "API_ERROR"
        )
        
        # Create the service
        service = STTService(mock_watson_client)
        
        # Call the method and expect exception
        with pytest.raises(APIError) as exc_info:
            service.get_models()
        
        assert exc_info.value.code == "API_ERROR"
        mock_watson_client.get_request.assert_called_once_with('/v1/models')

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