import pytest
from unittest.mock import patch, MagicMock

from backend.services.service_factory import ServiceFactory
from backend.services.text_service import TextService
from backend.services.iam_token import IAMTokenService
from backend.utils.errors import ValidationError, AuthenticationError, APIError


class TestTextGenerationFlow:
    """Integration tests for the text generation flow"""
    
    @pytest.fixture
    def mock_credentials_manager(self):
        """Mock credentials manager for testing"""
        mock_manager = MagicMock()
        mock_manager.get_service_credentials.return_value = {
            "apikey": "test_api_key",
            "url": "https://test.watsonx.ai/api"
        }
        return mock_manager
    
    @pytest.fixture
    def mock_iam_token_service(self):
        """Mock IAM token service for testing"""
        mock_service = MagicMock(spec=IAMTokenService)
        mock_service.get_token.return_value = "mock_token"
        return mock_service
    
    @pytest.fixture
    def service_factory(self, mock_credentials_manager, mock_iam_token_service):
        """Create a service factory with mocked dependencies"""
        return ServiceFactory(mock_credentials_manager, mock_iam_token_service)
    
    @patch('backend.services.watson_client.WatsonClient.post_request')
    def test_text_generation_success(self, mock_post_request, service_factory):
        """Test successful text generation flow"""
        # Mock response from the Watson API
        mock_response = {
            "generated_text": "This is a test response from the model.",
            "model_id": "ibm/granite-20b-multilingual",
            "created_at": "2023-07-15T10:30:45Z"
        }
        mock_post_request.return_value = mock_response
        
        # Create the text service
        text_service = service_factory.create_text_service()
        
        # Test parameters
        model_id = "ibm/granite-20b-multilingual"
        prompt = "Generate a test response"
        params = {
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        # Call the generate_text method
        result = text_service.generate_text(model_id, prompt, params)
        
        # Assertions
        assert result == mock_response
        mock_post_request.assert_called_once()
        # Check that the endpoint is correct
        args, _ = mock_post_request.call_args
        assert "/v1/text/generation" in args[0]
        # Check that the payload contains the expected data
        _, kwargs = mock_post_request.call_args
        assert kwargs['json']['model_id'] == model_id
        assert kwargs['json']['input'] == prompt
        assert kwargs['json']['parameters']['max_tokens'] == params['max_tokens']
        assert kwargs['json']['parameters']['temperature'] == params['temperature']
    
    @patch('backend.services.watson_client.WatsonClient.post_request')
    def test_text_generation_validation_error(self, mock_post_request, service_factory):
        """Test text generation with validation error"""
        # Create the text service
        text_service = service_factory.create_text_service()
        
        # Test with invalid parameters
        model_id = ""  # Empty model ID should cause validation error
        prompt = "Generate a test response"
        params = {
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        # Call the method and expect exception
        with pytest.raises(ValidationError) as exc_info:
            text_service.generate_text(model_id, prompt, params)
        
        assert exc_info.value.code == "INVALID_MODEL_ID"
        mock_post_request.assert_not_called()
    
    @patch('backend.services.watson_client.WatsonClient.post_request')
    def test_text_generation_auth_error(self, mock_post_request, service_factory):
        """Test text generation with authentication error"""
        # Mock the post_request to raise an authentication error
        mock_post_request.side_effect = AuthenticationError(
            "Authentication failed", "AUTHENTICATION_ERROR"
        )
        
        # Create the text service
        text_service = service_factory.create_text_service()
        
        # Test parameters
        model_id = "ibm/granite-20b-multilingual"
        prompt = "Generate a test response"
        params = {
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        # Call the method and expect exception
        with pytest.raises(AuthenticationError) as exc_info:
            text_service.generate_text(model_id, prompt, params)
        
        assert exc_info.value.code == "AUTHENTICATION_ERROR"
        mock_post_request.assert_called_once()
    
    @patch('backend.services.watson_client.WatsonClient.post_request')
    def test_text_generation_api_error(self, mock_post_request, service_factory):
        """Test text generation with API error"""
        # Mock the post_request to raise an API error
        mock_post_request.side_effect = APIError(
            "API request failed", "API_ERROR"
        )
        
        # Create the text service
        text_service = service_factory.create_text_service()
        
        # Test parameters
        model_id = "ibm/granite-20b-multilingual"
        prompt = "Generate a test response"
        params = {
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        # Call the method and expect exception
        with pytest.raises(APIError) as exc_info:
            text_service.generate_text(model_id, prompt, params)
        
        assert exc_info.value.code == "API_ERROR"
        mock_post_request.assert_called_once()
    
    @patch('backend.services.watson_client.WatsonClient.post_request')
    def test_text_generation_with_default_params(self, mock_post_request, service_factory):
        """Test text generation with default parameters"""
        # Mock response from the Watson API
        mock_response = {
            "generated_text": "This is a test response from the model.",
            "model_id": "ibm/granite-20b-multilingual",
            "created_at": "2023-07-15T10:30:45Z"
        }
        mock_post_request.return_value = mock_response
        
        # Create the text service
        text_service = service_factory.create_text_service()
        
        # Test parameters
        model_id = "ibm/granite-20b-multilingual"
        prompt = "Generate a test response"
        # No params provided, should use defaults
        
        # Call the generate_text method
        result = text_service.generate_text(model_id, prompt)
        
        # Assertions
        assert result == mock_response
        mock_post_request.assert_called_once()
        # Check that the payload contains default parameters
        _, kwargs = mock_post_request.call_args
        assert 'parameters' in kwargs['json'] 