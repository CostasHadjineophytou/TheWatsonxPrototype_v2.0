import pytest
from unittest.mock import patch, MagicMock, call

from backend.services.nlu_service import NLUService
from backend.utils.errors import ValidationError, AuthenticationError, APIError


class TestNLUService:
    """Tests for the NLUService class"""

    def test_init(self, mock_watson_client):
        """Test initializing the NLUService"""
        service = NLUService(mock_watson_client)
        assert service.client == mock_watson_client

    @patch('backend.validators.service_validator.ServiceValidator.validate_nlu_params')
    def test_analyze_text_success(self, mock_validate, mock_watson_client):
        """Test analyzing text successfully"""
        # Mock the client's post_request method
        mock_response = {
            'sentiment': {
                'document': {
                    'score': 0.8,
                    'label': 'positive'
                }
            },
            'entities': [
                {
                    'type': 'Person',
                    'text': 'John Doe',
                    'relevance': 0.9
                }
            ]
        }
        mock_watson_client.post_request.return_value = mock_response
        
        # Create the service
        service = NLUService(mock_watson_client)
        
        # Parameters for analysis
        text = "John Doe is a great person to work with."
        features = {
            'sentiment': {},
            'entities': {}
        }
        
        # Call the method
        result = service.analyze_text(text, features)
        
        # Assertions
        assert result == mock_response
        mock_validate.assert_called_once()
        mock_watson_client.post_request.assert_called_once()
        # Check that the first argument to post_request is the correct endpoint
        args, _ = mock_watson_client.post_request.call_args
        assert args[0] == '/v1/analyze'

    def test_analyze_text_empty_text(self, mock_watson_client):
        """Test analyzing with empty text"""
        # Create the service
        service = NLUService(mock_watson_client)
        
        # Call the method with empty text and expect exception
        with pytest.raises(ValidationError) as exc_info:
            service.analyze_text("", {'sentiment': {}})
        
        assert exc_info.value.code == "INVALID_TEXT"
        mock_watson_client.post_request.assert_not_called()

    def test_analyze_text_no_features(self, mock_watson_client):
        """Test analyzing with no features"""
        # Create the service
        service = NLUService(mock_watson_client)
        
        # Call the method with no features and expect exception
        with pytest.raises(ValidationError) as exc_info:
            service.analyze_text("Sample text", {})
        
        assert exc_info.value.code == "INVALID_FEATURES"
        mock_watson_client.post_request.assert_not_called()

    @patch('backend.validators.service_validator.ServiceValidator.validate_nlu_params')
    def test_analyze_text_validation_error(self, mock_validate, mock_watson_client):
        """Test analyzing text with validation error"""
        # Mock the validator to raise a validation error
        mock_validate.side_effect = ValidationError(
            "Invalid parameters", "INVALID_PARAMS"
        )
        
        # Create the service
        service = NLUService(mock_watson_client)
        
        # Call the method and expect exception
        with pytest.raises(ValidationError) as exc_info:
            service.analyze_text("Sample text", {'sentiment': {}})
        
        assert exc_info.value.code == "INVALID_PARAMS"
        mock_watson_client.post_request.assert_not_called()

    @patch('backend.validators.service_validator.ServiceValidator.validate_nlu_params')
    def test_analyze_text_auth_error(self, mock_validate, mock_watson_client):
        """Test analyzing text with authentication error"""
        # Mock the client to raise an authentication error
        mock_watson_client.post_request.side_effect = AuthenticationError(
            "Authentication failed", "AUTHENTICATION_ERROR"
        )
        
        # Create the service
        service = NLUService(mock_watson_client)
        
        # Call the method and expect exception
        with pytest.raises(AuthenticationError) as exc_info:
            service.analyze_text("Sample text", {'sentiment': {}})
        
        assert exc_info.value.code == "AUTHENTICATION_ERROR"
        mock_validate.assert_called_once()

    @patch('backend.validators.service_validator.ServiceValidator.validate_nlu_params')
    def test_analyze_text_api_error(self, mock_validate, mock_watson_client):
        """Test analyzing text with API error"""
        # Mock the client to raise an API error
        mock_watson_client.post_request.side_effect = APIError(
            "API request failed", "API_ERROR"
        )
        
        # Create the service
        service = NLUService(mock_watson_client)
        
        # Call the method and expect exception
        with pytest.raises(APIError) as exc_info:
            service.analyze_text("Sample text", {'sentiment': {}})
        
        assert exc_info.value.code == "API_ERROR"
        mock_validate.assert_called_once()

    @patch('backend.validators.service_validator.ServiceValidator.validate_nlu_params')
    def test_analyze_text_with_url_success(self, mock_validate, mock_watson_client):
        """Test analyzing text from URL successfully"""
        # Mock the client's post_request method
        mock_response = {
            'sentiment': {
                'document': {
                    'score': 0.6,
                    'label': 'positive'
                }
            },
            'concepts': [
                {
                    'text': 'Artificial Intelligence',
                    'relevance': 0.95
                }
            ]
        }
        mock_watson_client.post_request.return_value = mock_response
        
        # Create the service
        service = NLUService(mock_watson_client)
        
        # Parameters for analysis
        url = "https://example.com/article"
        features = {
            'sentiment': {},
            'concepts': {}
        }
        
        # Call the method
        result = service.analyze_url(url, features)
        
        # Assertions
        assert result == mock_response
        mock_validate.assert_called_once()
        mock_watson_client.post_request.assert_called_once()
        # Check that the first argument to post_request is the correct endpoint
        args, _ = mock_watson_client.post_request.call_args
        assert args[0] == '/v1/analyze'
        # Check that the payload contains the URL instead of text
        _, kwargs = mock_watson_client.post_request.call_args
        assert 'url' in kwargs['json']
        assert kwargs['json']['url'] == url

    def test_analyze_url_empty_url(self, mock_watson_client):
        """Test analyzing with empty URL"""
        # Create the service
        service = NLUService(mock_watson_client)
        
        # Call the method with empty URL and expect exception
        with pytest.raises(ValidationError) as exc_info:
            service.analyze_url("", {'sentiment': {}})
        
        assert exc_info.value.code == "INVALID_URL"
        mock_watson_client.post_request.assert_not_called()

    def test_analyze_url_invalid_url(self, mock_watson_client):
        """Test analyzing with invalid URL"""
        # Create the service
        service = NLUService(mock_watson_client)
        
        # Call the method with invalid URL and expect exception
        with pytest.raises(ValidationError) as exc_info:
            service.analyze_url("not-a-valid-url", {'sentiment': {}})
        
        assert exc_info.value.code == "INVALID_URL"
        mock_watson_client.post_request.assert_not_called()

    @patch('backend.validators.service_validator.ServiceValidator.validate_nlu_params')
    def test_analyze_url_api_error(self, mock_validate, mock_watson_client):
        """Test analyzing URL with API error"""
        # Mock the client to raise an API error
        mock_watson_client.post_request.side_effect = APIError(
            "API request failed", "API_ERROR"
        )
        
        # Create the service
        service = NLUService(mock_watson_client)
        
        # Call the method and expect exception
        with pytest.raises(APIError) as exc_info:
            service.analyze_url("https://example.com", {'sentiment': {}})
        
        assert exc_info.value.code == "API_ERROR"
        mock_validate.assert_called_once() 