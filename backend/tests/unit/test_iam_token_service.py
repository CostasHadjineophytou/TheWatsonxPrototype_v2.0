import pytest
from unittest.mock import patch, MagicMock, call
import time

from backend.services.iam_token import IAMTokenService
from backend.utils.errors import AuthenticationError, APIError


class TestIAMTokenService:
    """Tests for the IAMTokenService class"""

    def test_init(self):
        """Test initializing the IAMTokenService"""
        service = IAMTokenService()
        
        assert service.token is None
        assert service.expiration == 0

    @patch('requests.post')
    def test_get_token_first_time(self, mock_post):
        """Test getting a token for the first time"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'test_token',
            'expiration': int(time.time()) + 3600  # 1 hour from now
        }
        mock_post.return_value = mock_response
        
        # Create the service
        service = IAMTokenService()
        
        # Call the method
        credentials = {'api_key': 'test_api_key'}
        token = service.get_token(credentials)
        
        # Assertions
        assert token == 'test_token'
        assert service.token == 'test_token'
        assert service.expiration > int(time.time())
        
        # Verify the request was made
        mock_post.assert_called_once_with(
            'https://iam.cloud.ibm.com/identity/token',
            data={
                'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
                'apikey': 'test_api_key'
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

    @patch('requests.post')
    def test_get_token_cached(self, mock_post):
        """Test getting a cached token that hasn't expired"""
        # Create the service and set a token that hasn't expired
        service = IAMTokenService()
        service.token = 'cached_token'
        service.expiration = int(time.time()) + 1800  # 30 minutes from now
        
        # Call the method
        credentials = {'api_key': 'test_api_key'}
        token = service.get_token(credentials)
        
        # Assertions
        assert token == 'cached_token'
        
        # Verify no request was made (using cached token)
        mock_post.assert_not_called()

    @patch('requests.post')
    def test_get_token_expired(self, mock_post):
        """Test getting a token when the cached one has expired"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'new_token',
            'expiration': int(time.time()) + 3600  # 1 hour from now
        }
        mock_post.return_value = mock_response
        
        # Create the service and set an expired token
        service = IAMTokenService()
        service.token = 'expired_token'
        service.expiration = int(time.time()) - 100  # Expired 100 seconds ago
        
        # Call the method
        credentials = {'api_key': 'test_api_key'}
        token = service.get_token(credentials)
        
        # Assertions
        assert token == 'new_token'
        assert service.token == 'new_token'
        assert service.expiration > int(time.time())
        
        # Verify the request was made
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_get_token_no_credentials(self, mock_post):
        """Test getting a token with no credentials"""
        # Create the service
        service = IAMTokenService()
        
        # Call the method and expect exception
        with pytest.raises(AuthenticationError) as exc_info:
            service.get_token(None)
        
        assert exc_info.value.code == "NO_CREDENTIALS"
        assert "No credentials provided" in exc_info.value.message
        
        # Verify no request was made
        mock_post.assert_not_called()

    @patch('requests.post')
    def test_get_token_no_api_key(self, mock_post):
        """Test getting a token with credentials missing API key"""
        # Create the service
        service = IAMTokenService()
        
        # Call the method and expect exception
        credentials = {'url': 'https://test-url.com'}  # No API key
        
        with pytest.raises(AuthenticationError) as exc_info:
            service.get_token(credentials)
        
        assert exc_info.value.code == "NO_API_KEY"
        assert "API key is required" in exc_info.value.message
        
        # Verify no request was made
        mock_post.assert_not_called()

    @patch('requests.post')
    def test_get_token_auth_error(self, mock_post):
        """Test getting a token with authentication error"""
        # Mock the response for auth error
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {'error': 'Unauthorized'}
        mock_post.return_value = mock_response
        
        # Create the service
        service = IAMTokenService()
        
        # Call the method and expect exception
        credentials = {'api_key': 'invalid_api_key'}
        
        with pytest.raises(AuthenticationError) as exc_info:
            service.get_token(credentials)
        
        assert exc_info.value.code == "AUTHENTICATION_ERROR"
        assert "Failed to authenticate with IBM Cloud" in exc_info.value.message
        
        # Verify the request was made
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_get_token_api_error(self, mock_post):
        """Test getting a token with API error"""
        # Mock the response for API error
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {'error': 'Internal Server Error'}
        mock_post.return_value = mock_response
        
        # Create the service
        service = IAMTokenService()
        
        # Call the method and expect exception
        credentials = {'api_key': 'test_api_key'}
        
        with pytest.raises(APIError) as exc_info:
            service.get_token(credentials)
        
        assert exc_info.value.code == "API_ERROR"
        assert "Failed to get IAM token" in exc_info.value.message
        
        # Verify the request was made
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_get_token_connection_error(self, mock_post):
        """Test getting a token with connection error"""
        # Mock post to raise ConnectionError
        mock_post.side_effect = ConnectionError("Connection failed")
        
        # Create the service
        service = IAMTokenService()
        
        # Call the method and expect exception
        credentials = {'api_key': 'test_api_key'}
        
        with pytest.raises(APIError) as exc_info:
            service.get_token(credentials)
        
        assert exc_info.value.code == "CONNECTION_ERROR"
        assert "Failed to connect to IAM service" in exc_info.value.message
        
        # Verify the request was attempted
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_get_token_missing_access_token(self, mock_post):
        """Test getting a token with missing access_token in response"""
        # Mock the response with missing access_token
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'expiration': int(time.time()) + 3600  # No access_token
        }
        mock_post.return_value = mock_response
        
        # Create the service
        service = IAMTokenService()
        
        # Call the method and expect exception
        credentials = {'api_key': 'test_api_key'}
        
        with pytest.raises(APIError) as exc_info:
            service.get_token(credentials)
        
        assert exc_info.value.code == "INVALID_RESPONSE"
        assert "Invalid response from IAM service" in exc_info.value.message
        
        # Verify the request was made
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_get_token_missing_expiration(self, mock_post):
        """Test getting a token with missing expiration in response"""
        # Mock the response with missing expiration
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'test_token'  # No expiration
        }
        mock_post.return_value = mock_response
        
        # Create the service
        service = IAMTokenService()
        
        # Call the method and expect exception
        credentials = {'api_key': 'test_api_key'}
        
        with pytest.raises(APIError) as exc_info:
            service.get_token(credentials)
        
        assert exc_info.value.code == "INVALID_RESPONSE"
        assert "Invalid response from IAM service" in exc_info.value.message
        
        # Verify the request was made
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_get_token_refresh_before_expiry(self, mock_post):
        """Test getting a token that's close to expiry (should refresh)"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'new_token',
            'expiration': int(time.time()) + 3600  # 1 hour from now
        }
        mock_post.return_value = mock_response
        
        # Create the service and set a token that's close to expiry
        service = IAMTokenService()
        service.token = 'almost_expired_token'
        service.expiration = int(time.time()) + 60  # Expires in 60 seconds
        
        # Call the method
        credentials = {'api_key': 'test_api_key'}
        token = service.get_token(credentials)
        
        # Assertions
        assert token == 'new_token'
        assert service.token == 'new_token'
        
        # Verify the request was made (token refreshed)
        mock_post.assert_called_once() 