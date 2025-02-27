import pytest
from unittest.mock import patch, MagicMock, call
import time
import json

from backend.services.iam_token import IAMTokenService
from backend.utils.errors import ValidationError, AuthenticationError, APIError, ConfigurationError


class TestIAMTokenService:
    """Tests for the IAMTokenService class"""

    @pytest.fixture
    def mock_credentials_manager(self):
        """Mock credentials manager for testing"""
        mock_manager = MagicMock()
        mock_manager.get_service_credentials.return_value = {
            "apikey": "test_api_key",
            "url": "https://iam.cloud.ibm.com/identity/token"
        }
        return mock_manager

    def test_init(self, mock_credentials_manager):
        """Test initializing the IAMTokenService"""
        service = IAMTokenService(mock_credentials_manager)
        assert service.credentials_manager == mock_credentials_manager
        assert service._token is None
        assert service._expiration == 0

    def test_init_missing_credentials(self):
        """Test initializing with missing credentials"""
        # Create a mock credentials manager that returns None
        mock_manager = MagicMock()
        mock_manager.get_service_credentials.return_value = None
        
        # Expect exception when initializing
        with pytest.raises(ConfigurationError) as exc_info:
            IAMTokenService(mock_manager)
        
        assert exc_info.value.code == "MISSING_CREDENTIALS"

    def test_init_missing_apikey(self):
        """Test initializing with missing API key"""
        # Create a mock credentials manager that returns credentials without apikey
        mock_manager = MagicMock()
        mock_manager.get_service_credentials.return_value = {
            "url": "https://iam.cloud.ibm.com/identity/token"
        }
        
        # Expect exception when initializing
        with pytest.raises(ConfigurationError) as exc_info:
            IAMTokenService(mock_manager)
        
        assert exc_info.value.code == "MISSING_API_KEY"

    @patch('requests.post')
    def test_get_token_first_time(self, mock_post, mock_credentials_manager):
        """Test getting a token for the first time"""
        # Mock the response from the IAM API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "mock_token_value",
            "token_type": "Bearer",
            "expires_in": 3600,
            "expiration": int(time.time()) + 3600
        }
        mock_post.return_value = mock_response
        
        # Create the service
        service = IAMTokenService(mock_credentials_manager)
        
        # Call the method
        token = service.get_token()
        
        # Assertions
        assert token == "mock_token_value"
        assert service._token == "mock_token_value"
        assert service._expiration > 0
        mock_post.assert_called_once()
        # Check that the request was made with the correct parameters
        args, kwargs = mock_post.call_args
        assert args[0] == "https://iam.cloud.ibm.com/identity/token"
        assert "grant_type=urn:ibm:params:oauth:grant-type:apikey" in kwargs["data"]
        assert "apikey=test_api_key" in kwargs["data"]

    @patch('requests.post')
    def test_get_token_cached(self, mock_post, mock_credentials_manager):
        """Test getting a cached token"""
        # Set up the service with a cached token
        service = IAMTokenService(mock_credentials_manager)
        service._token = "cached_token"
        service._expiration = int(time.time()) + 1800  # Token expires in 30 minutes
        
        # Call the method
        token = service.get_token()
        
        # Assertions
        assert token == "cached_token"
        # The post method should not be called since we have a valid cached token
        mock_post.assert_not_called()

    @patch('requests.post')
    def test_get_token_expired(self, mock_post, mock_credentials_manager):
        """Test getting a token when the cached one is expired"""
        # Mock the response from the IAM API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "new_token_value",
            "token_type": "Bearer",
            "expires_in": 3600,
            "expiration": int(time.time()) + 3600
        }
        mock_post.return_value = mock_response
        
        # Set up the service with an expired token
        service = IAMTokenService(mock_credentials_manager)
        service._token = "expired_token"
        service._expiration = int(time.time()) - 100  # Token expired 100 seconds ago
        
        # Call the method
        token = service.get_token()
        
        # Assertions
        assert token == "new_token_value"
        assert service._token == "new_token_value"
        assert service._expiration > int(time.time())
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_get_token_auth_error(self, mock_post, mock_credentials_manager):
        """Test getting a token with authentication error"""
        # Mock the response from the IAM API with an error
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "errorCode": "BXNIM0415E",
            "errorMessage": "Provided API key could not be found"
        }
        mock_post.return_value = mock_response
        
        # Create the service
        service = IAMTokenService(mock_credentials_manager)
        
        # Call the method and expect exception
        with pytest.raises(AuthenticationError) as exc_info:
            service.get_token()
        
        assert exc_info.value.code == "INVALID_API_KEY"
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_get_token_server_error(self, mock_post, mock_credentials_manager):
        """Test getting a token with server error"""
        # Mock the response from the IAM API with a server error
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "errorCode": "INTERNAL_SERVER_ERROR",
            "errorMessage": "Internal server error"
        }
        mock_post.return_value = mock_response
        
        # Create the service
        service = IAMTokenService(mock_credentials_manager)
        
        # Call the method and expect exception
        with pytest.raises(APIError) as exc_info:
            service.get_token()
        
        assert exc_info.value.code == "IAM_SERVICE_ERROR"
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_get_token_connection_error(self, mock_post, mock_credentials_manager):
        """Test getting a token with connection error"""
        # Mock the post method to raise a connection error
        mock_post.side_effect = Exception("Connection error")
        
        # Create the service
        service = IAMTokenService(mock_credentials_manager)
        
        # Call the method and expect exception
        with pytest.raises(APIError) as exc_info:
            service.get_token()
        
        assert exc_info.value.code == "IAM_CONNECTION_ERROR"
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_refresh_token(self, mock_post, mock_credentials_manager):
        """Test explicitly refreshing a token"""
        # Mock the response from the IAM API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "refreshed_token_value",
            "token_type": "Bearer",
            "expires_in": 3600,
            "expiration": int(time.time()) + 3600
        }
        mock_post.return_value = mock_response
        
        # Set up the service with a valid token
        service = IAMTokenService(mock_credentials_manager)
        service._token = "old_token"
        service._expiration = int(time.time()) + 1800  # Token still valid for 30 minutes
        
        # Call the refresh method
        service.refresh_token()
        
        # Assertions
        assert service._token == "refreshed_token_value"
        assert service._expiration > int(time.time())
        mock_post.assert_called_once()

    def test_is_token_valid_with_valid_token(self, mock_credentials_manager):
        """Test checking if a token is valid when it is"""
        # Set up the service with a valid token
        service = IAMTokenService(mock_credentials_manager)
        service._token = "valid_token"
        service._expiration = int(time.time()) + 1800  # Token valid for 30 minutes
        
        # Check if the token is valid
        assert service.is_token_valid() is True

    def test_is_token_valid_with_expired_token(self, mock_credentials_manager):
        """Test checking if a token is valid when it is expired"""
        # Set up the service with an expired token
        service = IAMTokenService(mock_credentials_manager)
        service._token = "expired_token"
        service._expiration = int(time.time()) - 100  # Token expired 100 seconds ago
        
        # Check if the token is valid
        assert service.is_token_valid() is False

    def test_is_token_valid_with_no_token(self, mock_credentials_manager):
        """Test checking if a token is valid when none exists"""
        # Set up the service with no token
        service = IAMTokenService(mock_credentials_manager)
        service._token = None
        service._expiration = 0
        
        # Check if the token is valid
        assert service.is_token_valid() is False

    def test_is_token_valid_near_expiration(self, mock_credentials_manager):
        """Test checking if a token is valid when it's close to expiration"""
        # Set up the service with a token that's about to expire
        service = IAMTokenService(mock_credentials_manager)
        service._token = "almost_expired_token"
        service._expiration = int(time.time()) + 50  # Token expires in 50 seconds
        
        # Check if the token is valid (should be False since it's within the buffer time)
        assert service.is_token_valid() is False 