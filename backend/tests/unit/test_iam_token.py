import pytest
from unittest.mock import patch, MagicMock, call
import time
import json

from backend.services.iam_token import IAMTokenService
from backend.utils.errors import ValidationError, AuthenticationError, APIError, ConfigurationError
from backend.config.config import Config


class TestIAMTokenService:
    """Tests for the IAMTokenService class"""

    @pytest.fixture
    def mock_iam_service(self):
        """Create a mock IAM token service for testing"""
        with patch('backend.services.iam_token.BaseClient.__init__', return_value=None):
            service = IAMTokenService()
            service.api_key = "test_api_key"
            service.token_url = Config.IAM_TOKEN_URL
            service.validator = MagicMock()
            # Don't mock _make_request here, we'll patch it in each test
            return service

    def test_init(self):
        """Test initializing the IAMTokenService"""
        with patch('backend.services.iam_token.BaseClient.__init__', return_value=None) as mock_init:
            service = IAMTokenService()
            mock_init.assert_called_once()
            assert service.token_url == Config.IAM_TOKEN_URL

    def test_get_iam_token_success(self, mock_iam_service):
        """Test getting an IAM token successfully"""
        # Mock the response from the IAM API
        mock_response = {
            "access_token": "mock_token_value",
            "token_type": "Bearer",
            "expires_in": 3600,
            "expiration": int(time.time()) + 3600
        }
        
        # Patch the _make_request method directly on the service instance
        mock_iam_service._make_request = MagicMock(return_value=mock_response)
        
        # Call the method
        token = mock_iam_service.get_iam_token()
        
        # Assertions
        assert token == "mock_token_value"
        
        # Verify validator was called
        mock_iam_service.validator.validate_credentials.assert_called_once_with({"api_key": "test_api_key"})
        
        # Verify _make_request was called with correct parameters
        mock_iam_service._make_request.assert_called_once()
        args, kwargs = mock_iam_service._make_request.call_args
        assert kwargs["method"] == "POST"
        assert kwargs["url"] == Config.IAM_TOKEN_URL
        assert "Content-Type" in kwargs["headers"]
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        assert "grant_type" in kwargs["data"]
        assert kwargs["data"]["grant_type"] == "urn:ibm:params:oauth:grant-type:apikey"
        assert "apikey" in kwargs["data"]
        assert kwargs["data"]["apikey"] == "test_api_key"
        assert kwargs["is_form_data"] is True

    def test_get_iam_token_no_token_in_response(self, mock_iam_service):
        """Test getting an IAM token with no token in response"""
        # Mock the response from the IAM API with no access_token
        mock_response = {
            "token_type": "Bearer",
            "expires_in": 3600,
            "expiration": int(time.time()) + 3600
        }
        
        # Patch the _make_request method directly on the service instance
        mock_iam_service._make_request = MagicMock(return_value=mock_response)
        
        # Call the method and expect exception
        with pytest.raises(AuthenticationError) as exc_info:
            mock_iam_service.get_iam_token()
        
        assert exc_info.value.code == "NO_TOKEN"
        assert "No access token in response" in str(exc_info.value)
        
        # Verify validator was called
        mock_iam_service.validator.validate_credentials.assert_called_once_with({"api_key": "test_api_key"})

    def test_get_iam_token_validation_error(self, mock_iam_service):
        """Test getting an IAM token with validation error"""
        # Mock the validator to raise a validation error
        mock_iam_service.validator.validate_credentials.side_effect = ValidationError(
            "Invalid API key", "INVALID_API_KEY"
        )
        
        # Call the method and expect exception
        with pytest.raises(ValidationError) as exc_info:
            mock_iam_service.get_iam_token()
        
        assert exc_info.value.code == "INVALID_API_KEY"
        assert "Invalid API key" in str(exc_info.value)
        
        # Verify validator was called
        mock_iam_service.validator.validate_credentials.assert_called_once_with({"api_key": "test_api_key"})

    def test_get_iam_token_authentication_error(self, mock_iam_service):
        """Test getting an IAM token with authentication error"""
        # Mock _make_request to raise an authentication error
        mock_iam_service._make_request = MagicMock(side_effect=AuthenticationError(
            "Authentication failed", "AUTH_ERROR"
        ))
        
        # Call the method and expect exception
        with pytest.raises(AuthenticationError) as exc_info:
            mock_iam_service.get_iam_token()
        
        assert exc_info.value.code == "AUTH_ERROR"
        assert "Authentication failed" in str(exc_info.value)
        
        # Verify validator was called
        mock_iam_service.validator.validate_credentials.assert_called_once_with({"api_key": "test_api_key"})

    def test_get_iam_token_api_error(self, mock_iam_service):
        """Test getting an IAM token with API error"""
        # Mock _make_request to raise an API error
        mock_iam_service._make_request = MagicMock(side_effect=APIError(
            "API request failed", "API_ERROR"
        ))
        
        # Call the method and expect exception
        with pytest.raises(APIError) as exc_info:
            mock_iam_service.get_iam_token()
        
        assert exc_info.value.code == "API_ERROR"
        assert "API request failed" in str(exc_info.value)
        
        # Verify validator was called
        mock_iam_service.validator.validate_credentials.assert_called_once_with({"api_key": "test_api_key"})

    def test_get_iam_token_generic_exception(self, mock_iam_service):
        """Test getting an IAM token with a generic exception"""
        # Mock _make_request to raise a generic exception
        mock_iam_service._make_request = MagicMock(side_effect=Exception("Unknown error"))
        
        # Mock handle_error to return a specific error
        mock_iam_service.handle_error = MagicMock(return_value=APIError(
            "Failed to get IAM token", "IAM_ERROR"
        ))
        
        # Call the method and expect exception
        with pytest.raises(APIError) as exc_info:
            mock_iam_service.get_iam_token()
        
        assert exc_info.value.code == "IAM_ERROR"
        assert "Failed to get IAM token" in str(exc_info.value)
        
        # Verify validator was called
        mock_iam_service.validator.validate_credentials.assert_called_once_with({"api_key": "test_api_key"})
        
        # Verify handle_error was called
        mock_iam_service.handle_error.assert_called_once()
        args, kwargs = mock_iam_service.handle_error.call_args
        assert isinstance(args[0], Exception)
        assert args[1] == "Failed to get IAM token" 